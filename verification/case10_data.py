"""Caso 10 — datos del galpón del altiplano (geometría, secciones y cargas).

Este módulo **no analiza nada**: es el único juego de datos que comparten los dos
motores, igual que en los casos 7, 8 y 9. Todo lo que hay acá está portado de
`Skills_SAP/scripts/galpon_altiplano_build.py` (rev.G, el script autoritativo del
modelo SAP2000 `galpon_altiplano.sdb`, v27.1), y cada constante lleva su
procedencia. La memoria de cálculo de la serie es `struct_pad/SERIE-GALPON.md`.

El caso: galpón industrial a dos aguas para faena minera de altiplano (Pica,
Tarapacá, ~3 800 m). Luz 24,0 m, pendiente 10°, alero 8,0 m, 5 marcos a 6,0 m.
Transversal (X) marcos a momento de **peralte variable** con bases articuladas;
longitudinal (Y) arriostrado, más arriostramiento continuo de techo.

**Por qué el peralte variable se puede reproducir.** El script de SAP se prohíbe
a sí mismo la sección no prismática (*Non-prismatic*) del programa: el tapered se
discretiza en tramos prismáticos, cuatro en la columna y seis en el dintel, con
una sección constante por tramo tomada en su punto medio. Esa decisión —tomada
para que el modelo fuera reproducible desde acá— es lo que permite que este
archivo exista.

Ejes locales, y no es cosmético
-------------------------------
SAP2000 y OpenSees numeran distinto, y las secciones de este modelo tienen
`I33 / I22 ≈ 25`, así que equivocarse no se disimula:

    SAP eje local 2  <->  OpenSees local y   (y por lo tanto  I22  <->  Iy)
    SAP eje local 3  <->  OpenSees local z   (y por lo tanto  I33  <->  Iz)

El `vecxz` de cada barra se elige para que el eje fuerte (`Iz`) flecte en el plano
que corresponde, comprobando la convención de `loads.local_axes`
(`ey = û(vecxz × ex)`, `ez = ex × ey`):

- **Columnas del marco** — verticales, eje fuerte en el plano X-Z (el del marco):
  `vecxz = (0,1,0)` deja `ey ∥ X`. Es la orientación por defecto de SAP para una
  barra vertical (local 2 ∥ X), y por eso el script no les pone `SetLocalAxes`.
- **Dinteles** — inclinados en el plano X-Z, eje fuerte en ese mismo plano:
  `vecxz = (0,1,0)` deja `ey` dentro del plano vertical y `ez ∥ Y`.
- **Pilares de hastial** — el script les pone `SetLocalAxes(90°)`, que gira el eje
  2 de X a Y: el eje fuerte flecta contra el viento sobre la testera.
  `vecxz = (1,0,0)` deja `ey ∥ Y`.
- **Puntales y diagonales** — cajones con `Iy = Iz`; el `vecxz` solo tiene que no
  ser paralelo a la barra.

Cuidado con el signo del eje 2: la convención de OpenSees deja `ey` apuntando
hacia abajo en el dintel, al revés que SAP. Afecta el **signo** de `M3` y `V2`,
no su magnitud. Por eso las cargas de viento se aplican acá como vector global
—que es como el propio script las contabiliza en su assert de equilibrio— y no
por eje local.
"""

from __future__ import annotations

import math

# ============================ GEOMETRÍA ============================
# Verbatim de galpon_altiplano_build.py. SERIE-GALPON.md §2 «El caso».
LUZ, PEND, H_ALERO, SEP, NMARCOS = 24.0, 10.0, 8.0, 6.0, 5
NCOL, NSEG = 4, 6            # tramos de la columna y del dintel (la malla del tapered)
TAN10 = math.tan(math.radians(PEND))
COS10 = math.cos(math.radians(PEND))
SIN10 = math.sin(math.radians(PEND))
NJ, LARGO = 18, (NMARCOS - 1) * SEP
DXJ = (LUZ / 2.0) / 9.0      # 9 espacios de costanera por faldón -> 1,3333 m
JS = [0, 3, 6, 9, 12, 15, 18]        # cortes de la malla: donde llega el arriostramiento
BAYS, BAYS_ARR = [1, 2, 3, 4], [1, 4]  # los 4 vanos; arriostrados solo los extremos
J_PIL, F_HAS = [3, 6, 9, 12, 15], [1, NMARCOS]  # pilares de hastial y marcos de testera

