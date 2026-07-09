"""Caso 7 — Galpón 3D completo (NCh2369), Rukan vs SAP2000.

El caso que reúne toda la escalera del MVP en tres dimensiones de verdad:

- **Modelo 3D real** (no plano) armado con ``engine.build``: nudos de techo
  libres en los 6 GDL.
- **Arriostramientos liberados en 3D** (caso 6): 8 diagonales en cruz, cada una
  con M2 y M3 liberados en ambos extremos → bielas axiales en el espacio.
- **Modal espectral NCh2369 en dos direcciones** (caso 5), con la respuesta
  espectral general de ``rukan.modal`` (fuerzas estáticas equivalentes modo a
  modo → cualquier reacción o fuerza de barra, combinada por CQC).
- **Combinación direccional 100/30**: la columna de esquina recibe carga axial
  de los dos sismos ortogonales; el diseño combina 100 % de una dirección con
  30 % de la otra.

Sistema: galpón rectangular de un piso, 10 m (X) × 6 m (Y) × 5 m de alto,
columnas y vigas de sección tubular (I22 = I33, isótropas a flexión → sin
ambigüedad de eje local en 3D), arriostramiento en cruz en los cuatro muros con
las diagonales liberadas. Masa sísmica de 6 t por esquina de techo (24 t total),
horizontal (X, Y). Espectro NCh2369 zona 2, suelo C, R = 5, ξ = 3 %.

Patrón de referencia: SAP2000 v25 vía MCP (``case7_galpon3d.sdb``; scripts
``case7_galpon3d_build`` y ``case7_galpon3d_rs``). Área de corte nula en SAP →
Euler-Bernoulli, igual que OpenSees.

Nota: el sismo vertical NCh2369 es despreciable en esta caja arriostrada rígida
(la masa está sobre columnas axialmente rígidas) y se trata aparte; aquí se
verifican las dos direcciones horizontales y su combinación 100/30.
"""

from __future__ import annotations

import openseespy.opensees as ops

from rukan import units as u
from rukan.engine import build
from rukan.model import FrameElement, Material, Model, NodalMass, Node, Section
from rukan.modal import directional_combination, run_directional_spectral
from rukan.spectra import nch2369_spectrum

# =============================== DATOS ================================
E_ = u.stress(200 * u.ureg.GPa)
NU = 0.3
G_ = E_ / (2.0 * (1.0 + NU))

# Secciones tubulares (I22 = I33), idénticas a SAP.
COL = Section(1, A=9.6e-3, Iy=9.0e-5, Iz=9.0e-5, J=1.35e-4)
VIGA = Section(2, A=6.0e-3, Iy=3.6e-5, Iz=3.6e-5, J=5.5e-5)
DIAG = Section(3, A=3.4e-3, Iy=1.1e-5, Iz=1.1e-5, J=1.7e-5)

FIXED = (True,) * 6
FREE = (False,) * 6

coords = {1: (0, 0, 0), 2: (10, 0, 0), 3: (10, 6, 0), 4: (0, 6, 0),
          5: (0, 0, 5), 6: (10, 0, 5), 7: (10, 6, 5), 8: (0, 6, 5)}
# Nodos de intersección de las X-braces (uno por muro), sin masa.
centers = {9: (5, 0, 2.5), 10: (5, 6, 2.5), 11: (0, 3, 2.5), 12: (10, 3, 2.5)}
nodes = [Node(i, float(x), float(y), float(z), FIXED if i <= 4 else FREE)
         for i, (x, y, z) in coords.items()]
nodes += [Node(c, float(x), float(y), float(z), FREE) for c, (x, y, z) in centers.items()]

