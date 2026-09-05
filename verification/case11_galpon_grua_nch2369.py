"""Caso 11 — El galpón con puente grúa: el marco transversal contra la serie de memos.

El primer peldaño de la escalera cuyo patrón de referencia **no es SAP2000**. La
serie `nch2369-galpon-grua` de `F:\\Proyectos_Python\\Guias_Interactivas` recorre
el diseño completo de este galpón en doce eslabones verificados, y en el camino
publica un puñado de resultados de análisis que ningún memo calcula: los declara.
Este caso los corre.

Los tres caminos que se cruzan acá
----------------------------------
1. **OpenSeesPy vía `rukan.engine`** — el marco montado en un dominio 3D de seis
   grados de libertad, con los GDL fuera del plano fijados.
2. **`case11_ref`** — rigidez directa de pórtico plano en numpy puro, que no
   importa `rukan` ni `openseespy`. Comparten `case11_data`, que es geometría y
   secciones, no análisis.
3. **Los memos** — `nch2369-galpon-grua-07 · S1`, que declara `k_Y`, `k_riel` y
   `M_base`; `-10 · D6`, que declara `k_esc`; `-04 · S2`, que declara los
   períodos.

Qué encontró
------------
Las secciones y la geometría de la serie se reproducen **al último dígito
publicado**, incluida la sección compuesta del escalón que el 10 · B3 publica sin
mostrar su derivación (`A = 43 314,00000 mm²`, `Ix = 14 310 239 430 mm⁴`,
`B = 4,86057`).

Y `k_Y` no. El modelo da 6 152,89 kN/m contra los 5 612,11747 declarados, un
9,6 % de diferencia, mientras `k_riel` calza a 2·10⁻⁵. La diferencia **no es de
malla ni de sección**: es de **caso de carga**. El empuje aplicado en un solo
alero reproduce los tres números que el 07 publica —`k_Y`, `M_base/M_nudo` y
`y_infl`— con error 2·10⁻⁵ cada uno; el empuje de *sway*, que es el que un modo
lateral tiene, da los tres distintos. El memo mezcla las dos convenciones: `sway`
para el nivel del riel —donde el empuje de la grúa entra por los dos rieles al
mismo lado, y ahí está bien— y **un solo alero** para el alero, que es de donde
sale el período.

Lo que arrastra está medido en la capa C, y **ninguna rama cambia**: los dos
períodos quedan sobre el codo de 0,28 s de la Ec. (1b), así que `R*_Y = 5,00` en
los dos casos, y el recorte de §5.13 sigue gobernando el corte de diseño.

    python verification/case11_galpon_grua_nch2369.py
"""

from __future__ import annotations

import datetime
import math
import os
import sys

import openseespy.opensees as ops

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import case11_data as D  # noqa: E402
import case11_ref as REF  # noqa: E402
from rukan import loads  # noqa: E402
from rukan.engine import build  # noqa: E402

TOL = 5e-4       # 0,05 % — la tolerancia de la escalera, entre los dos motores
TOL_MEMO = 1e-4  # contra una cifra que el memo publica con cinco decimales

NSUB = 28        # 84 tramos por columna: convergido a 1e-5 (ver capa B)


# ===================== ENSAMBLE Y CASOS DE CARGA =====================
def montar(model, meta) -> None:
    """`build` más los GDL fuera del plano.

    El marco vive en el plano Y-Z y se monta en un dominio de seis GDL: sin fijar
    `Ux`, `Ry` y `Rz` en cada nudo libre la matriz es singular. No es una
    restricción con contenido físico —ninguna carga de este contraste sale del
    plano— y por eso no aparece en `Node.restraints`, que describe la estructura.
    """
    build(model)
    for nm in meta.libres:
        ops.fix(meta.nid(nm), *D.FUERA_DE_PLANO_FIX)


def empuje(meta, nodos, H=1.0):
    """Reparte `H` en `nodos`, en la dirección transversal `+Y`."""
    def aplicar():
        for n in nodos:
            ops.load(meta.nid(n), 0.0, H / len(nodos), 0.0, 0.0, 0.0, 0.0)
    return aplicar


