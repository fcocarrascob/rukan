"""Caso 11 — datos del galpón con puente grúa de la serie `nch2369-galpon-grua`.

Este módulo **no analiza nada**: es el juego de datos del caso, igual que
`case10_data.py`. Lo distinto es de dónde vienen: no de un script de SAP2000 sino
de los doce eslabones ya verificados de la serie
`F:\\Proyectos_Python\\Guias_Interactivas\\memos\\estructural\\nch2369-galpon-grua-*`.
Cada constante lleva el eslabón y el paso que la publica, y ese es el contrato:
si acá aparece un número que ningún memo publica, es un número inventado.

El caso
-------
Galpón industrial de acero, una nave a dos aguas, en precordillera de Ñuble
(zona 2, suelo C). Luz 25,00 m, largo 30,00 m en cuatro vanos de 7,50, alero
10,50 m y cumbrera 13,00. Marcos de momento de alma variable en la dirección
transversal, con **bases empotradas**; arriostramiento concéntrico longitudinal
en **dos** de los cuatro vanos —los otros dos llevan portones— más
arriostramiento continuo de techo. Puente grúa birriel de 200 kN, sin cabina,
con el riel a 7,50 m.

Ejes, y no es cosmético
-----------------------
Se adopta **la convención de los memos**, que es la contraria a la de los casos
7 y 10 de esta misma escalera:

    X  longitudinal, 0 a 30 m   — la dirección arriostrada, la del recorrido de
                                  la grúa. Es la de `T_star_X` del 04.
    Y  transversal,  0 a 25 m   — la luz, el plano de los marcos de momento.
                                  Es la de `T_star_Y`.
    Z  vertical,     0 a 13 m

Los marcos están en x = 0; 7,5; 15; 22,5; 30 y cada uno ocupa un plano Y-Z.
Cambiar esto para parecerse al caso 10 obligaría a traducir cada número de la
serie al leerlo, que es exactamente donde se pierden los signos.

Convención de ejes locales de `rukan.loads.local_axes`: `ey = û(vecxz × ex)` y
`ez = ex × ey`. Para que el eje fuerte (`Iz`) flecte **en el plano del marco**,
tanto columnas como rafters llevan `vecxz = (1, 0, 0)`, que deja `ey` dentro del
plano Y-Z. Los cajones de puntal y diagonal tienen `Iy = Iz` y su `vecxz` solo
tiene que no ser paralelo a la barra.
"""

from __future__ import annotations

import math

# ============================ GEOMETRÍA ============================
# 01 · S1 y `## Caso`; la cumbrera y el largo los deriva 05 · A1.
LUZ = 25.0            # m, entre ejes de columnas          (01 · S1)
SEP = 7.5             # m, separación de marcos            (01 · S1)
NMARCOS = 5           # 4 vanos                            (01 · S1)
LARGO = (NMARCOS - 1) * SEP                              # 30,00 m (05 · A1)
H_ALERO = 10.5        # m, altura libre de columna         (01 · S1)
S_PEND = 5.0          # razón horizontal de la pendiente   (02 · C2)
H_CUMB = H_ALERO + (LUZ / 2.0) / S_PEND                  # 13,00 m (05 · A1)
PEND = 1.0 / S_PEND   # 20 %                               (01 · S1)

# Puente grúa. La luz de 23,00 deja el riel a 1,00 m del eje de columna.
LUZ_GRUA = 23.0       # m                                  (01 · S3)
E_COL_RIEL = (LUZ - LUZ_GRUA) / 2.0                      # 1,00 m  (10 · A2)
Z_RIEL = 7.5          # m, nivel superior del riel         (01 · S3)
H_RIEL_PERFIL = 0.13176   # m, riel ASCE 85 lb/yd          (08 · S3)
D_CARRIL = 0.684      # m, canto de la viga carrilera      (08 · `## Caso`)
H_ASIENTO = Z_RIEL - H_RIEL_PERFIL - D_CARRIL            # 6,68424 m (10 · A2)
X_G_TOPE = 2.0        # m, tope de recorrido del puente    (12 · C1)