# Columnas (verticales), vigas de techo (tubo → vecxz cualquiera válido).
elements = [
    FrameElement(1, 1, 5, 1, 1, (1., 0., 0.)),
    FrameElement(2, 2, 6, 1, 1, (1., 0., 0.)),
    FrameElement(3, 3, 7, 1, 1, (1., 0., 0.)),
    FrameElement(4, 4, 8, 1, 1, (1., 0., 0.)),
    FrameElement(10, 5, 6, 1, 2, (0., 0., 1.)),
    FrameElement(11, 6, 7, 1, 2, (0., 0., 1.)),
    FrameElement(12, 7, 8, 1, 2, (0., 0., 1.)),
    FrameElement(13, 8, 5, 1, 2, (0., 0., 1.)),
]

# X-braces PARTIDAS en el nodo de intersección: cada diagonal se corta en el
# cruce y se libera (M2 y M3) SOLO en el extremo que conecta a la columna; el
# nodo de intersección queda continuo (los dos diagonales se conectan ahí, como
# en la realidad). Muros X-Z (centros 9,10): vecxz=(0,1,0); Y-Z (11,12): (1,0,0).
walls = {9: ((0., 1., 0.), [(1, 6), (2, 5)]), 10: ((0., 1., 0.), [(4, 7), (3, 8)]),
         11: ((1., 0., 0.), [(1, 8), (4, 5)]), 12: ((1., 0., 0.), [(2, 7), (3, 6)])}
brace_id = {}
eid = 20
for cid, (vz, diags) in walls.items():
    for a, b in diags:
        # a -> centro: liberar en el extremo i (nudo a = columna)
        elements.append(FrameElement(eid, a, cid, 1, 3, vz, release_z_i=True, release_y_i=True))
        brace_id[(a, cid)] = eid; eid += 1
        # centro -> b: liberar en el extremo j (nudo b = columna)
        elements.append(FrameElement(eid, cid, b, 1, 3, vz, release_z_j=True, release_y_j=True))
        brace_id[(cid, b)] = eid; eid += 1

masses = [NodalMass(i, (6.0, 6.0, 0.0, 0.0, 0.0, 0.0)) for i in (5, 6, 7, 8)]

model = Model(nodes=nodes, materials=[Material(1, E=E_, nu=NU, rho=0.0)],
              sections=[COL, VIGA, DIAG], elements=elements, masses=masses)

# ======================== ANÁLISIS ESPECTRAL =========================
spectrum = nch2369_spectrum(zone=2, soil="C", importance=1.0, R=5.0, damping=0.03)

D19 = brace_id[(1, 9)]  # media-diagonal nudo 1 -> intersección (= D1_9 en SAP)
extractors = {
    "baseFx": lambda: sum(ops.nodeReaction(n, 1) for n in (1, 2, 3, 4)),
    "baseFy": lambda: sum(ops.nodeReaction(n, 2) for n in (1, 2, 3, 4)),
    "r1_Fx": lambda: ops.nodeReaction(1, 1),
    "r1_Fy": lambda: ops.nodeReaction(1, 2),
    "r1_Fz": lambda: ops.nodeReaction(1, 3),
    "diagN": lambda: -ops.eleResponse(D19, "localForces")[0],  # tracción +
    "u5x": lambda: ops.nodeDisp(5, 1) * 1000.0,
    "u5y": lambda: ops.nodeDisp(5, 2) * 1000.0,
}

build(model)
rx = run_directional_spectral(model, spectrum, "Ux", extractors, damping=0.03, n_modes=6)
build(model)  # re-montar para eigen limpio en la otra dirección
ry = run_directional_spectral(model, spectrum, "Uy", extractors, damping=0.03, n_modes=6)


def C(res, name):  # CQC combinado, magnitud
    return abs(res.combined(name, "CQC"))


# ============ REFERENCIA SAP2000 (v25, vía MCP) ======================
SAP = dict(
    baseX=70.8878, baseY=70.8830,
    r1X=(17.7219, 0.7933, 17.5241),   # Fx, Fy, Fz bajo RS_X
    r1Y=(0.7275, 17.7207, 29.1852),   # Fx, Fy, Fz bajo RS_Y
    diagN_X=19.5137, diagN_Y=0.8107,
    u5x_X=0.3693, u5y_Y=0.37001,
)

