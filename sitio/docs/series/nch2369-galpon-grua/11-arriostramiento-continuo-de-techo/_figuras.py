"""Las tres figuras del eslabon 11.

    python sitio/docs/series/nch2369-galpon-grua/11-arriostramiento-continuo-de-techo/_figuras.py

Portadas del repo de memos, con las cotas leidas del `valores.json` del eslabon
(`figuras.cotas`) en vez de tecleadas.

**La primera existe para que se vea por que el techo se subdivide.** Es la planta
**desarrollada** —las dos aguas abatidas sobre el papel, asi que la altura del
dibujo es longitud de rafter y no luz— con los cuatro vanos, las siete lineas de
puntal y las X de los 24 paneles, y encima, en trazos, la diagonal del agua
entera que el tope de esbeltez descarta. Puestas en el mismo dibujo se ve que la
subdivision no es una preferencia de traza: es lo unico que cabe.

**La segunda pone las dos longitudes de pandeo a la misma escala.** La linea de
trazos bajo cada barra es el largo real del miembro y la barra es su longitud de
pandeo: la diagonal usa la mitad porque tiene cruce, el puntal el entero porque
no lo tiene. Es la razon de que el puntal sea el miembro grueso del sistema pese
a llevar la septima parte de fuerza.

**La tercera pone las cuatro demandas de fuerza sobre el mismo nudo**, contra la
capacidad de la diagonal, para que se vea que la que gobierna no es la sismica
sino la de estabilidad del rafter acumulada. El empuje de grua **no** aparece
como barra a proposito: es una demanda de rigidez y no de fuerza, y el pie lo
dice.

Ninguna la reemplaza el visor: el modelo del sitio tiene el techo arriostrado y
lo dibuja en 3D, pero no abate las dos aguas sobre el papel, no rotula longitudes
de pandeo y no pone las cuatro demandas en la misma escala.
"""

from __future__ import annotations

import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from figuras import cotas, escribir  # noqa: E402

C = cotas(AQUI)


def es(v: float, d: int = 5) -> str:
    return f"{v:,.{d}f}".replace(",", "\0").replace(".", ",").replace("\0", " ")


# El puente entre los nombres cortos del dibujo y los simbolos del eslabon.
D = {
    "vano": C["vano_mm"], "vano_s": es(C["vano_mm"], 0), "n_vanos": 4, "n_marcos": 5,
    "largo": es(C["L_total"], 2), "luz": es(C["L_luz"], 2), "Lr": es(C["Lr_mm"], 2),
    "bpan": es(C["b_pan_techo"], 2), "Ld": es(C["L_diag_techo"], 2),
    "Ldagua": es(C["Ld_agua"], 2), "KL": es(C["KL_diag"], 2),
    "rmin": es(C["r_req"]), "rminp": es(C["r_req_punt"]), "rmina": es(C["r_agua"]),
    "lam": es(C["lam_glob"]), "n_lin": int(C["n_lin"]), "n_pan": int(C["n_pan"]),
    "n_diag": int(C["n_diag"]),
    "esbD": es(C["esb_diag"]), "usoD": es(C["uso_esb_diag"]),
    "esbP": es(C["esb_punt"]), "usoP": es(C["uso_esb_punt"]),
    "phiPn": es(C["phiPn_diag"]),
    "Bd": es(C["B_diag"], 0), "td": es(C["t_diag"], 0),
    "Bp": es(C["B_punt"], 0), "tp": es(C["t_punt"], 0),
    "SS": es(C["SS_marco"]), "Praf": es(C["Pbr_raf"]), "Pcol": es(C["Pbr_col"]),
    "usoGrua": es(C["uso_grua_real"]), "Pacum": es(C["Pbr_acum"]),
    "Pdiag": es(C["N_diag_acum"]), "Fdiag": es(C["N_diag_sismo"]),
    "Lsup": es(C["L_br_col"], 2), "rho": es(C["rho_diaf"]),
    "razon": es(C["supera_sismica"]),
}

TINTA, SUAVE, LINEA, FONDO = "#2b2a26", "#8a8578", "#c9c4b5", "#fcfcfa"
ACENTO, FRIO, VERDE, ACERO = "#a4442c", "#2f5d7c", "#4a6b46", "#d5d7da"
MONO = "ui-monospace,'IBM Plex Mono',Menlo,Consolas,monospace"


def txt(x, y, s, color=TINTA, anchor="start", size=11, peso="normal"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" text-anchor="{anchor}" '
            f'font-size="{size}" font-weight="{peso}">{s}</text>')


