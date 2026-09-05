"""Eslabón 01 — el umbral de las 20 t: una sola letra de §12.2.1 saca al galpón
de la cláusula 12.2, y con ella se van el R, el solo-tracción y el 0,5R1.

    python sitio/docs/series/nch2369-galpon-grua/01-el-umbral-de-las-20-t/_calculo.py [salida]

Es la raíz de la cadena: no hereda de nadie. Todo lo que publica es dato de
proyecto (S1 a S8) o una lectura de la Tabla 7 y de §12.2.1 de NCh2369:2025,
transcrita del memo 01 de `Guias_Interactivas`, que la leyó del PDF (ver la
tabla de referencias de `index.md`). Cada letra de §12.2.1 se mide como el
cociente entre lo que el galpón tiene y lo que la letra permite: menor que 1
es cumplimiento.
"""

from __future__ import annotations

import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from serie import Eslabon, main  # noqa: E402

E = Eslabon("nch2369-galpon-grua", orden=1, slug="el-umbral-de-las-20-t",
            titulo="El umbral de las 20 t: una sola letra de §12.2.1",
            normas=["NCh2369:2025"], carpeta=AQUI)

# ------------------------------------------------------------ el caso
L_luz = E.caso("L_luz", 25.0, "m")            # S1
s_marco = E.caso("s_marco", 7.5, "m")         # S1
n_vanos = E.caso("n_vanos", 4, "—")           # S1
L_total = E.caso("L_total", 30.0, "m")        # S1
h_libre = E.caso("h_libre", 10.5, "m")        # S1
pend = E.caso("pend", 20.0, "%")              # S1
h_cumb = E.caso("h_cumb", 2.5, "m")           # S1, sobre el alero
Qn_grua = E.caso("Qn_grua", 200.0, "kN")      # S3
Lg_grua = E.caso("Lg_grua", 23.0, "m")        # S3
h_riel = E.caso("h_riel", 7.5, "m")           # S3
g_techo = E.caso("g_techo", 38.0, "kg/m2")    # S4
P_eq = E.caso("P_eq", 12.0, "kN")             # S5, equipos por marco
n_altillos = E.caso("n_altillos", 0, "—")     # S5
zona = E.caso("zona", 2, "—")                 # S6
n_naves = E.caso("n_naves", 1, "—")           # S1
n_estanterias = E.caso("n_estanterias", 0, "—")  # S5
# los límites de §12.2.1, leídos de la norma (memo 01 · NCh-p6 a NCh-p9)
h_lim = E.caso("h_lim", 23.0, "m")            # c)
L_lim = E.caso("L_lim", 75.0, "m")            # c), nave individual
L_lim_par = E.caso("L_lim_par", 45.0, "m")    # c), naves paralelas
g_lim = E.caso("g_lim", 70.0, "kg/m2")        # d)
Qn_lim = E.caso("Qn_lim", 100.0, "kN")        # e), sin cabina
Qn_lim_cab = E.caso("Qn_lim_cab", 50.0, "kN")  # e), con cabina
P_eq_lim = E.caso("P_eq_lim", 50.0, "kN")     # g)
H_alt_lim = E.caso("H_alt_lim", 15.0, "kN")   # h), por columna
# la Tabla 7 (memo 01 · NCh-p13 a NCh-p15) y §12.2.2 / §8.3.4
R_liv = E.caso("R_liv", 4.0, "—")             # fila 5.7, galpón liviano
R_55 = E.caso("R_55", 5.0, "—")               # fila 5.5
R_gen = E.caso("R_gen", 3.0, "—")             # filas 5.2 y 5.4
xi_55 = E.caso("xi_55", 0.02, "—")            # fila 5.5, uniones soldadas
k_amp_liv = E.caso("k_amp_liv", 0.5, "—")     # §12.2.2: 0,5 R1
k_amp_gen = E.caso("k_amp_gen", 0.7, "—")     # §8.3.4: 0,7 R1

