"""La figura del eslabón 02: los dos diagramas de carga de nieve, uno sobre otro.

    python sitio/docs/series/nch2369-galpon-grua/02-nieve-balanceada-y-desbalanceada/_figuras.py

Portado de `_img/_figuras-nch2369-galpon-grua-02.py` del repo de memos. Las
cotas y las alturas de los diagramas se leen del `valores.json` del eslabón
(`figuras.cotas`), no se teclean.

La pregunta de esta figura es **dónde cae cada carga**, no cuánto vale: el modo
de falla propio de §8.2 es aplicar la acumulación al faldón equivocado, o
medirla desde el alero en vez de desde la cumbrera. Por eso los dos diagramas
van uno sobre otro, con el mismo eje, y la franja de acumulación se acota desde
la cumbrera.
"""

from __future__ import annotations

import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from figuras import (  # noqa: E402
    DESTAQUE, LINEA, TINTA, cota_h, cota_v, cotas, doc, encabezado, es,
    escribir, linea, txt,
)

C = cotas(AQUI)
D = {
    "luz": es(C["L_luz"]), "semi": es(C["W"]), "cumbrera": es(C["h_cumbrera"]),
    "ps": es(C["p_s"]), "bar": es(C["p_bar"], 3), "pico": es(C["p_pico"], 5),
    "Lac": es(C["L_ac"], 5),
}


def flechitas(x1, x2, ytecho1, ytecho2, alto, paso=13.0, color=TINTA):
    """Flechas verticales que bajan hasta la línea del techo, interpolada."""
    p, n = [], max(2, int((x2 - x1) / paso))
    for k in range(n + 1):
        t = k / n
        x = x1 + (x2 - x1) * t
        yt = ytecho1 + (ytecho2 - ytecho1) * t
        p.append(linea(x, yt - alto, x, yt - 4, color, 1.0))
        p.append(f'<path d="M {x:.1f} {yt:.1f} l -2.6 -5.2 l 5.2 0 z" fill="{color}"/>')
    return "\n".join(p)


def techo(px0, pxc, px1, ya, yc):
    return "\n".join([linea(px0, ya, pxc, yc, TINTA, 2.6),
                      linea(pxc, yc, px1, ya, TINTA, 2.6)])


def diagrama(x0, ybase, e, titulo, balanceada):
    """Un diagrama: el techo a dos aguas con su distribución de nieve encima."""
    luz = C["L_luz"] * e
    xc = x0 + luz / 2
    ya = ybase                              # alero
    yc = ybase - C["h_cumbrera"] * e        # cumbrera
    esc = 26.0                              # px por kN/m2
    p = [txt(x0, ybase + 34, titulo, anchor="start", size=11, peso="600")]

    if balanceada:
        h = C["p_s"] * esc
        p.append(flechitas(x0, xc, ya, yc, h))
        p.append(flechitas(xc, x0 + luz, yc, ya, h))
        p.append(linea(x0, ya - h, xc, yc - h, DESTAQUE, 2.0))
        p.append(linea(xc, yc - h, x0 + luz, ya - h, DESTAQUE, 2.0))
        p.append(txt(x0 + luz * 0.26, ya - h - 26 - (yc - ya) * 0.26,
                     D["ps"], size=10.5, c=DESTAQUE))
        p.append(txt(x0 + luz * 0.74, ya - h - 26 - (yc - ya) * 0.26,
                     D["ps"], size=10.5, c=DESTAQUE))
    else:
        # barlovento: la carga reducida, uniforme sobre el faldón izquierdo
        hb = C["p_bar"] * esc
        p.append(flechitas(x0, xc, ya, yc, hb))
        p.append(linea(x0, ya - hb, xc, yc - hb, DESTAQUE, 2.0))
        # su franja mide una décima de la de sotavento y no hay lugar encima,
        # así que los rótulos van DEBAJO de la línea del techo, que está despejada
        xb = x0 + luz * 0.30
        yb = ya + (yc - ya) * 0.30
        p.append(txt(xb, yb + 24, D["bar"], size=10.5, c=DESTAQUE))
        p.append(txt(xb, yb + 38, "barlovento", size=9.5, c=LINEA))

        # sotavento: la franja de acumulación pegada a la cumbrera, y p_s al resto
        xac = xc + C["L_ac"] * e
        hp, hs = C["p_pico"] * esc, C["p_s"] * esc
        yac = yc + (ya - yc) * (C["L_ac"] / C["W"])
        p.append(flechitas(xc, xac, yc, yac, hp))
        p.append(flechitas(xac, x0 + luz, yac, ya, hs))
        p.append(linea(xc, yc - hp, xac, yac - hp, DESTAQUE, 2.0))
        p.append(linea(xac, yac - hp, xac, yac - hs, DESTAQUE, 2.0))
        p.append(linea(xac, yac - hs, x0 + luz, ya - hs, DESTAQUE, 2.0))
        p.append(txt(xc + 30, yc - hp - 12, D["pico"], anchor="start",
                     size=10.5, c=DESTAQUE))
        p.append(txt(x0 + luz - 12, ya - hs - 14, D["ps"], anchor="end",
                     size=10.5, c=DESTAQUE))
        p.append(txt(x0 + luz * 0.80, ya - hs - 30, "sotavento", size=9.5, c=LINEA))
        p.append(cota_h(xc, xac, ya + 16, D["Lac"] + " m", arriba=False))

    p.append(techo(x0, xc, x0 + luz, ya, yc))
    p.append(linea(xc, yc, xc, ya + 22, LINEA, 0.8, "4 3"))
    return "\n".join(p)


def cargas() -> str:
    e = 22.0
    x0 = 150.0
    p = [encabezado(
        "Nieve balanceada y desbalanceada · §8.2",
        "El viento sopla de izquierda a derecha. La acumulación se mide",
        "DESDE LA CUMBRERA hacia el alero de sotavento, no al revés.")]

    p.append(diagrama(x0, 268.0, e, "Balanceada", True))
    p.append(diagrama(x0, 556.0, e, "Desbalanceada", False))

    # el viento, y las cotas generales
    p.append(linea(x0 - 88, 210, x0 - 26, 210, TINTA, 2.0))
    p.append('<path d="M %.1f 210 l -9 -5 l 0 10 z" fill="%s"/>' % (x0 - 24, TINTA))
    p.append(txt(x0 - 57, 198, "viento", size=10, c=TINTA))

    luz = C["L_luz"] * e
    p.append(cota_h(x0, x0 + luz / 2, 616, D["semi"] + " m", arriba=False))
    p.append(cota_h(x0, x0 + luz, 654, D["luz"] + " m", arriba=False))
    # la cumbrera sobre el alero, con su línea de extensión desde la cumbrera
    xc, ya = x0 + luz / 2, 556.0
    yc = ya - C["h_cumbrera"] * e
    p.append(linea(xc, yc, x0 + luz + 44, yc, "#c9c4b8", 0.7, "3 3"))
    p.append(linea(x0 + luz, ya, x0 + luz + 44, ya, "#c9c4b8", 0.7, "3 3"))
    p.append(cota_v(yc, ya, x0 + luz + 34, D["cumbrera"] + " m", izq=False))
    return doc(820, 710, "\n".join(p),
               "Diagramas de carga de nieve balanceada y desbalanceada sobre la "
               "sección a dos aguas del galpón")


if __name__ == "__main__":
    escribir(AQUI, {"cargas-de-nieve": cargas()})