def linea(x1, y1, x2, y2, c=LINEA, sw=1, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{c}" stroke-width="{sw}"{d}/>')


def rect(x, y, w, h, fill=ACERO, sw=1.1, color=TINTA):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'fill="{fill}" stroke="{color}" stroke-width="{sw}"/>')


def cabeza(x, y, dx, dy, c=SUAVE, k=4.0):
    n = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / n, dy / n
    px, py = -uy, ux
    return (f'<polygon points="{x:.1f},{y:.1f} {x - ux * k * 1.8 + px * k * 0.7:.1f},'
            f'{y - uy * k * 1.8 + py * k * 0.7:.1f} {x - ux * k * 1.8 - px * k * 0.7:.1f},'
            f'{y - uy * k * 1.8 - py * k * 0.7:.1f}" fill="{c}"/>')


def cota_h(y, x1, x2, etiqueta, c=SUAVE, dy=-6, size=10, anchor="middle"):
    return [linea(x1, y, x2, y, c, 1), cabeza(x1, y, -1, 0, c), cabeza(x2, y, 1, 0, c),
            txt((x1 + x2) / 2, y + dy, etiqueta, c, anchor, size)]


def cota_v(x, y1, y2, etiqueta, c=SUAVE, anchor="start", dx=6, size=10):
    return [linea(x, y1, x, y2, c, 1), cabeza(x, y1, 0, -1, c), cabeza(x, y2, 0, 1, c),
            txt(x + dx, (y1 + y2) / 2 + 3, etiqueta, c, anchor, size)]


def envoltura(w, h, alt, titulo, cuerpo):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
        f'height="{h}" role="img" aria-label="{alt}" font-family="{MONO}" '
        f'font-size="11">\n<title>{titulo}</title>\n'
        f'<rect width="{w}" height="{h}" fill="{FONDO}"/>\n'
        + "\n".join(cuerpo) + "\n</svg>\n")


# ------------------------------------------------------------------ figura 1
def planta() -> str:
    W, H = 880, 600
    x0, x1 = 150.0, 750.0                    # 30,00 m de largo
    y0, y1 = 116.0, 416.0                    # dos aguas desarrolladas, alero a alero
    dx = (x1 - x0) / 4                       # un vano
    yc = (y0 + y1) / 2                       # la cumbrera
    dy = (yc - y0) / 3                       # un panel, sobre el rafter
    p = [
        txt(24, 30, "El arriostramiento es continuo porque sin corte en los cuatro "
                    "vanos no hay redistribucion", TINTA, "start", 11.5, "600"),
        txt(24, 48, "planta desarrollada del techo   ·   las dos aguas abatidas sobre "
                    "el papel, asi que la altura del dibujo es longitud de rafter y no luz",
            SUAVE, "start", 10),
    ]
    for k in range(7):                       # las siete lineas de puntal
        y = y0 + k * dy
        p.append(linea(x0, y, x1, y, TINTA, 1.9 if k in (0, 3, 6) else 1.3))
    for k in range(5):                       # los cinco marcos
        x = x0 + k * dx
        p.append(linea(x, y0, x, y1, FRIO, 1.6))
        p.append(txt(x, y1 + 20, f"M{k + 1}", FRIO, "middle", 10, "600"))
    for i in range(4):                       # las X de los 24 paneles
        for j in range(6):
            xa, xb = x0 + i * dx, x0 + (i + 1) * dx
            ya, yb = y0 + j * dy, y0 + (j + 1) * dy
            p.append(linea(xa, ya, xb, yb, ACENTO, 1.0))
            p.append(linea(xa, yb, xb, ya, ACENTO, 1.0))
    p.append(linea(x0, y0, x0 + dx, yc, VERDE, 2.4, "8 4"))              # la descartada
    p.append(linea(x0 + 2 * dx, y0, x0 + 3 * dx, y0 + dy, ACENTO, 2.8))  # la adoptada
    p.append(txt(x0 - 12, y0 + 4, "alero", SUAVE, "end", 10))
    p.append(txt(x0 - 12, yc + 4, "cumbrera", SUAVE, "end", 10))
    p.append(txt(x0 - 12, y1 + 4, "alero", SUAVE, "end", 10))
    p += cota_v(x1 + 30, y0, y0 + dy, D["bpan"])
    p += cota_v(x0 - 76, y0, yc, D["Lr"], anchor="end", dx=-6)
    p += cota_h(y1 + 46, x0, x0 + dx, D["vano_s"])
    p += cota_h(y1 + 76, x0, x1, D["largo"] + " m")
    ly = H - 80                              # la leyenda, donde no tapa nada
    p.append(linea(28, ly - 4, 68, ly - 4, VERDE, 2.4, "8 4"))
    p.append(txt(76, ly, f"la diagonal del agua entera: {D['Ldagua']} mm, que pediria "
                         f"r ≥ {D['rmina']} mm y no existe en tubo", VERDE, "start", 10))
    p.append(linea(28, ly + 18, 68, ly + 18, ACENTO, 2.8))
    p.append(txt(76, ly + 22, f"la diagonal adoptada: {D['Ld']} mm sobre un vano de "
                              f"{D['vano_s']} y un panel de {D['bpan']}",
                 ACENTO, "start", 10))
    p.append(txt(28, ly + 46, f"{D['n_lin']} lineas de puntal   ·   {D['n_pan']} paneles"
                              f"   ·   {D['n_diag']} diagonales   ·   los dos vanos "
                              f"con porton llevan X igual   ·   luz {D['luz']} m en "
                              f"proyeccion", SUAVE, "start", 10))
    alt = ("Planta desarrollada del arriostramiento de techo con los cuatro vanos de 7 500 mm "
           "entre cinco marcos, las siete lineas de puntal separadas 4 249,18 mm sobre los "
           "12 747,55 mm de rafter, las X de los 24 paneles con su diagonal de 8 620,07 mm, y "
           "en trazos la diagonal del agua entera de 14 790,20 mm, que pediria un radio de "
           "giro de 130,35494 y no existe en tubo")
    return envoltura(W, H, alt, "Planta del arriostramiento de techo", p)