# ============================ COMPARACIÓN ============================
print("Caso 7 - Galpón 3D completo NCh2369 (Rukan vs SAP2000)")
print(f"  Periodos (X-brace, 4 modos acoplados ~0.07 s): "
      f"{[round(t,5) for t in rx.periods[:4]]}\n")


def row(label, r, s):
    err = abs(r - s) / abs(s) * 100.0 if s else abs(r)
    print(f"    {label:26s} Rukan {r:10.4f}   SAP {s:10.4f}   err {err:7.4f}%")


print("  Sismo X (CQC):")
row("corte basal Fx [kN]", C(rx, "baseFx"), SAP["baseX"])
row("reaccion esq. Fx [kN]", C(rx, "r1_Fx"), SAP["r1X"][0])
row("reaccion esq. Fz [kN]", C(rx, "r1_Fz"), SAP["r1X"][2])
row("axial diagonal [kN]", C(rx, "diagN"), SAP["diagN_X"])
row("despl. techo u5x [mm]", C(rx, "u5x"), SAP["u5x_X"])

print("  Sismo Y (CQC):")
row("corte basal Fy [kN]", C(ry, "baseFy"), SAP["baseY"])
row("reaccion esq. Fy [kN]", C(ry, "r1_Fy"), SAP["r1Y"][1])
row("reaccion esq. Fz [kN]", C(ry, "r1_Fz"), SAP["r1Y"][2])
row("despl. techo u5y [mm]", C(ry, "u5y"), SAP["u5y_Y"])

# --- Combinación direccional 100/30 sobre la axial de la columna de esquina ---
Fz_X_ruk, Fz_Y_ruk = C(rx, "r1_Fz"), C(ry, "r1_Fz")
Fz_X_sap, Fz_Y_sap = SAP["r1X"][2], SAP["r1Y"][2]
d100_30_ruk = directional_combination(Fz_X_ruk, Fz_Y_ruk, 0.3)
d100_30_sap = directional_combination(Fz_X_sap, Fz_Y_sap, 0.3)
srss_dir = (Fz_X_ruk**2 + Fz_Y_ruk**2) ** 0.5

print("\n  Axial de columna de esquina (nudo 1), combinacion direccional:")
print(f"    Fz(X) = {Fz_X_ruk:.4f} kN   Fz(Y) = {Fz_Y_ruk:.4f} kN")
print(f"    SRSS direccional          = {srss_dir:8.4f} kN")
print(f"    100/30  Rukan {d100_30_ruk:8.4f}   SAP {d100_30_sap:8.4f}   "
      f"err {abs(d100_30_ruk-d100_30_sap)/d100_30_sap*100:.4f}%")

# ============================ TOLERANCIAS ============================
TOL = 0.5  # % (RSA 3D vs SAP)
checks = [
    (C(rx, "baseFx"), SAP["baseX"]), (C(ry, "baseFy"), SAP["baseY"]),
    (C(rx, "r1_Fx"), SAP["r1X"][0]), (C(rx, "r1_Fz"), SAP["r1X"][2]),
    (C(ry, "r1_Fy"), SAP["r1Y"][1]), (C(ry, "r1_Fz"), SAP["r1Y"][2]),
    (C(rx, "diagN"), SAP["diagN_X"]),
    (C(rx, "u5x"), SAP["u5x_X"]), (C(ry, "u5y"), SAP["u5y_Y"]),
    (d100_30_ruk, d100_30_sap),
]
for r, s in checks:
    err = abs(r - s) / abs(s) * 100.0
    assert err < TOL, f"error {err:.4f}% excede {TOL}% (Rukan {r:.4f} vs SAP {s:.4f})"

print("\n  OK - galpon 3D: dos direcciones + 100/30 reproducen SAP2000 < 0.5%")
