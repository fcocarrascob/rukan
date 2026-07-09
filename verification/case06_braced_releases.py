"""Caso 6 — Arriostramiento y liberación de momentos, Rukan vs SAP2000.

Verifica la técnica de modelación que sostiene todo el diseño de arriostramientos
industriales: **liberar los momentos flectores en los extremos de la diagonal**.
Una diagonal de arriostramiento se conecta con un gusset apernado o una rótula:
transmite fuerza axial (y algo de corte), pero **no** momento. Modelarla
rígidamente conectada mete en la conexión un momento espurio que en la realidad
no existe. La forma correcta es liberar ese momento — convertir la barra en una
biela axial en su plano.

Sistema: pórtico de un vano (6 m) y un piso (4 m), plano X-Z, empotrado en la
base, con una diagonal del nudo base-izquierdo (1) al techo-derecho (4). Carga
lateral total de 100 kN en el techo (50 kN por nudo, +X). Se comparan tres
modelos contra SAP2000:

1.  **Diagonal rígida** (sin liberar): atrae un pequeño momento a sus extremos.
2.  **Diagonal liberada** (M2 y M3 liberados en ambos extremos, la práctica 3D
    habitual en SAP2000): momento nulo, axial puro — el modelo honesto de la
    conexión a corte/axial.
3.  **Diagonal como Truss** (biela pura de OpenSees): debe coincidir *exactamente*
    con la diagonal liberada, confirmando que liberar los dos extremos equivale a
    la idealización de reticulado.

Patrón de referencia: SAP2000 v25 vía MCP (modelo ``case6_braced_bay.sdb``,
`FrameObj.SetReleases` con M3 liberado en ambos extremos). Secciones con área de
corte nula en SAP → Euler-Bernoulli, igual que el `elasticBeamColumn` de OpenSees.

Enseñanza clave: liberar los momentos casi no cambia la respuesta global (la
diagonal trabaja en axial de todas formas), pero **anula el momento en la
conexión**, que es justo la fuerza para la que un gusset no está diseñado.
"""

from __future__ import annotations

import openseespy.opensees as ops

from rukan import units as u
from rukan.engine import build
from rukan.model import FrameElement, Material, Model, Node, Section

# =============================== DATOS ================================
E = 200 * u.ureg.GPa
NU = 0.3
L = 6.0 * u.ureg.m
H = 4.0 * u.ureg.m
P_LAT = 50.0 * u.ureg.kN   # por nudo del techo (2 → 100 kN totales)

# HEB240 (columnas y viga); tubo robusto 250x250 (diagonal).
COL = dict(A=0.0106, Iz=1.126e-4, Iy=3.92e-5, J=1.03e-6)
DIAG = dict(A=1.11e-2, Iz=1.04e-4, Iy=1.04e-4, J=1.5e-4)

E_ = u.stress(E)
G_ = E_ / (2.0 * (1.0 + NU))
L_ = u.length(L)
H_ = u.length(H)
P_ = u.force(P_LAT)

FREE_PLANE = (False, True, False, True, False, True)
FIXED = (True, True, True, True, True, True)
VECXZ = (0.0, 1.0, 0.0)  # eje local z = Y global → Iz e Iz-release = en el plano


def make_model(diagonal: str) -> Model:
    """``diagonal`` ∈ {'rigid', 'released', 'none'}."""
    nodes = [
        Node(1, 0.0, 0.0, 0.0, FIXED), Node(2, L_, 0.0, 0.0, FIXED),
        Node(3, 0.0, 0.0, H_, FREE_PLANE), Node(4, L_, 0.0, H_, FREE_PLANE),
    ]
    materials = [Material(1, E=E_, nu=NU, rho=0.0)]
    sections = [
        Section(1, A=COL["A"], Iy=COL["Iy"], Iz=COL["Iz"], J=COL["J"]),
        Section(2, A=DIAG["A"], Iy=DIAG["Iy"], Iz=DIAG["Iz"], J=DIAG["J"]),
    ]
    elements = [
        FrameElement(1, 1, 3, 1, 1, VECXZ),  # columna izq
        FrameElement(2, 2, 4, 1, 1, VECXZ),  # columna der
        FrameElement(3, 3, 4, 1, 1, VECXZ),  # viga
    ]
    if diagonal in ("rigid", "released"):
        rel = diagonal == "released"
        # En 3D una biela se libera en AMBOS planos de flexión (M2 y M3 en la
        # convención SAP), no solo en el plano del pórtico: así no transmite
        # momento en ninguna dirección. Aquí M2 (fuera de plano) es inerte por
        # las restricciones, pero se libera igual para reflejar la práctica real.
        elements.append(
            FrameElement(10, 1, 4, 1, 2, VECXZ,
                         release_z_i=rel, release_z_j=rel,
                         release_y_i=rel, release_y_j=rel)
        )
    return Model(nodes=nodes, materials=materials, sections=sections,
                 elements=elements, masses=[])


