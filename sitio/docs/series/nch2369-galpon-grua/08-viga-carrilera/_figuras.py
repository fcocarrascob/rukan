"""Las tres figuras del eslabon 08.

    python sitio/docs/series/nch2369-galpon-grua/08-viga-carrilera/_figuras.py

Portadas del repo de memos, con la diferencia de fondo del sitio: las cotas se
leen del `valores.json` del eslabon (`figuras.cotas`), no se teclean. La figura
no ilustra: comprueba.

**La primera existe para que se vea de donde sale la torsion.** La seccion va a
escala real en las dos direcciones, riel incluido, asi que se ve que el brazo del
empuje lateral -- desde la cabeza del riel hasta el centro del ala superior -- es
mas largo que el ala es gruesa, y que la excentricidad que la tolerancia de
montaje admite es minuscula y aun asi pone un tercio del par.

**La segunda muestra que las tres posiciones de rueda que gobiernan son tres
posiciones distintas.** La de momento maximo no es la de reaccion maxima ni la de
flecha maxima, y un modelo que evalue una sola se equivoca en las otras dos. El
visor de `modelos/carrilera` dibuja el diagrama de la primera; esta figura es la
que pone las tres juntas.

**La tercera pone las cuatro flechas de servicio contra sus limites en la misma
escala**, y agrega la que ninguna clausula mira: la suma de la deriva del marco y
la flecha de la viga, que ocurre en el mismo punto fisico.
"""

from __future__ import annotations

import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from figuras import cotas, escribir  # noqa: E402

C = cotas(AQUI)

# El puente entre los nombres cortos del dibujo y los simbolos del eslabon.
# Ninguna cifra nace aqui: todas salen del `valores.json`.
D = {
    "bfs": C["bfs_carril"], "tfs": C["tfs_carril"], "hw": C["hw_carril"],
    "tw": C["tw_carril"], "bfi": C["bfi_carril"], "tfi": C["tfi_carril"],
    "d": C["d_carril"], "ybar": C["ybar_carril"], "ho": C["h_o"],
    "d_riel": C["h_riel_perfil"], "e_riel": C["e_riel"],
    "L": C["s_marco"], "wb": C["wb_ruedas"], "x1": C["x1_rueda"],
    "x2": C["x2_rueda"], "b_flecha": C["b_flecha"],
    "c_mom": C["coef_077"], "c_reac": C["coef_reac"],
    "Mux": C["M_ux"], "R": C["R_serv"], "dv": C["delta_v"],
    "lim_C": C["dlim_v_C"], "lim_B": C["dlim_v_B"], "lim_lat": C["dlim_lat"],
    "dl_cmaa": C["delta_l_CMAA"], "dl_aist": C["delta_l_AIST"],
    "d_marco": C["d_riel_grua"], "d_total": C["d_total_riel"],
}

TINTA, SUAVE, LINEA, FONDO = "#2b2a26", "#8a8578", "#c9c4b5", "#fcfcfa"
ACENTO, FRIO, VERDE, ACERO, RIEL = (
    "#a4442c", "#2f5d7c", "#4a6b46", "#d5d7da", "#b3b6ba")
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


def cabeza(x, y, dx, dy, c=SUAVE, k=4.0):
    """Punta de flecha como triángulo: hay visores que ignoran <marker>."""
    n = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / n, dy / n
    px, py = -uy, ux
    return (f'<polygon points="{x:.1f},{y:.1f} {x - ux * k * 1.8 + px * k * 0.7:.1f},'
            f'{y - uy * k * 1.8 + py * k * 0.7:.1f} {x - ux * k * 1.8 - px * k * 0.7:.1f},'
            f'{y - uy * k * 1.8 - py * k * 0.7:.1f}" fill="{c}"/>')


