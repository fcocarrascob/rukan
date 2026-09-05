"""Los macros del sitio: las cifras de la prosa salen de la corrida, no del teclado.

`mkdocs-macros` carga este módulo y `define_env` registra tres funciones que el
markdown invoca con `{{ … }}`:

    {{ r('galpon-grua', 'T_star_Y', 5) }}        → 0,24878
    {{ r('galpon-grua', 'T_star_Y', 5, unidad=True) }}  → 0,24878 s
    {{ r('galpon-grua', 'd_alero', 3, factor=1000) }}   → 0,067  (la prosa pone «mm»)
    {{ cociente('galpon-grua', 1.0, 'd_alero', 2) }}   → 15 025,19  (k = H/δ, un paso)
    {{ tabla_modos('galpon-grua', 6) }}          → tabla markdown desde la escena
    {{ procedencia('galpon-grua') }}             → «corrido con rukan 0.1.0 @ …»

Reglas:

* Un símbolo que no existe en `resultados.json` **rompe el build** nombrándolo.
* `procedencia` recalcula el SHA-256 del proyecto y lo compara con el que
  traen resultados y escena: si alguien tocó el modelo sin recorrerlo, el sitio
  no se construye. Es la frescura por hash del repo de memos, sin arnés aparte.
* Coma decimal y espacio de miles, como en los memos.

Las funciones toman `raiz` (la carpeta que contiene `docs/`) para poder
probarse sin MkDocs; `define_env` la fija a `env.project_dir`.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def _carpeta(raiz: Path, modelo: str) -> Path:
    d = Path(raiz) / "docs" / "modelos" / modelo
    if not d.is_dir():
        raise FileNotFoundError(f"no existe el modelo {modelo!r} en docs/modelos/")
    return d


def _leer(raiz: Path, modelo: str, cual: str) -> dict:
    ruta = _carpeta(raiz, modelo) / f"{modelo}.{cual}.json"
    if not ruta.exists():
        raise FileNotFoundError(f"falta {ruta.name}: corre `python -m rukan {cual if cual == 'escena' else 'run'}`")
    return json.loads(ruta.read_text(encoding="utf-8"))


def fmt(v: float, cifras: int | None = None) -> str:
    """`15047.5712, 2` → `15 047,57`; sin cifras, seis significativas tal cual."""
    s = f"{v:,.{cifras}f}" if cifras is not None else f"{v:.6g}"
    return s.replace(",", "\0").replace(".", ",").replace("\0", " ")


def valor(raiz: Path, modelo: str, simbolo: str) -> float:
    doc = _leer(raiz, modelo, "resultados")
    if simbolo not in doc["valores"]:
        raise KeyError(f"{simbolo!r} no es una salida de {modelo}.resultados.json "
                       f"(hay: {', '.join(doc['valores'])})")
    return doc["valores"][simbolo]


def r(raiz: Path, modelo: str, simbolo: str, cifras: int | None = None,
      unidad: bool = False, factor: float = 1.0) -> str:
    """La cifra de una salida. `factor` la reescala (1000 → mm, 100 → %); con
    factor la unidad la escribe la prosa, no el macro."""
    s = fmt(factor * valor(raiz, modelo, simbolo), cifras)
    if unidad and factor == 1.0:
        u = _leer(raiz, modelo, "resultados").get("unidades", {}).get(simbolo, "")
        if u and u != "—":
            s = f"{s} {u}"
    return s


def cociente(raiz: Path, modelo: str, numerador: float, simbolo: str,
             cifras: int | None = None) -> str:
    """`numerador / salida`: el paso `k = H/δ` que el memo escribe y que no es
    una salida del análisis."""
    return fmt(numerador / valor(raiz, modelo, simbolo), cifras)


def tabla_modos(raiz: Path, modelo: str, n: int | None = None) -> str:
    esc = _leer(raiz, modelo, "escena")
    modos = esc["modos"][:n] if n else esc["modos"]
    filas = ["| Modo | T (s) | X (%) | Y (%) | Z (%) |", "|---:|---:|---:|---:|---:|"]
    for m in modos:
        p = m["participacion"]
        filas.append(f"| {m['n']} | {fmt(m['T'], 4)} | {fmt(100 * p['X'], 1)} | "
                     f"{fmt(100 * p['Y'], 1)} | {fmt(100 * p['Z'], 1)} |")
    return "\n".join(filas)


def procedencia(raiz: Path, modelo: str) -> str:
    proyecto = _carpeta(raiz, modelo) / f"{modelo}.proyecto.json"
    sha = hashlib.sha256(proyecto.read_bytes()).hexdigest()
    res, esc = _leer(raiz, modelo, "resultados"), _leer(raiz, modelo, "escena")
    for nombre, doc in (("resultados", res), ("escena", esc)):
        if doc.get("sha256_proyecto") != sha:
            raise ValueError(f"{modelo}.{nombre}.json no es de {proyecto.name}: el proyecto "
                             f"cambió y no se recorrió (`python -m rukan run` y `escena`)")
    return (f"Corrido con rukan {res['rukan']} @ {res['commit']} · "
            f"openseespy {res['openseespy']} · {res['generado']} · "
            f"SHA-256 del proyecto `{sha[:12]}…`")


def define_env(env) -> None:
    raiz = Path(env.project_dir)
    env.macro(lambda modelo, simbolo, cifras=None, unidad=False, factor=1.0:
              r(raiz, modelo, simbolo, cifras, unidad, factor), "r")
    env.macro(lambda modelo, numerador, simbolo, cifras=None:
              cociente(raiz, modelo, numerador, simbolo, cifras), "cociente")
    env.macro(lambda modelo, n=None: tabla_modos(raiz, modelo, n), "tabla_modos")
    env.macro(lambda modelo: procedencia(raiz, modelo), "procedencia")
