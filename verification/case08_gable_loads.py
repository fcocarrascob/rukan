"""Caso 8 — Peso propio, casos de carga y combinaciones (galpón a dos aguas).

Análisis indispensable: todo modelo real es **gravedad + otros casos**. Este caso
introduce el **peso propio**, los **casos de carga** y las **combinaciones**
(`src/rukan/loads.py`), sobre un galpón a dos aguas — el caso típico donde el
pórtico transversal **"se abre"** bajo la carga de techo.

Estructura: galpón a dos aguas de 3 marcos.
- **Transversal (X):** marco a momento — columnas + dos dinteles inclinados a la
  cumbrera. Bases articuladas → el pórtico se abre bajo gravedad.
- **Longitudinal (Y):** arriostrado — X-braces de muro partidas en el cruce y
  liberadas solo en el extremo de columna; diagonales de techo (diafragma).
- 6 m de luz transversal, alero 3 m, cumbrera 4 m; 3 marcos a 6 m (12 m de largo).
- Secciones tubulares (I22=I33). Acero, densidad de peso 76.98 kN/m³ (ρ=7.85 t/m³).

**Lo que se verifica aquí (peso propio):**
1. El peso propio **distribuido** (`self_weight_distributed`, con proyección de la
   gravedad a los ejes locales de cada barra) reproduce SAP2000: reacciones,
   **apertura del pórtico** (empuje + desplazamiento del alero) y descenso de la
   cumbrera, todo con error ~0%.
2. El contraste con el peso propio **concentrado en nudos** (`self_weight_nodal`):
   el peso total y las reacciones coinciden, pero el **momento del dintel bajo su
   propio peso se pierde** al concentrar — por eso, para esfuerzos estáticos, hay
   que distribuir; concentrar es correcto para la **masa** sísmica (casos 5, 7).

Los casos de carga adicionales (techo Lr, sismo espectral E) y las combinaciones
(1.2D+1.6Lr, 1.2D±E) se agregan sobre esta misma estructura (ver `loads.combine`).

Patrón de referencia: SAP2000 v25 vía MCP (`case8_gable.sdb`; scripts
`case8_gable_build` + `case8_gable_selfweight`). Peso propio con densidad de peso
del material (`SetWeightAndMass` opción 1); ¡ojo!: peso y masa están acoplados en
SAP (peso = masa·g), no se puede poner masa 0 con peso ≠ 0.
"""

from __future__ import annotations

import math

import openseespy.opensees as ops

from rukan.engine import build
from rukan.model import FrameElement, Material, Model, Node, Section
from rukan import loads
from rukan.modal import run_directional_spectral
from rukan.spectra import nch2369_spectrum

# =============================== DATOS ================================
E_ = 2.0e8
NU = 0.3
RHO = 7.8498  # t/m³  (ρ·g = 76.98 kN/m³, densidad de peso del acero en SAP)

SECS = [
    Section(1, A=9.6e-3, Iy=9.0e-5, Iz=9.0e-5, J=1.35e-4),  # COL
    Section(2, A=6.0e-3, Iy=3.6e-5, Iz=3.6e-5, J=5.5e-5),   # RAFT (dintel)
    Section(3, A=6.0e-3, Iy=3.6e-5, Iz=3.6e-5, J=5.5e-5),   # BEAM (cumbrera/aleros)
    Section(4, A=3.4e-3, Iy=1.1e-5, Iz=1.1e-5, J=1.7e-5),   # DIAG
]

PIN = (True, True, True, False, False, True)  # base articulada (giros de flexión libres)
FREE = (False,) * 6

# Nodos: 3 marcos (y=0,6,12) + centros de X-brace de muro (vano 1)
COORDS = {
    1: (0, 0, 0), 2: (6, 0, 0), 3: (0, 0, 3), 4: (6, 0, 3), 5: (3, 0, 4),
    6: (0, 6, 0), 7: (6, 6, 0), 8: (0, 6, 3), 9: (6, 6, 3), 10: (3, 6, 4),
    11: (0, 12, 0), 12: (6, 12, 0), 13: (0, 12, 3), 14: (6, 12, 3), 15: (3, 12, 4),
    22: (0, 3, 1.5), 23: (6, 3, 1.5),
}
BASES = (1, 2, 6, 7, 11, 12)


