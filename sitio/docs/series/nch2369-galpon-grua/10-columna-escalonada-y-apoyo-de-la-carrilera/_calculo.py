"""Eslabón 10 — la columna escalonada y el apoyo de la carrilera: el umbral que
descarta la ménsula es de fatiga, y ningún chequeo de tensión lo habría
encontrado.

    python sitio/docs/series/nch2369-galpon-grua/10-columna-escalonada-y-apoyo-de-la-carrilera/_calculo.py [salida]

Hereda del 01, del 03, del 06, del 07, del 08 y del 09: es el eslabón que más
consume de la serie. Transcrito del memo 10 de `Guias_Interactivas`, que leyó las
cláusulas del PDF (ver la tabla de referencias de `index.md`).

Cuatro cosas que este eslabón hace y conviene no perder de vista al leerlo:

* **§5.9.2 no dimensiona la ménsula: la admite o no la admite.** El tope de
  50 kips no es de resistencia sino de **fatiga**, y A3 lo demuestra: el rango de
  tensiones en la raíz **no depende de la reacción**, porque el módulo requerido
  crece con ella. Ningún chequeo de tensión lo habría encontrado.
* **El momento neto de excentricidad es la mitad del de la grúa sola**, porque el
  axial del techo y la reacción de la grúa caen a **lados opuestos** del
  centroide compuesto, que ya no está en el eje de la columna.
* **La columna escalonada rigidiza el marco 2,25 veces**, y con eso el período
  cruza la frontera que el 07 había puesto de techo: `R*` degrada. Y aun así no
  cuesta nada, porque el techo de §5.13 sigue mordiendo.
* **Lo que dimensiona el fuste de grúa es la Tabla 9**, por tercera vez en la
  serie, y no la compresión ni la flexión.

**Todos los pasos se redondean a cinco decimales**, que es lo que el memo imprime
y con lo que sustituye. De las 165 filas del `## Resumen`, 162 van en
`E.resumen()`; las otras tres están en `## Límites` y son la misma especie que
las del 07 y el 08: el memo imprime un dígito que su propia aritmética sobre las
cifras impresas no da.

   Lp_paso        370,489145 es un empate exacto; medio hacia arriba da ...915
                  y el memo imprimió ...914. No se propaga.
   mas_esbelto    106,29389 / 22,28895 da 4,76891 con las cifras impresas.
   esb_sup_plano  8 796,79500 / 305,89602 da 28,75747, cinco unidades del
                  28,75752 que el memo publica. Es el mayor de los tres.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from serie import Eslabon, main  # noqa: E402

E = Eslabon("nch2369-galpon-grua", orden=10,
            slug="columna-escalonada-y-apoyo-de-la-carrilera",
            titulo="La columna escalonada y el apoyo de la carrilera",
            normas=["AIST TR-13:2021", "AISC 360-22", "AISC 341-22",
                    "NCh2369:2025", "NCh3171:2017"],
            carpeta=AQUI)


def r5(x: float) -> float:
    return math.floor(float(x) * 1e5 + 0.5) / 1e5


def ent(x: float) -> float:
    return float(math.floor(float(x) + 0.5))


# ------------------------------------------------------------ lo que entra
L_luz = E.entra("L_luz", de="01", paso="S1")
s_marco = E.entra("s_marco", de="01", paso="S1")
h_libre = E.entra("h_libre", de="01", paso="S1")
Qn_grua = E.entra("Qn_grua", de="01", paso="S3")
Lg_grua = E.entra("Lg_grua", de="01", paso="S3")
h_riel = E.entra("h_riel", de="01", paso="S3")
Rw_max = E.entra("Rw_max", de="03", paso="B2")
Rv_max = E.entra("Rv_max", de="03", paso="C1")
C_V = E.entra("C_V", de="06", paso="B1")
E_z = E.entra("E_z", de="06", paso="B2")
Ez_carril = E.entra("Ez_carril", de="06", paso="B3")
D_grav = E.entra("D_grav", de="06", paso="C1")
Pu_max = E.entra("Pu_max", de="06", paso="C2")
Pu_desc = E.entra("Pu_desc", de="06", paso="C3")
dlim_grua = E.entra("dlim_grua", de="06", paso="E5")
d_col_base = E.entra("d_col_base", de="07", paso="B3")
d_col_riel = E.entra("d_col_riel", de="07", paso="B3")
d_col_nudo = E.entra("d_col_nudo", de="07", paso="B3")
bf_col = E.entra("bf_col", de="07", paso="B3")
tf_col = E.entra("tf_col", de="07", paso="B3")
tw_col = E.entra("tw_col", de="07", paso="B3")
Ag_col_riel = E.entra("Ag_col_riel", de="07", paso="B3")
Zx_col_base = E.entra("Zx_col_base", de="07", paso="B3")
Rcol_grua = E.entra("Rcol_grua", de="07", paso="E3")
Nbase_u = E.entra("Nbase_u", de="07", paso="E3")
Mbase_u = E.entra("Mbase_u", de="07", paso="S1")
bfs_carril = E.entra("bfs_carril", de="08", paso="S2")
tfs_carril = E.entra("tfs_carril", de="08", paso="S2")
hw_carril = E.entra("hw_carril", de="08", paso="S2")
tw_carril = E.entra("tw_carril", de="08", paso="S2")
bfi_carril = E.entra("bfi_carril", de="08", paso="S2")
tfi_carril = E.entra("tfi_carril", de="08", paso="S2")
d_carril = E.entra("d_carril", de="08", paso="C1")
w_carril = E.entra("w_carril", de="08", paso="C4")
Nfat_carril = E.entra("Nfat_carril", de="09", paso="A3")
sr_sup_carril = E.entra("sr_sup_carril", de="09", paso="B2")
sr_inf_carril = E.entra("sr_inf_carril", de="09", paso="B2")
a_alma_ala = E.entra("a_alma_ala", de="09", paso="D6")
FSR_catC = E.entra("FSR_catC", de="09", paso="E4")
FSR_catE = E.entra("FSR_catE", de="09", paso="E1")
FSR_catEp = E.entra("FSR_catEp", de="09", paso="E2")

# lo heredado, con los decimales que su eslabón imprimió
Rv_max_p, Rw_max_p = r5(Rv_max), r5(Rw_max)

# ------------------------------------------------------------ el caso
Fy = E.caso("Fy", 345.0, "MPa")
Ry = E.caso("Ry", 1.10, "—")
E_ac = E.caso("E_ac", 200000.0, "MPa")
Fexx = E.caso("Fexx", 490.0, "MPa")
phi_b = E.caso("phi_b", 0.90, "—")
phi_w = E.caso("phi_w", 0.75, "—")
cos45 = E.caso("cos45", 0.70711, "—")
g_grav = E.caso("g_grav", 9.81, "m/s2")
rho_acero = E.caso("rho_acero", 7850.0, "kg/m3")
n_columnas = E.caso("n_columnas", 10, "—")
n_marcos = E.caso("n_marcos", 5, "—")

# El fuste de grúa adoptado (S2) y la placa de alma (S3), en mm.
d_fuste_grua = E.caso("d_fuste_grua", 400.0, "mm")
bf_fuste_grua = E.caso("bf_fuste_grua", 300.0, "mm")
tf_fuste_grua = E.caso("tf_fuste_grua", 16.0, "mm")
tw_fuste_grua = E.caso("tw_fuste_grua", 10.0, "mm")
tf_fuste_14 = E.caso("tf_fuste_14", 14.0, "mm")     # el ala que no pasa (D0)
tp_alma = E.caso("tp_alma", 10.0, "mm")

# El atiesador de apoyo adoptado (F1), en mm.
b_st = E.caso("b_st", 110.0, "mm")
t_st = E.caso("t_st", 12.0, "mm")
recorte_st = E.caso("recorte_st", 25.0, "mm")       # el destalonado de contacto
n_tw_st = E.caso("n_tw_st", 12.0, "—")              # el alma que participa, 12 t_w
l_asiento = E.caso("l_asiento", 150.0, "mm")        # F2, el largo del asiento
h_riel_perfil = E.caso("h_riel_perfil", 131.76, "mm")   # del 08 · S3
sep_grapas_adopt = E.caso("sep_grapas_adopt", 750.0, "mm")  # F4, la adoptada

# El campo declarado del modelo del 07, y lo que el 07 imprimió y no publica.
k_Y = E.caso("k_Y", 5612.11747, "kN/m")             # del 07 · S1
k_esc = E.caso("k_esc", 2.24801, "—")               # D6, del modelo declarado
T_star_Y2 = E.caso("T_star_Y2", 0.38566, "s")       # del 07 · B5
Sa_Y2 = E.caso("Sa_Y2", 1.22333, "g")               # del 07 · B5
Q0_an_2 = E.caso("Q0_an_2", 366.06989, "kN")        # del 07 · B6
d_Y2 = E.caso("d_Y2", 65.22861, "mm")               # del 07 · C5
theta_Y2 = E.caso("theta_Y2", 0.02130, "—")         # del 07 · C6
Vu_col = E.caso("Vu_col", 105.84698, "kN")          # del 07 · E3
Pu_marco = E.caso("Pu_marco", 396.46548, "kN")      # del 07 · F2
Q0_marco = E.caso("Q0_marco", 60.48399, "kN")       # del 07 · E3
w_marco_07 = E.caso("w_marco_07", 73.25955, "kN")   # del 07 · B4
Ag_col_base = E.caso("Ag_col_base", 27284.0, "mm2")     # del 07 · B3
Ag_col_nudo = E.caso("Ag_col_nudo", 23084.0, "mm2")     # del 07 · B3
I_base_07 = E.caso("I_base_07", 4675712519.0, "mm4")    # del 07 · B3
phiMn_base_07 = E.caso("phiMn_base_07", 3206.51052, "kN·m")  # del 07 · F2
Q0_Y = E.caso("Q0_Y", 302.41994, "kN")              # del 05 · D5
P_sismico = E.caso("P_sismico", 1037.085, "kN")     # del 05 · C4
ArS = E.caso("ArS", 0.441, "g")                     # del 04 · A3
r_s = E.caso("r_s", 4.5, "—")                       # del 04 · A2
T_0 = E.caso("T_0", 0.40, "s")                      # del 04 · A2
p_suelo = E.caso("p_suelo", 1.5, "—")               # del 04 · A2
q_s = E.caso("q_s", 3.0, "—")                       # del 04 · A2
Cr_T1 = E.caso("Cr_T1", 0.28, "s")                  # del 04 · C2
R_T7 = E.caso("R_T7", 5.0, "—")                     # del 01 · D1
kcap_Y = E.caso("kcap_Y", 3.5, "—")                 # del 05 · F2
d_lim = E.caso("d_lim", 157.5, "mm")                # del 06 · E1
w_columna_05 = E.caso("w_columna_05", 1.75, "kN/m")  # del 05 · S1
wb_ruedas = E.caso("wb_ruedas", 3.4, "m")            # del 03 · S2
I_nudo_col = E.caso("I_nudo_col", 2160024719.0, "mm4")   # del 07 · B3

# Constantes de cláusula.
kip = E.caso("kip", 4.44822, "kN")                  # 1 kip
tope_kips_50 = E.caso("tope_kips_50", 50.0, "kips")  # AIST §5.9.2
lb_ton = E.caso("lb_ton", 2000.0, "lb")             # una short ton
kgf = E.caso("kgf", 9.80665, "m/s2")
pulgada = E.caso("pulgada", 25.4, "mm")
c_ala = E.caso("c_ala", 0.40, "—")                  # Tabla 9
c_alma = E.caso("c_alma", 3.96, "—")
c_alma_Ca = E.caso("c_alma_Ca", 3.04, "—")
c_nocional = E.caso("c_nocional", 0.002, "—")       # AISC §C2.2b
c_tau = E.caso("c_tau", 0.80, "—")                  # AISC §C2.3
c_B2 = E.caso("c_B2", 1.70, "—")                    # AISC §C2.2b
c_658 = E.caso("c_658", 0.658, "—")
c_st_esb = E.caso("c_st_esb", 0.56, "—")            # AISC Tabla B4.1a
c_st_K = E.caso("c_st_K", 0.75, "—")                # AISC §J10.8
c_pb = E.caso("c_pb", 1.8, "—")                     # AISC §J7
c_yield_alma = E.caso("c_yield_alma", 2.5, "—")     # AISC §J10.2
mu_desliz = E.caso("mu_desliz", 0.30, "—")          # AISC §J3.8
Du_desliz = E.caso("Du_desliz", 1.13, "—")
Tb_M20 = E.caso("Tb_M20", 142.0, "kN")              # AISC Tabla J3.1
Fnv_M20 = E.caso("Fnv_M20", 457.0, "MPa")           # AISC Tabla J3.2
Ab_M20 = E.caso("Ab_M20", 314.16, "mm2")
R_carril_s = E.caso("R_carril_s", 23.20000, "kN")   # del 07 · C1
sep_grapas_in = E.caso("sep_grapas_in", 30.0, "in")  # AIST §5.15.3
tope_tons = E.caso("tope_tons", 20.0, "tons")       # AIST §5.15.3
sep_J35 = E.caso("sep_J35", 24.0, "—")              # AISC §J3.5, 24 t
tope_12in = E.caso("tope_12in", 12.0, "in")
f_D = E.caso("f_D", 1.2, "—")
f_L = E.caso("f_L", 1.6, "—")


def i_soldada(d, bf, tf, tw):
    """Doble T soldada: inercia fuerte."""
    return (bf * d ** 3 - (bf - tw) * (d - 2 * tf) ** 3) / 12.0


def d_col(z):
    """Canto de la columna del edificio a la cota `z` en mm."""
    return d_col_base - (d_col_base - d_col_nudo) * z / (h_libre * 1e3)


def compuesta(d):
    """Sección compuesta a la cota donde la columna mide `d`: `(A, ybar, Ix, Iy)`.

    El fuste de grúa tiene su eje sobre el del riel, a `-e` del eje de columna;
    la placa va de la cara interior del fuste del edificio a la cara del fuste de
    grúa que la mira. `ybar` se mide desde el eje de la columna.
    """
    y_g = -e_col_riel
    y_int, y_fus = -d / 2.0, y_g + d_fuste_grua / 2.0
    l_p = y_int - y_fus
    hw = d - 2 * tf_col
    hf = d_fuste_grua - 2 * tf_fuste_grua
    partes = [
        (bf_col * tf_col, (d - tf_col) / 2.0, bf_col, tf_col),
        (bf_col * tf_col, -(d - tf_col) / 2.0, bf_col, tf_col),
        (tw_col * hw, 0.0, tw_col, hw),
        (tp_alma * l_p, (y_int + y_fus) / 2.0, tp_alma, l_p),
        (bf_fuste_grua * tf_fuste_grua, y_g + (d_fuste_grua - tf_fuste_grua) / 2.0,
         bf_fuste_grua, tf_fuste_grua),
        (bf_fuste_grua * tf_fuste_grua, y_g - (d_fuste_grua - tf_fuste_grua) / 2.0,
         bf_fuste_grua, tf_fuste_grua),
        (tw_fuste_grua * hf, y_g, tw_fuste_grua, hf),
    ]
    A = sum(a for a, _, _, _ in partes)
    yb = sum(a * y for a, y, _, _ in partes) / A
    ix = sum(b * h ** 3 / 12.0 + a * (y - yb) ** 2 for a, y, b, h in partes)
    iy = sum(h * b ** 3 / 12.0 for _, _, b, h in partes)
    return A, yb, ix, iy


def forma_H(T):
    u = T / T_0
    return (1 + r_s * u ** p_suelo) / (1 + u ** q_s)


# ======= A · el umbral que descarta la ménsula, y que es de fatiga =======
c_R = E.paso("A1", "c_R", r5(1 + (s_marco - wb_ruedas) / s_marco), "—")
R_u_reob = E.paso("A1", "R_u_reob", r5(Rv_max_p * c_R), "kN")
cierre_07 = E.paso("A1", "cierre_07", r5(R_u_reob - Rcol_grua), "kN")
tope_kips = E.paso("A1", "tope_kips", r5(tope_kips_50 * kip), "kN")
R_kips = E.paso("A1", "R_kips", r5(Rcol_grua / kip), "—")
uso_mensula = E.paso("A1", "uso_mensula", r5(Rcol_grua / tope_kips), "—")

e_col_riel = E.paso("A2", "e_col_riel", r5((L_luz - Lg_grua) / 2.0 * 1e3), "mm")
h_asiento = E.paso("A2", "h_asiento",
                   r5(h_riel * 1e3 - h_riel_perfil - d_carril), "mm")
M_u_raiz = E.paso("A2", "M_u_raiz",
                  r5(f_L * Rcol_grua * e_col_riel / 1e3), "kN·m")
R_fat_apoyo = E.paso("A2", "R_fat_apoyo", r5(Rw_max_p * c_R), "kN")
M_fat_raiz = E.paso("A2", "M_fat_raiz", r5(R_fat_apoyo * e_col_riel / 1e3), "kN·m")
S_req_x = M_u_raiz * 1e6 / (phi_b * Fy)        # sin redondear: es con el que divide
S_req = E.paso("A2", "S_req", ent(S_req_x), "mm3")
sr_raiz = E.paso("A2", "sr_raiz", r5(M_fat_raiz * 1e6 / S_req_x), "MPa")
uso_raiz_C = E.paso("A3", "uso_raiz_C", r5(sr_raiz / FSR_catC), "—")
uso_raiz_E = E.paso("A3", "uso_raiz_E", r5(sr_raiz / FSR_catE), "—")
uso_raiz_Ep = E.paso("A3", "uso_raiz_Ep", r5(sr_raiz / FSR_catEp), "—")
sr_invariante = E.paso("A3", "sr_invariante",
                       r5(R_fat_apoyo / (f_L * Rcol_grua) * phi_b * Fy), "MPa")
pide_fatiga = E.paso("A3", "pide_fatiga", r5(sr_raiz / FSR_catEp), "—")
sep_independiente = E.paso("A4", "sep_independiente",
                           r5(e_col_riel / d_col_base), "—")
d_paso = E.paso("B1", "d_paso", r5(d_col(h_asiento)), "mm")
mas_que_riel = E.paso("A4", "mas_que_riel", r5(d_paso / d_col_riel), "—")

# ========= B · la columna escalonada: geometría y sección compuesta ======
H_col_mm = E.paso("B1", "H_col_mm", r5(h_libre * 1e3), "mm")
L_sup = E.paso("B1", "L_sup", r5(H_col_mm - h_asiento), "mm")
a_r = E.paso("B1", "a_r", r5(L_sup / (h_libre * 1e3)), "—")
Lp_base = E.paso("B2", "Lp_base",
                 r5((e_col_riel - d_fuste_grua / 2.0) - d_col_base / 2.0), "mm")
Lp_paso = E.paso("B2", "Lp_paso",
                 r5((e_col_riel - d_fuste_grua / 2.0) - d_paso / 2.0), "mm")

A_b, yb_b, ix_b, iy_b = compuesta(d_col_base)
A_p, yb_p, _, _ = compuesta(d_paso)
Ag_comp_base = E.paso("B3", "Ag_comp_base", r5(A_b), "mm2")
xb_comp_base = E.paso("B3", "xb_comp_base", r5(yb_b), "mm")
Ix_comp_base = E.paso("B3", "Ix_comp_base", ent(ix_b), "mm4")
Iy_comp_base = E.paso("B3", "Iy_comp_base", ent(iy_b), "mm4")
Ag_comp_paso = E.paso("B3", "Ag_comp_paso", r5(A_p), "mm2")
xb_comp_paso = E.paso("B3", "xb_comp_paso", r5(yb_p), "mm")
multiplica_I = E.paso("B3", "multiplica_I", r5(Ix_comp_base / I_base_07), "—")
I_sup_paso = E.paso("B4", "I_sup_paso",
                    ent(i_soldada(d_paso, bf_col, tf_col, tw_col)), "mm4")
B_param = E.paso("B4", "B_param", r5(Ix_comp_base / I_sup_paso), "—")

rg = rho_acero * g_grav * 1e-9
w_07 = E.paso("B5", "w_07", r5((Ag_col_base + Ag_col_nudo) / 2.0 * rg), "kN/m")
A_add_base = tp_alma * Lp_base + 2 * bf_fuste_grua * tf_fuste_grua \
    + (d_fuste_grua - 2 * tf_fuste_grua) * tw_fuste_grua
A_add_paso = tp_alma * Lp_paso + 2 * bf_fuste_grua * tf_fuste_grua \
    + (d_fuste_grua - 2 * tf_fuste_grua) * tw_fuste_grua
w_add = E.paso("B5", "w_add", r5((A_add_base + A_add_paso) / 2.0 * rg), "kN/m")
frac_altura = E.paso("C3", "frac_altura", r5(h_asiento / (h_libre * 1e3)), "—")
w_col_10 = E.paso("B5", "w_col_10",
                  r5(w_07 + w_add * h_asiento / (h_libre * 1e3)), "kN/m")
supera_05 = E.paso("B5", "supera_05", r5(w_col_10 / w_columna_05), "—")
acero_marco = E.paso("B5", "acero_marco", r5(2 * w_col_10 * h_libre), "kN")
Ez_carril_real = E.paso("B5", "Ez_carril_real",
                        r5(C_V * (w_carril * 60.0 + 230.0)), "kN")
w_marco_10 = E.paso("B5", "w_marco_10",
                    r5(w_marco_07 - 2 * w_07 * h_libre + acero_marco), "kN")

Q_fuste = E.paso("B6", "Q_fuste",
                 ent((2 * bf_fuste_grua * tf_fuste_grua
                      + (d_fuste_grua - 2 * tf_fuste_grua) * tw_fuste_grua)
                     * abs(-e_col_riel - xb_comp_base)), "mm3")
q_placa = E.paso("B6", "q_placa",
                 r5(Vu_col * 1e3 * Q_fuste / Ix_comp_base), "N/mm")
R_filetes = E.paso("B6", "R_filetes",
                   r5(2 * phi_w * 0.60 * Fexx * cos45 * a_alma_ala), "N/mm")
uso_placa = E.paso("B6", "uso_placa", r5(q_placa / R_filetes), "—")

# ================== C · por dónde bajan los 299,26 kN ====================
N_sup = E.paso("C1", "N_sup", r5(Nbase_u - Rcol_grua), "kN")
w_fuste_inf = E.paso("C1", "w_fuste_inf",
                     r5((w_07 + w_add) * h_asiento / 1e3), "kN")
N_agrega = E.paso("C1", "N_agrega", r5(Rcol_grua + f_D * w_fuste_inf), "kN")
razon_P1P2 = E.paso("C1", "razon_P1P2", r5(N_sup / N_agrega), "—")
e_1 = E.paso("C1", "e_1", r5(0.0 - xb_comp_paso), "mm")
e_2 = E.paso("C1", "e_2", r5(-e_col_riel - xb_comp_paso), "mm")
M_1 = E.paso("C2", "M_1", r5(N_sup * e_1 / 1e3), "kN·m")
M_2 = E.paso("C2", "M_2", r5(Rcol_grua * e_2 / 1e3), "kN·m")
Mecc_10 = E.paso("C2", "Mecc_10", r5(M_1 + M_2), "kN·m")
cancela = E.paso("C2", "cancela", r5(M_1 / abs(M_2)), "—")
sobrestima = E.paso("C2", "sobrestima", r5(abs(M_2) / abs(Mecc_10)), "—")
frac_axial = E.paso("C3", "frac_axial", r5(N_sup / Nbase_u), "—")
comb_comprime = E.paso("C4", "comb_comprime", r5(Pu_max / n_columnas), "kN")
comb_descarga = E.paso("C4", "comb_descarga", r5(Pu_desc / n_columnas), "kN")
C_V_reob = E.paso("C4", "C_V_reob", r5(E_z / D_grav), "—")
N_con_peso = E.paso("C4", "N_con_peso", r5(Nbase_u + f_D * w_fuste_inf), "kN")
sube_axial = E.paso("C4", "sube_axial", r5(N_con_peso / Nbase_u), "—")

# ============ D · la estabilidad, por la ruta que §5.9.4 nombra ==========
raiz_ERyFy = math.sqrt(E_ac / (Ry * Fy))
lam_md = E.paso("D0", "lam_md", r5(c_ala * raiz_ERyFy), "—")
lam_ala_fuste = E.paso("D0", "lam_ala_fuste",
                       r5((bf_fuste_grua - tw_fuste_grua) / 2.0 / tf_fuste_grua), "—")
uso_ala_fuste = E.paso("D0", "uso_ala_fuste", r5(lam_ala_fuste / lam_md), "—")
lam_ala_14 = E.paso("D0", "lam_ala_14",
                    r5((bf_fuste_grua - tw_fuste_grua) / 2.0 / tf_fuste_14), "—")
uso_ala_14 = E.paso("D0", "uso_ala_14", r5(lam_ala_14 / lam_md), "—")
Ca_comp = E.paso("D0", "Ca_comp",
                 r5(Nbase_u * 1e3 / (phi_b * Ry * Fy * Ag_comp_base)), "—")
lam_alma_md = E.paso("D0", "lam_alma_md",
                     r5(c_alma * (1 - c_alma_Ca * Ca_comp) * raiz_ERyFy), "—")
lam_alma_07 = E.paso("D0", "lam_alma_07",
                     r5((d_col_base - 2 * tf_col) / tw_col), "—")
uso_alma_07 = E.paso("D0", "uso_alma_07", r5(lam_alma_07 / lam_alma_md), "—")
lam_alma_fuste = E.paso("D0", "lam_alma_fuste",
                        r5((d_fuste_grua - 2 * tf_fuste_grua) / tw_fuste_grua), "—")
uso_alma_fuste = E.paso("D0", "uso_alma_fuste",
                        r5(lam_alma_fuste / lam_alma_md), "—")
metodos = E.paso("D1", "metodos", r5(3 - 1), "—")

razon_fluencia = E.paso("D2", "razon_fluencia",
                        r5(Nbase_u / (Fy * Ag_comp_base * 1e-3)), "—")
tau_b = E.paso("D2", "tau_b", r5(1.0), "—")
N_nocional = E.paso("D2", "N_nocional", r5(c_nocional * Pu_marco), "kN")
frac_lateral = E.paso("D2", "frac_lateral", r5(N_nocional / Q0_marco), "—")
f_deriva = E.paso("D6", "f_deriva", r5(0.94557 * (0.25722 / 0.38566) ** 2), "—")
theta_red = E.paso("D3", "theta_red", r5(theta_Y2 * f_deriva / c_tau), "—")
B_2 = E.paso("D3", "B_2", r5(1.0 / (1.0 - theta_red)), "—")
uso_17 = E.paso("D3", "uso_17", r5(B_2 / c_B2), "—")

K_L_070 = E.caso("K_L_070", 1.21272, "—")   # Comm Tabla 2 de AIST, interpolada
K_L_080 = E.caso("K_L_080", 1.22272, "—")
E.paso("D4", "K_L_070", K_L_070, "—")
E.paso("D4", "K_L_080", K_L_080, "—")
K_L = E.paso("D4", "K_L",
             r5(K_L_070 + (K_L_080 - K_L_070) * (razon_P1P2 - 0.70) / 0.10), "—")
K_U = E.paso("D4", "K_U",
             r5(K_L * math.sqrt((1 + razon_P1P2) / (razon_P1P2 * B_param))), "—")
L_ef_inf = E.paso("D4", "L_ef_inf", r5(K_L * h_libre * 1e3), "mm")
L_ef_sup = E.paso("D4", "L_ef_sup", r5(K_U * h_libre * 1e3), "mm")
r_x = E.paso("D5", "r_x", r5(math.sqrt(Ix_comp_base / Ag_comp_base)), "mm")
r_y_comp = E.paso("D5", "r_y_comp", r5(math.sqrt(Iy_comp_base / Ag_comp_base)), "mm")
esb_plano_Lef = E.paso("D5", "esb_plano_Lef", r5(L_ef_inf / r_x), "—")
esb_plano_directo = E.paso("D5", "esb_plano_directo", r5(h_asiento / r_x), "—")
esb_fuera = E.paso("D5", "esb_fuera", r5(h_asiento / r_y_comp), "—")
mas_esbelto = E.paso("D5", "mas_esbelto", r5(esb_fuera / esb_plano_Lef), "—")

k_esc_marco = E.paso("D6", "k_esc_marco", r5(k_Y * k_esc), "kN/m")
T_esc = E.paso("D6", "T_esc", r5(T_star_Y2 / math.sqrt(k_esc)), "s")
techo_07 = E.paso("D6", "techo_07", r5((T_star_Y2 / Cr_T1) ** 2), "—")
cruza_techo = E.paso("D6", "cruza_techo", r5(k_esc / techo_07), "—")
R_deg = E.paso("D6", "R_deg", r5(1.5 + (R_T7 - 1.5) * T_esc / Cr_T1), "—")
cuanto_degrada = E.paso("D6", "cuanto_degrada", r5(R_T7 / R_deg), "—")
kcap_nuevo = E.paso("D6", "kcap_nuevo", r5(0.7 * R_deg), "—")
contra_350 = E.paso("D6", "contra_350", r5(kcap_nuevo / kcap_Y), "—")
Sa_nuevo = E.paso("D6", "Sa_nuevo", r5(ArS * forma_H(T_esc)), "g")
baja_ord = E.paso("D6", "baja_ord", r5(Sa_nuevo / Sa_Y2), "—")
Q0_esc = E.paso("D6", "Q0_esc", r5(Q0_an_2 * baja_ord * cuanto_degrada), "kN")
supera_techo = E.paso("D6", "supera_techo", r5(Q0_esc / Q0_Y), "—")
d_esc = E.paso("D6", "d_esc", r5(d_Y2 * f_deriva), "mm")
uso_63 = E.paso("D6", "uso_63", r5(d_esc / d_lim), "—")

# ================== E · las resistencias de los dos fustes ===============
F_e_inf = E.paso("E1", "F_e_inf",
                 r5(math.pi ** 2 * E_ac / esb_fuera ** 2), "MPa")
razon_FyFe = E.paso("E1", "razon_FyFe", r5(Fy / F_e_inf), "—")
F_cr_inf = E.paso("E1", "F_cr_inf", r5(c_658 ** razon_FyFe * Fy), "MPa")
phiPn_inf = E.paso("E1", "phiPn_inf",
                   r5(phi_b * F_cr_inf * Ag_comp_base * 1e-3), "kN")
uso_axial_inf = E.paso("E1", "uso_axial_inf", r5(Nbase_u / phiPn_inf), "—")
c_1 = E.paso("E2", "c_1", r5(d_col_base / 2.0 - xb_comp_base), "mm")
c_2 = E.paso("E2", "c_2",
             r5(e_col_riel + d_fuste_grua / 2.0 + xb_comp_base), "mm")
S_x1 = E.paso("E2", "S_x1", ent(Ix_comp_base / c_1), "mm3")
phiMn_inf = E.paso("E2", "phiMn_inf", r5(phi_b * Fy * S_x1 * 1e-6), "kN·m")
M_u_inf = E.paso("E2", "M_u_inf", r5(Mbase_u + abs(Mecc_10)), "kN·m")
uso_flex_inf = E.paso("E2", "uso_flex_inf", r5(M_u_inf / phiMn_inf), "—")
interaccion = E.paso("E2", "interaccion",
                     r5(uso_axial_inf / 2.0 + uso_flex_inf), "—")
multiplica_cap = E.paso("E2", "multiplica_cap",
                        r5(phiMn_inf / phiMn_base_07), "—")
Iy_nudo = E.paso("E3", "Iy_nudo",
                 ent(2 * tf_col * bf_col ** 3 / 12.0
                     + (d_col_nudo - 2 * tf_col) * tw_col ** 3 / 12.0), "mm4")
ry_sup = E.paso("E3", "ry_sup", r5(math.sqrt(Iy_nudo / Ag_col_nudo)), "mm")
esb_sup_fuera = E.paso("E3", "esb_sup_fuera", r5(L_sup / ry_sup), "—")
rx_sup = E.paso("E3", "rx_sup", r5(math.sqrt(I_nudo_col / Ag_col_nudo)), "mm")
esb_sup_plano = E.paso("E3", "esb_sup_plano", r5(L_ef_sup / rx_sup), "—")
ancho_base = E.paso("E4", "ancho_base",
                    r5(d_col_base / 2.0 + e_col_riel + d_fuste_grua / 2.0), "mm")
mayor_07 = E.paso("E4", "mayor_07", r5(ancho_base / d_col_base), "—")
pos_centroide = E.paso("E4", "pos_centroide",
                       r5(abs(xb_comp_base) / ancho_base), "—")

# ========== F · el apoyo de la carrilera sobre el fuste de grúa ==========
R_u_apoyo = E.paso("F1", "R_u_apoyo",
                   r5(f_L * Rcol_grua + f_D * w_carril * s_marco / 2.0), "kN")
esb_atiesador = E.paso("F1", "esb_atiesador", r5(b_st / t_st), "—")
lim_esb_at = E.paso("F1", "lim_esb_at",
                    r5(c_st_esb * math.sqrt(E_ac / Fy)), "—")
A_st = E.paso("F1", "A_st",
              r5(2 * b_st * t_st + n_tw_st * tw_carril * tw_carril), "mm2")
h_st = 2 * b_st + tw_carril
I_st = E.paso("F1", "I_st", ent(t_st * h_st ** 3 / 12.0), "mm4")
r_st = E.paso("F1", "r_st", r5(math.sqrt(I_st / A_st)), "mm")
esb_st_col = E.paso("F1", "esb_st_col", r5(c_st_K * hw_carril / r_st), "—")
F_e_st = r5(math.pi ** 2 * E_ac / esb_st_col ** 2)
F_cr_st = r5(c_658 ** (Fy / F_e_st) * Fy)
phiPn_st = E.paso("F1", "phiPn_st", r5(phi_b * F_cr_st * A_st * 1e-3), "kN")
uso_st_col = E.paso("F1", "uso_st_col", r5(R_u_apoyo / phiPn_st), "—")
A_pb = E.paso("F1", "A_pb", r5(2 * (b_st - recorte_st) * t_st), "mm2")
phiRn_pb = E.paso("F1", "phiRn_pb", r5(phi_w * c_pb * Fy * A_pb * 1e-3), "kN")
uso_st_contacto = E.paso("F1", "uso_st_contacto", r5(R_u_apoyo / phiRn_pb), "—")
phiRn_alma = E.paso("F2", "phiRn_alma",
                    r5(Fy * tw_carril * (c_yield_alma * tfs_carril + l_asiento)
                       * 1e-3), "kN")
uso_alma_sin = E.paso("F2", "uso_alma_sin", r5(R_u_apoyo / phiRn_alma), "—")
uso_tir_C = E.paso("F3", "uso_tir_C", r5(sr_sup_carril / FSR_catC), "—")
uso_tir_E = E.paso("F3", "uso_tir_E", r5(sr_sup_carril / FSR_catE), "—")
uso_tir_Ep = E.paso("F3", "uso_tir_Ep", r5(sr_sup_carril / FSR_catEp), "—")
uso_inf_C = E.paso("F3", "uso_inf_C", r5(sr_inf_carril / FSR_catC), "—")
uso_inf_E = E.paso("F3", "uso_inf_E", r5(sr_inf_carril / FSR_catE), "—")
uso_inf_Ep = E.paso("F3", "uso_inf_Ep", r5(sr_inf_carril / FSR_catEp), "—")
razon_alas = E.paso("F3", "razon_alas", r5(sr_inf_carril / sr_sup_carril), "—")

short_ton = E.paso("F4", "short_ton", r5(lb_ton * kip / 1000.0), "kN")
cap_short_tons = E.paso("F4", "cap_short_tons", r5(Qn_grua / short_ton), "—")
uso_tope_20 = E.paso("F4", "uso_tope_20", r5(cap_short_tons / tope_tons), "—")
cap_metricas = E.paso("F4", "cap_metricas", r5(Qn_grua / kgf), "—")
sep_grapas = E.paso("F4", "sep_grapas", r5(sep_grapas_in * pulgada), "mm")
espacios_grapas = E.paso("F4", "espacios_grapas",
                         r5(s_marco * 1e3 / sep_grapas_adopt), "—")
luz_junta = E.paso("F5", "luz_junta", r5(pulgada / 16.0), "mm")
veces_altura = E.paso("F5", "veces_altura", r5(h_riel_perfil / luz_junta), "—")

# ======= G · las conexiones, que dos cláusulas nunca usadas gobiernan =====
T_u_tirante = E.paso("G1", "T_u_tirante", r5(f_L * R_carril_s), "kN")
R_n_desliz = E.paso("G1", "R_n_desliz", r5(mu_desliz * Du_desliz * Tb_M20), "kN")
uso_tirante = E.paso("G1", "uso_tirante", r5(T_u_tirante / (2 * R_n_desliz)), "—")
R_n_corte = E.paso("G1", "R_n_corte",
                   r5(phi_w * Fnv_M20 * Ab_M20 * 1e-3), "kN")
cuesta_desliz = E.paso("G1", "cuesta_desliz", r5(R_n_corte / R_n_desliz), "—")
sep_J35_mm = E.paso("G2", "sep_J35_mm", r5(sep_J35 * tp_alma), "mm")
tope_12in_mm = E.paso("G2", "tope_12in_mm", r5(tope_12in * pulgada), "mm")
cual_gobierna = E.paso("G2", "cual_gobierna", r5(sep_J35_mm / tope_12in_mm), "—")

# ------------------------------------------------------------ Sale
E.sale("e_col_riel", e_col_riel, "mm", paso="A2", heredan=["12"])
E.sale("h_asiento", h_asiento, "mm", paso="A2", heredan=["11", "12"])
E.sale("d_fuste_grua", d_fuste_grua, "mm", paso="S2", heredan=["13"])
E.sale("bf_fuste_grua", bf_fuste_grua, "mm", paso="S2", heredan=["13"])
E.sale("tf_fuste_grua", tf_fuste_grua, "mm", paso="S2", heredan=["13"])
E.sale("tw_fuste_grua", tw_fuste_grua, "mm", paso="S2", heredan=["13"])
E.sale("tp_alma", tp_alma, "mm", paso="S3", heredan=["13"])
E.sale("Ag_comp_base", Ag_comp_base, "mm2", paso="B3", heredan=["13"])
E.sale("Ix_comp_base", Ix_comp_base, "mm4", paso="B3", heredan=["13"])
E.sale("xb_comp_base", xb_comp_base, "mm", paso="B3", heredan=["13"])
E.sale("Mecc_10", Mecc_10, "kN·m", paso="C2", heredan=["13"])
E.sale("w_col_10", w_col_10, "kN/m", paso="B5", heredan=["12"])
E.sale("w_marco_10", w_marco_10, "kN", paso="B5", heredan=["11"])
E.sale("k_esc", k_esc, "—", paso="D6", heredan=["11", "12"])

E.publicado({
    "e_col_riel": "1000,00000", "h_asiento": "6684,24000",
    "d_fuste_grua": "400", "bf_fuste_grua": "300", "tf_fuste_grua": "16",
    "tw_fuste_grua": "10", "tp_alma": "10", "Ag_comp_base": "43314,00000",
    "Ix_comp_base": "14310239430", "xb_comp_base": "-348,66036",
    "Mecc_10": "-93,21091", "w_col_10": "2,74863", "w_marco_10": "90,25",
    "k_esc": "2,24801",
})

E.resumen({
    "c_R": "1,54667", "R_u_reob": "299,26048", "cierre_07": "0,00065", "tope_kips": "222,41100",
    "R_kips": "67,27631", "uso_mensula": "1,34553",
    "e_col_riel": "1000,00000", "h_asiento": "6684,24000",
    "M_u_raiz": "478,81573", "R_fat_apoyo": "249,38373",
    "M_fat_raiz": "249,38373", "S_req": "1542080,00000", "sr_raiz": "161,71910",
    "uso_raiz_C": "0,75732", "uso_raiz_E": "1,20162", "uso_raiz_Ep": "1,69717",
    "sr_invariante": "161,71910", "pide_fatiga": "1,69717",
    "d_paso": "859,02171", "mas_que_riel": "1,02789",
    "sep_independiente": "0,95238", "L_sup": "3815,76000", "a_r": "0,36341",
    "Lp_base": "275,00000",
    "Ag_comp_base": "43314,00000", "xb_comp_base": "-348,66036",
    "Ix_comp_base": "14310239430", "Iy_comp_base": "171283622",
    "Ag_comp_paso": "41595,19539", "xb_comp_paso": "-374,02402",
    "multiplica_I": "3,06055", "I_sup_paso": "2944147775",
    "B_param": "4,86057",
    "w_07": "1,93938", "w_add": "1,27121", "w_col_10": "2,74863",
    "supera_05": "1,57065", "acero_marco": "57,72123",
    "Ez_carril_real": "173,23743",
    "q_placa": "63,97895", "Q_fuste": "8649790,00000",
    "R_filetes": "1871,01306", "uso_placa": "0,03419",
    "N_sup": "251,63775", "w_fuste_inf": "21,46035", "N_agrega": "325,01225",
    "razon_P1P2": "0,77424", "e_1": "374,02402", "e_2": "-625,97598",
    "M_1": "94,11856", "M_2": "-187,32947", "Mecc_10": "-93,21091",
    "cancela": "0,50242", "sobrestima": "2,00974",
    "frac_altura": "0,63659", "frac_axial": "0,45678",
    "comb_comprime": "179,33274", "comb_descarga": "38,45511",
    "C_V_reob": "0,52920", "N_con_peso": "576,65000", "sube_axial": "1,04675",
    "lam_md": "9,18267", "lam_ala_fuste": "9,06250",
    "uso_ala_fuste": "0,98691", "lam_ala_14": "10,35714",
    "uso_ala_14": "1,12790", "Ca_comp": "0,03724", "lam_alma_md": "80,61675",
    "lam_alma_07": "71,85714", "uso_alma_07": "0,89134",
    "lam_alma_fuste": "36,80000", "uso_alma_fuste": "0,45648",
    "metodos": "2,00000", "razon_fluencia": "0,03687", "tau_b": "1,00000",
    "N_nocional": "0,79293", "frac_lateral": "0,01311",
    "theta_red": "0,01120", "B_2": "1,01133", "uso_17": "0,59490",
    "K_L_070": "1,21272", "K_L_080": "1,22272", "K_L": "1,22014",
    "K_U": "0,83779", "L_ef_inf": "12811,47000", "L_ef_sup": "8796,79500",
    "r_x": "574,79013", "r_y_comp": "62,88452", "esb_plano_Lef": "22,28895",
    "esb_plano_directo": "11,62901", "esb_fuera": "106,29389",
    "k_esc_marco": "12616,09619", "T_esc": "0,25722", "techo_07": "1,89711",
    "cruza_techo": "1,18497", "R_deg": "4,71525", "cuanto_degrada": "1,06039",
    "kcap_nuevo": "3,30068", "contra_350": "0,94305", "Sa_nuevo": "1,15675",
    "baja_ord": "0,94557", "Q0_esc": "367,04838", "supera_techo": "1,21370",
    "f_deriva": "0,42062", "d_esc": "27,43646", "uso_63": "0,17420",
    "F_e_inf": "174,70814", "razon_FyFe": "1,97472", "F_cr_inf": "150,96148",
    "phiPn_inf": "5884,87099", "uso_axial_inf": "0,09361",
    "c_1": "873,66036", "c_2": "851,33964", "S_x1": "16379637,00000",
    "phiMn_inf": "5085,87729", "M_u_inf": "1128,76140",
    "uso_flex_inf": "0,22194", "interaccion": "0,26875",
    "multiplica_cap": "1,58611", "Iy_nudo": "99161439,00000",
    "ry_sup": "65,54142", "esb_sup_fuera": "58,21906",
    "ancho_base": "1725,00000",
    "mayor_07": "1,64286", "pos_centroide": "0,20212",
    "R_u_apoyo": "486,11752", "esb_atiesador": "9,16667",
    "lim_esb_at": "13,48322", "A_st": "3408,00000", "I_st": "11852352,00000",
    "r_st": "58,97290", "esb_st_col": "8,26651", "phiPn_st": "1052,90737",
    "uso_st_col": "0,46169", "A_pb": "2040,00000", "phiRn_pb": "950,13000",
    "uso_st_contacto": "0,51163", "phiRn_alma": "552,00000",
    "uso_alma_sin": "0,88065",
    "uso_tir_C": "0,36079", "uso_tir_E": "0,57246", "uso_tir_Ep": "0,80855",
    "uso_inf_C": "0,55441", "uso_inf_E": "0,87966", "uso_inf_Ep": "1,24243",
    "razon_alas": "1,53662",
    "T_u_tirante": "37,12000", "R_n_desliz": "48,13800",
    "uso_tirante": "0,38556", "R_n_corte": "107,67834",
    "cuesta_desliz": "2,23687",
    "short_ton": "8,89644", "cap_short_tons": "22,48090",
    "uso_tope_20": "1,12405", "cap_metricas": "20,39432",
    "sep_grapas": "762,00000", "espacios_grapas": "10,00000",
    "luz_junta": "1,58750", "veces_altura": "82,99843",
    "sep_J35_mm": "240,00000", "tope_12in_mm": "304,80000",
    "cual_gobierna": "0,78740",
})

if __name__ == "__main__":
    raise SystemExit(main(sys.argv, E))
