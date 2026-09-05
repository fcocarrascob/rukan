"""La figura del eslabón 03: el carro contra su tope y las dos reacciones de rueda.

    python sitio/docs/series/nch2369-galpon-grua/03-cargas-de-grua/_figuras.py

Portado de `_img/_figuras-nch2369-galpon-grua-03.py` del repo de memos, con las
cotas leídas del `valores.json` del eslabón (`figuras.cotas`).

La pregunta de esta figura es **de dónde sale la asimetría**: el carro contra su
tope carga un testero con tres veces lo que carga el otro, y esa es toda la
razón de que la reacción de rueda no sea un cuarto del peso. Por eso el carro se
dibuja en su posición más desfavorable, con la cota de aproximación medida contra
el eje del riel, y las dos reacciones rotuladas a la vez para poder compararlas.
"""

from __future__ import annotations

import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from figuras import (  # noqa: E402
    ACERO, DESTAQUE, LINEA, TINTA, cota_h, cotas, doc, encabezado, es, escribir,
    guia, linea, rect, txt,
)

C = cotas(AQUI)
D = {
    "Lg": es(C["Lg_grua"]), "a": es(C["a_gancho"]), "wb": es(C["wb_d"]),
    "Rmax": es(C["Rw_max"], 5), "Rmin": es(C["Rw_min"], 5),
    "Q": es(C["Qn_grua"]), "Wt": es(C["Wt_d"]), "Wb": es(C["Wb_d"]),
}

CARRIL = "#2f5d7c"


def reacciones() -> str:
    e = 25.0                       # px por metro
    x0, yriel = 148.0, 300.0
    Lg = C["Lg_grua"] * e
    x1 = x0 + Lg
    media_base = C["wb_d"] * e / 4          # las dos ruedas, a escala reducida
    p = [encabezado(
        "Reacciones de rueda · el carro contra su tope",
        "El carro en su posición más desfavorable carga un testero con",
        "tres veces lo que carga el opuesto. Las cuatro ruedas son motrices.")]

    # las dos vigas carrileras, de canto, con su riel
    for x in (x0, x1):
        p.append(rect(x - 30, yriel + 6, 60, 22, fill=ACERO, sw=1.3))
        p.append(rect(x - 9, yriel, 18, 6, fill=TINTA, sw=0.8))
        p.append(linea(x - 44, yriel + 28, x + 44, yriel + 28, CARRIL, 3.0))

    # el puente: viga entre los dos testeros
    p.append(rect(x0, yriel - 46, Lg, 20, fill="#fcfcfa", sw=1.5))

    # los dos testeros, cada uno con SUS DOS ruedas separadas wb
    for x in (x0, x1):
        p.append(rect(x - 34, yriel - 26, 68, 22, fill=ACERO, sw=1.3))
        for s in (-1, 1):
            xr = x + s * media_base
            p.append(f'<circle cx="{xr:.1f}" cy="{yriel - 2:.1f}" r="7" '
                     f'fill="#fcfcfa" stroke="{TINTA}" stroke-width="1.2"/>')

    # el carro, contra su tope
    xc = x0 + C["a_gancho"] * e
    p.append(rect(xc - 26, yriel - 74, 52, 28, fill=ACERO, sw=1.4))
    # El gancho va EN EL EJE del carro: correrlo desmentiría la cota de la
    # aproximación, que es justamente la distancia del riel a ese eje. Que pase
    # por delante del testero es la geometría real de una aproximación tan corta.
    p.append(linea(xc, yriel - 46, xc, yriel + 116, TINTA, 1.4))
    p.append(rect(xc - 22, yriel + 116, 44, 26, fill="#fcfcfa", sw=1.4))
    p.append(txt(xc, yriel + 133, D["Q"], size=10, c=TINTA))
    p.append(guia(xc + 26, yriel - 60, xc + 96, yriel - 96, D["Wt"] + " kN"))
    p.append(guia(x0 + Lg * 0.62, yriel - 36, x0 + Lg * 0.70, yriel - 96,
                  D["Wb"] + " kN"))

    # las reacciones, hacia abajo desde cada testero
    for x, val in ((x0 - 58, D["Rmax"]), (x1 + 58, D["Rmin"])):
        y2 = yriel + 96
        p.append(linea(x, yriel + 34, x, y2 - 7, DESTAQUE, 2.4))
        p.append(f'<path d="M {x:.1f} {y2:.1f} l -5 -11 l 10 0 z" fill="{DESTAQUE}"/>')
        p.append(txt(x, y2 + 20, val, size=10.5, c=DESTAQUE))
        p.append(txt(x, y2 + 34, "kN por rueda", size=9, c=LINEA))

    # cotas
    p.append(cota_h(x0, xc, yriel - 108, D["a"] + " m", arriba=True, ext=yriel - 74))
    p.append(cota_h(x0, x1, yriel - 146, D["Lg"] + " m", arriba=True))
    p.append(cota_h(x0 - media_base, x0 + media_base, yriel + 58,
                    D["wb"] + " m", arriba=False, ext=yriel + 5))
    return doc(860, 540, "\n".join(p),
               "Elevación del puente grúa con el carro contra su tope y las "
               "reacciones de rueda máxima y mínima")


if __name__ == "__main__":
    escribir(AQUI, {"reacciones-de-rueda": reacciones()})