def make_gable_model() -> tuple[Model, dict]:
    """Devuelve el modelo del galpón y un dict con ids de elementos clave."""
    nodes = [Node(i, float(x), float(y), float(z), PIN if i in BASES else FREE)
             for i, (x, y, z) in COORDS.items()]
    els: list[FrameElement] = []
    ids: dict = {}
    eid = 1

    def push(a, b, sec, vecxz, **kw):
        nonlocal eid
        els.append(FrameElement(eid, a, b, 1, sec, vecxz, **kw))
        ids[(a, b)] = eid
        eid += 1

    for a, b in [(1, 3), (2, 4), (6, 8), (7, 9), (11, 13), (12, 14)]:
        push(a, b, 1, (1., 0., 0.))                       # columnas
    for a, b in [(3, 5), (4, 5), (8, 10), (9, 10), (13, 15), (14, 15)]:
        push(a, b, 2, (0., 1., 0.))                       # dinteles
    for a, b in [(5, 10), (10, 15), (3, 8), (8, 13), (4, 9), (9, 14)]:
        push(a, b, 3, (0., 0., 1.))                       # cumbrera + aleros long.
    for a, b in [(3, 10), (8, 15), (4, 10), (9, 15)]:      # diagonales de techo (biela)
        push(a, b, 4, (0., 0., 1.), release_z_i=True, release_z_j=True,
             release_y_i=True, release_y_j=True)
    # X-braces de muro partidas, liberadas solo en el extremo de columna
    for a, b, rn in [(1, 22, 1), (22, 8, 8), (6, 22, 6), (22, 3, 3),
                     (2, 23, 2), (23, 9, 9), (7, 23, 7), (23, 4, 4)]:
        ri, rj = (rn == a), (rn == b)
        push(a, b, 4, (1., 0., 0.), release_z_i=ri, release_y_i=ri,
             release_z_j=rj, release_y_j=rj)

    model = Model(nodes=nodes, materials=[Material(1, E=E_, nu=NU, rho=RHO)],
                  sections=SECS, elements=els, masses=[])
    return model, ids


model, ids = make_gable_model()
raft = ids[(3, 5)]  # dintel R3_5
# Masa sísmica = masa propia concentrada en nudos (como la arma SAP2000).
model_m = Model(model.nodes, model.materials, model.sections, model.elements,
                loads.self_mass_lumped(model))

BASE_NODES = BASES
EXTRACT = {
    "b1_Fx": lambda: ops.nodeReaction(1, 1),
    "b1_Fz": lambda: ops.nodeReaction(1, 3),
    "baseFx": lambda: sum(ops.nodeReaction(n, 1) for n in BASE_NODES),
    "baseFz": lambda: sum(ops.nodeReaction(n, 3) for n in BASE_NODES),
    "eave3_Ux": lambda: ops.nodeDisp(3, 1) * 1000.0,
    "eave8_Ux": lambda: ops.nodeDisp(8, 1) * 1000.0,
    "apex5_Uz": lambda: ops.nodeDisp(5, 3) * 1000.0,
    "raft_My": lambda: ops.eleResponse(raft, "localForces")[10],
}

# ==================== CHEQUEO DE SANIDAD MODAL =======================
# Siempre conviene revisar el modal para cazar inconsistencias de los modos.
build(model_m)
periods = [2.0 * math.pi / math.sqrt(w) for w in ops.eigen("-fullGenLapack", 12)]
SAP_T = [0.22356, 0.10075, 0.09931, 0.06295, 0.05501, 0.0489,
         0.03914, 0.02453, 0.02439, 0.01393, 0.01181, 0.00814]

# ============================= CASOS ================================
spectrum = nch2369_spectrum(zone=2, soil="C", importance=1.0, R=5.0, damping=0.03)
D = loads.run_static_case(model, lambda: loads.self_weight_distributed(model), EXTRACT)
N = loads.run_static_case(model, lambda: loads.self_weight_nodal(model), EXTRACT)
Lr = loads.run_static_case(
    model, lambda: [ops.load(n, 0, 0, -5.0, 0, 0, 0) for n in (3, 4, 5, 8, 9, 10, 13, 14, 15)], EXTRACT)
build(model_m)
EX = loads.spectral_case(run_directional_spectral(model_m, spectrum, "Ux", EXTRACT, 0.03, 12), EXTRACT)
build(model_m)
EY = loads.spectral_case(run_directional_spectral(model_m, spectrum, "Uy", EXTRACT, 0.03, 12), EXTRACT)

# ============ REFERENCIA SAP2000 (v25, vía MCP) ======================
SAP = {
    "D":  dict(baseFz=52.817, b1_Fx=0.756, b1_Fz=8.4926, eave3_Ux=-0.1815, eave8_Ux=-0.28547, apex5_Uz=-0.55732),
    "Lr": dict(baseFz=45.0, b1_Fx=1.0172, b1_Fz=7.4949, eave3_Ux=-0.27045),
    "EX": dict(b1_Fx=2.2998, b1_Fz=2.2268, baseFx=13.5723, eave3_Ux=3.91056),  # baseFx = corte basal transversal
    "EY": dict(b1_Fx=0.0944, b1_Fz=3.2682, eave3_Ux=0.02545),
}

# ============================ COMPARACIÓN ============================
print("Caso 8 - Peso propio, casos de carga y combinaciones (Rukan vs SAP2000)")
print(f"  Peso propio total = {loads.total_weight(model):.4f} kN;  "
      f"masa propia = {loads.total_weight(model)/loads.G:.4f} t\n")