# Arriostramiento continuo de techo: tres espacios por agua medidos SOBRE el
# rafter, y siete líneas longitudinales — dos aleros, dos intermedias por agua y
# la cumbrera, que las dos aguas comparten.                (11 · C3 y C4)
NPAN_AGUA = 3
NJ = 2 * NPAN_AGUA                                        # 6 espacios, 7 líneas
L_RAFTER = math.hypot(LUZ / 2.0, (LUZ / 2.0) / S_PEND)   # 12,74755 m (11 · C1)
B_PAN_TECHO = L_RAFTER / NPAN_AGUA                        # 4,24918 m (11 · C3)
L_DIAG_TECHO = math.hypot(SEP, B_PAN_TECHO)               # 8,62007 m (11 · C3)

# Vanos y cuáles se arriostran. El 12 los ubica en los ejes extremos: los dos
# centrales llevan portón.                                 (01 · S2 · 12 · C4)
BAYS = [1, 2, 3, 4]
BAYS_ARR = [1, 4]
WALLS = {"A": 0.0, "B": LUZ}      # los dos muros longitudinales, en y = 0 y 25

# ============================ SECCIONES ============================
# Todas soldadas por planchas. El alma variable no está en ningún catálogo.
# Columna del edificio 1 050 -> 750, alas 300 × 22, alma 14   (07 · `## Caso`)
COL_BF, COL_TF, COL_TW = 0.300, 0.022, 0.014
COL_D_BASE, COL_D_NUDO = 1.050, 0.750
# Rafter 750 -> 425, alas 250 × 20, alma 12                  (07 · `## Caso`)
RAF_BF, RAF_TF, RAF_TW = 0.250, 0.020, 0.012
RAF_D_NUDO, RAF_D_CUMB = 0.750, 0.425
# Fuste de grúa 400, alas 300 × 16, alma 10                  (10 · S2)
FUS_D, FUS_BF, FUS_TF, FUS_TW = 0.400, 0.300, 0.016, 0.010
# Placa de alma que une los dos fustes, continua            (10 · S3)
TP_ALMA = 0.010
# Cajones del arriostramiento de techo                       (11 · E1 y E2)
TUBO_DIAG = (0.125, 0.005)     # A = 2 400 mm²
TUBO_PUNT = (0.200, 0.006)     # A = 4 656 mm²
# Diagonal del panel longitudinal: parámetro ilustrativo, es del 13 (12 · S1)
TUBO_PANEL = (0.125, 0.005)
# Viga carrilera soldada: ala superior 350 × 20, alma 650 × 8,
# ala inferior 250 × 14                                      (08 · `## Caso`)
CAR_BFS, CAR_TFS = 0.350, 0.020
CAR_HW, CAR_TW = 0.650, 0.008
CAR_BFI, CAR_TFI = 0.250, 0.014

# ============================ MATERIAL =============================
# ASTM A572 Gr. 50 en plancha.                               (07 · S5 · 10 · S1)
E_STEEL = 2.0e8       # kN/m²  (200 000 MPa)
NU = 0.3
FY = 345.0e3          # kN/m²  (345 MPa)
RY = 1.10
RHO_STEEL = 7.85      # tonne/m³
G_MEMO = 9.81         # m/s² — el que la serie usa en 05 · A3 y 07 · B5
XI = 0.02             # amortiguamiento, marco de momento soldado (01)

# ============================= CARGAS ==============================
# Los seis sumandos de W_edificio, en el orden del memo.     (05 · A3)
G_TECHO = 38.0 * G_MEMO / 1000.0   # 0,37278 kN/m² — estructura de techo
G_CUBIERTA = 0.12                  # kN/m² — cubierta
G_REVEST = 0.10                    # kN/m² — revestimiento de muros
W_COL_LIN = 1.75                   # kN/m por columna, 10 columnas
W_CARRIL_LIN = 1.20                # kN/m por línea de carrilera, 60 m
W_EQUIPOS = 12.00                  # kN por marco                (01 · S5)

A_PLANTA = LUZ * LARGO                                     # 750,00 m² (05 · A2)
A_MUROS = (2 * LARGO * H_ALERO + 2 * LUZ * H_ALERO
           + LUZ * (H_CUMB - H_ALERO))                     # 1 217,50 m² (05 · A2)
