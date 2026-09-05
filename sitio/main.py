"""Los macros del sitio: las cifras de la prosa salen de la corrida, no del teclado.

`mkdocs-macros` carga este módulo y `define_env` registra las funciones que el
markdown invoca con `{{ … }}`. Sobre un **modelo** (`docs/modelos/<slug>/`):

    {{ r('galpon-grua', 'T_star_Y', 5) }}        → 0,24878
    {{ r('galpon-grua', 'T_star_Y', 5, unidad=True) }}  → 0,24878 s
    {{ r('galpon-grua', 'd_alero', 3, factor=1000) }}   → 0,066  (la prosa pone «mm»)
    {{ cociente('galpon-grua', 1.0, 'd_alero', 2) }}   → 15 047,57  (k = H/δ, un paso)
    {{ tabla_modos('galpon-grua', 6) }}          → tabla markdown desde la escena
    {{ procedencia('galpon-grua') }}             → «corrido con rukan 0.1.0 @ …»

Sobre un **eslabón de una serie** (`docs/series/<serie>/<NN-slug>/`, ver `serie.py`):

    {{ v('nch2369-galpon-grua/04', 'R_star_Y', 5) }}   → 5,00000  (sale, pasos, entra o caso)
    {{ ficha('nch2369-galpon-grua/04') }}              → las tablas Entra y Sale, con enlaces
    {{ tabla_serie('nch2369-galpon-grua') }}           → la tabla de eslabones del índice
    {{ grafo_serie('nch2369-galpon-grua') }}           → el grafo de herencias, en mermaid
    {{ figura('nch2369-galpon-grua/04', 'espectros', 'alt') }}  → ![alt](figs/espectros.svg)

Reglas:

* Un símbolo que no existe **rompe el build** nombrándolo.
* `procedencia` recalcula el SHA-256 del proyecto y lo compara con el que
  traen resultados y escena: si alguien tocó el modelo sin recorrerlo, el sitio
  no se construye. Es la frescura por hash del repo de memos, sin arnés aparte.
* Coma decimal y espacio de miles, como en los memos. En la ficha, cada valor se
  escribe con los decimales que el memo original publicó (`publicado`), que es
  la precisión que ese eslabón prometió.

Las funciones toman `raiz` (la carpeta que contiene `docs/`) para poder
probarse sin MkDocs; `define_env` la fija a `env.project_dir`.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import serie as S  # noqa: E402

fmt = S.fmt


# ============================ modelos ================================
def _carpeta(raiz: Path, modelo: str) -> Path:
    d = Path(raiz) / "docs" / "modelos" / modelo
    if not d.is_dir():
        raise FileNotFoundError(f"no existe el modelo {modelo!r} en docs/modelos/")
    return d


def _leer(raiz: Path, modelo: str, cual: str) -> dict:
    ruta = _carpeta(raiz, modelo) / f"{modelo}.{cual}.json"
    if not ruta.exists():
        raise FileNotFoundError(f"falta {ruta.name}: corre `python -m rukan "
                                f"{cual if cual == 'escena' else 'run'}`")
    return json.loads(ruta.read_text(encoding="utf-8"))


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


# ============================ series =================================
def _eslabon(raiz: Path, ref: str) -> tuple[str, str, dict]:
    """`"nch2369-galpon-grua/04"` → (serie, nn, valores)."""
    if "/" not in ref:
        raise ValueError(f"el eslabón se escribe 'serie/NN', vino {ref!r}")
    serie_id, nn = ref.split("/", 1)
    return serie_id, nn, S.cargar(raiz, serie_id, nn)


def _buscar(d: dict, simbolo: str) -> dict | None:
    if simbolo in d["sale"]:
        return d["sale"][simbolo]
    for paso in d["pasos"].values():
        if simbolo in paso:
            return paso[simbolo]
    if simbolo in d["entra"]:
        return d["entra"][simbolo]
    if simbolo in d["caso"]:
        return d["caso"][simbolo]
    return None


def v(raiz: Path, eslabon: str, simbolo: str, cifras: int | None = None,
      factor: float = 1.0, unidad: bool = False) -> str:
    """La cifra de un símbolo del eslabón: en `sale`, `pasos`, `entra` o `caso`,
    en ese orden."""
    serie_id, nn, d = _eslabon(raiz, eslabon)
    x = _buscar(d, simbolo)
    if x is None:
        raise KeyError(f"{simbolo!r} no existe en el eslabón {nn} de {serie_id} "
                       f"(sale: {', '.join(d['sale'])})")
    s = fmt(factor * x["valor"], cifras)
    if unidad and factor == 1.0 and x.get("unidad") and x["unidad"] != "—":
        s = f"{s} {x['unidad']}"
    return s


def _como_publicado(d: dict, simbolo: str, valor_: float) -> str:
    """El valor con los decimales que el memo publicó; si no hay publicado,
    con los que el float trae."""
    pub = d.get("publicado", {}).get(simbolo)
    dec = S.decimales(pub) if pub is not None else S.decimales(valor_)
    return fmt(valor_, dec)


def _carpeta_de(raiz: Path, serie_id: str, nn: str) -> str:
    return S.carpeta_eslabon(raiz, serie_id, nn).name


def ficha(raiz: Path, eslabon: str) -> str:
    """La ficha de contrato: qué entra (y de dónde), qué sale (y de qué paso, y
    quién lo hereda), y la procedencia del JSON."""
    serie_id, nn, d = _eslabon(raiz, eslabon)
    out = [f"**Entra** — lo que este eslabón toma de otros, o del caso.", "",
           "| Símbolo | Valor | Unidad | De |", "|---|---:|---|---|"]
    for simbolo, x in d["entra"].items():
        de = x["de"]
        if de.startswith("modelo:"):
            slug = de[len("modelo:"):]
            origen = f"modelo [{slug}](../../../modelos/{slug}/)"
            texto = fmt(x["valor"], S.decimales(x["valor"]))
        else:
            origen = f"[{de}](../{_carpeta_de(raiz, serie_id, de)}/)"
            texto = _como_publicado(S.cargar(raiz, serie_id, de), simbolo, x["valor"])
        paso = f" · {x['paso']}" if x.get("paso") else ""
        out.append(f"| `{simbolo}` | {texto} | {x['unidad']} | {origen}{paso} |")
    for simbolo, x in d["caso"].items():
        out.append(f"| `{simbolo}` | {fmt(x['valor'], S.decimales(x['valor']))} | "
                   f"{x['unidad']} | caso |")
    out += ["", f"**Sale** — lo que este eslabón publica, y el paso en que nace.", "",
            "| Símbolo | Valor | Unidad | Nace en | Lo heredan |", "|---|---:|---|---|---|"]
    for simbolo, x in d["sale"].items():
        her = " · ".join(f"[{h}](../{_carpeta_de(raiz, serie_id, h)}/)" for h in x["heredan"]) \
            or "—"
        out.append(f"| `{simbolo}` | {_como_publicado(d, simbolo, x['valor'])} | "
                   f"{x['unidad']} | {x['paso']} | {her} |")
    out += ["", f"Esquema `{d['esquema']}` · generado {d.get('generado', '—')} · "
                f"rukan {d.get('rukan')} @ {d.get('commit')} · `_calculo.py` reproduce este "
                f"JSON y un test lo comprueba."]
    return "\n".join(out)


def tabla_serie(raiz: Path, serie_id: str) -> str:
    filas = ["| # | Eslabón | Normas | Salidas |", "|---:|---|---|---:|"]
    for e in S.eslabones(raiz, serie_id):
        carpeta = S.carpeta_eslabon(raiz, serie_id, e["_nn"]).name
        filas.append(f"| {e['orden']} | [{e['titulo']}]({carpeta}/) | "
                     f"{', '.join(e['normas'])} | {len(e['sale'])} |")
    return "\n".join(filas)


def grafo_serie(raiz: Path, serie_id: str) -> str:
    """El grafo de herencias, como `verify_serie.js --mermaid`: un nodo por
    eslabón, una arista por par origen → consumidor con hasta tres símbolos."""
    es = S.eslabones(raiz, serie_id)
    lineas = ["```mermaid", "graph TD"]
    for e in es:
        lineas.append(f'  E{e["_nn"]}["{e["_nn"]} · {e["titulo"]}"]')
    modelos: set[str] = set()
    aristas: dict[tuple[str, str], list[str]] = {}
    for e in es:
        for simbolo, x in e["entra"].items():
            de = x["de"]
            if de.startswith("modelo:"):
                slug = de[len("modelo:"):]
                modelos.add(slug)
                aristas.setdefault((f"M_{slug}", f"E{e['_nn']}"), []).append(simbolo)
            else:
                aristas.setdefault((f"E{de}", f"E{e['_nn']}"), []).append(simbolo)
    for slug in sorted(modelos):
        lineas.append(f'  M_{slug}(["modelo {slug}"])')
    for (a, b), simbolos in aristas.items():
        rotulo = ", ".join(simbolos[:3]) + (", …" if len(simbolos) > 3 else "")
        lineas.append(f"  {a} -->|{rotulo}| {b}")
    lineas.append("```")
    return "\n".join(lineas)


def figura(raiz: Path, eslabon: str, nombre: str, alt: str) -> str:
    serie_id, nn, _ = _eslabon(raiz, eslabon)
    ruta = S.carpeta_eslabon(raiz, serie_id, nn) / "figs" / f"{nombre}.svg"
    if not ruta.exists():
        raise FileNotFoundError(f"no existe la figura {nombre!r} del eslabón {nn}: "
                                f"falta {ruta}; corre _figuras.py")
    return f"![{alt}](figs/{nombre}.svg)"


# ============================ mkdocs-macros ==========================
def define_env(env) -> None:
    raiz = Path(env.project_dir)
    env.macro(lambda modelo, simbolo, cifras=None, unidad=False, factor=1.0:
              r(raiz, modelo, simbolo, cifras, unidad, factor), "r")
    env.macro(lambda modelo, numerador, simbolo, cifras=None:
              cociente(raiz, modelo, numerador, simbolo, cifras), "cociente")
    env.macro(lambda modelo, n=None: tabla_modos(raiz, modelo, n), "tabla_modos")
    env.macro(lambda modelo: procedencia(raiz, modelo), "procedencia")
    env.macro(lambda eslabon, simbolo, cifras=None, factor=1.0, unidad=False:
              v(raiz, eslabon, simbolo, cifras, factor, unidad), "v")
    env.macro(lambda eslabon: ficha(raiz, eslabon), "ficha")
    env.macro(lambda serie_id: tabla_serie(raiz, serie_id), "tabla_serie")
    env.macro(lambda serie_id: grafo_serie(raiz, serie_id), "grafo_serie")
    env.macro(lambda eslabon, nombre, alt: figura(raiz, eslabon, nombre, alt), "figura")
