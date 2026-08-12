"""Caso 9 — Torre CBF/MRF: modal espectral NCh2369:2025 con espectro por dirección.

Torre industrial chilena de 3 niveles (6,0 m × 4,0 m × 12,0 m) con dos sistemas
sismorresistentes distintos por dirección:

- **X (CBF):** las dos caras de 6,0 m arriostradas con X apiladas por nivel,
  medias diagonales partidas en el cruce (liberadas solo en el extremo de
  columna) + viga puntal biarticulada.
- **Y (MRF):** los dos marcos de 4,0 m a momento, sin diagonales (paso libre
  bajo la torre). Columnas con el **eje fuerte orientado al plano Y**.
- Sin diafragma rígido: arriostramiento de planta en X en cada nivel y masas
  concentradas en los 4 nodos de columna por nivel (P_nivel/4, sin torsión).
- Bases articuladas en el plano CBF (RY libre) y empotradas en el plano MRF.

**Lo que se verifica aquí** (la novedad del peldaño 9): el AME NCh2369:2025 con
**espectro DISTINTO por dirección**. El R de la Tabla 7 es el MISMO en ambas
direcciones (R = 5: filas 5.1 y 5.3, anclajes dúctiles, uniones soldadas
ξ = 0,02), pero la rampa de período corto de la Ec. (1b) castiga al CBF rígido
(T*_X = 0,220 s < 0,328 s → R*_X ≈ 3,85) y no toca al MRF flexible
(T*_Y = 0,996 s → R*_Y = 5). El «R por dirección» sale del análisis, no de la
tabla. La cadena completa por dirección: T* → R* (Ec. 1b) → Q0 → banda
Q0mín/Q0máx (Ecs. 12/13) → R₁ (Ec. 14). Además: espectro vertical (Ec. 4, con
R_V = 2 y ξ_V = 0,03) y desplazamientos con el espectro de referencia (§6.1,
sin R, corregido por (0,05/ξ)^0,4).

El espectro se implementa **inline** (Ecs. 3, 4, 1a y 1b — con la rama
R ≤ 1 → R* = 1 —, leídas del PDF de la 3.ª ed.; ver lecturas registradas) y se
ancla contra ordenadas evaluadas a mano desde `nch2369-spectrum.ts` de
struct_pad. NO usa `rukan.spectra.nch2369_spectrum`: ese módulo aplica R*(T)
punto a punto (estilo 2003); aquí la 2025 pide R* CONSTANTE calculado en T*
(el período del modo con mayor masa traslacional en la dirección de análisis,
§5.4) — el caso es autocontenido.

Patrón de referencia: SAP2000 v25 vía MCP (`torre_cbf_mrf.sdb`): secciones
General con As2=As3=0 (sin deformación por corte, iguala `elasticBeamColumn`),
espectros de usuario de 501 puntos (T = 0..5 s, paso 0,01 s, en g), factor de
escala 9,80665, CQC con ξ = 0,02 (horizontal) / 0,03 (vertical), 12 modos.
Las propiedades de sección son las que SAP calculó de las placas (esquina
viva): fuente única de números para ambos motores.

**Gotcha de extracción (hallazgo de este caso, 2026-08-11)**: SAP2000 AJUSTA la
función de espectro de usuario desde el amortiguamiento de la función
(`DampRatio`, cuyo default en `Func.FuncRS.SetUser` es 0,05) hacia el
amortiguamiento modal del caso RS, con la amplificación de Newmark-Hall del
dominio de velocidad, a(β) = 2,31 − 0,41·ln(β%): ×1,22766636 para 5 %→2 % y
×1,12692239 para 5 %→3 %. Como las ordenadas de usuario YA traen el
(0,05/ξ)^0,4 de la Ec. (1a), dejar el `DampRatio` en su default DUPLICA la
corrección por amortiguamiento (+22,8 % / +12,7 % de demanda, en silencio). La
primera extracción de referencias venía contaminada exactamente por ese factor
(uniforme en todas las respuestas de cada caso, lo que lo delató); se corrigió
poniendo `DampRatio` = ξ del caso en las cuatro funciones y re-extrayendo.
"""

from __future__ import annotations

import math

import openseespy.opensees as ops

from rukan.engine import build
from rukan.model import FrameElement, Material, Model, NodalMass, Node, Section
from rukan.modal import G, directional_combination, run_directional_spectral
from rukan.spectra import Spectrum