W_EDIFICIO = (G_TECHO * A_PLANTA + G_CUBIERTA * A_PLANTA
              + G_REVEST * A_MUROS + W_COL_LIN * H_ALERO * 10
              + W_CARRIL_LIN * 2 * LARGO
              + W_EQUIPOS * NMARCOS)                       # 807,085 kN (05 · A3)

# Nieve.                                                    (02 · B4 y C4)
P_F = 1.26            # kN/m² — nieve plana
P_S = 1.26            # kN/m² — nieve balanceada sobre el techo
P_BAR = 0.378         # kN/m² — desbalanceada, lado de barlovento (02 · D5)
P_PICO = 2.11807      # kN/m² — pico de sotavento
L_AC = 4.02993        # m — largo de la acumulación

# Grúa. Todas de 03; la 12 fija dónde se estaciona.
WB_PUENTE = 190.0     # kN — puente                          (03 · S2)
WT_CARRO = 40.0       # kN — carro                           (03 · S2)
W_GRUA_SC = WB_PUENTE + WT_CARRO                           # 230,00 kN (05 · C3)
WB_RUEDAS = 3.4       # m — base de ruedas por testero       (03 · S2)
RW_MAX = 161.23913    # kN — reacción de rueda, sin impacto   (03 · B2)
RW_MIN = 53.76087     # kN                                   (03 · B3)
RV_MAX = 193.48696    # kN — con impacto vertical            (03 · C1)
SS_TOTAL = 60.0       # kN — empuje lateral total            (03 · D1)
SS_CARRIL = 30.0      # kN — por carrilera                   (03 · D3)
T_LONG = 86.0         # kN — tracción longitudinal           (03 · E1)

# Sitio y espectro.                                          (04)
ZONA, SUELO = 2, "C"
A_R = 0.42            # g                                    (04 · A1)
S_SUELO = 1.05                                             # (04 · A2)
AR_S = 0.441          # g                                    (04 · A3)
R_TABLA = 5.0                                              # (01)
IMPORTANCIA = 1.0                                          # (01 · S7)
F_XI = 1.4427                                              # (04 · B1)
CR_T1 = 0.28          # s — codo de la Ec. (1b)             (04 · C2)
T_0, R_S, P_SUELO, Q_S = 0.40, 4.50, 1.50, 3.00            # (04 · A2)

# Peso sísmico y corte de diseño que la serie ya publica, para contrastar.
P_SISMICO = W_EDIFICIO + W_GRUA_SC                         # 1 037,085 kN (05 · C4)
C_DIS = 0.29161                                            # (05 · D3)
Q0_MEMO = 302.41994   # kN, las dos direcciones             (05 · D5)

# Lo declarado que este modelo viene a reemplazar.
DECLARADO = {
    "T_star_X": (0.20, "s", "04 · S2"),
    "T_star_Y": (0.40, "s", "04 · S2"),
    "k_Y": (5612.11747, "kN/m", "07 · S1"),
    "k_riel": (15057.33721, "kN/m", "07 · S1"),
    "Mbase_u": (1035.55049, "kN·m", "07 · S1"),
    "k_esc": (2.24801, "—", "10 · D6"),
}


# ---------------------- Propiedades de sección ----------------------
def i_props(d: float, bf: float, tf: float, tw: float) -> tuple[float, float, float, float]:
    """Doble T soldada doblemente simétrica: `(A, I_fuerte, I_debil, J)`.

    `I_fuerte` flecta con el canto `d`; `J = Σbt³/3`, la fórmula de manual para
    una sección abierta.
    """
    h = d - 2.0 * tf
    A = 2.0 * bf * tf + h * tw
    i_f = tw * h ** 3 / 12.0 + 2.0 * (bf * tf ** 3 / 12.0 + bf * tf * ((d - tf) / 2.0) ** 2)
    i_d = 2.0 * tf * bf ** 3 / 12.0 + h * tw ** 3 / 12.0
    j = (2.0 * bf * tf ** 3 + h * tw ** 3) / 3.0
    return A, i_f, i_d, j


def box_props(b: float, t: float) -> tuple[float, float, float]:
    """Cajón cuadrado `b × b × t`: `(A, I, J)`. `J = t(b − t)³` es Bredt."""
    bi = b - 2.0 * t
    return b * b - bi * bi, (b ** 4 - bi ** 4) / 12.0, t * (b - t) ** 3


