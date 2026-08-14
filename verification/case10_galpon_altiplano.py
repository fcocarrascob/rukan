"""Caso 10 — El galpón del altiplano: el modelo completo contra SAP2000.

El peldaño más grande de la escalera, y el primero que se construye **sin el
programa delante**: SAP2000 no está instalado en este equipo. Eso se puede hacer
porque el modelo de referencia quedó congelado en dos fuentes que se leen sin él —
`Skills_SAP/scripts/galpon_altiplano_*.py`, cuyas cabeceras `# Result:` guardan la
salida verificada de cada paso, y `struct_pad/SERIE-GALPON.md`, la memoria de
cálculo de la serie. Los dos motores comparten **solo los datos**
(`case10_data.py`); el ensamble, los autovalores y la combinación modal los hace
cada uno por su cuenta.

Precisión sobre qué significa «compartir los datos»: la geometría, las secciones y
el cálculo de presiones de viento están **portados literalmente** del script de
SAP, no re-derivados. Es deliberado. Si este archivo volviera a leer la Figura 12
de NCh432 por su cuenta, una discrepancia quedaría ambigua —¿falló el análisis o
la lectura de la norma?— y esa es justo la distinción que el contraste existe para
hacer. La fidelidad del port se comprueba por sus resultantes: las cinco de viento
coinciden con las de SAP a 5e-7 kN.

Estructura: galpón industrial a dos aguas de 24 × 24 m para faena minera de
altiplano (Pica, Tarapacá, ~3 800 m). 5 marcos a 6,0 m, luz 24,0 m, pendiente 10°,
alero 8,0 m, bases articuladas.

- **Transversal (X)**: marcos a momento de **peralte variable**, columna y dintel
  soldados por planchas, discretizados en 4 y 6 tramos prismáticos.
- **Longitudinal (Y)**: crucería en los vanos extremos más arriostramiento
  continuo de techo (puntales en las 7 líneas × 4 vanos, diagonales en anillo).
- 105 nodos, 188 barras, 20 bases. 11 estados de carga.

Capa A — estática (este archivo, primera parte)
-----------------------------------------------
1. El **conteo y el peso de acero**: 188 barras y 23 826,406894506 kg. Ese último
   número es el assert más barato y el más completo que hay, porque para salir
   bien tienen que estar bien a la vez todas las coordenadas, toda la conectividad
   y todas las áreas.
2. El **equilibrio de los 11 estados**: la reacción de base contra la resultante
   analítica Σg·L. SAP da residuo 0,0 en los 11; acá tiene que dar lo mismo.
3. Las **resultantes de viento** contra `galpon_altiplano_cargas_viento`.

Cuidado con dos cosas al leer los asserts
-----------------------------------------
- `galpon_altiplano_modal` está **superado**: corría 30 modos y reporta el modo Y
  en el puesto 8 con T = 0,268 s. El verdadero es el **41** con 0,1610609 s. La
  cabecera autoritativa del modal es la de `galpon_altiplano_build`.
- La cabecera `# Result:` de `galpon_altiplano_espectral` quedó estampada por una
  corrida de sondeo sobre un modelo de prueba de 3 nodos. Solo su bloque
  `T_estrella` / `R_estrella` corresponde al galpón.
"""

from __future__ import annotations

import math
import os
import sys

import openseespy.opensees as ops

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import case10_data as D  # noqa: E402
from rukan import loads  # noqa: E402
from rukan.engine import build  # noqa: E402
from rukan.loads import local_axes  # noqa: E402
from rukan.modal import run_directional_spectral  # noqa: E402
from rukan.spectra import nch2369_spectrum, r_star_for  # noqa: E402

TOL = 5e-4  # 0,05 % — la tolerancia de la escalera


# ===================== ENSAMBLE Y APLICACIÓN DE CARGA =====================
def assemble(model, meta) -> None:
    """`build` más las ataduras que `engine.py` todavía no sabe hacer.

    El pilar de hastial lleva **P, M2 y M3 liberados arriba**: no cuelga del dintel
    ni lo apuntala. `FrameElement` tiene liberación de momento pero no axial, así
    que el tope del pilar es un nodo propio, atado al de techo solo en el plano
    horizontal y en el giro vertical (`PILAR_TIE`), y libre en Z — que es
    exactamente lo que significa liberar la P.

    Sus giros Rx y Ry se fijan porque quedan sin rigidez: el elemento ya liberó los
    dos momentos en ese extremo, y un GDL sin rigidez es una matriz singular. No es
    una restricción con contenido físico — la reacción en esos GDL sale 0,0, y el
    caso lo verifica.
    """
    build(model)
    for r_node, p_node in meta.pilar_tie:
        ops.fix(p_node, 0, 0, 0, 1, 1, 0)
        ops.equalDOF(r_node, p_node, *D.PILAR_TIE)