# =============================== DATOS ================================
E_ = 2.0e8   # kN/m²
NU = 0.3

# Sitio y sistema (NCh2369:2025): zona 3, suelo D, categoría II.
I_ = 1.0                 # factor de importancia (Cat. II)
AR = 0.56                # Ar = 1,4·A0 [g] (Tabla 3, zona 3)
S_, R_SUELO, T0, P_, Q_, T1 = 1.00, 3.50, 0.60, 1.00, 2.50, 0.41  # Tabla 6, suelo D
R_TABLA = 5.0            # Tabla 7, filas 5.1 (MRF) y 5.3 (CBF): el MISMO R
XI_H = 0.02              # uniones soldadas (Tabla 7)
R_V, XI_V = 2.0, 0.03    # vertical (§5.4, Ec. 2)

# Gravedad y masa sísmica (§5.1.2, plataformas de operación: P = D + 0,25·L).
P_NIVEL = {1: 325.0, 2: 612.5, 3: 262.5}   # kN por nivel (z = 4, 8, 12)
P_TOTAL = 1200.0                            # kN

# Secciones General (m/m⁴) calculadas por SAP desde las placas (esquina viva)
# — fuente única para ambos motores. Iy = I22 (débil), Iz = I33 (fuerte).
SECS = [
    Section(1, A=0.011744, Iy=7.201143466666666e-5, Iz=2.066117546666666e-4,
            J=8.365533866666667e-7),                                   # HN30 columnas
    Section(2, A=0.00468, Iy=5.63004e-6, Iz=7.4076e-5, J=1.1568784e-7),  # IN30 vigas
    Section(3, A=0.002856, Iy=6.757772e-6, Iz=6.757772e-6, J=1.0110954e-5),  # CAJ125X6
    Section(4, A=0.001536, Iy=2.363392e-6, Iz=2.363392e-6, J=3.538944e-6),   # CAJ100X4
]

# ==================== ESPECTRO NCh2369:2025 (inline) ==================


def sa_h(T: float) -> float:
    """Ec. (3): espectro horizontal de referencia S_aH(T)/g (ξ = 5 %, sin R)."""
    if T == 0.0:
        return AR * S_
    ratio = T / T0
    return AR * S_ * (1.0 + R_SUELO * ratio**P_) / (1.0 + ratio**Q_)


def sa_v(T: float) -> float:
    """Ec. (4): espectro vertical de referencia S_aV(T)/g — factor 0,7 y 1,7·T."""
    if T == 0.0:
        return 0.7 * AR * S_
    ratio = 1.7 * T / T0
    return 0.7 * AR * S_ * (1.0 + R_SUELO * ratio**P_) / (1.0 + ratio**Q_)


def r_star(t_star: float, R: float) -> float:
    """Ec. (1b): R* con la rama R ≤ 1 → R* = 1 (¡impresa en la norma!) y la
    rampa de período corto para T* < Cr·T1, con Cr = 0,16·R."""
    if R <= 1.0:
        return 1.0
    lim = 0.16 * R * T1
    if lim <= 0.0 or t_star >= lim:
        return R
    return 1.5 + (R - 1.5) * t_star / lim


def esc_xi(xi: float) -> float:
    """Factor de amortiguamiento (0,05/ξ)^0,4 de las Ecs. (1a) y (2)."""
    return (0.05 / xi) ** 0.4


def make_spectrum(sa_fn, factor: float) -> Spectrum:
    """Tabula el espectro como SAP: 501 puntos T = 0..5, paso 0,01, T a 4 decimales."""
    periods, accels = [], []
    for i in range(501):
        T = round(i * 0.01, 4)
        periods.append(T)
        accels.append(factor * sa_fn(T))
    return Spectrum(periods=periods, accels=accels)