def carrilera_props() -> tuple[float, float, float, float]:
    """Viga carrilera monosimétrica: `(A, I_fuerte, I_debil, J)`.

    Tres rectángulos —ala superior, alma, ala inferior— con el eje neutro donde
    lo pone el equilibrio de áreas, no en el medio del canto.
    """
    partes = [(CAR_BFS * CAR_TFS, CAR_TFS / 2.0, CAR_BFS, CAR_TFS),
              (CAR_TW * CAR_HW, CAR_TFS + CAR_HW / 2.0, CAR_TW, CAR_HW),
              (CAR_BFI * CAR_TFI, CAR_TFS + CAR_HW + CAR_TFI / 2.0, CAR_BFI, CAR_TFI)]
    A = sum(a for a, _, _, _ in partes)
    yc = sum(a * y for a, y, _, _ in partes) / A
    i_f = sum(b * h ** 3 / 12.0 + a * (y - yc) ** 2 for a, y, b, h in partes)
    i_d = sum(h * b ** 3 / 12.0 for _, _, b, h in partes)
    j = sum(b * h ** 3 / 3.0 for _, _, b, h in partes)
    return A, i_f, i_d, j


def d_col(z: float) -> float:
    """Canto de la columna del edificio a la cota `z`, en metros.

    Lineal entre 1 050 en la base y 750 en el nudo de alero. En z = 7,50 da
    835,71429 mm, que es lo que el 07 · B3 publica.
    """
    return COL_D_BASE + (COL_D_NUDO - COL_D_BASE) * z / H_ALERO


def d_raf(s: float) -> float:
    """Canto del rafter a la distancia `s` desde el alero, medida sobre el rafter."""
    return RAF_D_NUDO + (RAF_D_CUMB - RAF_D_NUDO) * s / L_RAFTER


def comp_props(z: float) -> tuple[float, float, float, float, float]:
    """Sección compuesta del fuste escalonado a la cota `z`: `(A, ybar, Ix, Iy, J)`.

    Cuatro alas y un alma continua: el fuste del edificio en `y = 0`, la placa de
    unión de 10 mm y el fuste de grúa con su eje sobre el del riel, en
    `y = E_COL_RIEL`. La placa va de la cara interior del fuste del edificio a la
    cara del fuste de grúa que lo mira, así que su largo **crece hacia arriba**:
    la cuña del edificio se adelgaza y el hueco se abre.  (10 · S2, S3 y B3)

    `ybar` se mide desde el eje de la columna, positivo hacia la grúa.
    """
    d = d_col(z)
    hw = d - 2.0 * COL_TF
    y_int = d / 2.0                       # cara interior del fuste del edificio
    y_fus = E_COL_RIEL - FUS_D / 2.0      # cara del fuste de grúa que la mira
    l_placa = y_fus - y_int
    hf = FUS_D - 2.0 * FUS_TF
    # (área, y del centroide, ancho, alto) de cada rectángulo, con el alto en `y`.
    partes = [
        (COL_BF * COL_TF, (d - COL_TF) / 2.0, COL_BF, COL_TF),
        (COL_BF * COL_TF, -(d - COL_TF) / 2.0, COL_BF, COL_TF),
        (COL_TW * hw, 0.0, COL_TW, hw),
        (TP_ALMA * l_placa, (y_int + y_fus) / 2.0, TP_ALMA, l_placa),
        (FUS_BF * FUS_TF, E_COL_RIEL + (FUS_D - FUS_TF) / 2.0, FUS_BF, FUS_TF),
        (FUS_BF * FUS_TF, E_COL_RIEL - (FUS_D - FUS_TF) / 2.0, FUS_BF, FUS_TF),
        (FUS_TW * hf, E_COL_RIEL, FUS_TW, hf),
    ]
    A = sum(a for a, _, _, _ in partes)
    ybar = sum(a * y for a, y, _, _ in partes) / A
    ix = sum(b * h ** 3 / 12.0 + a * (y - ybar) ** 2 for a, y, b, h in partes)
    iy = sum(h * b ** 3 / 12.0 for _, _, b, h in partes)
    j = sum(b * h ** 3 / 3.0 for _, _, b, h in partes)
    return A, ybar, ix, iy, j


