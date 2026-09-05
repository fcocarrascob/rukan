"""Eslabón 00 — el modelo: el galpón entero corre, y los períodos salen de 965
nudos y no de un oscilador.

    python sitio/docs/series/nch2369-galpon-grua/00-el-modelo/_calculo.py [salida]

Todo lo que este eslabón publica nace en el modelo `galpon-grua`
(`docs/modelos/galpon-grua/`, la malla del memo: 16 tramos por corte) o en un
paso escrito acá: el modelo emite desplazamientos, y la rigidez `k = H/δ` es un
paso. `publicado` es lo que el memo 00 de `Guias_Interactivas` imprimió el
2026-09-05; si un valor se aparta media unidad del último decimal, esto falla.

Los datos declarados (`caso`) son los de la serie: geometría del 01, masa del
05, planchas del 07 y el 10, y las rigideces que el 07 y el 10 publicaron sin
modelo, contra las que el memo compara. Los períodos con 4 y 8 tramos vienen de
la capa D del caso 11 de `verification/`, que mide la convergencia de la malla.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from serie import Eslabon, main  # noqa: E402

E = Eslabon("nch2369-galpon-grua", orden=0, slug="el-modelo",
            titulo="El modelo: el galpón entero corre por primera vez",
            normas=["NCh2369:2025"], carpeta=AQUI)

# ------------------------------------------------------------ el caso
G = 9.81
L_luz = E.caso("L_luz", 25.0, "m")
s_marco = E.caso("s_marco", 7.5, "m")
h_libre = E.caso("h_libre", 10.5, "m")
h_riel = E.caso("h_riel", 7.5, "m")
h_asiento = E.caso("h_asiento", 6.68424, "m")
P_sismico = E.caso("P_sismico", 1037.085, "kN")
Wgrua_sc = E.caso("Wgrua_sc", 230.0, "kN")
A_diag_techo = E.caso("A_diag_techo", 2400.0, "mm2")
A_punt_techo = E.caso("A_punt_techo", 4656.0, "mm2")
n_marcos = E.caso("n_marcos", 5, "—")
H_marco = E.caso("H_marco", 1000.0, "kN")           # S5: 500 kN a cada alero
E_acero = E.caso("E_acero", 200000.0, "MPa")
# lo que la serie declaró sin modelo, contra lo que se compara
k_Y_07 = E.caso("k_Y_07", 5612.11747, "kN/m")        # 07 · S1
k_riel_07 = E.caso("k_riel_07", 15057.33721, "kN/m")  # 07 · S1
k_esc_10 = E.caso("k_esc_10", 2.24801, "—")           # 10 · D6
T_Y_10 = E.caso("T_Y_10", 0.25722, "s")               # 10 · D6
T_X_04 = E.caso("T_X_04", 0.20, "s")                  # 04 · S2
# la convergencia de la malla (caso 11, capa D)
T_Y_nsub4 = E.caso("T_Y_nsub4", 0.2489536, "s")
T_Y_nsub8 = E.caso("T_Y_nsub8", 0.2488182, "s")

# ------------------------------------------------------------ el modelo
T_star_X = E.entra("T_star_X", de="modelo:galpon-grua", paso="M1")
T_star_Y = E.entra("T_star_Y", de="modelo:galpon-grua", paso="M1")
Ux = E.entra("Ux", de="modelo:galpon-grua", paso="M1")
Uy = E.entra("Uy", de="modelo:galpon-grua", paso="M1")
macum_X = E.entra("macum_X", de="modelo:galpon-grua", paso="M1")
macum_Y = E.entra("macum_Y", de="modelo:galpon-grua", paso="M1")
macum_Z = E.entra("macum_Z", de="modelo:galpon-grua", paso="M1")
d_alero = E.entra("d_alero", de="modelo:galpon-grua", paso="M2")
d_riel = E.entra("d_riel", de="modelo:galpon-grua", paso="M2")
peso_total = E.entra("peso_total", de="modelo:galpon-grua", paso="M1")

# ------------------------------------------------------------ A · el modelo es el galpón de la serie
m_total = E.paso("A1", "m_total", P_sismico / G, "t")
T_Y_nsub16 = T_star_Y
razon_conv = E.paso("A3", "razon_conv", (T_Y_nsub8 - T_Y_nsub16) / (T_Y_nsub4 - T_Y_nsub8), "—")
err_richardson = E.paso("A3", "err_richardson", (T_Y_nsub8 - T_Y_nsub16) / 3.0, "s")
T_Y_conv = E.paso("A3", "T_Y_conv", T_Y_nsub16 - err_richardson, "s")

# ------------------------------------------------------------ B · los dos empujes
# El memo sustituye en la fórmula la cifra que imprime (siete decimales), no la
# del motor; con la de siete decimales su k se reproduce a los cinco que publica.
d_alero_H = E.paso("B1", "d_alero_H", round(d_alero, 7), "m")
d_riel_H = E.paso("B2", "d_riel_H", round(d_riel, 7), "m")
k_Y_3D = E.paso("B1", "k_Y_3D", H_marco / d_alero_H, "kN/m")
raz_kY_07 = E.paso("B1", "raz_kY_07", k_Y_3D / k_Y_07, "—")
raz_kY_esc = E.paso("B1", "raz_kY_esc", k_Y_3D / (k_Y_07 * k_esc_10), "—")
k_riel_3D = E.paso("B2", "k_riel_3D", H_marco / d_riel_H, "kN/m")
raz_kriel_07 = E.paso("B2", "raz_kriel_07", k_riel_3D / k_riel_07, "—")

# ------------------------------------------------------------ C · períodos y masas
raz_TY_10 = E.paso("C1", "raz_TY_10", T_star_Y / T_Y_10, "—")
raz_TX_04 = E.paso("C2", "raz_TX_04", T_star_X / T_X_04, "—")
raz_macum_X = E.paso("C3", "raz_macum_X", macum_X / 0.90, "—")
raz_macum_Y = E.paso("C3", "raz_macum_Y", macum_Y / 0.90, "—")

# ------------------------------------------------------------ D · los osciladores de 1 GDL
m_marco = E.paso("D1", "m_marco", P_sismico / (n_marcos * G), "t")
T1_Y = E.paso("D1", "T1_Y", 2 * math.pi * math.sqrt(m_marco / k_Y_3D), "s")
raz_T1_Y = E.paso("D1", "raz_T1_Y", T_star_Y / T1_Y, "—")
# el panel del 12 · B5: tubo 125×125×5 sobre el vano de 7,50 × 10,50, en tensión-compresión
L_diag_panel = E.paso("D2", "L_diag_panel", math.hypot(s_marco, h_libre) * 1000.0, "mm")
cos2_panel = E.paso("D2", "cos2_panel", (s_marco * 1000.0 / L_diag_panel) ** 2, "—")
A_panel = E.caso("A_panel", 2400.0, "mm2")
k_pan = E.paso("D2", "k_pan", 2 * E_acero * A_panel * cos2_panel / L_diag_panel, "kN/m")
n_paneles = E.caso("n_paneles", 4, "—")
T1_X = E.paso("D2", "T1_X", 2 * math.pi * math.sqrt(m_total / (n_paneles * k_pan)), "s")
raz_T1_X = E.paso("D2", "raz_T1_X", T_star_X / T1_X, "—")
# la regla 5b: el oscilador con la k_Y del 07 (un solo alero) habría dado 0,38 s
T1_Y_07 = E.paso("D1", "T1_Y_07", 2 * math.pi * math.sqrt(m_marco / k_Y_07), "s")

# ------------------------------------------------------------ Sale
E.sale("T_star_X", T_star_X, "s", paso="M1")
E.sale("T_star_Y", T_star_Y, "s", paso="M1")
E.sale("Ux_star", Ux, "—", paso="M1")
E.sale("Uy_star", Uy, "—", paso="M1")
E.sale("macum_X", macum_X, "—", paso="M1")
E.sale("macum_Y", macum_Y, "—", paso="M1")
E.sale("d_alero_H", d_alero, "m", paso="M2")
E.sale("d_riel_H", d_riel, "m", paso="M2")
E.sale("k_Y_3D", k_Y_3D, "kN/m", paso="B1")
E.sale("k_riel_3D", k_riel_3D, "kN/m", paso="B2")

# lo que el memo 00 de Guias_Interactivas imprimió en su `## Sale` (2026-09-05)
E.publicado({
    "T_star_X": "0,20602", "T_star_Y": "0,24878",
    "Ux_star": "0,69109", "Uy_star": "0,94330",
    "macum_X": "0,99731", "macum_Y": "0,99387",
    "d_alero_H": "0,0664559", "d_riel_H": "0,0236292",
    "k_Y_3D": "15047,57290", "k_riel_3D": "42320,51868",
})

if __name__ == "__main__":
    raise SystemExit(main(sys.argv, E))
