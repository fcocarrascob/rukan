"""Nota 06 — El marco de peralte variable: qué se pierde al prismatizar, y cuántos tramos hacen falta.

**Esta nota no es de la serie Laboratorio.** El script vive acá porque es donde
vive el trabajo con OpenSeesPy y donde está la referencia independiente en numpy,
pero su destino es el **post 2 de la serie del galpón del altiplano**
(`rukan-verificacion-galpon-tapered`, Rukan 8) en struct_pad. Cumple igual el
criterio de admisión del laboratorio: dos caminos independientes para el mismo
problema, y `lab/_lib/ref.py` no importa `rukan` ni `openseespy`.

La pregunta, en una frase
-------------------------
Un marco de galpón con columna y dintel de **peralte variable** no se puede meter
tal cual en un motor que no tenga sección no prismática. Hay dos salidas: cambiar
el tapered por un **prismático equivalente**, o **discretizarlo** en tramos de
sección constante. Esta nota mide qué cuesta cada una.

Por qué importa, y no es un detalle de mallado
----------------------------------------------
El modelo SAP2000 de la serie **se prohibió a sí mismo** la sección no prismática
del programa, y lo dejó escrito en su propio script: *«PROHIBIDA la seccion no
prismatica de SAP (no reproducible desde rukan)»*. Es una decisión de modelación
tomada por **verificabilidad**: se renuncia a una comodidad del programa para que
un segundo motor pueda rehacer el modelo y confrontarlo. Esta nota es lo que
justifica esa renuncia — y de paso mide el precio de la salida fácil.

El caso
-------
El marco transversal del galpón del altiplano, aislado y completamente declarado
(la memoria de cálculo de la serie es `struct_pad/SERIE-GALPON.md`):

- Luz 24,0 m, pendiente 10°, altura de alero 8,0 m, **bases articuladas**.
- Columna de peralte variable **350 → 800 mm** (creciendo hacia la rodilla);
  dintel **800 → 350 mm** (decreciendo hacia la cumbrera).
- Soldado por planchas: alas 220 × 12 mm, alma 6 mm, en todas las secciones.
- Acero A36 de plancha: E = 200 000 MPa, ρ = 7,85 t/m³.
- **Ancho tributario 6,0 m**, el de un marco interior.

Las tres cargas, declaradas — sin esto el estudio no es reproducible, que es
exactamente lo que le pasó a la primera versión de este trabajo (`SERIE-GALPON.md`
§8):

1. **Gravedad**, la combinación gobernante `G3A_B = 1,2·(D + D_sd) + 1,6·S`, con
   `D_sd = 0,35 kPa` de techo y `0,12 kPa` de muro, `S = 1,20 kPa` de nieve
   balanceada sobre proyección horizontal, más el peso propio del acero.
2. **Masa sísmica** `D + 0,20·S` sobre el ancho tributario, concentrada en los
   nudos — la que da el período.
3. **Lateral**, una fuerza total de **1 kN repartida en proporción a la masa
   nodal**: el equivalente estático del primer modo, que es lo que mide una
   verificación de deriva. Normalizada, porque lo que se compara son razones.

Los dos caminos
---------------
1. `lab/_lib/ref.py` — rigidez directa en numpy puro, con los GDL sin masa
   **condensados** para el modal (`Portico2D.periodos`).
2. `rukan` sobre OpenSeesPy — el mismo marco como `elasticBeamColumn`.

Ninguna de las dos sabe de la otra, y las dos tienen que dar lo mismo antes de
que cualquier número entre a un post.
"""

from __future__ import annotations

import math

import numpy as np
import openseespy.opensees as ops

from lab._lib.ref import Barra2D, Portico2D
from lab._lib.report import Fila, reportar
from rukan.engine import build
from rukan.model import FrameElement, Material, Model, Node, Section

# ============================== DATOS ==============================
LUZ, PEND, H_ALERO = 24.0, 10.0, 8.0
TRIB = 6.0                       # ancho tributario del marco interior [m]
D_BASE, D_ALERO, D_CUMBRE = 0.350, 0.800, 0.350
BF, TF, TW = 0.220, 0.012, 0.006
E_STEEL, NU = 2.0e8, 0.3         # kN/m²
GAMMA = 76.9822                  # kN/m³
G_ACC = 9.80665
RHO = GAMMA / G_ACC              # t/m³