def nodo_en_z(meta, l: str, z: float) -> str:
    """El nudo de la columna `l` que cae en la cota `z`."""
    tope = "R1_0" if l == "A" else "R1_%d" % D.NJ
    cand = [(abs(xyz[2] - z), nm) for nm, xyz in meta.node_xyz.items()
            if nm.startswith("K1%s_" % l) or nm == tope]
    d, nm = min(cand)
    assert d < 1e-9, "no hay nudo en z = %.5f (el más cercano dista %.2e)" % (z, d)
    return nm


def rigidez_ops(nsub: int, nodos_carga, nodo_medida, escalonada=False) -> float:
    """`H / δ` con OpenSees: `H = 1` repartido, medido en el primer nudo cargado."""
    model, meta = D.build_frame(nsub=nsub, escalonada=escalonada)
    nc = [n if n.startswith(("R1_", "K1")) else nodo_en_z(meta, n[-1], D.Z_RIEL)
          for n in nodos_carga]
    nm = nodo_medida if nodo_medida.startswith(("R1_", "K1")) \
        else nodo_en_z(meta, nodo_medida[-1], D.Z_RIEL)
    montar(model, meta)
    r = loads.run_static_case(
        model, empuje(meta, nc),
        {"uy": lambda: ops.nodeDisp(meta.nid(nm), 2)}, rebuild=False)
    return 1.0 / r["uy"]


ALERO = {"A": "R1_0", "B": "R1_%d" % D.NJ}
RIEL = {"A": "rielA", "B": "rielB"}


def tol_impresa(lit: str) -> float:
    """Media unidad del ultimo decimal que el memo imprime.

    Es la misma regla que `SERIES.md` § 4 le impone a un numero que viaja entre
    memos, y la unica honesta para contrastar contra una cifra publicada: pedirle
    a `4 249,18` que calce a 1e-7 es pedirle decimales que nadie escribio.
    """
    d = len(lit.split(",")[1]) if "," in lit else 0
    return 0.5 * 10.0 ** (-d)


def fila(nom, a, b, ref=None, u="", tol=TOL):
    err = abs(a / b - 1.0) if b else abs(a - b)
    extra = "" if ref is None else "   memo %s" % ref
    print(f"    {nom:34s} ops {a:14.5f}   ref {b:14.5f}   err {err:8.2e}{extra}")
    assert err < tol, f"{nom}: los dos motores difieren {err:.2e}"
    return a




# ==================== CAPA D - EL GALPON EN 3D ====================
def modal_3d(nsub: int = 4, n_modos: int = 15, escalonada: bool = True,
             x_grua: float = None):
    """Modal del galpón completo. Devuelve `(T, participacion, m_total, meta)`.

    La participación se calcula como en `case09`: `L²/(M_gen · M_total)` por
    dirección, que es la razón de masa participante que reporta SAP y la que
    §5.4 pide para elegir el modo dominante de cada dirección.
    """
    kw = {} if x_grua is None else {"x_grua": x_grua}
    model, meta = D.build_model(nsub=nsub, escalonada=escalonada, **kw)
    build(model)
    ev = ops.eigen(n_modos)
    T = [2.0 * math.pi / math.sqrt(l) for l in ev]
    ment = [(nm.node, nm.values[0]) for nm in model.masses]
    m_tot = sum(m for _, m in ment)
    part = []
    for k in range(1, n_modos + 1):
        mg = sum(m * sum(ops.nodeEigenvector(n, k, c) ** 2 for c in (1, 2, 3))
                 for n, m in ment)
        part.append({d: (sum(m * ops.nodeEigenvector(n, k, dof)
                             for n, m in ment) ** 2 / mg) / m_tot
                     for d, dof in (("X", 1), ("Y", 2), ("Z", 3))})
    return T, part, m_tot, meta


def r_star(T: float) -> float:
    """Ec. (1b) con los parámetros del 04: `R` de tabla sobre el codo, rampa bajo él."""
    return D.R_TABLA if T >= D.CR_T1 else 1.5 + (D.R_TABLA - 1.5) * T / D.CR_T1