# ------------------------------------------------------------------ figura 2
def panel() -> str:
    W, H = 880, 410
    p = [
        txt(24, 30, "El punto de cruce vale exactamente 2 en la diagonal y cero en el "
                    "puntal", TINTA, "start", 11.5, "600"),
        txt(24, 48, "un panel arriostrado   ·   las dos longitudes de pandeo a la misma "
                    "escala, contra el tope de esbeltez de " + D["lam"], SUAVE, "start", 10),
    ]
    ax0, ax1, ay0, ay1 = 96.0, 396.0, 108.0, 278.0
    p.append(rect(ax0, ay0, ax1 - ax0, ay1 - ay0, "none", 1.6, TINTA))
    p.append(linea(ax0, ay0, ax1, ay1, ACENTO, 2.4))
    p.append(linea(ax0, ay1, ax1, ay0, ACENTO, 1.4, "6 4"))
    cx, cy = (ax0 + ax1) / 2, (ay0 + ay1) / 2
    p.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5.5" fill="{FONDO}" '
             f'stroke="{ACENTO}" stroke-width="1.8"/>')
    p.append(txt(cx + 30, cy - 34, "cruce §8.8.3", ACENTO, "start", 10, "600"))
    p.append(linea(cx + 5, cy - 5, cx + 28, cy - 30, ACENTO, 0.9))
    p.append(txt(cx + 30, cy - 21, "una diagonal continua", ACENTO, "start", 9.5))
    p += cota_h(ay1 + 34, ax0, ax1, D["vano_s"])
    p += cota_v(ax1 + 30, ay0, ay1, D["bpan"])
    p.append(txt(ax0, ay0 - 12, "diagonal " + D["Ld"], TINTA, "start", 10, "600"))
    bx0, ancho = 500.0, 300.0                # escala comun: 300 px son 8 620,07 mm
    esc = ancho / C["L_diag_techo"]
    barras = [
        (f"diagonal {D['Bd']} × {D['Bd']} × {D['td']}", "KL = " + D["KL"],
         C["L_diag_techo"], C["KL_diag"], D["esbD"], D["usoD"], ACENTO),
        (f"puntal {D['Bp']} × {D['Bp']} × {D['tp']}", "KL = " + D["vano_s"],
         C["vano_mm"], C["vano_mm"], D["esbP"], D["usoP"], FRIO),
    ]
    for k, (etq, sub, L, KL, esb, uso, color) in enumerate(barras):
        y = 122.0 + k * 92
        p.append(txt(bx0, y - 12, etq, TINTA, "start", 10.5, "600"))
        p.append(linea(bx0, y + 26, bx0 + L * esc, y + 26, LINEA, 1, "4 3"))
        p.append(rect(bx0, y, KL * esc, 16, color, 1.0, TINTA))
        p.append(txt(bx0, y + 44, sub, SUAVE, "start", 10))
        p.append(txt(bx0, y + 60, f"esbeltez {esb}   ·   uso {uso}", SUAVE, "start", 10))
    p.append(txt(bx0, 320, "el radio de giro que el tope pide", SUAVE, "start", 10))
    p.append(txt(bx0, 338, f"diagonal   r ≥ {D['rmin']} mm", ACENTO, "start", 10.5, "600"))
    p.append(txt(bx0, 356, f"puntal     r ≥ {D['rminp']} mm", FRIO, "start", 10.5, "600"))
    p.append(txt(24, H - 26, "la linea de trazos bajo cada barra es el largo real del "
                             "miembro y la barra es su longitud de pandeo",
                 SUAVE, "start", 10))
    alt = ("El panel arriostrado con su diagonal de 8 620,07 mm sobre un vano de 7 500 y un "
           "panel de 4 249,18, el punto de cruce de la 8.8.3 con una diagonal continua, y las "
           "dos longitudes de pandeo a la misma escala: 4 310,04 mm en la diagonal contra "
           "7 500 en el puntal, con las esbelteces de 87,90206 y 94,65151 y los radios de giro "
           "de 37,98693 y 66,10201 que el tope de 113,46099 pide")
    return envoltura(W, H, alt, "El panel y las dos longitudes de pandeo", p)