D_TECHO, D_MURO, S_BAL = 0.35, 0.12, 1.20   # kPa
H_LATERAL = 1.0                  # kN, total repartido segun masa nodal

TAN, COS = math.tan(math.radians(PEND)), math.cos(math.radians(PEND))
FLECHA = (LUZ / 2.0) * TAN       # 2,116 m
L_FALDON = (LUZ / 2.0) / COS

N_REF = 36                       # malla de referencia, por miembro
N_MODELO = (4, 3)                # la del .sdb: 4 tramos de columna, 3 por faldon


def i_props(d: float) -> tuple[float, float]:
    """(A, I) de la doble T soldada de peralte `d`."""
    h = d - 2.0 * TF
    A = 2.0 * BF * TF + h * TW
    I = TW * h ** 3 / 12.0 + 2.0 * (BF * TF ** 3 / 12.0 + BF * TF * ((d - TF) / 2.0) ** 2)
    return A, I


def _d_lineal(d0: float, d1: float, k: int, n: int) -> float:
    """Peralte del tramo `k` de `n` (1-based), medido en su punto medio."""
    return d0 + (d1 - d0) * (k - 0.5) / n


# ============================ EL MARCO =============================
class Marco:
    """Geometría y cargas del marco, para una malla dada.

    `n_col` y `n_faldon` son los tramos prismáticos de la columna y de cada
    faldón. Si `d_fija` no es None, todas las barras usan ese peralte: es el
    **prismático equivalente**.
    """

    def __init__(self, n_col: int, n_faldon: int, d_fija: float | None = None):
        self.n_col, self.n_faldon, self.d_fija = n_col, n_faldon, d_fija
        self.xy: list[tuple[float, float]] = []
        self.barras: list[tuple[int, int, float, float, str]] = []  # i, j, A, I, tipo
        self._armar()

    def _nodo(self, x, y) -> int:
        for k, (a, b) in enumerate(self.xy):
            if abs(a - x) < 1e-9 and abs(b - y) < 1e-9:
                return k
        self.xy.append((x, y))
        return len(self.xy) - 1

    def _sec(self, d0, d1, k, n):
        d = self.d_fija if self.d_fija is not None else _d_lineal(d0, d1, k, n)
        return i_props(d)

    def _armar(self) -> None:
        nc, nf = self.n_col, self.n_faldon
        # Columnas: de la base al alero, peralte creciendo hacia la rodilla.
        for x in (0.0, LUZ):
            for k in range(1, nc + 1):
                a = self._nodo(x, (k - 1) * H_ALERO / nc)
                b = self._nodo(x, k * H_ALERO / nc)
                A, I = self._sec(D_BASE, D_ALERO, k, nc)
                self.barras.append((a, b, A, I, "col"))
        # Faldones: del alero a la cumbrera, peralte decreciendo.
        for x0, signo in ((0.0, 1.0), (LUZ, -1.0)):
            for k in range(1, nf + 1):
                xa = x0 + signo * (k - 1) * (LUZ / 2.0) / nf
                xb = x0 + signo * k * (LUZ / 2.0) / nf
                za = H_ALERO + abs(xa - x0) * TAN
                zb = H_ALERO + abs(xb - x0) * TAN
                a, b = self._nodo(xa, za), self._nodo(xb, zb)
                A, I = self._sec(D_ALERO, D_CUMBRE, k, nf)
                self.barras.append((a, b, A, I, "din"))

    # --- puntos de interes ---
    @property
    def n_base_a(self) -> int:
        return self._nodo(0.0, 0.0)

    @property
    def n_alero_a(self) -> int:
        return self._nodo(0.0, H_ALERO)

    @property
    def n_alero_b(self) -> int:
        return self._nodo(LUZ, H_ALERO)

    @property
    def n_cumbrera(self) -> int:
        return self._nodo(LUZ / 2.0, H_ALERO + FLECHA)

    def largo(self, b) -> float:
        (x1, y1), (x2, y2) = self.xy[b[0]], self.xy[b[1]]
        return math.hypot(x2 - x1, y2 - y1)

    # --- cargas ---
    def w_gravedad(self, b) -> float:
        """Carga uniforme de G3A_B sobre la barra, por unidad de largo, hacia abajo."""
        A, tipo = b[2], b[4]
        w = 1.2 * RHO * A * G_ACC                       # peso propio, x1,2
        if tipo == "din":
            L, Lh = self.largo(b), abs(self.xy[b[1]][0] - self.xy[b[0]][0])
            w += 1.2 * D_TECHO * TRIB                    # muerta de techo, por largo
            w += 1.6 * S_BAL * TRIB * Lh / L             # nieve, por PROYECCION
        else:
            w += 1.2 * D_MURO * TRIB
        return w

    def masas(self) -> dict[int, float]:
        """Masa sismica D + 0,20·S concentrada en nudos [t]."""
        m: dict[int, float] = {}
        for b in self.barras:
            A, tipo = b[2], b[4]
            L = self.largo(b)
            W = RHO * A * G_ACC * L
            if tipo == "din":
                Lh = abs(self.xy[b[1]][0] - self.xy[b[0]][0])
                W += D_TECHO * TRIB * L + 0.20 * S_BAL * TRIB * Lh
            else:
                W += D_MURO * TRIB * L
            for n in (b[0], b[1]):
                m[n] = m.get(n, 0.0) + W / G_ACC / 2.0
        return m

    def fuerzas_laterales(self) -> dict[int, float]:
        """1 kN total, repartido en proporcion a la masa de los nudos LIBRES."""
        m = self.masas()
        bases = {self._nodo(0.0, 0.0), self._nodo(LUZ, 0.0)}
        libres = {n: v for n, v in m.items() if n not in bases}
        tot = sum(libres.values())
        return {n: H_LATERAL * v / tot for n, v in libres.items()}