# ------------------------- Malla del techo --------------------------
def y_roof(j: int) -> float:
    """Abscisa transversal de la línea `j` del techo (`j = 0..NJ`)."""
    return j * (LUZ / NJ)


def z_roof(j: int) -> float:
    """Cota de la línea `j`: sube hasta la cumbrera y baja."""
    return H_ALERO + min(y_roof(j), LUZ - y_roof(j)) * PEND


def yz_raf(s: float) -> tuple[float, float]:
    """Coordenadas `(y, z)` del punto del rafter a la distancia `s` desde el alero A.

    `s` se mide **sobre el rafter** y recorre las dos aguas: de 0 en el alero A a
    `2·L_RAFTER` en el alero B. Es la abscisa con que se miden los tres espacios
    del arriostramiento de techo (11 · C3), y no es la proyección horizontal.
    """
    k = (LUZ / 2.0) / L_RAFTER
    y = s * k if s <= L_RAFTER else LUZ - (2.0 * L_RAFTER - s) * k
    return y, H_ALERO + min(y, LUZ - y) * PEND


def x_marco(f: int) -> float:
    return (f - 1) * SEP


def trib(f: int) -> float:
    """Ancho tributario del marco `f`: medio vano en las testeras."""
    return SEP / 2.0 if f in (1, NMARCOS) else SEP


# ==================== ENSAMBLE DEL MODELO ==========================
from rukan.model import FrameElement, Material, Model, NodalMass, Node, Section  # noqa: E402

# El marco vive en el plano Y-Z: los GDL fuera de ese plano son Ux, Ry y Rz.
FUERA_DE_PLANO = (1, 5, 6)                   # indices de GDL, base 1
FUERA_DE_PLANO_FIX = (1, 0, 0, 0, 1, 1)      # el mismo, como argumento de ops.fix
EMPOTRADA = (True,) * 6
LIBRE = (False,) * 6
# `vecxz` que deja `ey` dentro del plano del marco, para columnas y rafters.
VEC_MARCO = (1.0, 0.0, 0.0)


def _malla(cortes: list[float], nsub: int) -> list[float]:
    """Subdivide una lista de cortes obligatorios en `nsub` tramos cada uno."""
    out = [cortes[0]]
    for a, b in zip(cortes[:-1], cortes[1:]):
        out += [a + (b - a) * (i + 1) / nsub for i in range(nsub)]
    return out


class Meta:
    """Índices del modelo: nombre <-> id, longitudes y sección de cada barra."""

    def __init__(self) -> None:
        self.node_id: dict[str, int] = {}
        self.node_xyz: dict[str, tuple[float, float, float]] = {}
        self.elem_id: dict[str, int] = {}
        self.elem_len: dict[str, float] = {}
        self.elem_sec: dict[str, str] = {}
        self.bases: list[str] = []
        self.libres: list[str] = []

    def nid(self, n: str) -> int:
        return self.node_id[n]

    def eid(self, n: str) -> int:
        return self.elem_id[n]


class _Armador:
    """Acumulador de nodos, secciones y barras con nombre."""

    def __init__(self) -> None:
        self.meta = Meta()
        self.nodes: list[Node] = []
        self.sections: list[Section] = []
        self.sec_id: dict[str, int] = {}
        self.els: list[FrameElement] = []

    def nodo(self, nm, x, y, z, restr=LIBRE):
        i = len(self.nodes) + 1
        self.nodes.append(Node(i, x, y, z, restr))
        self.meta.node_id[nm] = i
        self.meta.node_xyz[nm] = (x, y, z)
        (self.meta.bases if restr is EMPOTRADA else self.meta.libres).append(nm)
        return nm

    def seccion(self, nm, A, Iy, Iz, J):
        if nm not in self.sec_id:
            i = len(self.sections) + 1
            self.sec_id[nm] = i
            self.sections.append(Section(i, A=A, Iy=Iy, Iz=Iz, J=J))
        return nm

    def barra(self, nm, a, b, sec, vecxz, **kw):
        i = len(self.els) + 1
        self.els.append(FrameElement(i, self.meta.node_id[a], self.meta.node_id[b],
                                     1, self.sec_id[sec], vecxz, **kw))
        self.meta.elem_id[nm] = i
        self.meta.elem_sec[nm] = sec
        self.meta.elem_len[nm] = math.dist(self.meta.node_xyz[a], self.meta.node_xyz[b])
        return nm

    def modelo(self, masses=None) -> Model:
        return Model(nodes=self.nodes,
                     materials=[Material(1, E=E_STEEL, nu=NU, rho=RHO_STEEL)],
                     sections=self.sections, elements=self.els,
                     masses=masses or [])


