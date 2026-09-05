"""Eslabón 05 — masa sísmica y carga suspendida: el 2,75 de la Ec. (13) es el
espectro evaluado en T_0, y al aplicar el techo los dos cortes basales quedan
iguales.

    python sitio/docs/series/nch2369-galpon-grua/05-masa-sismica-y-carga-suspendida/_calculo.py [salida]

Es el primer eslabón que hereda de cuatro: geometría del 01, nieve del 02, pesos
de la grúa del 03 y espectro del 04. Se arma el peso sísmico, se decide qué parte
de la grúa entra en él y se evalúan el corte basal de cada dirección contra el
piso de §5.12 y el techo de §5.13. Transcrito del memo 05 de `Guias_Interactivas`,
que leyó las cláusulas del PDF (ver la tabla de referencias de `index.md`).

Tres cosas que este eslabón hace y conviene no perder de vista al leerlo:

* **El techo de §5.13 usa el R de tabla, no el R\\***. Por eso los dos cortes de
  diseño quedan idénticos: la fila 5.5 le dio un solo R al edificio y el techo no
  distingue direcciones.
* **El 2,75 de la Ec. (13) es `(1 + r)/2`**, o sea la forma de la Ec. (3) evaluada
  en `T_0`. Exacto en los suelos A, B y C, donde `r = 4,50`; falso en el D y el E.
* **La nieve no entra en la masa sísmica por un criterio adoptado** (S4), no por
  una cláusula: §5.1.2 no la nombra. El umbral de 1,44 kN/m² viene de la práctica
  norteamericana y entra como supuesto.

Un hallazgo de la migración: el memo imprimió `k_req_Y = 5216,93102` donde el
valor es 5 216,931030 —el último dígito truncado en vez de redondeado—, y su arnés
no lo vio porque comparaba con tolerancia relativa. Acá la tolerancia es absoluta.

Cinco pasos del memo sustituyen cifras **impresas** y no exactas: los dos cortes
del análisis usan las ordenadas de diseño del 04 con sus cinco decimales, el techo
de §5.13 usa la corrección por amortiguamiento con los suyos, la fuerza inercial
de la grúa usa el coeficiente de diseño con los suyos y el corte amplificado usa el
corte de diseño con los suyos. Se reproducen con ese
redondeo, que es lo que el memo escribió en su fórmula.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from serie import Eslabon, main  # noqa: E402

E = Eslabon("nch2369-galpon-grua", orden=5, slug="masa-sismica-y-carga-suspendida",
            titulo="Masa sísmica y carga suspendida",
            normas=["NCh2369:2025", "AIST TR-13:2021", "NCh431:2010"], carpeta=AQUI)

# ------------------------------------------------------------ lo que entra
L_luz = E.entra("L_luz", de="01", paso="S1")
s_marco = E.entra("s_marco", de="01", paso="S1")
h_libre = E.entra("h_libre", de="01", paso="S1")
p_g = E.entra("p_g", de="02", paso="A1")
p_f = E.entra("p_f", de="02", paso="B4")
S_pend = E.entra("S_pend", de="02", paso="C2")
Wb_puente = E.entra("Wb_puente", de="03", paso="S2")
Wt_carro = E.entra("Wt_carro", de="03", paso="S2")
A_r = E.entra("A_r", de="04", paso="A1")
S_suelo = E.entra("S_suelo", de="04", paso="A2")
r_s = E.entra("r_s", de="04", paso="A2")
T_1 = E.entra("T_1", de="04", paso="A2")
f_xi = E.entra("f_xi", de="04", paso="B1")
Cr_T1 = E.entra("Cr_T1", de="04", paso="C2")
T_star_X = E.entra("T_star_X", de="04", paso="S2")
T_star_Y = E.entra("T_star_Y", de="04", paso="S2")
R_star_X = E.entra("R_star_X", de="04", paso="C4")
R_star_Y = E.entra("R_star_Y", de="04", paso="C5")
Sa_dis_X = E.entra("Sa_dis_X", de="04", paso="C6")
Sa_dis_Y = E.entra("Sa_dis_Y", de="04", paso="C6")

# ------------------------------------------------------------ el caso
n_vanos = E.caso("n_vanos", 4, "—")                 # del 01
n_marcos = E.caso("n_marcos", 5, "—")               # del 01
g_cubierta = E.caso("g_cubierta", 0.12, "kN/m2")    # S1, cubierta y aislación
g_muros = E.caso("g_muros", 0.10, "kN/m2")          # S1, revestimiento
w_columna = E.caso("w_columna", 1.75, "kN/m")       # S1
n_columnas = E.caso("n_columnas", 10, "—")          # S1
w_carrilera = E.caso("w_carrilera", 1.20, "kN/m")   # S1
L_carrilera = E.caso("L_carrilera", 60.0, "m")      # S1, dos líneas de 30 m
g_techo_kg = E.caso("g_techo_kg", 38.0, "kg/m2")    # del 01, S4
P_eq = E.caso("P_eq", 12.0, "kN")                   # del 01, S5, por marco
g_grav = E.caso("g_grav", 9.81, "m/s2")
I = E.caso("I", 1.00, "—")                          # del 01, Categoría II
R_T7 = E.caso("R_T7", 5, "—")                       # del 01, la fila 5.5
k_amp = E.caso("k_amp", 0.70, "—")                  # del 01, §8.3.4
r_D = E.caso("r_D", 3.50, "—")                      # Tabla 6, el suelo de la otra serie
p_nieve_lim = E.caso("p_nieve_lim", 1.44, "kN/m2")  # S4, el umbral adoptado
frac_nieve = E.caso("frac_nieve", 0.20, "—")        # S4, la fracción que entraría
p_g_normal = E.caso("p_g_normal", 0.25, "kN/m2")    # NCh431 §4
h_turno = E.caso("h_turno", 4, "h")                 # del 03, S4
h_dia_total = E.caso("h_dia_total", 24, "h")
mu_roce = E.caso("mu_roce", 0.60, "—")              # AIST §3.11.2, con frenos aplicados
t32_tra = E.caso("t32_tra", 0.20, "—")              # del 03, tracción de ruedas motrices
c_min = E.caso("c_min", 0.25, "—")                  # Ec. (12), el piso
c_max = E.caso("c_max", 2.75, "—")                  # Ec. (13), el techo
k_prel_Y_d = E.caso("k_prel_Y_d", 4730.10, "kN/m")  # la sección preliminar del arnés del 04

# ------------------------------------------------------------ A · las áreas
L_largo = E.paso("A1", "L_largo", n_vanos * s_marco, "m")
h_cumb = E.paso("A1", "h_cumb", (L_luz / 2.0) / S_pend, "m")
A_planta = E.paso("A2", "A_planta", L_luz * L_largo, "m2")
A_muros = E.paso("A2", "A_muros",
                 2 * L_largo * h_libre + 2 * L_luz * h_libre + L_luz * h_cumb, "m2")
A_frontones = E.paso("A2", "A_frontones", L_luz * h_cumb, "m2")
g_techo = E.paso("A3", "g_techo", g_techo_kg * g_grav / 1000.0, "kN/m2")
W_edificio = E.paso("A3", "W_edificio",
                    g_techo * A_planta + g_cubierta * A_planta + g_muros * A_muros
                    + w_columna * h_libre * n_columnas + w_carrilera * L_carrilera
                    + P_eq * n_marcos, "kN")

# ------------------------------------------------------------ B · las sobrecargas que no entran
n_filas = E.paso("B1", "n_filas", 4 - 1, "—")
raz_normal = E.paso("B2", "raz_normal", p_g / p_g_normal, "—")
raz_nieve = E.paso("B2", "raz_nieve", p_f / p_nieve_lim, "—")
W_nieve = E.paso("B2", "W_nieve", frac_nieve * p_f * A_planta, "kN")

# ------------------------------------------------------------ C · la grúa
frac_turno = E.paso("C1", "frac_turno", h_turno / h_dia_total, "—")
n_condiciones = E.paso("C2", "n_condiciones", 2, "—")
Wgrua_sc = E.paso("C3", "Wgrua_sc", Wb_puente + Wt_carro, "kN")
P_sismico = E.paso("C4", "P_sismico", W_edificio + Wgrua_sc, "kN")
frac_grua = E.paso("C4", "frac_grua", Wgrua_sc / P_sismico, "—")

# ------------------------------------------------------------ D · el corte basal
# el memo multiplica el peso por las ordenadas **impresas** del 04, a cinco decimales
Sa_dis_X_pub = E.paso("D1", "Sa_dis_X_pub", round(Sa_dis_X, 5), "g")
Sa_dis_Y_pub = E.paso("D1", "Sa_dis_Y_pub", round(Sa_dis_Y, 5), "g")
Q0_X_an = E.paso("D1", "Q0_X_an", Sa_dis_X_pub * P_sismico, "kN")
Q0_Y_an = E.paso("D1", "Q0_Y_an", Sa_dis_Y_pub * P_sismico, "kN")
Q0_min = E.paso("D2", "Q0_min", c_min * I * A_r * S_suelo * P_sismico, "kN")
holgura_Y = E.paso("D2", "holgura_Y", Q0_Y_an / Q0_min, "—")
holgura_X = E.paso("D2", "holgura_X", Q0_X_an / Q0_min, "—")
forma_T0_C = E.paso("D3", "forma_T0_C", (1 + r_s) / 2.0, "—")
f_xi_pub = E.paso("D3", "f_xi_pub", round(f_xi, 5), "—")     # el memo escribe 1,44270
Q0_max = E.paso("D3", "Q0_max",
                c_max * I * A_r * S_suelo / (R_T7 + 1) * f_xi_pub * P_sismico, "kN")
C_dis = E.paso("D3", "C_dis", Q0_max / P_sismico, "—")
forma_T0_D = E.paso("D4", "forma_T0_D", (1 + r_D) / 2.0, "—")
exceso_D = E.paso("D4", "exceso_D", c_max / forma_T0_D, "—")
super_X = E.paso("D5", "super_X", Q0_X_an / Q0_max, "—")
super_Y = E.paso("D5", "super_Y", Q0_Y_an / Q0_max, "—")
Q0_dis = E.paso("D5", "Q0_dis", min(Q0_X_an, Q0_Y_an, Q0_max), "kN")

# ------------------------------------------------------------ E · cuánto de la grúa llega
# el memo multiplica el coeficiente **impreso** de D3, a cinco decimales
C_dis_pub = E.paso("E1", "C_dis_pub", round(C_dis, 5), "—")
F_grua = E.paso("E1", "F_grua", C_dis_pub * Wgrua_sc, "kN")
T_trac = E.paso("E1", "T_trac", t32_tra * Wgrua_sc, "kN")
T_roce = E.paso("E1", "T_roce", mu_roce * Wgrua_sc, "kN")
exc_trac = E.paso("E2", "exc_trac", F_grua / T_trac, "—")
uso_roce = E.paso("E2", "uso_roce", F_grua / T_roce, "—")

# ------------------------------------------------------------ F · R1 y la rigidez que se pide
R1_X = E.paso("F1", "R1_X", R_star_X * min(holgura_X, 1.0), "—")
R1_Y = E.paso("F1", "R1_Y", R_star_Y * min(holgura_Y, 1.0), "—")
kcap_X = E.paso("F2", "kcap_X", k_amp * R1_X, "—")
kcap_Y = E.paso("F2", "kcap_Y", k_amp * R1_Y, "—")
# el memo amplifica el corte **impreso**, a cinco decimales
Q0_dis_pub = E.paso("F2", "Q0_dis_pub", round(Q0_dis, 5), "kN")
Q_amp_Y = E.paso("F2", "Q_amp_Y", kcap_Y * Q0_dis_pub, "kN")
k_req_Y = E.paso("F3", "k_req_Y",
                 P_sismico / (n_marcos * g_grav) * (2 * math.pi / T_star_Y) ** 2, "kN/m")
raz_k = E.paso("F3", "raz_k", k_req_Y / k_prel_Y_d, "—")

# ------------------------------------------------------------ Sale
E.sale("A_planta", A_planta, "m2", paso="A2", heredan=["06", "11"])
E.sale("A_muros", A_muros, "m2", paso="A2", heredan=["06"])
E.sale("W_edificio", W_edificio, "kN", paso="A3", heredan=["06", "11", "12"])
E.sale("Wgrua_sc", Wgrua_sc, "kN", paso="C3", heredan=["06", "12"])
E.sale("P_sismico", P_sismico, "kN", paso="C4", heredan=["06", "07", "12"])
E.sale("C_dis", C_dis, "—", paso="D3", heredan=["06", "11", "12"])
E.sale("Q0_X", Q0_dis, "kN", paso="D5", heredan=["06", "11", "12"])
E.sale("Q0_Y", Q0_dis, "kN", paso="D5", heredan=["06", "07", "12"])
E.sale("R1_X", R1_X, "—", paso="F1", heredan=["13"])
E.sale("R1_Y", R1_Y, "—", paso="F1", heredan=["07"])
E.sale("kcap_X", kcap_X, "—", paso="F2", heredan=["11", "13"])
E.sale("kcap_Y", kcap_Y, "—", paso="F2", heredan=["07"])
E.sale("k_prel_Y", k_prel_Y_d, "kN/m", paso="F3", heredan=["07"])
E.sale("k_req_Y", k_req_Y, "kN/m", paso="F3", heredan=["07"])

# lo que el memo 05 de Guias_Interactivas imprimió en su `## Sale`
E.publicado({
    "A_planta": "750,00000", "A_muros": "1217,50000", "W_edificio": "807,08500",
    "Wgrua_sc": "230,00000", "P_sismico": "1037,08500", "C_dis": "0,29161",
    "Q0_X": "302,41994", "Q0_Y": "302,41994", "R1_X": "4,00000", "R1_Y": "5,00000",
    "kcap_X": "2,80000", "kcap_Y": "3,50000",
    "k_prel_Y": "4730,10000",
    # el memo imprimió `5216,93102` y el valor es 5 216,931030: su último dígito
    # está truncado, no redondeado. El arnés del repo de memos comparaba con
    # tolerancia **relativa** (6e-6 sobre la magnitud) y no lo veía; acá la
    # tolerancia es absoluta, media unidad del último decimal, así que el oráculo
    # se escribe con los cuatro decimales que el memo sí acertó.
    "k_req_Y": "5216,9310",
})

if __name__ == "__main__":
    raise SystemExit(main(sys.argv, E))