# --- Anclas contra struct_pad (src/lib/nch2369-spectrum.ts), a mano -----------
# Cada valor se evaluó a mano desde las fórmulas del TS (computeSpectrum con
# zona 3, suelo D), plegando los números en la expresión literal:
#   A1  T=0,2 < 0,328 (rampa), R=5, ξ=0,02:
#       sa = 0,56·(1+3,5·(0,2/0,6))/(1+(0,2/0,6)^2,5) = 1,1401901040551568
#       r* = 1,5+3,5·0,2/0,328 = 3,6341463414634148 → Sa = sa·2,5^0,4/r*
#   A2  R=1 (rama R≤1 → r*=1), T=0,5, ξ=0,03:
#       sa = 0,56·(1+3,5·(0,5/0,6))/(1+(0,5/0,6)^2,5) = 1,342360076294995
#   A3  T=0, R=5: forma = Ar·S = 0,56; r*(0)=1,5 → 0,56·2,5^0,4/1,5
#   A4  T=0,4 ≥ 0,328 (meseta): r*=R=5; sa(0,4) = 1,3696411814453577
#   A5  vertical T=0,3, R_V=2, ξ_V=0,03 (factor 0,7 y corrimiento 1,7·T):
#       sa_v = 0,7·0,56·(1+3,5·0,85)/(1+0,85^2,5) = 0,9352311961008789
ESC02, ESC03 = esc_xi(0.02), esc_xi(0.03)
assert abs(I_ * sa_h(0.2) * ESC02 / r_star(0.2, 5.0) - 0.4526378415389607) < 1e-9, "ancla A1"
assert r_star(0.05, 1.0) == 1.0, "ancla A2a: rama R<=1 -> R*=1 (T en plena rampa)"
assert abs(I_ * sa_h(0.5) * ESC03 / r_star(0.5, 1.0) - 1.6466774074475594) < 1e-9, "ancla A2"
assert abs(I_ * sa_h(0.0) * ESC02 / r_star(0.0, 5.0) - 0.5386079648720264) < 1e-9, "ancla A3"
assert abs(I_ * sa_h(0.4) * ESC02 / r_star(0.4, 5.0) - 0.3951962407195725) < 1e-9, "ancla A4"
assert abs(I_ * sa_v(0.3) * ESC03 / R_V - 0.5736255526944926) < 1e-9, "ancla A5 (vertical)"

# ============================== MODELO ================================
# Esquinas c1..c4 y niveles z = 0, 4, 8, 12; nodo (nivel, esquina) = 10·nivel+c.
CORNERS = {1: (0.0, 0.0), 2: (6.0, 0.0), 3: (0.0, 4.0), 4: (6.0, 4.0)}


def nid(lev: int, c: int) -> int:
    return 10 * lev + c


BASES = tuple(nid(0, c) for c in CORNERS)          # 1..4
# Bases: UX, UY, UZ, RX, RZ fijos; RY libre (articulada en el plano CBF X-Z,
# empotrada en el plano MRF Y-Z).
BASE_FIX = (True, True, True, True, False, True)
FREE = (False,) * 6


