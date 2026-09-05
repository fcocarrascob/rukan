"""Las tres figuras del eslabon 10.

    python sitio/docs/series/nch2369-galpon-grua/10-columna-escalonada-y-apoyo-de-la-carrilera/_figuras.py

Portadas del repo de memos, con las cotas leidas del `valores.json` del eslabon
(`figuras.cotas`) en vez de tecleadas. La figura no ilustra: comprueba.

La elevacion y la seccion no las reemplaza el visor del galpon: el modelo 3D
**tiene** la columna escalonada, pero la dibuja sin rotular los cantos de alma ni
el centroide compuesto, y la escala horizontal exagerada de la elevacion es lo
que hace visible el escalon.
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
D = {
    "dbase": C["d_col_base"], "dnudo": C["d_col_nudo"], "bf": C["bf_col"],
    "tf": C["tf_col"], "tw": C["tw_col"], "H": C["H_col_mm"],
    "dpaso": C["d_paso"], "hasiento": C["h_asiento"], "Lsup": C["L_sup"],
    "ar": C["a_r"],
    "dg": C["d_fuste_grua"], "bfg": C["bf_fuste_grua"], "tfg": C["tf_fuste_grua"],
    "twg": C["tw_fuste_grua"], "e": C["e_col_riel"], "tp": C["tp_alma"],
    "Lpbase": C["Lp_base"], "Lppaso": C["Lp_paso"],
    "A": C["Ag_comp_base"], "xb": abs(C["xb_comp_base"]), "c1": C["c_1"],
    "c2": C["c_2"], "ancho": C["ancho_base"],
    "R": C["Rcol_grua"], "kips": C["R_kips"], "tope": C["tope_kips_50"],
    "topekN": C["tope_kips"],
    "dc": C["d_carril"], "bfs": C["bfs_carril"], "tfs": C["tfs_carril"],
    "twc": C["tw_carril"], "bfi": C["bfi_carril"], "tfi": C["tfi_carril"],
    "hriel": C["h_riel"] * 1e3, "riel": C["h_riel_perfil"],
    "bs": C["b_st"], "ts": C["t_st"], "clip": C["recorte_st"],
    "grapa": C["sep_grapas_adopt"],
    "usoE_sup": C["uso_tir_E"], "usoE_inf": C["uso_inf_E"],
    "razon": C["razon_alas"],
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
    n = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / n, dy / n
    px, py = -uy, ux
    return (f'<polygon points="{x:.1f},{y:.1f} {x - ux * k * 1.8 + px * k * 0.7:.1f},'
            f'{y - uy * k * 1.8 + py * k * 0.7:.1f} {x - ux * k * 1.8 - px * k * 0.7:.1f},'
            f'{y - uy * k * 1.8 - py * k * 0.7:.1f}" fill="{c}"/>')


def cota_v(x, y1, y2, etiqueta, c=SUAVE, anchor="start", dx=6, size=10):
    return [linea(x, y1, x, y2, c, 1), cabeza(x, y1, 0, -1, c), cabeza(x, y2, 0, 1, c),
            txt(x + dx, (y1 + y2) / 2 + 3, etiqueta, c, anchor, size)]


def cota_h(y, x1, x2, etiqueta, c=SUAVE, dy=-6, size=10, anchor="middle"):
    return [linea(x1, y, x2, y, c, 1), cabeza(x1, y, -1, 0, c), cabeza(x2, y, 1, 0, c),
            txt((x1 + x2) / 2, y + dy, etiqueta, c, anchor, size)]


def envoltura(w, h, alt, titulo, cuerpo):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
        f'height="{h}" role="img" aria-label="{alt}" font-family="{MONO}" '
        f'font-size="11">\n<title>{titulo}</title>\n'
        f'<rect width="{w}" height="{h}" fill="{FONDO}"/>\n'
        + "\n".join(cuerpo) + "\n</svg>\n")


# ------------------------------------------------------------------ figura 1
def columna() -> str:
    """La columna escalonada y, al lado, la ménsula que la cláusula descarta.

    Escala horizontal exagerada 2,64 veces contra la vertical, declarada en el pie:
    a escala real el conjunto mide 75 px de ancho por 441 de alto y no se le puede
    rotular nada. Lo que la exageración **no** toca son las proporciones
    horizontales, que es donde vive la comparación= el voladizo de 1 000 mm contra
    el canto de 1 050 de la columna.
    """
    W, H = 880, 600
    SY = 0.0420
    SX = 0.1110
    Y0 = 512.0

    py = lambda mm: Y0 - mm * SY
    o = [txt(24, 30, "La ménsula no cabe por cláusula, y el escalón que la reemplaza "
                     "baja el axial de la grúa por un fuste propio",
             TINTA, "start", 11.5, "600"),
         txt(24, 48, "izquierda: columna escalonada de §5.9.1   ·   derecha: la ménsula "
                     "de §5.9.2   ·   escala horizontal exagerada 2,64 veces",
             SUAVE, "start", 10)]

    XE = 330.0
    px = lambda mm: XE + mm * SX
    hp, ht = D["hasiento"], D["H"]
    xg = -D["e"]

    o.append(poli([(px(D["dbase"] / 2), py(0)), (px(D["dnudo"] / 2), py(ht)),
                   (px(-D["dnudo"] / 2), py(ht)), (px(-D["dbase"] / 2), py(0)),
                   (px(D["dbase"] / 2), py(0))], TINTA, 1.4, ACERO))
    o.append(poli([(px(xg + D["dg"] / 2), py(0)), (px(-D["dbase"] / 2), py(0)),
                   (px(-D["dpaso"] / 2), py(hp)), (px(xg + D["dg"] / 2), py(hp)),
                   (px(xg + D["dg"] / 2), py(0))], SUAVE, 1.1, "#e9e6de"))
    o.append(rect(px(xg - D["dg"] / 2), py(hp), D["dg"] * SX, hp * SY, ACERO, 1.4))
    o.append(rect(px(xg - D["dg"] / 2) - 5, py(0), D["ancho"] * SX + 10, 7, TINTA, 1.0, TINTA))
    o.append(linea(px(-D["dpaso"] / 2), py(hp), px(xg + D["dg"] / 2), py(hp), VERDE, 1.8))

    o.append(rect(px(xg - D["bfi"] / 2), py(hp + D["dc"]), D["bfi"] * SX, D["dc"] * SY,
                  "#eceff1", 1.2))
    o.append(rect(px(xg - D["bfs"] / 2), py(hp + D["dc"]), D["bfs"] * SX, D["tfs"] * SY,
                  "#dfe4e7", 1.0))
    o.append(rect(px(xg - 45), py(D["hriel"]), 90 * SX, D["riel"] * SY, FRIO, 0.8, FRIO))

    xc1 = px(D["dbase"] / 2) + 46
    o.extend(cota_v(xc1, py(ht), py(hp), es(D["Lsup"], 2), SUAVE))
    o.extend(cota_v(xc1, py(hp), py(0), es(hp, 2), SUAVE))
    o.extend(cota_v(xc1 + 96, py(ht), py(0), ent(ht), TINTA))
    o.append(txt(xc1 + 102, py(ht / 2) + 18, "a_r = " + es(D["ar"]), TINTA, "start", 9.5))

    o.extend(cota_h(py(0) + 30, px(xg), px(0), ent(D["e"]), SUAVE, -6))
    o.extend(cota_h(py(0) + 58, px(xg - D["dg"] / 2), px(D["dbase"] / 2), ent(D["ancho"]),
                    TINTA, -6))
    o.append(txt(px(0), py(0) + 78, "eje de la columna del marco", SUAVE, "middle", 9.5))

    def guia(xdib, ymm, lineas, color=TINTA, size=9.5):
        yy = py(ymm)
        out = [linea(px(xdib), yy, px(-1560), yy, LINEA, 0.8)]
        for k, t in enumerate(lineas):
            out.append(txt(px(-1575), yy + 4 + (k - (len(lineas) - 1) / 2) * 13, t,
                           color, "end", size))
        return out

    o.extend(guia(xg - D["dg"] / 2, D["hriel"] + 90, ["riel " + es(D["riel"], 2)], FRIO))
    o.extend(guia(xg - D["bfi"] / 2, hp + D["dc"] / 2, ["carrilera " + ent(D["dc"])], FRIO))
    o.extend(guia(-D["dpaso"] / 2, hp, ["escalón a la cota " + es(hp, 2),
                                        "canto ahí " + es(D["dpaso"])], VERDE))
    o.extend(guia(xg, hp * 0.58, ["fuste de grúa",
                                  ent(D["dg"]) + " × " + ent(D["bfg"])], TINTA))
    o.extend(guia(-720, hp * 0.24, ["placa de alma", "continua " + ent(D["tp"])], SUAVE, 9))

    o.append(linea(px(D["dbase"] / 2), py(0), px(D["dbase"] / 2) + 16, py(0), LINEA, 0.8))
    o.append(txt(px(D["dbase"] / 2) + 20, py(0) + 3, ent(D["dbase"]), TINTA, "start", 9.5))
    o.append(linea(px(D["dnudo"] / 2), py(ht), px(D["dnudo"] / 2) + 16, py(ht), LINEA, 0.8))
    o.append(txt(px(D["dnudo"] / 2) + 20, py(ht) + 3, ent(D["dnudo"]), TINTA, "start", 9.5))

    XM = 728.0
    qx = lambda mm: XM + mm * SX
    o.append(poli([(qx(D["dbase"] / 2), py(0)), (qx(D["dnudo"] / 2), py(ht)),
                   (qx(-D["dnudo"] / 2), py(ht)), (qx(-D["dbase"] / 2), py(0)),
                   (qx(D["dbase"] / 2), py(0))], SUAVE, 1.2, "#eeece6"))
    o.append(rect(qx(-D["dbase"] / 2) - 5, py(0), D["dbase"] * SX + 10, 7, SUAVE, 1.0, SUAVE))
    hb = D["hasiento"]
    o.append(poli([(qx(-D["dpaso"] / 2), py(hb)), (qx(-D["e"] - 125), py(hb)),
                   (qx(-D["e"] - 125), py(hb - 160)), (qx(-D["dpaso"] / 2), py(hb - 760)),
                   (qx(-D["dpaso"] / 2), py(hb))], ACENTO, 1.6, "#f3e2dd"))
    o.append(rect(qx(-D["e"] - D["bfi"] / 2), py(hb + D["dc"]), D["bfi"] * SX, D["dc"] * SY,
                  "#eceff1", 1.2))
    o.append(rect(qx(-D["e"] - 45), py(hb + D["dc"] + D["riel"]), 90 * SX, D["riel"] * SY,
                  FRIO, 0.8, FRIO))
    o.extend(cota_h(py(0) + 30, qx(-D["e"]), qx(0), ent(D["e"]), ACENTO, -6))
    o.append(linea(qx(-D["e"]), py(hb), qx(-D["e"]), py(hb) - 52, ACENTO, 1.5))
    o.append(cabeza(qx(-D["e"]), py(hb), 0, 1, ACENTO, 5))
    o.append(txt(qx(-D["e"]) - 10, py(hb) - 42, es(D["R"]) + " kN", ACENTO, "end", 10, "600"))
    xk = qx(-D["e"] - 200)
    o.append(txt(xk, py(9200), es(D["kips"]) + " kips", ACENTO, "end", 11, "600"))
    o.append(txt(xk, py(9200) + 16, "contra el tope de " + ent(D["tope"]) + " de §5.9.2",
                 ACENTO, "end", 9.5))
    o.append(txt(xk, py(9200) + 30, "= " + es(D["topekN"], 3) + " kN", SUAVE, "end", 9.5))
    o.append(txt(qx(0), py(0) + 78, "el voladizo mide 0,95 cantos de columna",
                 SUAVE, "middle", 9.5))

    alt = ("Elevación comparada con la escala horizontal exagerada 2,64 veces: a la "
           "izquierda la columna escalonada de 10 500 mm con el escalón a 6 684,24 donde "
           "se sienta la carrilera de 684 bajo el riel de 131,76, el fuste de grúa de 400 "
           "a 1 000 mm del eje unido por placa de alma continua de 10 y una base de "
           "1 725; a la derecha la ménsula descartada, con el mismo voladizo de 1 000 mm "
           "entregando 299,25983 kN, que son 67,27631 kips contra el tope de 50")
    return envoltura(W, H, alt, "Columna escalonada contra ménsula", o)


# ------------------------------------------------------------------ figura 2
def seccion() -> str:
    """La sección compuesta de la base y los dos brazos que se restan."""
    W, H = 800, 440
    S = 0.245
    XC, Y0 = 560.0, 190.0               # eje del fuste del edificio, eje de la sección

    px = lambda mm: XC + mm * S
    o = [txt(24, 30, "El centroide compuesto no está en el eje de ninguno de los dos "
                     "fustes, y por eso los dos axiales se restan",
             TINTA, "start", 11.5, "600"),
         txt(24, 48, "sección del fuste inferior en la base   ·   el eje x-x del "
                     "Comentario es el vertical", SUAVE, "start", 10)]

    bf, tf, tw, d = D["bf"], D["tf"], D["tw"], D["dbase"]
    bg, tg, wg, dg = D["bfg"], D["tfg"], D["twg"], D["dg"]
    xg, tp = -D["e"], D["tp"]
    hy = bf / 2                          # semiancho fuera del plano

    # fuste del edificio
    o += [rect(px(d / 2 - tf), Y0 - hy * S, tf * S, bf * S),
          rect(px(-d / 2), Y0 - hy * S, tf * S, bf * S),
          rect(px(-d / 2 + tf), Y0 - tw * S / 2, (d - 2 * tf) * S, tw * S)]
    # placa de alma continua
    o.append(rect(px(xg + dg / 2), Y0 - tp * S / 2, D["Lpbase"] * S, tp * S, "#e9e6de"))
    # fuste de grúa
    o += [rect(px(xg + dg / 2 - tg), Y0 - hy * S, tg * S, bg * S),
          rect(px(xg - dg / 2), Y0 - hy * S, tg * S, bg * S),
          rect(px(xg - dg / 2 + tg), Y0 - wg * S / 2, (dg - 2 * tg) * S, wg * S)]

    # ejes
    o.append(linea(px(-D["xb"]), Y0 - 118, px(-D["xb"]), Y0 + 118, ACENTO, 1.3, "6 3"))
    o.append(txt(px(-D["xb"]), Y0 - 124, "x-x", ACENTO, "middle", 10, "600"))
    o.append(linea(px(d / 2) + 26, Y0, px(xg - dg / 2) - 26, Y0, LINEA, 1, "5 4"))
    o.append(linea(px(0), Y0 - 96, px(0), Y0 + 96, LINEA, 1, "3 3"))
    o.append(linea(px(xg), Y0 - 96, px(xg), Y0 + 96, LINEA, 1, "3 3"))

    # cotas
    o += cota_h(Y0 + 118, px(-D["xb"]), px(0), f"{es(D['xb'])}", ACENTO, 15)
    o += cota_h(Y0 + 152, px(xg), px(0), f"{ent(D['e'])}", SUAVE, 15)
    o += cota_h(Y0 + 186, px(xg - dg / 2), px(d / 2), f"{ent(D['ancho'])}", TINTA, 15)
    o += cota_h(Y0 - 108, px(-D["xb"]), px(d / 2), f"{es(D['c1'])}", FRIO, -6)
    o += cota_h(Y0 - 108, px(xg - dg / 2), px(-D["xb"]), f"{es(D['c2'])}", FRIO, -6)
    o += cota_h(Y0 + 84, px(-d / 2), px(xg + dg / 2), f"{ent(D['Lpbase'])}", SUAVE, 14)

    o.append(txt(px(d / 2) + 16, Y0 + 4, f"{ent(d)}", TINTA, "start", 9.5))
    o.append(txt(px(d / 2) + 16, Y0 + 18, f"alas {ent(bf)}×{tf}", SUAVE, "start", 9))
    o.append(txt(px(d / 2) + 16, Y0 + 31, f"alma {tw}", SUAVE, "start", 9))
    o.append(txt(px(xg), Y0 + hy * S + 22, f"{ent(dg)}   alas {ent(bg)}×{tg}   alma {wg}",
                 TINTA, "middle", 9.5))

    # los dos axiales
    o.append(linea(px(0), Y0 - 78, px(0), Y0 - 52, VERDE, 1.6))
    o.append(cabeza(px(0), Y0 - 52, 0, 1, VERDE, 5))
    o.append(txt(px(0) + 6, Y0 - 68, "P1 del techo", VERDE, "start", 9.5))
    o.append(linea(px(xg), Y0 - 78, px(xg), Y0 - 52, ACENTO, 1.6))
    o.append(cabeza(px(xg), Y0 - 52, 0, 1, ACENTO, 5))
    o.append(txt(px(xg) - 6, Y0 - 68, "P2 de la grúa", ACENTO, "end", 9.5))
    o.append(txt(24, 415, f"A = {ent(D['A'])} mm²   ·   los dos brazos caen a lados "
                          "opuestos del eje x-x, así que los momentos se restan",
                SUAVE, "start", 10))

    alt = ("Sección del fuste inferior en la base: fuste del edificio de 1 050 con alas "
           "300 por 22 y alma 14, fuste de grúa de 400 con alas 300 por 16 y alma 10 a "
           "1 000 mm, placa de alma continua de 275 por 10, centroide compuesto a "
           "348,66036 del eje y fibras extremas a 873,66036 y 851,33964")
    return envoltura(W, H, alt, "Sección compuesta del fuste inferior", o)


# ------------------------------------------------------------------ figura 3
def apoyo() -> str:
    """El asiento, con la categoría de fatiga de cada detalle."""
    W, H = 840, 540
    S = 0.30
    XC, Y0 = 350.0, 128.0               # eje del alma de la viga, cara superior del ala

    px = lambda mm: XC + mm * S
    py = lambda mm: Y0 + mm * S

    o = [txt(24, 30, "El tirante va arriba y el asiento transfiere por contacto: la "
                     "misma categoría usa 0,57246 arriba y 0,87966 abajo",
             TINTA, "start", 11.5, "600"),
         txt(24, 48, "detalle del apoyo sobre el fuste de grúa, visto a lo largo de la "
                     "carrilera   ·   categoría de la Tabla A-3.1 en cada punto",
             SUAVE, "start", 10)]

    bfs, tfs, twc = D["bfs"], D["tfs"], D["twc"]
    bfi, tfi, dc = D["bfi"], D["tfi"], D["dc"]
    hw = dc - tfs - tfi
    clip, ts, bs = D["clip"], D["ts"], D["bs"]

    # el fuste de grúa y su placa de asiento, dibujados primero para que la viga se vea encima
    o.append(rect(px(-D["dg"] / 2), py(dc) + 9, D["dg"] * S, 92, ACERO, 1.4))
    o.append(linea(px(-D["dg"] / 2 + D["tfg"]), py(dc) + 9, px(-D["dg"] / 2 + D["tfg"]),
                   py(dc) + 101, TINTA, 0.8))
    o.append(linea(px(D["dg"] / 2 - D["tfg"]), py(dc) + 9, px(D["dg"] / 2 - D["tfg"]),
                   py(dc) + 101, TINTA, 0.8))
    o.append(rect(px(-D["bfg"] / 2) - 6, py(dc), D["bfg"] * S + 12, 9, "#dcd8cc", 1.2))

    # la viga
    o += [rect(px(-bfs / 2), py(0), bfs * S, tfs * S),
          rect(px(-twc / 2), py(tfs), twc * S, hw * S),
          rect(px(-bfi / 2), py(tfs + hw), bfi * S, tfi * S)]

    # atiesadores de apoyo: llegan al ala inferior y se destalonan en las esquinas
    for lado in (1, -1):
        x0 = px(twc / 2) if lado > 0 else px(-twc / 2) - ts * S
        o.append(poli([(x0, py(tfs) + clip * S), (x0 + ts * S, py(tfs) + clip * S),
                       (x0 + ts * S, py(tfs + hw)), (x0, py(tfs + hw)),
                       (x0, py(tfs) + clip * S)], VERDE, 1.2, "#e6ece4"))
    o.append(linea(px(twc / 2 + ts), py(tfs + hw) - 4, px(bfs / 2) + 78, py(dc) - 26, VERDE, 0.9))
    o.append(txt(px(bfs / 2) + 84, py(dc) - 40, f"atiesador de apoyo {bs}×{ts}",
                 VERDE, "start", 9.5))
    o.append(txt(px(bfs / 2) + 84, py(dc) - 26, f"ajustado al ala inferior, sin soldar",
                 VERDE, "start", 9.5))
    o.append(txt(px(bfs / 2) + 84, py(dc) - 12, f"destalonado {clip} · cat. C",
                 VERDE, "start", 9.5))

    # el riel y sus grapas
    o.append(rect(px(-40), py(-D["riel"]), 80 * S, D["riel"] * S, FRIO, 0.9, FRIO))
    for lado in (1, -1):
        gx = px(lado * 62)
        o.append(rect(gx - 5 if lado > 0 else gx - 8, py(0) - 9, 13, 9, "#cfd6da", 0.9, FRIO))
    o.append(txt(px(0), py(-D["riel"]) - 8, f"riel {es(D['riel'], 2)}", FRIO, "middle", 9.5))
    o.append(linea(px(-62), py(0) - 9, px(-bfs / 2) - 20, py(0) - 34, LINEA, 0.8))
    o.append(txt(px(-bfs / 2) - 26, py(0) - 44, "grapas en pares opuestos", SUAVE, "end", 9.5))
    o.append(txt(px(-bfs / 2) - 26, py(0) - 30, f"a {ent(D['grapa'])} mm, sin ganchos §5.15.3",
                 SUAVE, "end", 9.5))

    # el tirante: del ala superior baja al fuste de grúa, con holgura vertical
    tx = px(bfs / 2)
    o.append(rect(tx, py(0), 12, dc * S + 9, "#eef0f1", 1.2, FRIO))
    for k in (0.22, 0.42):
        o.append('<circle cx="%.1f" cy="%.1f" r="2.4" fill="%s"/>'
                 % (tx + 6, py(dc * k), FRIO))
    o.append(txt(tx + 20, py(60), "tirante al ala superior", FRIO, "start", 9.5))
    o.append(txt(tx + 20, py(60) + 14, f"cat. E: uso {es(D['usoE_sup'])}",
                 FRIO, "start", 9.5, "600"))
    o.append(txt(tx + 20, py(60) + 28, f"el mismo abajo daría {es(D['usoE_inf'])}",
                 ACENTO, "start", 9.5, "600"))
    o.append(txt(tx + 20, py(60) + 42, f"la razón es {es(D['razon'])}", SUAVE, "start", 9))
    o.append(txt(tx + 20, py(60) + 56, "apernado, deslizamiento crítico §5.13",
                 SUAVE, "start", 9))

    # el contacto en el ala inferior
    o.append(linea(px(-bfi / 2), py(dc), px(-bfs / 2) - 20, py(dc) + 22, ACENTO, 0.9))
    o.append(txt(px(-bfs / 2) - 26, py(dc) + 14, "contacto, sin soldadura", ACENTO, "end", 9.5, "600"))
    o.append(txt(px(-bfs / 2) - 26, py(dc) + 28, "§5.8.1 y §5.8.9", ACENTO, "end", 9))
    o.append(txt(px(0), py(dc) + 62, f"fuste de grúa {ent(D['dg'])}", TINTA, "middle", 9.5))

    o += cota_v(px(-bfs / 2) - 178, py(0), py(dc), f"{ent(dc)}", TINTA, "end", -8)
    o.append(txt(px(0), py(dc) + 128, f"ala superior {ent(bfs)}×{tfs}   ·   alma {twc}   "
                                      f"·   ala inferior {ent(bfi)}×{tfi}",
                 SUAVE, "middle", 9.5))
    o.append(txt(24, 492, "el atiesador de apoyo hereda la categoría C del 09, y en el "
                          "apoyo el momento es cero:", SUAVE, "start", 10))
    o.append(txt(24, 508, "lo que ve es la reacción entera, ciclo a ciclo, y no un rango "
                          "de flexión", SUAVE, "start", 10))

    alt = ("Detalle del apoyo visto a lo largo de la carrilera: los atiesadores de apoyo de "
           "110 por 12 que llegan ajustados al ala inferior con destalonado de esquina de 25, "
           "el asiento sobre el fuste de grúa de 400 que transfiere por contacto sin soldar "
           "el ala inferior, el tirante empernado al ala superior que baja hasta el fuste con "
           "uso 0,57246 en categoría E contra el 0,87966 que tendría abajo, y las grapas del "
           "riel de 131,76 en pares opuestos a 750 mm")
    return envoltura(W, H, alt, "Detalle del apoyo de la carrilera", o)

if __name__ == "__main__":
    escribir(AQUI, {"columna": columna(), "seccion": seccion(), "apoyo": apoyo()})
