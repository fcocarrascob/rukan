"""Rukan — la escena: lo que un visor necesita para dibujar, en JSON.

Es la versión numérica de `vista.escena()`, que solo sabe llegar a SVG. Esquema
``rukan/escena@2``:

    esquema, proyecto, sha256_proyecto, rukan, commit, openseespy, generado
    titulo, unidades
    nudos[]        {id, nombre, xyz[3], fijo[6]?}
    barras[]       {id, nombre, i, j, seccion, vecxz[3]}
    masas[]        {nudo, m[3]}
    modos[]        {n, T, participacion{X,Y,Z}, phi[n_nudos][3]}
    casos          {nombre: {u[n_nudos][6], reacciones{nudo: [6]},
                             fuerzas[n_barras][12], w[n_barras][3]?}}
    combinaciones  {nombre: lo mismo}

Reglas:

* **La misma procedencia que los resultados** (`io.cabecera`): el hash del
  proyecto va adentro, y el sitio falla el build si no coincide.
* **Todos los casos**, no solo los que alguna sonda cita: la escena es para
  mirar, y lo que no se corrió no se puede mirar.
* `phi` en el orden de `nudos`, normalizado a `max|phi| = 1`; el visor escala.
* `fuerzas` lleva el **signo del diagrama**, con `analysis.signo_diagrama`, que
  es la misma función que usan las sondas: no hay dos convenciones.
* `w` es la **carga de vano en ejes locales** de cada barra, `(wx, wy, wz)` —el
  orden de los ejes, no el de `eleLoad -beamUniform`, que es `(Wy, Wz, Wx)`—. Con
  ella y las seis primeras de `fuerzas` (el extremo i), `esfuerzos.esfuerzo`
  entrega el diagrama en cualquier punto: por eso la escena guarda **magnitudes
  primarias** en vez de muestrear el diagrama en n estaciones, que pesaría
  treinta y cinco veces más y sería una magnitud derivada. La clave se omite
  entera en los casos sin carga distribuida: la escena no gasta bytes en ceros.
* `vecxz` viaja con cada barra porque el visor necesita sus ejes locales para
  dibujar el diagrama normal al eje. Es dato del modelo, no derivado.
* Floats con `CIFRAS` cifras significativas, para que el galpón de 965 nudos
  quepa en un archivo razonable. Es una escena, no un resultado que se cita.
"""

from __future__ import annotations

import json
from pathlib import Path

import openseespy.opensees as ops

from . import analysis, io, loads
from .engine import build
from .io import COMPONENTES, ESQUEMA_ESCENA, UNIDADES_INTERNAS, Proyecto

CIFRAS = 7

_SIGNOS = [analysis.signo_diagrama(ext, c) for ext in ("i", "j") for c in COMPONENTES]


def _r(x: float) -> float:
    return float(f"{x:.{CIFRAS}g}") + 0.0      # `+ 0.0` mata el -0.0


def _rl(xs) -> list:
    return [_r(x) for x in xs]