def make_tower_model() -> Model:
    nodes = [Node(nid(0, c), x, y, 0.0, BASE_FIX) for c, (x, y) in CORNERS.items()]
    for s in (1, 2, 3):
        nodes += [Node(nid(s, c), x, y, 4.0 * s, FREE) for c, (x, y) in CORNERS.items()]
        nodes.append(Node(40 + s, 3.0, 0.0, 4.0 * s - 2.0, FREE))  # cruce X cara A (y=0)
        nodes.append(Node(50 + s, 3.0, 4.0, 4.0 * s - 2.0, FREE))  # cruce X cara B (y=4)
        nodes.append(Node(60 + s, 3.0, 2.0, 4.0 * s, FREE))        # cruce planta

    els: list[FrameElement] = []

    def push(eid, a, b, sec, vecxz, **kw):
        els.append(FrameElement(eid, a, b, 1, sec, vecxz, **kw))

    REL_I = dict(release_z_i=True, release_y_i=True)
    REL_J = dict(release_z_j=True, release_y_j=True)

    for s in (1, 2, 3):
        # Columnas HN30 con eje fuerte al plano Y: vecxz=(1,0,0) → local y ∥ Y,
        # la flexión de eje fuerte (Iz) ocurre en el plano MRF (equivale al
        # SetLocalAxes 90 de SAP). COL{c}{s} = tag 100+4(s−1)+c.
        for c in (1, 2, 3, 4):
            push(100 + 4 * (s - 1) + c, nid(s - 1, c), nid(s, c), 1, (1.0, 0.0, 0.0))
        # Vigas de momento VMY (Y, 4 m) IN30 SIN releases; vecxz=(1,0,0) →
        # local y ∥ Z: eje fuerte flectando en el plano vertical.
        push(200 + 2 * (s - 1) + 1, nid(s, 1), nid(s, 3), 2, (1.0, 0.0, 0.0))
        push(200 + 2 * (s - 1) + 2, nid(s, 2), nid(s, 4), 2, (1.0, 0.0, 0.0))
        # Puntales VPX (X, 6 m) IN30, M2+M3 liberados en ambos extremos.
        push(300 + 2 * (s - 1) + 1, nid(s, 1), nid(s, 2), 2, (0.0, 1.0, 0.0), **REL_I, **REL_J)
        push(300 + 2 * (s - 1) + 2, nid(s, 3), nid(s, 4), 2, (0.0, 1.0, 0.0), **REL_I, **REL_J)
        # Medias diagonales CAJ125X6 partidas en el cruce, liberadas SOLO en el
        # extremo de columna. Orden por diagonal (inferior, superior), como en
        # SAP: D{s}{cara}{1..4} = tag 400+8(s−1)+4·cara+k.
        for fi, (ca, cb, ctr) in enumerate([(1, 2, 40 + s), (3, 4, 50 + s)]):
            t = 400 + 8 * (s - 1) + 4 * fi
            push(t + 1, nid(s - 1, ca), ctr, 3, (0.0, 1.0, 0.0), **REL_I)  # inferior diag 1
            push(t + 2, ctr, nid(s, cb), 3, (0.0, 1.0, 0.0), **REL_J)      # superior diag 1
            push(t + 3, nid(s - 1, cb), ctr, 3, (0.0, 1.0, 0.0), **REL_I)  # inferior diag 2
            push(t + 4, ctr, nid(s, ca), 3, (0.0, 1.0, 0.0), **REL_J)      # superior diag 2
        # Arriostramiento de planta CAJ100X4, mismas reglas de release.
        t, ctr = 500 + 4 * (s - 1), 60 + s
        push(t + 1, nid(s, 1), ctr, 4, (0.0, 0.0, 1.0), **REL_I)
        push(t + 2, ctr, nid(s, 4), 4, (0.0, 0.0, 1.0), **REL_J)
        push(t + 3, nid(s, 2), ctr, 4, (0.0, 0.0, 1.0), **REL_I)
        push(t + 4, ctr, nid(s, 3), 4, (0.0, 0.0, 1.0), **REL_J)

    # Masa sísmica: P_nivel/4 por esquina (sin torsión), traslacional en X,Y,Z.
    # Material SIN masa (rho=0): en SAP la masa viene solo de las cargas.
    masses = [NodalMass(nid(s, c), (P_NIVEL[s] / 4.0 / G,) * 3 + (0.0,) * 3)
              for s in (1, 2, 3) for c in (1, 2, 3, 4)]

    return Model(nodes=nodes, materials=[Material(1, E=E_, nu=NU, rho=0.0)],
                 sections=SECS, elements=els, masses=masses)


model = make_tower_model()
COL11 = 101                      # columna esquina 1, piso 1 (extremo i = base)
D1A = (401, 402, 403, 404)       # medias diagonales piso 1, cara A

# ==================== MODAL: T*, R* Y MASAS PARTICIPANTES =============
N_MODES = 12


def modal_participation(mdl: Model, n_modes: int):
    """Períodos y razones de masa participante por dirección (como SAP)."""
    build(mdl)
    eigs = ops.eigen("-fullGenLapack", n_modes)
    periods = [2.0 * math.pi / math.sqrt(lam) for lam in eigs]
    entries = [(nm.node, nm.values[:3]) for nm in mdl.masses if any(nm.values[:3])]
    m_tot = [sum(v[d] for _, v in entries) for d in range(3)]
    ratios = [[], [], []]
    for k in range(1, n_modes + 1):
        m_gen, L = 0.0, [0.0, 0.0, 0.0]
        for node, mv in entries:
            for c, mc in enumerate(mv):
                if mc:
                    phi = ops.nodeEigenvector(node, k, c + 1)
                    m_gen += mc * phi * phi
                    L[c] += mc * phi
        for d in range(3):
            ratios[d].append(L[d] ** 2 / (m_gen * m_tot[d]))
    return periods, ratios


periods, pmasa = modal_participation(model, N_MODES)
ux_r, uy_r, uz_r = pmasa

# T* = período del modo con mayor masa traslacional en la dirección (§5.4).
ix_star = max(range(N_MODES), key=lambda i: ux_r[i])
iy_star = max(range(N_MODES), key=lambda i: uy_r[i])
T_STAR_X, T_STAR_Y = periods[ix_star], periods[iy_star]

