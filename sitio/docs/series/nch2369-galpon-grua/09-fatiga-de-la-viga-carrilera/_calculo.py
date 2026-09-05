"""Eslabón 09 — la fatiga de la viga carrilera: el ala que la fatiga castiga es
la única de la sección que no tiene vida infinita, y el tamaño del filete
alma-ala lo decide una vida útil que nadie fijó.

    python sitio/docs/series/nch2369-galpon-grua/09-fatiga-de-la-viga-carrilera/_calculo.py [salida]

Hereda del 01, del 03 y del 08. Transcrito del memo 09 de `Guias_Interactivas`,
que leyó las cláusulas del PDF (ver la tabla de referencias de `index.md`).

Cuatro cosas que este eslabón hace y conviene no perder de vista al leerlo:

* **NCh2369 no tiene fatiga**, y AIST tampoco da un número: da una dirección —la
  última edición de AISC— y una tabla que cruza clase de edificio con ciclos.
* **El conteo es por rueda, no por grúa**, y ese factor 2 mueve exactamente lo
  mismo que subir una clase de edificio: 1,26 en el admisible.
* **La fibra que la fatiga castiga es la del módulo menor**, o sea el ala
  inferior, que es la que el 08 hizo pequeña para poder hacer grande la superior.
  Es la única de la sección que queda **sobre el umbral de vida indefinida**.
* **El filete alma-ala lo dimensiona la fatiga y no la resistencia**, y lo que
  manda dentro de la fatiga no es el flujo de corte sino la **fuerza de contacto
  de la rueda** repartida en el largo efectivo que AIST define él mismo.

**Todos los pasos se redondean a cinco decimales**, que es lo que el memo imprime
y con lo que sustituye en el paso siguiente. Las 117 filas del `## Resumen` van
en `E.resumen()`.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from serie import Eslabon, main  # noqa: E402

E = Eslabon("nch2369-galpon-grua", orden=9, slug="fatiga-de-la-viga-carrilera",
            titulo="La fatiga de la viga carrilera",
            normas=["AISC 360-22", "AIST TR-13:2021", "NCh2369:2025"],
            carpeta=AQUI)


def r5(x: float) -> float:
    """Cinco decimales, con redondeo medio hacia arriba."""
    return math.floor(float(x) * 1e5 + 0.5) / 1e5


def ent(x: float) -> float:
    return float(math.floor(float(x) + 0.5))


# ------------------------------------------------------------ lo que entra
s_marco = E.entra("s_marco", de="01", paso="S1")
Qn_grua = E.entra("Qn_grua", de="01", paso="S3")
Wb_puente = E.entra("Wb_puente", de="03", paso="S2")
Wt_carro = E.entra("Wt_carro", de="03", paso="S2")
wb_ruedas = E.entra("wb_ruedas", de="03", paso="S2")
Rw_max = E.entra("Rw_max", de="03", paso="B2")
Rv_max = E.entra("Rv_max", de="03", paso="C1")
SS_carril = E.entra("SS_carril", de="03", paso="D3")
N_ciclos = E.entra("N_ciclos", de="03", paso="A1")
vida_grua = E.entra("vida_grua", de="03", paso="S4")
bfs_carril = E.entra("bfs_carril", de="08", paso="S2")
tfs_carril = E.entra("tfs_carril", de="08", paso="S2")
hw_carril = E.entra("hw_carril", de="08", paso="S2")
tw_carril = E.entra("tw_carril", de="08", paso="S2")
bfi_carril = E.entra("bfi_carril", de="08", paso="S2")
tfi_carril = E.entra("tfi_carril", de="08", paso="S2")
d_carril = E.entra("d_carril", de="08", paso="C1")
Ix_carril = E.entra("Ix_carril", de="08", paso="C2")
Sxc_carril = E.entra("Sxc_carril", de="08", paso="C2")
Sxt_carril = E.entra("Sxt_carril", de="08", paso="C2")
ybar_carril = E.entra("ybar_carril", de="08", paso="C2")
w_carril = E.entra("w_carril", de="08", paso="C4")
M_serv = E.entra("M_serv", de="08", paso="D1")
e_riel = E.entra("e_riel", de="08", paso="D3")
ev_carril = E.entra("ev_carril", de="08", paso="D3")
lef_carril = E.entra("lef_carril", de="08", paso="E6")
N_50 = E.entra("N_50", de="08", paso="B2")

# lo heredado, con los decimales que su eslabón imprimió
Rv_max_p, Rw_max_p = r5(Rv_max), r5(Rw_max)

# ------------------------------------------------------------ el caso
Fy = E.caso("Fy", 345.0, "MPa")
Fexx = E.caso("Fexx", 490.0, "MPa")          # E70, AISC §J2.4
phi_w = E.caso("phi_w", 0.75, "—")           # AISC §J2.4
cos45 = E.caso("cos45", 0.70711, "—")        # garganta de un filete
a_filete = E.caso("a_filete", 6.0, "mm")     # el filete adoptado (D6)
a_min_J24 = E.caso("a_min_J24", 5.0, "mm")   # AISC Tabla J2.4, sobre 8 mm
frac_exc_08 = E.caso("frac_exc_08", 0.35315, "—")   # del 08 · D3
uso_inf_dec = E.caso("uso_inf_dec", 0.39695, "—")   # C4, para la razón de C5

# Las curvas S-N de AISC, Ap. 3. `Cf` en las unidades de la Ec. A-3-1M y el
# umbral en MPa; las dos columnas de la Tabla A-3.1.
Cf_B = E.caso("Cf_B", 12.0, "—")
Cf_Bp = E.caso("Cf_Bp", 6.1, "—")
Cf_C = E.caso("Cf_C", 4.4, "—")
Cf_E = E.caso("Cf_E", 1.1, "—")
Cf_Ep = E.caso("Cf_Ep", 0.39, "—")
Cf_F = E.caso("Cf_F", 1.5, "—")
k_SN = E.caso("k_SN", 6900.0, "MPa")         # Ec. A-3-1M
k_SN_F = E.caso("k_SN_F", 690.0, "MPa")      # Ec. A-3-2M
exp_SN = E.caso("exp_SN", 0.333, "—")
exp_SN_F = E.caso("exp_SN_F", 0.167, "—")
thr_A = E.caso("thr_A", 170.0, "MPa")        # umbral de la categoría A
thr_B = E.caso("thr_B", 110.0, "MPa")
thr_Bp = E.caso("thr_Bp", 83.0, "MPa")
thr_C = E.caso("thr_C", 69.0, "MPa")
thr_E = E.caso("thr_E", 31.0, "MPa")
thr_F = E.caso("thr_F", 55.0, "MPa")     # la garganta del filete, caso 8.2
# Una década del eje del gráfico S-N. No es un resultado: es la escala, y se
# declara porque toda cifra dibujada tiene que existir entre los valores.
eje_100 = E.caso("eje_100", 100.0, "MPa")

# Constantes de cláusula y del régimen declarado.
ciclos_techoC = E.caso("ciclos_techoC", 100000.0, "ciclos")
ciclos_pisoC = E.caso("ciclos_pisoC", 20000.0, "ciclos")
vida_aist = E.caso("vida_aist", 50.0, "años")
dias_ano = E.caso("dias_ano", 365.0, "días")
ciclos_rueda = E.caso("ciclos_rueda", 2.0, "—")   # AIST §5.8.1, dos ruedas
turnos = E.caso("turnos", 3, "—")                 # del 03, el régimen declarado
levantes = E.caso("levantes", 4, "—")
dias_op = E.caso("dias_op", 250, "días")
c_pico = E.caso("c_pico", 0.66, "—")              # AISC Ap. §3.1
destalone = E.caso("destalone", 6.0, "mm")        # E4, el destalonado del atiesador
k_corte_at = E.caso("k_corte_at", 6.0, "—")       # E4, «4 a 6 veces el alma»
f_D = E.caso("f_D", 1.2, "—")
f_L = E.caso("f_L", 1.6, "—")


def FSR(Cf: float, n: float) -> float:
    """Ec. A-3-1M: el rango admisible de las categorías A a E′."""
    return k_SN * (Cf / n) ** exp_SN


def FSR_F(n: float) -> float:
    """Ec. A-3-2M: la categoría F, con otro exponente y otra constante."""
    return k_SN_F * (Cf_F / n) ** exp_SN_F


# ========== A · la fatiga que NCh2369 no tiene, y con cuántos ciclos ======
apl_diarias = E.paso("A1", "apl_diarias",
                     r5(ciclos_techoC / (vida_aist * dias_ano)), "—")
regimen_dia = E.paso("A1", "regimen_dia",
                     r5(turnos * levantes * dias_op / dias_ano), "—")
veces_base = E.paso("A1", "veces_base", r5(regimen_dia / apl_diarias), "—")
frac_techoC = E.paso("A2", "frac_techoC", r5(N_ciclos / ciclos_techoC), "—")
veces_umbral = E.paso("A2", "veces_umbral", r5(N_ciclos / ciclos_pisoC), "—")
Nfat_carril = E.paso("A3", "Nfat_carril", r5(ciclos_rueda * N_ciclos), "ciclos")
razon_vidas = E.paso("A3", "razon_vidas", r5(vida_aist / vida_grua), "—")
dos_150k = E.paso("A3", "dos_150k", r5(Nfat_carril / N_50), "—")

kappa = E.paso("A4", "kappa",
               r5((2 * Rw_max_p - Wb_puente / 2.0) / (Qn_grua + Wt_carro)), "—")
C_ds = E.paso("A4", "C_ds", r5(Wb_puente / 4.0 + Wt_carro * kappa / 2.0), "kN")
C_vs = E.paso("A4", "C_vs", r5(Qn_grua * kappa / 2.0), "kN")
P_fat = E.paso("A4", "P_fat", r5(C_ds + C_vs), "kN")
cierre_03 = E.paso("A4", "cierre_03", r5(P_fat - Rw_max_p), "kN")
H_fat = E.paso("A4", "H_fat", r5(SS_carril / (2 * 2)), "kN")
menos_mayorada = E.paso("A4", "menos_mayorada", r5(f_L * Rv_max_p / P_fat), "—")
menos_impacto = E.paso("A4", "menos_impacto", r5(Rv_max_p / P_fat), "—")

# ============ B · el rango de tensiones, que las alas no reparten =========
x1_mm = E.paso("B1", "x1_mm",
               r5(s_marco * 1e3 / 2.0 - wb_ruedas * 1e3 / 4.0), "mm")
coef_077 = E.paso("B1", "coef_077",
                  r5((2 * s_marco - wb_ruedas) / (2 * s_marco)), "—")
coef_M = E.paso("B1", "coef_M", r5(coef_077 * x1_mm * 1e-3), "m")
M_fat = E.paso("B1", "M_fat", r5(P_fat * coef_M), "kN·m")
cierre_08 = E.paso("B1", "cierre_08", r5(M_fat - M_serv), "kN·m")

sr_inf_carril = E.paso("B2", "sr_inf_carril", r5(M_fat * 1e6 / Sxt_carril), "MPa")
sr_sup_carril = E.paso("B2", "sr_sup_carril", r5(M_fat * 1e6 / Sxc_carril), "MPa")
razon_modulos = E.paso("B2", "razon_modulos", r5(Sxc_carril / Sxt_carril), "—")
y_inf = E.paso("B2", "y_inf", r5(d_carril - ybar_carril), "mm")

h_o = E.paso("B3", "h_o",
             r5(d_carril - tfs_carril / 2.0 - tfi_carril / 2.0), "mm")
T_empuje_fat = E.paso("B3", "T_empuje_fat", r5(H_fat * ev_carril), "kN·mm")
T_exc_fat = E.paso("B3", "T_exc_fat", r5(P_fat * e_riel), "kN·mm")
T_fat = E.paso("B3", "T_fat", r5(T_empuje_fat + T_exc_fat), "kN·mm")
frac_exc_fat = E.paso("B3", "frac_exc_fat", r5(T_exc_fat / T_fat), "—")
sube_frac = E.paso("B3", "sube_frac", r5(frac_exc_fat / frac_exc_08), "—")
F_par_fat = E.paso("B3", "F_par_fat", r5(T_fat / h_o), "kN")
H_ala_fat = E.paso("B3", "H_ala_fat", r5(H_fat + F_par_fat), "kN")
amplif_fat = E.paso("B3", "amplif_fat", r5(H_ala_fat / H_fat), "—")
S_y = E.paso("B3", "S_y", ent(tfs_carril * bfs_carril ** 2 / 6.0), "mm3")
M_uy_fat = E.paso("B3", "M_uy_fat", r5(coef_M * H_ala_fat), "kN·m")
sigma_y_fat = E.paso("B3", "sigma_y_fat", r5(M_uy_fat * 1e6 / S_y), "MPa")
sr_punta = E.paso("B3", "sr_punta", r5(sr_sup_carril + sigma_y_fat), "MPa")

M_pp = E.paso("B4", "M_pp", r5(w_carril * s_marco ** 2 / 8.0), "kN·m")
sigma_max = E.paso("B4", "sigma_max",
                   r5((M_fat + M_pp) * 1e6 / Sxt_carril), "MPa")
tope_pico = E.paso("B4", "tope_pico", r5(c_pico * Fy), "MPa")
uso_pico = E.paso("B4", "uso_pico", r5(sigma_max / tope_pico), "—")

# ========= C · las categorías, y el ala que no tiene vida infinita ========
cuesta_umbral = E.paso("C1", "cuesta_umbral", r5(thr_B / thr_Bp), "—")
cuesta_adm = E.paso("C1", "cuesta_adm", r5((Cf_B / Cf_Bp) ** exp_SN), "—")
uso_umbral_inf = E.paso("C2", "uso_umbral_inf", r5(sr_inf_carril / thr_B), "—")
n_agota_B = E.paso("C2", "n_agota_B",
                   ent(Cf_B / (sr_inf_carril / k_SN) ** (1.0 / exp_SN)), "ciclos")
veces_conteo = E.paso("C2", "veces_conteo", r5(n_agota_B / Nfat_carril), "—")
uso_umbral_sup = E.paso("C3", "uso_umbral_sup", r5(sr_sup_carril / thr_B), "—")
uso_umbral_punta = E.paso("C3", "uso_umbral_punta", r5(sr_punta / thr_A), "—")
FSR_B150 = E.paso("C4", "FSR_B150", r5(FSR(Cf_B, Nfat_carril)), "MPa")
uso_inf = E.paso("C4", "uso_inf", r5(sr_inf_carril / FSR_B150), "—")
uso_sup = E.paso("C4", "uso_sup", r5(sr_sup_carril / FSR_B150), "—")
# El conteo de la clase B: el doble del de la C, por el mismo factor 2 con que
# el conteo por rueda dobla el de grúa.
n300 = E.paso("C5", "n300", r5(ciclos_rueda * N_50), "ciclos")
FSR_B300 = E.paso("C5", "FSR_B300", r5(FSR(Cf_B, n300)), "MPa")
uso_inf_B = E.paso("C5", "uso_inf_B", r5(sr_inf_carril / FSR_B300), "—")
factor_sens = E.paso("C5", "factor_sens", r5(2.0 ** exp_SN), "—")
razon_usos = E.paso("C5", "razon_usos", r5(uso_inf_B / uso_inf_dec), "—")

# ============ D · la soldadura alma-ala superior, dimensionada ============
a_equiv = E.paso("D1", "a_equiv", r5(tw_carril / (2 * cos45)), "mm")
Q_s = E.paso("D2", "Q_s",
             ent(bfs_carril * tfs_carril * (ybar_carril - tfs_carril / 2.0)), "mm3")
c_R = E.paso("D2", "c_R", r5(1 + (s_marco - wb_ruedas) / s_marco), "—")
V_fat = E.paso("D2", "V_fat", r5(P_fat * c_R), "kN")
q_s = E.paso("D2", "q_s", r5(V_fat * 1e3 * Q_s / Ix_carril), "N/mm")
Q_i = E.paso("D2", "Q_i",
             ent(bfi_carril * tfi_carril * (y_inf - tfi_carril / 2.0)), "mm3")
q_i = E.paso("D2", "q_i", r5(V_fat * 1e3 * Q_i / Ix_carril), "N/mm")
menos_flujo = E.paso("D2", "menos_flujo", r5(q_i / q_s), "—")
w_loc = E.paso("D3", "w_loc", r5(P_fat * 1e3 / lef_carril), "N/mm")
supera_contacto = E.paso("D3", "supera_contacto", r5(w_loc / q_s), "—")
q_t = E.paso("D4", "q_t", r5(F_par_fat * 1e3 / lef_carril), "N/mm")
R_result = E.paso("D5", "R_result",
                  r5(math.sqrt(q_s ** 2 + w_loc ** 2 + q_t ** 2)), "N/mm")
R_soldadura = E.paso("D5", "R_soldadura", r5(R_result / 2.0), "N/mm")
frac_par = E.paso("D5", "frac_par", r5(q_t / R_result), "—")
ve_inferior = E.paso("D5", "ve_inferior", r5(q_i / R_result), "—")

FSR_F150 = E.paso("D6", "FSR_F150", r5(FSR_F(Nfat_carril)), "MPa")
FSR_F300 = E.paso("D6", "FSR_F300", r5(FSR_F(n300)), "MPa")
a_fat_C = E.paso("D6", "a_fat_C", r5(R_soldadura / (cos45 * FSR_F150)), "mm")
a_fat_B = E.paso("D6", "a_fat_B", r5(R_soldadura / (cos45 * FSR_F300)), "mm")
tau_SR = E.paso("D6", "tau_SR", r5(R_soldadura / (cos45 * a_filete)), "MPa")
uso_garg_C = E.paso("D6", "uso_garg_C", r5(tau_SR / FSR_F150), "—")
uso_garg_B = E.paso("D6", "uso_garg_B", r5(tau_SR / FSR_F300), "—")
tau_SR_5 = E.paso("D6", "tau_SR_5", r5(R_soldadura / (cos45 * a_min_J24)), "MPa")
uso_min_J24 = E.paso("D6", "uso_min_J24", r5(tau_SR_5 / FSR_F300), "—")

R_u = E.paso("D7", "R_u", r5(Rv_max_p * c_R), "kN")
cierre_08_R = E.paso("D7", "cierre_08_R", r5(R_u - 299.25983), "kN")
# La rueda mayorada, con los decimales con que el 08 la imprimió: es lo que
# el memo sustituye en las tres expresiones que siguen.
P_nch_p = E.paso("D7", "P_nch_p", r5(f_L * Rv_max_p), "kN")
V_u = E.paso("D7", "V_u",
             r5(f_L * R_u + f_D * w_carril * s_marco / 2.0), "kN")
q_u = E.paso("D7", "q_u", r5(V_u * 1e3 * Q_s / Ix_carril), "N/mm")
w_loc_u = E.paso("D7", "w_loc_u", r5(P_nch_p * 1e3 / lef_carril), "N/mm")
T_u = E.paso("D7", "T_u",
             r5(f_L * SS_carril / 2.0 * ev_carril + P_nch_p * e_riel), "kN·mm")
F_par_u = E.paso("D7", "F_par_u", r5(T_u / h_o), "kN")
q_t_u = E.paso("D7", "q_t_u", r5(F_par_u * 1e3 / lef_carril), "N/mm")
R_u_result = E.paso("D7", "R_u_result",
                    r5(math.sqrt(q_u ** 2 + w_loc_u ** 2 + q_t_u ** 2) / 2.0), "N/mm")
phi_Fnw = E.paso("D7", "phi_Fnw", r5(phi_w * 0.60 * Fexx * cos45), "N/mm2")
a_resistencia = E.paso("D7", "a_resistencia", r5(R_u_result / phi_Fnw), "mm")
uso_estatico = E.paso("D7", "uso_estatico",
                      r5(R_u_result / (phi_Fnw * a_filete)), "—")

# ====== E · los detalles que la cláusula prohíbe, y su aritmética =========
FSR_catE = E.paso("E1", "FSR_catE", r5(FSR(Cf_E, Nfat_carril)), "MPa")
uso_acc_C = E.paso("E1", "uso_acc_C", r5(sr_inf_carril / FSR_catE), "—")
FSR_E300 = E.paso("E1", "FSR_E300", r5(FSR(Cf_E, n300)), "MPa")
uso_acc_B = E.paso("E1", "uso_acc_B", r5(sr_inf_carril / FSR_E300), "—")
FSR_catEp = E.paso("E2", "FSR_catEp", r5(FSR(Cf_Ep, Nfat_carril)), "MPa")
uso_acc_Ep = E.paso("E2", "uso_acc_Ep", r5(sr_inf_carril / FSR_catEp), "—")
n_cond = E.paso("E3", "n_cond", r5(1 + 0), "—")
costo_intermitente = E.paso("E3", "costo_intermitente",
                            r5(FSR_B150 / FSR_catE), "—")

FSR_catC = E.paso("E4", "FSR_catC", r5(FSR(Cf_C, Nfat_carril)), "MPa")
a_alma_ala = E.paso("D6", "a_alma_ala", a_filete, "mm")
y_st = E.paso("E4", "y_st",
              r5(y_inf - tfi_carril - destalone - k_corte_at * tw_carril), "mm")
sigma_st = E.paso("E4", "sigma_st", r5(sr_inf_carril * y_st / y_inf), "MPa")
uso_atiesador = E.paso("E4", "uso_atiesador", r5(sigma_st / FSR_catC), "—")
uso_si_llega = E.paso("E4", "uso_si_llega", r5(sr_inf_carril / FSR_catC), "—")
rebaja_cortar = E.paso("E4", "rebaja_cortar", r5(sigma_st / sr_inf_carril), "—")
uso_umbral_pie = E.paso("E4", "uso_umbral_pie", r5(sigma_st / thr_C), "—")
n_agota_C = E.paso("E4", "n_agota_C",
                   ent(Cf_C / (sigma_st / k_SN) ** (1.0 / exp_SN)), "ciclos")
veces_conteo_C = E.paso("E4", "veces_conteo_C", r5(n_agota_C / Nfat_carril), "—")

# ============= F · lo que la fatiga le devuelve a la serie ================
FSR_B75 = E.paso("F1", "FSR_B75", r5(FSR(Cf_B, N_ciclos)), "MPa")
uso_sin_rueda = E.paso("F1", "uso_sin_rueda", r5(sr_inf_carril / FSR_B75), "—")
razon_conteos = E.paso("F1", "razon_conteos", r5(uso_inf / uso_sin_rueda), "—")
FSR_F75 = E.paso("F1", "FSR_F75", r5(FSR_F(N_ciclos)), "MPa")
a_sin_rueda = E.paso("F1", "a_sin_rueda",
                     r5(R_soldadura / (cos45 * FSR_F75)), "mm")
FSR_Bp150 = E.paso("F2", "FSR_Bp150", r5(FSR(Cf_Bp, Nfat_carril)), "MPa")
uso_respaldo = E.paso("F2", "uso_respaldo", r5(sr_inf_carril / FSR_Bp150), "—")
parecido_B = E.paso("F2", "parecido_B", r5(uso_respaldo / uso_inf_B), "—")

# ------------------------------------------------------------ Sale
E.sale("Nfat_carril", Nfat_carril, "ciclos", paso="A3", heredan=["10"])
E.sale("sr_sup_carril", sr_sup_carril, "MPa", paso="B2", heredan=["10"])
E.sale("sr_inf_carril", sr_inf_carril, "MPa", paso="B2", heredan=["10"])
E.sale("a_alma_ala", a_alma_ala, "mm", paso="D6", heredan=["10"])
E.sale("FSR_catC", FSR_catC, "MPa", paso="E4", heredan=["10"])
E.sale("FSR_catE", FSR_catE, "MPa", paso="E1", heredan=["10"])
E.sale("FSR_catEp", FSR_catEp, "MPa", paso="E2", heredan=["10"])

# lo que el memo 09 de Guias_Interactivas imprimió en su `## Sale`
E.publicado({
    "Nfat_carril": "150000", "sr_sup_carril": "77,04436",
    "sr_inf_carril": "118,38827", "a_alma_ala": "6", "FSR_catC": "213,54059",
    "FSR_catE": "134,58432", "FSR_catEp": "95,28734",
})

# y las 117 filas de su `## Resumen`
E.resumen({
    "apl_diarias": "5,47945", "regimen_dia": "8,21918", "veces_base": "1,50000",
    "frac_techoC": "0,75000", "veces_umbral": "3,75000",
    "Nfat_carril": "150000,00000", "razon_vidas": "2,00000",
    "dos_150k": "1,00000",
    "kappa": "0,94783", "C_ds": "66,45660", "C_vs": "94,78300",
    "P_fat": "161,23960", "cierre_03": "0,00047", "H_fat": "7,50000",
    "menos_mayorada": "1,91999", "menos_impacto": "1,20000",
    "x1_mm": "2900,00000", "coef_077": "0,77333", "coef_M": "2,24266",
    "M_fat": "361,60560", "cierre_08": "0,00105",
    "sr_inf_carril": "118,38827", "sr_sup_carril": "77,04436",
    "razon_modulos": "1,53662", "y_inf": "414,35032", "h_o": "667,00000",
    "T_fat": "2030,63760", "T_empuje_fat": "1063,20000",
    "T_exc_fat": "967,43760", "frac_exc_fat": "0,47642",
    "sube_frac": "1,34906", "F_par_fat": "3,04443", "H_ala_fat": "10,54443",
    "amplif_fat": "1,40592", "S_y": "408333,00000", "M_uy_fat": "23,64757",
    "sigma_y_fat": "57,91246", "sr_punta": "134,95682",
    "M_pp": "11,40905", "sigma_max": "122,12355", "tope_pico": "227,70000",
    "uso_pico": "0,53634",
    "cuesta_umbral": "1,32530", "cuesta_adm": "1,25272",
    "uso_umbral_inf": "1,07626", "n_agota_B": "2404941,00000",
    "veces_conteo": "16,03294", "uso_umbral_sup": "0,70040",
    "uso_umbral_punta": "0,79386", "FSR_B150": "298,24835",
    "uso_inf": "0,39695", "uso_sup": "0,25832", "FSR_B300": "236,77458",
    "uso_inf_B": "0,50000", "factor_sens": "1,25963", "razon_usos": "1,25960",
    "a_equiv": "5,65683", "Q_s": "1817548,00000", "c_R": "1,54667",
    "V_fat": "249,38445", "q_s": "358,14678", "Q_i": "1425726,00000",
    "q_i": "280,93848", "menos_flujo": "0,78442", "w_loc": "531,23221",
    "supera_contacto": "1,48328", "q_t": "10,03041", "R_result": "640,76313",
    "R_soldadura": "320,38157", "frac_par": "0,01565",
    "ve_inferior": "0,43844", "FSR_F150": "100,89023", "FSR_F300": "89,86221",
    "a_fat_C": "4,49088", "a_fat_B": "5,04201", "tau_SR": "75,51432",
    "uso_garg_C": "0,74848", "uso_garg_B": "0,84033", "tau_SR_5": "90,61718",
    "uso_min_J24": "1,00840",
    "R_u": "299,26048", "cierre_08_R": "0,00065", "V_u": "486,11856",
    "q_u": "698,12612", "w_loc_u": "1019,96290", "T_u": "5259,71484",
    "F_par_u": "7,88563", "q_t_u": "25,98059", "R_u_result": "618,13821",
    "phi_Fnw": "155,91775", "a_resistencia": "3,96451",
    "uso_estatico": "0,66075",
    "FSR_catE": "134,58432", "uso_acc_C": "0,87966", "FSR_E300": "106,84433",
    "uso_acc_B": "1,10804", "FSR_catEp": "95,28734", "uso_acc_Ep": "1,24243",
    "n_cond": "1,00000", "costo_intermitente": "2,21607",
    "FSR_catC": "213,54059", "y_st": "346,35032", "sigma_st": "98,95929",
    "uso_atiesador": "0,46342", "uso_si_llega": "0,55441",
    "rebaja_cortar": "0,83589", "uso_umbral_pie": "1,43419",
    "n_agota_C": "1510657,00000", "veces_conteo_C": "10,07105",
    "FSR_B75": "375,68257", "uso_sin_rueda": "0,31513",
    "razon_conteos": "1,25964", "FSR_F75": "113,27162",
    "a_sin_rueda": "3,99999", "FSR_Bp150": "238,08144",
    "uso_respaldo": "0,49726", "parecido_B": "0,99452",
})

if __name__ == "__main__":
    raise SystemExit(main(sys.argv, E))
