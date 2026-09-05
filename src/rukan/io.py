"""Rukan — el archivo de proyecto: modelo + casos + análisis + salidas, en JSON.

Es el documento que un memo cita, que `python -m rukan run` corre y que una GUI
editará. Esquema ``rukan/proyecto@1``:

    esquema, titulo, unidades, origen
    materiales[]  {id, E, nu, rho}
    secciones[]   {id, nombre, A, Iy, Iz, J}
    nudos[]       {id, nombre, x, y, z, fijo[6]}
    barras[]      {id, nombre, i, j, material, seccion, vecxz[3], libera{z_i,z_j,y_i,y_j}}
    masas[]       {nudo, valores[6]}
    casos         {nombre: {peso_propio: distribuido|nodal, nodales: [{nudo, F[6]}]}}
    combinaciones {nombre: {caso: factor}}
    analisis      {modal: {n_modos}}
    salidas       {simbolo: {que, ...}}

Tres reglas que no son de forma:

1. **Las salidas son magnitudes primarias del análisis** —un período, un
   desplazamiento bajo un caso con nombre, una reacción, una fuerza de barra—.
   Nada derivado: `k = H/δ` es un paso escrito en el memo que lo consume, igual
   que cualquier conversión (`SERIES.md` § 4 del repo de memos).
2. **`nudo` y `barra` aceptan nombre o id** en `masas`, `casos` y `salidas`, y
   `i`/`j`/`material`/`seccion` de una barra también. `to_dict` escribe siempre
   ids y deja el nombre en `nombre`, así el archivo no tiene dos formas de decir
   lo mismo.
3. **Pint solo en la frontera.** `unidades` declara el sistema del archivo; si
   no es el interno (m, kN, t), `from_dict` convierte con `units.py` y el núcleo
   nunca ve otra cosa. `to_dict` escribe siempre el interno.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import units as u
from .model import DOF, FrameElement, Material, Model, NodalMass, Node, Section

ESQUEMA_PROYECTO = "rukan/proyecto@1"
ESQUEMA_RESULTADOS = "rukan/resultados@1"
ESQUEMA_ESCENA = "rukan/escena@1"
UNIDADES_INTERNAS = {"longitud": "m", "fuerza": "kN", "masa": "t"}

DIRECCIONES = ("X", "Y", "Z")
COMPONENTES = ("N", "Vy", "Vz", "T", "My", "Mz")
EXTREMOS = ("i", "j")
PESO_PROPIO = ("distribuido", "nodal")
ANALISIS = ("modal",)
# Qué campos exige cada sonda, además de `que`.
SONDAS: dict[str, tuple[str, ...]] = {
    "periodo": ("modo",),
    "periodo_dominante": ("direccion",),
    "participacion_dominante": ("direccion",),
    "masa_acumulada": ("direccion",),
    "desplazamiento": ("nudo", "gdl", "caso"),
    "reaccion": ("nudo", "gdl", "caso"),
    "fuerza": ("barra", "extremo", "componente", "caso"),
    "peso_total": (),
}
SONDAS_MODALES = ("periodo", "periodo_dominante", "participacion_dominante",
                  "masa_acumulada")
SONDAS_ESTATICAS = ("desplazamiento", "reaccion", "fuerza")

_CLAVES = ("esquema", "titulo", "unidades", "origen", "materiales", "secciones",
           "nudos", "barras", "masas", "casos", "combinaciones", "analisis", "salidas")


class ErrorDeEsquema(ValueError):
    """El archivo no cumple el esquema. El mensaje nombra el campo que falla."""


@dataclass
class Proyecto:
    model: Model
    titulo: str = ""
    casos: dict[str, dict] = field(default_factory=dict)
    combinaciones: dict[str, dict[str, float]] = field(default_factory=dict)
    analisis: dict[str, dict] = field(default_factory=dict)
    salidas: dict[str, dict] = field(default_factory=dict)
    origen: dict[str, Any] = field(default_factory=dict)

    # --- resolución nombre -> id -------------------------------------------
    def nudo_id(self, ref: int | str) -> int:
        return _resolver(self.model.nodes, ref, "nudo")

    def barra_id(self, ref: int | str) -> int:
        return _resolver(self.model.elements, ref, "barra")

    def validar(self) -> None:
        """Lanza `ErrorDeEsquema` si casos, combinaciones, análisis o salidas
        no cierran contra el modelo."""
        _validar_modelo(self.model)
        _validar_casos(self)
        _validar_combinaciones(self)
        _validar_analisis(self)
        _validar_salidas(self)


def _resolver(items, ref, que: str) -> int:
    if isinstance(ref, bool) or not isinstance(ref, (int, str)):
        raise ErrorDeEsquema(f"{que}: referencia inválida {ref!r}")
    if isinstance(ref, int):
        if any(it.id == ref for it in items):
            return ref
        raise ErrorDeEsquema(f"{que}: no existe el id {ref}")
    for it in items:
        if it.nombre == ref:
            return it.id
    raise ErrorDeEsquema(f"{que}: no existe el nombre {ref!r}")


# ============================ VALIDACIÓN ==============================
def _unicos(items, coleccion: str) -> None:
    ids: set[int] = set()
    nombres: set[str] = set()
    for it in items:
        if it.id in ids:
            raise ErrorDeEsquema(f"{coleccion}: id {it.id} repetido")
        ids.add(it.id)
        nm = getattr(it, "nombre", "")
        if nm:
            if nm in nombres:
                raise ErrorDeEsquema(f"{coleccion}: nombre {nm!r} repetido")
            nombres.add(nm)


def _validar_modelo(m: Model) -> None:
    _unicos(m.nodes, "nudos")
    _unicos(m.materials, "materiales")
    _unicos(m.sections, "secciones")
    _unicos(m.elements, "barras")
    nudos = {n.id for n in m.nodes}
    mats = {x.id for x in m.materials}
    secs = {s.id for s in m.sections}
    for e in m.elements:
        for campo, ref, ok in (("i", e.node_i, nudos), ("j", e.node_j, nudos),
                               ("material", e.material, mats),
                               ("seccion", e.section, secs)):
            if ref not in ok:
                raise ErrorDeEsquema(f"barras: la barra {e.id} apunta a {campo} = {ref}"
                                     " que no existe")
        if len(e.vecxz) != 3:
            raise ErrorDeEsquema(f"barras: vecxz de la barra {e.id} no tiene 3 componentes")
    for nm in m.masses:
        if nm.node not in nudos:
            raise ErrorDeEsquema(f"masas: el nudo {nm.node} no existe")
        if len(nm.values) != 6:
            raise ErrorDeEsquema(f"masas: valores del nudo {nm.node} no tiene 6 componentes")


def _validar_casos(p: Proyecto) -> None:
    for nombre, caso in p.casos.items():
        if not isinstance(caso, dict):
            raise ErrorDeEsquema(f"casos: {nombre!r} no es un objeto")
        for k in caso:
            if k not in ("peso_propio", "nodales"):
                raise ErrorDeEsquema(f"casos: {nombre!r} trae la clave {k!r}, que no existe")
        pp = caso.get("peso_propio")
        if pp is not None and pp not in PESO_PROPIO:
            raise ErrorDeEsquema(f"casos: peso_propio de {nombre!r} es {pp!r}; "
                                 f"vale {' | '.join(PESO_PROPIO)}")
        for carga in caso.get("nodales", []):
            if set(carga) != {"nudo", "F"}:
                raise ErrorDeEsquema(f"casos: cada carga nodal de {nombre!r} lleva "
                                     "exactamente `nudo` y `F`")
            try:
                p.nudo_id(carga["nudo"])
            except ErrorDeEsquema as exc:
                raise ErrorDeEsquema(f"casos: {nombre!r}: {exc}") from None
            if len(carga["F"]) != 6:
                raise ErrorDeEsquema(f"casos: F de {nombre!r} no tiene 6 componentes")


def _validar_combinaciones(p: Proyecto) -> None:
    for nombre, factores in p.combinaciones.items():
        if not isinstance(factores, dict) or not factores:
            raise ErrorDeEsquema(f"combinaciones: {nombre!r} no es {{caso: factor}}")
        for caso in factores:
            if caso not in p.casos:
                raise ErrorDeEsquema(f"combinaciones: {nombre!r} usa el caso {caso!r}, "
                                     "que no está en `casos`")


def _validar_analisis(p: Proyecto) -> None:
    for k in p.analisis:
        if k not in ANALISIS:
            raise ErrorDeEsquema(f"analisis: {k!r} no existe en este esquema; "
                                 f"vale {' | '.join(ANALISIS)}")
    modal = p.analisis.get("modal")
    if modal is not None:
        n = modal.get("n_modos")
        if not isinstance(n, int) or isinstance(n, bool) or n < 1:
            raise ErrorDeEsquema("analisis: modal.n_modos debe ser un entero >= 1")
        for k in modal:
            if k != "n_modos":
                raise ErrorDeEsquema(f"analisis: modal trae la clave {k!r}, que no existe")


def _validar_salidas(p: Proyecto) -> None:
    n_modos = p.analisis.get("modal", {}).get("n_modos")
    for simbolo, s in p.salidas.items():
        pre = f"salidas: {simbolo!r}"
        if not isinstance(s, dict) or "que" not in s:
            raise ErrorDeEsquema(f"{pre} no trae `que`")
        que = s["que"]
        if que not in SONDAS:
            raise ErrorDeEsquema(f"{pre}: que = {que!r} no existe; "
                                 f"vale {' | '.join(SONDAS)}")
        faltan = [c for c in SONDAS[que] if c not in s]
        if faltan:
            raise ErrorDeEsquema(f"{pre} ({que}) no trae {', '.join(faltan)}")
        sobran = [c for c in s if c != "que" and c not in SONDAS[que]]
        if sobran:
            raise ErrorDeEsquema(f"{pre} ({que}) trae {', '.join(sobran)}, que no aplica")
        if que in SONDAS_MODALES and n_modos is None:
            raise ErrorDeEsquema(f"{pre} ({que}) necesita `analisis.modal`")
        if "modo" in s:
            k = s["modo"]
            if not isinstance(k, int) or isinstance(k, bool) or not 1 <= k <= n_modos:
                raise ErrorDeEsquema(f"{pre}: modo = {k!r} no está entre 1 y {n_modos}")
        if "direccion" in s and s["direccion"] not in DIRECCIONES:
            raise ErrorDeEsquema(f"{pre}: direccion = {s['direccion']!r}; vale X | Y | Z")
        if "gdl" in s and s["gdl"] not in DOF:
            raise ErrorDeEsquema(f"{pre}: gdl = {s['gdl']!r}; vale {' | '.join(DOF)}")
        if "componente" in s and s["componente"] not in COMPONENTES:
            raise ErrorDeEsquema(f"{pre}: componente = {s['componente']!r}; "
                                 f"vale {' | '.join(COMPONENTES)}")
        if "extremo" in s and s["extremo"] not in EXTREMOS:
            raise ErrorDeEsquema(f"{pre}: extremo = {s['extremo']!r}; vale i | j")
        if "caso" in s and s["caso"] not in p.casos and s["caso"] not in p.combinaciones:
            raise ErrorDeEsquema(f"{pre}: caso = {s['caso']!r} no es un caso ni una "
                                 "combinación")
        try:
            if "nudo" in s:
                p.nudo_id(s["nudo"])
            if "barra" in s:
                p.barra_id(s["barra"])
        except ErrorDeEsquema as exc:
            raise ErrorDeEsquema(f"{pre}: {exc}") from None


# ============================ UNIDADES ================================
def _factores(unidades: dict) -> tuple[float, float, float]:
    """`(fL, fF, fM)`: cuánto vale 1 unidad del archivo en el sistema interno."""
    for k in ("longitud", "fuerza", "masa"):
        if k not in unidades:
            raise ErrorDeEsquema(f"unidades: falta {k!r}")
    try:
        fL = u.length(1.0 * u.ureg(unidades["longitud"]))
        fF = u.force(1.0 * u.ureg(unidades["fuerza"]))
        fM = u.mass(1.0 * u.ureg(unidades["masa"]))
    except Exception as exc:  # pint: UndefinedUnitError, DimensionalityError
        raise ErrorDeEsquema(f"unidades: no se reconoce {unidades!r} ({exc})") from None
    return fL, fF, fM


# ============================ DICT -> PROYECTO ========================
def _campo(d: dict, k: str, donde: str):
    if k not in d:
        raise ErrorDeEsquema(f"{donde}: falta {k!r}")
    return d[k]


def _num(d: dict, k: str, donde: str, factor: float = 1.0) -> float:
    v = _campo(d, k, donde)
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ErrorDeEsquema(f"{donde}: {k!r} = {v!r} no es un número")
    return float(v) * factor


def _seis(d: dict, k: str, donde: str, factores=(1.0,) * 6):
    v = _campo(d, k, donde)
    if not isinstance(v, (list, tuple)) or len(v) != 6:
        raise ErrorDeEsquema(f"{donde}: {k!r} no tiene 6 componentes")
    return tuple(float(x) * f for x, f in zip(v, factores))


def _ref_en(lista: list[dict], ref, campo: str, donde: str) -> int:
    """Resuelve `ref` (id o nombre) contra una lista de dicts ya leídos."""
    if isinstance(ref, bool) or not isinstance(ref, (int, str)):
        raise ErrorDeEsquema(f"{donde}: {campo} = {ref!r} no es id ni nombre")
    for it in lista:
        if (isinstance(ref, int) and it["id"] == ref) or \
           (isinstance(ref, str) and it.get("nombre", "") == ref):
            return it["id"]
    raise ErrorDeEsquema(f"{donde}: {campo} = {ref!r} no existe")


def from_dict(d: dict) -> Proyecto:
    """Construye y **valida** el proyecto. Convierte unidades en la frontera."""
    if not isinstance(d, dict) or d.get("esquema") != ESQUEMA_PROYECTO:
        raise ErrorDeEsquema(f"esquema: se esperaba {ESQUEMA_PROYECTO!r}, "
                             f"vino {d.get('esquema') if isinstance(d, dict) else d!r}")
    for k in d:
        if k not in _CLAVES:
            raise ErrorDeEsquema(f"{k!r} no es una clave del esquema")
    fL, fF, fM = _factores(d.get("unidades", UNIDADES_INTERNAS))

    mats = [Material(id=int(_campo(x, "id", "materiales")),
                     E=_num(x, "E", "materiales", fF / fL ** 2),
                     nu=_num(x, "nu", "materiales"),
                     rho=_num(x, "rho", "materiales", fM / fL ** 3) if "rho" in x else 0.0)
            for x in d.get("materiales", [])]
    secs_d = d.get("secciones", [])
    secs = [Section(id=int(_campo(x, "id", "secciones")),
                    A=_num(x, "A", "secciones", fL ** 2),
                    Iy=_num(x, "Iy", "secciones", fL ** 4),
                    Iz=_num(x, "Iz", "secciones", fL ** 4),
                    J=_num(x, "J", "secciones", fL ** 4),
                    nombre=str(x.get("nombre", "")))
            for x in secs_d]
    nudos_d = d.get("nudos", [])
    nudos = [Node(id=int(_campo(x, "id", "nudos")),
                  x=_num(x, "x", "nudos", fL), y=_num(x, "y", "nudos", fL),
                  z=_num(x, "z", "nudos", fL),
                  restraints=tuple(bool(r) for r in _seis(x, "fijo", "nudos"))
                  if "fijo" in x else (False,) * 6,
                  nombre=str(x.get("nombre", "")))
             for x in nudos_d]
    mats_d = d.get("materiales", [])
    barras = []
    for x in d.get("barras", []):
        donde = f"barras ({x.get('nombre') or x.get('id')})"
        lib = x.get("libera", {})
        for k in lib:
            if k not in ("z_i", "z_j", "y_i", "y_j"):
                raise ErrorDeEsquema(f"{donde}: libera trae {k!r}")
        barras.append(FrameElement(
            id=int(_campo(x, "id", "barras")),
            node_i=_ref_en(nudos_d, _campo(x, "i", donde), "i", donde),
            node_j=_ref_en(nudos_d, _campo(x, "j", donde), "j", donde),
            material=_ref_en(mats_d, _campo(x, "material", donde), "material", donde),
            section=_ref_en(secs_d, _campo(x, "seccion", donde), "seccion", donde),
            vecxz=tuple(float(v) for v in x.get("vecxz", (1.0, 0.0, 0.0))),
            release_z_i=bool(lib.get("z_i", False)), release_z_j=bool(lib.get("z_j", False)),
            release_y_i=bool(lib.get("y_i", False)), release_y_j=bool(lib.get("y_j", False)),
            nombre=str(x.get("nombre", ""))))
    fm = (fM,) * 3 + (fM * fL ** 2,) * 3
    masas = [NodalMass(node=_ref_en(nudos_d, _campo(x, "nudo", "masas"), "nudo", "masas"),
                       values=_seis(x, "valores", "masas", fm))
             for x in d.get("masas", [])]

    casos = copy.deepcopy(d.get("casos", {}))
    if (fF, fL) != (1.0, 1.0):
        ff = (fF,) * 3 + (fF * fL,) * 3
        for caso in casos.values():
            for carga in (caso.get("nodales", []) if isinstance(caso, dict) else []):
                if isinstance(carga.get("F"), (list, tuple)) and len(carga["F"]) == 6:
                    carga["F"] = [float(v) * f for v, f in zip(carga["F"], ff)]

    p = Proyecto(model=Model(nodes=nudos, materials=mats, sections=secs,
                             elements=barras, masses=masas),
                 titulo=str(d.get("titulo", "")), casos=casos,
                 combinaciones=copy.deepcopy(d.get("combinaciones", {})),
                 analisis=copy.deepcopy(d.get("analisis", {})),
                 salidas=copy.deepcopy(d.get("salidas", {})),
                 origen=copy.deepcopy(d.get("origen", {})))
    p.validar()
    return p


# ============================ PROYECTO -> DICT ========================
def to_dict(p: Proyecto) -> dict:
    """JSON plano, siempre en el sistema interno, ids en las referencias del
    modelo y el nombre en `nombre`. `casos`, `combinaciones`, `analisis` y
    `salidas` se copian como los escribió el autor."""
    m = p.model
    d: dict[str, Any] = {"esquema": ESQUEMA_PROYECTO}
    if p.titulo:
        d["titulo"] = p.titulo
    d["unidades"] = dict(UNIDADES_INTERNAS)
    if p.origen:
        d["origen"] = copy.deepcopy(p.origen)
    d["materiales"] = [{"id": x.id, "E": x.E, "nu": x.nu, "rho": x.rho} for x in m.materials]
    d["secciones"] = [_con_nombre({"id": s.id}, s.nombre)
                      | {"A": s.A, "Iy": s.Iy, "Iz": s.Iz, "J": s.J} for s in m.sections]
    nudos = []
    for n in m.nodes:
        x = _con_nombre({"id": n.id}, n.nombre) | {"x": n.x, "y": n.y, "z": n.z}
        if any(n.restraints):
            x["fijo"] = [1 if r else 0 for r in n.restraints]
        nudos.append(x)
    d["nudos"] = nudos
    barras = []
    for e in m.elements:
        x = _con_nombre({"id": e.id}, e.nombre) | {
            "i": e.node_i, "j": e.node_j, "material": e.material, "seccion": e.section,
            "vecxz": list(e.vecxz)}
        lib = {k: True for k, v in (("z_i", e.release_z_i), ("z_j", e.release_z_j),
                                    ("y_i", e.release_y_i), ("y_j", e.release_y_j)) if v}
        if lib:
            x["libera"] = lib
        barras.append(x)
    d["barras"] = barras
    d["masas"] = [{"nudo": nm.node, "valores": list(nm.values)} for nm in m.masses]
    d["casos"] = copy.deepcopy(p.casos)
    d["combinaciones"] = copy.deepcopy(p.combinaciones)
    d["analisis"] = copy.deepcopy(p.analisis)
    d["salidas"] = copy.deepcopy(p.salidas)
    return d


def _con_nombre(x: dict, nombre: str) -> dict:
    if nombre:
        x["nombre"] = nombre
    return x


# ============================ ARCHIVOS ================================
def load(ruta: str | Path) -> Proyecto:
    with open(ruta, encoding="utf-8") as fh:
        return from_dict(json.load(fh))


def save(p: Proyecto, ruta: str | Path) -> None:
    with open(ruta, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(to_dict(p), fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def sha256(ruta: str | Path) -> str:
    return hashlib.sha256(Path(ruta).read_bytes()).hexdigest()


def _stem(ruta_proyecto: str | Path) -> tuple[Path, str]:
    r = Path(ruta_proyecto)
    stem = r.name[:-len(".proyecto.json")] if r.name.endswith(".proyecto.json") \
        else r.stem
    return r, stem


def ruta_resultados(ruta_proyecto: str | Path) -> Path:
    """`x.proyecto.json` → `x.resultados.json`; `x.json` → `x.resultados.json`."""
    r, stem = _stem(ruta_proyecto)
    return r.with_name(stem + ".resultados.json")


def ruta_escena(ruta_proyecto: str | Path) -> Path:
    """`x.proyecto.json` → `x.escena.json`, la que dibuja el visor del sitio."""
    r, stem = _stem(ruta_proyecto)
    return r.with_name(stem + ".escena.json")


def cabecera(ruta_proyecto: str | Path) -> dict:
    """La procedencia que comparten resultados y escena: qué proyecto (por
    nombre **y** por hash), qué rukan, qué commit, qué openseespy, cuándo."""
    import datetime
    import subprocess
    from importlib import metadata

    from . import __version__

    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                                cwd=Path(__file__).resolve().parent,
                                capture_output=True, text=True, timeout=10
                                ).stdout.strip() or None
    except Exception:
        commit = None
    try:
        ops_version = metadata.version("openseespy")
    except metadata.PackageNotFoundError:
        ops_version = None
    return {
        "proyecto": Path(ruta_proyecto).name,
        "sha256_proyecto": sha256(ruta_proyecto),
        "rukan": __version__,
        "commit": commit,
        "openseespy": ops_version,
        "generado": datetime.datetime.now().isoformat(timespec="seconds"),
    }


def resultados(ruta_proyecto: str | Path, valores: dict[str, float],
               unidades: dict[str, str]) -> dict:
    """El documento de resultados. Es lo que `_kit/verify_modelo.py` del repo
    de memos cruza contra `## Sale`."""
    return {"esquema": ESQUEMA_RESULTADOS, **cabecera(ruta_proyecto),
            "unidades": dict(unidades), "valores": dict(valores)}