# R* por dirección con la Ec. (1b), desde el T* del propio análisis modal.
R_STAR_X = r_star(T_STAR_X, R_TABLA)
R_STAR_Y = r_star(T_STAR_Y, R_TABLA)

# ===================== ESPECTROS POR CASO (como SAP) ==================
sp_x_dis = make_spectrum(sa_h, I_ * ESC02 / R_STAR_X)   # diseño X (Ec. 1a)
sp_y_dis = make_spectrum(sa_h, I_ * ESC02 / R_STAR_Y)   # diseño Y (Ec. 1a)
sp_h_ref = make_spectrum(sa_h, I_ * ESC02)              # referencia §6.1 (sin R)
sp_z_dis = make_spectrum(sa_v, I_ * ESC03 / R_V)        # vertical diseño (Ec. 2)

# ========================= CASOS ESPECTRALES ==========================


def ext_horizontal(dof: int) -> dict:
    # Las derivas dr{k} se combinan como respuesta modal propia (CQC de
    # derivas), no como resta de máximos CQC: los máximos de dos niveles no
    # ocurren en el mismo instante. Aquí difieren < 2 % (el modo dominante
    # lleva ~87-89 % de la masa), pero el extractor es la forma correcta y
    # alimenta la verificación §6.3 del post de deformaciones.
    return {
        "Q0": lambda: sum(ops.nodeReaction(n, dof) for n in BASES),
        "u1": lambda: ops.nodeDisp(nid(1, 1), dof),
        "u2": lambda: ops.nodeDisp(nid(2, 1), dof),
        "u3": lambda: ops.nodeDisp(nid(3, 1), dof),
        "dr1": lambda: ops.nodeDisp(nid(1, 1), dof),
        "dr2": lambda: ops.nodeDisp(nid(2, 1), dof) - ops.nodeDisp(nid(1, 1), dof),
        "dr3": lambda: ops.nodeDisp(nid(3, 1), dof) - ops.nodeDisp(nid(2, 1), dof),
        "colP": lambda: -ops.eleResponse(COL11, "localForces")[0],
        "colM3": lambda: ops.eleResponse(COL11, "localForces")[5],
    }


def run_case(sp: Spectrum, direction: str, extractors: dict, xi: float) -> dict:
    build(model)
    res = run_directional_spectral(model, sp, direction, extractors,
                                   damping=xi, n_modes=N_MODES)
    # SAP entrega los CQC positivos: se reporta la magnitud.
    return {k: abs(res.combined(k, "CQC")) for k in extractors}


ext_x = ext_horizontal(1)
ext_x.update({f"D1A{k}": (lambda tag=tag: -ops.eleResponse(tag, "localForces")[0])
              for k, tag in enumerate(D1A, start=1)})

RSX_DIS = run_case(sp_x_dis, "Ux", ext_x, XI_H)
RSY_DIS = run_case(sp_y_dis, "Uy", ext_horizontal(2), XI_H)
RSX_REF = run_case(sp_h_ref, "Ux", ext_horizontal(1), XI_H)
RSY_REF = run_case(sp_h_ref, "Uy", ext_horizontal(2), XI_H)
RSZ_DIS = run_case(sp_z_dis, "Uz",
                   {"Q0": lambda: sum(ops.nodeReaction(n, 3) for n in BASES)}, XI_V)

# ==================== POST-PROCESO NORMATIVO ==========================
Q0MIN = 0.25 * I_ * (AR * S_) * P_TOTAL                      # Ec. (12); Ar·S/g = 0,56
Q0MAX = 2.75 * I_ * AR * S_ / (R_TABLA + 1.0) * ESC02 * P_TOTAL  # Ec. (13)


def banda(q0: float) -> str:
    """Posición del corte basal en la banda Q0mín/Q0máx (Ecs. 12 y 13)."""
    if q0 < Q0MIN:
        return "BAJO Q0min -> amplificar por Q0min/Q0 (obligatorio, Ec. 12)"
    if q0 > Q0MAX:
        return "SOBRE Q0max -> recorte opcional (Ec. 13, §5.13)"
    return "dentro de la banda"


def r1(r_est: float, q0: float) -> float:
    """Ec. (14): R1 = R*·min(Q0/Q0mín; 1)."""
    return r_est * min(q0 / Q0MIN, 1.0)


R1_X, R1_Y = r1(R_STAR_X, RSX_DIS["Q0"]), r1(R_STAR_Y, RSY_DIS["Q0"])