PANELES = [(b, 0, 3) for b in BAYS] + [(b, 15, 18) for b in BAYS]
PANELES += [(b, j1, j2) for b in BAYS_ARR for (j1, j2) in ((3, 6), (6, 9), (9, 12), (12, 15))]
PUNTALES = [(b, j) for b in BAYS for j in JS]
SEGS = [(JS[i], JS[i + 1]) for i in range(NSEG)]

# ============================ SECCIONES ============================
# Todas soldadas por planchas: el tapered no está en ningún catálogo, así que no
# se depende del ICHA. SERIE-GALPON.md §6.2.1.
BF, TF, TW = 0.220, 0.012, 0.006          # alas 220×12, alma 6 — iguales en las 7
D_BASE, D_ALERO, D_CUMBRE = 0.350, 0.800, 0.350   # peraltes teóricos de los extremos

# ============================= CARGAS ==============================
# SERIE-GALPON.md §4.3 «Datos de proyecto». S = 1,20 kPa es de estudio de sitio:
# NCh431 no existe en PDF, y NCh432 §5.1.2 manda estudio para alta montaña.
D_TECHO, D_MURO = 0.35, 0.12   # kPa — muerta superpuesta de techo y de revestimiento
LR = 0.30                      # kPa — sobrecarga de techo (a = 0 la saca del sismo)
S_BAL, F_UNB = 1.20, 0.50      # kPa — nieve balanceada, y el 50 % de la desbalanceada

# Viento: NCh432:2025. q_h = 0,613·K_z·K_zt·K_e·V²  con la Tabla 1 (zona I-B,
# V = 30 m/s), K_zt = 1,948 de la loma (Figura 3) y K_e = 0,6362 a 3 800 m
# (Nota 2 de la Tabla 4). SERIE-GALPON.md §4.1 y §5.24.
QH = 0.613 * 1.00 * 0.95 * 1.948 * 0.6362 * 30.0 ** 2 / 1000.0   # kPa
KD, GCPI = 0.85, 0.18          # direccionalidad y presión interna (edificio cerrado)
QK = QH * KD
A_ZONA = max(min(0.10 * min(LUZ, LARGO), 0.4 * H_ALERO), 0.04 * min(LUZ, LARGO), 0.9)

# ============================ MATERIAL =============================
# A36 de plancha. R_y = 1,3 (AISC 341-22 Tabla A3.2, «Plates, Strips, and Sheets»).
E_STEEL = 2.0e8       # kN/m²
NU = 0.3
GAMMA_STEEL = 76.9822           # kN/m³, el que el script le da a SAP
G_ACC = 9.80665                 # m/s², el mismo con que SAP convierte carga en masa
RHO = GAMMA_STEEL / G_ACC       # tonne/m³ -> 7,85 exacto, que es de donde salió el 76,9822
XI = 0.02                       # amortiguamiento, uniones soldadas (NCh2369 Tabla 5)


# ---------------------- Propiedades de sección ----------------------
# El offset del J: SAP no usa Σbt³/3
# ------------------------------------------------
# SERIE-GALPON.md §5.40 midió `GetSectProps` contra Σbt³/3 en las cuatro
# secciones extremas y encontró que SAP reporta entre 2,9 % y 3,2 % MENOS rigidez
# torsional. Puestas las cuatro juntas, la diferencia no es un porcentaje: es una
# **constante exacta de −8 981,3 mm⁴**, la misma en las cuatro.
#
#     COL_1  271 980,7 − 280 962,0 = −8 981,3
#     COL_4  296 280,7 − 305 262,0 = −8 981,3
#     DIN_1  294 930,7 − 303 912,0 = −8 981,3
#     DIN_3  273 330,7 − 282 312,0 = −8 981,3
#
# Tiene sentido: las siete secciones comparten ala (220×12) y alma (6 mm), y solo
# cambia el peralte. Si toda la diferencia vive en el término del ala, la
# diferencia tiene que ser constante — y lo es, al último dígito. Eso es lo que
# permite reconstruir el J de SAP para las tres secciones que §5.40 no midió
# (COL_2, COL_3, DIN_2) sin inventar nada: cuatro datos, un offset, cero grados de
# libertad sobrantes.
#
# El porcentaje sube cuando el alma pesa poco en el total, que es exactamente lo
# que se observa (−3,197 % en COL_1, de peralte 406 mm; −2,942 % en COL_4, de 744).
J_OFFSET_SAP = -8981.3e-12   # m⁴ — vale solo para el ala 220×12 de este modelo