def _sec_col(ar: _Armador, z: float, escalonada: bool) -> str:
    """Sección de la columna a la cota `z`: compuesta bajo el asiento si escalonada."""
    if escalonada and z < H_ASIENTO:
        A, _, ix, iy, j = comp_props(z)
        return ar.seccion("CMP_%.5f" % z, A=A, Iy=iy, Iz=ix, J=j)
    A, i_f, i_d, j = i_props(d_col(z), COL_BF, COL_TF, COL_TW)
    return ar.seccion("COL_%.5f" % z, A=A, Iy=i_d, Iz=i_f, J=j)


def _sec_raf(ar: _Armador, s: float) -> str:
    A, i_f, i_d, j = i_props(d_raf(s), RAF_BF, RAF_TF, RAF_TW)
    return ar.seccion("RAF_%.5f" % s, A=A, Iy=i_d, Iz=i_f, J=j)


def _marco(ar: _Armador, f: int, nsub: int, escalonada: bool) -> None:
    """Arma el marco `f`: dos columnas de alma variable y dos rafters."""
    x = x_marco(f)
    # Los cortes obligatorios de la columna son los niveles que la serie nombra.
    zc = _malla([0.0, H_ASIENTO, Z_RIEL, H_ALERO], nsub)
    for l, y in WALLS.items():
        for k, z in enumerate(zc):
            if k == 0:
                ar.nodo("K%d%s_0" % (f, l), x, y, 0.0, EMPOTRADA)
            elif k < len(zc) - 1:
                ar.nodo("K%d%s_%d" % (f, l, k), x, y, z)
        # el tope de la columna es el nudo de alero, que es la línea 0 o NJ del techo
        j_alero = 0 if l == "A" else NJ
        ar.nodo("R%d_%d" % (f, j_alero), x, y, H_ALERO)
        for k in range(len(zc) - 1):
            a = "K%d%s_%d" % (f, l, k)
            b = ("R%d_%d" % (f, j_alero) if k == len(zc) - 2
                 else "K%d%s_%d" % (f, l, k + 1))
            zm = 0.5 * (zc[k] + zc[k + 1])
            ar.barra("COL%d%s_%d" % (f, l, k + 1), a, b,
                     _sec_col(ar, zm, escalonada), VEC_MARCO)
    # Rafters: la malla obligatoria son las líneas del arriostramiento de techo.
    sj = _malla([j * B_PAN_TECHO for j in range(NJ + 1)], nsub)

    def linea(k: int) -> int | None:
        """La línea de techo en que cae la estación `k`, o `None` si es intermedia."""
        q = sj[k] / B_PAN_TECHO
        return int(round(q)) if abs(q - round(q)) < 1e-9 else None

    def nom(k: int) -> str:
        j = linea(k)
        return "R%d_%d" % (f, j) if j is not None else "S%d_%d" % (f, k)

    for k, s in enumerate(sj):
        j = linea(k)
        if j is not None:
            if j not in (0, NJ):          # los aleros ya los puso la columna
                ar.nodo("R%d_%d" % (f, j), x, y_roof(j), z_roof(j))
        else:
            yy, zz = yz_raf(s)
            ar.nodo("S%d_%d" % (f, k), x, yy, zz)

    for k in range(len(sj) - 1):
        sm = 0.5 * (sj[k] + sj[k + 1])
        smir = sm if sm <= L_RAFTER else 2 * L_RAFTER - sm
        ar.barra("RAF%d_%d" % (f, k + 1), nom(k), nom(k + 1),
                 _sec_raf(ar, smir), VEC_MARCO)


