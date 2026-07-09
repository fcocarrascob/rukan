"""Caso 2 — Edificio de corte de 2 GDL (análisis modal multi-grado).

Verifica el análisis modal de OpenSees en un sistema de 2 GDL contra la
solución analítica cerrada: dos períodos, dos formas modales y los factores de
participación / masas modales efectivas.

Sistema: edificio de corte de dos pisos (vigas infinitamente rígidas → los
nudos no rotan, cada columna trabaja doblemente empotrada). Con pisos iguales
(misma rigidez k y misma masa m) las matrices son

    K = k · [[ 2, -1], [-1, 1]]      M = m · [[1, 0], [0, 1]]

y el problema de autovalores (K - ω²M)φ = 0 tiene solución exacta en términos
de la razón áurea. Definiendo β = ω²·m/k:

    β² - 3β + 1 = 0   →   β = (3 ∓ √5)/2 = {0.381966, 2.618034}

Las formas modales resultan φ⁽¹⁾ = (1, 1.618034) y φ⁽²⁾ = (1, -0.618034),
donde 1.618034 = (1+√5)/2 es la razón áurea.

En OpenSees el edificio de corte se reproduce de forma exacta con columnas
'elasticBeamColumn' fijando la rotación (Rz) y el desplazamiento vertical (Uy)
en cada piso: ambos extremos de cada columna quedan sin giro → rigidez lateral
12·E·I/h³ por piso, idéntica a la hipótesis de vigas rígidas.

Referencia: Chopra, A. K., *Dynamics of Structures*, cap. 10 (sistemas de
varios GDL, análisis modal).
"""

from __future__ import annotations

import math

import openseespy.opensees as ops

from rukan import units as u

# --- Datos de entrada (con unidades: la frontera Pint) ---
E = 200 * u.ureg.GPa            # acero estructural
Iz = 1.0e-4 * u.ureg.m**4       # columna ~ HEB240 (10 000 cm⁴)
A = 1.0e-2 * u.ureg.m**2        # irrelevante (Uy fijo, sin deformación axial)
h = 3.0 * u.ureg.m              # altura de piso
m_floor = 10 * u.ureg.tonne     # masa por piso (igual en ambos)

# --- Frontera: a floats en el sistema interno (kN, m, s, tonne) ---
E_ = u.stress(E)
Iz_ = u.inertia(Iz)
A_ = u.area(A)
h_ = u.length(h)
m_ = u.mass(m_floor)

# Rigidez de corte de un piso: columna doblemente empotrada.
k_ = 12.0 * E_ * Iz_ / h_**3

# --- Modelo OpenSees: stick de 3 nodos (base + 2 pisos) ---
ops.wipe()
ops.model("basic", "-ndm", 2, "-ndf", 3)  # 2D: GDL por nodo (Ux, Uy, Rz)

ops.node(1, 0.0, 0.0)      # base
ops.node(2, 0.0, h_)       # piso 1
ops.node(3, 0.0, 2.0 * h_)  # piso 2

ops.fix(1, 1, 1, 1)        # base empotrada
ops.fix(2, 0, 1, 1)        # piso 1: solo Ux libre (edificio de corte)
ops.fix(3, 0, 1, 1)        # piso 2: solo Ux libre

# Masas laterales concentradas en cada piso.
ops.mass(2, m_, 0.0, 0.0)
ops.mass(3, m_, 0.0, 0.0)

ops.geomTransf("Linear", 1)
ops.element("elasticBeamColumn", 1, 1, 2, A_, E_, Iz_, 1)
ops.element("elasticBeamColumn", 2, 2, 3, A_, E_, Iz_, 1)

# --- Análisis modal (2 modos; fullGenLapack extrae todos los de un sistema
# chico sin problema; el aviso "VERY SLOW" es irrelevante a esta escala) ---
eigenvalues = ops.eigen("-fullGenLapack", 2)
omega = [math.sqrt(lam) for lam in eigenvalues]
T_os = [2.0 * math.pi / w for w in omega]

