"""Eslabón 03 — cargas de puente grúa: el empuje lateral es el mayor de tres
reglas simultáneas, y ninguna de las tres es la que CMAA usa para diseñar la grúa.

    python sitio/docs/series/nch2369-galpon-grua/03-cargas-de-grua/_calculo.py [salida]

Hereda del 01 la capacidad nominal, la luz del puente y la separación de marcos.
Lo demás son datos declarados de la grúa (S2, S3, S4), la fila de la Tabla 3.2 de
AIST TR-13:2021 (S5) y la aritmética de §3.7, transcritas del memo 03 de
`Guias_Interactivas`, que las leyó del PDF (ver la tabla de referencias de
`index.md`).

Dos cosas que este eslabón separa y conviene no volver a mezclar:

* **Tres reglas a la vez, no una.** §3.7.2 exige el **mayor** entre el empuje de
  la Tabla 3.2, el 20 % del carro más la carga izada y el 10 % del peso total. Las
  tres crecen con magnitudes distintas, así que cuál gobierna se evalúa; acá se
  calculan las tres y `SS_total` es el máximo.
* **Dos juegos de factores con nombres parecidos.** El impacto del 20 % de AIST
  carga al **edificio** y viaja por la cadena; el `HLF` y el `DLF` de CMAA cargan
  a la **grúa** y se calculan acá solo para mostrar que no son lo mismo: no salen
  en `sale`.

Los pasos `L1` a `L3` son las cifras que el memo publica en su `## Resumen` y usa
en su `## Límites` (flechas admisibles, fuerza de servicio y razón luz/base), sin
bloque narrativo propio.
"""

from __future__ import annotations

import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from serie import Eslabon, main  # noqa: E402

E = Eslabon("nch2369-galpon-grua", orden=3, slug="cargas-de-grua",
            titulo="Cargas de puente grúa",
            normas=["AIST TR-13:2021", "CMAA 70:2010", "NCh2369:2025"], carpeta=AQUI)

# ------------------------------------------------------------ lo que entra
Qn_grua = E.entra("Qn_grua", de="01", paso="S3")
Lg_grua = E.entra("Lg_grua", de="01", paso="S3")
s_marco = E.entra("s_marco", de="01", paso="S1")

# ------------------------------------------------------------ el caso
Wb_d = E.caso("Wb_d", 190.0, "kN")             # S2, peso del puente
Wt_d = E.caso("Wt_d", 40.0, "kN")              # S2, peso del carro con su izaje
wb_d = E.caso("wb_d", 3.40, "m")               # S2, separación de ruedas por testero
a_gancho = E.caso("a_gancho", 1.20, "m")       # S2, aproximación mínima del gancho al riel
n_ruedas = E.caso("n_ruedas", 4, "—")          # S2, dos por testero, todas motrices
v_izaje = E.caso("v_izaje", 4.00, "m/min")     # S3
v_tras = E.caso("v_tras", 30.00, "m/min")      # S3
izajes_h = E.caso("izajes_h", 3, "1/h")        # S4, el régimen de operación
h_dia = E.caso("h_dia", 4, "h/d")              # S4
dias_ano = E.caso("dias_ano", 250, "d/a")      # S4
vida_d = E.caso("vida_d", 25, "años")          # S4
# la Tabla 3.2, fila «Motor room maintenance cranes, etc.» (S5)
t32_imp = E.caso("t32_imp", 0.20, "—")
t32_emp = E.caso("t32_emp", 0.30, "—")
t32_tra = E.caso("t32_tra", 0.20, "—")
# la fila «Mill cranes» de la misma tabla, la alternativa que se descartó
mill_imp = E.caso("mill_imp", 0.25, "—")
mill_emp = E.caso("mill_emp", 0.40, "—")
# los pisos de CMAA §3.3.2.1.4 (S3)
HLF_piso = E.caso("HLF_piso", 0.15, "—")
DLF_piso = E.caso("DLF_piso", 1.10, "—")
cmaa_lat = E.caso("cmaa_lat", 0.10, "—")       # §1.4.6, la fuerza lateral de servicio

PIE = 0.3048                                    # m por pie, la conversión de CMAA

# ------------------------------------------------------------ A · la clase de servicio
N_ciclos = E.paso("A1", "N_ciclos", izajes_h * h_dia * dias_ano * vida_d, "ciclos")
N_jornada = E.paso("A3", "N_jornada", 8 * 8 * dias_ano * vida_d, "ciclos")

# ------------------------------------------------------------ B · las reacciones de rueda
W_tot = E.paso("B1", "W_tot", Qn_grua + Wt_d + Wb_d, "kN")
R_test = E.paso("B1", "R_test",
                (Qn_grua + Wt_d) * (Lg_grua - a_gancho) / Lg_grua + Wb_d / 2, "kN")
