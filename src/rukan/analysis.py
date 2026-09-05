"""Rukan — el runner del proyecto: corre lo que `analisis` y `casos` piden y
evalúa cada sonda de `salidas`.

Todo lo que hace ya existía repartido en los casos de verificación: el modal con
participación 3D es el de los casos 9 y 11, los casos estáticos son
`loads.run_static_case`, las combinaciones `loads.combine`. Lo nuevo es que
ahora lo declara un archivo y no un script por caso.

Convención de fuerzas de barra (`fuerza`)
-----------------------------------------
`ops.eleResponse(tag, "localForces")` da las **fuerzas nodales sobre la barra**
en cada extremo, ``[Pi, Vyi, Vzi, Ti, Myi, Mzi, Pj, ...]``. Lo que un memo cita
es el **diagrama** de esfuerzos internos, y el paso de una cosa a la otra es de
signo. La convención verificada contra SAP2000 en los casos 6, 9 y 10:

    N  (tracción +)   i: -Pi      j: +Pj
    My, Mz            i: +Mi      j: -Mj

Corte y torsión siguen la regla de las fuerzas (`i: -`, `j: +`) por analogía con
la axial; **no se han verificado contra SAP2000 todavía**. Lo que sí quedó
cerrado en la `nota07` del laboratorio es que el signo del **corte** no es una
elección: con `Mz` anclado en sus dos extremos a la convención de momento de
arriba, `dMz/dx = +Vy` y `dMy/dx = -Vz` lo determinan. La **torsión** es el único
componente sin diagrama del cual derivarse, y sigue esperando el caso de
verificación contra SAP2000 que `ROADMAP.md` encola.

Esfuerzos a lo largo de la barra (`esfuerzo`)
---------------------------------------------
`localForces` solo entrega los dos extremos: entre ellos no hay nada, y el
momento del vano no está. La sonda `esfuerzo` evalúa `esfuerzos.esfuerzo`, que
superpone la carga de vano del caso (`cargas_de_vano`) sobre esas fuerzas de
extremo. La estación se declara como `x` (metros desde el extremo i) o `x_rel`
(0 a 1). Como el esfuerzo a `x` fijo es **lineal** en el caso, las combinaciones
lo combinan como a cualquier otra respuesta.

Participación modal
-------------------
Como en los casos 9 y 11: `Γ_d² · M_gen / M_total,d`, con la masa generalizada
sumada en las tres traslaciones —la razón de masa participante que reporta SAP y
la que §5.4 de NCh2369 pide para elegir el modo dominante—. Las masas
rotacionales no entran.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

import openseespy.opensees as ops

from . import esfuerzos, loads
from .engine import build
from .io import DOF, SONDAS_ESTATICAS, SONDAS_MODALES, Proyecto
from .model import Model

_DIR = {"X": 0, "Y": 1, "Z": 2}
_COMP = {"N": 0, "Vy": 1, "Vz": 2, "T": 3, "My": 4, "Mz": 5}
_ES_MOMENTO_FLECTOR = {"My", "Mz"}


# ============================ MODAL ===================================
@dataclass
class ModalResult:
    periodos: list[float]                    # por modo, 1..n
    participacion: list[dict[str, float]]    # por modo, {"X":..,"Y":..,"Z":..}
    masa_total: dict[str, float]

    def dominante(self, direccion: str) -> int:
        """Índice **0-based** del modo con mayor participación en `direccion`."""
        return max(range(len(self.periodos)),
                   key=lambda k: self.participacion[k][direccion])

    def acumulada(self, direccion: str) -> float:
        return sum(p[direccion] for p in self.participacion)


def modal(model: Model, n_modos: int) -> ModalResult:
    """Modal del modelo **ya montado** (`engine.build`).

    Solver: `-fullGenLapack` en modelos chicos (donde ARPACK no puede pedir casi
    todos los modos) y el ARPACK por omisión de OpenSees en los grandes, que es
    el que corren los casos 9 a 11.
    """
    # Un `eigen` anterior en el mismo dominio deja un análisis sin EigenSOE y el
    # segundo falla con "no EigenSOE has been set": se limpia siempre.
    ops.wipeAnalysis()
    n_libres = sum(6 - sum(n.restraints) for n in model.nodes)
    if n_libres <= 200:
        ev = ops.eigen("-fullGenLapack", n_modos)
    else:
        ev = ops.eigen(n_modos)
    periodos = [2.0 * math.pi / math.sqrt(lam) for lam in ev]
    ment = [(nm.node, nm.values[:3]) for nm in model.masses]
    m_tot = {d: sum(m[k] for _, m in ment) for d, k in _DIR.items()}
    part = []
    for k in range(1, n_modos + 1):
        phi = {n: [ops.nodeEigenvector(n, k, c) for c in (1, 2, 3)] for n, _ in ment}
        mg = sum(m[c] * phi[n][c] ** 2 for n, m in ment for c in range(3))
        fila = {}
        for d, c in _DIR.items():
            if mg <= 0.0 or m_tot[d] <= 0.0:
                fila[d] = 0.0
            else:
                L = sum(m[c] * phi[n][c] for n, m in ment)
                fila[d] = L * L / mg / m_tot[d]
        part.append(fila)
    return ModalResult(periodos=periodos, participacion=part, masa_total=m_tot)


# ============================ ESTÁTICO ================================
def aplicar(p: Proyecto, caso: dict) -> Callable[[], None]:
    """El callable que carga un caso del proyecto con un `ops.pattern` activo."""
    model = p.model

    def aplicar() -> None:
        pp = caso.get("peso_propio")
        if pp == "distribuido":
            loads.self_weight_distributed(model)
        elif pp == "nodal":
            loads.self_weight_nodal(model)
        for carga in caso.get("nodales", []):
            ops.load(p.nudo_id(carga["nudo"]), *(float(v) for v in carga["F"]))
    return aplicar


def cargas_de_vano(p: Proyecto, caso: dict) -> dict[int, tuple[float, float, float]]:
    """La carga uniforme en ejes locales de cada barra en `caso`, ``{id: w}``.

    Solo el peso propio **distribuido** la produce: concentrado en los nudos no
    carga el vano, y las cargas nodales tampoco. Es lo que `esfuerzos` necesita
    para superponer sobre las fuerzas de extremo, y lo que la escena emite.
    """
    if caso.get("peso_propio") == "distribuido":
        return loads.uniform_local_loads(p.model)
    return {}


def _clave(p: Proyecto, s: dict) -> str:
    """La respuesta primaria que una sonda estática necesita, sin el caso."""
    que = s["que"]
    if que == "desplazamiento":
        return f"d|{p.nudo_id(s['nudo'])}|{s['gdl']}"
    if que == "reaccion":
        return f"r|{p.nudo_id(s['nudo'])}|{s['gdl']}"
    if que == "esfuerzo":
        largo = p.largo_barra(s["barra"])
        x = s["x"] if "x" in s else s["x_rel"] * largo
        return f"e|{p.barra_id(s['barra'])}|{s['componente']}|{x!r}|{largo!r}"
    return f"f|{p.barra_id(s['barra'])}|{s['extremo']}|{s['componente']}"


def _extractor(clave: str, cargas: dict[int, tuple[float, float, float]]
               ) -> Callable[[], float]:
    """El callable que lee una respuesta primaria del dominio ya resuelto.

    `cargas` son las de vano **del caso que se está corriendo**: una sonda
    `esfuerzo` las necesita para superponerlas sobre las fuerzas de extremo, y
    por eso los extractores se arman por caso y no una sola vez. Las
    combinaciones siguen siendo lineales sobre el resultado, que es exacto
    porque el esfuerzo a `x` fijo es lineal en el caso.
    """
    partes = clave.split("|")
    if partes[0] == "d":
        nid, dof = int(partes[1]), DOF.index(partes[2]) + 1
        return lambda: ops.nodeDisp(nid, dof)
    if partes[0] == "r":
        nid, dof = int(partes[1]), DOF.index(partes[2]) + 1
        return lambda: ops.nodeReaction(nid, dof)
    if partes[0] == "e":
        tag, comp = int(partes[1]), partes[2]
        x, largo = float(partes[3]), float(partes[4])
        w = cargas.get(tag)
        return lambda: esfuerzos.esfuerzo(ops.eleResponse(tag, "localForces"),
                                          w, largo, comp, x)
    tag, extremo, comp = int(partes[1]), partes[2], partes[3]
    idx = _COMP[comp] + (0 if extremo == "i" else 6)
    signo = signo_diagrama(extremo, comp)
    return lambda: signo * ops.eleResponse(tag, "localForces")[idx]


def signo_diagrama(extremo: str, componente: str) -> float:
    """Fuerza nodal sobre la barra → esfuerzo del diagrama (convención del
    docstring). Es la única definición: la escena y las sondas la comparten."""
    flector = componente in _ES_MOMENTO_FLECTOR
    if extremo == "i":
        return 1.0 if flector else -1.0
    return -1.0 if flector else 1.0


def _casos_usados(p: Proyecto) -> set[str]:
    usados: set[str] = set()
    for s in p.salidas.values():
        if s["que"] in SONDAS_ESTATICAS:
            c = s["caso"]
            usados |= set(p.combinaciones[c]) if c in p.combinaciones else {c}
    return usados


# ============================ EL RUNNER ===============================
def run(p: Proyecto) -> dict[str, float]:
    """Corre el proyecto y devuelve `{simbolo: valor}` para cada salida.

    Solo corre lo que alguna salida necesita: el modal si hay sondas modales, y
    cada caso estático si una sonda lo cita directo o a través de una combinación.
    """
    p.validar()
    model = p.model
    out: dict[str, float] = {}

    mr: ModalResult | None = None
    if any(s["que"] in SONDAS_MODALES for s in p.salidas.values()):
        build(model)
        mr = modal(model, p.analisis["modal"]["n_modos"])

    claves = sorted({_clave(p, s) for s in p.salidas.values()
                     if s["que"] in SONDAS_ESTATICAS})
    res_casos: dict[str, dict[str, float]] = {}
    for nombre in sorted(_casos_usados(p)):
        caso = p.casos[nombre]
        extractores = {c: _extractor(c, cargas_de_vano(p, caso)) for c in claves}
        res_casos[nombre] = loads.run_static_case(model, aplicar(p, caso),
                                                  extractores, rebuild=True)
    res_combos = {n: loads.combine(res_casos, f) for n, f in p.combinaciones.items()
                  if set(f) <= set(res_casos)}

    for simbolo, s in p.salidas.items():
        que = s["que"]
        if que == "periodo":
            out[simbolo] = mr.periodos[s["modo"] - 1]
        elif que == "periodo_dominante":
            out[simbolo] = mr.periodos[mr.dominante(s["direccion"])]
        elif que == "participacion_dominante":
            k = mr.dominante(s["direccion"])
            out[simbolo] = mr.participacion[k][s["direccion"]]
        elif que == "masa_acumulada":
            out[simbolo] = mr.acumulada(s["direccion"])
        elif que == "peso_total":
            out[simbolo] = loads.total_weight(model)
        else:
            c = s["caso"]
            fuente = res_casos[c] if c in res_casos else res_combos[c]
            out[simbolo] = fuente[_clave(p, s)]
    return out


def unidades(p: Proyecto) -> dict[str, str]:
    """La unidad de cada salida en el sistema interno, para el archivo de
    resultados. Los adimensionales van con `—`, como en las tablas de la serie."""
    u: dict[str, str] = {}
    for simbolo, s in p.salidas.items():
        que = s["que"]
        if que == "periodo" or que == "periodo_dominante":
            u[simbolo] = "s"
        elif que in ("participacion_dominante", "masa_acumulada"):
            u[simbolo] = "—"
        elif que == "peso_total":
            u[simbolo] = "kN"
        elif que == "desplazamiento":
            u[simbolo] = "m" if s["gdl"].startswith("U") else "rad"
        elif que == "reaccion":
            u[simbolo] = "kN" if s["gdl"].startswith("U") else "kN·m"
        else:
            u[simbolo] = "kN" if s["componente"] in ("N", "Vy", "Vz") else "kN·m"
    return u