def solve(diagonal: str, truss: bool = False) -> dict:
    """Arma, aplica la carga lateral, resuelve estático y extrae resultados."""
    model = make_model("none" if truss else diagonal)
    build(model)

    if truss:  # diagonal como biela pura de OpenSees (axial, sin momento)
        ops.uniaxialMaterial("Elastic", 99, E_)
        ops.element("Truss", 10, 1, 4, DIAG["A"], 99)

    ops.timeSeries("Linear", 1)
    ops.pattern("Plain", 1, 1)
    ops.load(3, P_, 0.0, 0.0, 0.0, 0.0, 0.0)
    ops.load(4, P_, 0.0, 0.0, 0.0, 0.0, 0.0)

    ops.system("BandGeneral"); ops.numberer("RCM"); ops.constraints("Transformation")
    ops.integrator("LoadControl", 1.0); ops.algorithm("Linear"); ops.analysis("Static")
    ops.analyze(1)

    out = dict(u3=ops.nodeDisp(3, 1) * 1000, u4=ops.nodeDisp(4, 1) * 1000)
    has_diag = truss or diagonal in ("rigid", "released")
    if has_diag:
        if truss:
            out["diag_N"] = ops.eleResponse(10, "axialForce")[0]
            out["diag_M3"] = (0.0, 0.0)
        else:
            f = ops.eleResponse(10, "localForces")  # [Ni,Vy,Vz,T,My,Mz, Nj,...]
            out["diag_N"] = -f[0]   # signo: tracción positiva (OpenSees Ni<0 en tracción)
            # Diagrama de momento interno (convención SAP) = (Mz_i, -Mz_j):
            # OpenSees da momentos nodales de extremo; el extremo j invierte signo.
            out["diag_M3"] = (f[5], -f[11])
    ops.reactions()
    out["base1"] = (ops.nodeReaction(1, 1), ops.nodeReaction(1, 5))  # F1(Fx), M2(My)
    out["base2"] = (ops.nodeReaction(2, 1), ops.nodeReaction(2, 5))
    return out


# ============ REFERENCIA SAP2000 (v25, vía MCP) ======================
SAP_RIGID = dict(u3=0.67389, u4=0.53699, diag_N=116.4948, diag_M3=(-0.3872, -0.1867),
                 base1=(-98.5727, -4.4545), base2=(-1.4273, -3.4147))
SAP_RELEASED = dict(u3=0.67419, u4=0.53731, diag_N=116.5537, diag_M3=(0.0, 0.0),
                    base1=(-98.6157, -4.0807), base2=(-1.3843, -3.3582))

rig = solve("rigid")
rel = solve("released")
trs = solve("released", truss=True)
bare = solve("none")

# ============================ COMPARACIÓN ============================
print("Caso 6 - Arriostramiento y liberación de momentos (Rukan vs SAP2000)")
print(f"  Carga lateral total = 100 kN en el techo\n")

print(f"  Deriva de techo (bare frame, sin diagonal): u3 = {bare['u3']:.4f} mm")
print(f"  -> con la diagonal cae a ~{rel['u3']:.4f} mm: el arriostramiento se lleva el corte en AXIAL\n")


def cmp_block(title, r, sap):
    print(f"  {title}")
    print(f"    u_techo [mm]        Rukan {r['u3']:9.5f}   SAP {sap['u3']:9.5f}   "
          f"err {abs(r['u3']-sap['u3'])/sap['u3']*100:7.4f}%")
    print(f"    N diagonal [kN]     Rukan {r['diag_N']:9.4f}   SAP {sap['diag_N']:9.4f}   "
          f"err {abs(r['diag_N']-sap['diag_N'])/sap['diag_N']*100:7.4f}%")
    print(f"    M3 diag i,j [kNm]   Rukan ({r['diag_M3'][0]:+.4f},{r['diag_M3'][1]:+.4f})   "
          f"SAP ({sap['diag_M3'][0]:+.4f},{sap['diag_M3'][1]:+.4f})")
    print(f"    M base col.1 [kNm]  Rukan {r['base1'][1]:9.4f}   SAP {sap['base1'][1]:9.4f}")
    print()


cmp_block("Diagonal RÍGIDA:", rig, SAP_RIGID)
cmp_block("Diagonal LIBERADA:", rel, SAP_RELEASED)

print("  Equivalencia liberada == Truss (biela pura de OpenSees):")
print(f"    u_techo:  liberada {rel['u3']:.6f} mm   truss {trs['u3']:.6f} mm")
print(f"    N diag:   liberada {rel['diag_N']:.5f} kN   truss {trs['diag_N']:.5f} kN")

# ============================ TOLERANCIAS ============================
TOL = 0.1  # % (estático lineal vs SAP)


def check(r, sap, tag):
    for key in ("u3", "u4", "diag_N"):
        err = abs(r[key] - sap[key]) / abs(sap[key]) * 100.0
        assert err < TOL, f"{tag}: error en {key} = {err:.4f}%"
    for a, b in zip(r["diag_M3"], sap["diag_M3"]):
        assert abs(a - b) < 0.01, f"{tag}: M3 diagonal {a:.4f} != {b:.4f}"


check(rig, SAP_RIGID, "rigida")
check(rel, SAP_RELEASED, "liberada")

# Liberada ≡ Truss (misma respuesta a nivel numérico)
assert abs(rel["u3"] - trs["u3"]) / abs(trs["u3"]) * 100 < 0.01, "liberada != truss (u)"
assert abs(rel["diag_N"] - trs["diag_N"]) / abs(trs["diag_N"]) * 100 < 0.01, "liberada != truss (N)"

# La diagonal liberada NO transmite momento
assert abs(rel["diag_M3"][0]) < 1e-6 and abs(rel["diag_M3"][1]) < 1e-6, "M3 liberado no es cero"

print("\n  OK - liberar los extremos anula el momento en la conexión (M3=0) y")
print("       reproduce SAP2000 y el elemento Truss dentro de tolerancia.")
