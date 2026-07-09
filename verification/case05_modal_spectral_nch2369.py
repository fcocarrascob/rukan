"""Caso 5 — Modal espectral 2D (NCh2369), Rukan vs SAP2000.

El peldaño decisivo de la escalera de verificación: donde el cálculo a mano deja
de alcanzar y el patrón de referencia pasa a ser **SAP2000**. Verifica dos cosas
encadenadas sobre un mismo pórtico plano:

1.  El **análisis modal** del ensamblador 3D de Rukan (``engine.build``): que los
    períodos y las masas modales efectivas reproduzcan los de SAP2000.
2.  El **análisis de respuesta espectral propio** (``rukan.modal``): aplicar el
    espectro NCh2369 modo a modo y combinar con **CQC y SRSS**, algo que
    OpenSees no hace de un botón. Se contrasta el corte basal combinado y el
    desplazamiento de techo contra SAP2000.

Sistema: pórtico plano de momento, 1 vano de 6 m, 2 pisos de 4 m, en el plano
X-Z. Columnas y vigas ``elasticBeamColumn`` (Euler-Bernoulli); en SAP2000 las
secciones se definen con **área de corte nula** para desactivar la deformación
por corte y así igualar exactamente el modelo de OpenSees. Masas laterales
concentradas: 10 t en el piso 1 y 8 t en el techo.

Espectro NCh2369: zona 2, suelo C, I = 1.0, R = 5, ξ = 3 %. La misma tabla
``(T, Sa/g)`` se alimenta a ambos motores (ver ``rukan.spectra``).

Patrón de referencia: SAP2000 v25, extraído vía MCP (modelo
``case5_portico2p.sdb``). Factor de escala del caso RS = 9.80665 (g en m/s²),
que es la misma ``G`` con la que Rukan convierte Sa/g a pseudo-aceleración.
"""

from __future__ import annotations

from rukan import units as u
from rukan.engine import build
from rukan.model import FrameElement, Material, Model, NodalMass, Node, Section
from rukan.modal import modal_displacement, run_spectral
from rukan.spectra import nch2369_spectrum

# =============================== DATOS ================================
E = 200 * u.ureg.GPa
NU = 0.3
L = 6.0 * u.ureg.m      # luz del vano
H = 4.0 * u.ureg.m      # altura de piso

# Secciones (propiedades explícitas, idénticas a las de SAP2000).
# Iz = inercia de flexión EN EL PLANO (eje fuerte); Iy = fuera de plano.
COL = dict(A=0.0106 * u.ureg.m**2, Iz=1.126e-4 * u.ureg.m**4,
           Iy=3.92e-5 * u.ureg.m**4, J=1.03e-6 * u.ureg.m**4)
BEAM = dict(A=0.00538 * u.ureg.m**2, Iz=8.356e-5 * u.ureg.m**4,
            Iy=6.04e-6 * u.ureg.m**4, J=2.01e-7 * u.ureg.m**4)

M_FLOOR1 = 5.0 * u.ureg.tonne   # por nudo (2 nudos → 10 t en el piso 1)
M_FLOOR2 = 4.0 * u.ureg.tonne   # por nudo (2 nudos → 8 t en el techo)

# --- Frontera Pint → floats del sistema interno (kN, m, s, tonne) ---
E_ = u.stress(E)
G_ = E_ / (2.0 * (1.0 + NU))
L_ = u.length(L)
H_ = u.length(H)

# ===================== MODELO (3D, plano X-Z) ========================
# GDL en el plano: Ux, Uz, Ry. Restringidos fuera de plano: Uy, Rx, Rz.
FREE_PLANE = (False, True, False, True, False, True)
FIXED = (True, True, True, True, True, True)

nodes = [
    Node(1, 0.0, 0.0, 0.0, FIXED),        # base izq
    Node(2, L_, 0.0, 0.0, FIXED),         # base der
    Node(3, 0.0, 0.0, H_, FREE_PLANE),    # piso 1 izq
    Node(4, L_, 0.0, H_, FREE_PLANE),     # piso 1 der
    Node(5, 0.0, 0.0, 2 * H_, FREE_PLANE),  # techo izq
    Node(6, L_, 0.0, 2 * H_, FREE_PLANE),   # techo der
]

materials = [Material(1, E=E_, nu=NU, rho=0.0)]  # sin masa propia
sections = [
    Section(1, A=u.area(COL["A"]), Iy=u.inertia(COL["Iy"]),
            Iz=u.inertia(COL["Iz"]), J=u.inertia(COL["J"])),      # columnas
    Section(2, A=u.area(BEAM["A"]), Iy=u.inertia(BEAM["Iy"]),
            Iz=u.inertia(BEAM["Iz"]), J=u.inertia(BEAM["J"])),    # vigas
]

