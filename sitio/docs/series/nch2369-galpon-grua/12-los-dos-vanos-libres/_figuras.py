"""Las tres figuras del eslabon 12.

    python sitio/docs/series/nch2369-galpon-grua/12-los-dos-vanos-libres/_figuras.py

Portadas del repo de memos, con las cotas leidas del `valores.json` del eslabon
(`figuras.cotas`) en vez de tecleadas.

**La primera existe para mostrar que los dos vanos libres no descentran nada.**
Los vanos arriostrados son los extremos, asi que el centro de rigidez cae en el
centro de la nave: lo unico que se corre es el centro de masa, y lo corre la
grua. Las dos marcas y la cota entre ellas son el contenido entero de la figura.

**La segunda pone las dos lecturas del mismo edificio sobre la misma curva.** El
eje horizontal es la rigidez del panel longitudinal relativa a la del marco, que
es justo lo que un modelo plano de la direccion de marcos no tiene: el origen del
eje **es** el modelo plano. El umbral de §5.2.2 corta la curva entre las dos
marcas.

**La tercera muestra por que el periodo no decide.** El espectro de diseno baja
dentro de la rampa de la Ec. (1b) y vuelve a subir despues, pero el recorte de
§5.13 es una recta horizontal que lo tapa entero hasta el borde de la ventana.
Los dos periodos de la serie caen dentro del tramo tapado.

Ninguna la reemplaza el visor: la planta del modelo no rotula centros de masa ni
de rigidez, y las otras dos no son geometria sino curvas de un parametro.
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


D = {
    "largo": es(C["L_total"], 2), "luz": es(C["L_luz"], 2),
    "vano": es(C["s_marco"], 2), "centro": es(C["x_CR"], 2),
    "semiluz": es(C["y_CR"], 2),
    "xg": es(C["x_g_tope"], 2), "xcm": es(C["x_CM"]), "e": es(C["e_tors"]),
    "pct": es(C["pct_grua"], 1),
    "raz3d": es(C["raz_tors_Y"]), "razpl": es(C["raz_tors_plano"]),
    "umbral": es(C["tope_tors"], 2), "rho": es(C["rho_pan"]),
    "rholim": es(C["rho_lim"]), "kbrlim": es(C["kbr_lim"]),
    "margen": es(C["uso_kbr"]),
    "Cdis": es(C["C_dis"]), "Sa0": es(C["Sa_cero"]), "SaX": es(C["Sa_TX"]),
    "Safr": es(C["Sa_frontera"]), "Tcorte": es(C["T_borde"]),
    "TX": es(C["T_star_X"], 2), "TY": es(C["T_star_Y2"]),
    "Tfr": es(C["Cr_T1"]), "Tmaxl": es(C["T_estac_max"]),
    "Samaxl": es(C["Sa_max"]), "Tminl": es(C["T_estac_min"]),
    "Saminl": es(C["Sa_min"]), "cociente": es(C["cerca_max"]),
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


def cota_h(y, x1, x2, etiqueta, c=SUAVE, dy=-6, size=10):
    return [linea(x1, y, x2, y, c, 1), cabeza(x1, y, -1, 0, c), cabeza(x2, y, 1, 0, c),
            txt((x1 + x2) / 2, y + dy, etiqueta, c, "middle", size)]


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
    """La planta: rigidez simetrica, masa corrida por la grua."""
    W, H = 860, 700
    esc = 15.0                                   # px por metro
    x0, y0 = 180.0, 140.0
    x1 = x0 + C["L_total"] * esc
    y1 = y0 + C["L_luz"] * esc
    mx = lambda m: x0 + m * esc                  # noqa: E731
    banda = 18.0

    p = [txt(24, 34, "Planta · rigidez simetrica, masa corrida", TINTA, "start", 13, "bold"),
         txt(24, 54, "los dos vanos arriostrados son los extremos, asi que el centro de "
                     "rigidez no se mueve", SUAVE, "start", 10)]
    p.append(rect(x0, y0, x1 - x0, y1 - y0, "#ffffff", 1.2, TINTA))

    for i in range(5):
        x = mx(C["s_marco"] * i)
        p.append(linea(x, y0, x, y1, TINTA, 1.6))
        p.append(txt(x, y1 + 20, f"M{i + 1}", SUAVE, "middle", 10))

    for j in range(4):
        xa, xb = mx(C["s_marco"] * j), mx(C["s_marco"] * (j + 1))
        for yb in (y0, y1 - banda):
            if j in (0, 3):
                p.append(rect(xa, yb, xb - xa, banda, "none", 1.0, FRIO))
                p.append(linea(xa, yb, xb, yb + banda, FRIO, 1.4))
                p.append(linea(xa, yb + banda, xb, yb, FRIO, 1.4))
            else:
                p.append(rect(xa + 6, yb + 4, xb - xa - 12, banda - 8, "none", 1.0, ACERO))
                p.append(linea(xa + 6, yb + banda / 2, xb - 6, yb + banda / 2,
                               ACERO, 1.0, "4 3"))
        p.append(txt((xa + xb) / 2, y0 - 14,
                     "arriostrado" if j in (0, 3) else "porton",
                     FRIO if j in (0, 3) else SUAVE, "middle", 10))

    xg = mx(C["x_g_tope"])
    p.append(rect(xg - 7, y0 + banda + 10, 14, (y1 - banda - 10) - (y0 + banda + 10),
                  ACERO, 1.3, TINTA))
    p.append(txt(xg + 12, y0 + banda + 26, "puente grua", TINTA, "start", 10, "bold"))

    ycm = (y0 + y1) / 2
    xcr, xcm = mx(C["x_CR"]), mx(C["x_CM"])
    p.append(linea(xcr, y0 - 4, xcr, y1 + 4, VERDE, 1.4, "6 4"))
    p.append(linea(xcm, y0 - 4, xcm, y1 + 4, ACENTO, 1.4, "6 4"))
    p.append(f'<circle cx="{xcr:.1f}" cy="{ycm:.1f}" r="5" fill="none" '
             f'stroke="{VERDE}" stroke-width="1.6"/>')
    p.append(f'<circle cx="{xcm:.1f}" cy="{ycm:.1f}" r="5" fill="{ACENTO}"/>')
    p.append(txt(xcr + 10, ycm - 12, f"CR  {D['centro']} m", VERDE, "start", 10))
    p.append(txt(xcm - 10, ycm + 22, f"CM  {D['xcm']} m", ACENTO, "end", 10))

    p += cota_h(y1 + 46, xcm, xcr, f"e = {D['e']} m", ACENTO, -7, 11)
    p += cota_h(y1 + 78, x0, mx(C["s_marco"]), f"{D['vano']} m", SUAVE, -6)
    p += cota_h(y1 + 110, x0, x1, "", SUAVE)
    p.append(txt((x0 + x1) / 2, y1 + 128, f"{D['largo']} m", SUAVE, "middle", 10))
    p += cota_v(x1 + 34, y0, y1, f"{D['luz']} m", SUAVE, "start", 8)
    p += cota_h(y0 - 40, x0, xg, f"{D['xg']} m", TINTA, -6)

    p.append(txt(24, H - 40, f"El centro de rigidez cae en {D['centro']} m por simetria y no "
                             f"lo mueven los portones: lo que descentra la masa es donde se "
                             f"estaciona la grua,", SUAVE, "start", 10))
    p.append(txt(24, H - 22, f"que pesa el {D['pct']} % del peso sismico. Media luz vale "
                             f"{D['semiluz']} m y da el brazo de los paneles longitudinales.",
                 SUAVE, "start", 10))

    alt = ("Planta del galpon con los cuatro vanos entre los cinco marcos: los dos extremos "
           "arriostrados y los dos centrales con porton, el centro de rigidez en 15,00 m por "
           "simetria, la grua estacionada a 2,00 m del marco extremo, el centro de masa "
           "corrido a 12,11692 m y la excentricidad de 2,88308 m acotada entre los dos")
    return envoltura(W, H, alt, "La planta y las dos marcas que no coinciden", p)


# ------------------------------------------------------------------ figura 2
def razon() -> str:
    """La razon de derivas contra la rigidez relativa del panel."""
    W, H = 860, 520
    x0, x1 = 120.0, 780.0
    y0, y1 = 100.0, 400.0
    rmax, lo, hi = 3.0, 1.05, 1.45
    px = lambda r: x0 + (x1 - x0) * r / rmax          # noqa: E731
    py = lambda v: y1 - (y1 - y0) * (v - lo) / (hi - lo)  # noqa: E731

    def f(r):
        return 1.0 + C["brazo_Y"] * C["e_tors"] / (C["sum_x2"] + C["sum_y2"] * r)

    p = [txt(24, 34, "La razon de derivas contra la rigidez del panel longitudinal",
             TINTA, "start", 13, "bold"),
         txt(24, 54, "el origen del eje horizontal es el modelo plano: ahi el panel no existe",
             SUAVE, "start", 10)]

    p.append(linea(x0, y0, x0, y1, TINTA, 1.2))
    p.append(linea(x0, y1, x1, y1, TINTA, 1.2))
    for v in (1.10, 1.20, 1.30, 1.40):
        y = py(v)
        p.append(linea(x0 - 4, y, x1, y, LINEA, 0.8))
        p.append(txt(x0 - 10, y + 4, f"{v:.2f}".replace(".", ","), SUAVE, "end", 10))
    for r in (0.0, 1.0, 2.0, 3.0):
        x = px(r)
        p.append(linea(x, y1, x, y1 + 5, SUAVE, 1))
        p.append(txt(x, y1 + 20, f"{r:.1f}".replace(".", ","), SUAVE, "middle", 10))
    p.append(txt((x0 + x1) / 2, y1 + 42, "rigidez del panel dividida por la del marco",
                 SUAVE, "middle", 10))

    yu = py(C["tope_tors"])
    p.append(linea(x0, yu, x1, yu, ACENTO, 1.6, "7 4"))
    p.append(txt(x1 - 6, yu - 9, f"umbral de §5.2.2 = {D['umbral']}", ACENTO, "end", 11))

    n = 240
    pts = [f"{px(rmax * i / n):.1f},{py(f(rmax * i / n)):.1f}" for i in range(n + 1)]
    p.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{FRIO}" '
             f'stroke-width="2"/>')

    for r, col in ((0.0, ACENTO), (C["rho_lim"], VERDE), (C["rho_pan"], FRIO)):
        x, y = px(r), py(f(r))
        p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{col}"/>')

    p.append(txt(px(0.0) + 12, py(f(0.0)) - 6, D["razpl"], ACENTO, "start", 11, "bold"))
    p.append(txt(px(0.0) + 12, py(f(0.0)) + 12, "modelos planos por direccion",
                 ACENTO, "start", 10))
    p.append(txt(px(C["rho_pan"]), py(f(C["rho_pan"])) + 24, D["raz3d"],
                 FRIO, "middle", 11, "bold"))
    p.append(txt(px(C["rho_pan"]), py(f(C["rho_pan"])) + 42, "panel ilustrativo, modelo 3D",
                 FRIO, "middle", 10))
    p.append(linea(px(C["rho_lim"]), yu, px(C["rho_lim"]), y1, VERDE, 1.2, "4 3"))
    p.append(txt(px(C["rho_lim"]) + 10, py(1.28), f"{D['rholim']} · cota inferior",
                 VERDE, "start", 10))
    p.append(txt(px(C["rho_lim"]) + 10, py(1.245), f"del 13 = {D['kbrlim']} kN/m",
                 VERDE, "start", 10))

    p.append(txt(24, H - 40, "Las dos lecturas del mismo edificio caen una a cada lado del "
                             "umbral. Lo que las separa no es una hipotesis de carga: es si "
                             "el modelo tiene", SUAVE, "start", 10))
    p.append(txt(24, H - 22, f"la otra direccion adentro. El margen del panel ilustrativo "
                             f"sobre la cota inferior vale {D['margen']}.", SUAVE, "start", 10))

    alt = ("La razon entre la deriva del marco extremo y la promedio contra la rigidez "
           "relativa del panel longitudinal: la curva baja de 1,38441 en el origen a 1,11962 "
           "en el panel ilustrativo y cruza el umbral de 1,20 de la clausula 5.2.2 en 0,82985")
    return envoltura(W, H, alt, "Las dos lecturas del mismo edificio", p)


# ------------------------------------------------------------------ figura 3
def espectro() -> str:
    """El espectro de diseno contra el recorte de §5.13."""
    W, H = 860, 520
    x0, x1 = 120.0, 780.0
    y0, y1 = 100.0, 400.0
    Tmax, lo, hi = 0.80, 0.24, 0.45
    px = lambda T: x0 + (x1 - x0) * T / Tmax          # noqa: E731
    py = lambda v: y1 - (y1 - y0) * (v - lo) / (hi - lo)  # noqa: E731

    ArS, r_s, T_0 = C["ArS"], C["r_s"], C["T_0"]
    p_s, q_s, f_xi = C["p_suelo"], C["q_s"], C["f_xi"]
    Cr, R, Rmin = C["Cr_T1"], C["R_T7"], C["R_min"]

    def Sad(T):
        u = T / T_0
        sar = ArS * (1 + r_s * u ** p_s) / (1 + u ** q_s)
        rst = R if T >= Cr else Rmin + (R - Rmin) * T / Cr
        return sar * f_xi / rst

    p = [txt(24, 34, "El espectro de diseno y el recorte que lo tapa", TINTA, "start", 13,
             "bold"),
         txt(24, 54, "mientras el recorte gobierne, el periodo no cambia ningun numero que se "
                     "disene", SUAVE, "start", 10)]

    p.append(linea(x0, y0, x0, y1, TINTA, 1.2))
    p.append(linea(x0, y1, x1, y1, TINTA, 1.2))
    for v in (0.25, 0.30, 0.35, 0.40, 0.45):
        y = py(v)
        p.append(linea(x0 - 4, y, x1, y, LINEA, 0.8))
        p.append(txt(x0 - 10, y + 4, f"{v:.2f}".replace(".", ","), SUAVE, "end", 10))
    for T in (0.0, 0.20, 0.40, 0.60, 0.80):
        x = px(T)
        p.append(linea(x, y1, x, y1 + 5, SUAVE, 1))
        p.append(txt(x, y1 + 20, f"{T:.2f}".replace(".", ","), SUAVE, "middle", 10))
    p.append(txt((x0 + x1) / 2, y1 + 42, "periodo, en segundos", SUAVE, "middle", 10))
    p.append(txt(x0 - 10, y0 - 16, "aceleracion de diseno, en g", SUAVE, "start", 10))

    yc = py(C["C_dis"])
    p.append(linea(x0, yc, x1, yc, ACENTO, 1.8))
    p.append(txt(x1 - 6, yc + 18, f"recorte de §5.13 = {D['Cdis']} g", ACENTO, "end", 11))

    pts, n = [], 320
    for i in range(n + 1):
        T = max(1e-4, Tmax * i / n)
        v = Sad(T)
        if v < lo:
            break
        pts.append(f"{px(T):.1f},{py(min(hi, v)):.1f}")
    p.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{FRIO}" '
             f'stroke-width="2"/>')

    p.append(linea(px(Cr), y0, px(Cr), y1, SUAVE, 1.0, "4 3"))
    p.append(txt(px(Cr) + 8, y0 + 14, f"frontera de la rampa {D['Tfr']} s", SUAVE,
                 "start", 10))

    for T, etiqueta in ((C["T_star_X"], f"T*X {D['TX']}"),
                        (C["T_star_Y2"], f"T*Y {D['TY']}")):
        x, y = px(T), py(Sad(T))
        p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{VERDE}"/>')
        p.append(txt(x, y - 14, etiqueta, VERDE, "middle", 10))
    xm, ym = px(C["T_estac_max"]), py(Sad(C["T_estac_max"]))
    p.append(f'<circle cx="{xm:.1f}" cy="{ym:.1f}" r="4" fill="none" stroke="{TINTA}" '
             f'stroke-width="1.4"/>')
    p.append(txt(xm - 14, ym - 28, f"maximo de la rampa {D['Tmaxl']} s", TINTA, "end", 10))
    xc = px(C["T_borde"])
    p.append(f'<circle cx="{xc:.1f}" cy="{yc:.1f}" r="5" fill="none" stroke="{ACENTO}" '
             f'stroke-width="1.8"/>')
    p.append(txt(xc + 12, yc - 12, f"{D['Tcorte']} s", ACENTO, "start", 11, "bold"))
    p.append(txt(xc + 12, yc - 30, "aca el recorte suelta", ACENTO, "start", 10))

    p.append(txt(24, H - 58, f"Dentro de la rampa la ordenada no es monotona: cae de "
                             f"{D['Sa0']} g en el origen a un minimo de {D['Saminl']}",
                 SUAVE, "start", 10))
    p.append(txt(24, H - 40, f"en {D['Tminl']} s, sube a {D['Samaxl']} en {D['Tmaxl']} y "
                             f"vuelve a caer a {D['Safr']} en la frontera.", SUAVE, "start", 10))
    p.append(txt(24, H - 22, f"El periodo adoptado entrega {D['cociente']} de ese maximo "
                             f"local, asi que si maximiza la respuesta de su rama.",
                 SUAVE, "start", 10))

    alt = ("El espectro de diseno horizontal contra el periodo, con el recorte de la clausula "
           "5.13 como recta horizontal en 0,29161 g: la curva baja dentro de la rampa, vuelve "
           "a subir y corta el recorte en 0,55049 s, con los dos periodos de la serie dentro "
           "del tramo gobernado por el recorte")
    return envoltura(W, H, alt, "El recorte que tapa el periodo", p)


if __name__ == "__main__":
    escribir(AQUI, {"planta": planta(), "razon": razon(), "espectro": espectro()})
