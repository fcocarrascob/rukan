"""Caso 3 — Reticulado triangular (estática, fuerzas axiales).

Primer caso de análisis estático de Rukan. Verifica las fuerzas axiales que
OpenSees calcula en las barras de un reticulado isostático contra la solución
a mano por el método de los nudos.

Sistema: reticulado triangular simétrico (tipo pendolón). Apoyo fijo (rótula)
en A, apoyo móvil (rodillo) en B, ambos en la base; nudo superior C en el
vértice, con una carga vertical P hacia abajo.

        C  (b/2, h)
       / \\        ↓ P
      /   \\
     A-----B
   (0,0)  (b,0)

Al ser isostático (m + r = 2j: 3 barras + 3 reacciones = 2·3 nudos), las
fuerzas de barra no dependen de EA. Por simetría, con ángulo θ de las
diagonales respecto a la horizontal (tanθ = h/(b/2)):

    diagonales:   N = -P / (2 senθ)        (compresión)
    cordón inf.:  N = (P/2)·(b/2)/h        (tracción)

Convención de OpenSees para 'Truss': fuerza axial positiva = tracción.

Referencia: Hibbeler, *Structural Analysis*, método de los nudos (análisis de
armaduras isostáticas).
"""

from __future__ import annotations

import math

import openseespy.opensees as ops

from rukan import units as u

# --- Datos de entrada (con unidades: la frontera Pint) ---
b = 6.0 * u.ureg.m           # luz de la base
h = 3.0 * u.ureg.m           # altura del vértice
P = 100.0 * u.ureg.kN        # carga vertical en el vértice
E = 200 * u.ureg.GPa         # acero (irrelevante en isostático, pero real)
A_bar = 20 * u.ureg.cm**2    # área de barra (idem)

# --- Frontera: a floats en el sistema interno (kN, m) ---
b_ = u.length(b)
h_ = u.length(h)
P_ = u.force(P)
E_ = u.stress(E)
A_ = u.area(A_bar)

# --- Modelo OpenSees: reticulado 2D (2 GDL por nodo) ---
ops.wipe()
ops.model("basic", "-ndm", 2, "-ndf", 2)

ops.node(1, 0.0, 0.0)        # A
ops.node(2, b_, 0.0)         # B
ops.node(3, b_ / 2.0, h_)    # C (vértice)

ops.fix(1, 1, 1)             # A: rótula (Ux, Uy fijos)
ops.fix(2, 0, 1)             # B: rodillo (solo Uy fijo)

ops.uniaxialMaterial("Elastic", 1, E_)
ops.element("Truss", 1, 1, 3, A_, 1)   # A-C (diagonal)
ops.element("Truss", 2, 3, 2, A_, 1)   # C-B (diagonal)
ops.element("Truss", 3, 1, 2, A_, 1)   # A-B (cordón inferior)

# Carga vertical hacia abajo en el vértice.
ops.timeSeries("Linear", 1)
ops.pattern("Plain", 1, 1)
ops.load(3, 0.0, -P_)

# --- Análisis estático lineal ---
ops.system("BandSPD")
ops.numberer("RCM")
ops.constraints("Plain")
ops.integrator("LoadControl", 1.0)
ops.algorithm("Linear")
ops.analysis("Static")
ops.analyze(1)

# Fuerzas axiales de OpenSees (positivo = tracción).
N_os = {tag: ops.eleResponse(tag, "axialForce")[0] for tag in (1, 2, 3)}

# --- Solución a mano (método de los nudos) ---
theta = math.atan2(h_, b_ / 2.0)
N_diag = -P_ / (2.0 * math.sin(theta))       # compresión
N_bottom = (P_ / 2.0) * (b_ / 2.0) / h_       # tracción
N_hand = {1: N_diag, 2: N_diag, 3: N_bottom}

# --- Comparación ---
labels = {1: "A-C (diagonal)", 2: "C-B (diagonal)", 3: "A-B (cordon inf.)"}
print("Caso 3 - Reticulado triangular (estatica)")
print(f"  P = {P_:.1f} kN,  b = {b_:.1f} m,  h = {h_:.1f} m,  theta = {math.degrees(theta):.2f} deg\n")
print("  Barra              a mano [kN]   OpenSees [kN]     error %")
for tag in (1, 2, 3):
    err = abs(N_os[tag] - N_hand[tag]) / abs(N_hand[tag]) * 100.0
    signo = "T" if N_hand[tag] > 0 else "C"
    print(f"    {labels[tag]:18s} {N_hand[tag]:10.4f}   {N_os[tag]:12.4f}   {err:9.6f}  ({signo})")

TOL_PCT = 0.001
for tag in (1, 2, 3):
    err = abs(N_os[tag] - N_hand[tag]) / abs(N_hand[tag]) * 100.0
    assert err < TOL_PCT, f"Barra {tag}: error {err:.6f}% excede tolerancia"

# Chequeo de equilibrio global: reacciones verticales = P/2 cada apoyo.
ops.reactions()
Ay = ops.nodeReaction(1, 2)
By = ops.nodeReaction(2, 2)
print(f"\n  Reacciones verticales: Ay = {Ay:.3f} kN, By = {By:.3f} kN (esperado P/2 = {P_/2:.3f})")
assert abs(Ay - P_ / 2.0) < 1e-6 and abs(By - P_ / 2.0) < 1e-6, "Reacciones no equilibran"
print("  OK")
