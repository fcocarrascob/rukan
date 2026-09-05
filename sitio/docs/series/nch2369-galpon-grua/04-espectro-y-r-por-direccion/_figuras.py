"""Las dos figuras del eslabón 04: los espectros y las dos rampas de la Ec. (1b).

    python sitio/docs/series/nch2369-galpon-grua/04-espectro-y-r-por-direccion/_figuras.py

Portado de `_img/_figuras-nch2369-galpon-grua-04.py` del repo de memos. Allá las
cotas vivían en un dict `D` tecleado; acá se leen del `valores.json` del eslabón
(`figuras.cotas`), y las curvas se dibujan con las mismas ecuaciones que el
`_calculo.py` escribe, con los mismos parámetros del suelo.

La pregunta de la primera figura es **dónde caen las dos direcciones**: el
espectro de referencia con su pico, el reducido punto a punto, y la frontera de
la rampa entre los dos períodos de análisis. La de la segunda es **por qué la
comparación del 01 no era 5 contra 4**: las dos rampas —la del galpón de la fila
5.5 y la del galpón liviano— terminan en fronteras distintas, porque
`C_r = 0,16 R` mueve la frontera junto con el R.

Dos decisiones de portabilidad, heredadas: las flechas se dibujan como triángulos
y no con `<marker>`, y el SVG trae su propio fondo claro para leerse en tema
oscuro.
"""

from __future__ import annotations

import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from figuras import cotas, es  # noqa: E402

C = cotas(AQUI)

TINTA, SUAVE, LINEA, FONDO = "#2b2a26", "#8a8578", "#c9c4b5", "#fcfcfa"
ACENTO, FRIO = "#a4442c", "#2f5d7c"
MONO = "ui-monospace,'IBM Plex Mono',Menlo,Consolas,monospace"


def sa_ref(T: float) -> float:
    """Ec. (3): espectro de referencia horizontal, en g."""
    if T <= 0.0:
        return C["ArS"]
    x = T / C["T_0"]
    return C["ArS"] * (1.0 + C["r_s"] * x ** C["p_suelo"]) / (1.0 + x ** C["q_s"])


def r_star(T: float, R: float) -> float:
    """Ec. (1b), con sus tres ramas."""
    if R <= 1.0:
        return 1.0
    lim = 0.16 * R * C["T_1"]
    return R if T >= lim else C["R_piso"] + (R - C["R_piso"]) * T / lim


def sa_dis(T: float, R: float) -> float:
    """Ec. (1a): el de referencia, corregido por ξ y reducido por R*."""
    return C["I"] * sa_ref(T) * C["f_xi"] / r_star(T, R)


def cab(w: int, h: int, etiqueta: str, titulo: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
        f'height="{h}" role="img" aria-label="{etiqueta}" '
        f'font-family="{MONO}" font-size="11">',
        f"<title>{titulo}</title>",
        f'<rect width="{w}" height="{h}" fill="{FONDO}"/>',
    ]


def txt(x, y, s, color=TINTA, anchor="start", size=11, peso="normal"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" text-anchor="{anchor}" '
            f'font-size="{size}" font-weight="{peso}">{s}</text>')


def ejes(o, X0, X1, Y0, Y1, px, py, ymarcas, xmarcas, rot_y, dy=1):
    for a in ymarcas:
        o.append(f'<line x1="{X0}" y1="{py(a):.1f}" x2="{X1}" y2="{py(a):.1f}" '
                 f'stroke="{LINEA}" stroke-width="0.6"/>')
        o.append(txt(X0 - 8, py(a) + 4, es(a, dy), SUAVE, "end"))
    for T in xmarcas:
        o.append(f'<line x1="{px(T):.1f}" y1="{Y0}" x2="{px(T):.1f}" y2="{Y1}" '
                 f'stroke="{LINEA}" stroke-width="0.6"/>')
        o.append(txt(px(T), Y1 + 18, es(T, 1), SUAVE, "middle"))
    o.append(txt(X0 - 8, py(0.0) + 4, "0", SUAVE, "end"))
    o.append(txt(X0, Y1 + 18, "0", SUAVE, "middle"))
    o.append(f'<line x1="{X0}" y1="{Y1}" x2="{X1 + 12}" y2="{Y1}" stroke="{TINTA}" '
             f'stroke-width="1"/>')
    o.append(f'<polygon points="{X1+12},{Y1} {X1+4},{Y1-3.5} {X1+4},{Y1+3.5}" fill="{TINTA}"/>')
    o.append(f'<line x1="{X0}" y1="{Y1}" x2="{X0}" y2="{Y0 - 12}" stroke="{TINTA}" '
             f'stroke-width="1"/>')
    o.append(f'<polygon points="{X0},{Y0-12} {X0-3.5},{Y0-4} {X0+3.5},{Y0-4}" fill="{TINTA}"/>')
    o.append(txt(X1 + 6, Y1 + 34, "T [s]", SUAVE, "middle"))
    o.append(txt(X0 - 52, Y0 - 16, rot_y, SUAVE, "start"))


