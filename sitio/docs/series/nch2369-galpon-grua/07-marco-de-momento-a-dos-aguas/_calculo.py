"""Eslabón 07 — el marco de momento a dos aguas: lo que lo dimensiona no es
ninguna de las dos derivas sino el período que el 04 declaró, y rigidizar no
cuesta nada porque §5.13 ya recortó.

    python sitio/docs/series/nch2369-galpon-grua/07-marco-de-momento-a-dos-aguas/_calculo.py [salida]

Hereda de los seis eslabones anteriores —los 43 símbolos que le prometieron— y es
el primero que consume la cadena entera. Transcrito del memo 07 de
`Guias_Interactivas`, que leyó las cláusulas del PDF (ver la tabla de referencias
de `index.md`).

Cuatro cosas que este eslabón hace y conviene no perder de vista al leerlo:

* **El marco no se resuelve acá.** El memo declara en su S1 un modelo plano de
  rigidez directa con 42 segmentos prismáticos por miembro y bases empotradas, y
  dice explícitamente que «este memo describe y no ejecuta». Las dos rigideces
  laterales, la rigidez vertical y **todos los momentos de barra** son valores
  declarados, no pasos. Acá entran como `caso()` en el bloque «el campo
  declarado», con el paso del memo que los usa. El sitio los contrasta contra el
  modelo 3D en `index.md`, que es cosa distinta de reproducirlos.
* **El criterio que dimensiona es el período**, y ningún eslabón lo había
  presentado como un requisito de rigidez. La deriva de servicio de la grúa, que
  el 06 llamó «la que manda» por ser seis veces más estricta que §6.3, queda
  usada en 0,164 contra 0,414 del sísmico.
* **Rigidizar no cuesta fuerza** porque el techo de la Ec. (13) se arma sin el
  período adentro: el corte del análisis sube y el de diseño no se mueve.
* **La deriva y la apertura de trocha son dos mitades del mismo desplazamiento.**
  La antisimétrica es deriva y la simétrica es el marco abriéndose; tienen
  límites distintos y en cláusulas distintas de AIST §5.3.

**Todos los pasos se redondean a cinco decimales**, que es lo que el memo imprime
y con lo que sustituye en el paso siguiente; su modelo independiente hacía lo
mismo (`r5` en su `.check.js`). Las cifras que entran de otros eslabones se
consumen también con los decimales que ese eslabón publicó: `_p` marca esas
variables.

Las 137 filas del `## Resumen` del memo van en `E.resumen()`, que las valida
contra el paso que las produce con la misma regla que `E.publicado()` aplica a
las 24 salidas. Sin eso, 113 cifras que esta página imprime no tendrían oráculo.
Tres filas quedan fuera y están en `## Límites`: el memo imprimió una cifra y
sustituyó otra, una unidad más en el último dígito.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from serie import Eslabon, main  # noqa: E402

E = Eslabon("nch2369-galpon-grua", orden=7, slug="marco-de-momento-a-dos-aguas",
            titulo="El marco de momento a dos aguas",
            normas=["NCh2369:2025", "AISC 341-22", "AISC 360-22", "AIST TR-13:2021",
                    "NCh431:2010"],
            carpeta=AQUI)


def r5(x: float) -> float:
    """Cinco decimales, con redondeo **medio hacia arriba**: el `Math.round` del
    modelo independiente del memo, no el medio-al-par de `round()` de Python."""
    return math.floor(float(x) * 1e5 + 0.5) / 1e5


def r2(x: float) -> float:
    """Dos decimales: la precisión con que el memo imprime las longitudes en mm."""
    return math.floor(float(x) * 1e2 + 0.5) / 1e2


# ------------------------------------------------------------ lo que entra
I = E.entra("I", de="01", paso="A1")
L_luz = E.entra("L_luz", de="01", paso="S1")
s_marco = E.entra("s_marco", de="01", paso="S1")
h_libre = E.entra("h_libre", de="01", paso="S1")
h_riel = E.entra("h_riel", de="01", paso="S3")
p_s = E.entra("p_s", de="02", paso="C4")
p_bar = E.entra("p_bar", de="02", paso="D5")
p_pico = E.entra("p_pico", de="02", paso="D5")
L_ac = E.entra("L_ac", de="02", paso="D3")
theta_techo = E.entra("theta_techo", de="02", paso="C1")
S_pend = E.entra("S_pend", de="02", paso="C2")
wb_ruedas = E.entra("wb_ruedas", de="03", paso="S2")
Rv_max = E.entra("Rv_max", de="03", paso="C1")
SS_total = E.entra("SS_total", de="03", paso="D1")
SS_carril = E.entra("SS_carril", de="03", paso="D3")
ArS = E.entra("ArS", de="04", paso="A3")
r_s = E.entra("r_s", de="04", paso="A2")
T_0 = E.entra("T_0", de="04", paso="A2")
p_suelo = E.entra("p_suelo", de="04", paso="A2")
q_s = E.entra("q_s", de="04", paso="A2")
f_xi = E.entra("f_xi", de="04", paso="B1")
T_pico = E.entra("T_pico", de="04", paso="B2")
Sa_pico = E.entra("Sa_pico", de="04", paso="B2")
Cr_T1 = E.entra("Cr_T1", de="04", paso="C2")
T_star_Y = E.entra("T_star_Y", de="04", paso="S2")
R_star_Y = E.entra("R_star_Y", de="04", paso="C5")
Sa_ref_Y = E.entra("Sa_ref_Y", de="04", paso="C5")
P_sismico = E.entra("P_sismico", de="05", paso="C4")
Q0_Y = E.entra("Q0_Y", de="05", paso="D5")
R1_Y = E.entra("R1_Y", de="05", paso="F1")
kcap_Y = E.entra("kcap_Y", de="05", paso="F2")
k_prel_Y = E.entra("k_prel_Y", de="05", paso="F3")
k_req_Y = E.entra("k_req_Y", de="05", paso="F3")
C_V = E.entra("C_V", de="06", paso="B1")
E_z = E.entra("E_z", de="06", paso="B2")
Ez_techo = E.entra("Ez_techo", de="06", paso="B3")
D_grav = E.entra("D_grav", de="06", paso="C1")
S_comb = E.entra("S_comb", de="06", paso="D1")
Pu_nieve = E.entra("Pu_nieve", de="06", paso="D2")
d_lim = E.entra("d_lim", de="06", paso="E1")
d_Y = E.entra("d_Y", de="06", paso="E2")
dlim_grua = E.entra("dlim_grua", de="06", paso="E5")
f_PDelta_Y = E.entra("f_PDelta_Y", de="06", paso="F1")

# lo heredado, con los decimales que su eslabón imprimió: es lo que el memo sustituyó
Sa_pico_p, Sa_ref_Y_p, f_xi_p = r5(Sa_pico), r5(Sa_ref_Y), r5(f_xi)
k_req_p, Q0_p = r5(k_req_Y), r5(Q0_Y)
p_pico_p, L_ac_p = r5(p_pico), r5(L_ac)

# ------------------------------------------------------------ el caso
# Material: ASTM A572 Gr. 50 en plancha (S5).
Fy = E.caso("Fy", 345.0, "MPa")
Ry = E.caso("Ry", 1.10, "—")
E_ac = E.caso("E_ac", 200000.0, "MPa")
phi_b = E.caso("phi_b", 0.90, "—")
g_grav = E.caso("g_grav", 9.81, "m/s2")
n_marcos = E.caso("n_marcos", 5, "—")
n_columnas = E.caso("n_columnas", 10, "—")
rho_acero = E.caso("rho_acero", 7.85, "t/m3")

# Secciones adoptadas (S2), en mm.
d_col_base = E.caso("d_col_base", 1050.0, "mm")
d_col_nudo = E.caso("d_col_nudo", 750.0, "mm")
bf_col = E.caso("bf_col", 300.0, "mm")
tf_col = E.caso("tf_col", 22.0, "mm")
tw_col = E.caso("tw_col", 14.0, "mm")
tw_col_tip = E.caso("tw_col_tip", 12.0, "mm")     # el que la tipología usaría
d_raf_nudo = E.caso("d_raf_nudo", 750.0, "mm")
d_raf_cumb = E.caso("d_raf_cumb", 425.0, "mm")
bf_raf = E.caso("bf_raf", 250.0, "mm")
tf_raf = E.caso("tf_raf", 20.0, "mm")
tw_raf = E.caso("tw_raf", 12.0, "mm")
tw_raf_tip = E.caso("tw_raf_tip", 8.0, "mm")      # el que la tipología usaría

# Datos de otros eslabones que su productor no prometió a éste, con su origen.
g_techo = E.caso("g_techo", 0.37278, "kN/m2")     # del 05 · A3
w_columna = E.caso("w_columna", 1.75, "kN/m")     # del 05 · S1
A_planta = E.caso("A_planta", 750.0, "m2")        # del 05 · A2
T_fin_ventana = E.caso("T_fin_ventana", 0.21632, "s")   # del 06 · B6
xi_V = E.caso("xi_V", 0.03, "—")                  # §5.4, fijo para la vertical
xi_ref = E.caso("xi_ref", 0.05, "—")              # §5.4.2
R_V = E.caso("R_V", 2.00, "—")                    # §5.4, fijo para la vertical
cv_vert = E.caso("cv_vert", 0.70, "—")            # §5.7.1, la fracción vertical
f_T_vert = E.caso("f_T_vert", 1.7, "—")           # §5.7.1, el 1,7 T del vertical

# Constantes de cláusula.
psf = E.caso("psf", 0.0478803, "kN/m2")           # 1 psf, AIST §5.3
psf_umbral = E.caso("psf_umbral", 30.0, "psf")    # AIST §5.3, el umbral de la rebaja
trocha_lim = E.caso("trocha_lim", 25.40, "mm")    # AIST §5.3, +1 in
c_ala = E.caso("c_ala", 0.40, "—")                # Tabla 9, ala de I/H soldado
c_alma = E.caso("c_alma", 3.96, "—")              # Tabla 9, alma en flexo-compresión
c_alma_Ca = E.caso("c_alma_Ca", 3.04, "—")        # Tabla 9, el coeficiente de C_a
c_Lb = E.caso("c_Lb", 0.19, "—")                  # §8.7.7
c_Pbr = E.caso("c_Pbr", 0.06, "—")                # §8.7.7
c_Pbr_aisc = E.caso("c_Pbr_aisc", 0.02, "—")      # AISC 341 §D1.2a
c_scwb = E.caso("c_scwb", 1.2, "—")               # §8.7.4
c_exc_aisc = E.caso("c_exc_aisc", 0.30, "—")      # AISC 341 §E3.4a
n_esp_agua = E.caso("n_esp_agua", 3, "—")         # E6, los espacios adoptados
reb_50 = E.caso("reb_50", 0.50, "—")              # AIST §5.3, bajo 30 psf
reb_25 = E.caso("reb_25", 0.75, "—")              # AIST §5.3, sobre 30 psf
phi_v = E.caso("phi_v", 0.90, "—")                # §G2
c_corte = E.caso("c_corte", 0.60, "—")            # §G2, 0,6 Fy

# ------------------------------------------------- el campo declarado (S1)
# Los resultados del modelo plano que el memo describe y no ejecuta. Van como
# datos, no como pasos: el memo es explícito en que no los produce.
k_Y = E.caso("k_Y", 5612.11747, "kN/m")                 # B4
k_riel = E.caso("k_riel", 15057.33721, "kN/m")          # B4
k_riel_inf = E.caso("k_riel_inf", 51522.74517, "kN/m")  # C3, diafragma rígido
Mbase_u = E.caso("Mbase_u", 1035.55049, "kN·m")         # B2, F2
M_nudo_bal = E.caso("M_nudo_bal", 914.39164, "kN·m")    # D2, F2
M_nudo_des = E.caso("M_nudo_des", 866.94355, "kN·m")    # D2
M_cumb = E.caso("M_cumb", 225.29112, "kN·m")            # F2
razon_sway = E.caso("razon_sway", 2.81628, "—")         # B2
y_infl = E.caso("y_infl", 7.74863, "m")                 # B2
flecha_cumb = E.caso("flecha_cumb", 18.14242, "mm")     # F1
trocha_D = E.caso("trocha_D", 6.42686, "mm")            # C7
trocha_S = E.caso("trocha_S", 14.54407, "mm")           # C7
d_riel_des = E.caso("d_riel_des", 1.70543, "mm")        # D3
d_alero_des = E.caso("d_alero_des", 3.62141, "mm")      # D3
N_grav = E.caso("N_grav", 251.63775, "kN")              # E3, axial del nudo
N_raf = E.caso("N_raf", 218.03265, "kN")                # E2, axial del rafter


# --------------------------------------------- la Ec. (3), sin el `A_r S`
def forma_H(T: float) -> float:
    """La forma de la Ec. (3) en función del período."""
    u = T / T_0
    return (1 + r_s * u ** p_suelo) / (1 + u ** q_s)


def i_soldada(d: float, bf: float, tf: float, tw: float) -> tuple[float, float, float]:
    """Doble T soldada: `(I_fuerte, Z_fuerte, A)` en mm, mm⁴, mm³, mm²."""
    h = d - 2 * tf
    I_ = (bf * d ** 3 - (bf - tw) * h ** 3) / 12.0
    Z_ = bf * tf * (d - tf) + tw * h ** 2 / 4.0
    A_ = 2 * bf * tf + h * tw
    return I_, Z_, A_


# ================== A · las dos obligaciones que hereda ==================
alpha = E.paso("A1", "alpha", r5(k_req_p / k_prel_Y), "—")
frac_pico_dec = E.paso("A2", "frac_pico_dec", r5(Sa_ref_Y_p / Sa_pico_p), "—")
T_alpha = E.paso("A2", "T_alpha", r5(T_star_Y / math.sqrt(alpha)), "s")
Sa_alpha = E.paso("A2", "Sa_alpha", r5(ArS * forma_H(T_alpha)), "g")
sube_ord = E.paso("A2", "sube_ord", r5(Sa_alpha / Sa_ref_Y_p), "—")
Q0_an_alpha = E.paso("A3", "Q0_an_alpha",
                     r5(I * Sa_alpha * f_xi_p / R_star_Y * P_sismico), "kN")
sobre_techo_alpha = E.paso("A3", "sobre_techo_alpha", r5(Q0_an_alpha / Q0_p), "—")
k_frontera = E.paso("A3", "k_frontera", r5((T_star_Y / Cr_T1) ** 2), "—")

# ============== B · el marco: geometría, alma variable y rigidez ==========
f_cumb = E.paso("B1", "f_cumb", r5(L_luz / (2 * S_pend)), "m")
tan_pend = E.paso("B1", "tan_pend", r5(1.0 / S_pend), "—")
h_cumb = E.paso("B1", "h_cumb", r5(h_libre + f_cumb), "m")
L_r_x = math.hypot(L_luz / 2.0, f_cumb)          # sin redondear: lo pide el peso
L_r = E.paso("B1", "L_r", r5(L_r_x), "m")
y_infl_riel = E.paso("B2", "y_infl_riel", r5(y_infl / h_riel), "—")
razon_criticas = E.paso("B2", "razon_criticas", r5(Mbase_u / M_nudo_bal), "—")

I_base, Zx_col_base, Ag_col_base = i_soldada(d_col_base, bf_col, tf_col, tw_col)
I_nudo_col, Z_nudo_col, Ag_col_nudo = i_soldada(d_col_nudo, bf_col, tf_col, tw_col)
I_nudo_raf, Zx_raf, Ag_raf_nudo = i_soldada(d_raf_nudo, bf_raf, tf_raf, tw_raf)
I_cumb, Z_cumb, Ag_raf_cumb = i_soldada(d_raf_cumb, bf_raf, tf_raf, tw_raf)
E.paso("B3", "I_base", round(I_base), "mm4")
E.paso("B3", "Zx_col_base", round(Zx_col_base), "mm3")
E.paso("B3", "Ag_col_base", round(Ag_col_base), "mm2")
E.paso("B3", "I_nudo_col", round(I_nudo_col), "mm4")
E.paso("B3", "Z_nudo_col", round(Z_nudo_col), "mm3")
E.paso("B3", "Ag_col_nudo", round(Ag_col_nudo), "mm2")
E.paso("B3", "I_nudo_raf", round(I_nudo_raf), "mm4")
E.paso("B3", "Zx_raf", round(Zx_raf), "mm3")
E.paso("B3", "Ag_raf_nudo", round(Ag_raf_nudo), "mm2")
E.paso("B3", "I_cumb", round(I_cumb), "mm4")
E.paso("B3", "Z_cumb", round(Z_cumb), "mm3")
Iy_raf = E.paso("B3", "Iy_raf",
                round(2 * tf_raf * bf_raf ** 3 / 12.0
                      + (d_raf_nudo - 2 * tf_raf) * tw_raf ** 3 / 12.0), "mm4")
ry_raf = E.paso("B3", "ry_raf", r5(math.sqrt(Iy_raf / Ag_raf_nudo)), "mm")
d_col_riel = E.paso("B3", "d_col_riel",
                    r5(d_col_base - (d_col_base - d_col_nudo) * h_riel / h_libre), "mm")
Ag_col_riel = E.paso("B3", "Ag_col_riel",
                     r2(2 * bf_col * tf_col + (d_col_riel - 2 * tf_col) * tw_col), "mm2")

margen_k = E.paso("B4", "margen_k", r5(k_Y / k_req_p), "—")
w_presup_marco = E.paso("B4", "w_presup_marco",
                        r5((g_techo * A_planta + w_columna * h_libre * n_columnas)
                           / n_marcos), "kN")
# El peso del marco adoptado: los dos miembros son cuñas de espesor constante,
# así que su volumen es el trapecio entre las dos áreas de extremo. El memo lo
# escribe sin desarrollarlo; acá se deriva y cae a 4,2e-6 de su cifra.
vol_marco = (2 * h_libre * (Ag_col_base + Ag_col_nudo) / 2.0
             + 2 * L_r_x * (Ag_raf_nudo + Ag_raf_cumb) / 2.0) * 1e-6
w_marco = E.paso("B4", "w_marco", r5(vol_marco * rho_acero * g_grav), "kN")
consumo_presup = E.paso("B4", "consumo_presup", r5(w_marco / w_presup_marco), "—")
m_marco = E.paso("B5", "m_marco", r5(P_sismico / (n_marcos * g_grav)), "t")
T_star_Y2 = E.paso("B5", "T_star_Y2", r5(2 * math.pi * math.sqrt(m_marco / k_Y)), "s")
Sa_Y2 = E.paso("B5", "Sa_Y2", r5(ArS * forma_H(T_star_Y2)), "g")
subio_ord = E.paso("B5", "subio_ord", r5(Sa_Y2 / Sa_ref_Y_p), "—")
frac_pico_2 = E.paso("B5", "frac_pico_2", r5(Sa_Y2 / Sa_pico_p), "—")
Q0_an_2 = E.paso("B6", "Q0_an_2", r5(I * Sa_Y2 * f_xi_p / R_star_Y * P_sismico), "kN")
sobre_techo_2 = E.paso("B6", "sobre_techo_2", r5(Q0_an_2 / Q0_p), "—")

# ================== C · la deriva que manda de verdad ====================
R_carril = E.paso("C1", "R_carril",
                  r5(SS_carril / 2.0 * (1 + (s_marco - wb_ruedas) / s_marco)), "kN")
SS_marco = E.paso("C1", "SS_marco", r5(2 * R_carril), "kN")
frac_empuje = E.paso("C1", "frac_empuje", r5(SS_marco / SS_total), "—")
d_riel_grua = E.paso("C2", "d_riel_grua", r5(SS_marco / k_riel * 1e3), "mm")
uso_grua = E.paso("C2", "uso_grua", r5(d_riel_grua / dlim_grua), "—")
d_riel_inf = E.paso("C3", "d_riel_inf", r5(SS_marco / k_riel_inf * 1e3), "mm")
redistrib = E.paso("C3", "redistrib", r5(d_riel_grua / d_riel_inf), "—")
uso_inf = E.paso("C3", "uso_inf", r5(d_riel_inf / dlim_grua), "—")
k_tol = E.paso("C4", "k_tol", r5(k_Y * d_riel_grua / dlim_grua), "kN/m")
mas_flexible = E.paso("C4", "mas_flexible", r5(k_req_p / k_tol), "—")
d_Y2 = E.paso("C5", "d_Y2",
              r5(I * f_xi_p * Sa_Y2 * g_grav * T_star_Y2 ** 2
                 / (4 * math.pi ** 2) * 1e3), "mm")
bajo_vs_06 = E.paso("C5", "bajo_vs_06", r5(d_Y2 / d_Y), "—")
uso_63 = E.paso("C5", "uso_63", r5(d_Y2 / d_lim), "—")
sismo_sobre_grua = E.paso("C5", "sismo_sobre_grua", r5(d_Y2 / dlim_grua), "—")
razon_usos = E.paso("C5", "razon_usos", r5(uso_grua / uso_63), "—")
theta_Y2 = E.paso("C6", "theta_Y2",
                  r5(P_sismico * d_Y2 / (Q0_p * h_libre * 1e3)), "—")
f_PDelta_Y2 = E.paso("C6", "f_PDelta_Y2", r5(1.0 / (1.0 - theta_Y2)), "—")
bajo_PDelta = E.paso("C6", "bajo_PDelta", r5(f_PDelta_Y2 / f_PDelta_Y), "—")
p_s_psf = E.paso("C7", "p_s_psf", r5(p_s / psf), "psf")
margen_30psf = E.paso("C7", "margen_30psf", r5(psf_umbral * psf / p_s), "—")
trocha_50 = E.paso("C7", "trocha_50", r5(trocha_D + reb_50 * trocha_S), "mm")
uso_trocha = E.paso("C7", "uso_trocha", r5(trocha_50 / trocha_lim), "—")
trocha_sin = E.paso("C7", "trocha_sin", r5(trocha_D + trocha_S), "mm")
uso_sin = E.paso("C7", "uso_sin", r5(trocha_sin / trocha_lim), "—")
trocha_25 = E.paso("C7", "trocha_25", r5(trocha_D + reb_25 * trocha_S), "mm")
uso_25 = E.paso("C7", "uso_25", r5(trocha_25 / trocha_lim), "—")

# ============ D · cuál de las dos nieves del 02 gobierna el marco =========
w_bal = E.paso("D1", "w_bal", r5(p_s * s_marco), "kN/m")
w_bar = E.paso("D1", "w_bar", r5(p_bar * s_marco), "kN/m")
w_pico = E.paso("D1", "w_pico", r5(p_pico_p * s_marco), "kN/m")
L_sin_ac = E.paso("D1", "L_sin_ac", r5(L_luz / 2.0 - L_ac_p), "m")
F_bal = E.paso("D2", "F_bal", r5(p_s * L_luz * s_marco), "kN")
F_desb = E.paso("D2", "F_desb",
                r5(s_marco * (p_bar * L_luz / 2.0 + p_pico_p * L_ac_p
                              + p_s * L_sin_ac)), "kN")
menos_pesa = E.paso("D2", "menos_pesa", r5(F_desb / F_bal), "—")
mas_momento = E.paso("D2", "mas_momento", r5(M_nudo_bal / M_nudo_des), "—")
des_sobre_grua = E.paso("D3", "des_sobre_grua", r5(d_riel_des / d_riel_grua), "—")
crece_riel_alero = E.paso("D3", "crece_riel_alero", r5(d_alero_des / d_riel_des), "—")

# ============ E · §8.7 a nivel de miembro, sobre un alma que varía ========
conic_col = E.paso("E1", "conic_col",
                   r5((d_col_base - d_col_nudo) / (h_libre * 1e3)), "—")
conic_raf = E.paso("E1", "conic_raf",
                   r5((d_raf_nudo - d_raf_cumb) / r2(L_r * 1e3)), "—")
raiz_ERyFy = math.sqrt(E_ac / (Ry * Fy))
lam_ala = E.paso("E2", "lam_ala", r5(c_ala * raiz_ERyFy), "—")
uso_ala_raf = E.paso("E2", "uso_ala_raf",
                     r5(((bf_raf - tw_raf) / 2.0 / tf_raf) / lam_ala), "—")
Ca_raf = E.paso("E2", "Ca_raf",
                r5(N_raf * 1e3 / (phi_b * Ry * Fy * Ag_raf_nudo)), "—")
lam_alma_raf = E.paso("E2", "lam_alma_raf",
                      r5(c_alma * (1 - c_alma_Ca * Ca_raf) * raiz_ERyFy), "—")
uso_alma_raf12 = E.paso("E2", "uso_alma_raf12",
                        r5(((d_raf_nudo - 2 * tf_raf) / tw_raf) / lam_alma_raf), "—")
Ag_raf_tip = 2 * bf_raf * tf_raf + (d_raf_nudo - 2 * tf_raf) * tw_raf_tip
Ca_raf_tip = E.paso("E2", "Ca_raf_tip",
                    r5(N_raf * 1e3 / (phi_b * Ry * Fy * Ag_raf_tip)), "—")
lam_alma_raf_tip = E.paso("E2", "lam_alma_raf_tip",
                          r5(c_alma * (1 - c_alma_Ca * Ca_raf_tip) * raiz_ERyFy), "—")
uso_alma_raf8 = E.paso("E2", "uso_alma_raf8",
                       r5(((d_raf_nudo - 2 * tf_raf) / tw_raf_tip)
                          / lam_alma_raf_tip), "—")

Rcol_grua = E.paso("E3", "Rcol_grua",
                   r5(Rv_max * (1 + (s_marco - wb_ruedas) / s_marco)), "kN")
Nbase_u = E.paso("E3", "Nbase_u", r5(N_grav + Rcol_grua), "kN")
uso_ala_col = E.paso("E3", "uso_ala_col",
                     r5(((bf_col - tw_col) / 2.0 / tf_col) / lam_ala), "—")
Ca_col = E.paso("E3", "Ca_col",
                r5(Nbase_u * 1e3 / (phi_b * Ry * Fy * Ag_col_base)), "—")
lam_alma_col = E.paso("E3", "lam_alma_col",
                      r5(c_alma * (1 - c_alma_Ca * Ca_col) * raiz_ERyFy), "—")
uso_alma_col14 = E.paso("E3", "uso_alma_col14",
                        r5(((d_col_base - 2 * tf_col) / tw_col) / lam_alma_col), "—")
Ag_col_tip = 2 * bf_col * tf_col + (d_col_base - 2 * tf_col) * tw_col_tip
Ca_col_tip = E.paso("E3", "Ca_col_tip",
                    r5(Nbase_u * 1e3 / (phi_b * Ry * Fy * Ag_col_tip)), "—")
lam_alma_col_tip = E.paso("E3", "lam_alma_col_tip",
                          r5(c_alma * (1 - c_alma_Ca * Ca_col_tip) * raiz_ERyFy), "—")
uso_alma_col12 = E.paso("E3", "uso_alma_col12",
                        r5(((d_col_base - 2 * tf_col) / tw_col_tip)
                           / lam_alma_col_tip), "—")
Q0_marco = E.paso("E3", "Q0_marco", r5(Q0_p / n_marcos), "kN")
Vu_col = E.paso("E3", "Vu_col", r5(kcap_Y * Q0_marco / 2.0), "kN")
phiVn_base = E.paso("E3", "phiVn_base",
                    r5(phi_v * c_corte * Fy * d_col_base * tw_col * 1e-3), "kN")
uso_corte = E.paso("E3", "uso_corte", r5(Vu_col / phiVn_base), "—")

RyFy = Ry * Fy
Mpe_col = E.paso("E4", "Mpe_col", r5(RyFy * Z_nudo_col * 1e-6), "kN·m")
Mpe_raf = E.paso("E4", "Mpe_raf", r5(RyFy * Zx_raf * 1e-6), "kN·m")
Pye_col = E.paso("E4", "Pye_col", r5(RyFy * Ag_col_nudo * 1e-3), "kN")
red_axial = E.paso("E4", "red_axial", r5(1 - N_grav / Pye_col), "—")
Mpc_red = E.paso("E4", "Mpc_red", r5(Mpe_col * red_axial), "kN·m")
dem_874 = E.paso("E4", "dem_874", r5(c_scwb * Mpe_raf), "kN·m")
uso_874 = E.paso("E4", "uso_874", r5(dem_874 / Mpc_red), "—")
red_axial_grua = E.paso("E4", "red_axial_grua", r5(1 - Nbase_u / Pye_col), "—")
Mpc_red_grua = E.paso("E4", "Mpc_red_grua", r5(Mpe_col * red_axial_grua), "kN·m")
uso_874_grua = E.paso("E4", "uso_874_grua", r5(dem_874 / Mpc_red_grua), "—")
umbral_aisc = E.paso("E5", "umbral_aisc",
                     r5(c_exc_aisc * Fy * Ag_col_nudo * 1e-3), "kN")
usa_umbral = E.paso("E5", "usa_umbral", r5(N_grav / umbral_aisc), "—")

Lb_raf = E.paso("E6", "Lb_raf", r2(c_Lb * ry_raf * E_ac / RyFy), "mm")
caben_Lb = E.paso("E6", "caben_Lb", r5(r2(L_r * 1e3) / Lb_raf), "—")
b_pan = E.paso("E6", "b_pan", r2(r2(L_r * 1e3) / n_esp_agua), "mm")
Iy_cumb = 2 * tf_raf * bf_raf ** 3 / 12.0 + (d_raf_cumb - 2 * tf_raf) * tw_raf ** 3 / 12.0
ry_cumb = E.paso("E6", "ry_cumb", r5(math.sqrt(Iy_cumb / Ag_raf_cumb)), "mm")
crece_ry = E.paso("E6", "crece_ry", r5(ry_cumb / ry_raf), "—")
h_o_raf = E.paso("E6", "h_o_raf", r5(d_raf_nudo - tf_raf), "mm")
Pbr_mom = E.paso("E6", "Pbr_mom", r5(c_Pbr * RyFy * Zx_raf * 1e-6), "kN·m")
Pbr_raf = E.paso("E6", "Pbr_raf", r5(Pbr_mom * 1e6 / (h_o_raf * 1e3)), "kN")
Pbr_aisc = E.paso("E6", "Pbr_aisc",
                  r5(c_Pbr_aisc * Mpe_raf * 1e6 / (h_o_raf * 1e3)), "kN")
razon_lecturas = E.paso("E6", "razon_lecturas", r5(Pbr_raf / Pbr_aisc), "—")

# ============== F · el vertical del techo, y las resistencias =============
T_V = E.paso("F1", "T_V", r5(2 * math.pi * math.sqrt(flecha_cumb * 1e-3 / g_grav)), "s")
pasa_ventana = E.paso("F1", "pasa_ventana", r5(T_V / T_fin_ventana), "—")
f_xiV = E.paso("F1", "f_xiV", r5((xi_ref / xi_V) ** 0.4), "—")
SaV_dis = E.paso("F1", "SaV_dis",
                 r5(I * cv_vert * ArS * forma_H(f_T_vert * T_V) * f_xiV / R_V), "g")
modal_vs_est = E.paso("F1", "modal_vs_est", r5(SaV_dis / C_V), "—")
Ez_marco = E.paso("F2", "Ez_marco", r5(Ez_techo / n_marcos), "kN")
Pu_marco = E.paso("F2", "Pu_marco", r5(Pu_nieve / n_marcos), "kN")
S_marco_kN = E.paso("F2", "S_marco_kN", r5(S_comb / n_marcos), "kN")
phiMn_raf = E.paso("F2", "phiMn_raf", r5(phi_b * Fy * Zx_raf * 1e-6), "kN·m")
uso_raf = E.paso("F2", "uso_raf", r5(M_nudo_bal / phiMn_raf), "—")
phiMn_base = E.paso("F2", "phiMn_base", r5(phi_b * Fy * Zx_col_base * 1e-6), "kN·m")
uso_base = E.paso("F2", "uso_base", r5(Mbase_u / phiMn_base), "—")
phiMn_nudo = E.paso("F2", "phiMn_nudo", r5(phi_b * Fy * Z_nudo_col * 1e-6), "kN·m")
uso_nudo = E.paso("F2", "uso_nudo", r5(M_nudo_bal / phiMn_nudo), "—")
phiMn_cumb = E.paso("F2", "phiMn_cumb", r5(phi_b * Fy * Z_cumb * 1e-6), "kN·m")
uso_cumb = E.paso("F2", "uso_cumb", r5(M_cumb / phiMn_cumb), "—")

# ------------------------------------------------------------ Sale
E.sale("k_Y", k_Y, "kN/m", paso="S1", heredan=["11", "12"])
E.sale("k_riel", k_riel, "kN/m", paso="S1", heredan=["08", "11", "12"])
E.sale("T_star_Y2", T_star_Y2, "s", paso="B5", heredan=["12"])
E.sale("d_Y2", d_Y2, "mm", paso="C5", heredan=["12"])
E.sale("f_PDelta_Y2", f_PDelta_Y2, "—", paso="C6", heredan=["12"])
E.sale("SS_marco", SS_marco, "kN", paso="C1", heredan=["08", "11", "12"])
E.sale("d_riel_grua", d_riel_grua, "mm", paso="C2", heredan=["11"])
E.sale("d_riel_inf", d_riel_inf, "mm", paso="C3", heredan=["11"])
E.sale("w_presup_marco", w_presup_marco, "kN", paso="B4", heredan=["11"])
E.sale("d_col_base", d_col_base, "mm", paso="B3", heredan=["10", "13"])
E.sale("d_col_riel", d_col_riel, "mm", paso="B3", heredan=["10"])
E.sale("d_col_nudo", d_col_nudo, "mm", paso="B3", heredan=["10"])
E.sale("bf_col", bf_col, "mm", paso="B3", heredan=["10", "13"])
E.sale("tf_col", tf_col, "mm", paso="B3", heredan=["10", "13"])
E.sale("tw_col", tw_col, "mm", paso="B3", heredan=["10", "13"])
E.sale("Ag_col_riel", Ag_col_riel, "mm2", paso="B3", heredan=["10"])
E.sale("Zx_col_base", round(Zx_col_base), "mm3", paso="B3", heredan=["10", "13"])
E.sale("Mpe_col", Mpe_col, "kN·m", paso="E4", heredan=["13"])
E.sale("Mpe_raf", Mpe_raf, "kN·m", paso="E4", heredan=["11"])
E.sale("Zx_raf", round(Zx_raf), "mm3", paso="B3", heredan=["11"])
E.sale("Lb_raf", Lb_raf, "mm", paso="E6", heredan=["11"])
E.sale("Rcol_grua", Rcol_grua, "kN", paso="E3", heredan=["08", "10", "11"])
E.sale("Nbase_u", Nbase_u, "kN", paso="E3", heredan=["10", "11", "13"])
E.sale("Mbase_u", Mbase_u, "kN·m", paso="S1", heredan=["10", "13"])

# lo que el memo 07 de Guias_Interactivas imprimió en su `## Sale`
E.publicado({
    "k_Y": "5612,11747", "k_riel": "15057,33721", "T_star_Y2": "0,38566",
    "d_Y2": "65,22861", "f_PDelta_Y2": "1,02176", "SS_marco": "46,40000",
    "d_riel_grua": "3,08155", "d_riel_inf": "0,90057", "w_presup_marco": "92,66700",
    "d_col_base": "1050", "d_col_riel": "835,71429", "d_col_nudo": "750",
    "bf_col": "300", "tf_col": "22", "tw_col": "14", "Ag_col_riel": "24284,00",
    "Zx_col_base": "10326926", "Mpe_col": "2485,46922", "Mpe_raf": "1959,09285",
    "Zx_raf": "5162300", "Lb_raf": "5315,28", "Rcol_grua": "299,25983",
    "Nbase_u": "550,89758", "Mbase_u": "1035,55049",
})

# Y las 137 filas de su `## Resumen`, cada una contra el paso que la produce.
# Faltan tres, y no es que no reproduzcan: es que el memo imprimió una cifra y
# sustituyó otra, una unidad más en el último dígito. Están en `## Límites`.
#
#   Q0_an_alpha        el memo imprime Sa = 1,22625 y multiplica por 1,22626
#   sobre_techo_alpha  la misma cifra, propagada
#   uso_alma_col12     el memo imprime C_a = 0,06382 y sustituye 0,06383
#
# En los tres casos la cifra **impresa** es la correcta y es la que se usa: la
# regla de la serie es sustituir lo impreso, no lo que el memo tecleó después.
# Su propio arnés los dejaba pasar porque comparaba con tolerancia relativa
# (5e-5 en el corte del análisis) y el oráculo de acá es absoluto.
E.resumen({
    "alpha": "1,10292", "frac_pico_dec": "0,98044", "T_alpha": "0,38088",
    "Sa_alpha": "1,22625", "sube_ord": "1,01113", "k_frontera": "2,04082",
    "f_cumb": "2,50000", "tan_pend": "0,20000", "L_r": "12,74755",
    "razon_sway": "2,81628", "y_infl": "7,74863", "y_infl_riel": "1,03315",
    "razon_criticas": "1,13250",
    "I_base": "4675712519", "Zx_col_base": "10326926", "Ag_col_base": "27284",
    "I_nudo_col": "2160024719", "Z_nudo_col": "6549326", "Ag_col_nudo": "23084",
    "I_nudo_raf": "1690494333", "Zx_raf": "5162300", "Ag_raf_nudo": "18520",
    "Iy_raf": "52185573", "ry_raf": "53,08291", "I_cumb": "467462458",
    "Z_cumb": "2469675", "d_col_riel": "835,71429", "Ag_col_riel": "24284,00",
    "k_Y": "5612,11747", "k_riel": "15057,33721", "margen_k": "1,07575",
    "w_presup_marco": "92,66700", "consumo_presup": "0,79057",
    "m_marco": "21,14343", "T_star_Y2": "0,38566", "Sa_Y2": "1,22333",
    "subio_ord": "1,00872", "frac_pico_2": "0,98899", "Q0_an_2": "366,06989",
    "sobre_techo_2": "1,21047",
    "R_carril": "23,20000", "SS_marco": "46,40000", "frac_empuje": "0,77333",
    "d_riel_grua": "3,08155", "uso_grua": "0,16435", "d_riel_inf": "0,90057",
    "redistrib": "3,42178", "uso_inf": "0,04803", "k_tol": "922,34776",
    "mas_flexible": "5,65614", "d_Y2": "65,22861", "bajo_vs_06": "0,93769",
    "uso_63": "0,41415", "sismo_sobre_grua": "3,47886", "razon_usos": "0,39684",
    "theta_Y2": "0,02130", "f_PDelta_Y2": "1,02176", "bajo_PDelta": "0,99854",
    "p_s_psf": "26,31562", "margen_30psf": "1,14001", "trocha_D": "6,42686",
    "trocha_S": "14,54407", "trocha_50": "13,69890", "uso_trocha": "0,53933",
    "trocha_sin": "20,97093", "uso_sin": "0,82563", "trocha_25": "17,33491",
    "uso_25": "0,68248",
    "d_riel_des": "1,70543", "des_sobre_grua": "0,55343",
    "d_alero_des": "3,62141", "crece_riel_alero": "2,12346",
    "w_bal": "9,45000", "w_bar": "2,83500", "w_pico": "15,88553",
    "L_sin_ac": "8,47007", "F_bal": "236,25000", "F_desb": "179,49722",
    "menos_pesa": "0,75978", "mas_momento": "1,05473",
    "M_nudo_bal": "914,39164", "M_nudo_des": "866,94355", "Mbase_u": "1035,55049",
    "conic_col": "0,02857", "conic_raf": "0,02550", "lam_ala": "9,18267",
    "uso_ala_raf": "0,64796", "Ca_raf": "0,03447", "lam_alma_raf": "81,38227",
    "uso_alma_raf12": "0,72702", "uso_alma_raf8": "1,11414",
    "Rcol_grua": "299,25983", "Nbase_u": "550,89758", "uso_ala_col": "0,70786",
    "Ca_col": "0,05912", "lam_alma_col": "74,56995", "uso_alma_col14": "0,96362",
    "Vu_col": "105,84698",
    "phiVn_base": "2738,61000", "uso_corte": "0,03865",
    "Mpe_col": "2485,46922", "Mpe_raf": "1959,09285", "Pye_col": "8760,37800",
    "red_axial": "0,97128", "Mpc_red": "2414,08654", "dem_874": "2350,91142",
    "uso_874": "0,97383", "uso_874_grua": "1,00934",
    "umbral_aisc": "2389,19400", "usa_umbral": "0,10532",
    "Lb_raf": "5315,28", "caben_Lb": "2,39828", "b_pan": "4249,18",
    "crece_ry": "1,12500", "Pbr_mom": "117,54557", "Pbr_raf": "161,02133",
    "Pbr_aisc": "53,67378", "razon_lecturas": "3,00000",
    "flecha_cumb": "18,14242", "T_V": "0,27020", "pasa_ventana": "1,24908",
    "SaV_dis": "0,49231", "modal_vs_est": "0,93029", "Ez_marco": "45,46728",
    "Pu_marco": "396,46548", "S_marco_kN": "37,80000",
    "phiMn_raf": "1602,89415", "uso_raf": "0,57046",
    "phiMn_base": "3206,51052", "uso_base": "0,32295",
    "phiMn_nudo": "2033,56572", "uso_nudo": "0,44965",
    "phiMn_cumb": "766,83409", "uso_cumb": "0,29379",
})

if __name__ == "__main__":
    raise SystemExit(main(sys.argv, E))
