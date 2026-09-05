"""Las tres figuras del eslabon 09.

    python sitio/docs/series/nch2369-galpon-grua/09-fatiga-de-la-viga-carrilera/_figuras.py

Portadas del repo de memos, con las cotas leidas del `valores.json` del eslabon
(`figuras.cotas`) en vez de tecleadas. La figura no ilustra: comprueba.

Ninguna la reemplaza un visor: las tres son curvas S-N y mapas de categoria sobre
la seccion, que es informacion de norma y no de modelo.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from figuras import cotas, escribir  # noqa: E402

C = cotas(AQUI)

# El puente entre los nombres cortos del dibujo y los simbolos del eslabon.
# Ninguna cifra nace aqui.
D = {
    "bfs": C["bfs_carril"], "tfs": C["tfs_carril"], "hw": C["hw_carril"],
    "tw": C["tw_carril"], "bfi": C["bfi_carril"], "tfi": C["tfi_carril"],
    "d": C["d_carril"], "ybar": C["ybar_carril"], "yinf": C["y_inf"],
    "sr_inf": C["sr_inf_carril"], "sr_sup": C["sr_sup_carril"],
    "sr_punta": C["sr_punta"], "sr_st": C["sigma_st"], "y_st": C["y_st"],
    "fth_A": C["thr_A"], "fth_B": C["thr_B"], "fth_C": C["thr_C"],
    "fth_E": C["thr_E"], "fth_F": C["thr_F"],
    "n75": C["N_ciclos"], "n150": C["Nfat_carril"], "n300": C["n300"],
    "n_agota": C["n_agota_B"],
    "fsr_B150": C["FSR_B150"], "fsr_B300": C["FSR_B300"],
    "fsr_B75": C["FSR_B75"], "fsr_C150": C["FSR_catC"],
    "fsr_E150": C["FSR_catE"], "fsr_F150": C["FSR_F150"],
    "L": C["s_marco"], "wb": C["wb_ruedas"], "x1": C["x1_mm"] / 1e3,
    "a_filete": C["a_alma_ala"],
}

TINTA, SUAVE, LINEA, FONDO = "#2b2a26", "#8a8578", "#c9c4b5", "#fcfcfa"
ACENTO, FRIO, VERDE, ACERO = "#a4442c", "#2f5d7c", "#4a6b46", "#d5d7da"
MONO = "ui-monospace,'IBM Plex Mono',Menlo,Consolas,monospace"


def txt(x, y, s, color=TINTA, anchor="start", size=11, peso="normal"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" text-anchor="{anchor}" '
            f'font-size="{size}" font-weight="{peso}">{s}</text>')


def es(v: float, d: int = 5) -> str:
    return f"{v:,.{d}f}".replace(",", " ").replace(".", ",")


def ent(v: float) -> str:
    return f"{int(round(v)):,}".replace(",", " ")


def rect(x, y, w, h, fill=ACERO, sw=1.1, color=TINTA):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'fill="{fill}" stroke="{color}" stroke-width="{sw}"/>')


def linea(x1, y1, x2, y2, c=LINEA, sw=1, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{c}" stroke-width="{sw}"{d}/>')


def poli(pts, c=TINTA, sw=1.4, fill="none", dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polyline points="{p}" fill="{fill}" stroke="{c}" stroke-width="{sw}"{d}/>'


def cabeza(x, y, dx, dy, c=SUAVE, k=4.0):
    """Punta de flecha como triángulo: hay visores que ignoran <marker>."""
    n = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / n, dy / n
    px, py = -uy, ux
    return (f'<polygon points="{x:.1f},{y:.1f} {x - ux * k * 1.8 + px * k * 0.7:.1f},'
            f'{y - uy * k * 1.8 + py * k * 0.7:.1f} {x - ux * k * 1.8 - px * k * 0.7:.1f},'
            f'{y - uy * k * 1.8 - py * k * 0.7:.1f}" fill="{c}"/>')


def cota_v(x, y1, y2, etiqueta, c=SUAVE, anchor="start", dx=5, size=10):
    o = [linea(x, y1, x, y2, c, 1)]
    o.append(cabeza(x, y1, 0, -1, c))
    o.append(cabeza(x, y2, 0, 1, c))
    o.append(txt(x + dx, (y1 + y2) / 2 + 3, etiqueta, c, anchor, size))
    return o


def envoltura(w, h, alt, titulo, cuerpo):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
        f'height="{h}" role="img" aria-label="{alt}" font-family="{MONO}" '
        f'font-size="11">\n<title>{titulo}</title>\n'
        f'<rect width="{w}" height="{h}" fill="{FONDO}"/>\n'
        + "\n".join(cuerpo) + "\n</svg>\n")


# ------------------------------------------------------------------ figura 1
def categorias() -> str:
    """Los cuatro puntos de control sobre la sección, con su categoría y su umbral."""
    W, H = 760, 430
    S = 0.335                       # px por mm
    XC, Y0 = 232.0, 92.0            # eje del alma y cara superior del ala

    px = lambda mm: XC + mm * S
    py = lambda mm: Y0 + mm * S

    bfs, tfs, hw, tw = D["bfs"], D["tfs"], D["hw"], D["tw"]
    bfi, tfi, dtot = D["bfi"], D["tfi"], D["d"]

    o = [txt(24, 32, "Dos de los cuatro puntos tienen vida contada, y el que más lo está "
                     "ve menos tensión",
             TINTA, "start", 11.5, "600"),
         txt(24, 50, "cuatro puntos de control, su categoría de la Tabla A-3.1 y su umbral",
             SUAVE, "start", 10)]

    # --- la viga
    o += [
        rect(px(-bfs / 2), py(0), bfs * S, tfs * S),
        rect(px(-tw / 2), py(tfs), tw * S, hw * S),
        rect(px(-bfi / 2), py(tfs + hw), bfi * S, tfi * S),
    ]
    o.append(linea(px(-bfs / 2) - 12, py(D["ybar"]), px(bfs / 2) + 12, py(D["ybar"]),
                   FRIO, 1, "5 3"))
    xcot = px(-bfs / 2) - 24
    o += cota_v(xcot, py(0), py(D["ybar"]), es(D["ybar"]), FRIO, "end", -6, 9.5)
    o += cota_v(xcot, py(D["ybar"]), py(dtot), es(D["yinf"]), FRIO, "end", -6, 9.5)

    # --- el atiesador cortado: dos planchas a los lados del alma, corridas para
    #     que se vean como planchas y no como si el alma fuera de otro color
    yst = py(dtot - tfi - 6 - 6 * tw)
    for lado in (-1, 1):
        xa = XC + lado * (tw / 2 * S + 3.5)
        o.append(linea(xa, py(tfs + 10), xa, yst, VERDE, 2.6))
    o.append(txt(XC + 16, (py(tfs + 10) + yst) / 2, "atiesador", VERDE, "start", 9.5))
    o.append(txt(XC + 16, (py(tfs + 10) + yst) / 2 + 12, "de apoyo (del 10)",
                 VERDE, "start", 9))

    # --- los cuatro puntos, con su ficha a la derecha
    XF = 452
    puntos = [
        ("punta del ala superior", "A", D["sr_punta"], D["fth_A"],
         px(bfs / 2), py(tfs / 2), FRIO, False),
        ("soldadura alma-ala superior", "B", D["sr_sup"], D["fth_B"],
         px(tw / 2 + 4), py(tfs + 5), FRIO, False),
        ("pie del atiesador cortado", "C", D["sr_st"], D["fth_C"],
         XC + tw / 2 * S + 3.5, yst, ACENTO, True),
        ("soldadura alma-ala inferior", "B", D["sr_inf"], D["fth_B"],
         px(tw / 2 + 4), py(tfs + hw - 5), ACENTO, True),
    ]
    y = 96
    for nombre, cat, sr, fth, cx, cy, col, sobre in puntos:
        relleno = col if sobre else FONDO
        o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.6" fill="{relleno}" '
                 f'stroke="{col}" stroke-width="1.8"/>')
        o.append(linea(cx + 6, cy, XF - 12, y + 12, col, 0.8, "3 3"))
        o.append(f'<circle cx="{XF:.1f}" cy="{y + 12:.1f}" r="4.6" fill="{relleno}" '
                 f'stroke="{col}" stroke-width="1.8"/>')
        o.append(txt(XF + 14, y + 6, nombre, TINTA, "start", 10.5, "600"))
        o.append(txt(XF + 14, y + 21,
                     f'cat. {cat} · {es(sr)} · '
                     + ("SOBRE" if sobre else "bajo") + f' el umbral {ent(fth)}',
                     col, "start", 9.5, "700" if sobre else "normal"))
        y += 46

    o.append(linea(XF - 16, 88, XF - 16, 88 + 46 * 4 - 6, LINEA, 1))
    o.append(txt(XF + 14, y + 8, "MPa · los dos marcados llenos están sobre",
                 SUAVE, "start", 10))
    o.append(txt(XF + 14, y + 22, "su umbral, y no tienen vida indefinida",
                 SUAVE, "start", 10))

    # --- cotas de la sección
    o.append(txt(px(0), py(0) - 10, f'{ent(bfs)} × {ent(tfs)}', SUAVE, "middle", 9.5))
    o.append(txt(px(0), py(dtot) + 20, f'{ent(bfi)} × {ent(tfi)}', SUAVE, "middle", 9.5))
    o.append(txt(px(-tw / 2) - 8, py(tfs + hw / 2), f'{ent(hw)} × {ent(tw)}',
                 SUAVE, "end", 9.5))
    o.append(txt(24, H - 26, "el ala grande sube el eje neutro, así que el rango mayor cae abajo",
                 SUAVE, "start", 10))
    o.append(txt(24, H - 12,
                 f'y ahí AIST §5.8.1 no admite ninguna soldadura de accesorio',
                 SUAVE, "start", 10))

    alt = ("Mapa de categorias de fatiga sobre la seccion de la viga carrilera: el ala "
           "superior de 350 por 20 con su soldadura al alma en categoria B y rango de "
           "77,04436 bajo su umbral de 110, la punta del ala superior en categoria A con "
           "134,95682 bajo el suyo de 170, y los dos puntos que si estan sobre su umbral: "
           "el pie del atiesador cortado en categoria C con 98,95929 contra 69, y el ala "
           "inferior de 250 por 14 con su soldadura en categoria B y rango de 118,38827 "
           "contra 110")
    return envoltura(W, H, alt, "Dos comportamientos en la misma sección", o)


# ------------------------------------------------------------------ figura 2
def historial() -> str:
    """El historial de tensiones del ala inferior durante un paso de grúa."""
    W, H = 740, 410
    X0, X1 = 92.0, 660.0
    Y0, Y1 = 96.0, 292.0            # sigma = pico  →  sigma = 0

    L, wb = D["L"] * 1000, D["wb"] * 1000
    smax = D["sr_inf"]

    # momento bajo la primera rueda con el tren en la posición s (rueda 1 en x = s)
    def sigma(s):
        val = 0.0
        for a in (s, s + wb):       # la sección de control es la de momento máximo
            pass
        # sección de control fija en x1; momento por dos cargas unitarias
        xc = D["x1"] * 1000
        m = 0.0
        for a in (s, s + wb):
            if 0 <= a <= L:
                m += (a * (L - xc) / L if a <= xc else xc * (L - a) / L)
        return m

    # normalizado al máximo, que es el que el memo publica
    ss = [(-wb + i * (L + 2 * wb) / 400) for i in range(401)]
    vals = [sigma(s) for s in ss]
    top = max(vals) or 1.0

    fx = lambda s: X0 + (s + wb) / (L + 2 * wb) * (X1 - X0)
    fy = lambda v: Y1 - v / top * (Y1 - Y0)

    o = [txt(24, 32, "Un paso de grúa deja dos picos, y el valle entre ellos no baja a cero",
             TINTA, "start", 11.5, "600"),
         txt(24, 50, "tensión del ala inferior en la sección de momento máximo, "
                     "contra la posición del tren", SUAVE, "start", 10)]

    # ejes
    o.append(linea(X0, Y1, X1, Y1, TINTA, 1))
    o.append(linea(X0, Y0 - 14, X0, Y1, TINTA, 1))
    o.append(txt(X0 - 8, Y1 + 4, "0", SUAVE, "end", 9.5))
    o.append(txt(X0 - 8, Y0 + 4, es(smax), ACENTO, "end", 10))
    o.append(txt(X0 - 8, Y0 - 8, "MPa", SUAVE, "end", 9.5))

    o.append(poli([(fx(s), fy(v)) for s, v in zip(ss, vals)], ACENTO, 1.8))

    # los dos picos y el valle
    imax = max(range(len(vals)), key=lambda i: vals[i])
    o.append(linea(X0, Y0, X1, Y0, ACENTO, 0.8, "4 3"))

    # el segundo pico: la rueda de atrás sobre la sección de control
    s2 = D["x1"] * 1000 - wb
    v2 = sigma(s2)
    o.append(f'<circle cx="{fx(ss[imax]):.1f}" cy="{fy(vals[imax]):.1f}" r="3.6" '
             f'fill="{ACENTO}"/>')
    o.append(f'<circle cx="{fx(s2):.1f}" cy="{fy(v2):.1f}" r="3.6" fill="{FRIO}"/>')
    o.append(txt(fx(ss[imax]), fy(vals[imax]) - 12,
                 "la trasera, con la delantera aún adentro", ACENTO, "middle", 10))
    o.append(txt(fx(s2) - 6, fy(v2) - 12, "sólo la delantera", FRIO, "end", 10))

    # el valle, y el ciclo chico que el rainflow encuentra ahí
    ivalle = min(range(len(ss)), key=lambda i: (vals[i] if -600 < ss[i] < 2900 else 9e9))
    xv, yv = fx(ss[ivalle]), fy(vals[ivalle])
    o.append(f'<circle cx="{xv:.1f}" cy="{yv:.1f}" r="3.0" fill="{FONDO}" '
             f'stroke="{FRIO}" stroke-width="1.6"/>')
    xb = xv + 26
    o.append(linea(xv, yv, xb + 6, yv, FRIO, 0.8, "3 2"))
    o.append(linea(fx(s2), fy(v2), xb + 6, fy(v2), FRIO, 0.8, "3 2"))
    o += cota_v(xb, fy(v2), yv, "el ciclo chico", FRIO, "start", 8, 9.5)
    o.append(txt(xb + 8, (fy(v2) + yv) / 2 + 15, "8,6 % del rango", FRIO, "start", 9.5))

    # las dos maneras de contar, y por qué las dos tienen razón
    XB = 92
    o.append(txt(XB, 330, "§5.8.1 cuenta cada rueda:", TINTA, "start", 10.5, "600"))
    o.append(txt(XB, 346, f'2 × {ent(D["n75"])} = {ent(D["n150"])} ciclos de rango completo',
                 ACENTO, "start", 10))
    o.append(txt(XB, 364, "exacto para la soldadura, cuyo contacto sí baja a cero entre "
                          "rueda y rueda;", SUAVE, "start", 9.5))
    o.append(txt(XB, 378, "para esta curva el rainflow da un ciclo entero más uno del "
                          "8,6 %, o sea 1,00064", SUAVE, "start", 9.5))

    o.append(txt(X1, Y1 + 16, "el tren entra y sale del vano", SUAVE, "end", 9.5))
    o.append(txt(X0 + 4, Y1 + 16, f'vano de {es(D["L"], 2)} m · ruedas a {es(D["wb"], 2)} m',
                 SUAVE, "start", 9.5))

    alt = ("Historial de tensiones del ala inferior durante un paso de grua sobre el vano "
           "de 7,50 m con ruedas a 3,40 m: dos picos, uno por cada rueda, con el rango "
           "completo de 118,38827 y el valle intermedio sin bajar a cero, el ciclo chico "
           "del 8,6 por ciento que el rainflow encuentra ahi, y el conteo de 75 000 pasos "
           "que se duplica a 150 000 ciclos")
    return envoltura(W, H, alt, "Dos picos por paso", o)


# ------------------------------------------------------------------ figura 3
def curvas() -> str:
    """Las cuatro curvas S-N con los tres conteos y los dos umbrales."""
    W, H = 820, 440
    X0, X1 = 96.0, 610.0
    Y0, Y1 = 82.0, 320.0

    n_lo, n_hi = 2e4, 5e6
    s_lo, s_hi = 20.0, 500.0

    fx = lambda n: X0 + (math.log10(n) - math.log10(n_lo)) / (
        math.log10(n_hi) - math.log10(n_lo)) * (X1 - X0)
    fy = lambda s: Y1 - (math.log10(s) - math.log10(s_lo)) / (
        math.log10(s_hi) - math.log10(s_lo)) * (Y1 - Y0)

    o = [txt(24, 32, "La recta de la categoría B cruza el rango del ala inferior "
                     "muy lejos del conteo de diseño",
             TINTA, "start", 11.5, "600"),
         txt(24, 50, "curvas S-N de la Ec. A-3-1M, con el umbral de vida indefinida como "
                     "horizontal", SUAVE, "start", 10)]

    # rejilla de décadas
    for k in (4, 5, 6):
        for m in range(1, 10):
            n = m * 10 ** k
            if n_lo <= n <= n_hi:
                o.append(linea(fx(n), Y0, fx(n), Y1, LINEA, 0.5 if m > 1 else 0.9))
    for s in (20, 50, 100, 200):
        if s_lo <= s <= s_hi:
            o.append(linea(X0, fy(s), X1, fy(s), LINEA, 0.5))
            o.append(txt(X0 - 8, fy(s) + 4, ent(s), SUAVE, "end", 9.5))
    o.append(txt(X0 - 8, Y0 - 10, "MPa", SUAVE, "end", 9.5))

    # las cuatro curvas: la sloped mientras esté sobre su umbral y dentro del lienzo,
    # y la horizontal del umbral SÓLO si la curva llega a él dentro de la ventana.
    def curva(nombre, ley, fth, col, dash=""):
        pts, n, tocaEn = [], n_lo, None
        while n <= n_hi:
            s = ley(n)
            if s < fth:
                tocaEn = tocaEn or n
                break
            if s <= s_hi:
                pts.append((fx(n), fy(s)))
            n *= 1.04
        o.append(poli(pts, col, 1.6, dash=dash))
        if tocaEn:
            o.append(linea(fx(tocaEn), fy(fth), X1, fy(fth), col, 1.2, "6 3"))
            o.append(txt(X1 + 8, fy(fth) + 4, f'{nombre} · umbral {ent(fth)}',
                         col, "start", 10))
        else:
            o.append(txt(pts[-1][0] + 6, pts[-1][1] + 4,
                         f'{nombre} · umbral {ent(fth)}, más a la derecha', col, "start", 9.5))

    curva("B", lambda n: 6900 * (12.0 / n) ** 0.333, D["fth_B"], ACENTO)
    curva("C", lambda n: 6900 * (4.4 / n) ** 0.333, D["fth_C"], VERDE)
    curva("E", lambda n: 6900 * (1.1 / n) ** 0.333, D["fth_E"], FRIO)
    curva("F", lambda n: 690 * (1.5 / n) ** 0.167, D["fth_F"], SUAVE, dash="5 3")

    # los tres conteos
    for n, etiqueta, col in ((D["n75"], "75 000", SUAVE), (D["n150"], "150 000", TINTA),
                             (D["n300"], "300 000", SUAVE)):
        o.append(linea(fx(n), Y0, fx(n), Y1 + 6, col, 1.1, "3 3"))
        o.append(txt(fx(n), Y1 + 20, etiqueta, col, "middle", 9.5))

    # el rango del ala inferior y el cruce
    o.append(linea(X0, fy(D["sr_inf"]), X1, fy(D["sr_inf"]), ACENTO, 1.6))
    o.append(txt(X0 + 6, fy(D["sr_inf"]) - 24, f'{es(D["sr_inf"])} · rango del ala inferior',
                 ACENTO, "start", 10))
    o.append(linea(X0 + 6, fy(D["sr_inf"]) - 20, X0 + 6, fy(D["sr_inf"]) - 2, ACENTO, 0.8))
    o.append(f'<circle cx="{fx(D["n_agota"]):.1f}" cy="{fy(D["sr_inf"]):.1f}" r="4.2" '
             f'fill="{ACENTO}"/>')
    o.append(linea(fx(D["n_agota"]), fy(D["sr_inf"]), fx(D["n_agota"]), Y1 + 6,
                   ACENTO, 1.1, "3 3"))
    o.append(txt(fx(D["n_agota"]), Y1 + 20, ent(D["n_agota"]), ACENTO, "middle", 9.5))
    o.append(txt(fx(D["n_agota"]), Y1 + 33, "se agota", ACENTO, "middle", 9))

    o.append(f'<circle cx="{fx(D["n150"]):.1f}" cy="{fy(D["fsr_B150"]):.1f}" r="3.4" '
             f'fill="{FONDO}" stroke="{ACENTO}" stroke-width="1.6"/>')
    o.append(txt(fx(D["n150"]) + 8, fy(D["fsr_B150"]) - 6, es(D["fsr_B150"]),
                 ACENTO, "start", 9.5))

    o.append(linea(X0, Y1, X1, Y1, TINTA, 1))
    o.append(linea(X0, Y0, X0, Y1, TINTA, 1))
    o.append(txt(X1, Y1 + 36, "ciclos", SUAVE, "end", 10))
    o.append(txt(24, H - 42, "el rango del ala inferior queda SOBRE la horizontal de 110:",
                 TINTA, "start", 10))
    o.append(txt(24, H - 28, "no hay vida indefinida, y la recta dice a cuántos ciclos "
                             "se agota", SUAVE, "start", 10))
    o.append(txt(24, H - 14, f'el filete se verifica en la curva F, con {es(D["fsr_F150"])} '
                             f'a los 150 000', SUAVE, "start", 10))

    alt = ("Curvas S-N de las categorias B, C, E y F contra el numero de ciclos, con los "
           "umbrales de vida indefinida en 110, 69, 31 y 55, los tres conteos de 75 000, "
           "150 000 y 300 000 marcados, el admisible de 298,24835 sobre la curva B a los "
           "150 000, y el rango de 118,38827 del ala inferior cruzando la curva B a los "
           "2 404 941 ciclos")
    return envoltura(W, H, alt, "Dónde cruza el rango del ala inferior", o)

if __name__ == "__main__":
    escribir(AQUI, {"categorias": categorias(), "historial": historial(),
                    "curvas": curvas()})