# ------------------------------------------------------------------ figura 3
def demandas() -> str:
    W, H = 880, 400
    p = [
        txt(24, 30, "Las cuatro demandas de fuerza del mismo nudo, y la que gobierna no "
                    "es la sismica", TINTA, "start", 11.5, "600"),
        txt(24, 48, "fuerza en la diagonal del vano extremo   ·   la de estabilidad del "
                    "rafter acumulada es " + D["razon"] + " veces la del diafragma",
            SUAVE, "start", 10),
    ]
    x0 = 306.0
    esc = 400.0 / C["phiPn_diag"]            # la capacidad de la diagonal cierra la escala
    filas = [
        ("diafragma sismico longitudinal", "D1", D["Fdiag"], C["N_diag_sismo"], FRIO),
        ("arriostramiento del rafter, un punto", "D4", D["Praf"], C["Pbr_raf"], SUAVE),
        ("arriostramiento del fuste superior", "D5", D["Pcol"], C["Pbr_col"], VERDE),
        ("acumulacion de Ap. 6.1, vano extremo", "D6", D["Pdiag"], C["N_diag_acum"], ACENTO),
    ]
    ytop = 104.0
    for k, (etq, paso, val, num, color) in enumerate(filas):
        y = ytop + k * 54
        p.append(txt(x0 - 12, y + 12, etq, TINTA, "end", 10.5))
        p.append(txt(x0 - 12, y + 26, paso, SUAVE, "end", 9.5))
        w = max(num * esc, 2.0)
        p.append(rect(x0, y, w, 18, color, 0.9, TINTA))
        # el rotulo va adentro cuando la barra llega cerca de la linea de capacidad
        if w > 280:
            p.append(txt(x0 + w - 8, y + 13, f"{val} kN", FONDO, "end", 10, "600"))
        else:
            p.append(txt(x0 + w + 8, y + 13, f"{val} kN", color, "start", 10, "600"))
    ybot = ytop + 3 * 54 + 30
    p.append(linea(x0, ytop - 10, x0, ybot, LINEA, 1))
    xcap = x0 + C["phiPn_diag"] * esc
    p.append(linea(xcap, ytop - 10, xcap, ybot, VERDE, 1.4, "6 4"))
    p.append(txt(xcap, ytop - 18, "φPn = " + D["phiPn"] + " kN", VERDE, "end", 10, "600"))
    p.append(txt(24, H - 64, f"la quinta demanda no es una fuerza sino una rigidez: el "
                             f"empuje de grua de {D['SS']} kN se reparte entre los cinco "
                             f"marcos porque el diafragma", SUAVE, "start", 10))
    p.append(txt(24, H - 46, f"es {D['rho']} veces mas rigido, y el uso del limite de "
                             f"servicio de la grua queda en {D['usoGrua']}",
                 SUAVE, "start", 10))
    p.append(txt(24, H - 22, f"el fuste superior pide {D['Pcol']} kN sobre {D['Lsup']} mm "
                             f"de longitud no arriostrada, y la acumulacion por marco y "
                             f"agua vale {D['Pacum']} kN", SUAVE, "start", 10))
    alt = ("Las cuatro demandas de fuerza sobre la diagonal del arriostramiento de techo, a la "
           "misma escala: 47,33782 kN del diafragma sismico, 161,02133 del arriostramiento del "
           "rafter en un punto, 2,51638 del fuste superior y 347,00299 de la acumulacion del "
           "Apendice 6, contra los 423,43911 kN de capacidad de la diagonal")
    return envoltura(W, H, alt, "Las cuatro demandas sobre el mismo nudo", p)


if __name__ == "__main__":
    escribir(AQUI, {"planta": planta(), "panel": panel(), "demandas": demandas()})
