"""Las dos figuras del eslabón 07.

    python sitio/docs/series/nch2369-galpon-grua/07-marco-de-momento-a-dos-aguas/_figuras.py

Portadas de `_figuras-nch2369-galpon-grua-07.py` del repo de memos, con la
diferencia de fondo del sitio: las cotas se leen del `valores.json` del eslabón
(`figuras.cotas`), no se teclean. **La figura no ilustra: comprueba.**

**La primera existe para que se vea la conicidad, que es lo contrario de la del
catálogo.** El marco va a escala real en las dos direcciones y con la altura de
alma también a escala, así que la columna se ve gorda abajo y delgada arriba —al
revés del marco de alma variable que un proveedor despacha, que presupone base
rotulada—. El punto de inflexión del modo lateral se marca porque cae a 25 cm del
riel, y ésa es la razón mecánica de que el empuje de la grúa produzca tan poca
deriva.

**La segunda contesta cuál criterio de deriva manda, con la demanda adentro.** El
06 dibujó los dos límites y mostró que el de la grúa es seis veces más estricto;
acá las tres barras son **demandas**, y las dos que ese límite estricto mira son
las dos más cortas. La barra de la nieve es sólo la parte **antisimétrica** del
desplazamiento: la simétrica es apertura de trocha y se verifica aparte.

No las reemplaza un visor. El modelo 3D del sitio tiene la columna **escalonada**
del eslabón 10, que este marco todavía no conoce, y dibuja la geometría sin
rotular cantos de alma ni el punto de inflexión.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from figuras import cotas, escribir  # noqa: E402

C = cotas(AQUI)

TINTA, SUAVE, LINEA, FONDO = "#2b2a26", "#8a8578", "#c9c4b5", "#fcfcfa"
ACENTO, FRIO, VERDE, ACERO = "#a4442c", "#2f5d7c", "#4a6b46", "#d5d7da"
MONO = "ui-monospace,'IBM Plex Mono',Menlo,Consolas,monospace"


def txt(x, y, s, color=TINTA, anchor="start", size=11, peso="normal"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" text-anchor="{anchor}" '
            f'font-size="{size}" font-weight="{peso}">{s}</text>')


def es(v: float, d: int = 5) -> str:
    """Coma decimal y separador de miles fino, como toda cifra visible del repo."""
    return f"{v:,.{d}f}".replace(",", " ").replace(".", ",")


def ent(v: float) -> str:
    return f"{int(round(v)):,}".replace(",", " ")


# ------------------------------------------------------------------ figura 1
def marco() -> str:
    """Elevación del marco, con la altura de alma dibujada a escala."""
    W, H = 720, 386
    ESC = 18.0                      # px por metro de eje
    ESC_D = 0.028                   # px por mm de altura de alma
    X0, YB = 152.0, 336.0           # base de la columna izquierda

    px = lambda x: X0 + x * ESC
    py = lambda y: YB - y * ESC

    L, ha, hc = C["L_luz"], C["h_libre"], C["h_cumb"]

    def canto(x, y, dx, dy, d):
        """Los dos bordes del alma, separados `d` mm perpendicular al eje."""
        n = math.hypot(dx, dy)
        ux, uy = -dy / n, dx / n
        e = d * ESC_D / 2
        return (px(x) + ux * e, py(y) - uy * e), (px(x) - ux * e, py(y) + uy * e)

    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
        f'height="{H}" role="img" aria-label="Elevacion del marco a dos aguas con las '
        f'dos columnas conicas mas gruesas en la base que en el nudo y los dos rafters '
        f'adelgazando hacia la cumbrera, con el nivel de riel y el punto de inflexion '
        f'del modo lateral marcados" font-family="{MONO}" font-size="11">',
        "<title>El marco de alma variable, con la conicidad al revés</title>",
        f'<rect width="{W}" height="{H}" fill="{FONDO}"/>',
        txt(24, 28, "La conicidad de la columna abre hacia abajo, porque la base está empotrada",
            TINTA, "start", 11.5, "600"),
    ]

    tramos = [
        (0.0, 0.0, 0.0, ha, C["d_col_base"], C["d_col_nudo"]),      # columna izquierda
        (0.0, ha, L / 2, hc, C["d_col_nudo"], C["d_raf_cumb"]),     # rafter izquierdo
        (L / 2, hc, L, ha, C["d_raf_cumb"], C["d_col_nudo"]),       # rafter derecho
        (L, ha, L, 0.0, C["d_col_nudo"], C["d_col_base"]),          # columna derecha
    ]
    for x1, y1, x2, y2, d1, d2 in tramos:
        dx, dy = x2 - x1, y2 - y1
        a1, b1 = canto(x1, y1, dx, dy, d1)
        a2, b2 = canto(x2, y2, dx, dy, d2)
        pts = (f"{a1[0]:.1f},{a1[1]:.1f} {a2[0]:.1f},{a2[1]:.1f} "
               f"{b2[0]:.1f},{b2[1]:.1f} {b1[0]:.1f},{b1[1]:.1f}")
        o.append(f'<polygon points="{pts}" fill="{ACERO}" stroke="{TINTA}" stroke-width="1.1"/>')

    o.append(f'<line x1="{px(-1.4):.1f}" y1="{YB:.1f}" x2="{px(L + 1.4):.1f}" y2="{YB:.1f}" '
             f'stroke="{TINTA}" stroke-width="1.6"/>')
    for xb in (0.0, L):
        for k in range(5):
            xx = px(xb) - 12 + 6 * k
            o.append(f'<line x1="{xx:.1f}" y1="{YB:.1f}" x2="{xx - 6:.1f}" y2="{YB + 8:.1f}" '
                     f'stroke="{SUAVE}" stroke-width="1"/>')

    yr = py(C["h_riel"])
    o.append(f'<line x1="{px(-1.2):.1f}" y1="{yr:.1f}" x2="{px(L + 1.2):.1f}" y2="{yr:.1f}" '
             f'stroke="{ACENTO}" stroke-width="1.2" stroke-dasharray="5 4"/>')
    o.append(txt(622, yr - 5, f'riel {es(C["h_riel"], 2)} m', ACENTO, "start", 10))
    o.append(txt(622, yr + 9, f'd {es(C["d_col_riel"])}', ACENTO, "start", 10))

    yi = py(C["y_infl"])
    for xb in (0.0, L):
        o.append(f'<circle cx="{px(xb):.1f}" cy="{yi:.1f}" r="3.4" fill="{FRIO}"/>')
    o.append(txt(136, yi - 15, "inflexión", FRIO, "end", 10))
    o.append(txt(136, yi - 3, f'{es(C["y_infl"])} m', FRIO, "end", 10))

    for xb in (0.0, L):
        x = px(xb) - 46
        o.append(f'<line x1="{x:.1f}" y1="{yr:.1f}" x2="{x + 30:.1f}" y2="{yr:.1f}" '
                 f'stroke="{ACENTO}" stroke-width="2.2"/>')
        o.append(f'<path d="M {x + 38:.1f} {yr:.1f} l -9 -4.5 l 0 9 z" fill="{ACENTO}"/>')
    o.append(txt(px(L / 2), yr + 30,
                 f'los dos rieles empujan al mismo lado · {es(C["SS_marco"])} kN',
                 ACENTO, "middle", 10))

    o.append(txt(94, py(0.0) - 6, f'alma {ent(C["d_col_base"])}', TINTA, "end", 10.5))
    o.append(txt(94, py(ha) + 4, f'alma {ent(C["d_col_nudo"])}', TINTA, "end", 10.5))
    o.append(txt(px(L / 2), py(hc) - 16, f'alma {ent(C["d_raf_cumb"])}', TINTA, "middle", 10.5))

    ycot = YB + 30
    o.append(f'<line x1="{px(0.0):.1f}" y1="{ycot:.1f}" x2="{px(L):.1f}" y2="{ycot:.1f}" '
             f'stroke="{SUAVE}" stroke-width="1"/>')
    o.append(txt(px(L / 2), ycot - 5, f'luz {es(C["L_luz"], 2)} m', SUAVE, "middle", 10))
    o.append(txt(622, py(ha) + 4, f'alero {es(C["h_libre"], 2)} m', SUAVE, "start", 10))
    o.append(txt(px(L / 2), py(hc) - 42, f'cumbrera {es(C["h_cumb"], 2)} m', SUAVE, "middle", 10))
    o.append(txt(px(L * 0.75), py((ha + hc) / 2) - 30,
                 f'media agua {es(C["L_r"])} m', SUAVE, "middle", 10))

    o.append(txt(696, 50, f'columna · alas {ent(C["bf_col"])} x {ent(C["tf_col"])} · '
                 f'alma {ent(C["tw_col"])}', SUAVE, "end", 10))
    o.append(txt(696, 64, f'rafter · alas {ent(C["bf_raf"])} x {ent(C["tf_raf"])} · '
                 f'alma {ent(C["tw_raf"])}', SUAVE, "end", 10))
    o.append("</svg>")
    return "\n".join(o) + "\n"


# ------------------------------------------------------------------ figura 2
def derivas() -> str:
    """Las tres demandas laterales contra los dos límites, a la misma escala."""
    W, H = 720, 300
    X0, X1 = 252, 632
    TOPE = C["d_lim"] * 1.06
    px = lambda v: X0 + (X1 - X0) * v / TOPE

    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
        f'height="{H}" role="img" aria-label="Las tres demandas laterales del marco '
        f'contra los dos limites de deriva: el empuje de la grua es la barra mas corta '
        f'y es la que el limite mas estricto mira, la nieve desbalanceada es mayor y '
        f'ningun limite la mira, y el sismo pasa la clausula 6.3" '
        f'font-family="{MONO}" font-size="11">',
        "<title>El límite más estricto es el menos exigido</title>",
        f'<rect width="{W}" height="{H}" fill="{FONDO}"/>',
        txt(24, 28, "El límite seis veces más estricto es el que queda menos exigido",
            TINTA, "start", 11.5, "600"),
    ]

    for v, col, nom, anc in ((C["dlim_grua"], ACENTO, "grúa · AIST §5.3", "start"),
                             (C["d_lim"], VERDE, "§6.3 · 0,015 h", "end")):
        o.append(f'<line x1="{px(v):.1f}" y1="56" x2="{px(v):.1f}" y2="236" '
                 f'stroke="{col}" stroke-width="1.4" stroke-dasharray="4 3"/>')
        o.append(txt(px(v) + (6 if anc == "start" else -6), 50, nom, col, anc, 10))
        o.append(txt(px(v) + (6 if anc == "start" else -6), 254, es(v, 2), col, anc, 10))

    filas = [
        ("empuje de grúa · al riel", C["d_riel_grua"], ACENTO, "uso 0,164"),
        ("nieve desbalanceada · al riel", C["d_riel_des"], SUAVE, "0,55 de la grúa"),
        ("sismo de §6.1 · al alero", C["d_Y2"], FRIO, "uso 0,414"),
    ]
    y = 76
    for nom, v, col, nota in filas:
        o.append(f'<rect x="{X0}" y="{y}" width="{max(px(v) - X0, 1.5):.1f}" height="24" '
                 f'fill="{col}" opacity="0.85"/>')
        o.append(txt(X0 - 10, y + 16, nom, TINTA, "end", 10.5))
        lx = px(v) + 8
        if lx < px(C["dlim_grua"]) + 14:
            lx = px(C["dlim_grua"]) + 14
        o.append(txt(lx, y + 16, es(v), col, "start", 10.5))
        o.append(txt(lx + 74, y + 16, nota, SUAVE, "start", 10))
        y += 54

    o.append(f'<line x1="{X0}" y1="56" x2="{X0}" y2="242" stroke="{TINTA}" stroke-width="1"/>')
    o.append(txt(X0 - 10, 254, "mm", SUAVE, "end", 10))
    o.append(txt(24, 282, "el sismo no es un estado de servicio: por eso lo mide el otro límite",
                 SUAVE, "start", 10))
    o.append("</svg>")
    return "\n".join(o) + "\n"


if __name__ == "__main__":
    escribir(AQUI, {"marco": marco(), "derivas": derivas()})
