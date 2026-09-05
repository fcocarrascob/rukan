"""Eslabón 04 — espectro y R* por dirección: la Ec. (1b) le devuelve a 4 el R de
5 que el 01 ganó, y solo en la dirección arriostrada.

    python sitio/docs/series/nch2369-galpon-grua/04-espectro-y-r-por-direccion/_calculo.py [salida]

Hereda del 01 el coeficiente de importancia, la fila de la Tabla 7 con su R y su
ξ, el amplificador y la geometría. Zona 2, suelo C y los dos períodos de análisis
son dato de proyecto (S1, S2). Las tres ecuaciones —(1a), (1b) y (3)— se
transcriben del memo 04 de `Guias_Interactivas`, que las leyó del PDF (ver la
tabla de referencias de `index.md`).

Tres cosas que este eslabón hace y conviene no perder de vista al leerlo:

* **La Ec. (1b) tiene tres ramas**, no una: `R* = 1` si `R ≤ 1`, la meseta `R* = R`
  desde la frontera `C_r T_1 = 0,16 R T_1`, y la rampa lineal desde 1,5 bajo ella.
  `r_estrella()` las escribe las tres.
* **La frontera se mueve con el R.** Por eso el galpón liviano de la fila 5.7
  tiene la suya, 0,224 s, y la comparación honesta del bloque D no es 5 contra 4.
* **Los períodos son declarados** (S2), no salida de un modelo. El 00 publica los
  del modelo corrido y todavía no se heredan: la cascada es un cambio explícito
  posterior a la migración de la serie. Lo que este eslabón sostiene es la
  **rama** de cada dirección, y C7 la mide en margen de masa.

El pico del espectro de referencia sale en forma cerrada porque `q = 2p` con los
parámetros del suelo C: sustituyendo `u = (T/T_0)^p` la Ec. (3) queda
`(1 + r u)/(1 + u²)`, cuya derivada anulada da la cuadrática `r u² + 2u - r = 0`.
Dos filas del `## Resumen` del memo son razones contra el pico **redondeado a los
cinco decimales que el memo imprimió**: se reproducen con ese redondeo, que es lo
que el memo sustituyó en su fórmula.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from serie import Eslabon, main  # noqa: E402

E = Eslabon("nch2369-galpon-grua", orden=4, slug="espectro-y-r-por-direccion",
            titulo="Espectro y R* por dirección", normas=["NCh2369:2025"], carpeta=AQUI)

# ------------------------------------------------------------ lo que entra
I = E.entra("I", de="01", paso="A1")
R_T7 = E.entra("R_T7", de="01", paso="D1")
xi = E.entra("xi", de="01", paso="D1")
k_amp = E.entra("k_amp", de="01", paso="C3")
s_marco = E.entra("s_marco", de="01", paso="S1")
h_libre = E.entra("h_libre", de="01", paso="S1")

# ------------------------------------------------------------ el caso
zona = E.caso("zona", 2, "—")                  # S1
A_0 = E.caso("A_0", 0.30, "g")                 # Tabla 3, zona 2
# Tabla 6, la fila del suelo C (S1)
S_C = E.caso("S_C", 1.05, "—")
r_C = E.caso("r_C", 4.50, "—")
T0_C = E.caso("T0_C", 0.40, "s")
p_C = E.caso("p_C", 1.50, "—")
q_C = E.caso("q_C", 3.00, "—")
T1_C = E.caso("T1_C", 0.35, "s")
# Tabla 6, la fila del suelo D y Tabla 3 zona 3: el sitio de la serie de harneros
A_0_h = E.caso("A_0_h", 0.40, "g")
S_D = E.caso("S_D", 1.00, "—")
r_D = E.caso("r_D", 3.50, "—")
T0_D = E.caso("T0_D", 0.60, "s")
p_D = E.caso("p_D", 1.00, "—")
q_D = E.caso("q_D", 2.50, "—")
# los dos períodos declarados (S2) y el R del galpón liviano de la fila 5.7
TX_d = E.caso("TX_d", 0.20, "s")
TY_d = E.caso("TY_d", 0.40, "s")
R_liv = E.caso("R_liv", 4.0, "—")
k_amp_liv = E.caso("k_amp_liv", 0.50, "—")     # §12.2.2, el 0,5 R1 del galpón liviano
xi_ref = E.caso("xi_ref", 0.05, "—")           # §5.4.2, el ξ de los espectros de referencia
R_piso = E.caso("R_piso", 1.5, "—")            # Ec. (1b), el piso de la rampa


# ------------------------------------------------- las tres ecuaciones de §5.4
def sa_ref(T: float, ar_s: float, r: float, T0: float, p: float, q: float) -> float:
    """Ec. (3): el espectro de referencia horizontal, en g, para ξ = 0,05."""
    if T <= 0.0:
        return ar_s
    x = T / T0
    return ar_s * (1.0 + r * x ** p) / (1.0 + x ** q)


def r_estrella(T: float, R: float, T1: float) -> float:
    """Ec. (1b), con sus tres ramas explícitas y `C_r = 0,16 R` adentro."""
    if R <= 1.0:
        return 1.0                                  # rama 1
    lim = 0.16 * R * T1
    if T >= lim:
        return R                                    # rama 2, la meseta
    return 1.5 + (R - 1.5) * T / lim                # rama 3, la rampa


# ------------------------------------------------------------ A · el sitio
A_r = E.paso("A1", "A_r", 1.4 * A_0, "g")
S_suelo = E.paso("A2", "S_suelo", S_C, "—")
r_s = E.paso("A2", "r_s", r_C, "—")
T_0 = E.paso("A2", "T_0", T0_C, "s")
p_suelo = E.paso("A2", "p_suelo", p_C, "—")
q_s = E.paso("A2", "q_s", q_C, "—")
T_1 = E.paso("A2", "T_1", T1_C, "s")
ArS = E.paso("A3", "ArS", A_r * S_suelo, "g")
ArS_harneros = E.paso("A3", "ArS_harneros", 1.4 * A_0_h * S_D, "g")
raz_ArS = E.paso("A3", "raz_ArS", ArS / ArS_harneros, "—")

# ------------------------------------------------------------ B · el espectro de referencia
f_xi = E.paso("B1", "f_xi", (xi_ref / xi) ** 0.4, "—")
# el máximo de la Ec. (3): con q = 2p, `u = (T/T_0)^p` deja `r u² + 2u - r = 0`
assert abs(q_s - 2 * p_suelo) < 1e-12, "el pico en forma cerrada exige q = 2p"
u_pico = E.paso("B2", "u_pico", (math.sqrt(1.0 + r_s ** 2) - 1.0) / r_s, "—")
T_pico = E.paso("B2", "T_pico", T_0 * u_pico ** (1.0 / p_suelo), "s")
Sa_pico = E.paso("B2", "Sa_pico", sa_ref(T_pico, ArS, r_s, T_0, p_suelo, q_s), "g")
Sa_ref_X = E.paso("C4", "Sa_ref_X", sa_ref(TX_d, ArS, r_s, T_0, p_suelo, q_s), "g")
Sa_h_020 = E.paso("B2", "Sa_h_020",
                  sa_ref(TX_d, ArS_harneros, r_D, T0_D, p_D, q_D), "g")
raz_Sa_020 = E.paso("B2", "raz_Sa_020", Sa_ref_X / Sa_h_020, "—")

# ------------------------------------------------------------ C · las dos direcciones
Cr_T1 = E.paso("C2", "Cr_T1", 0.16 * R_T7 * T_1, "s")
# el memo sustituye en esta razón el pico **impreso**, a cinco decimales
T_pico_pub = E.paso("C2", "T_pico_pub", round(T_pico, 5), "s")
raz_pico_frontera = E.paso("C2", "raz_pico_frontera", T_pico_pub / Cr_T1, "—")
T_star_X = E.paso("C3", "T_star_X", TX_d, "s")
T_star_Y = E.paso("C3", "T_star_Y", TY_d, "s")
raz_T = E.paso("C3", "raz_T", T_star_Y / T_star_X, "—")
R_star_X = E.paso("C4", "R_star_X", r_estrella(T_star_X, R_T7, T_1), "—")
pena_rampa = E.paso("C4", "pena_rampa", R_T7 / R_star_X, "—")
sens_R = E.paso("C4", "sens_R", (R_T7 - R_piso) / Cr_T1, "1/s")
R_star_Y = E.paso("C5", "R_star_Y", r_estrella(T_star_Y, R_T7, T_1), "—")
Sa_ref_Y = E.paso("C5", "Sa_ref_Y", sa_ref(T_star_Y, ArS, r_s, T_0, p_suelo, q_s), "g")
Sa_pico_pub = E.paso("C5", "Sa_pico_pub", round(Sa_pico, 5), "g")
frac_pico = E.paso("C5", "frac_pico", Sa_ref_Y / Sa_pico_pub, "—")
Sa_dis_X = E.paso("C6", "Sa_dis_X", I * Sa_ref_X * f_xi / R_star_X, "g")
Sa_dis_Y = E.paso("C6", "Sa_dis_Y", I * Sa_ref_Y * f_xi / R_star_Y, "g")
# el memo divide en C6 las dos ordenadas **impresas**, no las exactas: con las
# exactas la razón da 1,04686 y el memo publicó 1,04687
Sa_dis_X_pub = E.paso("C6", "Sa_dis_X_pub", round(Sa_dis_X, 5), "g")
Sa_dis_Y_pub = E.paso("C6", "Sa_dis_Y_pub", round(Sa_dis_Y, 5), "g")
raz_Sa_dis = E.paso("C6", "raz_Sa_dis", Sa_dis_X_pub / Sa_dis_Y_pub, "—")
marg_X = E.paso("C7", "marg_X", (Cr_T1 / T_star_X) ** 2, "—")
marg_Y = E.paso("C7", "marg_Y", (Cr_T1 / T_star_Y) ** 2, "—")

# ------------------------------------------------------------ D · las cotas del 01
Cr_T1_liv = E.paso("D1", "Cr_T1_liv", 0.16 * R_liv * T_1, "s")
R_star_X_liv = E.paso("D1", "R_star_X_liv", r_estrella(T_star_X, R_liv, T_1), "—")
R_star_Y_liv = E.paso("D3", "R_star_Y_liv", r_estrella(T_star_Y, R_liv, T_1), "—")
alivio_X = E.paso("D2", "alivio_X", (1 / R_star_X) / (1 / R_star_X_liv), "—")
alivio_Y = E.paso("D3", "alivio_Y", (1 / R_star_Y) / (1 / R_star_Y_liv), "—")
sobre_nofusible = E.paso("D4", "sobre_nofusible", k_amp / k_amp_liv, "—")
amp_X = E.paso("D5", "amp_X", k_amp * R_star_X, "—")
amp_X_liv = E.paso("D5", "amp_X_liv", k_amp_liv * R_star_X_liv, "—")
alza_X = E.paso("D5", "alza_X", amp_X / amp_X_liv, "—")
amp_Y = E.paso("D5", "amp_Y", k_amp * R_star_Y, "—")
amp_Y_liv = E.paso("D5", "amp_Y_liv", k_amp_liv * R_star_Y_liv, "—")
alza_Y = E.paso("D5", "alza_Y", amp_Y / amp_Y_liv, "—")

# ------------------------------------------------------------ Sale
E.sale("A_r", A_r, "g", paso="A1", heredan=["05", "06"])
E.sale("S_suelo", S_suelo, "—", paso="A2", heredan=["05", "06"])
E.sale("r_s", r_s, "—", paso="A2", heredan=["05", "06", "07", "12"])
E.sale("T_0", T_0, "s", paso="A2", heredan=["06", "07", "12"])
E.sale("p_suelo", p_suelo, "—", paso="A2", heredan=["06", "07", "12"])
E.sale("q_s", q_s, "—", paso="A2", heredan=["06", "07", "12"])
E.sale("T_1", T_1, "s", paso="A2", heredan=["05"])
E.sale("T_pico", T_pico, "s", paso="B2", heredan=["06", "07"])
E.sale("Sa_pico", Sa_pico, "g", paso="B2", heredan=["06", "07"])
E.sale("ArS", ArS, "g", paso="A3", heredan=["06", "07", "12"])
E.sale("f_xi", f_xi, "—", paso="B1", heredan=["05", "06", "07", "12"])
E.sale("Cr_T1", Cr_T1, "s", paso="C2", heredan=["05", "07", "12"])
E.sale("T_star_X", T_star_X, "s", paso="S2", heredan=["05", "06", "12"])
E.sale("T_star_Y", T_star_Y, "s", paso="S2", heredan=["05", "06", "07", "12"])
E.sale("R_star_X", R_star_X, "—", paso="C4", heredan=["05", "06", "12"])
E.sale("R_star_Y", R_star_Y, "—", paso="C5", heredan=["05", "06", "07", "12"])
E.sale("Sa_ref_X", Sa_ref_X, "g", paso="C4", heredan=["06", "12"])
E.sale("Sa_ref_Y", Sa_ref_Y, "g", paso="C5", heredan=["06", "07"])
E.sale("Sa_dis_X", Sa_dis_X, "g", paso="C6", heredan=["05"])
E.sale("Sa_dis_Y", Sa_dis_Y, "g", paso="C6", heredan=["05"])

# lo que el memo 04 de Guias_Interactivas imprimió en su `## Sale`
E.publicado({
    "A_r": "0,42", "S_suelo": "1,05", "r_s": "4,50", "T_0": "0,40",
    "p_suelo": "1,50", "q_s": "3,00", "T_1": "0,35",
    "T_pico": "0,34533", "Sa_pico": "1,23695", "ArS": "0,44100", "f_xi": "1,44270",
    "Cr_T1": "0,28000", "T_star_X": "0,20", "T_star_Y": "0,40",
    "R_star_X": "4,00000", "R_star_Y": "5,00000",
    "Sa_ref_X": "1,01567", "Sa_ref_Y": "1,21275",
    "Sa_dis_X": "0,36633", "Sa_dis_Y": "0,34993",
})

if __name__ == "__main__":
    raise SystemExit(main(sys.argv, E))
