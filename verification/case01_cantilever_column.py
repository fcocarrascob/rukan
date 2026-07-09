"""Caso 1 — Columna en voladizo con masa en la punta.

Verifica el *toolchain* (OpenSeesPy + capa de unidades) contra la solución
analítica de dinámica estructural para un sistema de 1 GDL.

Sistema: columna vertical empotrada en la base, masa concentrada ``m`` en la
punta. La rigidez lateral de una columna empotrada-libre gobernada por flexión
es

    k = 3·E·I / L³

y el período fundamental de un oscilador de 1 GDL sin amortiguar:

    T = 2π·√(m / k) = 2π·√( m·L³ / (3·E·I) )

El elemento ``elasticBeamColumn`` de OpenSees usa funciones de forma cúbicas
exactas para una viga prismática Euler-Bernoulli, de modo que la rigidez de
punta reproduce 3EI/L³ de forma exacta: la discrepancia esperada es de orden
del error de máquina.

Referencia: Chopra, A. K., *Dynamics of Structures*, cap. 2 (sistema de 1 GDL).
"""

from __future__ import annotations

import math

import openseespy.opensees as ops

from rukan import units as u

# --- Datos de entrada (con unidades: la frontera Pint) ---
E = 200 * u.ureg.GPa            # acero estructural
Iz = 1.0e-4 * u.ureg.m**4       # = 10 000 cm⁴
A = 1.0e-2 * u.ureg.m**2        # no influye en la respuesta lateral
L = 3.0 * u.ureg.m
m_tip = 1000 * u.ureg.kg        # masa concentrada en la punta

# --- Frontera: a floats en el sistema interno (kN, m, s, tonne) ---
E_ = u.stress(E)
Iz_ = u.inertia(Iz)
A_ = u.area(A)
L_ = u.length(L)
m_ = u.mass(m_tip)

# --- Modelo OpenSees: 2 nodos, columna vertical, base empotrada ---
ops.wipe()
ops.model("basic", "-ndm", 2, "-ndf", 3)  # 2D: GDL por nodo (Ux, Uy, Rz)

ops.node(1, 0.0, 0.0)  # base
ops.node(2, 0.0, L_)   # punta
ops.fix(1, 1, 1, 1)    # empotramiento en la base

# Masa lateral (Ux) en la punta; despreciable en Uy/Rz.
ops.mass(2, m_, 0.0, 0.0)

ops.geomTransf("Linear", 1)
ops.element("elasticBeamColumn", 1, 1, 2, A_, E_, Iz_, 1)

# --- Análisis modal ---
# Se usa 'fullGenLapack' porque la matriz de masa es singular (solo el GDL
# lateral tiene masa): el solver por defecto exige masa positiva en todos los
# GDL activos. El aviso "VERY SLOW" es irrelevante en un modelo de este tamaño.
eigenvalues = ops.eigen("-fullGenLapack", 1)  # devuelve [omega²]
omega2 = eigenvalues[0]
T_opensees = 2.0 * math.pi / math.sqrt(omega2)

# --- Solución analítica ---
k_hand = 3.0 * E_ * Iz_ / L_**3
T_hand = 2.0 * math.pi * math.sqrt(m_ / k_hand)

# --- Comparación ---
error_pct = abs(T_opensees - T_hand) / T_hand * 100.0

print("Caso 1 - Columna en voladizo con masa en la punta")
print(f"  k (a mano)    = {k_hand:12.4f} kN/m")
print(f"  T (a mano)    = {T_hand:12.6f} s")
print(f"  T (OpenSees)  = {T_opensees:12.6f} s")
print(f"  error         = {error_pct:12.6f} %")

TOL_PCT = 0.01
assert error_pct < TOL_PCT, (
    f"Discrepancia {error_pct:.6f}% excede la tolerancia de {TOL_PCT}%"
)
print("  OK")