# ============ REFERENCIA SAP2000 (v25, vía MCP, torre_cbf_mrf.sdb) ============
SAP_T = [0.9956718610259325, 0.3773198547254339, 0.2693380143954706,
         0.22018507693652142, 0.1406833613427464, 0.13913695750363383,
         0.10267683083068721, 0.07432103783404385, 0.06815490625974081,
         0.05786183341839766, 0.05690707068346985, 0.05436326258464671]
SAP_PM_UY1, SAP_PM_UX4 = 0.871135, 0.891008     # masas participantes dominantes
SAP_SUM_UX, SAP_SUM_UY = 0.9723226715049605, 0.9999995435124162
SAP_R_STAR_X = 3.8495358819445884               # 1,5 + 3,5·T*_X/0,328
# Referencias re-extraídas el 2026-08-11 con DampRatio de las funciones = ξ del
# caso (ver el gotcha en el docstring): sin el ajuste interno de SAP.
SAP_Q0 = {"RSX_DIS": 474.8771023518899, "RSY_DIS": 255.90984459005924,
          "RSX_REF": 1828.0564450174725, "RSY_REF": 1279.549222950296,
          "RSZ_DIS": 419.8168852847656}
SAP_U = {"RSX_DIS": (0.0024835935108407344, 0.005110112542013143, 0.006751484889126112),
         "RSX_REF": (0.009560682336146141, 0.01967156159125466, 0.025990083337097642),
         "RSY_DIS": (0.022444107034522907, 0.05626981961914234, 0.07834022622871419),
         "RSY_REF": (0.11222053517261452, 0.2813490980957116, 0.3917011311435709)}
# Medias diagonales piso 1 cara A bajo RSX_DIS (P, kN): 1/3 inferiores, 2/4 superiores
# (conectividad verificada en el modelo: D1A1=N01→C1A, D1A2=N12→C1A, D1A3=N02→C1A,
# D1A4=N11→C1A, liberadas en el extremo de esquina).
SAP_D1A = (142.8653012101638, 142.8324650804491, 142.86530092168053, 142.83246479566293)
SAP_COL11 = {"P": 174.7161191540306, "M3": 200.95231638493965}  # base, RSY_DIS

# ============================ COMPARACIÓN =============================
print("Caso 9 - Torre CBF/MRF: AME NCh2369:2025 con espectro por direccion (Rukan vs SAP2000)")
print("  Anclas del espectro (Ecs. 3/4/1a/1b vs nch2369-spectrum.ts, a mano): OK (6 puntos)\n")

print("  Periodos (12 modos):")
for i, (t, s) in enumerate(zip(periods, SAP_T), start=1):
    err = abs(t - s) / s * 100.0
    print(f"    T{i:<2d} Rukan {t:.9f}  SAP {s:.9f}  err {err:8.5f}%")

print("\n  Masas participantes (razones):")
print(f"    modo 1 Uy: Rukan {uy_r[0]:.6f}  SAP {SAP_PM_UY1:.6f}   <- T*_Y")
print(f"    modo 4 Ux: Rukan {ux_r[3]:.6f}  SAP {SAP_PM_UX4:.6f}   <- T*_X")
print(f"    Suma Ux = {sum(ux_r):.6f} (SAP {SAP_SUM_UX:.6f});  "
      f"Suma Uy = {sum(uy_r):.6f} (SAP {SAP_SUM_UY:.6f})  [>= 0,90, §5.6.2]")

print("\n  T* y R* por direccion (Ec. 1b, CrT1 = 0,328 s):")
print(f"    X (CBF): T* = T{ix_star+1} = {T_STAR_X:.6f} s < 0,328 -> "
      f"R*_X = {R_STAR_X:.10f} (SAP {SAP_R_STAR_X:.10f})")
print(f"    Y (MRF): T* = T{iy_star+1} = {T_STAR_Y:.6f} s >= 0,328 -> R*_Y = {R_STAR_Y:.1f}")

print("\n  Cortes basales CQC [kN]:")
CASOS = {"RSX_DIS": RSX_DIS, "RSY_DIS": RSY_DIS, "RSX_REF": RSX_REF,
         "RSY_REF": RSY_REF, "RSZ_DIS": RSZ_DIS}
for name, caso in CASOS.items():
    r, s = caso["Q0"], SAP_Q0[name]
    print(f"    {name}  Rukan {r:12.4f}  SAP {s:12.4f}  err {abs(r-s)/s*100:8.5f}%")