def cota_h(x1, x2, y, etiqueta, c=SUAVE, size=10):
    o = [linea(x1, y, x2, y, c, 1)]
    o.append(cabeza(x1, y, -1, 0, c))
    o.append(cabeza(x2, y, 1, 0, c))
    o.append(txt((x1 + x2) / 2, y - 4, etiqueta, c, "middle", size))
    return o


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
def seccion() -> str:
    """La sección con el riel encima, a escala real en las dos direcciones."""
    W, H = 720, 470
    S = 0.345                       # px por mm
    XC, Y0 = 300.0, 122.0           # eje del alma y cara superior del ala

    px = lambda mm: XC + mm * S
    py = lambda mm: Y0 + mm * S

    bfs, tfs, hw, tw = D["bfs"], D["tfs"], D["hw"], D["tw"]
    bfi, tfi, dtot = D["bfi"], D["tfi"], D["d"]
    dr, er = D["d_riel"], D["e_riel"]

    o = [txt(24, 30, "El brazo de torsión no está en la viga: está en el riel y en su tolerancia",
             TINTA, "start", 11.5, "600"),
         txt(24, 48, "sección a escala real · el empuje lateral entra en la cabeza del riel",
             SUAVE, "start", 10)]

    # --- el riel, desplazado su excentricidad máxima
    xr = XC + er * S
    hcab, hpat = dr * 0.30, dr * 0.28
    o += [
        rect(px(-66) + er * S, py(-dr), 66 * 2 * S, hcab * S, RIEL),          # cabeza
        rect(xr - 9 * S, py(-dr) + hcab * S, 18 * S, (dr - hcab - hpat) * S, RIEL),  # alma
        rect(px(-66) + er * S, py(-hpat), 66 * 2 * S, hpat * S, RIEL),        # patín
    ]

    # --- la viga
    o += [
        rect(px(-bfs / 2), py(0), bfs * S, tfs * S),
        rect(px(-tw / 2), py(tfs), tw * S, hw * S),
        rect(px(-bfi / 2), py(tfs + hw), bfi * S, tfi * S),
    ]

    # --- eje del alma y eje del riel, que no coinciden
    o.append(linea(XC, py(-dr) - 16, XC, py(dtot) + 14, SUAVE, 0.9, "3 3"))
    o.append(linea(xr, py(-dr) - 16, xr, py(0) - 4, ACENTO, 0.9, "3 3"))
    o.append(txt(xr + 26, py(-dr) - 20, f'e = {es(er, 2)} mm', ACENTO, "start", 10))
    o.append(txt(xr + 26, py(-dr) - 8, "(tres cuartos del alma)", ACENTO, "start", 9.5))
    o.append(linea(xr + 3, py(-dr) - 24, xr + 24, py(-dr) - 24, ACENTO, 0.9))

    # --- el empuje lateral en la cabeza del riel
    yh = py(-dr) + hcab * S / 2
    o.append(linea(px(-155), yh, px(-72), yh, ACENTO, 1.6))
    o.append(cabeza(px(-72), yh, 1, 0, ACENTO, 5))
    o.append(txt(px(-160), yh + 4, "empuje lateral", ACENTO, "end", 10))

    # --- centro de gravedad
    yg = py(D["ybar"])
    o.append(linea(px(-bfs / 2) - 34, yg, px(bfs / 2) + 12, yg, FRIO, 1.1, "5 3"))
    o.append(f'<circle cx="{XC:.1f}" cy="{yg:.1f}" r="3.2" fill="{FRIO}"/>')
    o.append(txt(px(bfs / 2) + 18, yg - 3, "centro de gravedad", FRIO, "start", 10))
    o.append(txt(px(bfs / 2) + 18, yg + 10, f'{es(D["ybar"])} mm', FRIO, "start", 10))

    # --- cotas verticales a la izquierda
    xL = px(-bfs / 2) - 30
    o += cota_v(xL, py(0), yg, f'{es(D["ybar"])}', SUAVE, "end", -6)
    xL2 = px(-bfs / 2) - 76
    o += cota_v(xL2, py(0), py(dtot), f'{ent(dtot)}', TINTA, "end", -6)
    o.append(txt(xL2 - 6, py(dtot) + 14, "canto total", SUAVE, "end", 9.5))

    # --- ho, entre centroides de ala, a la derecha
    xR = px(bfs / 2) + 128
    o += cota_v(xR, py(tfs / 2), py(dtot - tfi / 2), f'{ent(D["ho"])}', VERDE, "start", 6)
    o.append(txt(xR + 6, py(dtot - tfi / 2) - 6, "entre centroides", VERDE, "start", 9.5))
    o.append(txt(xR + 6, py(dtot - tfi / 2) + 6, "de ala", VERDE, "start", 9.5))
    o.append(linea(px(bfs / 2) + 34, py(tfs / 2), xR, py(tfs / 2), LINEA, 0.8, "3 3"))
    o.append(linea(px(bfi / 2) + 60, py(dtot - tfi / 2), xR, py(dtot - tfi / 2), LINEA, 0.8, "3 3"))

    # --- cotas horizontales, apiladas abajo para no chocar con el pie del riel
    o.append(linea(px(-bfs / 2), py(tfs), px(-bfs / 2), py(dtot) + 46, LINEA, 0.8, "3 3"))
    o.append(linea(px(bfs / 2), py(tfs), px(bfs / 2), py(dtot) + 46, LINEA, 0.8, "3 3"))
    o += cota_h(px(-bfi / 2), px(bfi / 2), py(dtot) + 26, f'{ent(bfi)}', TINTA)
    o += cota_h(px(-bfs / 2), px(bfs / 2), py(dtot) + 50, f'{ent(bfs)}', TINTA)

    # --- espesores
    o.append(txt(px(bfs / 2) + 8, py(tfs / 2) + 4, f'{ent(tfs)}', TINTA, "start", 10))
    o.append(txt(px(tw / 2) + 10, py(tfs + hw / 2), f'alma {ent(tw)}', TINTA, "start", 10))
    o.append(txt(px(tw / 2) + 10, py(tfs + hw / 2) + 13, f'{ent(D["hw"])} de alto', SUAVE, "start", 9.5))
    o.append(txt(px(bfi / 2) + 8, py(dtot - tfi / 2) + 4, f'{ent(tfi)}', TINTA, "start", 10))
    o.append(txt(px(66) + 14 + er * S, py(-dr) + 8, f'riel {es(dr, 2)} de alto', RIEL, "start", 10))

    o.append(txt(24, H - 30, "el ala superior es el doble del área de la inferior:",
                 SUAVE, "start", 10))
    o.append(txt(24, H - 16, "por eso el centro de gravedad sube y el ala traccionada fluye primero",
                 SUAVE, "start", 10))

    alt = ("Seccion transversal de la viga carrilera con el riel encima, a escala: ala "
           "superior de 350 por 20, alma de 650 por 8, ala inferior de 250 por 14, canto "
           "total 684, centro de gravedad a 269,64968 de la fibra superior, 667 entre "
           "centroides de ala y el riel desplazado 6,00 respecto del eje del alma")
    return envoltura(W, H, alt, "De dónde sale la torsión de la carrilera", o)