# ------------------------------------------------------------ A · categoría e importancia
I = E.paso("A1", "I", 1.0, "—")               # Categoría II, §4.3.2

# ------------------------------------------------------------ B · las ocho letras
u_h = E.paso("B2", "u_h", h_libre / h_lim, "—")
u_L = E.paso("B3", "u_L", L_luz / L_lim, "—")
u_d = E.paso("B4", "u_d", g_techo / g_lim, "—")
u_e = E.paso("B5", "u_e", Qn_grua / Qn_lim, "—")
u_e_cab = E.paso("B5", "u_e_cab", Qn_grua / Qn_lim_cab, "—")
u_g = E.paso("B7", "u_g", P_eq / P_eq_lim, "—")
u_h_alt = E.paso("B8", "u_h_alt", 0.0 / H_alt_lim, "—")
cumplen = [n_naves == 1, u_h <= 1, u_L <= 1, u_d <= 1, u_e <= 1,
           n_estanterias == 0, u_g <= 1, u_h_alt <= 1]
n_cumplen = E.paso("C1", "n_cumplen", sum(cumplen), "—")
n_fallan = E.paso("C1", "n_fallan", 8 - sum(cumplen), "—")

# ------------------------------------------------------------ C · lo que se pierde
k_amp = E.paso("C3", "k_amp", k_amp_gen, "—")

# ------------------------------------------------------------ D · la fila que queda
R_T7 = E.paso("D1", "R_T7", R_55, "—")
xi = E.paso("D1", "xi", xi_55, "—")
amp_55 = E.paso("D3", "amp_55", k_amp_gen * R_55, "—")
amp_liv = E.paso("D3", "amp_liv", k_amp_liv * R_liv, "—")
raz_amp = E.paso("D3", "raz_amp", amp_55 / amp_liv, "—")
raz_no_fusible = E.paso("D4", "raz_no_fusible", k_amp_gen / k_amp_liv, "—")
raz_fusible = E.paso("D5", "raz_fusible", (1 / R_55) / (1 / R_liv), "—")
raz_sin_ductil = E.paso("D6", "raz_sin_ductil", (1 / R_gen) / (1 / R_55), "—")

# ------------------------------------------------------------ Sale
E.sale("I", I, "—", paso="A1", heredan=["02", "04", "06", "07", "12"])
E.sale("L_luz", L_luz, "m", paso="S1", heredan=["02", "05", "07", "10", "11", "12"])
E.sale("s_marco", s_marco, "m", paso="S1",
       heredan=["02", "03", "04", "05", "07", "08", "09", "10", "11", "12"])
E.sale("h_libre", h_libre, "m", paso="S1", heredan=["04", "05", "06", "07", "10", "11", "12"])
E.sale("g_techo", g_techo, "kg/m2", paso="S4", heredan=["11"])
E.sale("Qn_grua", Qn_grua, "kN", paso="S3", heredan=["03", "08", "09", "10"])
E.sale("Lg_grua", Lg_grua, "m", paso="S3", heredan=["03", "10"])
E.sale("h_riel", h_riel, "m", paso="S3", heredan=["06", "07", "10", "12"])
E.sale("R_T7", R_T7, "—", paso="D1", heredan=["04", "06", "12"])
E.sale("xi", xi, "—", paso="D1", heredan=["04", "12"])
E.sale("k_amp", k_amp, "—", paso="C3", heredan=["04"])

# lo que el memo 01 de Guias_Interactivas imprimió en su `## Sale`
E.publicado({
    "I": "1,00", "L_luz": "25,00", "s_marco": "7,50", "h_libre": "10,50",
    "g_techo": "38,00", "Qn_grua": "200,00", "Lg_grua": "23,00", "h_riel": "7,50",
    "R_T7": "5", "xi": "0,02", "k_amp": "0,70",
})

if __name__ == "__main__":
    raise SystemExit(main(sys.argv, E))
