"""Las figuras SVG de un eslabón, escritas a mano y con las cotas leídas del cálculo.

Portado de `_img/_figuras.py` del repo de memos, con una diferencia de fondo:
allá las cotas vivían en un dict `D` tecleado en el script y un arnés comprobaba
que existieran en el memo; acá `cotas(valores)` las lee del `valores.json` del
eslabón, así que ningún número nace en la capa de dibujo por construcción. El
test `cotas_sin_respaldo` (serie.py) sigue existiendo por si un script escribe
una cifra a mano.

Portabilidad, heredada: flechas como triángulos y no con `<marker>`; `viewBox`
siempre; fondo claro propio; ningún `<text>` rotado.

    from figuras import Figura, doc, rect, linea, txt, cota_h, cota_v, guia, encabezado
"""

from __future__ import annotations

import json
from pathlib import Path

TINTA, LINEA, COTA, ACERO, HORM, MORT, DESTAQUE, PERNO = (
    "#1b1b1b", "#5b5b5b", "#8a6d3b", "#d5d7da", "#e9e4d9", "#cfc6b4",
    "#a4442c", "#eceef0",
)
FUENTE = "ui-monospace, 'SF Mono', 'Cascadia Mono', Consolas, monospace"


def es(v: float, cifras: int = 2) -> str:
    """`25.0, 2` → `25,00`; `12903.49` → `12 903,49`. Coma decimal, espacio de miles."""
    s = f"{v:,.{cifras}f}"
    return s.replace(",", "\0").replace(".", ",").replace("\0", " ")


def cotas(carpeta: Path) -> dict[str, float]:
    """Todos los valores numéricos del eslabón (`caso`, `entra`, `pasos`, `sale`)
    en un dict plano símbolo → valor, para rotular con `es()`."""
    carpeta = Path(carpeta)
    ruta = next(carpeta.glob("*.valores.json"))
    d = json.loads(ruta.read_text(encoding="utf-8"))
    out: dict[str, float] = {}
    for grupo in ("caso", "entra", "sale"):
        for k, x in d.get(grupo, {}).items():
            out.setdefault(k, float(x["valor"]))
    for paso in d.get("pasos", {}).values():
        for k, x in paso.items():
            out.setdefault(k, float(x["valor"]))
    return out


def doc(w, h, cuerpo, titulo):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" role="img" aria-label="{titulo}">\n'
        f'<title>{titulo}</title>\n'
        f'<rect width="{w}" height="{h}" fill="#fcfcfa"/>\n'
        f'<g font-family="{FUENTE}" font-size="11" fill="{TINTA}" '
        f'stroke-linecap="round">\n{cuerpo}\n</g>\n</svg>\n'
    )


def rect(x, y, w, h, fill=ACERO, sw=1.2):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'fill="{fill}" stroke="{TINTA}" stroke-width="{sw}"/>')


def linea(x1, y1, x2, y2, c=LINEA, sw=1, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{c}" stroke-width="{sw}"{d}/>')


def txt(x, y, s, anchor="middle", c=TINTA, size=11, peso="400"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" fill="{c}" '
            f'font-size="{size}" font-weight="{peso}">{s}</text>')


def flecha(x, y1, y2, c=DESTAQUE, sw=2.4, cabeza=9):
    """Flecha vertical con la punta dibujada, no con un marker."""
    signo = 1 if y2 > y1 else -1
    return "\n".join([
        linea(x, y1, x, y2 - signo * cabeza * 0.6, c, sw),
        f'<path d="M {x:.1f} {y2:.1f} l {-cabeza*0.45:.1f} {-signo*cabeza:.1f} '
        f'l {cabeza*0.9:.1f} 0 z" fill="{c}"/>',
    ])


def cota_h(x1, x2, y, etiqueta, arriba=True, ext=None, dxlab=0):
    """Cota horizontal. `ext` = (y_desde) dibuja las líneas de extensión.
    `dxlab` corre el rótulo cuando el centro de la cota cae sobre el dibujo."""
    dy = -5 if arriba else 13
    p = []
    if ext is not None:
        p += [linea(x1, ext, x1, y, "#c9c4b8", 0.7, "3 3"),
              linea(x2, ext, x2, y, "#c9c4b8", 0.7, "3 3")]
    p += [linea(x1, y - 4, x1, y + 4, COTA),
          linea(x2, y - 4, x2, y + 4, COTA),
          linea(x1, y, x2, y, COTA),
          txt((x1 + x2) / 2 + dxlab, y + dy, etiqueta, c=COTA, size=10.5)]
    return "\n".join(p)


def cota_v(y1, y2, x, etiqueta, izq=True):
    dx = -6 if izq else 6
    anchor = "end" if izq else "start"
    return "\n".join([
        linea(x - 4, y1, x + 4, y1, COTA),
        linea(x - 4, y2, x + 4, y2, COTA),
        linea(x, y1, x, y2, COTA),
        txt(x + dx, (y1 + y2) / 2 + 4, etiqueta, anchor=anchor, c=COTA, size=10.5),
    ])


def guia(x1, y1, x2, y2, etiqueta, anchor="start"):
    return "\n".join([
        linea(x1, y1, x2, y2, COTA, 0.9),
        txt(x2 + (5 if anchor == "start" else -5), y2 + 3.5, etiqueta,
            anchor=anchor, c=COTA, size=10.5),
    ])


def encabezado(titulo, *sub):
    p = [txt(38, 30, titulo, anchor="start", size=12.5, peso="600")]
    for i, s in enumerate(sub):
        p.append(txt(38, 47 + i * 15, s, anchor="start", c=LINEA, size=10))
    return "\n".join(p)


def escribir(carpeta: Path, figuras: dict[str, str]) -> None:
    """Escribe `figs/<nombre>.svg` por cada par nombre → svg."""
    figs = Path(carpeta) / "figs"
    figs.mkdir(exist_ok=True)
    for nombre, svg in figuras.items():
        destino = figs / f"{nombre}.svg"
        destino.write_text(svg, encoding="utf-8", newline="\n")
        print(f"  ok  figs/{destino.name}  ({len(svg)} bytes)")