# ------------------------------------------------------------------ figura 2
def posiciones() -> str:
    """Las tres posiciones de rueda que gobiernan, sobre el mismo vano."""
    W, H = 720, 400
    ESC = 46.0                      # px por metro
    X0 = 204.0
    L, wb = D["L"], D["wb"]
    px = lambda m: X0 + m * ESC

    o = [txt(24, 30, "Tres posiciones de rueda, tres resultados: ninguna sirve para las otras dos",
             TINTA, "start", 11.5, "600")]

    def apoyo(x, y):
        return (f'<polygon points="{x:.1f},{y:.1f} {x - 7:.1f},{y + 11:.1f} '
                f'{x + 7:.1f},{y + 11:.1f}" fill="{TINTA}"/>')

    def rueda(x, y, c=ACENTO):
        return (f'<circle cx="{x:.1f}" cy="{y - 9:.1f}" r="7" fill="{FONDO}" '
                f'stroke="{c}" stroke-width="1.6"/>')

    paneles = [
        ("momento máximo", [D["x1"], D["x2"]], ACENTO,
         f'M = {es(D["Mux"])} kN·m', f'reacción {es(D["c_mom"])} por rueda'),
        ("reacción máxima", [0.0, wb], FRIO,
         f'R = {es(D["R"])} kN', f'coeficiente {es(D["c_reac"])}'),
        ("flecha máxima", [(L - wb) / 2, (L + wb) / 2], VERDE,
         f'flecha {es(D["dv"])} mm', f'{ent(D["b_flecha"])} mm a cada apoyo'),
    ]

    y = 88
    for nombre, xs, col, res, nota in paneles:
        o.append(linea(px(0), y, px(L), y, TINTA, 1.6))
        o.append(apoyo(px(0), y))
        o.append(apoyo(px(L), y))
        o.append(txt(X0 - 18, y - 6, nombre, TINTA, "end", 10.5, "600"))
        o.append(txt(X0 - 18, y + 8, nota, SUAVE, "end", 9.5))
        for xr in xs:
            o.append(rueda(px(xr), y, col))
            o.append(linea(px(xr), y - 26, px(xr), y - 18, col, 1.4))
            o.append(cabeza(px(xr), y - 18, 0, 1, col, 4))
        o.append(txt(px(L) + 16, y + 4, res, col, "start", 10.5))
        # la cota de la base de ruedas
        o += cota_h(px(xs[0]), px(xs[1]), y + 30, f'{es(wb, 2)} m', SUAVE, 9.5)
        y += 104

    # el vano, una sola vez, abajo
    o += cota_h(px(0), px(L), y - 34, f'vano {es(L, 2)} m', TINTA, 10.5)
    o.append(txt(24, H - 16,
                 "la de momento máximo pone la primera rueda a 2,90 m y la segunda a 6,30; "
                 "la de flecha las deja simétricas",
                 SUAVE, "start", 10))

    alt = ("Tres elevaciones del mismo vano de 7,50 metros con las dos ruedas a 3,40 de "
           "separacion en las tres posiciones que gobiernan: momento maximo con la primera "
           "rueda a 2,90, reaccion maxima con una rueda sobre el apoyo, y flecha maxima con "
           "las dos simetricas respecto del centro")
    return envoltura(W, H, alt, "Las tres posiciones de rueda que gobiernan", o)