# Formas modales (componente Ux de cada piso), normalizadas a φ_piso1 = 1.
phi_os = []
for mode in (1, 2):
    p1 = ops.nodeEigenvector(2, mode, 1)
    p2 = ops.nodeEigenvector(3, mode, 1)
    phi_os.append((1.0, p2 / p1))

# Factores de participación y masa modal efectiva (movimiento horizontal del
# suelo → vector de influencia ι = [1, 1]). Γ = Σmφ / Σmφ² ; M* = (Σmφ)²/Σmφ².
masses = [m_, m_]
part_os, meff_os = [], []
for (f1, f2) in phi_os:
    phi = [f1, f2]
    s_mphi = sum(mi * pi for mi, pi in zip(masses, phi))
    s_mphi2 = sum(mi * pi * pi for mi, pi in zip(masses, phi))
    part_os.append(s_mphi / s_mphi2)
    meff_os.append(s_mphi**2 / s_mphi2)
m_total = sum(masses)

# --- Solución analítica (razón áurea) ---
sqrt5 = math.sqrt(5.0)
beta = [(3.0 - sqrt5) / 2.0, (3.0 + sqrt5) / 2.0]
omega_h = [math.sqrt(b * k_ / m_) for b in beta]
T_h = [2.0 * math.pi / w for w in omega_h]
phi_h = [(1.0, 2.0 - beta[0]), (1.0, 2.0 - beta[1])]  # (1, 1.618034) y (1, -0.618034)
part_h, meff_h = [], []
for (f1, f2) in phi_h:
    phi = [f1, f2]
    s_mphi = sum(mi * pi for mi, pi in zip(masses, phi))
    s_mphi2 = sum(mi * pi * pi for mi, pi in zip(masses, phi))
    part_h.append(s_mphi / s_mphi2)
    meff_h.append(s_mphi**2 / s_mphi2)

# --- Comparación ---
print("Caso 2 - Edificio de corte de 2 GDL")
print(f"  k (rigidez de piso) = {k_:12.4f} kN/m")
print(f"  m (masa de piso)    = {m_:12.4f} tonne\n")

print("  Periodos [s]           a mano      OpenSees      error %")
for i in range(2):
    err = abs(T_os[i] - T_h[i]) / T_h[i] * 100.0
    print(f"    T{i + 1}                 {T_h[i]:10.6f}  {T_os[i]:10.6f}  {err:10.6f}")

print("\n  Forma modal (phi2/phi1)  a mano      OpenSees")
for i in range(2):
    print(f"    Modo {i + 1}             {phi_h[i][1]:10.6f}  {phi_os[i][1]:10.6f}")

print("\n  Masa modal efectiva      a mano      OpenSees")
for i in range(2):
    r_h = meff_h[i] / m_total * 100.0
    r_os = meff_os[i] / m_total * 100.0
    print(f"    Modo {i + 1} [% masa]      {r_h:9.4f}%  {r_os:9.4f}%")

# --- Tolerancias ---
TOL_PCT = 0.01
for i in range(2):
    err_T = abs(T_os[i] - T_h[i]) / T_h[i] * 100.0
    err_phi = abs(phi_os[i][1] - phi_h[i][1]) / abs(phi_h[i][1]) * 100.0
    err_m = abs(meff_os[i] - meff_h[i]) / meff_h[i] * 100.0
    assert err_T < TOL_PCT, f"Modo {i + 1}: error en periodo {err_T:.6f}%"
    assert err_phi < TOL_PCT, f"Modo {i + 1}: error en forma modal {err_phi:.6f}%"
    assert err_m < TOL_PCT, f"Modo {i + 1}: error en masa efectiva {err_m:.6f}%"

print("\n  OK - suma de masas efectivas = "
      f"{sum(meff_os) / m_total * 100.0:.4f}% del total")