def build_frame(nsub: int = 14, escalonada: bool = False) -> tuple[Model, Meta]:
    """Un solo marco transversal, en el plano Y-Z, con bases empotradas.

    Es el modelo que el 07 · S1 describe y no ejecuta: alma variable discretizada
    en tramos prismáticos con la sección de su punto medio. Con `nsub = 14` la
    columna lleva 42 tramos —los mismos que el memo declara— y el rafter 84.

    `escalonada` mete la sección compuesta del 10 bajo el nivel del asiento, que
    es lo único que separa al modelo del 07 del modelo del 10.

    Los GDL fuera del plano se fijan en cada nudo libre: un marco plano montado en
    un dominio de seis GDL tiene la matriz singular sin eso, y fijarlos no le quita
    nada porque ninguna carga de este contraste sale del plano.
    """
    ar = _Armador()
    _marco(ar, 1, nsub, escalonada)
    return ar.modelo(), ar.meta


# ======================= EL GALPÓN COMPLETO EN 3D ==========================
# Las barras que no son del marco: puntales y diagonales de techo, y las X de
# los dos vanos arriostrados. Todas son bielas —momentos liberados en los dos
# extremos— porque eso es lo que son: el 11 · C2 las dimensiona por pandeo con
# el punto de cruce, no por flexión.
BIELA = dict(release_y_i=True, release_z_i=True,
             release_y_j=True, release_z_j=True)


def _sec_tubo(ar: "_Armador", nm: str, b: float, t: float) -> str:
    A, I, J = box_props(b, t)
    return ar.seccion(nm, A=A, Iy=I, Iz=I, J=J)


def _vecxz(pa, pb) -> tuple[float, float, float]:
    """Un `vecxz` cualquiera que no sea paralelo a la barra.

    En un cajón `Iy = Iz`, así que la orientación no cambia el análisis; solo
    decide en qué índice sale cada momento. Se toma `ẑ` salvo para las barras
    verticales, que no las hay entre las bielas de este modelo.
    """
    ex = (pb[0] - pa[0], pb[1] - pa[1], pb[2] - pa[2])
    return (0.0, 0.0, 1.0) if math.hypot(ex[0], ex[1]) > 1e-9 else (1.0, 0.0, 0.0)


def build_model(nsub: int = 4, escalonada: bool = True,
                x_grua: float = LARGO / 2.0) -> tuple[Model, Meta]:
    """El galpón completo: cinco marcos, techo arriostrado y dos vanos en X.

    `x_grua` es la abscisa del centro del puente. Por omisión va al centro de la
    nave; el 12 · C1 lo estaciona en `X_G_TOPE` = 2,00 m del marco extremo, que es
    la posición que maximiza la torsión en planta.

    La masa es la del 05 · A3, sumando sus **seis** términos donde cada uno actúa
    —techo y cubierta sobre el techo, revestimiento sobre muros y hastiales,
    columnas sobre columnas, carrileras al nivel del asiento y equipos por
    marco—, más los 230,00 kN de la grúa del 05 · C3. No se usa el peso propio
    de los elementos: la serie fijó su masa por áreas y este modelo tiene que
    consumir la misma, o el contraste compara dos edificios distintos.
    """
    ar = _Armador()
    for f in range(1, NMARCOS + 1):
        _marco(ar, f, nsub, escalonada)

    punt = _sec_tubo(ar, "PUNT", *TUBO_PUNT)
    diag = _sec_tubo(ar, "DIAG", *TUBO_DIAG)
    pan = _sec_tubo(ar, "PANEL", *TUBO_PANEL)

    def biela(nm, a, b, sec):
        ar.barra(nm, a, b, sec,
                 _vecxz(ar.meta.node_xyz[a], ar.meta.node_xyz[b]), **BIELA)

    # Puntales: las siete líneas longitudinales, en los cuatro vanos (11 · C4).
    for b in BAYS:
        for j in range(NJ + 1):
            biela("PUN%d_%d" % (b, j), "R%d_%d" % (b, j), "R%d_%d" % (b + 1, j), punt)
    # Diagonales de techo: una X por panel, 3 por agua y por vano (11 · C4).
    for b in BAYS:
        for j in range(NJ):
            biela("DTA%d_%d" % (b, j), "R%d_%d" % (b, j), "R%d_%d" % (b + 1, j + 1), diag)
            biela("DTB%d_%d" % (b, j), "R%d_%d" % (b, j + 1), "R%d_%d" % (b + 1, j), diag)
    # Las X de los dos vanos arriostrados, en los dos muros (01 · S2, 12 · C4).
    for b in BAYS_ARR:
        for l in WALLS:
            j = 0 if l == "A" else NJ
            biela("PXA%s%d" % (l, b), "K%d%s_0" % (b, l), "R%d_%d" % (b + 1, j), pan)
            biela("PXB%s%d" % (l, b), "K%d%s_0" % (b + 1, l), "R%d_%d" % (b, j), pan)

    return ar.modelo(masas(ar.meta, x_grua)), ar.meta


