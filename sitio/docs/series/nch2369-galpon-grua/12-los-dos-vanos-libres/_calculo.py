"""Eslabón 12 — los dos vanos libres: la irregularidad torsional cae entre las
dos lecturas del mismo edificio, y el umbral de §5.2.2 pasa justo por el medio.

    python sitio/docs/series/nch2369-galpon-grua/12-los-dos-vanos-libres/_calculo.py [salida]

Hereda de los nueve eslabones anteriores que le prometieron algo —01, 02, 03, 04,
05, 06, 07, 10 y 11— con **51 símbolos**, la tabla `## Entra` mas larga de la
serie. Transcrito del memo 12 de `Guias_Interactivas`, que leyó las cláusulas del
PDF (ver la tabla de referencias de `index.md`).

Cuatro cosas que este eslabón hace:

* **El título es engañoso y el propio memo lo dice.** Los dos vanos arriostrados
  son los **extremos**, así que la excentricidad de rigidez es cero y los dos
  vanos libres no producen torsión. La produce **dónde se estaciona la grúa**.
* **La irregularidad torsional cae entre las dos lecturas del mismo edificio**:
  1,120 con el modelo tridimensional y 1,384 con modelos planos, una a cada lado
  del umbral de 1,20. La diferencia no es una hipótesis de carga ni una sección:
  es si el modelo tiene o no tiene la otra dirección adentro.
* **La clasificación del diafragma es una obligación normativa** que el 11 hizo
  sin citar la cláusula, y su criterio se **invierte**: hay una rigidez *máxima*
  de panel compatible con diafragma rígido, no una mínima.
* **El `k_esc` del 10 tiene acá su primera consecuencia desfavorable**: rigidizar
  el marco transversal empeora la irregularidad torsional, y casi duplica el
  exceso sobre 1.

**Todos los pasos se redondean a cinco decimales.** Las 15 filas del `## Resumen`
van en `E.resumen()`. Dos cifras de la prosa del memo no reproducen y están en
`## Límites`:

   T_estac_min   el mínimo local de la rampa está en 0,0764878 s, que redondea a
                 0,07649; el memo publica 0,07650. La ordenada es la misma a
                 cinco decimales (0,35404 g), así que no cambia nada.
   d_riel_11     el memo consume 0,93897 mm del 11, que es la cifra que aquel
                 publicó; la aritmética del 11 sobre sus propias cifras impresas
                 da 0,93896. Se consume la impresa, como manda la regla, y el
                 hallazgo está anotado en el `## Límites` del 11.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from serie import Eslabon, main  # noqa: E402

E = Eslabon("nch2369-galpon-grua", orden=12, slug="los-dos-vanos-libres",
            titulo="Los dos vanos libres",
            normas=["NCh2369:2025", "NCh433:2026", "AISC 360-22",
                    "AIST TR-13:2021"],
            carpeta=AQUI)


def r5(x: float) -> float:
    return math.floor(float(x) * 1e5 + 0.5) / 1e5


def r2(x: float) -> float:
    return math.floor(float(x) * 1e2 + 0.5) / 1e2


# ------------------------------------------------------------ lo que entra
I_imp = E.entra("I", de="01", paso="A1")
L_luz = E.entra("L_luz", de="01", paso="S1")
s_marco = E.entra("s_marco", de="01", paso="S1")
h_libre = E.entra("h_libre", de="01", paso="S1")
h_riel = E.entra("h_riel", de="01", paso="S3")
R_T7 = E.entra("R_T7", de="01", paso="D1")
xi = E.entra("xi", de="01", paso="D1")
S_pend = E.entra("S_pend", de="02", paso="C2")
Wb_puente = E.entra("Wb_puente", de="03", paso="S2")
Wt_carro = E.entra("Wt_carro", de="03", paso="S2")
wb_ruedas = E.entra("wb_ruedas", de="03", paso="S2")
Rw_max = E.entra("Rw_max", de="03", paso="B2")
Rw_min = E.entra("Rw_min", de="03", paso="B3")
T_long = E.entra("T_long", de="03", paso="E1")
ArS = E.entra("ArS", de="04", paso="A3")
r_s = E.entra("r_s", de="04", paso="A2")
T_0 = E.entra("T_0", de="04", paso="A2")
p_suelo = E.entra("p_suelo", de="04", paso="A2")
q_s = E.entra("q_s", de="04", paso="A2")
f_xi = E.entra("f_xi", de="04", paso="B1")
Cr_T1 = E.entra("Cr_T1", de="04", paso="C2")
T_star_X = E.entra("T_star_X", de="04", paso="S2")
T_star_Y = E.entra("T_star_Y", de="04", paso="S2")
R_star_X = E.entra("R_star_X", de="04", paso="C4")
R_star_Y = E.entra("R_star_Y", de="04", paso="C5")
Sa_ref_X = E.entra("Sa_ref_X", de="04", paso="C4")
W_edificio = E.entra("W_edificio", de="05", paso="A3")
Wgrua_sc = E.entra("Wgrua_sc", de="05", paso="C3")
P_sismico = E.entra("P_sismico", de="05", paso="C4")
C_dis = E.entra("C_dis", de="05", paso="D3")
Q0_X = E.entra("Q0_X", de="05", paso="D5")
Q0_Y = E.entra("Q0_Y", de="05", paso="D5")
d_lim = E.entra("d_lim", de="06", paso="E1")
dlim_grua = E.entra("dlim_grua", de="06", paso="E5")
k_Y = E.entra("k_Y", de="07", paso="S1")
k_riel = E.entra("k_riel", de="07", paso="S1")
T_star_Y2 = E.entra("T_star_Y2", de="07", paso="B5")
d_Y2 = E.entra("d_Y2", de="07", paso="C5")
f_PDelta_Y2 = E.entra("f_PDelta_Y2", de="07", paso="C6")
SS_marco = E.entra("SS_marco", de="07", paso="C1")
e_col_riel = E.entra("e_col_riel", de="10", paso="A2")
h_asiento = E.entra("h_asiento", de="10", paso="A2")
w_col_10 = E.entra("w_col_10", de="10", paso="B5")
k_esc = E.entra("k_esc", de="10", paso="D6")
b_pan_techo = E.entra("b_pan_techo", de="11", paso="C3")
L_diag_techo = E.entra("L_diag_techo", de="11", paso="C3")
kd_vano = E.entra("kd_vano", de="11", paso="D2")
f_marco_grua = E.entra("f_marco_grua", de="11", paso="D2")
F_diaf_X = E.entra("F_diaf_X", de="11", paso="D1")
F_col_alero = E.entra("F_col_alero", de="11", paso="D1")
A_punt_techo = E.entra("A_punt_techo", de="11", paso="E2")

# ------------------------------------------------------------ el caso
n_vanos = E.caso("n_vanos", 4, "—")
n_marcos = E.caso("n_marcos", 5, "—")
n_paneles = E.caso("n_paneles", 4, "—")            # dos vanos × dos muros
h_tope = E.caso("h_tope", 12.00, "m")              # §5.2.2, el tope de altura
tope_masa = E.caso("tope_masa", 1.50, "—")         # §5.2.2, la razón de masas
tope_tors = E.caso("tope_tors", 1.20, "—")         # §5.2.2, la razón de derivas
tope_diaf = E.caso("tope_diaf", 2.00, "—")         # §5.3.3, el factor de la Figura 1
e_acc_frac = E.caso("e_acc_frac", 0.10, "—")       # NCh433 §6.2.8
holgura_tope = E.caso("holgura_tope", 0.30, "m")   # tope y holgura del puente (S3)
E_ac = E.caso("E_ac", 200000.0, "MPa")
Fy = E.caso("Fy", 345.0, "MPa")
phi_c = E.caso("phi_c", 0.90, "—")
c_658 = E.caso("c_658", 0.658, "—")
A_diag_pan = E.caso("A_diag_pan", 2400.0, "mm2")   # el panel ilustrativo (S1)
B_punt = E.caso("B_punt", 200.0, "mm")
t_punt = E.caso("t_punt", 6.0, "mm")
R_min = E.caso("R_min", 1.50, "—")                 # la cota de R* en el origen
# La deriva del riel que el 11 · D2 publicó. Su propia aritmética sobre las
# cifras impresas da 0,93896; se consume la impresa. Ver `## Limites`.
d_riel_11 = E.caso("d_riel_11", 0.93897, "mm")

# ============ A · el método de análisis que once eslabones dieron por sentado ==
h_cumb = E.paso("A1", "h_cumb", r5(h_libre + L_luz / (2 * S_pend)), "m")
uso_h_cumb = E.paso("A1", "uso_h_cumb", r5(h_cumb / h_tope), "—")
uso_h_alero = E.paso("A1", "uso_h_alero", r5(h_libre / h_tope), "—")

raz_masa = E.paso("A3", "raz_masa", r5(W_edificio / Wgrua_sc), "—")
uso_masa = E.paso("A3", "uso_masa", r5(raz_masa / tope_masa), "—")
raz_piso = E.paso("A4", "raz_piso", r5(k_riel / k_Y), "—")

# ===== B · el diafragma, que §5.3.3 obliga a clasificar =======================
L_total = E.paso("B1", "L_total", r5(n_vanos * s_marco), "m")
GA_eq = E.paso("B1", "GA_eq", r5(kd_vano * s_marco), "kN")

w_x = E.paso("B3", "w_x", r5(Q0_X / L_total), "kN/m")
R_br = E.paso("B3", "R_br", r5(Q0_X / 2.0), "kN")
x_br = E.paso("B3", "x_br", r5(s_marco / 2.0), "m")     # eje del vano arriostrado
L_diaf = E.paso("B3", "L_diaf", r5(L_total - 2 * x_br), "m")
# La integral del corte de la viga de cortante, con los dos voladizos adentro:
# el memo la imprime en cuatro terminos y los dos de carga usan el `w_x` impreso.
MDD = E.paso("B3", "MDD",
             r5((R_br * (L_total / 2.0) - R_br * x_br
                 - w_x * (L_total / 2.0) ** 2 / 2.0 + w_x * x_br ** 2 / 2.0)
                / GA_eq * 1000.0), "mm")

kbr_max = E.paso("B4", "kbr_max", r2(R_br / MDD * 1000.0), "kN/m")

Ld_pan = E.paso("B5", "Ld_pan",
                r2(math.hypot(s_marco * 1e3, h_libre * 1e3)), "mm")
# El memo escribe la rigidez del panel con el vano y la diagonal **en metros
# cuadrados**, y sustituye los dos cuadrados impresos: con la diagonal sin
# redondear daria 25 134,61 y no el 25 134,62 que publica.
b_pan_m2 = E.paso("B5", "b_pan_m2", r2(s_marco ** 2), "m2")
Ld_pan_m2 = E.paso("B5", "Ld_pan_m2", r2((Ld_pan / 1e3) ** 2), "m2")
k_pan = E.paso("B5", "k_pan",
               r2(2 * E_ac * A_diag_pan * b_pan_m2 / (Ld_pan_m2 * Ld_pan)), "kN/m")
factor_diaf = E.paso("B5", "factor_diaf", r5(kbr_max / k_pan), "—")
factor_diaf_Y = E.paso("B6", "factor_diaf_Y",
                       r5(f_marco_grua / (1.0 / n_marcos)), "—")

# ================ C · la torsión en planta, que es lo único que decide ========
kY_ef = E.paso("C1", "kY_ef", r5(k_Y * k_esc), "kN/m")
x_CR = E.paso("C1", "x_CR", r5(L_total / 2.0), "m")   # por simetria
y_CR = E.paso("C1", "y_CR", r5(L_luz / 2.0), "m")
sum_x2 = E.paso("C2", "sum_x2",
                r5(2 * (2 * s_marco) ** 2 + 2 * s_marco ** 2), "m2")
sum_y2 = E.paso("C2", "sum_y2", r5(n_paneles * (L_luz / 2.0) ** 2), "m2")
brazo_Y = E.paso("C2", "brazo_Y", r5(n_marcos * (2 * s_marco)), "m")
brazo_X = E.paso("C2", "brazo_X", r5(n_paneles * (L_luz / 2.0)), "m")

x_g_tope = E.paso("C3", "x_g_tope", r5(wb_ruedas / 2.0 + holgura_tope), "m")
x_CM = E.paso("C3", "x_CM",
              r5((W_edificio * (L_total / 2.0) + Wgrua_sc * x_g_tope) / P_sismico), "m")
e_tors = E.paso("C3", "e_tors", r5(L_total / 2.0 - x_CM), "m")
e_rel = E.paso("C3", "e_rel", r5(e_tors / L_total), "—")
pct_grua = E.paso("C3", "pct_grua", r5(100.0 * Wgrua_sc / P_sismico), "%")


def razon(brazo, e, suma_propia, suma_cruzada, rho):
    """`δmáx/δprom` con forma cerrada: traslación más giro."""
    return 1.0 + brazo * e / (suma_propia + suma_cruzada * rho)


rho_pan = E.paso("C4", "rho_pan", r5(k_pan / kY_ef), "—")
raz_tors_Y = E.paso("C4", "raz_tors_Y",
                    r5(razon(brazo_Y, e_tors, sum_x2, sum_y2, rho_pan)), "—")
# La misma C4 leida como cociente entre los dos marcos extremos, que es lo que
# el modelo del sitio entrega directo: `delta_prom` es la traslacion, asi que
# `delta_1/delta_5 = (1+d)/(1-d)` con `d = raz_tors_Y - 1`.
raz_extremos = E.paso("C4", "raz_extremos",
                      r5(raz_tors_Y / (2.0 - raz_tors_Y)), "—")
raz_tors_plano = E.paso("C5", "raz_tors_plano",
                        r5(razon(brazo_Y, e_tors, sum_x2, sum_y2, 0.0)), "—")

rho_lim = E.paso("C6", "rho_lim",
                 r5((brazo_Y * e_tors / (tope_tors - 1.0) - sum_x2) / sum_y2), "—")
kbr_lim = E.paso("C6", "kbr_lim", r5(rho_lim * kY_ef), "kN/m")
uso_kbr = E.paso("C6", "uso_kbr", r5(k_pan / kbr_lim), "—")

rho_sin_esc = E.paso("C7", "rho_sin_esc", r5(rho_pan * k_esc), "—")
raz_sin_esc = E.paso("C7", "raz_sin_esc",
                     r5(razon(brazo_Y, e_tors, sum_x2, sum_y2, rho_sin_esc)), "—")
crece_esc = E.paso("C7", "crece_esc",
                   r5((raz_tors_Y - 1.0) / (raz_sin_esc - 1.0)), "—")

e_acc = E.paso("C8", "e_acc", r5(e_acc_frac * L_total), "m")
veces_acc = E.paso("C8", "veces_acc", r5(e_acc / e_tors), "—")
den_tors = E.paso("C8", "den_tors", r5(sum_x2 + sum_y2 * rho_pan), "m2")
raz_tors_acc = E.paso("C8", "raz_tors_acc",
                      r5(1.0 + brazo_Y * (e_tors + e_acc) / den_tors), "—")

x_g_crit = E.paso("C9", "x_g_crit",
                  r5(L_total / 2.0 - (tope_tors - 1.0) * sum_x2 / brazo_Y
                     * (P_sismico / Wgrua_sc)), "m")
nave_prohibida = E.paso("C9", "nave_prohibida",
                        r5(2 * x_g_crit / L_total), "—")

d_ext = E.paso("C10", "d_ext", r5(d_Y2 * raz_tors_Y), "mm")
uso_deriva_ext = E.paso("C10", "uso_deriva_ext", r5(d_ext / d_lim), "—")
d_riel_ext = E.paso("C10", "d_riel_ext", r5(d_riel_11 * raz_tors_Y), "mm")
uso_riel_tors = E.paso("C10", "uso_riel_tors", r5(d_riel_ext / dlim_grua), "—")

# ==================== D · el colector que cruza el portón =====================
w_al = E.paso("D1", "w_al", r5(F_diaf_X / (2 * L_total)), "kN/m")
N_col_vano = E.paso("D1", "N_col_vano", r5(w_al * s_marco), "kN")
N_col_ext = E.paso("D1", "N_col_ext", r5(F_diaf_X / n_vanos), "kN")

frac_testero = E.paso("D2", "frac_testero", r5(Rw_max / (Rw_max + Rw_min)), "—")
y_grua = E.paso("D2", "y_grua", r5((1.0 - frac_testero) * L_luz), "m")
y_CM = E.paso("D2", "y_CM",
              r5((W_edificio * (L_luz / 2.0) + Wgrua_sc * y_grua) / P_sismico), "m")
e_x = E.paso("D2", "e_x", r5(L_luz / 2.0 - y_CM), "m")
menor_que_Y = E.paso("D2", "menor_que_Y", r5(e_tors / e_x), "—")

raz_tors_X = E.paso("D3", "raz_tors_X",
                    r5(razon(brazo_X, e_x, sum_y2, sum_x2, 1.0 / rho_pan)), "—")
F_col_12 = E.paso("D3", "F_col_12", r5(F_col_alero * raz_tors_X), "kN")

T_linea = E.paso("D4", "T_linea", r5(T_long / 2.0), "kN")
veces_traccion = E.paso("D4", "veces_traccion", r5(F_col_12 / T_linea), "—")

I_punt = (B_punt ** 4 - (B_punt - 2 * t_punt) ** 4) / 12.0
r_punt = E.paso("D5", "r_punt", r5(math.sqrt(I_punt / A_punt_techo)), "mm")
sl_punt = s_marco * 1e3 / r_punt
esb_punt = E.paso("D5", "esb_punt", r5(sl_punt), "—")
Fe_punt_ex = math.pi ** 2 * E_ac / sl_punt ** 2
Fe_punt = E.paso("D5", "Fe_punt", r5(Fe_punt_ex), "MPa")
razon_punt = E.paso("D5", "razon_punt", r5(Fy / Fe_punt_ex), "—")
Fcr_punt_ex = c_658 ** (Fy / Fe_punt_ex) * Fy
Fcr_punt = E.paso("D5", "Fcr_punt", r5(Fcr_punt_ex), "MPa")
phiPn_punt = E.paso("D5", "phiPn_punt",
                    r5(phi_c * Fcr_punt_ex * A_punt_techo / 1000.0), "kN")
uso_colector = E.paso("D5", "uso_colector", r5(F_col_12 / phiPn_punt), "—")

# ========== E · el período con que se calcula R*, que no decide nada ==========
def SaH(T: float) -> float:
    """El espectro horizontal de referencia de §5.4.1, sin `R*`."""
    return ArS * (1 + r_s * (T / T_0) ** p_suelo) / (1 + (T / T_0) ** q_s)


def R_estrella(T: float) -> float:
    """La rampa de §5.4.1: de `R_min` en el origen a `R_T7` en `Cr_T1`."""
    return R_min + (R_T7 - R_min) * min(T, Cr_T1) / Cr_T1


def Sa(T: float) -> float:
    return I_imp * SaH(T) * f_xi / R_estrella(T)


def estacionarios(n: int = 280001) -> tuple[float, float]:
    """Los dos puntos estacionarios interiores de la rampa, por barrido."""
    ts = [i * Cr_T1 / (n - 1) for i in range(1, n)]
    v = [Sa(t) for t in ts]
    tmin = tmax = 0.0
    for i in range(1, len(ts) - 1):
        if v[i] < v[i - 1] and v[i] <= v[i + 1]:
            tmin = ts[i]
        if v[i] > v[i - 1] and v[i] >= v[i + 1]:
            tmax = ts[i]
    return tmin, tmax


_tmin, _tmax = estacionarios()
T_estac_min = E.paso("E2", "T_estac_min", r5(_tmin), "s")
T_estac_max = E.paso("E2", "T_estac_max", r5(_tmax), "s")

R_en_max = E.paso("E2", "R_en_max", r5(R_estrella(T_estac_max)), "—")
SaH_max = E.paso("E2", "SaH_max", r5(SaH(T_estac_max)), "g")
Sa_max = E.paso("E2", "Sa_max", r5(I_imp * SaH_max * f_xi / R_en_max), "g")
R_en_min = E.paso("E2", "R_en_min", r5(R_estrella(T_estac_min)), "—")
SaH_min = E.paso("E2", "SaH_min", r5(SaH(T_estac_min)), "g")
Sa_min = E.paso("E2", "Sa_min", r5(I_imp * SaH_min * f_xi / R_en_min), "g")

Sa_TX = E.paso("E2b", "Sa_TX", r5(I_imp * Sa_ref_X * f_xi / R_star_X), "g")
cerca_max = E.paso("E2", "cerca_max", r5(Sa_TX / Sa_max), "—")
sube_del_min = E.paso("E2", "sube_del_min", r5(Sa_max / Sa_min), "—")
sobre_recorte_X = E.paso("E2b", "sobre_recorte_X", r5(Sa_TX / r5(C_dis)), "—")
Sa_cero = E.paso("E2b", "Sa_cero", r5(I_imp * ArS * f_xi / R_min), "g")
frac_del_origen = E.paso("E2b", "frac_del_origen", r5(Sa_TX / Sa_cero), "—")

Sa_frontera = E.paso("E2", "Sa_frontera",
                     r5(I_imp * SaH(Cr_T1) * f_xi / R_T7), "g")
SaH_05 = E.paso("E3", "SaH_05", r5(SaH(0.50)), "g")
Sa_05 = E.paso("E3", "Sa_05", r5(I_imp * SaH_05 * f_xi / R_star_Y), "g")
sobre_recorte = E.paso("E3", "sobre_recorte", r5(Sa_05 / r5(C_dis)), "—")


def borde_ventana(objetivo: float) -> float:
    """El período en que el espectro de diseño baja al coeficiente recortado."""
    lo, hi = Cr_T1, 5.0
    for _ in range(200):
        m = (lo + hi) / 2.0
        if I_imp * SaH(m) * f_xi / R_T7 > objetivo:
            lo = m
        else:
            hi = m
    return lo


# El memo sustituye el `C_dis` **impreso**, y con el exacto el borde se corre
# una milésima de milisegundo. Ver el patrón del lote B.
T_borde = E.paso("E4", "T_borde", r5(borde_ventana(r5(C_dis))), "s")
margen_Y = E.paso("E4", "margen_Y", r5(T_borde / T_star_Y2), "—")
margen_X = E.paso("E4", "margen_X", r5(T_borde / T_star_X), "—")

# ------------------------------------------------------------ Sale
E.sale("x_g_tope", x_g_tope, "m", paso="S3", heredan=["13"])
E.sale("e_tors", e_tors, "m", paso="C3", heredan=["13"])
E.sale("raz_tors_Y", raz_tors_Y, "—", paso="C4", heredan=["13"])
E.sale("raz_tors_X", raz_tors_X, "—", paso="D3", heredan=["13"])
E.sale("kbr_lim", kbr_lim, "kN/m", paso="C6", heredan=["13"])
E.sale("F_col_12", F_col_12, "kN", paso="D3", heredan=["13"])

E.publicado({
    "x_g_tope": "2,00", "e_tors": "2,88308", "raz_tors_Y": "1,11962",
    "raz_tors_X": "1,07637", "kbr_lim": "10469,46742", "F_col_12": "177,32963",
})

E.resumen({
    "uso_h_cumb": "1,08333", "uso_h_alero": "0,87500",
    "raz_masa": "3,50907", "raz_piso": "2,68300",
    "factor_diaf": "11,04259", "factor_diaf_Y": "1,07040",
    "raz_tors_Y": "1,11962", "raz_tors_plano": "1,38441",
    "raz_tors_acc": "1,24409", "uso_kbr": "2,40075",
    "uso_deriva_ext": "0,46369", "uso_riel_tors": "0,05607",
    "uso_colector": "0,23623", "veces_traccion": "4,12394",
    "sobre_recorte": "1,07702",
})

if __name__ == "__main__":
    raise SystemExit(main(sys.argv, E))
