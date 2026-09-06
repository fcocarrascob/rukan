"""Eslabón 11 — el arriostramiento continuo de techo: el tope de esbeltez de
§8.8.4 es la transición inelástica de AISC escrita exacta, y la exención sólo
alcanza a la otra mitad de la cláusula.

    python sitio/docs/series/nch2369-galpon-grua/11-arriostramiento-continuo-de-techo/_calculo.py [salida]

Hereda del 01, del 02, del 05, del 06, del 07 y del 10. Transcrito del memo 11 de
`Guias_Interactivas`, que leyó las cláusulas del PDF (ver la tabla de referencias
de `index.md`).

Cuatro cosas que este eslabón hace y conviene no perder de vista al leerlo:

* **El tope de esbeltez global de §8.8.4 no es un número redondo**: es
  `1,5 π √(E/Fy)`, que coincide con la transición inelástica de AISC dentro del
  0,05 %. La cláusula está escribiendo la frontera entre pandeo elástico e
  inelástico, y por eso su exención **no** alcanza a la esbeltez global sino sólo
  a la local de la Tabla 9.
* **Lo que dimensiona la diagonal no es el sismo**: es la acumulación del
  Apéndice 6 de AISC sobre los miembros que el arriostramiento estabiliza, que
  supera a la demanda sísmica por siete veces.
* **El puntal de alero es un colector**: se dimensiona por recoger y arrastrar,
  no por resistir. Es la primera vez en la serie que un elemento se dimensiona
  así.
* **Acá se cierra la banda que el 07 dejó abierta.** El reparto del empuje de
  grúa entre los cinco marcos tiene forma cerrada, y cae prácticamente en el
  extremo favorable de aquella banda.

**Todos los pasos se redondean a cinco decimales.** De las 118 filas del
`## Resumen`, 102 van en `E.resumen()`; las **16** restantes estan en
`## Limites`. Son mas que en cualquier eslabon anterior, y tienen una causa
identificable: el arnes del memo 11 compara los bloques D y E con **1e-4
absoluto** y el bloque A con 5e-5, asi que su quinto decimal nunca se verifico.
El oraculo de aca es media unidad del ultimo decimal publicado, y lo delata.

   mas_laxa           300/113,46099 da 2,64408 y el memo publica 2,64414.
   t_req_200 y _125   200/(17,44708+3) da 9,78135 y 125/(...) da 6,11334; el
                      memo publica 9,78229 y 6,11393, que corresponden a un
                      lambda_md de 17,44506 y no al 17,44708 que el mismo
                      renglon imprime. Es el mayor de los dieciseis, y no se
                      propaga: la pared adoptada es 5 mm en la diagonal y 6 en
                      el puntal, muy por debajo de los dos.
   r_4, r_piso        8 149,00/(2*113,46099) da 35,91102 y 7 500/(2*113,46099)
   y gana_34          da 33,05101; el memo publica 35,91104 y 33,05100, y su
                      cociente 1,08654 contra el 1,08653 de las cifras impresas.
   r_sin_cruce        8 620,07/113,46099 da 75,97387; el memo publica 75,97386.
   razon_k07          15 057,33721/5 612,11747 da 2,68300; el memo publica
                      2,68299. **Se propaga**: la deriva del riel se calcula con
                      la cifra impresa, como manda la regla.
   d_riel_real        con las cinco cifras impresas la expresion da 0,93896 y
   y sobre_cota_baja  el memo publica 0,93897; el cociente arrastra a 1,04263
                      contra 1,04264. No cambia nada: el uso del limite es 5 %.
   supera_sismica     347,00299/47,33782 da 7,33035; el memo publica 7,33042.
   esb_punt_150       7 500/58,83876 da 127,46700; el memo publica 127,46699.
   razon_esp          379,50/255,46515 da 1,48553; el memo publica 1,48554.
   Pce_diag           0,658^(379,50/F_e)*379,50*2 400e-3 da 489,09470, y con el
                      exponente impreso 1,48554 da 489,09173; el memo publica
                      489,08276. Es el segundo mayor, y tampoco decide nada: la
                      capacidad esperada solo se usa para mostrar que el tope de
                      esbeltez salva la diagonal por 2,6 veces.
   salva_tope         910,80/347,00299 da 2,62476; el memo publica 2,62477.

Ninguno de los dieciseis cambia una seccion, una traza ni una conclusion.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from serie import Eslabon, main  # noqa: E402

E = Eslabon("nch2369-galpon-grua", orden=11, slug="arriostramiento-continuo-de-techo",
            titulo="El arriostramiento continuo de techo",
            normas=["NCh2369:2025", "AISC 360-22", "AISC 341-22",
                    "AIST TR-13:2021", "NCh431:2010"],
            carpeta=AQUI)


def r5(x: float) -> float:
    return math.floor(float(x) * 1e5 + 0.5) / 1e5


def r2(x: float) -> float:
    return math.floor(float(x) * 1e2 + 0.5) / 1e2


def ent(x: float) -> float:
    return float(math.floor(float(x) + 0.5))


# ------------------------------------------------------------ lo que entra
L_luz = E.entra("L_luz", de="01", paso="S1")
s_marco = E.entra("s_marco", de="01", paso="S1")
h_libre = E.entra("h_libre", de="01", paso="S1")
g_techo = E.entra("g_techo", de="01", paso="S4")
theta_techo = E.entra("theta_techo", de="02", paso="C1")
S_pend = E.entra("S_pend", de="02", paso="C2")
A_planta = E.entra("A_planta", de="05", paso="A2")
W_edificio = E.entra("W_edificio", de="05", paso="A3")
C_dis = E.entra("C_dis", de="05", paso="D3")
Q0_X = E.entra("Q0_X", de="05", paso="D5")
kcap_X = E.entra("kcap_X", de="05", paso="F2")
dlim_grua = E.entra("dlim_grua", de="06", paso="E5")
k_Y = E.entra("k_Y", de="07", paso="S1")
k_riel = E.entra("k_riel", de="07", paso="S1")
d_riel_grua = E.entra("d_riel_grua", de="07", paso="C2")
d_riel_inf = E.entra("d_riel_inf", de="07", paso="C3")
SS_marco = E.entra("SS_marco", de="07", paso="C1")
Mpe_raf = E.entra("Mpe_raf", de="07", paso="E4")
Zx_raf = E.entra("Zx_raf", de="07", paso="B3")
Lb_raf = E.entra("Lb_raf", de="07", paso="E6")
Rcol_grua = E.entra("Rcol_grua", de="07", paso="E3")
Nbase_u = E.entra("Nbase_u", de="07", paso="E3")
w_presup_marco = E.entra("w_presup_marco", de="07", paso="B4")
h_asiento = E.entra("h_asiento", de="10", paso="A2")
k_esc = E.entra("k_esc", de="10", paso="D6")
w_marco_10 = E.entra("w_marco_10", de="10", paso="B5")

# ------------------------------------------------------------ el caso
Fy = E.caso("Fy", 345.0, "MPa")
Ry = E.caso("Ry", 1.10, "—")
E_ac = E.caso("E_ac", 200000.0, "MPa")
phi_c = E.caso("phi_c", 0.90, "—")
g_grav = E.caso("g_grav", 9.81, "m/s2")
rho_acero = E.caso("rho_acero", 7850.0, "kg/m3")
n_vanos = E.caso("n_vanos", 4, "—")
n_vanos_arr = E.caso("n_vanos_arr", 2, "—")
n_aguas = E.caso("n_aguas", 2, "—")
n_pan_agua = E.caso("n_pan_agua", 3, "—")
h_o_raf = E.caso("h_o_raf", 730.0, "mm")            # del 07 · E6
RyFy = E.caso("RyFy", 379.50, "MPa")

# Los dos cajones adoptados, `(B, t)` en mm.
B_diag, t_diag = (E.caso("B_diag", 125.0, "mm"), E.caso("t_diag", 5.0, "mm"))
B_punt, t_punt = (E.caso("B_punt", 200.0, "mm"), E.caso("t_punt", 6.0, "mm"))
t_diag_4 = E.caso("t_diag_4", 4.0, "mm")            # la pared que no alcanza (E1)
B_punt_150 = E.caso("B_punt_150", 150.0, "mm")      # el tubo que no pasa (E2)
t_punt_150 = E.caso("t_punt_150", 6.0, "mm")
t_t9_diag = E.caso("t_t9_diag", 8.0, "mm")          # el espesor que la Tabla 9 pediría
t_t9_punt = E.caso("t_t9_punt", 10.0, "mm")

# Constantes de cláusula.
c_lam_glob = E.caso("c_lam_glob", 1.5, "—")         # §8.8.4
c_aisc_E3 = E.caso("c_aisc_E3", 4.71, "—")          # AISC §E3
c_658 = E.caso("c_658", 0.658, "—")
c_traccion = E.caso("c_traccion", 300.0, "—")       # AISC §D1
c_lam_md = E.caso("c_lam_md", 0.76, "—")            # Tabla 9, pared de tubo
c_b_plano = E.caso("c_b_plano", 3.0, "—")           # b = B - 3t
c_Pbr = E.caso("c_Pbr", 0.06, "—")                  # §8.7.7
c_beta_raf = E.caso("c_beta_raf", 10.0, "—")        # AISC Ap. §6.3.1b
c_Pbr_col = E.caso("c_Pbr_col", 0.01, "—")          # AISC Ap. §6.2.2
c_beta_col = E.caso("c_beta_col", 8.0, "—")         # AISC Ap. §6.2.2
phi_br = E.caso("phi_br", 0.75, "—")                # AISC Ap. §6
c_acum = E.caso("c_acum", 0.5, "—")                 # Ap. §6.1, el medio del extremo
c_15 = E.caso("c_15", 1.5, "—")                     # D6, el vano extremo
c_tope_885 = E.caso("c_tope_885", 1.0, "—")         # §8.8.5


def caja(B, t):
    """Cajón cuadrado de esquinas vivas: `(A, I, r)`."""
    A = 4 * t * (B - t)
    I = (B ** 4 - (B - 2 * t) ** 4) / 12.0
    return A, I, math.sqrt(I / A)


def Fcr(esb, fy):
    """AISC Ec. E3-2, la rama inelástica."""
    Fe = math.pi ** 2 * E_ac / esb ** 2
    return c_658 ** (fy / Fe) * fy


# ===== A · qué obliga §12.1.2, y qué obliga §8.8.4 sobre lo que obliga =====
L_total = E.paso("A1", "L_total", r5(n_vanos * s_marco), "m")
n_marcos_liga = E.paso("A1", "n_marcos_liga", r5(n_vanos + 1), "—")
frac_vanos_arr = E.paso("A1", "frac_vanos_arr", r5(n_vanos_arr / n_vanos), "—")
vano_mm = E.paso("A1", "vano_mm", r5(s_marco * 1e3), "mm")   # el vano, para rotular

raiz_EFy = math.sqrt(E_ac / Fy)
lam_glob = E.paso("A2", "lam_glob", r5(c_lam_glob * math.pi * raiz_EFy), "—")
lam_aisc = E.paso("A2", "lam_aisc", r5(c_aisc_E3 * raiz_EFy), "—")
difieren = E.paso("A2", "difieren", r5(lam_glob / lam_aisc), "—")
# El memo escribe pi^2 E / 113,46099^2, pero el tope es exactamente
# `1,5 pi sqrt(E/Fy)`, asi que `F_e` vale `Fy/2,25` cerrado: con la cifra
# impresa daria 153,33334 y el memo publico el exacto.
Fe_tope = E.paso("A2", "Fe_tope",
                 r5(math.pi ** 2 * E_ac / (c_lam_glob * math.pi * raiz_EFy) ** 2),
                 "MPa")
razon_tope = E.paso("A2", "razon_tope", r5(Fy / Fe_tope), "—")
Fcr_min = E.paso("A2", "Fcr_min", r5(c_658 ** razon_tope * Fy), "MPa")
frac_fluencia = E.paso("A2", "frac_fluencia", r5(Fcr_min / Fy), "—")
rinde_menos = E.paso("A3", "rinde_menos", r5(Fy / Fcr_min), "—")
mas_laxa = E.paso("A3", "mas_laxa", r5(c_traccion / lam_glob), "—")

f_cumb = E.paso("A4", "f_cumb", r5(L_luz / (2 * S_pend)), "m")
L_r = E.paso("A4", "L_r", r5(math.hypot(L_luz / 2.0, f_cumb)), "m")
Lr_mm = E.paso("A4", "Lr_mm", r2(L_r * 1e3), "mm")
Ld_agua = E.paso("A4", "Ld_agua", r2(math.hypot(vano_mm, Lr_mm)), "mm")
Ld_planta = E.paso("A4", "Ld_planta",
                   r2(math.hypot(s_marco * 1e3, L_luz / 2.0 * 1e3)), "mm")
subestima = E.paso("A4", "subestima", r5(Ld_agua / Ld_planta), "—")
r_agua = E.paso("A4", "r_agua", r5(Ld_agua / lam_glob), "mm")

# ========= B · la exención de §8.8.4, y a cuál de las dos alcanza =========
lam_md_tubo = E.paso("B1", "lam_md_tubo",
                     r5(c_lam_md * math.sqrt(E_ac / (Ry * Fy))), "—")
t_req_200 = E.paso("B1", "t_req_200",
                   r5(B_punt / (lam_md_tubo + c_b_plano)), "mm")
t_req_125 = E.paso("B1", "t_req_125",
                   r5(B_diag / (lam_md_tubo + c_b_plano)), "mm")
uso_t9_125 = E.paso("B2", "uso_t9_125",
                    r5((B_diag - c_b_plano * t_t9_diag) / t_t9_diag / lam_md_tubo), "—")
uso_t9_200 = E.paso("B2", "uso_t9_200",
                    r5((B_punt - c_b_plano * t_t9_punt) / t_t9_punt / lam_md_tubo), "—")
demanda_mas = E.paso("B3", "demanda_mas", r5((kcap_X - 1.0) / 1.0), "—")
fusibles = E.paso("B3", "fusibles", r5(n_aguas - n_aguas), "—")

# ====== C · la traza: cuántos paneles por agua, y qué radio piden =========
b_pan_2 = E.paso("C1", "b_pan_2", r2(Lr_mm / 2.0), "mm")
Ld_2 = E.paso("C1", "Ld_2", r2(math.hypot(s_marco * 1e3, b_pan_2)), "mm")
b_pan_4 = E.paso("C1", "b_pan_4", r2(Lr_mm / 4.0), "mm")
Ld_4 = E.paso("C1", "Ld_4", r2(math.hypot(s_marco * 1e3, b_pan_4)), "mm")
r_1 = E.paso("C1", "r_1", r5(Ld_agua / (2 * lam_glob)), "mm")
r_2v = E.paso("C1", "r_2", r5(Ld_2 / (2 * lam_glob)), "mm")
r_4 = E.paso("C1", "r_4", r5(Ld_4 / (2 * lam_glob)), "mm")
r_piso = E.paso("C1", "r_piso", r5(s_marco * 1e3 / (2 * lam_glob)), "mm")
gana_34 = E.paso("C1", "gana_34", r5(r_4 / r_piso), "—")

b_pan_techo = E.paso("C3", "b_pan_techo", r2(Lr_mm / n_pan_agua), "mm")
L_diag_techo = E.paso("C3", "L_diag_techo",
                      r2(math.hypot(s_marco * 1e3, b_pan_techo)), "mm")
KL_diag_ex = L_diag_techo / 2.0
KL_diag = E.paso("C2", "KL_diag", r2(KL_diag_ex), "mm")
r_sin_cruce = E.paso("C2", "r_sin_cruce", r5(L_diag_techo / lam_glob), "mm")
r_req = E.paso("C3", "r_req", r5(KL_diag_ex / lam_glob), "mm")
vale_cruce = E.paso("C2", "vale_cruce", r5(r_sin_cruce / r_req), "—")
uso_sep_rafter = E.paso("C3", "uso_sep_rafter", r5(b_pan_techo / Lb_raf), "—")

n_lin = E.paso("C4", "n_lin",
               r5(n_aguas + n_aguas * (n_pan_agua - 1) + 1), "—")
n_pan = E.paso("C4", "n_pan", r5(n_pan_agua * n_aguas * n_vanos), "—")
n_diag = E.paso("C4", "n_diag", r5(2 * n_pan), "—")
L_punt_tot = E.paso("C4", "L_punt_tot", r5(n_lin * L_total), "m")
L_diag_tot = E.paso("C4", "L_diag_tot", r5(n_diag * L_diag_techo / 1e3), "m")

m_diag = E.paso("E4", "m_diag", r5(caja(B_diag, t_diag)[0] * rho_acero * 1e-6), "kg/m")
m_punt = E.paso("E4", "m_punt", r5(caja(B_punt, t_punt)[0] * rho_acero * 1e-6), "kg/m")
m_diag_t9 = caja(B_diag, t_t9_diag)[0] * rho_acero * 1e-6
m_punt_t9 = caja(B_punt, t_t9_punt)[0] * rho_acero * 1e-6
W_arr = E.paso("E4", "W_arr",
               r2(n_diag * L_diag_techo / 1e3 * m_diag + L_punt_tot * m_punt), "kg")
pesa_sin_exencion = E.paso("B2", "pesa_sin_exencion",
                           r5((L_diag_tot * r5(m_diag_t9) + L_punt_tot * r5(m_punt_t9))
                              / W_arr), "—")

# ============ D · las cuatro demandas, y cuál dimensiona =================
F_diaf_sin = E.paso("D1", "F_diaf_sin", r5(r5(C_dis) * W_edificio), "kN")
F_diaf_X = E.paso("D1", "F_diaf_X", r5(F_diaf_sin * kcap_X), "kN")
V_z = E.paso("D1", "V_z", r5(F_diaf_X / (n_vanos * n_aguas)), "kN")
cos_diag = E.paso("D1", "cos_diag", r5(L_diag_techo / (2 * s_marco * 1e3)), "—")
N_diag_sismo = E.paso("D1", "N_diag_sismo", r5(V_z * cos_diag), "kN")
F_col_alero = E.paso("D1", "F_col_alero", r5(F_diaf_X / n_vanos), "kN")

A_diag_techo, I_diag_x, r_diag_x = caja(B_diag, t_diag)
k_pan = E.paso("D2", "k_pan",
               r5(2 * E_ac * A_diag_techo * b_pan_techo ** 2 / L_diag_techo ** 3), "N/mm")
cos2_pend = E.paso("D2", "cos2_pend", r5(1.0 / (1.0 + (1.0 / S_pend) ** 2)), "—")
kd_vano = E.paso("D2", "kd_vano",
                 r5(2 * n_pan_agua * k_pan * cos2_pend), "kN/m")
rho_diaf = E.paso("D2", "rho_diaf", r5(kd_vano / k_Y), "—")


def reparto(rho):
    """La fracción que retiene el marco cargado, con cinco marcos ligados."""
    return (1 + 3 * rho + rho ** 2) / (1 + 5 * rho + 5 * rho ** 2)


f_marco_grua = E.paso("D2", "f_marco_grua", r5(reparto(rho_diaf)), "—")
chi2 = E.paso("D2", "chi2",
              r5((1.0 / k_riel - d_riel_inf / (SS_marco * 1000.0))
                 / (0.8 / k_Y)), "—")
razon_k07 = E.paso("D2", "razon_k07", r5(k_riel / k_Y), "—")
razon_k07_p = 2.68299   # lo que el memo imprime y sustituye; ver `## Limites`
d_riel_real = E.paso("D2", "d_riel_real",
                     r5(r5(d_riel_grua)
                        * (1 - chi2 * (1 - f_marco_grua) * razon_k07_p)), "mm")
uso_grua_real = E.paso("D2", "uso_grua_real", r5(d_riel_real / dlim_grua), "—")
sobre_cota_baja = E.paso("D2", "sobre_cota_baja",
                         r5(d_riel_real / r5(d_riel_inf)), "—")
rho_esc = E.paso("D3", "rho_esc", r5(rho_diaf / k_esc), "—")
f_esc = E.paso("D3", "f_esc", r5(reparto(rho_esc)), "—")
baja_cuota = E.paso("D3", "baja_cuota",
                    r5((1 - f_esc) / (1 - f_marco_grua)), "—")

Pbr_raf = E.paso("D4", "Pbr_raf",
                 r5(c_Pbr * RyFy * Zx_raf * 1e-6 / (h_o_raf / 1e3)), "kN")
beta_raf = E.paso("D4", "beta_raf",
                  r5(c_beta_raf * Mpe_raf * 1e6 / (phi_br * Lb_raf * h_o_raf)), "N/mm")
rebaja_Lb = E.paso("D4", "rebaja_Lb", r5(Lb_raf / b_pan_techo), "—")
k_nudo = E.paso("D4", "k_nudo",
                r5(4 * E_ac * A_diag_techo * (s_marco * 1e3) ** 2
                   / L_diag_techo ** 3), "N/mm")
factor_rig_raf = E.paso("D4", "factor_rig_raf", r5(k_nudo / beta_raf), "—")
P_r_col = E.paso("D5", "P_r_col", r5(Nbase_u - Rcol_grua), "kN")
L_br_col = E.paso("D5", "L_br_col", r5(h_libre * 1e3 - h_asiento), "mm")
Pbr_col = E.paso("D5", "Pbr_col", r5(c_Pbr_col * P_r_col), "kN")
beta_col = E.paso("D5", "beta_col",
                  r5(c_beta_col * P_r_col * 1000.0 / (phi_br * L_br_col)), "N/mm")
factor_rig_col = E.paso("D5", "factor_rig_col", r5(k_nudo / beta_col), "—")
pide_col = E.paso("D5", "pide_col", r5(Pbr_col / Pbr_raf), "—")
Pbr_acum = E.paso("D6", "Pbr_acum",
                  r5(2 * Pbr_raf + c_acum * Pbr_raf), "kN")
P_vano_extremo = E.paso("D6", "P_vano_extremo", r5(c_15 * Pbr_acum), "kN")
N_diag_acum = E.paso("D6", "N_diag_acum", r5(P_vano_extremo * cos_diag), "kN")
supera_sismica = E.paso("D6", "supera_sismica", r5(N_diag_acum / N_diag_sismo), "—")
suma_ap61 = E.paso("D6", "suma_ap61",
                   r5(n_marcos_liga * n_aguas * Pbr_acum), "kN")
veces_Q0 = E.paso("D6", "veces_Q0", r5(suma_ap61 / Q0_X), "—")

# ================ E · las dos secciones, y lo que pesan =================
E.paso("E1", "A_diag_techo", r5(A_diag_techo), "mm2")
I_diag = E.paso("E1", "I_diag", r5(I_diag_x), "mm4")
r_diag = E.paso("E1", "r_diag", r5(r_diag_x), "mm")
sl_diag = KL_diag / r_diag
esb_diag = E.paso("E1", "esb_diag", r5(sl_diag), "—")
uso_esb_diag = E.paso("E1", "uso_esb_diag", r5(esb_diag / lam_glob), "—")
Fe_diag_ex = math.pi ** 2 * E_ac / sl_diag ** 2
Fe_diag = E.paso("E1", "Fe_diag", r5(Fe_diag_ex), "MPa")
razon_diag = E.paso("E1", "razon_diag", r5(Fy / Fe_diag_ex), "—")
Fcr_diag_ex = c_658 ** (Fy / Fe_diag_ex) * Fy
Fcr_diag = E.paso("E1", "Fcr_diag", r5(Fcr_diag_ex), "MPa")
phiPn_diag = E.paso("E1", "phiPn_diag",
                    r5(phi_c * Fcr_diag_ex * A_diag_techo * 1e-3), "kN")
uso_ax_diag = E.paso("E1", "uso_ax_diag", r5(N_diag_acum / phiPn_diag), "—")
A4_, I4_, r4_ = caja(B_diag, t_diag_4)
esb_diag_4 = E.paso("E1", "esb_diag_4", r5(KL_diag / r5(r4_)), "—")
phiPn_diag_4 = phi_c * Fcr(esb_diag_4, Fy) * A4_ * 1e-3
uso_ax_diag_4 = E.paso("E1", "uso_ax_diag_4",
                       r5(N_diag_acum / r5(phiPn_diag_4)), "—")

A_punt_techo, I_punt_x, r_punt_x = caja(B_punt, t_punt)
E.paso("E2", "A_punt_techo", r5(A_punt_techo), "mm2")
r_punt = E.paso("E2", "r_punt", r5(r_punt_x), "mm")
sl_punt = s_marco * 1e3 / r_punt
esb_punt = E.paso("E2", "esb_punt", r5(sl_punt), "—")
r_req_punt = E.paso("E2", "r_req_punt", r5(s_marco * 1e3 / lam_glob), "mm")
uso_esb_punt = E.paso("E2", "uso_esb_punt", r5(esb_punt / lam_glob), "—")
r_150 = caja(B_punt_150, t_punt_150)[2]
esb_punt_150 = E.paso("E2", "esb_punt_150", r5(s_marco * 1e3 / r5(r_150)), "—")
uso_esb_150 = E.paso("E2", "uso_esb_150", r5(esb_punt_150 / lam_glob), "—")
Fe_punt_ex = math.pi ** 2 * E_ac / sl_punt ** 2
Fe_punt = E.paso("E2", "Fe_punt", r5(Fe_punt_ex), "MPa")
Fcr_punt_ex = c_658 ** (Fy / Fe_punt_ex) * Fy
Fcr_punt = E.paso("E2", "Fcr_punt", r5(Fcr_punt_ex), "MPa")
phiPn_punt = E.paso("E2", "phiPn_punt",
                    r5(phi_c * Fcr_punt_ex * A_punt_techo * 1e-3), "kN")
uso_ax_punt = E.paso("E2", "uso_ax_punt", r5(F_col_alero / phiPn_punt), "—")

Tye_diag = E.paso("E3", "Tye_diag", r5(RyFy * A_diag_techo * 1e-3), "kN")
razon_esp = E.paso("E3", "razon_esp", r5(RyFy / Fe_diag_ex), "—")
Pce_diag = E.paso("E3", "Pce_diag",
                  r5(c_658 ** (RyFy / Fe_diag_ex) * RyFy * A_diag_techo * 1e-3), "kN")
salva_tope = E.paso("E3", "salva_tope", r5(Tye_diag / N_diag_acum), "—")

g_arr = E.paso("E4", "g_arr", r5(W_arr / A_planta), "kg/m2")
uso_presup_techo = E.paso("E4", "uso_presup_techo", r5(g_arr / g_techo), "—")
W_arr_marco = E.paso("E4", "W_arr_marco",
                     r5(W_arr * g_grav * 1e-3 / n_marcos_liga), "kN")
sobre_presup = E.paso("E4", "sobre_presup",
                      r5((r2(w_marco_10) + W_arr_marco) / w_presup_marco), "—")

# ------------------------------------------------------------ Sale
E.sale("lam_glob", lam_glob, "—", paso="A2", heredan=["13"])
E.sale("b_pan_techo", b_pan_techo, "mm", paso="C3", heredan=["12"])
E.sale("L_diag_techo", L_diag_techo, "mm", paso="C3", heredan=["12", "13"])
E.sale("A_diag_techo", A_diag_techo, "mm2", paso="E1", heredan=["13"])
E.sale("A_punt_techo", A_punt_techo, "mm2", paso="E2", heredan=["12", "13"])
E.sale("kd_vano", kd_vano, "kN/m", paso="D2", heredan=["12"])
E.sale("f_marco_grua", f_marco_grua, "—", paso="D2", heredan=["12"])
E.sale("F_diaf_X", F_diaf_X, "kN", paso="D1", heredan=["12", "13"])
E.sale("F_col_alero", F_col_alero, "kN", paso="D1", heredan=["12", "13"])
E.sale("Pbr_acum", Pbr_acum, "kN", paso="D6", heredan=["13"])

E.publicado({
    "lam_glob": "113,46099", "b_pan_techo": "4249,18",
    "L_diag_techo": "8620,07", "A_diag_techo": "2400,00000",
    "A_punt_techo": "4656,00000", "kd_vano": "156123,29866",
    "f_marco_grua": "0,21408", "F_diaf_X": "658,99137",
    "F_col_alero": "164,74784", "Pbr_acum": "402,55333",
})

E.resumen({
    "L_total": "30,00000", "n_marcos_liga": "5,00000",
    "frac_vanos_arr": "0,50000", "lam_glob": "113,46099",
    "lam_aisc": "113,40347", "difieren": "1,00051", "Fe_tope": "153,33333",
    "razon_tope": "2,25000", "Fcr_min": "134,53254",
    "frac_fluencia": "0,38995", "rinde_menos": "2,56444",
    "f_cumb": "2,50000", "L_r": "12,74755",
    "Ld_agua": "14790,20000", "Ld_planta": "14577,38000",
    "subestima": "1,01460", "r_agua": "130,35494",
    "lam_md_tubo": "17,44708",
    "uso_t9_125": "0,72362", "uso_t9_200": "0,97438",
    "kcap_X": "2,80000",
    "demanda_mas": "1,80000", "fusibles": "0,00000",
    "b_pan_2": "6373,78000", "Ld_2": "9842,51000", "b_pan_4": "3186,89000",
    "Ld_4": "8149,00000", "r_1": "65,17747", "r_2": "43,37398",
    "KL_diag": "4310,04000",
    "vale_cruce": "2,00000", "b_pan_techo": "4249,18000",
    "uso_sep_rafter": "0,79943", "L_diag_techo": "8620,07000",
    "r_req": "37,98693",
    "n_lin": "7,00000", "n_pan": "24,00000", "n_diag": "48,00000",
    "L_punt_tot": "210,00000", "L_diag_tot": "413,76336",
    "F_diaf_sin": "235,35406", "F_diaf_X": "658,99137", "V_z": "82,37392",
    "cos_diag": "0,57467", "N_diag_sismo": "47,33782",
    "F_col_alero": "164,74784", "k_pan": "27061,32847",
    "cos2_pend": "0,96154", "kd_vano": "156123,29866",
    "rho_diaf": "27,81896", "f_marco_grua": "0,21408", "chi2": "0,32974",
    "uso_grua_real": "0,05008",
    "rho_esc": "12,37493", "f_esc": "0,23084", "baja_cuota": "0,97867",
    "Pbr_raf": "161,02133", "beta_raf": "6732,00994", "rebaja_Lb": "1,25090",
    "k_nudo": "168613,12512", "factor_rig_raf": "25,04648",
    "P_r_col": "251,63775", "L_br_col": "3815,76000", "Pbr_col": "2,51638",
    "beta_col": "703,43418", "factor_rig_col": "239,69993",
    "pide_col": "0,01563", "Pbr_acum": "402,55333",
    "P_vano_extremo": "603,83000", "N_diag_acum": "347,00299",
    "suma_ap61": "4025,53330",
    "veces_Q0": "13,31107",
    "A_diag_techo": "2400,00000", "I_diag": "5770000,00000",
    "r_diag": "49,03230", "esb_diag": "87,90206", "uso_esb_diag": "0,77473",
    "Fe_diag": "255,46515", "razon_diag": "1,35048", "Fcr_diag": "196,03662",
    "phiPn_diag": "423,43911", "uso_ax_diag": "0,81949",
    "esb_diag_4": "87,20359", "uso_ax_diag_4": "1,00684",
    "A_punt_techo": "4656,00000", "r_punt": "79,23804", "esb_punt": "94,65151",
    "r_req_punt": "66,10201", "uso_esb_punt": "0,83422",
    "uso_esb_150": "1,12344",
    "Fe_punt": "220,33052", "Fcr_punt": "179,13971",
    "phiPn_punt": "750,66703", "uso_ax_punt": "0,21947",
    "Tye_diag": "910,80000",
    "m_diag": "18,84000", "m_punt": "36,54960", "W_arr": "15470,72000",
    "g_arr": "20,62763", "uso_presup_techo": "0,54283",
    "W_arr_marco": "30,35355", "sobre_presup": "1,30147",
})

if __name__ == "__main__":
    raise SystemExit(main(sys.argv, E))