# ------------------------------------------------------------------ figura 3
def flechas() -> str:
    """Las cuatro flechas de servicio contra sus límites, en la misma escala."""
    W, H = 720, 330
    X0, ESC = 264.0, 19.0           # px por mm
    px = lambda mm: X0 + mm * ESC

    o = [txt(24, 30, "La flecha que la cabeza del riel realmente ve no la mide ninguna cláusula",
             TINTA, "start", 11.5, "600")]

    # los dos límites verticales y el lateral
    for v, c, nombre, lado in (
            (D["lim_B"], SUAVE, "clase B · L/1000", "end"),
            (D["lim_C"], VERDE, "clase C · L/600", "start"),
            (D["lim_lat"], ACENTO, "lateral · L/400", "start")):
        o.append(linea(px(v), 58, px(v), 250, c, 1.4, "4 3"))
        o.append(txt(px(v) + (6 if lado == "start" else -6), 52, nombre, c, lado, 10))
        o.append(txt(px(v) + (6 if lado == "start" else -6), 268, es(v, 2), c, lado, 10))

    filas = [
        
        ("flecha lateral · CMAA 10 %", D["dl_cmaa"], ACENTO, "uso 0,781 · gobierna"),
        ("flecha lateral · AIST 30 %", D["dl_aist"], SUAVE, "uso 0,727"),
        ("marco + viga · en la cabeza", D["d_total"], FRIO, "0,945 · nadie la mide"),
    ]
    y = 76
    for nombre, v, col, nota in filas:
        o.append(f'<rect x="{X0}" y="{y}" width="{max(px(v) - X0, 1.5):.1f}" height="22" '
                 f'fill="{col}" opacity="0.85"/>')
        o.append(txt(X0 - 10, y + 9, nombre, TINTA, "end", 10.5))
        o.append(txt(X0 - 10, y + 22, nota, SUAVE, "end", 9.5))
        lx = max(px(v) + 8, px(D["lim_lat"]) + 14)
        o.append(txt(lx, y + 15, es(v), col, "start", 10.5))
        y += 44

    # la barra de la suma se compone: marco + viga
    o.append(f'<rect x="{X0}" y="{y - 44}" width="{px(D["d_marco"]) - X0:.1f}" height="22" '
             f'fill="{TINTA}" opacity="0.55"/>')
    o.append(txt(X0 + 6, y - 29, "marco", FONDO, "start", 9))

    o.append(linea(X0, 58, X0, 256, TINTA, 1))
    o.append(txt(X0 - 10, 268, "mm", SUAVE, "end", 10))
    o.append(txt(24, H - 30, "los dos 18,75 son el mismo número por dos caminos:",
                 SUAVE, "start", 10))
    o.append(txt(24, H - 16, "h/400 al riel y L/400 sobre el vano — y sus demandas se suman",
                 SUAVE, "start", 10))

    alt = ("Cuatro flechas de servicio de la viga carrilera contra sus limites en la misma "
           "escala de milimetros: la vertical de 8,26725 contra 12,50 y 7,50, la lateral de "
           "14,64206 con la fuerza de CMAA y 13,62144 con la de AIST contra 18,75, y la suma "
           "de la deriva del marco con la flecha de la viga, 17,72361, contra el mismo 18,75 "
           "que ninguna clausula aplica a la suma")
    return envoltura(W, H, alt, "La flecha que nadie mide", o)

if __name__ == "__main__":
    escribir(AQUI, {"seccion": seccion(), "posiciones": posiciones(),
                    "flechas": flechas()})