Rw_max = E.paso("B2", "Rw_max", R_test / 2, "kN")
R_test_min = E.paso("B3", "R_test_min", (Qn_grua + Wt_d) * a_gancho / Lg_grua + Wb_d / 2, "kN")
Rw_min = E.paso("B3", "Rw_min", R_test_min / 2, "kN")
R_suma = E.paso("B3", "R_suma", R_test + R_test_min, "kN")
raz_ruedas = E.paso("B3", "raz_ruedas", Rw_max / Rw_min, "—")

# ------------------------------------------------------------ C · el impacto, y los dos que no
Rv_max = E.paso("C1", "Rv_max", (1 + t32_imp) * Rw_max, "kN")
v_izaje_fpm = E.paso("C2", "v_izaje_fpm", v_izaje / PIE, "ft/min")
HLF_bruto = E.paso("C2", "HLF_bruto", 0.005 * v_izaje_fpm, "—")
HLF = E.paso("C2", "HLF", min(max(HLF_bruto, HLF_piso), 0.50), "—")
v_tras_fpm = E.paso("C3", "v_tras_fpm", v_tras / PIE, "ft/min")
DLF_bruto = E.paso("C3", "DLF_bruto", 1.05 + v_tras_fpm / 2000.0, "—")
DLF = E.paso("C3", "DLF", min(max(DLF_bruto, DLF_piso), 1.20), "—")

# ------------------------------------------------------------ D · el empuje lateral
SS_1 = E.paso("D1", "SS_1", t32_emp * Qn_grua, "kN")
SS_2 = E.paso("D1", "SS_2", 0.20 * (Qn_grua + Wt_d), "kN")
SS_3 = E.paso("D1", "SS_3", 0.10 * W_tot, "kN")
SS_total = E.paso("D2", "SS_total", max(SS_1, SS_2, SS_3), "kN")
raz_SS12 = E.paso("D2", "raz_SS12", SS_1 / SS_2, "—")
raz_SS13 = E.paso("D2", "raz_SS13", SS_1 / SS_3, "—")
SS_carril = E.paso("D3", "SS_carril", SS_total / 2, "kN")

# ------------------------------------------------------------ E · la tracción longitudinal
T_long = E.paso("E1", "T_long", t32_tra * W_tot, "kN")
raz_TS = E.paso("E2", "raz_TS", T_long / SS_total, "—")

# ------------------------------------------------------------ F · lo que CMAA devuelve
n_sismo_cmaa = E.paso("F1", "n_sismo_cmaa", 0, "cláusulas")
n_clausulas = E.paso("F2", "n_clausulas", 3, "cláusulas")

# ------------------------------------------------------------ L · lo que el memo deja en Límites
flecha_v = E.paso("L1", "flecha_v", s_marco * 1000.0 / 600.0, "mm")
flecha_l = E.paso("L1", "flecha_l", s_marco * 1000.0 / 400.0, "mm")
lat_servicio = E.paso("L2", "lat_servicio", cmaa_lat * Rw_max, "kN")
raz_aist_cmaa = E.paso("L2", "raz_aist_cmaa", t32_emp / cmaa_lat, "—")
raz_luz_base = E.paso("L3", "raz_luz_base", Lg_grua / wb_d, "—")

# ------------------------------------------------------------ Sale
E.sale("Wb_puente", Wb_d, "kN", paso="S2", heredan=["05", "08", "09", "12"])
E.sale("Wt_carro", Wt_d, "kN", paso="S2", heredan=["05", "08", "09", "12"])
E.sale("wb_ruedas", wb_d, "m", paso="S2", heredan=["06", "07", "08", "09", "12"])
E.sale("Rw_max", Rw_max, "kN", paso="B2", heredan=["08", "09", "10", "12"])
E.sale("Rw_min", Rw_min, "kN", paso="B3", heredan=["08", "12"])
E.sale("Rv_max", Rv_max, "kN", paso="C1", heredan=["07", "08", "09", "10"])
E.sale("SS_total", SS_total, "kN", paso="D1", heredan=["07", "08"])
E.sale("SS_carril", SS_carril, "kN", paso="D3", heredan=["07", "08", "09"])
E.sale("T_long", T_long, "kN", paso="E1", heredan=["08", "12"])
E.sale("N_ciclos", N_ciclos, "ciclos", paso="A1", heredan=["08", "09"])
E.sale("vida_grua", vida_d, "años", paso="S4", heredan=["08", "09"])

# lo que el memo 03 de Guias_Interactivas imprimió en su `## Sale`
E.publicado({
    "Wb_puente": "190,00", "Wt_carro": "40,00", "wb_ruedas": "3,40",
    "Rw_max": "161,23913", "Rw_min": "53,76087", "Rv_max": "193,48696",
    "SS_total": "60,00000", "SS_carril": "30,00000", "T_long": "86,00000",
    "N_ciclos": "75000", "vida_grua": "25",
})

if __name__ == "__main__":
    raise SystemExit(main(sys.argv, E))