def i_props(d: float, bf: float, tf: float, tw: float) -> tuple[float, float, float, float]:
    """Propiedades de una doble T soldada doblemente simétrica: (A, I33, I22, J_manual).

    `J_manual` es Σbt³/3 con `h = d − 2·t_f`, la fórmula de manual. No es el J que
    usa SAP: para eso está `j_sap()`.
    """
    h = d - 2.0 * tf                                  # altura libre del alma
    A = 2.0 * bf * tf + h * tw
    I33 = tw * h ** 3 / 12.0 + 2.0 * (bf * tf ** 3 / 12.0 + bf * tf * ((d - tf) / 2.0) ** 2)
    I22 = 2.0 * tf * bf ** 3 / 12.0 + h * tw ** 3 / 12.0
    J = (2.0 * bf * tf ** 3 + h * tw ** 3) / 3.0
    return A, I33, I22, J


def j_sap(d: float, bf: float = BF, tf: float = TF, tw: float = TW) -> float:
    """El J que reporta `GetSectProps` para las secciones tapered de este modelo."""
    return i_props(d, bf, tf, tw)[3] + J_OFFSET_SAP


def box_props(b: float, t: float) -> tuple[float, float, float]:
    """Cajón cuadrado soldado `b × b × t`: (A, I, J).

    `J = t·(b − t)³` es Bredt para la sección cerrada, y es la que usa SAP: las
    tres constantes coinciden dígito a dígito con las que el caso 9 extrajo del
    modelo para CAJ100X4 y CAJ125X6.
    """
    bi = b - 2.0 * t
    A = b * b - bi * bi
    I = (b ** 4 - bi ** 4) / 12.0
    J = t * (b - t) ** 3
    return A, I, J


def d_col(k: int) -> float:
    """Peralte de la sección del tramo `k` de la columna (k = 1..4), en su punto medio."""
    return D_BASE + (D_ALERO - D_BASE) * (k - 0.5) / NCOL