print("  Chequeo de sanidad modal (periodos vs SAP2000):")
print("   modo:  1(X marco)   2        8(Y braceado)")
for i in (0, 1, 7):
    print(f"    T{i+1} = {periods[i]:.5f} s  (SAP {SAP_T[i]:.5f}, err "
          f"{abs(periods[i]-SAP_T[i])/SAP_T[i]*100:.3f}%)")

def show(name, ruk, sap, keys):
    print(f"\n  Caso {name}:")
    for k in keys:
        r, s = ruk[k], sap[k]
        err = abs(abs(r) - abs(s)) / abs(s) * 100.0 if abs(s) > 1e-9 else 0.0
        print(f"    {k:10s} Rukan {r:11.4f}  SAP {s:11.4f}  err {err:7.3f}%")

show("D (peso propio)", D, SAP["D"], ["baseFz", "b1_Fx", "b1_Fz", "eave3_Ux", "eave8_Ux", "apex5_Uz"])
show("Lr (techo)", Lr, SAP["Lr"], ["baseFz", "b1_Fx", "b1_Fz", "eave3_Ux"])
show("E_X (sismo transversal, CQC)", {k: abs(v) for k, v in EX.items()}, SAP["EX"], ["b1_Fx", "b1_Fz", "baseFx", "eave3_Ux"])
show("E_Y (sismo longitudinal, CQC)", {k: abs(v) for k, v in EY.items()}, SAP["EY"], ["b1_Fx", "b1_Fz", "eave3_Ux"])

# Peso propio: distribuido vs concentrado (el contraste didáctico)
print("\n  Peso propio DISTRIBUIDO vs CONCENTRADO en nudos:")
for k in ("baseFz", "eave8_Ux", "raft_My"):
    print(f"    {k:10s} distribuido {D[k]:10.4f}   concentrado {N[k]:10.4f}")
print("    -> el momento del dintel (raft_My) se PIERDE al concentrar en nudos")

# ========================= COMBINACIONES ============================
# Combinar casos como en SAP2000: r_combo = Σ factor·r_caso.
c_grav = loads.combine({"D": D, "Lr": Lr}, {"D": 1.2, "Lr": 1.6})
c_sis_p = loads.combine({"D": D, "E": EX}, {"D": 1.2, "E": 1.0})
c_sis_m = loads.combine({"D": D, "E": EX}, {"D": 1.2, "E": -1.0})
print("\n  Combinaciones (axial columna esquina b1_Fz, apertura eave3_Ux):")
print(f"    1.2D+1.6Lr : b1_Fz {c_grav['b1_Fz']:9.4f}   eave3_Ux {c_grav['eave3_Ux']:8.4f}")
print(f"    1.2D + E_X : b1_Fz {c_sis_p['b1_Fz']:9.4f}   eave3_Ux {c_sis_p['eave3_Ux']:8.4f}")
print(f"    1.2D - E_X : b1_Fz {c_sis_m['b1_Fz']:9.4f}   eave3_Ux {c_sis_m['eave3_Ux']:8.4f}")

# ============================ TOLERANCIAS ============================
TOL = 0.5   # % (estático) — RSA algo más holgado por combinación modal
# Modal (sanidad)
for i in (0, 1, 7):
    assert abs(periods[i] - SAP_T[i]) / SAP_T[i] * 100 < 0.5, f"periodo modo {i+1}"
# Casos estáticos
for name, ruk in (("D", D), ("Lr", Lr)):
    for k, s in SAP[name].items():
        assert abs(abs(ruk[k]) - abs(s)) / abs(s) * 100 < TOL, f"{name}.{k}"
# Casos espectrales (cantidades sin ambigüedad de signo/suma)
for k, s in SAP["EX"].items():
    assert abs(abs(EX[k]) - abs(s)) / abs(s) * 100 < 1.0, f"EX.{k}"
for k in ("b1_Fx", "b1_Fz", "eave3_Ux"):
    assert abs(abs(EY[k]) - abs(SAP["EY"][k])) / abs(SAP["EY"][k]) * 100 < 1.0, f"EY.{k}"
# Peso propio: total conservado, momento del dintel perdido al concentrar
assert abs(abs(N["baseFz"]) - SAP["D"]["baseFz"]) / SAP["D"]["baseFz"] * 100 < TOL
assert abs(N["raft_My"]) < 0.25 * abs(D["raft_My"]), "concentrar deberia perder el momento del dintel"
# Linealidad de la combinacion
assert abs(c_grav["b1_Fz"] - (1.2 * D["b1_Fz"] + 1.6 * Lr["b1_Fz"])) < 1e-9

print("\n  OK - 4 casos (D, Lr, E_X, E_Y) reproducen SAP2000; combinaciones lineales;")
print("       peso propio distribuido correcto, concentrado pierde flexion; modal sano.")