# ====================== CAMINO 1: numpy puro =======================
def resolver_ref(mc: Marco) -> dict[str, float]:
    coords = np.array(mc.xy)
    bases = {mc._nodo(0.0, 0.0): (True, True, False),
             mc._nodo(LUZ, 0.0): (True, True, False)}

    # Gravedad. Los ejes locales de ref.py son x a lo largo de la barra e y a 90°
    # antihorario, o sea (c, s) y (−s, c). Una carga global (0, −w) se proyecta
    # como transversal −w·c y **axial** −w·s. La axial hay que ponerla: en la
    # columna es la unica que hay, y sin ella su peso desaparece del modelo.
    barras_g = []
    for b in mc.barras:
        (x1, y1), (x2, y2) = mc.xy[b[0]], mc.xy[b[1]]
        L = math.hypot(x2 - x1, y2 - y1)
        c, s = (x2 - x1) / L, (y2 - y1) / L
        w = mc.w_gravedad(b)
        barras_g.append(Barra2D(b[0], b[1], E_STEEL, b[2], b[3], w=-w * c, wx=-w * s))
    rg = Portico2D(coords, barras_g, bases).resolver()

    # Lateral.
    barras_0 = [Barra2D(b[0], b[1], E_STEEL, b[2], b[3]) for b in mc.barras]
    cargas = {n: (f, 0.0, 0.0) for n, f in mc.fuerzas_laterales().items()}
    rl = Portico2D(coords, barras_0, bases, cargas).resolver()

    # Modal.
    T = Portico2D(coords, barras_0, bases).periodos(mc.masas(), 3)

    # Momentos: el de la rodilla es el del extremo j de la ultima barra de la
    # columna A; el de cumbrera, el del extremo j de la ultima del faldon A.
    i_col_a = mc.n_col - 1
    i_din_a = 2 * mc.n_col + mc.n_faldon - 1
    return {
        "T1": T[0],
        "dx_alero": abs(rl.desplazamiento(mc.n_alero_a, 0)),
        "dz_cumbrera": abs(rg.desplazamiento(mc.n_cumbrera, 1)),
        "M_alero": abs(rg.momento_extremos(i_col_a)[1]),
        "M_cumbrera": abs(rg.momento_extremos(i_din_a)[1]),
    }