def d_din(m: int) -> float:
    """Peralte de la sección del tramo `m` del dintel (m = 1..3), en su punto medio."""
    return D_ALERO + (D_CUMBRE - D_ALERO) * (m - 0.5) / (NSEG // 2)


def m_seg(i: int) -> int:
    """Sección que le toca al tramo `i` del dintel (0-based), por simetría del faldón."""
    return i + 1 if i < NSEG // 2 else NSEG - i


# ------------------------- Nodos y barras --------------------------
def x_roof(j: int) -> float:
    return j * DXJ


def z_roof(j: int) -> float:
    return H_ALERO + (j if j <= 9 else NJ - j) * DXJ * TAN10


def y_of(f: int) -> float:
    return (f - 1) * SEP


def n_roof(f: int, j: int) -> str:
    return "R%d_%02d" % (f, j)


def n_col(f: int, l: str, k: int) -> str:
    """Nodo `k` de la columna (`k = 0` la base). En `k = NCOL` ya es el nodo de alero."""
    return n_roof(f, 0 if l == "A" else NJ) if k == NCOL else "K%d%s_%d" % (f, l, k)


def trib(f: int) -> float:
    """Ancho tributario del marco `f`: medio vano en las testeras, uno entero adentro."""
    return SEP / 2.0 if f in F_HAS else SEP


def area_franja(xa: float, xb: float) -> float:
    """Área de fachada de hastial entre las abscisas `xa` y `xb` (bajo las dos aguas)."""
    if xb <= xa:
        return 0.0

    def prim(x):
        return H_ALERO * x + TAN10 * x * x / 2.0

    if xb <= LUZ / 2.0:
        return prim(xb) - prim(xa)
    if xa >= LUZ / 2.0:
        return area_franja(LUZ - xb, LUZ - xa)
    return area_franja(xa, LUZ / 2.0) + area_franja(LUZ / 2.0, xb)


# Normal exterior del faldón, por lado, en ejes globales. Es la dirección del eje
# local 2 de SAP para el dintel, y con ella el viento se aplica como vector global.
NORM = {"I": (-SIN10, 0.0, COS10), "D": (SIN10, 0.0, COS10)}


# ==================== ENSAMBLE DEL MODELO ==========================
from rukan.model import FrameElement, Material, Model, NodalMass, Node, Section  # noqa: E402

def _sections(ncol: int) -> tuple[list[Section], dict[str, int]]:
    """Las secciones del modelo para una malla de `ncol` tramos de columna.

    El dintel siempre va en 6 tramos: sus cortes no son una malla libre, son las
    líneas donde llega el arriostramiento de techo (§6.2.2), y moverlos cambiaría
    la estructura, no la discretización.
    """
    out: list[Section] = []
    sid: dict[str, int] = {}

    def push(nm, sec_kw):
        i = len(out) + 1
        sid[nm] = i
        out.append(Section(i, **sec_kw))

    for k in range(1, ncol + 1):
        d = D_BASE + (D_ALERO - D_BASE) * (k - 0.5) / ncol
        A, I33, I22, _ = i_props(d, BF, TF, TW)
        push("COL_%d" % k, dict(A=A, Iy=I22, Iz=I33, J=j_sap(d)))
    for m in range(1, NSEG // 2 + 1):
        A, I33, I22, _ = i_props(d_din(m), BF, TF, TW)
        push("DIN_%d" % m, dict(A=A, Iy=I22, Iz=I33, J=j_sap(d_din(m))))
    for nm, b, t in (("CAJ100X4", 0.100, 0.004), ("CAJ75X4", 0.075, 0.004),
                     ("CAJ125X6", 0.125, 0.006)):
        A, I, J = box_props(b, t)
        push(nm, dict(A=A, Iy=I, Iz=I, J=J))
    # Pilar de hastial I 400×150×8/6. Es la única sección cuyo J NO se puede
    # reconstruir: el offset de §5.40-bis se calibró sobre el ala 220×12 y este
    # perfil tiene otra. Se usa Σbt³/3, que sobreestima ~3 % la rigidez torsional
    # de un miembro cuyo M3 máximo es 23,4 kNm y cuya torsión es despreciable.
    A, I33, I22, J = i_props(0.400, 0.150, 0.008, 0.006)
    push("PIL400", dict(A=A, Iy=I22, Iz=I33, J=J))
    return out, sid


# Restricción de base: SAP usa [U1,U2,U3,R1,R2,R3] = T,T,T,F,F,T — articulada para
# la flexión en los dos planos, pero con el giro en torno al eje vertical impedido.
BASE = (True, True, True, False, False, True)
FREE = (False,) * 6


class Meta:
    """Índices del modelo: nombre <-> id, longitudes y sección de cada barra."""

    def __init__(self):
        self.node_id: dict[str, int] = {}
        self.node_xyz: dict[str, tuple[float, float, float]] = {}
        self.elem_id: dict[str, int] = {}
        self.elem_len: dict[str, float] = {}
        self.elem_sec: dict[str, str] = {}
        self.tapered: list[str] = []
        self.bases: list[str] = []
        # Nodo auxiliar del tope de cada pilar de hastial (ver `PILAR_TIE`).
        self.pilar_tie: list[tuple[int, int]] = []

    def eid(self, name: str) -> int:
        return self.elem_id[name]

    def nid(self, name: str) -> int:
        return self.node_id[name]


def build_model(ncol: int = NCOL) -> tuple[Model, Meta]:
    """Arma el galpón completo. `ncol` es la malla del tapered de la columna.

    Con `ncol = 4` reproduce el modelo del `.sdb`: 105 nodos, 188 barras y 20
    bases. Variarlo es el estudio de convergencia, y por eso la malla es un
    parámetro y no una constante enterrada en el armado.
    """
    js = list(JS)
    segs = list(SEGS)

    def n_col_l(f, l, k):
        return n_roof(f, 0 if l == "A" else NJ) if k == ncol else "K%d%s_%d" % (f, l, k)

    meta = Meta()
    nodes: list[Node] = []
    sections, sec_id = _sections(ncol)

    def vecxz_sap(a: str, b: str) -> tuple[float, float, float]:
        """El `vecxz` que reproduce el eje local 2 por omisión de SAP2000.

        Para una barra **no vertical**, SAP pone el eje 2 en el plano vertical que
        la contiene. Con la convención `ey = û(vecxz × ex)` eso se consigue con
        `vecxz = ẑ × ex`, que es horizontal y normal a ese plano. Para una barra
        vertical SAP pone el eje 2 paralelo a X global, que es el `(0,1,0)` de las
        columnas.

        Importa aunque la sección sea un cajón con `Iy = Iz`: no cambia el
        análisis, pero decide **en qué índice** sale cada momento, y sin esto el
        momento de peso propio del puntal aparece en `My` mientras SAP lo reporta
        en `M3`.
        """
        pa, pb = meta.node_xyz[a], meta.node_xyz[b]
        ex = (pb[0] - pa[0], pb[1] - pa[1], pb[2] - pa[2])
        v = (-ex[1], ex[0], 0.0)          # ẑ × ex
        n = math.hypot(v[0], v[1])
        return (0.0, 1.0, 0.0) if n < 1e-12 else (v[0] / n, v[1] / n, 0.0)

    def pt(nm, x, y, z, restr=FREE):
        i = len(nodes) + 1
        nodes.append(Node(i, x, y, z, restr))
        meta.node_id[nm] = i
        meta.node_xyz[nm] = (x, y, z)

    # --- Nodos, en el mismo orden que el script de SAP ---
    for f in range(1, NMARCOS + 1):
        y = y_of(f)
        for j in js:
            pt(n_roof(f, j), x_roof(j), y, z_roof(j))
        for l, x in (("A", 0.0), ("B", LUZ)):
            for k in range(ncol):
                pt(n_col_l(f, l, k), x, y, k * H_ALERO / ncol, BASE if k == 0 else FREE)
                if k == 0:
                    meta.bases.append(n_col_l(f, l, k))
    for f in F_HAS:
        for j in J_PIL:
            pt("H%d_%02d" % (f, j), x_roof(j), y_of(f), 0.0, BASE)
            meta.bases.append("H%d_%02d" % (f, j))
    for b in BAYS_ARR:
        for l, x in (("A", 0.0), ("B", LUZ)):
            pt("XM%s%d" % (l, b), x, y_of(b) + SEP / 2.0, H_ALERO / 2.0)
    for (b, j1, j2) in PANELES:
        pt("XT%d_%02d" % (b, j1), 0.5 * (x_roof(j1) + x_roof(j2)),
           y_of(b) + SEP / 2.0, 0.5 * (z_roof(j1) + z_roof(j2)))

    # --- Barras ---
    els: list[FrameElement] = []

    def add(nm, a, b, sec, vecxz, **kw):
        i = len(els) + 1
        els.append(FrameElement(i, meta.node_id[a], meta.node_id[b],
                                1, sec_id[sec], vecxz, **kw))
        meta.elem_id[nm] = i
        meta.elem_sec[nm] = sec
        pa, pb = meta.node_xyz[a], meta.node_xyz[b]
        meta.elem_len[nm] = math.dist(pa, pb)

    REL_M = dict(release_y_i=True, release_z_i=True,
                 release_y_j=True, release_z_j=True)
    REL_I = dict(release_y_i=True, release_z_i=True)
    REL_J = dict(release_y_j=True, release_z_j=True)

    for f in range(1, NMARCOS + 1):
        for l in ("A", "B"):
            for k in range(1, ncol + 1):
                nm = "COL%d%s_%d" % (f, l, k)
                add(nm, n_col_l(f, l, k - 1), n_col_l(f, l, k), "COL_%d" % k, (0.0, 1.0, 0.0))
                meta.tapered.append(nm)
        for i, (j1, j2) in enumerate(segs):
            nm = "DIN%d_%d" % (f, i + 1)
            add(nm, n_roof(f, j1), n_roof(f, j2), "DIN_%d" % m_seg(i), (0.0, 1.0, 0.0))
            meta.tapered.append(nm)
    for (b, j) in PUNTALES:
        nm = "PUN%02d_%d" % (j, b)
        a, c = n_roof(b, j), n_roof(b + 1, j)
        add(nm, a, c, "CAJ125X6", vecxz_sap(a, c), **REL_M)
    for b in BAYS_ARR:
        for l, jj in (("A", 0), ("B", NJ)):
            cen = "XM%s%d" % (l, b)
            # §8.6.4: en el cruce SOLO UNA diagonal es continua. Las mitades _1 y _4
            # forman la continua (sin liberación en el centro); _2 y _3 llegan
            # apernadas. Modelar las dos continuas sería más rígido que la norma.
            for suf, a, rel in (("1", n_col_l(b, l, 0), REL_I),
                                ("4", n_roof(b + 1, jj), REL_I),
                                ("2", n_col_l(b + 1, l, 0), {**REL_I, **REL_J}),
                                ("3", n_roof(b, jj), {**REL_I, **REL_J})):
                add("ARW%s%d_%s" % (l, b, suf), a, cen, "CAJ100X4",
                    vecxz_sap(a, cen), **rel)
    for (b, j1, j2) in PANELES:
        cen = "XT%d_%02d" % (b, j1)
        for suf, a, rel in (("1", n_roof(b, j1), REL_I),
                            ("4", n_roof(b + 1, j2), REL_I),
                            ("2", n_roof(b, j2), {**REL_I, **REL_J}),
                            ("3", n_roof(b + 1, j1), {**REL_I, **REL_J})):
            add("ART%d_%02d_%s" % (b, j1, suf), a, cen, "CAJ75X4",
                vecxz_sap(a, cen), **rel)
    # Pilares de hastial. SAP les libera P, M2 y M3 en el extremo superior: el pilar
    # NO cuelga del dintel ni lo apuntala. `FrameElement` no tiene liberación axial,
    # así que el tope va a un nodo propio atado al de techo solo en el plano
    # horizontal (Ux, Uy) y en el giro vertical (Rz) — ver `PILAR_TIE` y la nota del
    # caso. El nodo auxiliar hereda la Z del nodo de techo (misma posición).
    for f in F_HAS:
        for j in J_PIL:
            top = "P%d_%02d" % (f, j)
            xr, yr, zr = meta.node_xyz[n_roof(f, j)]
            pt(top, xr, yr, zr)
            nm = "PIL%d_%02d" % (f, j)
            add(nm, "H%d_%02d" % (f, j), top, "PIL400", (1.0, 0.0, 0.0), **REL_J)
            meta.pilar_tie.append((meta.node_id[n_roof(f, j)], meta.node_id[top]))

    model = Model(nodes=nodes,
                  materials=[Material(1, E=E_STEEL, nu=NU, rho=RHO)],
                  sections=sections, elements=els, masses=[])
    return model, meta


# GDL que se atan entre el nodo de techo y el tope del pilar de hastial.
# 1 = Ux, 2 = Uy, 6 = Rz. Se deja LIBRE el 3 (Uz), que es la liberación axial, y
# los giros 4 y 5, que el elemento ya libera por `-releasey/-releasez`.
PILAR_TIE = (1, 2, 6)


# ======================= CARGAS POR ESTADO =========================
# Los 10 estados aplicados (el 11.º, DEAD, es el peso propio y lo pone rukan).
# Cada uno es una lista de `(barra, (gx, gy, gz))` con la fuerza **por unidad de
# largo de barra**, en ejes globales. Elegir ese formato —y no los códigos de
# dirección de SAP— es lo que permite verificar cada estado por equilibrio: la
# resultante analítica es Σ g·L, y tiene que dar la reacción de base cambiada de
# signo. El script de SAP hace exactamente ese assert y le da 0,0 en los 11.
#
# GOTCHA de SAP que hay que deshacer al portar: `SetLoadDistributed` toma fuerza
# por unidad de largo, y el código de dirección decide sobre qué largo:
#   Dir 10 = gravedad por largo DE BARRA        -> g = (0, 0, −w)
#   Dir 11 = gravedad por PROYECCIÓN horizontal -> g = (0, 0, −w·L_h/L_m)
#   Dir 4 / 5 = global X / Y                    -> g = (w, 0, 0) / (0, w, 0)
#   Dir 2 + CSys "Local" = normal al faldón     -> g = w · NORM[lado]
# La nieve va por proyección y la muerta de techo por largo de barra: son dos
# reparticiones distintas sobre la misma barra inclinada, y confundirlas mete un
# 1,5 % en el faldón (1/cos 10°).

# Coeficientes GC_pf de NCh432:2025, Figura 12 (cubierta a dos aguas, edificio
# cerrado). T05/T20 son las filas de θ = 5° y 20°; C1 interpola a los 10° del
# galpón. C2 es el caso de viento longitudinal, que la figura da directo.
_T05 = {"1": 0.40, "2": -0.69, "3": -0.37, "4": -0.29,
        "1E": 0.61, "2E": -1.07, "3E": -0.53, "4E": -0.43}
_T20 = {"1": 0.53, "2": -0.69, "3": -0.48, "4": -0.43,
        "1E": 0.80, "2E": -1.07, "3E": -0.69, "4E": -0.64}
_C1 = {k: _T05[k] + (_T20[k] - _T05[k]) * (PEND - 5.0) / 15.0 for k in _T05}
_C2 = {"1": -0.45, "2": -0.69, "3": -0.37, "4": -0.45, "5": 0.40, "6": -0.29,
       "1E": -0.48, "2E": -1.07, "3E": -0.53, "4E": -0.48, "5E": 0.61, "6E": -0.43}

# Las zonas de esquina (sufijo E) se promedian por área sobre cada cara, en vez de
# modelar las ocho posiciones de franja de §7.3.2.1: la resultante por cara queda
# idéntica y solo se pierde la concentración local, que es materia de C&R (§6.2.2).
_FRL = 2 * A_ZONA / LARGO
_FRH = area_franja(0.0, A_ZONA) / area_franja(0.0, LUZ)
_G1 = {z: _C1[z + "E"] * _FRL + _C1[z] * (1 - _FRL) for z in "1234"}
_G2 = {z: _C2[z + "E"] * _FRL + _C2[z] * (1 - _FRL) for z in "1234"}
_G2.update({z: _C2[z + "E"] * _FRH + _C2[z] * (1 - _FRH) for z in "56"})

# mA/mB = muros longitudinales; fI/fD = faldones izquierdo y derecho;
# h0/h24 = hastiales (solo los hay bajo viento longitudinal).
VIENTO = {
    "WTXP": {"mA": _G1["1"], "mB": _G1["4"], "fI": _G1["2"], "fD": _G1["3"], "h0": None, "h24": None},
    "WTXN": {"mA": _G1["4"], "mB": _G1["1"], "fI": _G1["3"], "fD": _G1["2"], "h0": None, "h24": None},
    "WLYP": {"mA": _G2["1"], "mB": _G2["4"], "fI": _G2["2"], "fD": _G2["3"], "h0": _G2["5"], "h24": _G2["6"]},
    "WLYN": {"mA": _G2["4"], "mB": _G2["1"], "fI": _G2["3"], "fD": _G2["2"], "h0": _G2["6"], "h24": _G2["5"]},
    "WPI": {"mA": -GCPI, "mB": -GCPI, "fI": -GCPI, "fD": -GCPI, "h0": -GCPI, "h24": -GCPI},
}

PATTERNS = ["DSD", "LR", "SBAL", "SUNBI", "SUNBD",
            "WTXP", "WTXN", "WLYP", "WLYN", "WPI"]


def load_patterns(meta: Meta) -> dict[str, list[tuple[str, tuple[float, float, float]]]]:
    """Los 10 estados aplicados, como `{estado: [(barra, g_global_por_largo)]}`."""
    out: dict[str, list] = {p: [] for p in PATTERNS}

    def put(pat, nm, g):
        out[pat].append((nm, g))

    # --- Gravedad ---
    for f in range(1, NMARCOS + 1):
        tl = trib(f)
        for i, (j1, j2) in enumerate(SEGS):
            nm = "DIN%d_%d" % (f, i + 1)
            Lm, Lh = meta.elem_len[nm], (j2 - j1) * DXJ
            lado = "I" if j2 <= 9 else "D"
            put("DSD", nm, (0.0, 0.0, -D_TECHO * tl))
            put("LR", nm, (0.0, 0.0, -LR * tl * Lh / Lm))
            put("SBAL", nm, (0.0, 0.0, -S_BAL * tl * Lh / Lm))
            for pat, fac in (("SUNBI", 1.0 if lado == "I" else F_UNB),
                             ("SUNBD", F_UNB if lado == "I" else 1.0)):
                put(pat, nm, (0.0, 0.0, -S_BAL * fac * tl * Lh / Lm))
        for l in ("A", "B"):
            for k in range(1, NCOL + 1):
                put("DSD", "COL%d%s_%d" % (f, l, k), (0.0, 0.0, -D_MURO * tl))
    for f in F_HAS:
        for j in J_PIL:
            A = area_franja(j * DXJ - 2.0, j * DXJ + 2.0)
            put("DSD", "PIL%d_%02d" % (f, j), (0.0, 0.0, -D_MURO * A / z_roof(j)))
        for l, (xa, xb) in (("A", (0.0, 2.0)), ("B", (LUZ - 2.0, LUZ))):
            w = D_MURO * area_franja(xa, xb) / H_ALERO
            for k in range(1, NCOL + 1):
                put("DSD", "COL%d%s_%d" % (f, l, k), (0.0, 0.0, -w))

    # --- Viento ---
    for pat, e in VIENTO.items():
        for f in range(1, NMARCOS + 1):
            tl = trib(f)
            for i, (j1, j2) in enumerate(SEGS):
                nm = "DIN%d_%d" % (f, i + 1)
                lado = "I" if j2 <= 9 else "D"
                w = -QK * e["fI" if lado == "I" else "fD"] * tl
                n = NORM[lado]
                put(pat, nm, (w * n[0], w * n[1], w * n[2]))
            for cara, l, signo in (("mA", "A", 1.0), ("mB", "B", -1.0)):
                if e[cara] is None:
                    continue
                w = signo * QK * e[cara] * tl
                for k in range(1, NCOL + 1):
                    put(pat, "COL%d%s_%d" % (f, l, k), (w, 0.0, 0.0))
        for cara, f, signo in (("h0", 1, 1.0), ("h24", NMARCOS, -1.0)):
            if e[cara] is None:
                continue
            for j in J_PIL:
                A = area_franja(j * DXJ - 2.0, j * DXJ + 2.0)
                put(pat, "PIL%d_%02d" % (f, j), (0.0, signo * QK * e[cara] * A / z_roof(j), 0.0))
            for l, (xa, xb) in (("A", (0.0, 2.0)), ("B", (LUZ - 2.0, LUZ))):
                w = signo * QK * e[cara] * area_franja(xa, xb) / H_ALERO
                for k in range(1, NCOL + 1):
                    put(pat, "COL%d%s_%d" % (f, l, k), (0.0, w, 0.0))
    return out


def seismic_mass(model: Model, meta: Meta, pats: dict,
                 include_pilar: bool = False) -> list[NodalMass]:
    """Masa sísmica `D + 0,20·S`, concentrada en los nudos.

    Es la fuente de masa del modelo: `MASA_SIS` = `DEAD` + `DSD` + `0,20·SBAL`,
    tomada **de las cargas** (`MassFromElements = False`), así que el peso propio
    entra por el estado `DEAD` y no por los elementos. Cada carga distribuida se
    reparte mitad y mitad a los dos nudos de su barra, que es como SAP la convierte.

    `include_pilar` — la decisión que decide el período
    -------------------------------------------------
    Con `False` (por omisión) se **excluye** la masa de los pilares de hastial, y
    ese es el ajuste que hace calzar el modal con SAP2000: T₁ pasa de 0,883866 s a
    0,852628 s contra los 0,852657 s de SAP, y las masas modales acumuladas
    coinciden —X e Y a la cuarta cifra, Z a la tercera: 0,6509 contra 0,6513—.
    Con `True` el modelo queda 3,7 % más flexible.

    El porqué es el mismo release que se documenta en `assemble`: el pilar de
    hastial lleva la **P liberada arriba**, así que todo su peso vertical —el
    propio y el del revestimiento que carga— reacciona en su propia base y nunca
    llega al nudo de techo. Todo indica que SAP arrastra esa liberación al armado de
    la masa y deja los 77,89 kN del pilar fuera de la matriz: es la explicación que
    cierra los números, no una lectura del programa — no se contrastó contra las
    masas nodales del .sdb.

    **Eso es discutible, y el post lo discute**: la liberación axial gobierna el
    camino de la carga *vertical*, pero la inercia *horizontal* del pilar existe
    igual — el pilar hay que acelerarlo, y siendo biarticulado le entrega la mitad
    de esa inercia al techo. Acá se reproduce el criterio de SAP para poder
    contrastar; el efecto de no reproducirlo está medido y es un 3,7 % de período.
    """
    els = {e.id: e for e in model.elements}
    secs = {s.id: s for s in model.sections}
    # La masa que caiga en el nudo auxiliar del tope del pilar se lleva al nudo de
    # techo, que es donde SAP la tiene: allí ese tope y el nudo de techo son uno.
    remap = {p: r for r, p in meta.pilar_tie}
    acc: dict[int, float] = {}

    def put(nid, m):
        n = remap.get(nid, nid)
        acc[n] = acc.get(n, 0.0) + m

    for nm, L in meta.elem_len.items():
        if not include_pilar and nm.startswith("PIL"):
            continue
        e = els[meta.elem_id[nm]]
        m_half = secs[e.section].A * L * RHO / 2.0
        put(e.node_i, m_half)
        put(e.node_j, m_half)
    for pat, fac in (("DSD", 1.0), ("SBAL", 0.20)):
        for nm, g in pats[pat]:
            if not include_pilar and nm.startswith("PIL"):
                continue
            W = abs(g[2]) * meta.elem_len[nm] * fac
            e = els[meta.elem_id[nm]]
            put(e.node_i, W / G_ACC / 2.0)
            put(e.node_j, W / G_ACC / 2.0)
    return [NodalMass(n, (m, m, m, 0.0, 0.0, 0.0)) for n, m in acc.items()]


def resultants(meta: Meta, pats: dict) -> dict[str, tuple[float, float, float]]:
    """Resultante analítica Σ g·L de cada estado [kN]. Es el patrón del equilibrio."""
    out = {}
    for pat, items in pats.items():
        fx = fy = fz = 0.0
        for nm, g in items:
            L = meta.elem_len[nm]
            fx += g[0] * L
            fy += g[1] * L
            fz += g[2] * L
        out[pat] = (fx, fy, fz)
    return out
