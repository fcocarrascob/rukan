"""La figura del eslabón 05: los dos cortes basales entre el piso y el techo.

    python sitio/docs/series/nch2369-galpon-grua/05-masa-sismica-y-carga-suspendida/_figuras.py

Portado de `_img/_figuras-nch2369-galpon-grua-05.py` del repo de memos, con las
cotas leídas del `valores.json` del eslabón (`figuras.cotas`).

La pregunta de esta figura es **qué le hace el techo de §5.13 a la diferencia
entre direcciones**: las dos barras del análisis se dibujan a escala junto al
piso y al techo, y las dos flechas de recorte terminan en el mismo punto.
"""

from __future__ import annotations

import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from figuras import cotas, escribir  # noqa: E402

C = cotas(AQUI)

TINTA, SUAVE, FONDO = "#2b2a26", "#8a8578", "#fcfcfa"
ACENTO, FRIO, VERDE = "#a4442c", "#2f5d7c", "#4a6b46"
MONO = "ui-monospace,'IBM Plex Mono',Menlo,Consolas,monospace"


def txt(x, y, s, color=TINTA, anchor="start", size=11, peso="normal"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" text-anchor="{anchor}" '
            f'font-size="{size}" font-weight="{peso}">{s}</text>')


def es(v: float, d: int = 5) -> str:
    """Coma decimal y separador de miles fino, como toda cifra visible del sitio."""
    return f"{v:,.{d}f}".replace(",", " ").replace(".", ",")


def corte_basal() -> str:
    W, H = 720, 328
    X0, X1 = 210, 640
    TOPE = C["Q0_X_an"] * 1.02
    def px(v): return X0 + (X1 - X0) * v / TOPE

    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
        f'height="{H}" role="img" aria-label="Los dos cortes basales del analisis '
        f'contra el piso de 5.12 y el techo de 5.13, y el corte de diseno unico al '
        f'que los dos quedan recortados" font-family="{MONO}" font-size="11">',
        "<title>Corte basal entre el piso y el techo</title>",
        f'<rect width="{W}" height="{H}" fill="{FONDO}"/>',
        txt(24, 26, "El techo de §5.13 borra la diferencia entre direcciones",
            TINTA, "start", 11.5, "600"),
    ]

    # la banda admisible, entre el piso y el techo
    o.append(f'<rect x="{px(C["Q0_min"]):.1f}" y="52" '
             f'width="{px(C["Q0_max"]) - px(C["Q0_min"]):.1f}" '
             f'height="200" fill="{VERDE}" opacity="0.07"/>')
    for v, col, nom in ((C["Q0_min"], VERDE, "piso §5.12"),
                        (C["Q0_max"], ACENTO, "techo §5.13")):
        o.append(f'<line x1="{px(v):.1f}" y1="52" x2="{px(v):.1f}" y2="252" '
                 f'stroke="{col}" stroke-width="1.4" stroke-dasharray="4 3"/>')
        o.append(txt(px(v), 46, nom, col, "middle", 10))

    filas = [
        ("Q0 análisis · X arriostrada", C["Q0_X_an"], FRIO, C["super_X"]),
        ("Q0 análisis · Y marcos", C["Q0_Y_an"], FRIO, C["super_Y"]),
        ("Q0 de diseño · las dos", C["Q0_max"], ACENTO, None),
    ]
    y = 78
    for nom, v, col, u in filas:
        o.append(f'<rect x="{X0}" y="{y}" width="{px(v) - X0:.1f}" height="26" '
                 f'fill="{col}" opacity="0.85"/>')
        o.append(txt(X0 - 10, y + 17, nom, TINTA, "end", 10.5))
        o.append(txt(px(v) + 8, y + 17, es(v, 5), col, "start", 10.5))
        if u is not None:
            # la flecha del recorte, desde el extremo de la barra hasta el techo
            o.append(f'<line x1="{px(v) - 4:.1f}" y1="{y + 13}" '
                     f'x2="{px(C["Q0_max"]) + 10:.1f}" y2="{y + 13}" '
                     f'stroke="{FONDO}" stroke-width="1.6"/>')
            o.append(f'<polygon points="{px(C["Q0_max"]) + 2:.1f},{y + 13} '
                     f'{px(C["Q0_max"]) + 12:.1f},{y + 8.5} '
                     f'{px(C["Q0_max"]) + 12:.1f},{y + 17.5}" fill="{FONDO}"/>')
            # el rótulo va a la IZQUIERDA de la línea del techo: centrado entre las
            # dos barras caía justo encima de ella
            o.append(txt(px(C["Q0_max"]) - 10, y + 40, "supera " + es(u, 5),
                         SUAVE, "end", 10))
        y += 62

    o.append(f'<line x1="{X0}" y1="52" x2="{X0}" y2="264" stroke="{TINTA}" stroke-width="1"/>')
    o.append(txt(X0 - 10, 290, "kN sobre el nivel basal", SUAVE, "end", 10))
    o.append(txt(px(C["Q0_max"]), 290,
                 "las dos direcciones terminan en el mismo corte", ACENTO, "middle", 10))
    o.append("</svg>")
    return "\n".join(o) + "\n"


if __name__ == "__main__":
    escribir(AQUI, {"corte-basal": corte_basal()})
