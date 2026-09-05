"""Eslabón 02 — nieve balanceada y desbalanceada: la acumulación de sotavento
sube el peak un 68 % y la fórmula del pie de la Figura 4 no reproduce sus
propias curvas.

    python sitio/docs/series/nch2369-galpon-grua/02-nieve-balanceada-y-desbalanceada/_calculo.py [salida]

Hereda del 01 la luz, la separación de marcos y el coeficiente de importancia.
Todo lo demás es lectura de tabla de NCh431:2010 (la celda de la Tabla 1, los
factores de las Tablas 2 y 4, la rama de la Figura 1 c\N{RIGHT SINGLE QUOTATION MARK}) o aritmética de sus
ecuaciones, transcritas del memo 02 de `Guias_Interactivas`, que las leyó del
PDF (ver la tabla de referencias de `index.md`).

Dos cosas que este eslabón hace y conviene no perder de vista al leerlo:

* **`S` no es la pendiente.** §8.2 usa la distancia horizontal por unidad de
  elevación en dos lugares con efectos opuestos: divide la intensidad de la
  acumulación y multiplica su extensión. Acá `S`, `tan θ` y `θ` se calculan por
  separado, y `S · tan θ = 1`.
* **La Figura 4 se digitaliza, no se despeja.** La fórmula que la propia figura
  imprime al pie da 6,49 veces menos que sus curvas, del lado inseguro. Las seis
  lecturas de la curva entran como dato del caso (S6) y el bloque E las contrasta
  contra ASCE 7.

El bloque E se calcula antes que el D porque D3 y D4 consumen su `h_d`; el memo
lo narra al final para no interrumpir la distribución con la digitalización.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from serie import Eslabon, main  # noqa: E402

E = Eslabon("nch2369-galpon-grua", orden=2, slug="nieve-balanceada-y-desbalanceada",
            titulo="Nieve balanceada y desbalanceada",
            normas=["NCh431:2010", "NCh2369:2025", "NCh3171:2017"], carpeta=AQUI)

# ------------------------------------------------------------ lo que entra
L_luz = E.entra("L_luz", de="01", paso="S1")
s_marco = E.entra("s_marco", de="01", paso="S1")
I = E.entra("I", de="01", paso="A1")

# ------------------------------------------------------------ el caso
h_cumbrera = E.caso("h_cumbrera", 2.50, "m")       # S2, la cumbrera sobre el alero
lat = E.caso("lat", 36.90, "°")                    # S1, latitud sur
alt = E.caso("alt", 1200.0, "m")                   # S1, altitud sobre el mar
p_g_T1 = E.caso("p_g_T1", 1.50, "kN/m2")           # Tabla 1, celda 1 000-1 250 x 36-38 S
p_g_normal = E.caso("p_g_normal", 0.25, "kN/m2")   # §4, el umbral de sobrecarga normal
C_e_T4 = E.caso("C_e_T4", 1.00, "—")               # Tabla 4, terreno C, parcialmente expuesto
C_e_exp = E.caso("C_e_exp", 0.90, "—")             # Tabla 4, el mismo terreno totalmente expuesto
C_e_mont = E.caso("C_e_mont", 0.80, "—")           # Tabla 4, áreas montañosas azotadas
C_t_T2 = E.caso("C_t_T2", 1.20, "—")               # Tabla 2, estructura no calefaccionada
C_t_cal = E.caso("C_t_cal", 1.00, "—")             # Tabla 2, estructura calefaccionada
C_s_F1 = E.caso("C_s_F1", 1.00, "—")               # Figura 1 c), por cualquiera de sus dos ramas
theta_min = E.caso("theta_min", 2.38, "°")         # §5.2 y §8.2, el umbral fijo
theta_max = E.caso("theta_max", 70.0, "°")         # §8.2, el techo demasiado inclinado
gamma_tope = E.caso("gamma_tope", 4.70, "kN/m3")   # §9.2, el tope de la Ec. (3)
p_g_lluvia = E.caso("p_g_lluvia", 0.96, "kN/m2")   # §12, hasta dónde rige lluvia sobre nieve
# la Figura 4 digitalizada en p_g = 1,50 kN/m2 (S6): I_u en m -> h_d en m
hd_c75 = E.caso("hd_c75", 0.46230, "m")
hd_c15 = E.caso("hd_c15", 0.76130, "m")
hd_c30 = E.caso("hd_c30", 1.04850, "m")
hd_c60 = E.caso("hd_c60", 1.41340, "m")
hd_c120 = E.caso("hd_c120", 1.89250, "m")
hd_c180 = E.caso("hd_c180", 2.23670, "m")

# ------------------------------------------------------------ A · el sitio
p_g = E.paso("A1", "p_g", p_g_T1, "kN/m2")
raz_normal = E.paso("A2", "raz_normal", p_g / p_g_normal, "—")

# ------------------------------------------------------------ B · los cuatro factores
C_e = E.paso("B1", "C_e", C_e_T4, "—")
C_t = E.paso("B2", "C_t", C_t_T2, "—")
p_f = E.paso("B4", "p_f", 0.7 * C_e * C_t * I * p_g, "kN/m2")
W = E.paso("B5", "W", L_luz / 2.0, "m")
theta_lim = E.paso("B5", "theta_lim", 21.3 / W + 0.5, "°")

# ------------------------------------------------------------ C · la pendiente
tan_theta = E.paso("C1", "tan_theta", h_cumbrera / W, "—")
theta_techo = E.paso("C1", "theta_techo", math.degrees(math.atan(tan_theta)), "°")
S_pend = E.paso("C2", "S_pend", W / h_cumbrera, "—")
C_s = E.paso("C3", "C_s", C_s_F1, "—")
p_s = E.paso("C4", "p_s", C_s * p_f, "kN/m2")

# ------------------------------------------------------------ E · la Figura 4
# (el memo la narra al final; se calcula acá porque D3 y D4 consumen h_d)
I_u = E.paso("E1", "I_u", W, "m")
hd_pie = E.paso("E2", "hd_pie", 0.132 * I_u ** (1 / 3) * (p_g + 10.0) ** 0.25 - 0.46, "m")
t_int = E.paso("E3", "t_int",
               (I_u ** (1 / 3) - 7.5 ** (1 / 3)) / (15.0 ** (1 / 3) - 7.5 ** (1 / 3)), "—")
h_d = E.paso("E3", "h_d", hd_c75 + t_int * (hd_c15 - hd_c75), "m")
raz_pie = E.paso("E4", "raz_pie", h_d / hd_pie, "—")
# ASCE 7 evaluado en unidades imperiales y devuelto a metros (S6): el contraste
PIE, PSF = 0.3048, 20.8854362
Iu_asce = E.paso("E5", "Iu_asce", 120.0, "m")       # la curva que peor cierra de las cinco
hd_asce_120 = E.paso("E5", "hd_asce_120",
                     (0.43 * (Iu_asce / PIE) ** (1 / 3)
                      * (p_g * PSF + 10.0) ** 0.25 - 1.5) * PIE, "m")
raz_asce = E.paso("E5", "raz_asce", hd_asce_120 / hd_c120, "—")

# ------------------------------------------------------------ D · la desbalanceada
raz_theta = E.paso("D1", "raz_theta", theta_techo / theta_min, "—")
gamma_nieve = E.paso("D2", "gamma_nieve", min(0.426 * p_g + 2.2, gamma_tope), "kN/m3")
L_ac = E.paso("D3", "L_ac", 8.0 * math.sqrt(S_pend) * h_d / 3.0, "m")
frac_faldon = E.paso("D3", "frac_faldon", L_ac / W, "—")
p_d = E.paso("D4", "p_d", h_d * gamma_nieve / math.sqrt(S_pend), "kN/m2")
p_bar = E.paso("D5", "p_bar", 0.3 * p_s, "kN/m2")
p_pico = E.paso("D5", "p_pico", p_s + p_d, "kN/m2")
raz_pico = E.paso("D5", "raz_pico", p_pico / p_s, "—")
F_bal = E.paso("D6", "F_bal", p_s * s_marco * L_luz, "kN")
F_des = E.paso("D6", "F_des",
               p_bar * s_marco * W + p_s * s_marco * W + p_d * s_marco * L_ac, "kN")
raz_des = E.paso("D6", "raz_des", F_des / F_bal, "—")

# ------------------------------------------------------------ Sale
E.sale("p_g", p_g, "kN/m2", paso="A1", heredan=["05"])
E.sale("p_f", p_f, "kN/m2", paso="B4", heredan=["05", "06"])
E.sale("p_s", p_s, "kN/m2", paso="C4", heredan=["06", "07"])
E.sale("p_bar", p_bar, "kN/m2", paso="D5", heredan=["07"])
E.sale("p_pico", p_pico, "kN/m2", paso="D5", heredan=["07"])
E.sale("L_ac", L_ac, "m", paso="D3", heredan=["07"])
E.sale("theta_techo", theta_techo, "°", paso="C1", heredan=["07", "11"])
E.sale("S_pend", S_pend, "—", paso="C2", heredan=["05", "07", "11", "12"])

# lo que el memo 02 de Guias_Interactivas imprimió en su `## Sale`
E.publicado({
    "p_g": "1,50", "p_f": "1,26000", "p_s": "1,26000", "p_bar": "0,37800",
    "p_pico": "2,11807", "L_ac": "4,02993", "theta_techo": "11,30993",
    "S_pend": "5,00000",
})

if __name__ == "__main__":
    raise SystemExit(main(sys.argv, E))