print("\n  Desplazamientos por nivel, columna esquina 1 [m]:")
for name in ("RSX_DIS", "RSX_REF", "RSY_DIS", "RSY_REF"):
    for lev in (1, 2, 3):
        r, s = CASOS[name][f"u{lev}"], SAP_U[name][lev - 1]
        print(f"    {name} n{lev}  Rukan {r:.9f}  SAP {s:.9f}  err {abs(r-s)/s*100:8.5f}%")

print("\n  Derivas de entrepiso §6.3 (CQC de derivas modales), espectro de referencia [mm]:")
LIM_63 = 0.015 * 4.0 * 1000.0  # 0,015·h con h = 4 000 mm
for name, rot in (("RSX_REF", "X (CBF)"), ("RSY_REF", "Y (MRF)")):
    ds = [CASOS[name][f"dr{i}"] * 1000.0 for i in (1, 2, 3)]
    veredictos = "  ".join(f"piso {i}: {d:8.3f} ({d/LIM_63:5.3f} del limite)"
                           for i, d in enumerate(ds, start=1))
    print(f"    {rot}  {veredictos}")

print("\n  Medias diagonales piso 1 cara A, axial P bajo RSX_DIS [kN]:")
for k in (1, 2, 3, 4):
    r, s = RSX_DIS[f"D1A{k}"], SAP_D1A[k - 1]
    print(f"    D1A{k}  Rukan {r:.6f}  SAP {s:.6f}  err {abs(r-s)/s*100:8.5f}%")

print("\n  COL11 en la base bajo RSY_DIS (plano MRF, eje fuerte):")
print(f"    P  [kN]   Rukan {RSY_DIS['colP']:.6f}  SAP {SAP_COL11['P']:.6f}  "
      f"err {abs(RSY_DIS['colP']-SAP_COL11['P'])/SAP_COL11['P']*100:.5f}%")
print(f"    M3 [kN m] Rukan {RSY_DIS['colM3']:.6f}  SAP {SAP_COL11['M3']:.6f}  "
      f"err {abs(RSY_DIS['colM3']-SAP_COL11['M3'])/SAP_COL11['M3']*100:.5f}%")

# Combinación direccional 100/30 (§4.5.2) sobre la columna de esquina.
p_dir = directional_combination(RSX_DIS["colP"], RSY_DIS["colP"], 0.3)
m_dir = directional_combination(RSX_DIS["colM3"], RSY_DIS["colM3"], 0.3)
print("\n  Combinacion direccional 100/30 (COL11 base, X vs Y de diseno):")
print(f"    P  : X {RSX_DIS['colP']:9.4f}  Y {RSY_DIS['colP']:9.4f}  -> 100/30 = {p_dir:9.4f} kN")
print(f"    M3 : X {RSX_DIS['colM3']:9.4f}  Y {RSY_DIS['colM3']:9.4f}  -> 100/30 = {m_dir:9.4f} kN m")

print("\n  Cadena normativa por direccion (P = 1200 kN):")
print(f"    Q0min = {Q0MIN:.4f} kN (Ec. 12)   Q0max = {Q0MAX:.4f} kN (Ec. 13)")
print(f"    X: T* {T_STAR_X:.4f} s  R* {R_STAR_X:.4f}  Q0 {RSX_DIS['Q0']:8.2f} kN  "
      f"-> {banda(RSX_DIS['Q0'])}")
print(f"       R1_X = {R1_X:.4f}  ->  0,7·R1_X = {0.7*R1_X:.4f}")
print(f"    Y: T* {T_STAR_Y:.4f} s  R* {R_STAR_Y:.4f}  Q0 {RSY_DIS['Q0']:8.2f} kN  "
      f"-> {banda(RSY_DIS['Q0'])}")
print(f"       R1_Y = {R1_Y:.4f}  ->  0,7·R1_Y = {0.7*R1_Y:.4f}")
print(f"    Vertical: Q0Z = {RSZ_DIS['Q0']:.2f} kN (R_V = 2, xi_V = 0,03)")

# ============================ TOLERANCIAS =============================
TOL = 1e-4  # relativa (0,01 %), como los casos 5-8 con tabla espectral idéntica


def check(name: str, ruk: float, sap: float, tol: float = TOL) -> None:
    err = abs(abs(ruk) - abs(sap)) / abs(sap)
    assert err < tol, f"{name}: Rukan {ruk!r} vs SAP {sap!r} (err rel {err:.3e})"