# vecxz=(0,1,0) → eje local z = Y global (fuera de plano): Iz flexiona en el
# plano X-Z, tanto para columnas (eje Z) como para vigas (eje X).
VECXZ = (0.0, 1.0, 0.0)
elements = [
    FrameElement(1, 1, 3, 1, 1, VECXZ),  # columna izq inferior
    FrameElement(2, 3, 5, 1, 1, VECXZ),  # columna izq superior
    FrameElement(3, 2, 4, 1, 1, VECXZ),  # columna der inferior
    FrameElement(4, 4, 6, 1, 1, VECXZ),  # columna der superior
    FrameElement(5, 3, 4, 1, 2, VECXZ),  # dintel piso 1
    FrameElement(6, 5, 6, 1, 2, VECXZ),  # dintel techo
]

m1 = u.mass(M_FLOOR1)
m2 = u.mass(M_FLOOR2)
masses = [
    NodalMass(3, (m1, 0.0, 0.0, 0.0, 0.0, 0.0)),
    NodalMass(4, (m1, 0.0, 0.0, 0.0, 0.0, 0.0)),
    NodalMass(5, (m2, 0.0, 0.0, 0.0, 0.0, 0.0)),
    NodalMass(6, (m2, 0.0, 0.0, 0.0, 0.0, 0.0)),
]

model = Model(nodes=nodes, materials=materials, sections=sections,
              elements=elements, masses=masses)

# ===================== ANÁLISIS ESPECTRAL ============================
build(model)
spectrum = nch2369_spectrum(zone=2, soil="C", importance=1.0, R=5.0, damping=0.03)
res = run_spectral(model, spectrum, direction="Ux", damping=0.03, n_modes=4)

V_cqc = res.base_shear("CQC")
V_srss = res.base_shear("SRSS")
roof_cqc = modal_displacement(res, node=5, direction="Ux", rule="CQC")
roof_srss = modal_displacement(res, node=5, direction="Ux", rule="SRSS")

# ============ REFERENCIA SAP2000 (v25, vía MCP) ======================
SAP = dict(
    periods=[0.526046, 0.156774, 0.023279, 0.020948],
    mass_ratio=[0.869489, 0.130511, 0.0, 0.0],
    V_cqc=40.142668,
    V_srss=40.129816,
    roof_cqc=0.02204216,
    roof_srss=0.02204301,
)

# ============================ COMPARACIÓN ============================
print("Caso 5 - Modal espectral 2D NCh2369 (Rukan vs SAP2000)")
print(f"  Masa sismica total = {res.total_mass:.2f} t   (10 t piso 1 + 8 t techo)\n")

print("  Modo   T Rukan [s]   T SAP [s]     err %    M*/M Rukan   M*/M SAP")
for i, m in enumerate(res.modes):
    err_T = abs(m.period - SAP["periods"][i]) / SAP["periods"][i] * 100.0
    print(f"    {m.index}     {m.period:9.6f}   {SAP['periods'][i]:9.6f}  {err_T:7.4f}   "
          f"{m.eff_mass_ratio*100:8.4f}%  {SAP['mass_ratio'][i]*100:8.4f}%")

print("\n  Sa/g por modo (espectro NCh2369):")
for m in res.modes:
    print(f"    modo {m.index}: T={m.period:.4f} s  ->  Sa/g={m.sa_over_g:.5f}  "
          f"->  V_modal={m.base_shear:8.4f} kN")

print("\n  Corte basal combinado           Rukan        SAP2000       err %")
for name, r, s in [("CQC", V_cqc, SAP["V_cqc"]), ("SRSS", V_srss, SAP["V_srss"])]:
    err = abs(r - s) / s * 100.0
    print(f"    V_{name:4s} [kN]                 {r:9.4f}    {s:9.4f}   {err:8.4f}")

print("\n  Despl. lateral de techo         Rukan        SAP2000       err %")
for name, r, s in [("CQC", roof_cqc, SAP["roof_cqc"]), ("SRSS", roof_srss, SAP["roof_srss"])]:
    err = abs(r - s) / s * 100.0
    print(f"    u_techo_{name:4s} [mm]           {r*1000:9.4f}    {s*1000:9.4f}   {err:8.4f}")

# ============================ TOLERANCIAS ============================
TOL_MODAL = 0.5   # % (períodos y masas: análisis modal, debe ser muy fino)
TOL_RSA = 1.0     # % (respuesta espectral combinada)

for i, m in enumerate(res.modes):
    err_T = abs(m.period - SAP["periods"][i]) / SAP["periods"][i] * 100.0
    assert err_T < TOL_MODAL, f"Modo {i+1}: error en periodo {err_T:.4f}%"
    err_m = abs(m.eff_mass_ratio - SAP["mass_ratio"][i]) * 100.0  # dif. en puntos %
    assert err_m < TOL_MODAL, f"Modo {i+1}: error en masa modal {err_m:.4f} pts%"

for name, r, s in [("V_cqc", V_cqc, SAP["V_cqc"]), ("V_srss", V_srss, SAP["V_srss"]),
                   ("roof_cqc", roof_cqc, SAP["roof_cqc"]), ("roof_srss", roof_srss, SAP["roof_srss"])]:
    err = abs(r - s) / s * 100.0
    assert err < TOL_RSA, f"{name}: error {err:.4f}% excede {TOL_RSA}%"

print(f"\n  OK - masa modal capturada = {sum(m.eff_mass_ratio for m in res.modes)*100:.2f}% del total")
