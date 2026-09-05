"""Las dos figuras del eslabón 06: las dos rutas del vertical, y los dos límites
de deriva.

    python sitio/docs/series/nch2369-galpon-grua/06-combinaciones-y-derivas/_figuras.py

Portado de `_img/_figuras-nch2369-galpon-grua-06.py` del repo de memos, con las
cotas leídas del `valores.json` del eslabón (`figuras.cotas`) y la curva trazada
con la misma Ec. (4) que el `_calculo.py` escribe.

**La primera figura contesta si elegir entre las dos rutas de §5.7 decide algo.**
La respuesta se ve mejor en una curva con una recta encima que en cualquier tabla:
la recta del coeficiente estático pasa **por el pico** de la curva modal, apenas
por debajo, y solo lo cruza en una ventana de 26 ms.

**La segunda contesta cuál de los dos límites de deriva manda.** Las dos líneas
verticales están a escala real una respecto de la otra —18,75 contra 157,50 mm,
factor 6— y las tres barras muestran de un golpe que el desplazamiento correcto
pasa los dos criterios, y que el equivocado también: por eso el error de calcular
la deriva con el corte de diseño no se ve.

**Ningún eje lleva marcas numéricas propias.** Un rótulo de 0,1 o de 50 sería un
número nacido en la capa de dibujo, sin respaldo en el eslabón. Cada punto y cada
barra llevan su propio valor.
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


def sa_vertical(t: float) -> float:
    """Ec. (2) con la Ec. (4) adentro: el 1,7 multiplica a T_V/T_0."""
    u = 1.7 * t / C["T_0"]
    forma = (1 + C["r_s"] * u ** C["p_suelo"]) / (1 + u ** C["q_s"])
    return C["I"] * 0.7 * C["ArS"] * forma * C["f_xiV"] / C["R_V"]


# ------------------------------------------------------------------ figura 1
def vertical() -> str:
    W, H = 720, 340
    X0, X1, Y0, Y1 = 112, 660, 72, 262
    TMAX, SMAX = 0.80, 0.60
    def px(t): return X0 + (X1 - X0) * t / TMAX
    def py(s): return Y1 - (Y1 - Y0) * s / SMAX

    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
        f'height="{H}" role="img" aria-label="El espectro de diseno vertical de la '
        f'Ec. 2 y la recta del coeficiente estatico de 5.7.1, que pasa justo por '
        f'debajo del pico de la curva" font-family="{MONO}" font-size="11">',
        "<title>Las dos rutas de la acción sísmica vertical</title>",
        f'<rect width="{W}" height="{H}" fill="{FONDO}"/>',
        txt(24, 28, "El coeficiente estático de §5.7.1 es el pico de la ruta modal, redondeado",
            TINTA, "start", 11.5, "600"),
    ]

    # la ventana donde la modal supera al estático
    o.append(f'<rect x="{px(C["T_cru1"]):.1f}" y="{Y0}" '
             f'width="{px(C["T_cru2"]) - px(C["T_cru1"]):.1f}" height="{Y1 - Y0}" '
             f'fill="{ACENTO}" opacity="0.13"/>')

    # la curva del espectro de diseño vertical
    pasos = 320
    pts = [f"{px(TMAX * k / pasos):.2f},{py(sa_vertical(TMAX * k / pasos)):.2f}"
           for k in range(pasos + 1)]
    o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{FRIO}" '
             f'stroke-width="2"/>')

    # la recta del estático
    o.append(f'<line x1="{X0}" y1="{py(C["C_V"]):.1f}" x2="{X1}" y2="{py(C["C_V"]):.1f}" '
             f'stroke="{VERDE}" stroke-width="1.6" stroke-dasharray="6 4"/>')

    # el pico
    o.append(f'<circle cx="{px(C["TV_pico"]):.1f}" cy="{py(C["SaV_dis_pico"]):.1f}" '
             f'r="3.4" fill="{ACENTO}"/>')
    o.append(txt(px(C["TV_pico"]) + 16, py(C["SaV_dis_pico"]) - 30,
                 f'pico modal {es(C["SaV_dis_pico"])} g', ACENTO, "start", 10.5))
    o.append(txt(px(C["TV_pico"]) + 16, py(C["SaV_dis_pico"]) - 17,
                 f'en T_V = {es(C["TV_pico"])} s', ACENTO, "start", 10.5))
    o.append(txt(X1, py(C["C_V"]) + 15, f'estático §5.7.1 · C_V = {es(C["C_V"])}',
                 VERDE, "end", 10.5))

    # los dos cruces
    for t, anc, dx in ((C["T_cru1"], "end", -6), (C["T_cru2"], "start", 6)):
        o.append(f'<line x1="{px(t):.1f}" y1="{py(C["C_V"]):.1f}" x2="{px(t):.1f}" '
                 f'y2="{Y1}" stroke="{ACENTO}" stroke-width="1" stroke-dasharray="3 3"/>')
        o.append(txt(px(t) + dx, Y1 + 15, es(t), ACENTO, anc, 10))
    o.append(txt(px(C["T_cru2"]) + 46, Y1 + 15,
                 "s · la modal gobierna sólo entre esas dos", SUAVE, "start", 10))

    # los ejes, sin marcas numéricas
    o.append(f'<line x1="{X0}" y1="{Y0 - 8}" x2="{X0}" y2="{Y1}" stroke="{TINTA}" '
             f'stroke-width="1"/>')
    o.append(f'<line x1="{X0}" y1="{Y1}" x2="{X1 + 8}" y2="{Y1}" stroke="{TINTA}" '
             f'stroke-width="1"/>')
    o.append(txt(X0 - 8, Y0 + 4, "ordenada", SUAVE, "end", 10))
    o.append(txt(X0 - 8, Y0 + 17, "de diseño", SUAVE, "end", 10))
    o.append(txt(X0 - 8, Y0 + 30, "vertical, g", SUAVE, "end", 10))
    o.append(txt(X1 + 8, Y1 + 34, "período vertical T_V", SUAVE, "end", 10))
    # el extremo rígido de la curva, que es donde la otra serie tomó su factor
    y0 = py(sa_vertical(0.0))
    o.append(f'<circle cx="{X0:.1f}" cy="{y0:.1f}" r="3" fill="{SUAVE}"/>')
    for k, linea in enumerate(("acá, con T_V = 0,", "la otra serie midió", "su factor 2,56")):
        o.append(txt(X0 + 10, y0 + 22 + 13 * k, linea, SUAVE, "start", 10))
    o.append("</svg>")
    return "\n".join(o) + "\n"


# ------------------------------------------------------------------ figura 2
def derivas() -> str:
    W, H = 720, 288
    X0, X1 = 232, 646
    TOPE = C["d_lim"] * 1.06
    def px(v): return X0 + (X1 - X0) * v / TOPE

    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
        f'height="{H}" role="img" aria-label="Los tres desplazamientos contra los dos '
        f'limites de deriva, el de la grua y el de la clausula 6.3, que estan en '
        f'relacion seis a uno: el desplazamiento sismico de la direccion de marcos '
        f'pasa el segundo y supera al primero" font-family="{MONO}" font-size="11">',
        "<title>Los dos límites de deriva, y el que manda</title>",
        f'<rect width="{W}" height="{H}" fill="{FONDO}"/>',
        txt(24, 28, "El límite de la grúa es seis veces más estricto que el de §6.3",
            TINTA, "start", 11.5, "600"),
    ]

    for v, col, nom, anc in ((C["dlim_grua"], ACENTO, "grúa · AIST §5.3", "start"),
                             (C["d_lim"], VERDE, "§6.3 · 0,015 h", "end")):
        o.append(f'<line x1="{px(v):.1f}" y1="54" x2="{px(v):.1f}" y2="228" '
                 f'stroke="{col}" stroke-width="1.4" stroke-dasharray="4 3"/>')
        o.append(txt(px(v) + (6 if anc == "start" else -6), 48, nom, col, anc, 10))
        o.append(txt(px(v) + (6 if anc == "start" else -6), 246, es(v, 2), col, anc, 10))

    filas = [
        ("d con el espectro de referencia · Y", C["d_Y"], FRIO),
        ("d con el espectro de referencia · X", C["d_X"], FRIO),
        ("d con el corte de diseño · el error", C["d_Y_ing"], SUAVE),
    ]
    y = 74
    for nom, v, col in filas:
        o.append(f'<rect x="{X0}" y="{y}" width="{max(px(v) - X0, 1.5):.1f}" height="24" '
                 f'fill="{col}" opacity="0.85"/>')
        o.append(txt(X0 - 10, y + 16, nom, TINTA, "end", 10.5))
        # dos de las tres barras terminan casi sobre la línea de la grúa, y el
        # valor caía encima del trazo
        lx = px(v) + 8
        if abs(lx - px(C["dlim_grua"])) < 18:
            lx = px(C["dlim_grua"]) + 14
        o.append(txt(lx, y + 16, es(v), col, "start", 10.5))
        y += 52

    o.append(f'<line x1="{X0}" y1="54" x2="{X0}" y2="234" stroke="{TINTA}" stroke-width="1"/>')
    o.append(txt(X0 - 10, 246, "mm en el alero", SUAVE, "end", 10))
    o.append(txt(X0 + 10, 272, "el sismo pasa §6.3 y triplica con holgura el límite de "
                 "servicio de la grúa", SUAVE, "start", 10))
    o.append("</svg>")
    return "\n".join(o) + "\n"


if __name__ == "__main__":
    escribir(AQUI, {"vertical": vertical(), "derivas": derivas()})