# ==================== CAMINO 2: rukan / OpenSees ===================
def resolver_ops(mc: Marco) -> dict[str, float]:
    nodos, secs, els = [], [], []
    bases = {mc._nodo(0.0, 0.0), mc._nodo(LUZ, 0.0)}
    for k, (x, y) in enumerate(mc.xy):
        restr = (True, True, True, False, False, True) if k in bases else (False,) * 6
        nodos.append(Node(k + 1, x, 0.0, y, restr))
    for k, b in enumerate(mc.barras):
        secs.append(Section(k + 1, A=b[2], Iy=b[3], Iz=b[3], J=1.0))
        els.append(FrameElement(k + 1, b[0] + 1, b[1] + 1, 1, k + 1, (0.0, 1.0, 0.0)))
    mat = [Material(1, E=E_STEEL, nu=NU, rho=RHO)]

    def montar(masas=None):
        m = Model(nodos, mat, secs, els, masas or [])
        build(m)
        # El marco es plano: se bloquean los GDL fuera de plano.
        for n in nodos:
            if n.id not in {k + 1 for k in bases}:
                ops.fix(n.id, 0, 1, 0, 1, 0, 1)
        return m

    def estatico(aplicar):
        montar()
        ops.timeSeries("Linear", 1)
        ops.pattern("Plain", 1, 1)
        aplicar()
        ops.system("BandGeneral")
        ops.numberer("RCM")
        ops.constraints("Transformation")
        ops.integrator("LoadControl", 1.0)
        ops.algorithm("Linear")
        ops.analysis("Static")
        ops.analyze(1)

    # Gravedad: carga global (0,0,-w) proyectada a ejes locales.
    def cargas_g():
        for k, b in enumerate(mc.barras):
            (x1, y1), (x2, y2) = mc.xy[b[0]], mc.xy[b[1]]
            L = math.hypot(x2 - x1, y2 - y1)
            c, s = (x2 - x1) / L, (y2 - y1) / L
            w = mc.w_gravedad(b)
            # ex = (c,0,s); con vecxz = (0,1,0) -> ey = (s,0,-c), ez = (0,1,0).
            ops.eleLoad("-ele", k + 1, "-type", "-beamUniform",
                        (-w) * (-c), 0.0, (-w) * s)

    estatico(cargas_g)
    dz = abs(ops.nodeDisp(mc.n_cumbrera + 1, 3))
    i_col_a, i_din_a = mc.n_col, 2 * mc.n_col + mc.n_faldon
    m_alero = abs(ops.eleResponse(i_col_a, "localForces")[11])
    m_cumbrera = abs(ops.eleResponse(i_din_a, "localForces")[11])

    estatico(lambda: [ops.load(n + 1, f, 0, 0, 0, 0, 0)
                      for n, f in mc.fuerzas_laterales().items()])
    dx = abs(ops.nodeDisp(mc.n_alero_a + 1, 1))

    from rukan.model import NodalMass
    montar([NodalMass(n + 1, (m, m, m, 0.0, 0.0, 0.0)) for n, m in mc.masas().items()])
    T1 = 2.0 * math.pi / math.sqrt(ops.eigen("-fullGenLapack", 1)[0])

    return {"T1": T1, "dx_alero": dx, "dz_cumbrera": dz,
            "M_alero": m_alero, "M_cumbrera": m_cumbrera}