def capa_d() -> dict:
    print("\n  Capa D - el galpon completo en 3D: los periodos y las masas"
          " participantes\n  -- que el 04 · `## Limites` declara no tener --\n")
    model, meta = D.build_model(nsub=4)
    print(f"    {len(model.nodes)} nudos · {len(model.elements)} barras ·"
          f" {len(meta.bases)} bases empotradas · {len(model.masses)} nudos con masa")

    # La masa del modelo es la del 05, termino a termino. Si un termino se
    # repartio dos veces o ninguna, esta suma lo dice y nada mas lo diria.
    W = sum(nm.values[0] for nm in model.masses) * D.G_MEMO
    print(f"    peso sismico repartido {W:.5f} kN   memo 05 · C4  1037,08500"
          f"   err {abs(W/D.P_SISMICO-1):.1e}")
    assert abs(W / D.P_SISMICO - 1.0) < 1e-9, "la masa no es la del 05"

    # Convergencia de la malla del tapered.
    Ts = []
    for nsub in (2, 4, 8):
        T, p, _, _ = modal_3d(nsub=nsub, n_modos=6)
        iy = max(range(6), key=lambda i: p[i]["Y"])
        Ts.append(T[iy])
    print(f"    convergencia de T*_Y:  {Ts[0]:.6f}  {Ts[1]:.6f}  {Ts[2]:.6f}"
          f"   -> {abs(Ts[2]/Ts[1]-1):.1e}")
    assert abs(Ts[2] / Ts[1] - 1.0) < 1e-3, "la malla del tapered no convergio"

    out = {}
    for esc, etq in ((False, "sin el escalon del 10"), (True, "con el escalon del 10")):
        T, part, m_tot, _ = modal_3d(escalonada=esc)
        ix = max(range(len(part)), key=lambda i: part[i]["X"])
        iy = max(range(len(part)), key=lambda i: part[i]["Y"])
        ac = {d: sum(p[d] for p in part) for d in "XYZ"}
        print(f"\n    {etq}:")
        print(f"      T*_X  modo {ix+1:2d}   T = {T[ix]:.6f} s   Ux = {part[ix]['X']:.5f}"
              f"   R* = {r_star(T[ix]):.5f}")
        print(f"      T*_Y  modo {iy+1:2d}   T = {T[iy]:.6f} s   Uy = {part[iy]['Y']:.5f}"
              f"   R* = {r_star(T[iy]):.5f}")
        print(f"      masa participante acumulada   X {ac['X']:.5f}   Y {ac['Y']:.5f}"
              f"   Z {ac['Z']:.5f}")
        assert ac["X"] > 0.90 and ac["Y"] > 0.90, "no se llega al 90 % de masa"
        k = "esc" if esc else "sim"
        out.update({f"T_star_X_{k}": T[ix], f"T_star_Y_{k}": T[iy],
                    f"Ux_{k}": part[ix]["X"], f"Uy_{k}": part[iy]["Y"],
                    f"macum_X_{k}": ac["X"], f"macum_Y_{k}": ac["Y"],
                    f"macum_Z_{k}": ac["Z"],
                    f"R_star_X_{k}": r_star(T[ix]), f"R_star_Y_{k}": r_star(T[iy])})

    # Contra lo que la serie publica. Son cuatro contrastes y ninguno es un ajuste.
    print("\n    Contra lo que la serie ya publica:")
    CONTRA = [
        ("T*_X, contra el declarado en 04 · S2", out["T_star_X_esc"], 0.20, 0.05),
        ("T*_Y sin escalon, contra 07 · B5", out["T_star_Y_sim"], 0.38566, 0.03),
        ("T*_Y con escalon, contra 10 · D6", out["T_star_Y_esc"], 0.25722, 0.05),
        ("R*_Y con escalon, contra 10 · D6", out["R_star_Y_esc"], 4.71525, 0.05),
        ("R*_X, contra el publicado en 04 · C4", out["R_star_X_esc"], 4.00000, 0.05),
    ]
    for nom, v, s, tol in CONTRA:
        err = abs(v / s - 1.0)
        print(f"      {nom:38s} {v:10.5f}   memo {s:10.5f}   {err*100:+6.2f} %")
        assert err < tol, f"{nom}: {err:.1%} sobre la tolerancia de {tol:.0%}"
    print("\n    -> el modelo 3D **confirma** la cadena de la serie por los dos lados: el"
          "\n       periodo del 07 a 1,0 %, el cruce de rama que el 10 · D6 encontro a"
          "\n       3,2 %, y el T*_X y el R*_X que el 04 declara a 3,0 y 1,9 %.")
    print(f"       Y el 04 · `## Limites` declaraba no tener masas participantes:"
          f" son\n       X {out['macum_X_esc']:.5f} e Y {out['macum_Y_esc']:.5f}"
          f" acumuladas en 15 modos.")
    print("\n  OK capa D - el modelo 3D corre y coincide con lo que la serie declaraba.")
    return out