# Modal: los 12 periodos y las masas participantes dominantes.
for i, (t, s) in enumerate(zip(periods, SAP_T), start=1):
    check(f"periodo modo {i}", t, s)
assert abs(uy_r[0] - SAP_PM_UY1) < 1e-3, "masa participante Uy modo 1"
assert abs(ux_r[3] - SAP_PM_UX4) < 1e-3, "masa participante Ux modo 4"
assert sum(ux_r) >= 0.90 and sum(uy_r) >= 0.90, "90% de masa (§5.6.2)"

# R* por direccion desde el T* propio (Ec. 1b).
assert ix_star == 3 and iy_star == 0, "modos dominantes: T*_X = modo 4, T*_Y = modo 1"
check("R*_X", R_STAR_X, SAP_R_STAR_X)
assert R_STAR_Y == 5.0, "R*_Y (T*_Y >= CrT1 -> R* = R)"

# Cortes basales CQC de los 5 casos.
for name, caso in CASOS.items():
    check(f"Q0 {name}", caso["Q0"], SAP_Q0[name])

# Desplazamientos por nivel de las 4 columnas de la tabla.
for name, refs in SAP_U.items():
    for lev in (1, 2, 3):
        check(f"{name} u{lev}", CASOS[name][f"u{lev}"], refs[lev - 1])

# Axiales de las 4 medias diagonales y columna COL11 en la base.
for k in (1, 2, 3, 4):
    check(f"D1A{k}", RSX_DIS[f"D1A{k}"], SAP_D1A[k - 1])
check("COL11 P", RSY_DIS["colP"], SAP_COL11["P"])
check("COL11 M3", RSY_DIS["colM3"], SAP_COL11["M3"])

# Derivas §6.3 (regresión rukan; SAP no exporta la deriva CQC directamente en
# modelos sin diafragma, así que la referencia es el propio extractor, anclado
# la primera vez el 2026-08-12 y citado por el post de deformaciones).
DERIVAS_REF = {"RSX_REF": (9.561, 10.121, 6.368),
               "RSY_REF": (112.221, 169.469, 112.137)}  # mm
for name, refs in DERIVAS_REF.items():
    for i, ref in enumerate(refs, start=1):
        check(f"{name} dr{i}", CASOS[name][f"dr{i}"] * 1000.0, ref, 5e-4)
assert max(CASOS["RSX_REF"][f"dr{i}"] * 1000.0 for i in (1, 2, 3)) < LIM_63, \
    "X cumple 0,015h (§6.3)"
assert all(CASOS["RSY_REF"][f"dr{i}"] * 1000.0 > LIM_63 for i in (1, 2, 3)), \
    "Y excede 0,015h en los tres pisos (§6.3) - el hallazgo del post 3"

# Cadena normativa: banda, R1 y consistencias internas.
assert abs(Q0MIN - 168.0) < 1e-9, "Q0min = 0,25·0,56·1200 (Ec. 12)"
assert abs(Q0MAX - 444.3515710194218) < 1e-9, "Q0max = 2,75·0,56/6·1,4427·1200 (Ec. 13)"
assert RSX_DIS["Q0"] > Q0MAX, "X sobre Q0max (recorte opcional)"
assert Q0MIN < RSY_DIS["Q0"] < Q0MAX, "Y dentro de la banda"
check("R1_X", R1_X, SAP_R_STAR_X)  # Q0X > Q0min -> R1 = R*
assert R1_Y == 5.0, "R1_Y"
# Linealidad del espectro: referencia = diseno × R* (misma forma, distinta escala).
check("REF/DIS X = R*_X", RSX_REF["Q0"] / RSX_DIS["Q0"], R_STAR_X, 1e-9)
check("REF/DIS Y = R*_Y", RSY_REF["Q0"] / RSY_DIS["Q0"], R_STAR_Y, 1e-9)
# La 100/30 domina a cada direccion por separado.
assert p_dir >= max(RSX_DIS["colP"], RSY_DIS["colP"])

print("\n  OK - torre CBF/MRF: 12 periodos, 5 cortes basales, 12 desplazamientos,")
print("       4 diagonales y COL11 reproducen SAP2000 a < 0,01%; espectro por")
print("       direccion anclado a struct_pad; cadena T* -> R* -> Q0 -> banda -> R1")
print("       verificada (R de tabla igual, R1 distinto: el analisis lo decide).")
