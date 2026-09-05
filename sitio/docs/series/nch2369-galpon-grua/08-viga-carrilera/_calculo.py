"""Eslabón 08 — la viga carrilera: el apoyo simple no es una simplificación sino
lo que AIST prescribe, y la clase de edificio que fija la flecha vertical no es la
clase de servicio de la grúa.

    python sitio/docs/series/nch2369-galpon-grua/08-viga-carrilera/_calculo.py [salida]

Hereda del 01, del 03, del 06 y del 07. Transcrito del memo 08 de
`Guias_Interactivas`, que leyó las cláusulas del PDF (ver la tabla de referencias
de `index.md`).

Cuatro cosas que este eslabón hace y conviene no perder de vista al leerlo:

* **El apoyo simple es una cláusula, no una comodidad.** AIST §5.8.1 prohíbe que
  se desarrolle continuidad apreciable entre vanos adyacentes; A2 mide qué
  costaría desobedecerla y A3 qué le habría hecho al 07.
* **Las dos «clase C» no son la misma letra.** La clase de servicio de la grúa
  (CMAA) y la clase de edificio (AIST) se llaman igual y deciden cosas distintas;
  la que fija la flecha vertical es la de edificio, y con la vida útil que la
  propia cláusula recomienda sería B.
* **El ancho del ala superior no lo elige el diseñador**: lo fija el límite de
  compacidad, usado en 0,956.
* **Lo que dimensiona la viga es la interacción biaxial**, y el 10,7 % que le
  agrega la torsión sale de una **tolerancia de montaje** —la excentricidad
  máxima del riel sobre el alma—, no de una carga.

**Todos los pasos se redondean a cinco decimales**, que es lo que el memo imprime
y con lo que sustituye en el paso siguiente. Las propiedades de sección se
redondean al entero, que es como el memo las escribe y las usa.

Las 147 filas del `## Resumen` van en `E.resumen()`, que las valida contra el
paso que las produce con la misma regla que `E.publicado()` aplica a las 17
salidas. Dos quedan fuera y están en `## Límites`: el memo imprimió un dígito
que su propia regla de redondeo no da, y su arnés no lo vio porque comparaba con
tolerancia relativa. Es la misma especie que las tres del 07.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from serie import Eslabon, main  # noqa: E402

E = Eslabon("nch2369-galpon-grua", orden=8, slug="viga-carrilera",
            titulo="La viga carrilera",
            normas=["AIST TR-13:2021", "CMAA 70:2010", "AISC 360-22",
                    "NCh3171:2017", "NCh2369:2025"],
            carpeta=AQUI)


def r5(x: float) -> float:
    """Cinco decimales, con redondeo medio hacia arriba."""
    return math.floor(float(x) * 1e5 + 0.5) / 1e5


def r8(x: float) -> float:
    """Ocho decimales: el término torsional de la Ec. F4-8 es tan chico que el
    memo lo imprime así, y con cinco sería cero."""
    return math.floor(float(x) * 1e8 + 0.5) / 1e8


def ent(x: float) -> float:
    """Al entero: es como el memo escribe las propiedades de sección y, sobre
    todo, cómo las **sustituye** en los pasos que siguen."""
    return float(math.floor(float(x) + 0.5))


# ------------------------------------------------------------ lo que entra
s_marco = E.entra("s_marco", de="01", paso="S1")
Qn_grua = E.entra("Qn_grua", de="01", paso="S3")
Wb_puente = E.entra("Wb_puente", de="03", paso="S2")
Wt_carro = E.entra("Wt_carro", de="03", paso="S2")
wb_ruedas = E.entra("wb_ruedas", de="03", paso="S2")
Rw_max = E.entra("Rw_max", de="03", paso="B2")
Rw_min = E.entra("Rw_min", de="03", paso="B3")
Rv_max = E.entra("Rv_max", de="03", paso="C1")
SS_total = E.entra("SS_total", de="03", paso="D1")
SS_carril = E.entra("SS_carril", de="03", paso="D3")
T_long = E.entra("T_long", de="03", paso="E1")
N_ciclos = E.entra("N_ciclos", de="03", paso="A1")
vida_grua = E.entra("vida_grua", de="03", paso="S4")
C_V = E.entra("C_V", de="06", paso="B1")
Ez_carril = E.entra("Ez_carril", de="06", paso="B3")
dlim_grua = E.entra("dlim_grua", de="06", paso="E5")
k_riel = E.entra("k_riel", de="07", paso="S1")
SS_marco = E.entra("SS_marco", de="07", paso="C1")
Rcol_grua = E.entra("Rcol_grua", de="07", paso="E3")

# lo heredado, con los decimales que su eslabón imprimió: es lo que el memo sustituyó
Rv_max_p, Rw_max_p, Rw_min_p = r5(Rv_max), r5(Rw_max), r5(Rw_min)

# ------------------------------------------------------------ el caso
# Material y factores.
Fy = E.caso("Fy", 345.0, "MPa")
E_ac = E.caso("E_ac", 200000.0, "MPa")
phi_b = E.caso("phi_b", 0.90, "—")
g_grav = E.caso("g_grav", 9.81, "m/s2")
rho_acero = E.caso("rho_acero", 7850.0, "kg/m3")

# La sección adoptada (S2), en mm.
bfs_carril = E.caso("bfs_carril", 350.0, "mm")
tfs_carril = E.caso("tfs_carril", 20.0, "mm")
hw_carril = E.caso("hw_carril", 650.0, "mm")
tw_carril = E.caso("tw_carril", 8.0, "mm")
bfi_carril = E.caso("bfi_carril", 250.0, "mm")
tfi_carril = E.caso("tfi_carril", 14.0, "mm")

# El riel declarado (S3).
h_riel_perfil = E.caso("h_riel_perfil", 131.76, "mm")
m_riel = E.caso("m_riel", 42.16, "kg/m")

# Datos de otros eslabones que su productor no prometió a éste, con su origen.
L_carrilera = E.caso("L_carrilera", 60.0, "m")     # del 05 · S1, las dos líneas
w_carril_05 = E.caso("w_carril_05", 1.20, "kN/m")  # del 05 · S1, lo que declaró
Wgrua_sc = E.caso("Wgrua_sc", 230.0, "kN")         # del 05 · C3
P_sismico = E.caso("P_sismico", 1037.085, "kN")    # del 05 · C4
d_riel_grua = E.caso("d_riel_grua", 3.08155, "mm")  # del 07 · C2
uso_grua_07 = E.caso("uso_grua_07", 0.16435, "—")   # del 07 · C2

# Constantes de cláusula.
ciclos_techoC = E.caso("ciclos_techoC", 100000.0, "ciclos")   # AIST §1.4.3
ciclos_pisoC = E.caso("ciclos_pisoC", 20000.0, "ciclos")      # AIST §1.4.3
vida_aist = E.caso("vida_aist", 50.0, "años")                 # AIST §1.4
div_v_C = E.caso("div_v_C", 600.0, "—")            # AIST §5.8.7, clase C
div_v_B = E.caso("div_v_B", 1000.0, "—")           # AIST §5.8.7, clase B
div_lat = E.caso("div_lat", 400.0, "—")            # AIST §5.8.7 · CMAA §1.4.6
c_lam_p = E.caso("c_lam_p", 0.38, "—")             # AISC Tabla B4.1b, ala
c_lam_rw = E.caso("c_lam_rw", 5.7, "—")            # AISC Tabla B4.1b, alma
c_e_riel = E.caso("c_e_riel", 0.75, "—")           # AIST §5.17.6, tres cuartos del alma
c_tope = E.caso("c_tope", 1.6, "—")                # AISC §F4 y §F11
c_Lp = E.caso("c_Lp", 1.1, "—")                    # AISC Ec. F4-7
c_Lr = E.caso("c_Lr", 1.95, "—")                   # AISC Ec. F4-8
c_676 = E.caso("c_676", 6.76, "—")                 # AISC Ec. F4-8
c_kv = E.caso("c_kv", 5.34, "—")                   # AISC §G2.1, sin atiesadores
c_Cv1 = E.caso("c_Cv1", 1.10, "—")                 # AISC Ec. G2-3
c_atie = E.caso("c_atie", 2.54, "—")               # AISC §G2.3
c_corte = E.caso("c_corte", 0.6, "—")              # AISC §G2.1
c_658 = E.caso("c_658", 0.658, "—")                # AISC Ec. E3-2
c_CMAA = E.caso("c_CMAA", 0.10, "—")               # CMAA §1.4.6, el 10 % de la rueda
f_D = E.caso("f_D", 1.2, "—")                      # NCh3171 §9.1.1
f_L = E.caso("f_L", 1.6, "—")                      # NCh3171 §9.1.1

# ================= A · el apoyo, que resulta ser una cláusula =============
coef_reac = E.paso("A1", "coef_reac", r5(1 + (s_marco - wb_ruedas) / s_marco), "—")
R_carril_s = E.paso("A1", "R_carril_s", r5(SS_carril / 2.0 * coef_reac), "kN")
coef_077 = E.paso("A2", "coef_077",
                  r5((2 * s_marco - wb_ruedas) / (2 * s_marco)), "—")
x_cont = s_marco - wb_ruedas / 2.0
eta2 = E.paso("A2", "eta2",
              r5(x_cont * (s_marco ** 2 - x_cont ** 2) / (2 * s_marco ** 3)), "—")
eta_cont = E.paso("A2", "eta_cont", r5(2 * (coef_077 + eta2)), "—")
sube_cont = E.paso("A2", "sube_cont", r5(eta_cont / coef_reac), "—")
R_carril_cont = E.paso("A2", "R_carril_cont", r5(eta_cont / 2.0 * SS_carril), "kN")
SS_marco_cont = E.paso("A3", "SS_marco_cont", r5(2 * R_carril_cont), "kN")
d_riel_cont = E.paso("A3", "d_riel_cont", r5(SS_marco_cont / k_riel * 1e3), "mm")
uso_cont = E.paso("A3", "uso_cont", r5(d_riel_cont / dlim_grua), "—")
margen_cont = E.paso("A3", "margen_cont", r5(1.0 / uso_cont), "—")

# =============== B · las dos clases C, que no son la misma letra ==========
frac_techoC = E.paso("B1", "frac_techoC", r5(N_ciclos / ciclos_techoC), "—")
veces_pisoC = E.paso("B1", "veces_pisoC", r5(N_ciclos / ciclos_pisoC), "—")
N_50 = E.paso("B2", "N_50", r5(N_ciclos * vida_aist / vida_grua), "ciclos")
sobre_techoC = E.paso("B2", "sobre_techoC", r5(N_50 / ciclos_techoC), "—")
dlim_v_C = E.paso("B3", "dlim_v_C", r5(s_marco * 1e3 / div_v_C), "mm")
dlim_v_B = E.paso("B3", "dlim_v_B", r5(s_marco * 1e3 / div_v_B), "mm")
razon_lim_v = E.paso("B3", "razon_lim_v", r5(dlim_v_C / dlim_v_B), "—")
dlim_lat = E.paso("B3", "dlim_lat", r5(s_marco * 1e3 / div_lat), "mm")

# ================= C · la sección, y el peso que el 05 no tenía ===========
d_carril = E.paso("C1", "d_carril",
                  r5(tfs_carril + hw_carril + tfi_carril), "mm")
A_sup, A_alma, A_inf = (bfs_carril * tfs_carril, hw_carril * tw_carril,
                        bfi_carril * tfi_carril)
A_carril = E.paso("C1", "A_carril", r5(A_sup + A_alma + A_inf), "mm2")
razon_alas = E.paso("C1", "razon_alas", r5(A_sup / A_inf), "—")

y_sup, y_alma = tfs_carril / 2.0, tfs_carril + hw_carril / 2.0
y_inf_c = tfs_carril + hw_carril + tfi_carril / 2.0
ybar_carril = E.paso("C2", "ybar_carril",
                     r5((A_sup * y_sup + A_alma * y_alma + A_inf * y_inf_c)
                        / A_carril), "mm")
y_inf = E.paso("C2", "y_inf", r5(d_carril - ybar_carril), "mm")
Ix_carril = E.paso("C2", "Ix_carril", ent(
    bfs_carril * tfs_carril ** 3 / 12.0 + A_sup * (ybar_carril - y_sup) ** 2
    + tw_carril * hw_carril ** 3 / 12.0 + A_alma * (y_alma - ybar_carril) ** 2
    + bfi_carril * tfi_carril ** 3 / 12.0 + A_inf * (y_inf_c - ybar_carril) ** 2), "mm4")
Sxc_carril = E.paso("C2", "Sxc_carril", ent(Ix_carril / ybar_carril), "mm3")
Sxt_carril = E.paso("C2", "Sxt_carril", ent(Ix_carril / y_inf), "mm3")
y_p = E.paso("C2", "y_p",
             r5(tfs_carril + (A_carril / 2.0 - A_sup) / tw_carril), "mm")
a_arriba, a_abajo = (y_p - tfs_carril) * tw_carril, (d_carril - tfi_carril - y_p) * tw_carril
Zx_carril = E.paso("C2", "Zx_carril", ent(
    A_sup * (y_p - y_sup) + a_arriba * (y_p - tfs_carril) / 2.0
    + a_abajo * (d_carril - tfi_carril - y_p) / 2.0
    + A_inf * (y_inf_c - y_p)), "mm3")
h_o = E.paso("C2", "h_o",
             r5(d_carril - tfs_carril / 2.0 - tfi_carril / 2.0), "mm")
h_c = E.paso("C2", "h_c", r5(2 * (ybar_carril - tfs_carril)), "mm")
h_p = E.paso("C2", "h_p", r5(2 * (y_p - tfs_carril)), "mm")
J_carril = E.paso("C2", "J_carril", ent(
    (bfs_carril * tfs_carril ** 3 + bfi_carril * tfi_carril ** 3
     + hw_carril * tw_carril ** 3) / 3.0), "mm4")
Iy_carril = E.paso("C2", "Iy_carril", ent(
    tfs_carril * bfs_carril ** 3 / 12.0 + tfi_carril * bfi_carril ** 3 / 12.0
    + hw_carril * tw_carril ** 3 / 12.0), "mm4")
ry_carril = E.paso("C2", "ry_carril", r5(math.sqrt(Iy_carril / A_carril)), "mm")

raiz_EFy = math.sqrt(E_ac / Fy)
raiz_EFy_p = E.paso("C3", "raiz_EFy", r5(raiz_EFy), "—")
lam_ala_sup = E.paso("C3", "lam_ala_sup", r5(bfs_carril / (2 * tfs_carril)), "—")
lam_p_ala = E.paso("C3", "lam_p_ala", r5(c_lam_p * raiz_EFy_p), "—")
uso_compac = E.paso("C3", "uso_compac", r5(lam_ala_sup / lam_p_ala), "—")
bf_max = E.paso("C3", "bf_max", r5(2 * lam_p_ala * tfs_carril), "mm")
lam_alma = E.paso("C3", "lam_alma", r5(h_c / tw_carril), "—")
lam_rw = E.paso("C3", "lam_rw", r5(c_lam_rw * raiz_EFy_p), "—")

w_viga = E.paso("C4", "w_viga",
                r5(A_carril * rho_acero * g_grav * 1e-9), "kN/m")
w_riel = E.paso("C4", "w_riel", r5(m_riel * g_grav * 1e-3), "kN/m")
w_carril = E.paso("C4", "w_carril", r5(w_viga + w_riel), "kN/m")
sobre_05 = E.paso("C4", "sobre_05", r5(w_carril / w_carril_05), "—")
Ez_real = E.paso("C4", "Ez_real",
                 r5(C_V * (w_carril * L_carrilera + Wgrua_sc)), "kN")
sube_Ez = E.paso("C4", "sube_Ez", r5(Ez_real / Ez_carril), "—")
W_falta = E.paso("C4", "W_falta",
                 r5((w_carril - w_carril_05) * L_carrilera), "kN")
sube_P = E.paso("C4", "sube_P", r5((P_sismico + W_falta) / P_sismico), "—")

# ========= D · las solicitaciones, y una excentricidad que no se elige ====
x1_rueda = E.paso("D1", "x1_rueda", r5(s_marco / 2.0 - wb_ruedas / 4.0), "m")
x2_rueda = E.paso("D1", "x2_rueda", r5(x1_rueda + wb_ruedas), "m")
coef_M = E.paso("D1", "coef_M", r5(coef_077 * x1_rueda), "m")
M_serv = E.paso("D1", "M_serv", r5(Rw_max_p * coef_M), "kN·m")

kappa = E.paso("D2", "kappa",
               r5((2 * Rw_max_p - Wb_puente / 2.0) / (Qn_grua + Wt_carro)), "—")
R_Cds = E.paso("D2", "R_Cds", r5(Wb_puente / 4.0 + Wt_carro * kappa / 2.0), "kN")
R_Cvs = E.paso("D2", "R_Cvs", r5(Qn_grua * kappa / 2.0), "kN")
R_suma = E.paso("D2", "R_suma", r5(R_Cds + R_Cvs), "kN")
P_aist = E.paso("D2", "P_aist",
                r5(f_D * R_Cds + f_L * (R_Cvs + (Rv_max_p - Rw_max_p))), "kN")
P_nch = E.paso("D2", "P_nch", r5(f_L * Rv_max_p), "kN")
mas_nch = E.paso("D2", "mas_nch", r5(P_nch / P_aist), "—")
w_u = E.paso("D2", "w_u", r5(f_D * w_carril), "kN/m")
R_izq = E.paso("D2", "R_izq",
               r5(coef_077 * P_nch + w_u * s_marco / 2.0), "kN")
M_ux = E.paso("D2", "M_ux",
              r5(R_izq * x1_rueda - w_u * x1_rueda ** 2 / 2.0), "kN·m")

ev_carril = E.paso("D3", "ev_carril",
                   r5(h_riel_perfil + tfs_carril / 2.0), "mm")
e_riel = E.paso("D3", "e_riel", r5(c_e_riel * tw_carril), "mm")
H_rueda = E.paso("D3", "H_rueda", r5(SS_carril / 2.0 * f_L), "kN")
T_empuje = E.paso("D3", "T_empuje", r5(H_rueda * ev_carril), "kN·mm")
T_exc = E.paso("D3", "T_exc", r5(P_nch * e_riel), "kN·mm")
T_par = E.paso("D3", "T_par", r5(T_empuje + T_exc), "kN·mm")
frac_exc = E.paso("D3", "frac_exc", r5(T_exc / T_par), "—")
F_par = E.paso("D4", "F_par", r5(T_par / h_o), "kN")
H_ala = E.paso("D4", "H_ala", r5(H_rueda + F_par), "kN")
amplif_tors = E.paso("D4", "amplif_tors", r5(H_ala / H_rueda), "—")
M_uy = E.paso("D4", "M_uy", r5(coef_M * H_ala), "kN·m")
R_serv = E.paso("D5", "R_serv",
                r5(Rv_max_p * (1 + (s_marco - wb_ruedas) / s_marco)), "kN")
V_u = E.paso("D5", "V_u", r5(f_L * R_serv + w_u * s_marco / 2.0), "kN")
P_u = E.paso("D6", "P_u", r5(f_L * T_long / 2.0), "kN")

# ================ E · resistencias e interacción biaxial ==================
M_p = E.paso("E1", "M_p", r5(Fy * Zx_carril * 1e-6), "kN·m")
tope_16 = E.paso("E1", "tope_16", r5(c_tope * Fy * Sxc_carril * 1e-6), "kN·m")
M_yc = E.paso("E1", "M_yc", r5(Fy * Sxc_carril / 1e6), "kN·m")
M_yt = E.paso("E1", "M_yt", r5(Fy * Sxt_carril * 1e-6), "kN·m")
R_pc = E.paso("E1", "R_pc", r5(M_p / M_yc), "—")
R_pt = E.paso("E1", "R_pt", r5(M_p / M_yt), "—")
razon_alturas = E.paso("E1", "razon_alturas", r5(h_c / h_p), "—")
lam_pw = E.paso("E1", "lam_pw",
                r5(razon_alturas * raiz_EFy_p / (0.54 * R_pt - 0.09) ** 2), "—")
razon_S = E.paso("E1", "razon_S", r5(Sxt_carril / Sxc_carril), "—")
F_L = E.paso("E1", "F_L", r5(Fy * razon_S), "MPa")
queda_07Fy = E.paso("E1", "queda_07Fy", r5(F_L / (0.7 * Fy)), "—")

a_w = E.paso("E2", "a_w", r5(h_c * tw_carril / (bfs_carril * tfs_carril)), "—")
r_t = E.paso("E2", "r_t", r5(bfs_carril / math.sqrt(
    12 * (h_o / d_carril + a_w / 6.0 * hw_carril ** 2 / (h_o * d_carril)))), "mm")
L_p = E.paso("E2", "L_p", r5(c_Lp * r_t * raiz_EFy_p), "mm")
term_tors = E.paso("E2", "term_tors",
                   r8(J_carril / (Sxc_carril * h_o)), "—")
L_r_ltb = E.paso("E2", "L_r_ltb", r5(
    c_Lr * r_t * E_ac / F_L * math.sqrt(
        term_tors + math.sqrt(term_tors ** 2 + c_676 * (F_L / E_ac) ** 2))), "mm")
M_A = E.paso("E2", "M_A",
             r5(R_izq * s_marco / 4.0 - w_u * (s_marco / 4.0) ** 2 / 2.0), "kN·m")
M_B = E.paso("E2", "M_B",
             r5(R_izq * s_marco / 2.0 - w_u * (s_marco / 2.0) ** 2 / 2.0
                - P_nch * (s_marco / 2.0 - x1_rueda)), "kN·m")
M_C = E.paso("E2", "M_C",
             r5(R_izq * 3 * s_marco / 4.0 - w_u * (3 * s_marco / 4.0) ** 2 / 2.0
                - P_nch * (3 * s_marco / 4.0 - x1_rueda)), "kN·m")
C_b = E.paso("E2", "C_b", r5(12.5 * M_ux / (2.5 * M_ux + 3 * M_A + 4 * M_B + 3 * M_C)), "—")
interp = E.paso("E2", "interp", r5((s_marco * 1e3 - L_p) / (L_r_ltb - L_p)), "—")
M_arranque = E.paso("E2", "M_arranque", r5(F_L * Sxc_carril * 1e-6), "kN·m")
corchete = E.paso("E2", "corchete", r5(M_p - (M_p - M_arranque) * interp), "kN·m")
Mn_LTB = E.paso("E2", "Mn_LTB", r5(C_b * corchete), "kN·m")
Cb_min = E.paso("E2", "Cb_min", r5(M_p / corchete), "—")
margen_Cb = E.paso("E2", "margen_Cb", r5(C_b / Cb_min), "—")
M_cx = E.paso("E2", "M_cx", r5(phi_b * M_p), "kN·m")
uso_fuerte = E.paso("E2", "uso_fuerte", r5(M_ux / M_cx), "—")

Z_y = E.paso("E3", "Z_y", ent(tfs_carril * bfs_carril ** 2 / 4.0), "mm3")
S_y = E.paso("E3", "S_y", ent(tfs_carril * bfs_carril ** 2 / 6.0), "mm3")
M_ny = E.paso("E3", "M_ny", r5(Fy * Z_y * 1e-6), "kN·m")
tope_y = E.paso("E3", "tope_y", r5(c_tope * Fy * S_y * 1e-6), "kN·m")
M_cy = E.paso("E3", "M_cy", r5(phi_b * M_ny), "kN·m")
uso_debil = E.paso("E3", "uso_debil", r5(M_uy / M_cy), "—")
esbeltez_punt = E.paso("E3", "esbeltez_punt", r5(s_marco * 1e3 / ry_carril), "—")
F_e = E.paso("E3", "F_e",
             r5(math.pi ** 2 * E_ac / esbeltez_punt ** 2), "MPa")
razon_FyFe = E.paso("E3", "razon_FyFe", r5(Fy / F_e), "—")
F_cr = E.paso("E3", "F_cr", r5(c_658 ** razon_FyFe * Fy), "MPa")
P_c = E.paso("E3", "P_c", r5(phi_b * F_cr * A_carril * 1e-3), "kN")

razon_axial = E.paso("E4", "razon_axial", r5(P_u / P_c), "—")
term_axial = E.paso("E4", "term_axial", r5(P_u / (2 * P_c)), "—")
interaccion = E.paso("E4", "interaccion",
                     r5(term_axial + uso_fuerte + uso_debil), "—")
uso_debil_sin = E.paso("E4", "uso_debil_sin", r5(coef_M * H_rueda / M_cy), "—")
interaccion_sin = E.paso("E4", "interaccion_sin",
                         r5(term_axial + uso_fuerte + uso_debil_sin), "—")
pesa_tors = E.paso("E4", "pesa_tors", r5(interaccion / interaccion_sin), "—")

frontera_corte = E.paso("E5", "frontera_corte",
                        r5(c_Cv1 * math.sqrt(c_kv * E_ac / Fy)), "—")
lam_alma_corte = E.paso("E5", "lam_alma_corte", r5(hw_carril / tw_carril), "—")
C_v1 = E.paso("E5", "C_v1", r5(frontera_corte / lam_alma_corte), "—")
V_n = E.paso("E5", "V_n",
             r5(c_corte * Fy * hw_carril * tw_carril * C_v1 * 1e-3), "kN")
V_c = E.paso("E5", "V_c", r5(phi_b * V_n), "kN")
uso_corte = E.paso("E5", "uso_corte", r5(V_u / V_c), "—")
umbral_atie = E.paso("E5", "umbral_atie", r5(c_atie * raiz_EFy_p), "—")
lef_carril = E.paso("E6", "lef_carril",
                    r5(2 * (h_riel_perfil + tfs_carril)), "mm")
R_n = E.paso("E6", "R_n", r5(Fy * tw_carril * lef_carril * 1e-3), "kN")
uso_alma_rueda = E.paso("E6", "uso_alma_rueda", r5(P_nch / R_n), "—")

# ============ F · las tres flechas de servicio, y la que nadie mide =======
b_flecha = E.paso("F1", "b_flecha",
                  r5((s_marco * 1e3 - wb_ruedas * 1e3) / 2.0), "mm")
L_mm = s_marco * 1e3


def flecha(P_kN: float, inercia: float) -> float:
    """Dos cargas iguales simétricas respecto del centro, a `b` de cada apoyo."""
    return (2 * P_kN * 1e3 * b_flecha * (3 * L_mm ** 2 - 4 * b_flecha ** 2)
            / (48 * E_ac * inercia))


delta_v = E.paso("F1", "delta_v", r5(flecha(Rw_max_p, Ix_carril)), "mm")
uso_v_C = E.paso("F1", "uso_v_C", r5(delta_v / dlim_v_C), "—")
uso_v_B = E.paso("F3", "uso_v_B", r5(delta_v / dlim_v_B), "—")
I_clase_B = E.paso("F3", "I_clase_B", ent(Ix_carril * uso_v_B), "mm4")
I_ala = E.paso("F2", "I_ala", ent(tfs_carril * bfs_carril ** 3 / 12.0), "mm4")
H_CMAA = E.paso("F2", "H_CMAA", r5(c_CMAA * Rw_max_p), "kN")
delta_l_CMAA = E.paso("F2", "delta_l_CMAA", r5(flecha(H_CMAA, I_ala)), "mm")
uso_l_CMAA = E.paso("F2", "uso_l_CMAA", r5(delta_l_CMAA / dlim_lat), "—")
H_AIST = E.paso("F2", "H_AIST", r5(SS_carril / 2.0), "kN")
delta_l_AIST = E.paso("F2", "delta_l_AIST", r5(flecha(H_AIST, I_ala)), "mm")
uso_l_AIST = E.paso("F2", "uso_l_AIST", r5(delta_l_AIST / dlim_lat), "—")
mayor_CMAA = E.paso("F2", "mayor_CMAA", r5(H_CMAA / H_AIST), "—")
H_CMAA_desc = E.paso("F2", "H_CMAA_desc", r5(c_CMAA * Rw_min_p), "kN")
frac_desc = E.paso("F2", "frac_desc", r5(H_CMAA_desc / H_AIST), "—")
d_total_riel = E.paso("F4", "d_total_riel",
                      r5(d_riel_grua + delta_l_CMAA), "mm")
uso_suma = E.paso("F4", "uso_suma", r5(d_total_riel / dlim_grua), "—")
veces_viga = E.paso("F4", "veces_viga", r5(delta_l_CMAA / d_riel_grua), "—")

# ------------------------------------------------------------ Sale
E.sale("bfs_carril", bfs_carril, "mm", paso="S2", heredan=["09", "10"])
E.sale("tfs_carril", tfs_carril, "mm", paso="S2", heredan=["09", "10"])
E.sale("hw_carril", hw_carril, "mm", paso="S2", heredan=["09", "10"])
E.sale("tw_carril", tw_carril, "mm", paso="S2", heredan=["09", "10"])
E.sale("bfi_carril", bfi_carril, "mm", paso="S2", heredan=["09", "10"])
E.sale("tfi_carril", tfi_carril, "mm", paso="S2", heredan=["09", "10"])
E.sale("d_carril", d_carril, "mm", paso="C1", heredan=["09", "10"])
E.sale("Ix_carril", Ix_carril, "mm4", paso="C2", heredan=["09"])
E.sale("Sxc_carril", Sxc_carril, "mm3", paso="C2", heredan=["09"])
E.sale("Sxt_carril", Sxt_carril, "mm3", paso="C2", heredan=["09"])
E.sale("ybar_carril", ybar_carril, "mm", paso="C2", heredan=["09"])
E.sale("w_carril", w_carril, "kN/m", paso="C4", heredan=["09", "10"])
E.sale("M_serv", M_serv, "kN·m", paso="D1", heredan=["09"])
E.sale("e_riel", e_riel, "mm", paso="D3", heredan=["09"])
E.sale("ev_carril", ev_carril, "mm", paso="D3", heredan=["09"])
E.sale("lef_carril", lef_carril, "mm", paso="E6", heredan=["09"])
E.sale("N_50", N_50, "ciclos", paso="B2", heredan=["09"])

# lo que el memo 08 de Guias_Interactivas imprimió en su `## Sale`
E.publicado({
    "bfs_carril": "350", "tfs_carril": "20", "hw_carril": "650",
    "tw_carril": "8", "bfi_carril": "250", "tfi_carril": "14",
    "d_carril": "684", "Ix_carril": "1265593407", "Sxc_carril": "4693473",
    "Sxt_carril": "3054404", "ybar_carril": "269,64968", "w_carril": "1,62262",
    "M_serv": "361,60455", "e_riel": "6,00", "ev_carril": "141,76",
    "lef_carril": "303,52", "N_50": "150000",
})

# y las 146 filas de su `## Resumen`
E.resumen({
    "coef_reac": "1,54667", "R_carril_s": "23,20005", "x1_rueda": "2,90000",
    "coef_077": "0,77333", "eta2": "0,15542", "eta_cont": "1,85750",
    "sube_cont": "1,20097", "R_carril_cont": "27,86250",
    "SS_marco_cont": "55,72500", "d_riel_cont": "3,70085",
    "uso_cont": "0,19738", "margen_cont": "5,06637",
    "frac_techoC": "0,75000", "veces_pisoC": "3,75000", "N_50": "150000,00000",
    "sobre_techoC": "1,50000", "dlim_v_C": "12,50000", "dlim_v_B": "7,50000",
    "razon_lim_v": "1,66667", "dlim_lat": "18,75000",
    "d_carril": "684,00000", "A_carril": "15700,00000", "razon_alas": "2,00000",
    "ybar_carril": "269,64968", "y_inf": "414,35032", "Ix_carril": "1265593407",
    "Sxc_carril": "4693473", "Sxt_carril": "3054404", "y_p": "126,25000",
    "Zx_carril": "3969188", "h_o": "667,00000", "h_c": "499,29936",
    "h_p": "212,50000", "J_carril": "1272933", "Iy_carril": "89715233",
    "ry_carril": "75,59329", "lam_ala_sup": "8,75000", "lam_p_ala": "9,14932",
    "uso_compac": "0,95636", "bf_max": "365,97280", "lam_alma": "62,41242",
    "lam_rw": "137,23987",
    "w_viga": "1,20903", "w_riel": "0,41359", "w_carril": "1,62262",
    "sobre_05": "1,35218", "Ez_real": "173,23743", "sube_Ez": "1,08396",
    "W_falta": "25,35720", "sube_P": "1,02445",
    "coef_M": "2,24266", "M_serv": "361,60455", "kappa": "0,94783",
    "R_Cds": "66,45660", "R_Cvs": "94,78300", "R_suma": "161,23960",
    "P_aist": "282,99725", "P_nch": "309,57914", "mas_nch": "1,09393",
    "w_u": "1,94714", "R_izq": "246,70861", "M_ux": "707,26725",
    "ev_carril": "141,76000", "e_riel": "6,00000", "T_par": "5259,71484",
    "T_empuje": "3402,24000", "T_exc": "1857,47484", "frac_exc": "0,35315",
    "F_par": "7,88563", "H_ala": "31,88563", "amplif_tors": "1,32857",
    "M_uy": "71,50863", "R_serv": "299,25983", "V_u": "486,11750",
    "P_u": "68,80000",
    "M_p": "1369,36986", "tope_16": "2590,79710",
    "M_yt": "1053,76938", "R_pc": "0,84568", "R_pt": "1,29950",
    # `M_yc` fuera: 345 x 4 693 473 da 1 619,248185 exacto, un empate en el
    # sexto decimal. Medio hacia arriba -- la regla del propio memo -- da
    # ...19 y el memo imprimió ...18. No se propaga: `R_pc` sale igual.
    "razon_alturas": "2,34964", "lam_pw": "151,17752", "razon_S": "0,65078",
    "F_L": "224,51910", "queda_07Fy": "0,92969",
    "a_w": "0,57063", "r_t": "97,98640", "L_p": "2595,15873",
    "term_tors": "0,00040662", "L_r_ltb": "9856,66268", "M_A": "459,15594",
    "M_B": "648,32419", "M_C": "513,32841", "C_b": "1,21458",
    "interp": "0,67546", "M_arranque": "1053,77433", "corchete": "1156,19770",
    "Mn_LTB": "1404,29460", "Cb_min": "1,18437", "margen_Cb": "1,02551",
    "M_cx": "1232,43287", "uso_fuerte": "0,57388",
    "Z_y": "612500,00000", "S_y": "408333,00000", "M_ny": "211,31250",
    "tope_y": "225,39982", "M_cy": "190,18125", "uso_debil": "0,37600",
    "esbeltez_punt": "99,21516", "F_e": "200,52737", "razon_FyFe": "1,72046",
    "F_cr": "167,91288", "P_c": "2372,60899",
    "razon_axial": "0,02900", "term_axial": "0,01450",
    "interaccion": "0,96438", "uso_debil_sin": "0,28301",
    "interaccion_sin": "0,87139", "pesa_tors": "1,10671",
    "frontera_corte": "61,20244", "lam_alma_corte": "81,25000",
    "C_v1": "0,75326", "V_n": "810,80906", "V_c": "729,72815",
    "uso_corte": "0,66616", "umbral_atie": "61,15601",
    "lef_carril": "303,52000", "R_n": "837,71520", "uso_alma_rueda": "0,36955",
    "b_flecha": "2050,00000", "delta_v": "8,26725", "uso_v_C": "0,66138",
    "uso_v_B": "1,10230", "I_clase_B": "1395063613", "I_ala": "71458333",
    "H_CMAA": "16,12391", "delta_l_CMAA": "14,64206", "uso_l_CMAA": "0,78091",
    "delta_l_AIST": "13,62144", "uso_l_AIST": "0,72648",
    "mayor_CMAA": "1,07493", "H_CMAA_desc": "5,37609", "frac_desc": "0,35841",
    "d_total_riel": "17,72361", "uso_suma": "0,94526",
    # `veces_viga` fuera: 14,64206 / 3,08155 da 4,75152 con las cifras
    # impresas, que es lo que la regla de la serie manda sustituir; el memo
    # imprime esa división y publica 4,75151, que sale de dividir sin redondear.
})

if __name__ == "__main__":
    raise SystemExit(main(sys.argv, E))
