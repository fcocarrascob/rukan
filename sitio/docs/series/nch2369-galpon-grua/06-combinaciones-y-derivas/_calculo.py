"""Eslabón 06 — combinaciones y derivas: la componente vertical supera en 1,81 al
corte horizontal de diseño, y el desplazamiento se calcula como si el corte fuera
R+1 veces mayor.

    python sitio/docs/series/nch2369-galpon-grua/06-combinaciones-y-derivas/_calculo.py [salida]

Hereda de los cinco eslabones anteriores. Se arma el estado sísmico
direccionalmente combinado, se escriben las combinaciones de §4.5.1 y se verifica
§6.3 y §6.4. Transcrito del memo 06 de `Guias_Interactivas`, que leyó las
cláusulas del PDF (ver la tabla de referencias de `index.md`).

Cuatro cosas que este eslabón hace y conviene no perder de vista al leerlo:

* **El vertical de §5.7.1 no lleva reducción.** No se divide por `R` ni por `R*`,
  y el recorte de §5.13 no lo toca porque no sale del análisis sísmico. Por eso
  supera al horizontal de diseño.
* **El 1,2 de §5.7.1 es el pico de la ruta modal redondeado a un decimal**, y en
  el suelo C ese redondeo quedó 0,36 % corto. La ventana donde la modal gobierna
  se resuelve por bisección sobre la Ec. (4), no se declara.
* **La deriva de §6.1 no se divide por `R*` y §5.13 la excluye del recorte.** El
  factor entre las dos escalas es exactamente `R + 1`, y E3 lo obtiene por un
  segundo camino que no comparte una operación con el primero.
* **El límite que manda no es §6.3 sino AIST §5.3**, seis veces más estricto y
  por una razón que no depende de la altura.

**Todos los pasos se redondean a cinco decimales**, que es lo que el memo imprime
y con lo que sustituye en el paso siguiente; el modelo independiente del memo hacía
lo mismo (`r5` en su `.check.js`). Las cifras que entran de otros eslabones se
consumen también con los decimales que ese eslabón publicó: `_p` marca esas
variables.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3]))          # sitio/
from serie import Eslabon, main  # noqa: E402

E = Eslabon("nch2369-galpon-grua", orden=6, slug="combinaciones-y-derivas",
            titulo="Combinaciones y derivas",
            normas=["NCh2369:2025", "NCh3171:2017", "AIST TR-13:2021", "NCh431:2010"],
            carpeta=AQUI)


def r5(x: float) -> float:
    """Cinco decimales: la precisión con que el memo imprime y sustituye.

    Redondeo **medio hacia arriba**, que es el de `Math.round` del modelo
    independiente del memo, y no el medio-al-par de `round()` de Python: el pico
    del espectro vertical de referencia cae exactamente en un medio
    (0,7 · 1,23695 = 0,865865) y las dos reglas dan cifras distintas.
    """
    return math.floor(float(x) * 1e5 + 0.5) / 1e5


# La Tabla 6 entera y los tres coeficientes de §5.7.1, que C3 necesita para
# recorrer las veinticinco combinaciones de zona y suelo. No producen ninguna
# salida: solo respaldan el máximo que la prosa cita.
TABLA6 = {"A": 0.90, "B": 1.00, "C": 1.05, "D": 1.00, "E": 1.00}
CV_COEF = {"A": 1.2, "B": 1.2, "C": 1.2, "D": 1.1, "E": 1.0}

# ------------------------------------------------------------ lo que entra
I = E.entra("I", de="01", paso="A1")
h_libre = E.entra("h_libre", de="01", paso="S1")
h_riel = E.entra("h_riel", de="01", paso="S3")
R_T7 = E.entra("R_T7", de="01", paso="D1")
p_f = E.entra("p_f", de="02", paso="B4")
p_s = E.entra("p_s", de="02", paso="C4")
wb_ruedas = E.entra("wb_ruedas", de="03", paso="S2")
A_r = E.entra("A_r", de="04", paso="A1")
S_suelo = E.entra("S_suelo", de="04", paso="A2")
r_s = E.entra("r_s", de="04", paso="A2")
T_0 = E.entra("T_0", de="04", paso="A2")
p_suelo = E.entra("p_suelo", de="04", paso="A2")
q_s = E.entra("q_s", de="04", paso="A2")
T_pico = E.entra("T_pico", de="04", paso="B2")
Sa_pico = E.entra("Sa_pico", de="04", paso="B2")
ArS = E.entra("ArS", de="04", paso="A3")
f_xi = E.entra("f_xi", de="04", paso="B1")
T_star_X = E.entra("T_star_X", de="04", paso="S2")
T_star_Y = E.entra("T_star_Y", de="04", paso="S2")
R_star_X = E.entra("R_star_X", de="04", paso="C4")
R_star_Y = E.entra("R_star_Y", de="04", paso="C5")
Sa_ref_X = E.entra("Sa_ref_X", de="04", paso="C4")
Sa_ref_Y = E.entra("Sa_ref_Y", de="04", paso="C5")
A_planta = E.entra("A_planta", de="05", paso="A2")
A_muros = E.entra("A_muros", de="05", paso="A2")
W_edificio = E.entra("W_edificio", de="05", paso="A3")
Wgrua_sc = E.entra("Wgrua_sc", de="05", paso="C3")
P_sismico = E.entra("P_sismico", de="05", paso="C4")
C_dis = E.entra("C_dis", de="05", paso="D3")
Q0_X = E.entra("Q0_X", de="05", paso="D5")
Q0_Y = E.entra("Q0_Y", de="05", paso="D5")

# lo heredado, con los decimales que su eslabón imprimió: es lo que el memo sustituyó
f_xi_p, Sa_ref_X_p, Sa_ref_Y_p = r5(f_xi), r5(Sa_ref_X), r5(Sa_ref_Y)
T_pico_p, Sa_pico_p = r5(T_pico), r5(Sa_pico)
Q0_p, C_dis_p = r5(Q0_Y), r5(C_dis)

# ------------------------------------------------------------ el caso
g_grav = E.caso("g_grav", 9.81, "m/s2")
R_V = E.caso("R_V", 2.00, "—")                     # §5.4, fijo para la vertical
xi_V = E.caso("xi_V", 0.03, "—")                   # §5.4, fijo para la vertical
xi_ref = E.caso("xi_ref", 0.05, "—")               # §5.4.2
cv_ABC = E.caso("cv_ABC", 1.2, "—")                # §5.7.1, suelos A, B y C
cv_D = E.caso("cv_D", 1.1, "—")                    # §5.7.1, suelo D
A_r_z3 = E.caso("A_r_z3", 0.56, "g")               # Tabla 3, la zona más alta de Chile
g_techo = E.caso("g_techo", 0.37278, "kN/m2")      # del 05 · A3
g_cubierta = E.caso("g_cubierta", 0.12, "kN/m2")   # del 05 · S1
g_muros = E.caso("g_muros", 0.10, "kN/m2")         # del 05 · S1
w_columna = E.caso("w_columna", 1.75, "kN/m")      # del 05 · S1
n_columnas = E.caso("n_columnas", 10, "—")
w_carrilera = E.caso("w_carrilera", 1.20, "kN/m")  # del 05 · S1
L_carrilera = E.caso("L_carrilera", 60.0, "m")
P_eq = E.caso("P_eq", 12.0, "kN")                  # del 05 · S1
n_marcos = E.caso("n_marcos", 5, "—")
frac_nieve = E.caso("frac_nieve", 0.20, "—")       # NCh3171 §9.1.1, combinación (5)
t32_tra = E.caso("t32_tra", 0.20, "—")             # del 03, los «dos veintes» de AIST
deriva_lim = E.caso("deriva_lim", 0.015, "—")      # §6.3
grua_lim = E.caso("grua_lim", 400.0, "—")          # AIST §5.3, h/400
pulgada = E.caso("pulgada", 25.40, "mm")           # AIST §5.3, el tope de 2 in
c_max = E.caso("c_max", 2.75, "—")                 # Ec. (13), para el barrido de D3
f_100 = E.caso("f_100", 1.0, "—")                  # §4.5.2, la componente plena
f_30 = E.caso("f_30", 0.3, "—")                    # §4.5.2, la componente reducida


# ------------------------------------- la Ec. (3) y la Ec. (4), en unidades de A_r S
def forma_H(u: float) -> float:
    """La forma de la Ec. (3) en función de `u = T/T_0`, sin el `A_r S`."""
    return (1 + r_s * u ** p_suelo) / (1 + u ** q_s)


# el máximo de esa forma: con `q = 2p`, `u = (T/T_0)^p` deja `r u² + 2u - r = 0`
assert abs(q_s - 2 * p_suelo) < 1e-12, "el pico en forma cerrada exige q = 2p"
U_PICO = ((math.sqrt(1.0 + r_s ** 2) - 1.0) / r_s) ** (1.0 / p_suelo)

# ------------------------------------------------------------ A · las dos escalas
C_dis_re = E.paso("A1", "C_dis_re", r5(Q0_p / P_sismico), "—")
V_desp = E.paso("A2", "V_desp", r5(I * f_xi_p * Sa_ref_Y_p * P_sismico), "kN")
escala = E.paso("A2", "escala", r5(V_desp / Q0_p), "—")

# ------------------------------------------------------------ B · la componente vertical
C_V = E.paso("B1", "C_V", r5(cv_ABC * I * A_r * S_suelo), "—")
E_z = E.paso("B2", "E_z", r5(C_V * P_sismico), "kN")
Ez_sobre_Q0 = E.paso("B2", "Ez_sobre_Q0", r5(E_z / Q0_p), "—")
W_techo = E.paso("B3", "W_techo",
                 g_techo * A_planta + g_cubierta * A_planta + P_eq * n_marcos, "kN")
W_carril = E.paso("B3", "W_carril", w_carrilera * L_carrilera + Wgrua_sc, "kN")
W_muros = E.paso("B3", "W_muros",
                 g_muros * A_muros + w_columna * h_libre * n_columnas, "kN")
Ez_techo = E.paso("B3", "Ez_techo", r5(C_V * W_techo), "kN")
Ez_carril = E.paso("B3", "Ez_carril", r5(C_V * W_carril), "kN")
Ez_muros = E.paso("B3", "Ez_muros", r5(C_V * W_muros), "kN")
Ez_grua = E.paso("B3", "Ez_grua", r5(C_V * Wgrua_sc), "kN")
Ez_suma = E.paso("B3", "Ez_suma", r5(Ez_techo + Ez_carril + Ez_muros), "kN")
raz_veintes = E.paso("B4", "raz_veintes", r5(C_V / t32_tra), "—")
f_xiV = E.paso("B5", "f_xiV", r5((xi_ref / xi_V) ** 0.4), "—")
TV_pico = E.paso("B5", "TV_pico", r5(T_pico_p / 1.7), "s")
SaV_pico = E.paso("B5", "SaV_pico", r5(0.7 * Sa_pico_p), "g")
SaV_dis_pico = E.paso("B5", "SaV_dis_pico", r5(I * SaV_pico * f_xiV / R_V), "g")
raz_pico_modal = E.paso("B6", "raz_pico_modal", r5(SaV_dis_pico / C_V), "—")
coef_max_modal = E.paso("B6", "coef_max_modal",
                        r5(0.7 * forma_H(U_PICO) * f_xiV / R_V), "—")


def _cruce(a: float, b: float, objetivo: float) -> float:
    """Bisección sobre `forma_H(u) = objetivo`; `a` y `b` a lados distintos."""
    fa = forma_H(a) - objetivo
    for _ in range(300):
        m = 0.5 * (a + b)
        fm = forma_H(m) - objetivo
        if fa * fm <= 0:
            b = m
        else:
            a, fa = m, fm
    return 0.5 * (a + b)


OBJETIVO = cv_ABC * R_V / (0.7 * f_xiV)            # la recta del estático, en A_r S
T_cru1 = E.paso("B6", "T_cru1", r5(_cruce(1e-6, U_PICO, OBJETIVO) * T_0 / 1.7), "s")
T_cru2 = E.paso("B6", "T_cru2", r5(_cruce(60.0, U_PICO, OBJETIVO) * T_0 / 1.7), "s")
ancho_ventana = E.paso("B6", "ancho_ventana", r5(T_cru2 - T_cru1), "s")
raz_rutas_D = E.paso("B7", "raz_rutas_D", r5(cv_D * R_V / (0.7 * f_xiV)), "—")
raz_rutas_C = E.paso("B7", "raz_rutas_C", r5(cv_ABC * R_V / (0.7 * f_xiV)), "—")

# ------------------------------------------------------------ C · las combinaciones
D_grav = E.paso("C1", "D_grav", r5(W_edificio + Wgrua_sc), "kN")
Pu_max = E.paso("C2", "Pu_max", r5(1.2 * D_grav + E_z), "kN")
aporte_vert = E.paso("C2", "aporte_vert", r5(Pu_max / (1.2 * D_grav)), "—")
Pu_desc = E.paso("C3", "Pu_desc", r5(0.9 * D_grav - E_z), "kN")
frac_vert = E.paso("C3", "frac_vert", r5(E_z / (0.9 * D_grav)), "—")
CV_max_chile = E.paso("C3", "CV_max_chile", r5(cv_ABC * A_r_z3 * S_suelo), "—")
assert CV_max_chile == r5(max(A_r_z3 * TABLA6[k] * CV_COEF[k] for k in TABLA6)), \
    "el mayor C_V de Chile no es el de zona 3 con suelo C"
margen_09 = E.paso("C3", "margen_09", r5(0.90 / CV_max_chile), "—")
Pu_desc_sg = E.paso("C4", "Pu_desc_sg", r5((0.90 - C_V) * W_edificio), "kN")
peor_sg = E.paso("C4", "peor_sg", r5(Pu_desc_sg / Pu_desc), "—")
Pu_desc_ASD = E.paso("C5", "Pu_desc_ASD", r5(D_grav - 0.70 * E_z), "kN")
raz_ASD = E.paso("C5", "raz_ASD", r5(Pu_desc_ASD / Pu_desc), "—")
n_estados = E.paso("C5", "n_estados", 3 * 2 ** 3, "—")

# ------------------------------------------------------------ D · la nieve concurrente
S_comb = E.paso("D1", "S_comb", r5(frac_nieve * p_s * A_planta), "kN")
Pu_nieve = E.paso("D2", "Pu_nieve", r5(Pu_max + S_comb), "kN")
aporte_nieve = E.paso("D2", "aporte_nieve", r5(S_comb / Pu_max), "—")
P_masa = E.paso("D3", "P_masa", r5(P_sismico + S_comb), "kN")
sube_todo = E.paso("D3", "sube_todo", r5(P_masa / P_sismico), "—")
# El memo publicó 357,53340 acá: evaluó esta línea con el `f_xi` **exacto** y no
# con el 1,44270 que su propia fórmula imprime. Esta página evalúa la fórmula tal
# como está escrita, con la regla uniforme del eslabón, y da 357,53342. La
# diferencia es de 2·10⁻⁵ kN y queda anotada en `## Límites`.
Q0_nieve = E.paso("D3", "Q0_nieve",
                  r5(c_max * I * A_r * S_suelo / (R_T7 + 1) * f_xi_p * P_masa), "kN")
Pu_ambas = E.paso("D3", "Pu_ambas",
                  r5(1.2 * D_grav + r5(C_V * P_masa) + S_comb), "kN")
abierto = E.paso("D3", "abierto", r5(Pu_ambas / Pu_nieve), "—")

# ------------------------------------------------------------ E · la deriva
d_lim = E.paso("E1", "d_lim", r5(deriva_lim * h_libre * 1000), "mm")


def _desp(T: float, sa_ref: float) -> float:
    """§6.1 con la masa en un nivel: el desplazamiento espectral, en mm."""
    return r5(I * f_xi_p * sa_ref * g_grav * T * T / (4 * math.pi ** 2) * 1e3)


d_X = E.paso("E2", "d_X", _desp(T_star_X, Sa_ref_X_p), "mm")
d_Y = E.paso("E2", "d_Y", _desp(T_star_Y, Sa_ref_Y_p), "mm")
uso_X = E.paso("E2", "uso_X", r5(d_X / d_lim), "—")
uso_Y = E.paso("E2", "uso_Y", r5(d_Y / d_lim), "—")
frac_altura = E.paso("E2", "frac_altura", r5(d_Y / (h_libre * 1000)), "—")
K_Y = E.paso("E3", "K_Y", r5(P_sismico / g_grav * (2 * math.pi / T_star_Y) ** 2), "kN/m")
d_Y_por_K = E.paso("E3", "d_Y_por_K", r5(V_desp / K_Y * 1e3), "mm")
K_Y_marco = E.paso("E3", "K_Y_marco", r5(K_Y / n_marcos), "kN/m")
uso_10030 = E.paso("E4", "uso_10030", r5((d_Y + f_30 * d_X) / d_lim), "—")
dos_pulgadas = E.paso("E5", "dos_pulgadas", r5(2 * pulgada), "mm")
flojo_2in = E.paso("E5", "flojo_2in", r5(dos_pulgadas / (h_riel * 1000 / grua_lim)), "—")
dlim_grua = E.paso("E5", "dlim_grua", r5(min(h_riel * 1000 / grua_lim, dos_pulgadas)), "mm")
mas_estricto = E.paso("E5", "mas_estricto",
                      r5(deriva_lim * h_riel * 1000 / dlim_grua), "—")
sismo_sobre_grua = E.paso("E5", "sismo_sobre_grua", r5(d_Y / dlim_grua), "—")
h_gobierna_2in = E.paso("E5", "h_gobierna_2in", r5(dos_pulgadas / (1 / grua_lim)), "mm")
d_Y_ing = E.paso("E6", "d_Y_ing", r5(d_Y / (R_T7 + 1)), "mm")
uso_ing_grua = E.paso("E6", "uso_ing_grua", r5(d_Y_ing / dlim_grua), "—")

# ------------------------------------------------------------ F · P-Δ y el vuelco
theta_Y = E.paso("F1", "theta_Y", r5(P_sismico * d_Y / (Q0_p * h_libre * 1000)), "—")
theta_X = E.paso("F1", "theta_X", r5(P_sismico * d_X / (Q0_p * h_libre * 1000)), "—")
f_PDelta_Y = E.paso("F1", "f_PDelta_Y", r5(1 / (1 - theta_Y)), "—")


def _umbral(fh: float, fv: float) -> float:
    """La altura del centro de gravedad sobre la que la grúa levanta una rueda."""
    return r5((1 - fv * C_V) * (wb_ruedas / 2) / (fh * C_dis_p))


umb_ec1 = E.paso("F2", "umb_ec1", _umbral(f_100, f_30), "m")
umb_ec3 = E.paso("F2", "umb_ec3", _umbral(f_30, f_100), "m")
umb_pleno = E.paso("F2", "umb_pleno", _umbral(f_100, f_100), "m")
sube_10030 = E.paso("F2", "sube_10030", r5(umb_ec1 / umb_pleno), "—")
sobre_trocha = E.paso("F2", "sobre_trocha", r5(umb_ec1 / wb_ruedas), "—")

# ------------------------------------------------------------ Sale
E.sale("C_V", C_V, "—", paso="B1", heredan=["07", "08", "10", "13"])
E.sale("E_z", E_z, "kN", paso="B2", heredan=["07", "10", "13"])
E.sale("Ez_techo", Ez_techo, "kN", paso="B3", heredan=["07"])
E.sale("Ez_carril", Ez_carril, "kN", paso="B3", heredan=["08", "10"])
E.sale("D_grav", D_grav, "kN", paso="C1", heredan=["07", "10", "13"])
E.sale("Pu_max", Pu_max, "kN", paso="C2", heredan=["10", "13"])
E.sale("Pu_desc", Pu_desc, "kN", paso="C3", heredan=["10", "13"])
E.sale("S_comb", S_comb, "kN", paso="D1", heredan=["07"])
E.sale("Pu_nieve", Pu_nieve, "kN", paso="D2", heredan=["07"])
E.sale("d_lim", d_lim, "mm", paso="E1", heredan=["07", "12"])
E.sale("d_Y", d_Y, "mm", paso="E2", heredan=["07"])
E.sale("dlim_grua", dlim_grua, "mm", paso="E5", heredan=["07", "08", "10", "11", "12"])
E.sale("f_PDelta_Y", f_PDelta_Y, "—", paso="F1", heredan=["07"])

# lo que el memo 06 de Guias_Interactivas imprimió en su `## Sale`
E.publicado({
    "C_V": "0,52920", "E_z": "548,82538", "Ez_techo": "227,33638",
    "Ez_carril": "159,81840", "D_grav": "1037,08500", "Pu_max": "1793,32738",
    "Pu_desc": "384,55112", "S_comb": "189,00000", "Pu_nieve": "1982,32738",
    "d_lim": "157,50", "d_Y": "69,56272", "dlim_grua": "18,75",
    "f_PDelta_Y": "1,02325",
})

if __name__ == "__main__":
    raise SystemExit(main(sys.argv, E))