def curva(px, py, fn, color, ancho, TMAX, guion=None, n=400):
    pts = [f"{px(TMAX * i / n):.1f},{py(fn(TMAX * i / n)):.1f}" for i in range(n + 1)]
    dash = f' stroke-dasharray="{guion}"' if guion else ""
    return (f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" '
            f'stroke-width="{ancho}"{dash}/>')


# ================================================== figura 1 · los espectros
def espectros() -> str:
    W, H = 700, 366
    X0, X1, Y0, Y1 = 78, 630, 40, 272
    TMAX, SMAX = 1.20, 1.40
    def px(T): return X0 + (X1 - X0) * T / TMAX
    def py(a): return Y1 - (Y1 - Y0) * a / SMAX

    o = cab(W, H,
            "Espectro de referencia de zona 2 y suelo C con su pico, el espectro "
            "reducido por la Ec. 1b, la frontera de la rampa y los dos periodos "
            "de analisis",
            "Espectro NCh2369, zona 2 suelo C, con las dos direcciones")
    ejes(o, X0, X1, Y0, Y1, px, py, (0.4, 0.8, 1.2), (0.2, 0.4, 0.6, 0.8, 1.0, 1.2),
         "Sa / g", dy=1)

    # la frontera de la rampa, y la banda que queda a su izquierda
    o.append(f'<rect x="{X0}" y="{Y0}" width="{px(C["Cr_T1"]) - X0:.1f}" '
             f'height="{Y1 - Y0}" fill="{ACENTO}" opacity="0.05"/>')
    o.append(f'<line x1="{px(C["Cr_T1"]):.1f}" y1="{Y0}" x2="{px(C["Cr_T1"]):.1f}" '
             f'y2="{Y1}" stroke="{ACENTO}" stroke-width="1.2" stroke-dasharray="4 3"/>')
    o.append(txt((X0 + px(C["Cr_T1"])) / 2, Y0 + 16, "rampa", ACENTO, "middle", 10))
    o.append(txt(px(C["Cr_T1"]) + 6, Y1 - 8, "Cr·T1 = " + es(C["Cr_T1"], 2) + " s",
                 ACENTO, "start", 10))

    # las dos curvas
    o.append(curva(px, py, sa_ref, TINTA, 2.0, TMAX))
    o.append(curva(px, py, lambda T: sa_dis(T, C["R_T7"]), FRIO, 2.0, TMAX))

    # el pico del espectro de referencia
    o.append(f'<circle cx="{px(C["T_pico"]):.1f}" cy="{py(C["Sa_pico"]):.1f}" '
             f'r="3.5" fill="none" stroke="{TINTA}" stroke-width="1.4"/>')
    xg, yg = px(0.62), Y0 + 40
    o.append(f'<line x1="{px(C["T_pico"]) + 4:.1f}" y1="{py(C["Sa_pico"]):.1f}" '
             f'x2="{xg - 4:.1f}" y2="{yg - 4:.1f}" stroke="{SUAVE}" stroke-width="0.9"/>')
    o.append(txt(xg, yg - 6, "pico " + es(C["Sa_pico"], 5) + " g", TINTA, "start", 10))
    o.append(txt(xg, yg + 7, "en " + es(C["T_pico"], 5) + " s", SUAVE, "start", 10))

    # los dos períodos de análisis
    for T, sa, sd, nom, lado in (
            (C["T_star_X"], C["Sa_ref_X"], C["Sa_dis_X"], "X arriostrada", -1),
            (C["T_star_Y"], C["Sa_ref_Y"], C["Sa_dis_Y"], "Y marcos", 1)):
        o.append(f'<line x1="{px(T):.1f}" y1="{py(sd):.1f}" x2="{px(T):.1f}" '
                 f'y2="{py(sa):.1f}" stroke="{SUAVE}" stroke-width="0.9" '
                 f'stroke-dasharray="3 3"/>')
        o.append(f'<circle cx="{px(T):.1f}" cy="{py(sa):.1f}" r="4" fill="{TINTA}"/>')
        if lado > 0:                  # la de marcos, casi sobre el pico: el rótulo arriba
            o.append(txt(px(T), py(sa) - 10, es(sa, 5), TINTA, "middle", 10.5))
        else:
            o.append(txt(px(T) - 8, py(sa) - 8, es(sa, 5), TINTA, "end", 10.5))
        # las dos ordenadas de diseño quedan casi a la misma altura: van abajo
        o.append(f'<circle cx="{px(T):.1f}" cy="{py(sd):.1f}" r="4" fill="{FRIO}"/>')
        o.append(txt(px(T), py(sd) + 20, es(sd, 5), FRIO, "middle", 10.5))
        o.append(txt(px(T), Y1 + 34, nom, SUAVE, "middle", 10))
        o.append(txt(px(T), Y1 + 47, "T* = " + es(T, 2) + " s", SUAVE, "middle", 10))

    # leyenda
    o.append(f'<line x1="{X1-176}" y1="{Y0+2}" x2="{X1-152}" y2="{Y0+2}" '
             f'stroke="{TINTA}" stroke-width="2"/>')
    o.append(txt(X1 - 146, Y0 + 6, "referencia, Ec. (3)", SUAVE, "start", 10))
    o.append(f'<line x1="{X1-176}" y1="{Y0+18}" x2="{X1-152}" y2="{Y0+18}" '
             f'stroke="{FRIO}" stroke-width="2"/>')
    o.append(txt(X1 - 146, Y0 + 22, "diseño, Ecs. (1a) y (1b)", SUAVE, "start", 10))

    o.append(txt(X0, 22, "Zona 2 · suelo C · R de tabla 5 · ξ = " + es(C["xi"], 2),
                 TINTA, "start", 11.5, "600"))
    o.append("</svg>")
    return "\n".join(o) + "\n"