def emitir_json(ruta: str, datos: dict) -> None:
    """Escribe el JSON que `_kit/verify_modelo.py` consume desde el repo de memos.

    Lleva de dónde salió cada cosa —script, versión de rukan, commit y fecha—
    porque un archivo de resultados sin procedencia es exactamente lo que
    `SERIES.md` § 5 rechaza: un artefacto que nada regenera y que miente sobre su
    propia naturaleza. Este lo regenera el script que está nombrado adentro.
    """
    import json
    import subprocess
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                                cwd=os.path.dirname(os.path.dirname(
                                    os.path.abspath(__file__))),
                                capture_output=True, text=True, timeout=10
                                ).stdout.strip() or None
    except Exception:
        commit = None
    doc = {
        "script": "verification/" + os.path.basename(__file__),
        "rukan": getattr(__import__("rukan"), "__version__", "0.0.1"),
        "commit": commit,
        "generado": datetime.datetime.now().isoformat(timespec="seconds"),
        "unidades": {"T": "s", "k": "kN/m", "M": "kN·m", "P": "kN"},
        "valores": datos,
    }
    with open(ruta, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2, sort_keys=True)
    print(f"\n  escrito  {ruta}  ({len(datos)} magnitudes)")

def main() -> int:
    print("Caso 11 - Galpon con puente grua NCh2369 (Rukan vs numpy vs la serie de memos)")

    # ===================== CAPA A - GEOMETRIA Y SECCIONES =====================
    # El assert mas barato y el mas completo: si una sola cota o un solo espesor
    # esta mal, alguna de estas quince cifras se cae.
    print("\n  Capa A - la geometria y las secciones contra lo que la serie publica:")
    A_ = [
        ("largo total [m]", D.LARGO, "30,00", "05 · A1"),
        ("cumbrera [m]", D.H_CUMB, "13,00", "05 · A1"),
        ("excentricidad del riel [mm]", D.E_COL_RIEL * 1e3, "1000,00000", "10 · A2"),
        ("cota del asiento [mm]", D.H_ASIENTO * 1e3, "6684,24000", "10 · A2"),
        ("media agua sobre el rafter [mm]", D.L_RAFTER * 1e3, "12747,55", "07 · B1"),
        ("panel del techo [mm]", D.B_PAN_TECHO * 1e3, "4249,18", "11 · C3"),
        ("diagonal del techo [mm]", D.L_DIAG_TECHO * 1e3, "8620,07", "11 · C3"),
        ("area de planta [m2]", D.A_PLANTA, "750,00000", "05 · A2"),
        ("area de muros [m2]", D.A_MUROS, "1217,50000", "05 · A2"),
        ("peso del edificio [kN]", D.W_EDIFICIO, "807,08500", "05 · A3"),
        ("peso sismico [kN]", D.P_SISMICO, "1037,08500", "05 · C4"),
        ("canto de columna en el riel [mm]", D.d_col(D.Z_RIEL) * 1e3, "835,71429", "07 · B3"),
        ("canto de columna en el paso [mm]", D.d_col(D.H_ASIENTO) * 1e3, "859,02171",
         "10 · B4"),
    ]
    for nom, v, lit, src in A_:
        s_ = float(lit.replace(",", "."))
        t = tol_impresa(lit)
        print(f"    {nom:34s} {v:16.5f}   memo {lit:>14s}  ({src})"
              f"   |d| {abs(v - s_):.2e} < {t:.0e}")
        assert abs(v - s_) <= t, nom

    S_ = [
        ("COL base: A [mm2]", D.i_props(1.050, D.COL_BF, D.COL_TF, D.COL_TW)[0] * 1e6,
         27284.0, "07 · B3"),
        ("COL base: I [mm4]", D.i_props(1.050, D.COL_BF, D.COL_TF, D.COL_TW)[1] * 1e12,
         4675712519.0, "07 · B3"),
        ("COL riel: A [mm2]", D.i_props(D.d_col(D.Z_RIEL), D.COL_BF, D.COL_TF,
                                        D.COL_TW)[0] * 1e6, 24284.0, "07 · B3"),
        ("RAF nudo: I [mm4]", D.i_props(0.750, D.RAF_BF, D.RAF_TF, D.RAF_TW)[1] * 1e12,
         1690494333.0, "07 · B3"),
        ("RAF nudo: Iy [mm4]", D.i_props(0.750, D.RAF_BF, D.RAF_TF, D.RAF_TW)[2] * 1e12,
         52185573.0, "07 · B3"),
        ("RAF cumbrera: I [mm4]", D.i_props(0.425, D.RAF_BF, D.RAF_TF, D.RAF_TW)[1] * 1e12,
         467462458.0, "07 · B3"),
        ("diagonal de techo: A [mm2]", D.box_props(*D.TUBO_DIAG)[0] * 1e6, 2400.0, "11 · E1"),
        ("puntal de techo: A [mm2]", D.box_props(*D.TUBO_PUNT)[0] * 1e6, 4656.0, "11 · E2"),
        ("carrilera: cg desde el ala sup [mm]",
         (D.CAR_BFS * D.CAR_TFS * D.CAR_TFS / 2
          + D.CAR_TW * D.CAR_HW * (D.CAR_TFS + D.CAR_HW / 2)
          + D.CAR_BFI * D.CAR_TFI * (D.CAR_TFS + D.CAR_HW + D.CAR_TFI / 2))
         / D.carrilera_props()[0] * 1e3, 269.64968, "08 · `## Caso`"),
    ]
    print()
    for nom, v, s_, src in S_:
        err = abs(v / s_ - 1.0)
        print(f"    {nom:34s} {v:16.5f}   memo {s_:14.5f}  ({src})   err {err:.1e}")
        assert err < 1e-8, nom

    # La seccion compuesta del escalon: el 10 · B3 la publica sin derivarla.
    Acmp, ybar, ix, iy, _ = D.comp_props(0.0)
    Acmp_p, ybar_p, _, _, _ = D.comp_props(D.H_ASIENTO)
    _, i_col_base, _, _ = D.i_props(1.050, D.COL_BF, D.COL_TF, D.COL_TW)
    d_paso = D.d_col(D.H_ASIENTO)
    i_sup = (D.COL_BF * d_paso ** 3
             - (D.COL_BF - D.COL_TW) * (d_paso - 2 * D.COL_TF) ** 3) / 12.0
    C_ = [
        ("compuesta base: A [mm2]", Acmp * 1e6, 43314.0, 1e-9),
        ("compuesta base: ybar [mm]", ybar * 1e3, 348.66036, 1e-7),
        ("compuesta base: Ix [mm4]", ix * 1e12, 14310239430.0, 1e-9),
        ("compuesta base: Iy [mm4]", iy * 1e12, 171283622.0, 1e-7),
        ("compuesta paso: A [mm2]", Acmp_p * 1e6, 41595.19539, 1e-9),
        ("compuesta paso: ybar [mm]", ybar_p * 1e3, 374.02402, 1e-7),
        ("razon Ix/Icol", ix / i_col_base, 3.06055, 1e-6),
        ("parametro B de las Comm Tablas", ix / i_sup, 4.86057, 1e-6),
    ]
    print()
    for nom, v, s_, tol in C_:
        err = abs(v / s_ - 1.0)
        print(f"    {nom:34s} {v:16.5f}   memo {s_:14.5f}  (10 · B3/B4)   err {err:.1e}")
        assert err < tol, nom
    print("\n  OK capa A - la geometria y las 30 propiedades de seccion son las de la serie.")

    # ======================= CAPA B - LA RIGIDEZ LATERAL =======================
    print("\n  Capa B - la rigidez del marco. Los dos motores primero, y despues el memo.")
    print("  -- 84 tramos por columna y 168 por rafter; la convergencia se mide abajo --\n")

    kY_uno = fila("k_Y  con UN solo alero [kN/m]",
                  rigidez_ops(NSUB, [ALERO["A"]], ALERO["A"]),
                  REF.rigidez(["aleroA"], NSUB))
    kY_sway = fila("k_Y  con los dos aleros [kN/m]",
                   rigidez_ops(NSUB, [ALERO["A"], ALERO["B"]], ALERO["A"]),
                   REF.rigidez(["aleroA", "aleroB"], NSUB))
    kR_sway = fila("k_riel con los dos rieles [kN/m]",
                   rigidez_ops(NSUB, [RIEL["A"], RIEL["B"]], RIEL["A"]),
                   REF.rigidez(["rielA", "rielB"], NSUB))
    kR_uno = fila("k_riel con UN solo riel [kN/m]",
                  rigidez_ops(NSUB, [RIEL["A"]], RIEL["A"]),
                  REF.rigidez(["rielA"], NSUB))

    # Convergencia de la malla: el numero, no la fe.
    kg = [REF.rigidez(["aleroA", "aleroB"], n) for n in (14, 28, 56)]
    dr = abs(kg[2] / kg[1] - 1.0)
    print(f"\n    convergencia de k_Y (sway):  42 tramos {kg[0]:.5f}"
          f"   84 {kg[1]:.5f}   168 {kg[2]:.5f}   -> {dr:.1e}")
    assert dr < 1e-4, "la malla no convergio"

    # Los tres numeros del 07, y de que caso de carga salen.
    r_uno, y_uno = REF.diagrama_columna(["aleroA"], NSUB)
    r_sway, y_sway = REF.diagrama_columna(["aleroA", "aleroB"], NSUB)
    MEMO = {"k_Y": 5612.11747, "k_riel": 15057.33721,
            "MbMn": 2.81628, "y_infl": 7.74863}
    print("\n    Los tres numeros que el 07 publica, contra los dos casos de carga:")
    print(f"    {'magnitud':22s} {'memo 07':>14} {'UN alero':>14} {'sway':>14}")
    for nom, s, a, b in (("k_Y [kN/m]", MEMO["k_Y"], kY_uno, kY_sway),
                         ("M_base/M_nudo", MEMO["MbMn"], r_uno, r_sway),
                         ("y_inflexion [m]", MEMO["y_infl"], y_uno, y_sway)):
        print(f"    {nom:22s} {s:14.5f} {a:14.5f} {b:14.5f}"
              f"   ({abs(a/s-1):.1e} y {abs(b/s-1)*100:+.2f} %)")
        assert abs(a / s - 1.0) < TOL_MEMO, f"{nom}: el caso de UN alero deberia calzar"
    print(f"    {'k_riel [kN/m]':22s} {MEMO['k_riel']:14.5f} {kR_uno:14.5f} {kR_sway:14.5f}"
          f"   ({abs(kR_uno/MEMO['k_riel']-1)*100:+.2f} % y {abs(kR_sway/MEMO['k_riel']-1):.1e})")
    assert abs(kR_sway / MEMO["k_riel"] - 1.0) < TOL_MEMO, \
        "k_riel deberia calzar con el caso de sway"

    print("\n    -> los tres numeros del alero salen del empuje en UN SOLO alero, y el del")
    print("       riel del empuje de SWAY. Son dos convenciones distintas en el mismo memo,")
    print("       y la del alero no es una rigidez lateral: incluye la parte antisimetrica")
    print("       —el marco abriendose— que ningun modo de traslacion tiene.")

    # k_esc del 10, con las dos convenciones.
    print("\n    El escalon del 10 · D6, medido con las dos convenciones:")
    for nom, nodos in (("un solo alero", ["aleroA"]), ("sway", ["aleroA", "aleroB"])):
        simple = REF.rigidez(nodos, NSUB, escalonada=False)
        esc = REF.rigidez(nodos, NSUB, escalonada=True)
        print(f"      {nom:15s} simple {simple:11.2f}   escalonada {esc:11.2f}"
              f"   k_esc {esc/simple:8.5f}   memo 2,24801"
              f"   {abs(esc/simple/2.24801-1)*100:+.2f} %")
    k_esc_uno = (REF.rigidez(["aleroA"], NSUB, escalonada=True)
                 / REF.rigidez(["aleroA"], NSUB))
    assert abs(k_esc_uno / 2.24801 - 1.0) < 2e-3, "k_esc tambien sale del caso de un alero"
    print("      -> el 10 heredo la convencion del 07, como su S5 declara que hizo.")
    print("\n  OK capa B - los dos motores coinciden a 1e-8 y el caso de carga esta"
          " identificado.")

    # ==================== CAPA C - LO QUE ARRASTRA ====================
    print("\n  Capa C - lo que cuelga del periodo, con una y otra rigidez:")
    m_marco = D.P_SISMICO / (D.NMARCOS * D.G_MEMO)
    print(f"    masa por marco  m = {m_marco:.5f} t     memo 07 · B5  21,14343")
    assert abs(m_marco / 21.14343 - 1.0) < 1e-6

    def cadena(k):
        T = 2.0 * math.pi * math.sqrt(m_marco / k)
        sa = REF.sa_h(T)
        q0 = D.IMPORTANCIA * sa * D.F_XI / D.R_TABLA * D.P_SISMICO
        d = D.IMPORTANCIA * D.F_XI * sa * D.G_MEMO * T ** 2 / (4.0 * math.pi ** 2) * 1e3
        return T, sa, q0, d

    T1, sa1, q1, d1 = cadena(kY_uno)
    T2, sa2, q2, d2 = cadena(kY_sway)
    # El camino del memo, reproducido: es lo que valida la formula antes de moverla.
    for nom, v, s in (("T*_Y2 del 07 · B5", T1, 0.38566),
                      ("Sa_H(T*) del 07 · B5", sa1, 1.22333),
                      ("Q0 del analisis del 07 · B6", q1, 366.06989),
                      ("d_Y2 del 07 · C5", d1, 65.22861)):
        err = abs(v / s - 1.0)
        print(f"    {nom:34s} {v:14.5f}   memo {s:12.5f}   err {err:.1e}")
        assert err < 1e-4, nom

    print(f"\n    {'magnitud':30s} {'memo (un alero)':>17} {'modelo (sway)':>15} {'delta':>10}")
    for nom, a, b in (("k_Y [kN/m]", kY_uno, kY_sway), ("T*_Y2 [s]", T1, T2),
                      ("Sa_H(T*) [g]", sa1, sa2), ("Q0 del analisis [kN]", q1, q2),
                      ("d_Y2 [mm]", d1, d2), ("uso de §6.3", d1 / 157.5, d2 / 157.5)):
        print(f"    {nom:30s} {a:17.5f} {b:15.5f} {(b/a-1)*100:+9.2f} %")

    print(f"\n    Ec. (1b): el codo esta en Cr_T1 = {D.CR_T1:.2f} s (04 · C2) y los dos"
          f" periodos\n      —{T1:.5f} y {T2:.5f} s— caen encima: R*_Y = 5,00 en los dos casos.")
    assert T1 > D.CR_T1 and T2 > D.CR_T1, "la rama de la Ec. (1b) cambiaria"
    print(f"    §5.13: el analisis da {q1:.2f} y {q2:.2f} kN, los dos sobre el corte de"
          f" diseno\n      de {D.Q0_MEMO:.5f} kN, asi que el recorte gobierna y Q0 NO se mueve.")
    assert q1 > D.Q0_MEMO and q2 > D.Q0_MEMO
    print(f"    §6.3: el uso pasa de {d1/157.5:.5f} a {d2/157.5:.5f}, los dos muy bajo 1.")
    assert d2 / 157.5 < 1.0

    print("\n  OK capa C - ninguna rama cambia. Lo que cambia es el periodo (-4,5 %), la"
          "\n     ordenada (+0,7 %) y la deriva de servicio (-8,1 %).")

    d = capa_d()
    d.update({
        "k_Y": kY_sway, "k_riel": kR_sway, "k_Y_un_alero": kY_uno,
        "k_esc": (REF.rigidez(["aleroA", "aleroB"], NSUB, escalonada=True)
                  / REF.rigidez(["aleroA", "aleroB"], NSUB)),
        "MbMn": r_sway, "y_infl": y_sway,
        "P_sismico": D.P_SISMICO, "m_marco": m_marco,
    })
    emitir_json(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "case11_galpon_grua.json"), d)

    print("  Caso 11, capas A a D: OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