def apply_uniform(model, meta, items) -> None:
    """Aplica cargas uniformes dadas por su vector **global** por unidad de largo.

    `eleLoad -beamUniform` de OpenSees es en ejes locales, así que cada vector se
    proyecta con la misma convención de `loads.local_axes`. Trabajar en globales y
    proyectar acá —en vez de portar los códigos de dirección de SAP— es lo que hace
    que la resultante analítica Σg·L sea comparable con la reacción de base.
    """
    nodes = {n.id: n for n in model.nodes}
    els = {e.id: e for e in model.elements}
    for nm, g in items:
        e = els[meta.elem_id[nm]]
        ni, nj = nodes[e.node_i], nodes[e.node_j]
        ex, ey, ez = local_axes((ni.x, ni.y, ni.z), (nj.x, nj.y, nj.z), e.vecxz)
        wx = g[0] * ex[0] + g[1] * ex[1] + g[2] * ex[2]
        wy = g[0] * ey[0] + g[1] * ey[1] + g[2] * ey[2]
        wz = g[0] * ez[0] + g[1] * ez[1] + g[2] * ez[2]
        ops.eleLoad("-ele", e.id, "-type", "-beamUniform", wy, wz, wx)


def main() -> None:
    print("Caso 10 - Galpon del altiplano (Rukan vs SAP2000, modelo congelado)")

    model, meta = D.build_model()
    base_ids = [meta.nid(n) for n in meta.bases]
    secs = {s.id: s for s in model.sections}
    els = {e.id: e for e in model.elements}

    # ---------------- 1. Conteo y peso de acero ----------------
    vol = sum(secs[els[meta.eid(nm)].section].A * L for nm, L in meta.elem_len.items())
    acero = vol * 7850.0
    ACERO_SAP = 23826.406894506235
    print("\n  Conteo y peso (contra galpon_altiplano_build):")
    print(f"    barras                {len(model.elements):>18d}   SAP {188:>18d}")
    print(f"    bases articuladas     {len(meta.bases):>18d}   SAP {20:>18d}")
    print(f"    tramos tapered        {len(meta.tapered):>18d}   SAP {70:>18d}")
    print(f"    acero [kg]            {acero:>18.6f}   SAP {ACERO_SAP:>18.6f}"
          f"   err {abs(acero / ACERO_SAP - 1):.2e}")
    assert len(model.elements) == 188 and len(meta.bases) == 20
    assert len(meta.tapered) == 70
    assert abs(acero / ACERO_SAP - 1) < 1e-12

    # ---------------- 2. Equilibrio de los 11 estados ----------------
    pats = D.load_patterns(meta)
    res = D.resultants(meta, pats)
    # DEAD lo pone rukan desde ρ·A·L; su resultante analítica es el peso de acero.
    res["DEAD"] = (0.0, 0.0, -vol * D.GAMMA_STEEL)

    def base_react():
        return tuple(sum(ops.nodeReaction(n, k) for n in base_ids) for k in (1, 2, 3))

    def pilar_react():
        """Los GDL que se fijaron en el tope del pilar no deben tomar nada.

        Solo se miran Rx y Ry (4 y 5), que son los fijados. En los GDL **atados**
        por `equalDOF`, `nodeReaction` no devuelve una reacción externa sino la
        fuerza de la atadura —la que el pilar le entrega al techo, y que bajo
        `WLYP` vale −4,03 kN de corte—, así que mirarlos ahí sería leer mal la
        salida, no encontrar un error.
        """
        return max(abs(ops.nodeReaction(p, k)) for _, p in meta.pilar_tie for k in (4, 5))

    print("\n  Equilibrio de los 11 estados (reaccion de base + resultante = 0):")
    print(f"    {'estado':7s} {'Fx [kN]':>13s} {'Fy [kN]':>13s} {'Fz [kN]':>13s} {'residuo':>11s}")
    peor = 0.0
    for pat in ["DEAD"] + D.PATTERNS:
        assemble(model, meta)
        if pat == "DEAD":
            apply = lambda: loads.self_weight_distributed(model)  # noqa: E731
        else:
            apply = lambda p=pat: apply_uniform(model, meta, pats[p])  # noqa: E731
        r = loads.run_static_case(model, apply, {"R": base_react, "P": pilar_react},
                                  rebuild=False)
        R, resid_p = r["R"], r["P"]
        e = res[pat]
        resid = max(abs(R[k] + e[k]) for k in range(3))
        peor = max(peor, resid, resid_p)
        print(f"    {pat:7s} {-R[0]:13.6f} {-R[1]:13.6f} {-R[2]:13.6f} {resid:11.2e}")
    print(f"    residuo maximo de los 11 (y de los topes de pilar): {peor:.3e} kN"
          "   SAP: 0.0")
    assert peor < 1e-6, f"equilibrio: residuo {peor}"

    # ---------------- 3. Resultantes de viento ----------------
    VIENTO_SAP = {
        "WTXP": (81.939439, 0.0, 192.082392),
        "WTXN": (-81.939439, 0.0, 192.082392),
        "WLYP": (-10.205652, 86.625229, 185.722047),
        "WLYN": (10.205652, -86.625229, 185.722047),
        "WPI": (0.0, 0.0, 57.243097),
    }
    print("\n  Resultantes de viento (contra galpon_altiplano_cargas_viento):")
    print(f"    {'estado':6s} {'Fx rukan':>12s} {'Fx SAP':>12s} {'Fy rukan':>12s} "
          f"{'Fy SAP':>12s} {'Fz rukan':>12s} {'Fz SAP':>12s}")
    for pat, s in VIENTO_SAP.items():
        r = res[pat]
        print(f"    {pat:6s} {r[0]:12.6f} {s[0]:12.6f} {r[1]:12.6f} {s[1]:12.6f} "
              f"{r[2]:12.6f} {s[2]:12.6f}")
        assert max(abs(r[k] - s[k]) for k in range(3)) < 1e-5
    print(f"    q_h = {D.QH:.10f} kPa   K_d·q_h = {D.QK:.10f} kPa   a = {D.A_ZONA:.4f} m")

    print("\n  OK capa A - conteo, peso de acero y los 11 estados en equilibrio.")

    # =========================== CAPA B - MODAL ===========================
    # Primera capa que pone a prueba la RIGIDEZ, no solo las cargas. Y antes de
    # eso, el contraste estatico que la aisla de la masa: en un marco
    # hiperestatico el reparto de momentos depende solo de la rigidez relativa.
    print("\n  Momento de alero bajo G3A_B = 1,2(D+DSD) + 1,6·S_bal (marco 3, lado A):")
    print("  -- es un contraste de RIGIDEZ PURA: no interviene ninguna masa --")
    estatico = {}
    EXM = {
        "COL3A_4_M3": lambda: ops.eleResponse(meta.eid("COL3A_4"), "localForces")[11],
        "COL3A_1_M3": lambda: ops.eleResponse(meta.eid("COL3A_1"), "localForces")[11],
        "DIN3_1_M3": lambda: ops.eleResponse(meta.eid("DIN3_1"), "localForces")[5],
        "COL3A_4_P": lambda: -ops.eleResponse(meta.eid("COL3A_4"), "localForces")[0],
        "COL3A_1_P": lambda: -ops.eleResponse(meta.eid("COL3A_1"), "localForces")[0],
    }
    for pat in ("DEAD", "DSD", "SBAL"):
        assemble(model, meta)
        if pat == "DEAD":
            f = lambda: loads.self_weight_distributed(model)  # noqa: E731
        else:
            f = lambda p=pat: apply_uniform(model, meta, pats[p])  # noqa: E731
        estatico[pat] = loads.run_static_case(model, f, EXM, rebuild=False)
    g3a = {k: 1.2 * (estatico["DEAD"][k] + estatico["DSD"][k]) + 1.6 * estatico["SBAL"][k]
           for k in EXM}
    G3A_SAP = {"COL3A_4_M3": 633.284, "COL3A_1_M3": 158.321, "DIN3_1_M3": -633.206,
               "COL3A_4_P": -180.384, "COL3A_1_P": -190.140}
    # Se comparan MAGNITUDES: el signo de M3 no es comparable miembro a miembro,
    # porque el eje local 2 de OpenSees apunta al reves que el de SAP en el
    # dintel (y no en la columna). Es una sola inversion de eje, esta documentada
    # en `case10_data`, y no toca ninguna magnitud.
    for k, s in G3A_SAP.items():
        r = g3a[k]
        print(f"    {k:12s} rukan {r:12.4f}   SAP {s:12.4f}"
              f"   err {abs(abs(r / s) - 1):.2e}")
        assert abs(abs(r / s) - 1) < 1e-5, k

    # --- Modal de 60 modos ---
    masses = D.seismic_mass(model, meta, pats)
    model_m = D.Model(model.nodes, model.materials, model.sections,
                      model.elements, masses)
    assemble(model_m, meta)
    ev = ops.eigen("-fullGenLapack", 60)
    T = [2.0 * math.pi / math.sqrt(l) for l in ev]

    base_set = set(base_ids)
    m_all = sum(nm.values[0] for nm in masses)
    m_free = sum(nm.values[0] for nm in masses if nm.node not in base_set)
    ment = [(nm.node, nm.values[0]) for nm in masses]

    part = []
    for k in range(1, 61):
        mg = sum(m * sum(ops.nodeEigenvector(n, k, c) ** 2 for c in (1, 2, 3))
                 for n, m in ment)
        row = {}
        for d, dof in (("X", 1), ("Y", 2), ("Z", 3)):
            L = sum(m * ops.nodeEigenvector(n, k, dof) for n, m in ment)
            row[d] = (L * L / mg) / m_free
        part.append(row)
    ix = max(range(60), key=lambda i: part[i]["X"])
    iy = max(range(60), key=lambda i: part[i]["Y"])
    acum = {d: sum(r[d] for r in part) for d in "XYZ"}

    print("\n  Modal de 60 modos (masa sismica D + 0,20·S):")
    print(f"    masa del modelo dinamico  {m_all * D.G_ACC:12.3f} kN")
    print(f"    masa que participa        {m_free * D.G_ACC:12.3f} kN"
          "   (el resto cae en nudos de base restringidos)")
    print(f"    P declarado para la norma      674.861 kN"
          "   <- incluye los 77,89 kN del pilar de hastial")
    print(f"    T*_X   modo {ix + 1:2d}   T = {T[ix]:.13f} s   Ux = {part[ix]['X']:.5f}")
    print("    SAP    modo  1   T = 0.8526565963541679 s   Ux = 0.94627")
    print(f"    T*_Y   modo {iy + 1:2d}   T = {T[iy]:.13f} s   Uy = {part[iy]['Y']:.5f}")
    print("    SAP    modo 41   T = 0.1610608923144279 s   Uy = 0.47422")
    print(f"    acumuladas  X {acum['X']:.4f}   Y {acum['Y']:.4f}   Z {acum['Z']:.4f}"
          "     SAP  X 0.9763  Y 0.9783  Z 0.6513")
    T_SAP = {"X": 0.8526565963541679, "Y": 0.1610608923144279}
    assert ix == 0, "el modo dominante en X tiene que ser el 1"
    assert iy == 40, f"el modo dominante en Y tiene que ser el 41, salio el {iy + 1}"
    assert abs(T[ix] / T_SAP["X"] - 1) < 1e-4
    assert abs(T[iy] / T_SAP["Y"] - 1) < 1e-3
    for d, s in (("X", 0.9763), ("Y", 0.9783), ("Z", 0.6513)):
        assert abs(acum[d] - s) < 5e-4, d

    locales = sum(1 for r in part if r["X"] + r["Y"] + r["Z"] < 0.01)
    print(f"    modos locales del punto de cruce (participacion < 1 %): {locales} de 60")
    print("    -- el modo longitudinal REAL es el 41: quien corra 30 modos se lleva"
          " un T* equivocado")

    # --- R* por direccion, Ec. (1b) ---
    # Dos chequeos distintos, y conviene no mezclarlos. Bajo el codo
    # `0,16·R·T1 = 0,1728 s` la Ec. (1b) es LINEAL en T, asi que el R* de la
    # direccion longitudinal hereda entero el error del T*: pedirle que calce a
    # 1e-6 seria pedirle al periodo que calce a 1e-6.
    #   (1) la ECUACION, evaluada en el T* de SAP -> tiene que dar exacto;
    #   (2) el VALOR propagado, con el T* de rukan -> arrastra el 0,055 % de T*_Y.
    r_x_eq = r_star_for(T_SAP["X"], 4.0, "B")
    r_y_eq = r_star_for(T_SAP["Y"], 4.0, "B")
    r_x, r_y = r_star_for(T[ix], 4.0, "B"), r_star_for(T[iy], 4.0, "B")
    print("\n  R* por direccion (Ec. 1b, R = 4, suelo B, codo en 0,1728 s):")
    print(f"    la ecuacion en el T* de SAP:  R*_X {r_x_eq:.13f}   R*_Y {r_y_eq:.13f}")
    print("    SAP                        :  R*_X 4.0000000000000   R*_Y 3.8301633726046")
    print(f"    propagado con el T* de rukan: R*_X {r_x:.13f}   R*_Y {r_y:.13f}"
          f"   (+{(r_y / 3.8301633726045696 - 1) * 100:.3f} % en Y)")
    assert abs(r_x_eq - 4.0) < 1e-12
    assert abs(r_y_eq - 3.8301633726045696) < 1e-12   # la ecuacion, al ultimo bit
    assert abs(r_y / 3.8301633726045696 - 1) < 1e-3   # el valor, con su T*

    # --- Espectral por direccion: el flujo obligatorio de dos pasadas ---
    # Primero el modal (arriba), de ahi el T* dominante de cada direccion, de ahi
    # su R* por la Ec. (1b), y recien entonces UN espectro por direccion con ese
    # R* CONSTANTE. Evaluar la Ec. (1b) periodo a periodo da otra curva.
    esp = {d: nch2369_spectrum(zone=2, soil="B", importance=1.0, R=4.0,
                               damping=D.XI, r_fixed=r)
           for d, r in (("X", r_x_eq), ("Y", r_y_eq))}
    EXQ = {"Qx": lambda: -sum(ops.nodeReaction(n, 1) for n in base_ids),
           "Qy": lambda: -sum(ops.nodeReaction(n, 2) for n in base_ids)}
    q0 = {}
    for d, dirn in (("X", "Ux"), ("Y", "Uy")):
        assemble(model_m, meta)
        dr = run_directional_spectral(model_m, esp[d], dirn, EXQ, D.XI, 60)
        q0[d] = abs(dr.combined("Qx" if d == "X" else "Qy", "CQC"))

    P_NORMA = 674.8610909934324
    q_min, q_max = 70.86041455430902, 224.9066895021051
    print("\n  Corte basal espectral (CQC de 60 modos, R = 4):")
    print(f"    Q0X  rukan {q0['X']:10.6f} kN   SAP  86.960229 kN"
          f"   err {abs(q0['X'] / 86.960228719357 - 1):.2e}")
    print(f"    Q0Y  rukan {q0['Y']:10.6f} kN   SAP 130.257189 kN"
          f"   err {abs(q0['Y'] / 130.2571888641845 - 1):.2e}")
    print(f"    banda §5.12/§5.13 con P = {P_NORMA:.3f} kN:"
          f"  [{q_min:.5f} ; {q_max:.5f}] -> las dos direcciones dentro")
    print(f"    pero ese P es la masa DECLARADA; la que se sacude son"
          f" {m_free * D.G_ACC:.3f} kN (ver SERIE-GALPON.md §5.46)")
    assert abs(q0["X"] / 86.960228719357 - 1) < 3e-3
    assert abs(q0["Y"] / 130.2571888641845 - 1) < 3e-3
    assert q_min < q0["X"] < q_max and q_min < q0["Y"] < q_max

    print("\n  OK capa B - modal, T* de las dos direcciones, R* y corte basal.")

    # ================= CAPA C - COMBINACIONES Y ENVOLVENTE =================
    # 79 combinaciones LRFD: 63 de gravedad y viento por NCh3171 §9.1.1, 12
    # sismicas por NCh2369 §4.5.1 con la simultaneidad de §4.5.2, y 4 de la rama
    # ilustrativa con R = 5. El reparto lo resuelve NCh3171 §9 por escrito:
    # «cuando las normas de diseno sismico consideren otras combinaciones ...
    # ESTAS PREVALECEN».
    #
    # Como los casos espectrales son magnitudes +-, una combinacion lineal que
    # contenga uno da DOS valores: base +- suma de las contribuciones espectrales
    # en valor absoluto. Es lo que SAP reporta como Max/Min, y enumerar los signos
    # a mano los duplicaria.
    print("\n  Envolvente de 79 combinaciones (10 miembros de control):")

    MIEMBROS = ["COL3A_1", "COL3A_4", "DIN3_1", "DIN3_2", "DIN3_3",
                "PUN00_1", "PUN09_2", "ARWA1_1", "ART1_00_1", "PIL1_06"]

    def extractores():
        ex = {}
        for nm in MIEMBROS:
            t = meta.eid(nm)
            # La axial se lee en las DOS estaciones: en una barra con carga de
            # gravedad distribuida el axial varia a lo largo, y en el pilar de
            # hastial la estacion de arriba vale exactamente 0 porque ahi la P
            # esta liberada -- que es el `P_max = 0,0` que reporta SAP.
            ex[nm + "|Pi"] = lambda t=t: -ops.eleResponse(t, "localForces")[0]
            ex[nm + "|Pj"] = lambda t=t: ops.eleResponse(t, "localForces")[6]
            # Las TRES estaciones del diagrama de momento, que es lo que reporta
            # SAP. Ojo con la convencion: `localForces` da los momentos que actuan
            # SOBRE la barra en cada extremo, asi que el valor del DIAGRAMA en la
            # estacion j lleva signo cambiado. Sin eso los signos no calzan con
            # SAP en la mitad de los miembros -- y las magnitudes tampoco, porque
            # el promedio de las dos estaciones sale mal.
            ex[nm + "|Mi"] = lambda t=t: ops.eleResponse(t, "localForces")[5]
            ex[nm + "|Mj"] = lambda t=t: -ops.eleResponse(t, "localForces")[11]
            # Estacion central, sin la parabola de la carga: para los casos
            # espectrales (carga solo nodal, momento lineal) ya es el valor
            # exacto; a los estaticos se les suma w·L²/8 despues, que es lineal
            # en la combinacion. Es la estacion que gobierna el dintel de
            # cumbrera, y mirar solo los extremos la deja fuera por un 7 %.
            ex[nm + "|Mm"] = lambda t=t: (ops.eleResponse(t, "localForces")[5]
                                          - ops.eleResponse(t, "localForces")[11]) / 2.0
        return ex

    EXC = extractores()

    # --- Casos estaticos ---
    casos: dict[str, dict] = {}
    for pat in ["DEAD"] + D.PATTERNS:
        assemble(model, meta)
        if pat == "DEAD":
            f = lambda: loads.self_weight_distributed(model)  # noqa: E731
        else:
            f = lambda p=pat: apply_uniform(model, meta, pats[p])  # noqa: E731
        casos[pat] = loads.run_static_case(model, f, EXC, rebuild=False)

    # La parabola w·L²/8 de cada barra en cada estado, en ejes locales.
    nodes_by_id = {n.id: n for n in model.nodes}
    els_by_id = {e.id: e for e in model.elements}

    def wy_local(nm, items, dead=False):
        e = els_by_id[meta.eid(nm)]
        ni, nj = nodes_by_id[e.node_i], nodes_by_id[e.node_j]
        _, ey, _ = local_axes((ni.x, ni.y, ni.z), (nj.x, nj.y, nj.z), e.vecxz)
        if dead:
            g = (0.0, 0.0, -secs[e.section].A * D.RHO * D.G_ACC)
            return g[2] * ey[2]
        return sum(gg[0] * ey[0] + gg[1] * ey[1] + gg[2] * ey[2]
                   for n2, gg in items if n2 == nm)

    for pat in ["DEAD"] + D.PATTERNS:
        for nm in MIEMBROS:
            L = meta.elem_len[nm]
            w = wy_local(nm, pats.get(pat, []), dead=(pat == "DEAD"))
            casos[pat][nm + "|Mm"] += w * L * L / 8.0

    # EV: §5.7.1, caso estatico vertical C_V·(D + DSD + 0,20·S). Todo es lineal,
    # asi que sale de los casos ya corridos sin volver a resolver.
    CV = 1.2 * 1.0 * 0.42 * 1.00
    casos["EV"] = {k: CV * (casos["DEAD"][k] + casos["DSD"][k] + 0.20 * casos["SBAL"][k])
                   for k in EXC}
    fv = CV * P_NORMA
    print(f"    F_V = C_V·P = {CV:.3f} × {P_NORMA:.4f} = {fv:.7f} kN"
          "   SAP 340.1299898606887")
    assert abs(fv / 340.1299898606887 - 1) < 1e-12

    # --- Casos espectrales: RSX/RSY en R = 4 y R = 5 ---
    esp5 = {d: nch2369_spectrum(zone=2, soil="B", importance=1.0, R=5.0,
                                damping=D.XI, r_fixed=r_star_for(T_SAP[d], 5.0, "B"))
            for d in "XY"}
    for nombre, espectro, dirn in (("RSX_R4", esp["X"], "Ux"), ("RSY_R4", esp["Y"], "Uy"),
                                   ("RSX_R5", esp5["X"], "Ux"), ("RSY_R5", esp5["Y"], "Uy")):
        assemble(model_m, meta)
        dr = run_directional_spectral(model_m, espectro, dirn, EXC, D.XI, 60)
        casos[nombre] = {k: abs(dr.combined(k, "CQC")) for k in EXC}

    # --- Las 79 combinaciones ---
    DL = [("DEAD", 1.0), ("DSD", 1.0)]
    NIEVE = {"B": "SBAL", "I": "SUNBI", "D": "SUNBD"}
    VIENTOS = ["WTXP", "WTXN", "WLYP", "WLYN"]
    ESPECTRALES = {"RSX_R4", "RSY_R4", "RSX_R5", "RSY_R5"}

    def esc(base, f):
        return [(c, f * k) for c, k in base]

    combos: dict[str, list] = {}
    combos["G1"] = esc(DL, 1.4)
    for s, pat in NIEVE.items():
        combos["G2_%s" % s] = esc(DL, 1.2) + [(pat, 0.5)]
        combos["G3A_%s" % s] = esc(DL, 1.2) + [(pat, 1.6)]
        for w in VIENTOS:
            for sg, et in ((1.0, "P"), (-1.0, "N")):
                combos["G3B_%s%s%s" % (s, w[1:], et)] = (
                    esc(DL, 1.2) + [(pat, 1.6), (w, 0.8), ("WPI", 0.8 * sg)])
                combos["G4_%s%s%s" % (s, w[1:], et)] = (
                    esc(DL, 1.2) + [(pat, 0.5), (w, 1.6), ("WPI", 1.6 * sg)])
    for w in VIENTOS:
        for sg, et in ((1.0, "P"), (-1.0, "N")):
            combos["G6_%s%s" % (w[1:], et)] = esc(DL, 0.9) + [(w, 1.6), ("WPI", 1.6 * sg)]
    EQ = [("1", 1.0, 0.3, 0.3), ("2", 0.3, 1.0, 0.3), ("3", 0.3, 0.3, 1.0)]
    GRAV = [("A", esc(DL, 1.2) + [("SBAL", 0.2)]), ("B", esc(DL, 0.9))]
    for eq, fx, fy, fz in EQ:
        for sg, et in ((1.0, "P"), (-1.0, "N")):
            for g, base in GRAV:
                combos["E%s%s_%s" % (eq, et, g)] = (
                    base + [("RSX_R4", fx), ("RSY_R4", fy), ("EV", fz * sg)])
    for eq, fx, fy, fz in EQ[:2]:
        for sg, et in ((1.0, "P"), (-1.0, "N")):
            combos["R5_%s%s" % (eq, et)] = (
                esc(DL, 1.2) + [("SBAL", 0.2), ("RSX_R5", fx), ("RSY_R5", fy),
                                ("EV", fz * sg)])

    print(f"    combinaciones armadas: {len(combos)}   SAP 79")
    assert len(combos) == 79, len(combos)

    GRUPOS = {
        "ENV": list(combos),
        "ENVG": [c for c in combos if c[0] == "G"],
        "ENVE": [c for c in combos if c[0] == "E"],
    }
    assert len(GRUPOS["ENVG"]) == 63 and len(GRUPOS["ENVE"]) == 12

    def envolver(nombres, con_gobernantes=False):
        out, quien = {}, {}
        for nm in MIEMBROS:
            pmin, pmax, mabs = 1e30, -1e30, 0.0
            g = {"P_comp": None, "P_trac": None, "M3": None}
            for c in nombres:
                items = combos[c]
                for st in ("Pi", "Pj"):
                    base_p = sum(f * casos[k][nm + "|" + st] for k, f in items
                                 if k not in ESPECTRALES)
                    spr_p = sum(abs(f) * casos[k][nm + "|" + st] for k, f in items
                                if k in ESPECTRALES)
                    if base_p - spr_p < pmin:
                        pmin, g["P_comp"] = base_p - spr_p, c
                    if base_p + spr_p > pmax:
                        pmax, g["P_trac"] = base_p + spr_p, c
                for st in ("Mi", "Mj", "Mm"):
                    b = sum(f * casos[k][nm + "|" + st] for k, f in items
                            if k not in ESPECTRALES)
                    s = sum(abs(f) * casos[k][nm + "|" + st] for k, f in items
                            if k in ESPECTRALES)
                    v = max(abs(b + s), abs(b - s))
                    if v > mabs:
                        mabs, g["M3"] = v, c
            out[nm] = (pmin, pmax, mabs)
            quien[nm] = g
        return (out, quien) if con_gobernantes else out

    SAP_ENV = {
        "ENV": {"COL3A_1": (-190.14, 13.964, 158.321), "COL3A_4": (-180.384, 21.562, 633.284),
                "DIN3_1": (-136.003, 24.78, 633.206), "DIN3_2": (-148.067, 30.587, 176.334),
                "DIN3_3": (-137.454, 32.502, 207.932), "PUN00_1": (-16.113, 28.248, 1.686),
                "PUN09_2": (-96.087, 14.959, 1.686), "ARWA1_1": (-39.895, 23.651, 0.384),
                "ART1_00_1": (-28.234, 15.007, 2.014), "PIL1_06": (-13.504, 0.0, 23.432)},
        "ENVG": {"COL3A_1": (-190.14, 13.964, 158.321), "COL3A_4": (-180.384, 21.562, 633.284),
                 "DIN3_1": (-136.003, 24.78, 633.206), "DIN3_2": (-148.067, 30.587, 176.334),
                 "DIN3_3": (-137.454, 32.502, 207.932), "PUN00_1": (-5.756, 23.96, 1.385),
                 "PUN09_2": (-96.087, 14.959, 1.385), "ARWA1_1": (-34.233, 16.385, 0.312),
                 "ART1_00_1": (-28.234, 3.675, 1.57), "PIL1_06": (-11.095, 0.0, 23.432)},
        "ENVE": {"COL3A_1": (-110.549, -8.555, 84.486), "COL3A_4": (-96.694, -5.213, 337.165),
                 "DIN3_1": (-66.818, -1.34, 337.098), "DIN3_2": (-69.576, -1.585, 92.165),
                 "DIN3_3": (-63.525, -2.084, 108.078), "PUN00_1": (-16.113, 28.248, 1.686),
                 "PUN09_2": (-42.734, -0.645, 1.686), "ARWA1_1": (-39.895, 23.651, 0.384),
                 "ART1_00_1": (-28.215, 15.007, 2.014), "PIL1_06": (-13.504, 0.0, 0.0)},
    }
    peor_env = 0.0
    for grp in ("ENV", "ENVG", "ENVE"):
        r = envolver(GRUPOS[grp])
        print(f"\n    {grp} ({len(GRUPOS[grp])} combos)"
              f"{'  - total' if grp == 'ENV' else ('  - gravedad y viento' if grp == 'ENVG' else '  - sismo')}")
        print(f"      {'miembro':10s} {'P_min rukan':>12s} {'SAP':>10s} "
              f"{'P_max rukan':>12s} {'SAP':>10s} {'|M3| rukan':>12s} {'SAP':>10s}")
        for nm in MIEMBROS:
            a, b = r[nm], SAP_ENV[grp][nm]
            print(f"      {nm:10s} {a[0]:12.3f} {b[0]:10.3f} {a[1]:12.3f} {b[1]:10.3f} "
                  f"{a[2]:12.3f} {b[2]:10.3f}")
            for x, y in zip(a, b):
                if abs(y) > 1.0:
                    peor_env = max(peor_env, abs(x / y - 1))
                else:
                    peor_env = max(peor_env, abs(x - y) / max(abs(y), 0.5))
    print(f"\n    peor error relativo de las tres envolventes: {peor_env:.2e}")
    assert peor_env < 0.02, peor_env

    # --- De 79 combinaciones, ¿cuantas dimensionan algo? ---
    # Es la pregunta que justifica el post: armar el arbol completo es barato,
    # pero la envolvente la deciden unas pocas. Se contrasta ademas contra las
    # gobernantes que reporto SAP, miembro a miembro.
    _, quien = envolver(GRUPOS["ENV"], con_gobernantes=True)
    GOB_SAP = {
        "COL3A_1": ("G3A_B", "G6_TXPP", "G3A_B"), "COL3A_4": ("G3A_B", "G6_TXPP", "G3A_B"),
        "DIN3_1": ("G3A_B", "G6_LYNP", "G3A_B"), "DIN3_2": ("G3A_B", "G6_LYNP", "G3A_I"),
        "DIN3_3": ("G3A_B", "G6_LYNP", "G3A_B"), "PUN00_1": ("E2N_B", "E2P_A", "E3P_A"),
        "PUN09_2": ("G3A_B", "G6_TXNP", "E3P_A"), "ARWA1_1": ("E2P_A", "E2N_B", "E3P_A"),
        "ART1_00_1": ("G3A_B", "E2N_B", "E3P_A"), "PIL1_06": ("E3P_A", "E3N_A", "G4_BLYPN"),
    }
    print("\n  Cuantas de las 79 dimensionan algo (combo gobernante por miembro):")
    print(f"    {'miembro':10s} {'P_comp':>12s} {'SAP':>10s} {'P_trac':>12s} {'SAP':>10s}"
          f" {'|M3|':>12s} {'SAP':>10s}")
    usadas, coinciden, comparadas = set(), 0, 0
    for nm in MIEMBROS:
        g, s = quien[nm], GOB_SAP[nm]
        mios = (g["P_comp"], g["P_trac"], g["M3"])
        print(f"    {nm:10s} {mios[0]:>12s} {s[0]:>10s} {mios[1]:>12s} {s[1]:>10s}"
              f" {mios[2]:>12s} {s[2]:>10s}")
        usadas.update(mios)
        for a, b in zip(mios, s):
            comparadas += 1
            coinciden += (a == b)
    print(f"\n    combinaciones distintas que gobiernan algo: {len(usadas)} de 79")
    print(f"    -> {sorted(usadas)}")
    print(f"    coinciden con la gobernante de SAP: {coinciden} de {comparadas}")
    assert len(usadas) <= 12, len(usadas)
    # PIL1_06 no tiene traccion (P_max = 0,0 exacto en la estacion liberada), asi
    # que su "gobernante de traccion" es un empate y no tiene por que coincidir.
    assert coinciden >= comparadas - 2, (coinciden, comparadas)

    print("\n  OK capa C - 79 combinaciones, las tres envolventes y las gobernantes.")
    print("\n  OK caso 10 - el galpon del altiplano reproduce el modelo congelado"
          " de SAP2000\n     sin abrir el programa.")


if __name__ == "__main__":
    main()