# ============================================ figura 2 · las dos rampas de R*
def rampa_r() -> str:
    W, H = 700, 344
    X0, X1, Y0, Y1 = 78, 630, 40, 250
    TMAX, RMAX = 0.60, 5.60
    def px(T): return X0 + (X1 - X0) * T / TMAX
    def py(a): return Y1 - (Y1 - Y0) * a / RMAX

    o = cab(W, H,
            "Las dos rampas de la Ec. 1b: la del galpon de la fila 5.5 termina en "
            "la frontera de 0,28 s y la del galpon liviano en 0,224 s, con los dos "
            "periodos de analisis marcados",
            "Rampas de R* para R igual a 5 y R igual a 4")
    # las marcas del eje caen en 4 y en 5 a propósito: son los dos valores que el
    # eslabón compara, y así las dos mesetas quedan SOBRE una línea de la rejilla.
    ejes(o, X0, X1, Y0, Y1, px, py, (1.0, 2.0, 3.0, 4.0, 5.0),
         (0.1, 0.2, 0.3, 0.4, 0.5, 0.6), "R*", dy=1)

    for R, color, nom in ((C["R_T7"], FRIO, "fila 5.5 · R = 5"),
                          (C["R_liv"], ACENTO, "fila 5.7 · R = 4")):
        o.append(curva(px, py, lambda T, R=R: r_star(T, R), color, 2.0, TMAX))
        lim = 0.16 * R * C["T_1"]
        o.append(f'<line x1="{px(lim):.1f}" y1="{py(R):.1f}" x2="{px(lim):.1f}" '
                 f'y2="{Y1}" stroke="{color}" stroke-width="0.9" stroke-dasharray="3 3"/>')
        dx, anc = (5, "start") if R == C["R_T7"] else (-5, "end")
        o.append(txt(px(lim) + dx, Y1 - 8, es(lim, 3) + " s", color, anc, 10))
        o.append(txt(X1 - 8, py(R) - 7, nom, color, "end", 10))

    # los dos períodos, con los cuatro R* que producen
    for T, nom in ((C["T_star_X"], "X arriostrada"), (C["T_star_Y"], "Y marcos")):
        o.append(f'<line x1="{px(T):.1f}" y1="{Y0}" x2="{px(T):.1f}" y2="{Y1}" '
                 f'stroke="{SUAVE}" stroke-width="0.9" stroke-dasharray="3 3"/>')
        o.append(txt(px(T), Y1 + 34, nom, SUAVE, "middle", 10))
        o.append(txt(px(T), Y1 + 47, "T* = " + es(T, 2) + " s", SUAVE, "middle", 10))
        for R, color, dy in ((C["R_T7"], FRIO, -10), (C["R_liv"], ACENTO, 26)):
            v = r_star(T, R)
            o.append(f'<circle cx="{px(T):.1f}" cy="{py(v):.1f}" r="4" fill="{color}"/>')
            # en 0,20 s la rampa del liviano corre pegada a su propia frontera:
            # el rótulo se va a la izquierda para no cruzarla
            dx, anc = (-10, "end") if (color == ACENTO and T == C["T_star_X"]) \
                else (12, "start")
            o.append(txt(px(T) + dx, py(v) + dy, es(v, 5), color, anc, 10.5))

    o.append(txt(X0, 22, "La frontera se mueve con R, porque Cr = 0,16 R",
                 TINTA, "start", 11.5, "600"))
    o.append("</svg>")
    return "\n".join(o) + "\n"


if __name__ == "__main__":
    from figuras import escribir
    escribir(AQUI, {"espectros": espectros(), "rampa-r": rampa_r()})