def armar(p: Proyecto, ruta_proyecto: str | Path) -> dict:
    """Corre el modal (si el proyecto lo declara) y **todos** los casos, y
    devuelve la escena como dict plano listo para `json.dump`."""
    p.validar()
    m = p.model
    ids = [n.id for n in m.nodes]
    secciones = {s.id: s.nombre or str(s.id) for s in m.sections}
    doc: dict = {"esquema": ESQUEMA_ESCENA, **io.cabecera(ruta_proyecto),
                 "titulo": p.titulo, "unidades": dict(UNIDADES_INTERNAS)}
    nudos = []
    for n in m.nodes:
        x = {"id": n.id, "nombre": n.nombre, "xyz": _rl((n.x, n.y, n.z))}
        if any(n.restraints):
            x["fijo"] = [1 if r else 0 for r in n.restraints]
        nudos.append(x)
    doc["nudos"] = nudos
    doc["barras"] = [{"id": e.id, "nombre": e.nombre, "i": e.node_i, "j": e.node_j,
                      "seccion": secciones[e.section], "vecxz": _rl(e.vecxz)}
                     for e in m.elements]
    doc["masas"] = [{"nudo": nm.node, "m": _rl(nm.values[:3])} for nm in m.masses]

    doc["modos"] = []
    modal = p.analisis.get("modal")
    if modal:
        build(m)
        mr = analysis.modal(m, modal["n_modos"])
        for k, (T, part) in enumerate(zip(mr.periodos, mr.participacion), start=1):
            phi = [[ops.nodeEigenvector(n, k, c) for c in (1, 2, 3)] for n in ids]
            mx = max(abs(c) for v in phi for c in v) or 1.0
            doc["modos"].append({"n": k, "T": _r(T),
                                 "participacion": {d: _r(v) for d, v in part.items()},
                                 "phi": [_rl(c / mx for c in v) for v in phi]})

    apoyos = [n.id for n in m.nodes if any(n.restraints)]
    tags = [e.id for e in m.elements]
    extractores = {
        "u": lambda: [list(ops.nodeDisp(n)) for n in ids],
        "reacciones": lambda: {str(n): list(ops.nodeReaction(n)) for n in apoyos},
        "fuerzas": lambda: [[s * f for s, f in zip(_SIGNOS, ops.eleResponse(t, "localForces"))]
                            for t in tags],
    }
    crudos = {}
    for nombre, caso in p.casos.items():
        r = loads.run_static_case(m, analysis.aplicar(p, caso), extractores)
        cargas = analysis.cargas_de_vano(p, caso)
        if cargas:
            r["w"] = [list(cargas[e.id]) for e in m.elements]
        crudos[nombre] = r
    doc["casos"] = {nombre: _redondear(r) for nombre, r in crudos.items()}
    doc["combinaciones"] = {nombre: _redondear(_lineal(crudos, factores))
                            for nombre, factores in p.combinaciones.items()}
    return doc


def _lineal(casos: dict, factores: dict[str, float]) -> dict:
    """`Σ f_c · caso_c`, componente a componente, sobre `u`, `reacciones`,
    `fuerzas` y la carga de vano `w`. Que `w` se combine igual que lo demás no es
    una comodidad: es lo que hace que el diagrama de una combinación salga de la
    fórmula sin ningún caso especial."""
    base = casos[next(iter(factores))]
    out = {"u": [[0.0] * 6 for _ in base["u"]],
           "reacciones": {n: [0.0] * 6 for n in base["reacciones"]},
           "fuerzas": [[0.0] * 12 for _ in base["fuerzas"]]}
    if any("w" in casos[c] for c in factores):
        out["w"] = [[0.0] * 3 for _ in base["fuerzas"]]
    for c, f in factores.items():
        r = casos[c]
        for k, v in enumerate(r["u"]):
            out["u"][k] = [a + f * b for a, b in zip(out["u"][k], v)]
        for n, v in r["reacciones"].items():
            out["reacciones"][n] = [a + f * b for a, b in zip(out["reacciones"][n], v)]
        for k, v in enumerate(r["fuerzas"]):
            out["fuerzas"][k] = [a + f * b for a, b in zip(out["fuerzas"][k], v)]
        for k, v in enumerate(r.get("w", [])):
            out["w"][k] = [a + f * b for a, b in zip(out["w"][k], v)]
    return out


def _redondear(r: dict) -> dict:
    d = {"u": [_rl(v) for v in r["u"]],
         "reacciones": {n: _rl(v) for n, v in r["reacciones"].items()},
         "fuerzas": [_rl(v) for v in r["fuerzas"]]}
    if "w" in r:
        d["w"] = [_rl(v) for v in r["w"]]
    return d


def escribir(doc: dict, ruta: str | Path) -> None:
    with open(ruta, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, separators=(",", ":"))
        fh.write("\n")
