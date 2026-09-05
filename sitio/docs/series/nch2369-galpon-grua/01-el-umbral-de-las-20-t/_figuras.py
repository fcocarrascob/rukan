"""Las dos figuras del eslabón 01: la planta con los dos vanos libres y el
recorrido de la grúa, y la sección con la altura libre que §12.2.1 c) acota.

    python sitio/docs/series/nch2369-galpon-grua/01-el-umbral-de-las-20-t/_figuras.py

Portado de `_img/_figuras-nch2369-galpon-grua-01.py` del repo de memos. Las
cotas se leen del `valores.json` del eslabón (`figuras.cotas`), no se teclean.
La figura no ilustra: comprueba. La planta hace visible por qué los dos vanos
libres importan —el arriostramiento vertical existe solo en los ejes extremos y
la carga de la grúa entra por el medio— y la sección mide la altura libre.
"""

from __future__ import annotations

import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from figuras import (  # noqa: E402
    ACERO, COTA, DESTAQUE, LINEA, TINTA, cota_h, cota_v, cotas, doc, encabezado, es,
    escribir, guia, linea, rect, txt,
)

C = cotas(AQUI)
D = {
    "luz": es(C["L_luz"]), "marco": es(C["s_marco"]), "largo": es(C["L_total"]),
    "hlibre": es(C["h_libre"]), "cumbrera": es(C["h_cumb"]), "pend": es(C["pend"]),
    "luzgrua": es(C["Lg_grua"]), "riel": es(C["h_riel"]), "Qn": es(C["Qn_grua"]),
}
PISO = "#f4f6f7"
PORTON = "#f2e6df"
CARRIL = "#2f5d7c"


def equis(x1, x2, y, alto, color=DESTAQUE, sw=2.2):
    """Un par de diagonales cruzadas: el símbolo de vano arriostrado."""
    return "\n".join([
        linea(x1, y - alto / 2, x2, y + alto / 2, color, sw),
        linea(x1, y + alto / 2, x2, y - alto / 2, color, sw),
    ])


def planta() -> str:
    """Los cuatro vanos, los dos que se arriostran y los dos que no."""
    e = 18.0
    x0, y0 = 128.0, 150.0
    largo, ancho = C["L_total"] * e, C["L_luz"] * e
    p = [encabezado(
        "Planta · los cuatro vanos y el recorrido de la grúa",
        "El arriostramiento vertical existe solo en los vanos extremos;",
        "los dos centrales quedan libres por los portones, y la grúa",
        "los cruza descargando sobre las vigas carrileras.")]
    p.append(rect(x0, y0, largo, ancho, fill=PISO, sw=1.0))
    xs = [x0 + i * C["s_marco"] * e for i in range(5)]
    hb = 26.0
    for yb in (y0, y0 + ancho):
        p.append(rect(x0, yb - hb / 2, largo, hb, fill="#fcfcfa", sw=1.2))
    for k, (a, b) in enumerate(zip(xs[:-1], xs[1:])):
        for yb in (y0, y0 + ancho):
            if k in (0, 3):
                p.append(equis(a + 4, b - 4, yb, hb - 8))
            else:
                p.append(rect(a + 8, yb - 7, (b - a) - 16, 14, fill=PORTON, sw=1.0))
        etiqueta = "arriostrado" if k in (0, 3) else "portón"
        color = DESTAQUE if k in (0, 3) else LINEA
        p.append(txt((a + b) / 2, y0 - 34, etiqueta, size=10, c=color))
        p.append(txt((a + b) / 2, y0 + ancho + 46, etiqueta, size=10, c=color))
    for i, x in enumerate(xs):
        p.append(linea(x, y0 - hb / 2 - 8, x, y0 + ancho + hb / 2 + 8, TINTA, 1.4))
        p.append(txt(x, y0 - 52, "ABCDE"[i], size=10.5, c=TINTA, peso="600"))
    off = (C["L_luz"] - C["Lg_grua"]) / 2.0 * e
    yc1, yc2 = y0 + off, y0 + ancho - off
    for yy in (yc1, yc2):
        p.append(linea(x0 + 6, yy, x0 + largo - 6, yy, CARRIL, 3.4))
    xg = x0 + 17.0 * e
    p.append(rect(xg - 8, yc1, 16, yc2 - yc1, fill=ACERO, sw=1.3))
    p.append(rect(xg - 26, (yc1 + yc2) / 2 - 12, 52, 24, fill=ACERO, sw=1.3))
    p.append(guia(xg + 26, (yc1 + yc2) / 2, x0 + largo + 44, (yc1 + yc2) / 2 - 54,
                  D["Qn"] + " kN"))
    p.append(guia(x0 + 9.5 * e, yc1, x0 + 10.6 * e, yc1 + 74, "viga carrilera", anchor="start"))
    p.append(cota_h(xs[0], xs[1], y0 + ancho + 78, D["marco"] + " m", arriba=False,
                    ext=y0 + ancho + hb / 2))
    p.append(cota_h(x0, x0 + largo, y0 + ancho + 120, D["largo"] + " m", arriba=False))
    p.append(cota_v(y0, y0 + ancho, x0 - 58, D["luz"] + " m"))
    p.append(cota_v(yc1, yc2, x0 + largo + 108, D["luzgrua"] + " m", izq=False))
    return doc(880, 420 + ancho, "\n".join(p),
               "Planta del galpón con los cuatro vanos, los dos arriostrados y "
               "los dos con portón, las vigas carrileras y el puente grúa")


