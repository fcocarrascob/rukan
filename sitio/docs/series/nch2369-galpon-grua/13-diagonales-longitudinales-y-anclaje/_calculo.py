"""Eslabón 13 — diagonales longitudinales y anclaje: la sección ilustrativa no
pasa ninguno de los dos límites de §8.6.3, y el anclaje que la Tabla 7 exige
para `R = 5` se dimensiona acá, trece eslabones después de haberlo usado.

    python sitio/docs/series/nch2369-galpon-grua/13-diagonales-longitudinales-y-anclaje/_calculo.py [salida]

**Es el único eslabón de la serie sin memo previo**, y eso le cambia el arnés.
Los doce anteriores se migraron contra el oráculo `publicado()` — lo que el memo
original imprimió—; acá no hay memo, así que `E.publicado({})` va vacío a
propósito y lo que sostiene las cifras es otra cosa:

* **la cadena** — 37 símbolos entran de los eslabones 05, 06, 07, 10, 11 y 12, y
  `verificar_cadena` los comprueba uno por uno contra lo que aquéllos publicaron;
* **la hoja de valores de Harness** — `2026-simulado-galpon-grua/20_calculo/
  scripts/e13_diagonales_y_anclaje.py`, que lee las cláusulas de la página
  rasterizada y emite su memo con la cita al lado de cada número. Los límites de
  §8.6.3, §8.6.2 y §8.5.2 salen de ahí, no de este archivo;
* **un contraste cruzado que ya cerró**: `esb_lim` recalculado desde la página
  reproduce el `lam_glob` que el 11 · A2 publica, a cinco decimales, por un
  camino independiente.

Las cuatro cosas que este eslabón encuentra
-------------------------------------------
1. **El `TUBO_PANEL` no cumple ninguno de los dos límites de §8.6.3.** `b/t` da
   25,000 contra un `λ_md` de 17,44708, y la esbeltez 131,58193 contra 113,46099
   —y eso ya tomando el beneficio de §8.6.4—. Estaba declarado «parámetro
   ilustrativo, es del 13» en `case11_data.py`, y acá se cobra.
2. **El modelo no materializa la condición que le permitiría tomar `L/2`.** Las X
   del panel se montan como dos bielas completas que **se cruzan sin nudo**, y
   §8.6.4 exige conectarlas en el punto de cruce.
3. **El 13 realimenta al 12.** Cambiar la sección cambia `k_pan`, y con ella
   `rho_pan`, la irregularidad torsional y el colector. La cadena de esta serie
   es un ciclo, no un árbol, y es la primera vez que se ve.
4. **`R = 5` cuelga de este eslabón.** La fila 5.5 de la Tabla 7 da `R = 5` sólo
   «con arriostramiento continuo de techo, **y con anclajes dúctiles**». La
   condición se cumple o no acá, y §8.5.2 dice exactamente qué hay que hacer.

Todos los pasos se redondean a cinco decimales, como el resto de la serie.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from serie import Eslabon, main  # noqa: E402

E = Eslabon("nch2369-galpon-grua", orden=13, slug="diagonales-longitudinales-y-anclaje",
            titulo="Las diagonales longitudinales y el anclaje",
            normas=["NCh2369:2025", "AISC 360-22"],
            carpeta=AQUI)


def r5(x: float) -> float:
    return math.floor(float(x) * 1e5 + 0.5) / 1e5


# ------------------------------------------------------------ lo que entra
# 05 — el amplificador de capacidad, que las tres cláusulas de este eslabón usan.
R1_X = E.entra("R1_X", de="05", paso="F1")
kcap_X = E.entra("kcap_X", de="05", paso="F2")
# 06 — la vertical y las dos envolventes de carga axial en la base.
C_V = E.entra("C_V", de="06", paso="B1")
E_z = E.entra("E_z", de="06", paso="B2")
D_grav = E.entra("D_grav", de="06", paso="C1")
Pu_max = E.entra("Pu_max", de="06", paso="C2")
Pu_desc = E.entra("Pu_desc", de="06", paso="C3")
# 07 — la columna: su geometría, su módulo plástico y su capacidad esperada.
d_col_base = E.entra("d_col_base", de="07", paso="B3")
bf_col = E.entra("bf_col", de="07", paso="B3")
tf_col = E.entra("tf_col", de="07", paso="B3")
tw_col = E.entra("tw_col", de="07", paso="B3")
Zx_col_base = E.entra("Zx_col_base", de="07", paso="B3")
Mpe_col = E.entra("Mpe_col", de="07", paso="E4")
Nbase_u = E.entra("Nbase_u", de="07", paso="E3")
Mbase_u = E.entra("Mbase_u", de="07", paso="S1")
# 10 — el fuste de grúa y la sección compuesta de la base.
d_fuste_grua = E.entra("d_fuste_grua", de="10", paso="S2")
bf_fuste_grua = E.entra("bf_fuste_grua", de="10", paso="S2")
tf_fuste_grua = E.entra("tf_fuste_grua", de="10", paso="S2")
tw_fuste_grua = E.entra("tw_fuste_grua", de="10", paso="S2")
tp_alma = E.entra("tp_alma", de="10", paso="S3")
Ag_comp_base = E.entra("Ag_comp_base", de="10", paso="B3")
Ix_comp_base = E.entra("Ix_comp_base", de="10", paso="B3")
xb_comp_base = E.entra("xb_comp_base", de="10", paso="B3")
Mecc_10 = E.entra("Mecc_10", de="10", paso="C2")
# 11 — el techo arriostrado, y los tres encargos que dejó abiertos.
lam_glob = E.entra("lam_glob", de="11", paso="A2")
L_diag_techo = E.entra("L_diag_techo", de="11", paso="C3")
A_diag_techo = E.entra("A_diag_techo", de="11", paso="E1")
A_punt_techo = E.entra("A_punt_techo", de="11", paso="E2")
F_diaf_X = E.entra("F_diaf_X", de="11", paso="D1")
F_col_alero = E.entra("F_col_alero", de="11", paso="D1")
Pbr_acum = E.entra("Pbr_acum", de="11", paso="D6")
# 12 — la torsión en planta y las dos cotas que le puso al panel.
x_g_tope = E.entra("x_g_tope", de="12", paso="S3")
e_tors = E.entra("e_tors", de="12", paso="C3")
raz_tors_Y = E.entra("raz_tors_Y", de="12", paso="C4")
raz_tors_X = E.entra("raz_tors_X", de="12", paso="D3")
kbr_lim = E.entra("kbr_lim", de="12", paso="C6")
F_col_12 = E.entra("F_col_12", de="12", paso="D3")

# ------------------------------------------------------------ el caso
# Geometría del panel longitudinal, la misma que el 12 · B5 usa.
s_marco = E.caso("s_marco", 7.50, "m")
h_libre = E.caso("h_libre", 10.50, "m")
n_paneles = E.caso("n_paneles", 4, "—")        # dos vanos × dos muros
n_lineas = E.caso("n_lineas", 2, "—")          # los dos muros longitudinales
n_bases = E.caso("n_bases", 10, "—")           # cinco marcos × dos muros
# Material, de `case11_data.py`. `Fy` NO se leyó de NCh427/1, que es un hueco
# declarado del proyecto: viene del catálogo de la serie.
E_ac = E.caso("E_ac", 200000.0, "MPa")
Fy = E.caso("Fy", 345.0, "MPa")
Ry = E.caso("Ry", 1.10, "—")
phi_c = E.caso("phi_c", 0.90, "—")
phi_t = E.caso("phi_t", 0.90, "—")
c_658 = E.caso("c_658", 0.658, "—")
# La sección que `case11_data.py` trae, declarada «parámetro ilustrativo».
B_ilus = E.caso("B_ilus", 125.0, "mm")
t_ilus = E.caso("t_ilus", 5.0, "mm")
# La sección que este eslabón adopta. Ver `S1`.
B_pan = E.caso("B_pan", 175.0, "mm")
t_pan = E.caso("t_pan", 12.0, "mm")
# --- los valores leídos rasterizados, que la hoja de Harness respalda ---
c_lam_md = E.caso("c_lam_md", 0.76, "—")        # Tabla 9, impresa 98
c_esbeltez = E.caso("c_esbeltez", 1.50, "—")    # §8.6.3, impresa 87
frac_traccion = E.caso("frac_traccion", 0.30, "—")   # §8.6.2, impresa 87
hilo_min = E.caso("hilo_min", 75.0, "mm")       # §8.5.2, impresa 85
long_exp_min = E.caso("long_exp_min", 250.0, "mm")   # §8.5.2
n_diam_exp = E.caso("n_diam_exp", 8.0, "—")     # §8.5.2
frac_Mpe_base = E.caso("frac_Mpe_base", 0.50, "—")   # §8.5.2, bases empotradas
corte_exento = E.caso("corte_exento", 75.0, "kN")    # §8.5.3, excepción 1, LRFD


def props_cajon(B: float, t: float) -> tuple[float, float, float]:
    """Cajón cuadrado `B × B × t`: `(A, I, r)`, en mm."""
    bi = B - 2.0 * t
    A = B * B - bi * bi
    I = (B ** 4 - bi ** 4) / 12.0
    return A, I, math.sqrt(I / A)


def phiPn_compresion(A: float, esbeltez: float) -> tuple[float, float, float]:
    """AISC 360 Cap. E: `(Fe, Fcr, phi*Pn)` con `Pn` en kN."""
    Fe = math.pi ** 2 * E_ac / esbeltez ** 2
    Fcr = c_658 ** (Fy / Fe) * Fy if Fy / Fe <= 2.25 else 0.877 * Fe
    return Fe, Fcr, phi_c * Fcr * A / 1000.0


# ========== A · los dos límites de §8.6.3, y la sección que no los pasa =======
lam_md = E.paso("A1", "lam_md", r5(c_lam_md * math.sqrt(E_ac / (Ry * Fy))), "—")
# Contraste: el 11 · A2 publica este mismo límite por otro camino.
esb_lim = E.paso("A1", "esb_lim", r5(c_esbeltez * math.pi * math.sqrt(E_ac / Fy)), "—")
dif_lam = E.paso("A1", "dif_lam", r5(abs(esb_lim - lam_glob)), "—")

A_ilus, I_ilus, r_ilus = props_cajon(B_ilus, t_ilus)
A_ilus = E.paso("A2", "A_ilus", r5(A_ilus), "mm2")
r_ilus = E.paso("A2", "r_ilus", r5(r_ilus), "mm")
bt_ilus = E.paso("A2", "bt_ilus", r5(B_ilus / t_ilus), "—")
uso_bt_ilus = E.paso("A2", "uso_bt_ilus", r5(bt_ilus / lam_md), "—")

L_diag = E.paso("A3", "L_diag", r5(math.hypot(s_marco * 1e3, h_libre * 1e3)), "mm")
ang_diag = E.paso("A3", "ang_diag", r5(math.degrees(math.atan2(h_libre, s_marco))), "°")
esb_ilus_ent = E.paso("A3", "esb_ilus_ent", r5(L_diag / r_ilus), "—")
esb_ilus = E.paso("A3", "esb_ilus", r5(0.5 * L_diag / r_ilus), "—")
uso_esb_ilus = E.paso("A3", "uso_esb_ilus", r5(esb_ilus / esb_lim), "—")

# ============ B · la sección que sí los pasa, y lo que cuesta ================
A_pan, I_pan, r_pan = props_cajon(B_pan, t_pan)
A_pan = E.paso("B1", "A_pan", r5(A_pan), "mm2")
I_pan = E.paso("B1", "I_pan", r5(I_pan), "mm4")
r_pan = E.paso("B1", "r_pan", r5(r_pan), "mm")
bt_pan = E.paso("B1", "bt_pan", r5(B_pan / t_pan), "—")
uso_bt = E.paso("B1", "uso_bt", r5(bt_pan / lam_md), "—")

esb_pan = E.paso("B2", "esb_pan", r5(0.5 * L_diag / r_pan), "—")
uso_esb = E.paso("B2", "uso_esb", r5(esb_pan / esb_lim), "—")
r_req = E.paso("B2", "r_req", r5(0.5 * L_diag / esb_lim), "mm")

_Fe, _Fcr, _phiPn = phiPn_compresion(A_pan, esb_pan)
Fe_pan = E.paso("B3", "Fe_pan", r5(_Fe), "MPa")
Fcr_pan = E.paso("B3", "Fcr_pan", r5(_Fcr), "MPa")
phiPn_pan = E.paso("B3", "phiPn_pan", r5(_phiPn), "kN")
phiTn_pan = E.paso("B3", "phiTn_pan", r5(phi_t * Fy * A_pan / 1000.0), "kN")

crece_area = E.paso("B4", "crece_area", r5(A_pan / A_ilus), "—")

# ====== C · §8.6.2: el 30 % traccionado, y por qué la X lo cumple sola =======
V_linea = E.paso("C1", "V_linea", r5(F_diaf_X / n_lineas), "kN")
V_panel = E.paso("C1", "V_panel", r5(V_linea / (n_paneles / n_lineas)), "kN")
dif_col = E.paso("C1", "dif_col", r5(abs(V_panel - F_col_alero)), "kN")

cos_diag = E.paso("C2", "cos_diag", r5(s_marco * 1e3 / L_diag), "—")
N_diag = E.paso("C2", "N_diag", r5(0.5 * V_panel / cos_diag), "kN")
uso_diag_comp = E.paso("C2", "uso_diag_comp", r5(N_diag / phiPn_pan), "—")
uso_diag_trac = E.paso("C2", "uso_diag_trac", r5(N_diag / phiTn_pan), "—")

frac_trac = E.paso("C3", "frac_trac", r5(0.5), "—")
uso_862 = E.paso("C3", "uso_862", r5(frac_traccion / frac_trac), "—")
V_trac_min = E.paso("C3", "V_trac_min", r5(frac_traccion * V_linea), "kN")

# ============ D · la rigidez, que es una cota que el 12 dejó puesta ==========
k_pan_ilus = E.paso("D1", "k_pan_ilus",
                    r5(2 * E_ac * A_ilus * (s_marco * 1e3) ** 2 / L_diag ** 3), "kN/m")
k_pan = E.paso("D1", "k_pan",
               r5(2 * E_ac * A_pan * (s_marco * 1e3) ** 2 / L_diag ** 3), "kN/m")
uso_kbr_13 = E.paso("D2", "uso_kbr_13", r5(k_pan / kbr_lim), "—")
crece_k = E.paso("D2", "crece_k", r5(k_pan / k_pan_ilus), "—")

# ===== E · el colector y la acumulación, los dos encargos del 11 y el 12 =====
uso_col_pan = E.paso("E1", "uso_col_pan", r5(F_col_12 / phiTn_pan), "—")
N_acum_diag = E.paso("E2", "N_acum_diag", r5(Pbr_acum / cos_diag), "kN")
uso_acum = E.paso("E2", "uso_acum", r5(N_acum_diag / phiPn_pan), "—")
veces_sismo = E.paso("E2", "veces_sismo", r5(Pbr_acum / V_panel), "—")

# ========= F · el anclaje: la condición de la que cuelga `R = 5` =============
M_ancl_min = E.paso("F1", "M_ancl_min", r5(frac_Mpe_base * Mpe_col), "kN·m")
veces_Mbase = E.paso("F1", "veces_Mbase", r5(M_ancl_min / Mbase_u), "—")
M_ancl = E.paso("F1", "M_ancl", r5(max(M_ancl_min, Mbase_u)), "kN·m")

d_umbral = E.paso("F2", "d_umbral", r5(long_exp_min / n_diam_exp), "mm")

V_base_amp = E.paso("F3", "V_base_amp", r5(kcap_X * V_linea / (n_bases / n_lineas)), "kN")
uso_exento = E.paso("F3", "uso_exento", r5(V_base_amp / corte_exento), "—")

# ------------------------------------------------------------ Sale
# El 13 es el último de la serie: no hay `heredan`.
E.sale("lam_md", lam_md, "—", paso="A1")
E.sale("B_pan", B_pan, "mm", paso="S1")
E.sale("t_pan", t_pan, "mm", paso="S1")
E.sale("A_pan", A_pan, "mm2", paso="B1")
E.sale("esb_pan", esb_pan, "—", paso="B2")
E.sale("phiPn_pan", phiPn_pan, "kN", paso="B3")
E.sale("k_pan", k_pan, "kN/m", paso="D1")
E.sale("N_diag", N_diag, "kN", paso="C2")
E.sale("M_ancl", M_ancl, "kN·m", paso="F1")
E.sale("d_umbral", d_umbral, "mm", paso="F2")

# Sin oráculo: este eslabón no tiene memo previo que reproducir. Es lo que el
# lote E significa, y por eso `publicado` va vacío a propósito.
E.publicado({})

if __name__ == "__main__":
    raise SystemExit(main(sys.argv, E))