def masas(meta: Meta, x_grua: float = LARGO / 2.0) -> list[NodalMass]:
    """La masa sísmica del 05, repartida donde cada término actúa.

    Devuelve masas traslacionales en X, Y y Z. La suma tiene que dar
    `P_SISMICO / G_MEMO`, y el caso lo comprueba: es el assert que atrapa
    cualquier término repartido dos veces o ninguna.
    """
    acc: dict[str, float] = {}

    def put(nm: str, w_kn: float) -> None:
        acc[nm] = acc.get(nm, 0.0) + w_kn

    # 1 y 2 · techo y cubierta, por área tributaria de cada línea y cada marco.
    g_techo = G_TECHO + G_CUBIERTA
    for f in range(1, NMARCOS + 1):
        tx = trib(f)
        for j in range(NJ + 1):
            ty = (LUZ / NJ) * (0.5 if j in (0, NJ) else 1.0)
            put("R%d_%d" % (f, j), g_techo * tx * ty)
    # 3 · revestimiento: muros longitudinales sobre las columnas, y los dos
    #     hastiales sobre los marcos extremos —incluido el triángulo de cumbrera.
    for f in range(1, NMARCOS + 1):
        tx = trib(f)
        for l in WALLS:
            put("R%d_%d" % (f, 0 if l == "A" else NJ), G_REVEST * tx * H_ALERO)
    a_hastial = LUZ * H_ALERO + LUZ * (H_CUMB - H_ALERO) / 2.0
    for f in (1, NMARCOS):
        for j in range(NJ + 1):
            ty = (LUZ / NJ) * (0.5 if j in (0, NJ) else 1.0)
            put("R%d_%d" % (f, j), G_REVEST * a_hastial * ty / LUZ)
    # 4 · columnas: su peso lineal, la mitad al alero y la mitad a la base
    #     —que está restringida, así que no participa, igual que en el 05,
    #     donde el peso de columna entra entero al peso sísmico pero la mitad
    #     inferior no se sacude. Ver `## Modelo` del memo 00.
    for f in range(1, NMARCOS + 1):
        for l in WALLS:
            put("R%d_%d" % (f, 0 if l == "A" else NJ), W_COL_LIN * H_ALERO)
    # 5 · carrileras: 1,20 kN/m en dos líneas de 30 m, al nivel del asiento.
    for f in range(1, NMARCOS + 1):
        for l in WALLS:
            put("R%d_%d" % (f, 0 if l == "A" else NJ), W_CARRIL_LIN * trib(f))
    # 6 · equipos colgados, uno por marco, en la cumbrera.
    for f in range(1, NMARCOS + 1):
        put("R%d_%d" % (f, NJ // 2), W_EQUIPOS)
    # 7 · la grúa sin carga (05 · C3), repartida entre los dos marcos que la
    #     flanquean y entre los dos rieles por igual.
    fa = min(max((x_grua % SEP) / SEP, 0.0), 1.0)
    f0 = min(int(x_grua // SEP) + 1, NMARCOS - 1)
    for l in WALLS:
        j = 0 if l == "A" else NJ
        put("R%d_%d" % (f0, j), W_GRUA_SC * (1.0 - fa) / 2.0)
        put("R%d_%d" % (f0 + 1, j), W_GRUA_SC * fa / 2.0)

    return [NodalMass(meta.nid(nm), (w / G_MEMO,) * 3 + (0.0, 0.0, 0.0))
            for nm, w in acc.items()]