# ================================ MAIN =============================
def main() -> None:
    print("Nota 06 - El marco de peralte variable: prismatizar o discretizar")
    print(f"  Luz {LUZ} m · pendiente {PEND}° · alero {H_ALERO} m · flecha {FLECHA:.3f} m")
    print(f"  Tapered columna {D_BASE * 1e3:.0f}->{D_ALERO * 1e3:.0f} mm ·"
          f" dintel {D_ALERO * 1e3:.0f}->{D_CUMBRE * 1e3:.0f} mm"
          f" · alas {BF * 1e3:.0f}x{TF * 1e3:.0f}, alma {TW * 1e3:.0f}")
    print(f"  Ancho tributario {TRIB} m · bases articuladas\n")

    # ---- 1. Los dos caminos tienen que dar lo mismo ----
    mc = Marco(*N_MODELO)
    ref, opsr = resolver_ref(mc), resolver_ops(mc)
    reportar("Los dos caminos, sobre la malla del modelo (4 tramos de columna, 3 por faldon)", [
        Fila("Periodo fundamental", "s", ref=ref["T1"], ops=opsr["T1"]),
        Fila("Deriva de alero (H = 1 kN)", "mm",
             ref=ref["dx_alero"] * 1e3, ops=opsr["dx_alero"] * 1e3),
        Fila("Flecha de cumbrera (G3A_B)", "mm",
             ref=ref["dz_cumbrera"] * 1e3, ops=opsr["dz_cumbrera"] * 1e3),
        Fila("Momento de alero (G3A_B)", "kN·m",
             ref=ref["M_alero"], ops=opsr["M_alero"]),
        Fila("Momento de cumbrera (G3A_B)", "kN·m",
             ref=ref["M_cumbrera"], ops=opsr["M_cumbrera"]),
    ])

    # ---- 2. El prismatico equivalente ----
    print("\n  El prismatico equivalente contra el tapered (malla fina, N = %d):" % N_REF)
    base = resolver_ref(Marco(N_REF, N_REF))
    filas = [("tapered 350<->800", base)]
    for d in (D_BASE, (D_BASE + D_ALERO) / 2.0, D_ALERO):
        filas.append(("prismatico d = %.0f mm" % (d * 1e3),
                      resolver_ref(Marco(N_REF, N_REF, d_fija=d))))
    print(f"    {'variante':24s} {'T1 [s]':>9s} {'dx alero':>10s} {'M alero':>10s} "
          f"{'M cumbrera':>11s}")
    for nm, r in filas:
        print(f"    {nm:24s} {r['T1']:9.6f} {r['dx_alero'] * 1e3:10.4f} "
              f"{r['M_alero']:10.3f} {r['M_cumbrera']:11.3f}")
    print(f"    {'':24s} {'':>9s} {'[mm]':>10s} {'[kN·m]':>10s} {'[kN·m]':>11s}")

    print("\n    Diferencia del prismatico respecto del tapered:")
    for nm, r in filas[1:]:
        print(f"    {nm:24s} M alero {(r['M_alero'] / base['M_alero'] - 1) * 100:+7.1f} %"
              f"   M cumbrera {(r['M_cumbrera'] / base['M_cumbrera'] - 1) * 100:+7.1f} %")

    # ---- 3. Convergencia de la malla ----
    print(f"\n  Convergencia de la discretizacion (referencia N = {N_REF}):")
    print(f"    {'N':>3s} {'T1':>10s} {'flecha cumbrera':>17s} {'deriva de alero':>17s}")
    conv = {}
    for n in (1, 2, 3, 4, 6, 9, 12):
        r = resolver_ref(Marco(n, n))
        conv[n] = r
        print(f"    {n:3d} {(r['T1'] / base['T1'] - 1) * 100:+9.2f} %"
              f" {(r['dz_cumbrera'] / base['dz_cumbrera'] - 1) * 100:+16.2f} %"
              f" {(r['dx_alero'] / base['dx_alero'] - 1) * 100:+16.2f} %")

    # ---- asserts ----
    for n in (1, 2, 4):
        r = resolver_ops(Marco(n, n))
        s = conv[n]
        for k in ("T1", "dx_alero", "dz_cumbrera"):
            assert abs(r[k] / s[k] - 1) < 1e-9, (n, k, r[k], s[k])
    # La deriva converge mas lento que la flecha: es el hallazgo.
    e_flecha = abs(conv[1]["dz_cumbrera"] / base["dz_cumbrera"] - 1)
    e_deriva = abs(conv[1]["dx_alero"] / base["dx_alero"] - 1)
    assert e_deriva > 5.0 * e_flecha, (e_deriva, e_flecha)
    # Ningun prismatico reproduce las dos estaciones a la vez.
    for _, r in filas[1:]:
        peor = max(abs(r["M_alero"] / base["M_alero"] - 1),
                   abs(r["M_cumbrera"] / base["M_cumbrera"] - 1))
        assert peor > 0.15, peor

    print("\n  OK - los dos caminos coinciden, y ningun prismatico equivalente"
          " reproduce\n     el momento de alero y el de cumbrera a la vez.")


if __name__ == "__main__":
    main()