def seccion() -> str:
    """La sección a dos aguas, con la altura que §12.2.1 c) mide."""
    e = 20.0
    x0, ysuelo = 168.0, 500.0
    luz = C["L_luz"] * e
    halero = C["h_libre"] * e
    hcum = C["h_cumb"] * e
    yalero = ysuelo - halero
    ycum = yalero - hcum
    xc = x0 + luz / 2
    p = [encabezado(
        "Sección transversal · el marco de momento a dos aguas",
        "La altura libre interior de columna es la que acota §12.2.1 c).",
        "El puente grúa apoya sobre las vigas carrileras, y estas sobre",
        "las ménsulas soldadas a las columnas.")]
    p.append(linea(x0 - 74, ysuelo, x0 + luz + 74, ysuelo, TINTA, 2.0))
    for x in (x0, x0 + luz):
        p.append(rect(x - 7, yalero, 14, halero, sw=1.4))
    p.append(linea(x0, yalero, xc, ycum, TINTA, 2.6))
    p.append(linea(xc, ycum, x0 + luz, yalero, TINTA, 2.6))
    yriel = ysuelo - C["h_riel"] * e
    offx = (C["L_luz"] - C["Lg_grua"]) / 2.0 * e
    for x, sg in ((x0, 1), (x0 + luz, -1)):
        xm = x + sg * offx
        xa, xb = sorted((x + sg * 7, xm + sg * 13))
        p.append(rect(xa, yriel + 5, xb - xa, 13, fill=ACERO, sw=1.1))
        p.append(rect(xm - 13, yriel - 12, 26, 17, fill=ACERO, sw=1.4))
        p.append(rect(xm - 5, yriel - 17, 10, 5, fill=TINTA, sw=0.8))
    p.append(rect(x0 + offx, yriel - 41, luz - 2 * offx, 24, fill="#fcfcfa", sw=1.4))
    p.append(rect(xc - 22, yriel - 37, 44, 16, fill=ACERO, sw=1.1))
    p.append(guia(xc + 22, yriel - 29, xc + 148, yriel + 44, D["Qn"] + " kN"))
    p.append(guia(x0 + offx + 13, yriel - 4, x0 + 2.9 * e, yriel + 78, "viga carrilera",
                  anchor="start"))
    p.append(txt(x0 + luz * 0.78, yalero - hcum * 0.42 - 12, D["pend"] + " %", size=10.5, c=COTA))
    p.append(cota_v(yalero, ysuelo, x0 - 62, D["hlibre"] + " m"))
    p.append(cota_v(ycum, yalero, xc + 30, D["cumbrera"] + " m", izq=False))
    p.append(cota_v(yriel - 17, ysuelo, x0 + luz + 66, D["riel"] + " m", izq=False))
    p.append(cota_h(x0, x0 + luz, ysuelo + 48, D["luz"] + " m", arriba=False, ext=ysuelo))
    p.append(cota_h(x0 + offx, x0 + luz - offx, ysuelo + 92, D["luzgrua"] + " m", arriba=False))
    return doc(880, 640, "\n".join(p),
               "Sección transversal a dos aguas con la altura libre de columna, "
               "la viga carrilera sobre su ménsula y la cumbrera")


if __name__ == "__main__":
    escribir(AQUI, {"planta": planta(), "seccion": seccion()})
