"""Nota 02 — `Mp = Z·Fy` es una asíntota que nunca se toca.

**La pregunta:** el momento plástico de una sección se escribe `Mp = Z·Fy` y se
usa como si fuera un valor que la sección alcanza. ¿A qué curvatura lo alcanza?

**El caso:** perfil H soldado de galpón, flexión pura, material elastoplástico
perfecto. La sección se define por sus planchas —no por una tabla de perfiles—
así que todas las propiedades salen de la geometría declarada:

    ala 200 × 12 mm     alma 6 mm     alto total 400 mm
    Fy = 250 MPa        E = 200 GPa

**La fórmula cerrada.** Con `d = h/2` la semialtura y `a = d − tf` el borde
interior del ala, el núcleo elástico a curvatura φ tiene semiprofundidad
`c = ε_y/φ`. Escribiendo M como déficit respecto del bloque totalmente
plastificado::

    M(φ) = Mp − 2·Fy·∫₀^c (1 − y/c)·y·b(y) dy

    c ≤ a:      M = Fy·[ Z − tw·c²/3 ]
    a < c < d:  M = Fy·[ Z − 2( tw(a²/2 − a³/3c) + bf((c²−a²)/2 − c²/3 + a³/3c) ) ]
    c ≥ d:      M = E·I·φ

Los tramos empalman en `c = a`, y en `c = d` el segundo se reduce a `Fy·S = My`.
La derivación completa está en `SeccionI` (`lab/_lib/ref.py`): es mecánica de
sección —equilibrio, Navier y la ley constitutiva—, no una disposición
normativa, así que se deriva y queda auditable en vez de citarse.

**Las tres cosas que muestra la nota**

1. `Mp` **no se alcanza a curvatura finita**. El núcleo elástico mide
   `c = ε_y/φ > 0` para todo φ, así que siempre queda material sin plastificar
   y el déficit decae como 1/φ². Mp es el límite, no un valor.

2. Pero en un perfil I la asíntota es **benigna**: a 2 φ_y ya hay 98,3 % de Mp,
   y a 5 φ_y, 99,7 %. Un rectángulo macizo a las mismas curvaturas va en 91,7 %
   y 98,7 %. La diferencia es el factor de forma —1,103 contra 1,500—: el I ya
   puso el material en las alas, así que le queda poco por redistribuir. Esa es
   la razón de fondo por la que el diseño en acero usa Mp sin pedir disculpas.

3. De paso, sobre secciones de fibras: `Σ Aᵢ·yᵢ` reproduce **exactamente**
   `∫y dA` cuando cada fibra está en el centroide de su franja, así que **Mp
   sale exacto con una sola fibra por ala** — salvo que el alma lleve un número
   *impar* de fibras, porque entonces la franja central cruza el eje neutro y
   `|y|` deja de ser lineal ahí: con una fibra de alma, Mp sale 19 % bajo. En
   cambio `Σ Aᵢ·yᵢ²` **nunca** reproduce `∫y² dA` —falta el Steiner `b·t³/12`
   de cada franja—, y el déficit lo manda el **alma**, no el ala. Refinar el ala
   de 1 a 20 fibras mueve la rigidez en 0,03 %.

**Verificación (los dos caminos):** referencia = fórmula cerrada derivada e
integración de fibras en numpy (`lab/_lib/ref.py`, sin importar `rukan` ni
`openseespy`); motor = OpenSeesPy con `section Fiber` y `zeroLengthSection`.

Correr::

    python -m lab.nota02_momento_curvatura_acero
"""

from __future__ import annotations

import numpy as np
import openseespy.opensees as ops

from lab._lib import svg
from lab._lib.ref import SeccionI, discretizar_I
from lab._lib.report import Fila, reportar
from rukan import units as u

# ============================ DATOS DE ENTRADA ============================
# La frontera Pint: se define con unidades y se baja al sistema interno (kN, m).
BF = 200 * u.ureg.mm  # ancho del ala
TF = 12 * u.ureg.mm  # espesor del ala
TW = 6 * u.ureg.mm  # espesor del alma
H = 400 * u.ureg.mm  # alto total, alas incluidas
FY = 250 * u.ureg.MPa
E = 200 * u.ureg.GPa

BF_ = u.length(BF)
TF_ = u.length(TF)
TW_ = u.length(TW)
H_ = u.length(H)
FY_ = u.stress(FY)
E_ = u.stress(E)

EPS_Y = FY_ / E_

# ======================= REFERENCIA: FÓRMULA CERRADA =======================
SEC = SeccionI(bf=BF_, tf=TF_, tw=TW_, h=H_)
# Rectángulo macizo del mismo ancho y alto: el caso degenerado tf = h/2.
REC = SeccionI(bf=BF_, tf=H_ / 2, tw=TW_, h=H_)

PHI_Y = SEC.phi_y(FY_, E_)
MP = FY_ * SEC.Z
MY = FY_ * SEC.S

# Malla de referencia del motor. El alma es par (si no, Z sale mal) y bastante
# fina: con 40 fibras de alma la rigidez queda a 0,008 % de la exacta.
N_ALA, N_ALMA = 20, 40

# Curvatura a la que una malla queda *toda* plastificada: la fibra más interna
# está en a/n_alma, así que φ_plena = ε_y·n_alma/a. Pasado ese punto la rigidez
# tangente es cero y el sistema es singular — los análisis se quedan más acá.
PHI_PLENA_REF = EPS_Y / (SEC.a / N_ALMA)


# ============================== OPENSEES ==================================
def _montar(n_ala: int, n_alma: int) -> None:
    """Sección de fibras del perfil H sobre un `zeroLengthSection`.

    Dos nodos coincidentes: el 1 empotrado y el 2 libre solo en rotación. La
    sección es doblemente simétrica y el caso es flexión pura, así que no hay
    carga axial que aplicar y se fija también el GDL axial.
    """
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)
    ops.node(1, 0.0, 0.0)
    ops.node(2, 0.0, 0.0)
    ops.fix(1, 1, 1, 1)
    ops.fix(2, 1, 1, 0)

    # ElasticPP nombra exactamente la ley que asume la fórmula cerrada:
    # elastoplástico perfecto, sin endurecimiento.
    ops.uniaxialMaterial("ElasticPP", 1, E_, EPS_Y)

    d, a = SEC.d, SEC.a
    z = BF_ / 2.0
    ops.section("Fiber", 1)
    # patch('rect', mat, nSubdivY, nSubdivZ, yI, zI, yJ, zJ)
    ops.patch("rect", 1, n_ala, 1, -d, -z, -a, z)  # ala inferior
    ops.patch("rect", 1, n_alma, 1, -a, -TW_ / 2, a, TW_ / 2)  # alma
    ops.patch("rect", 1, n_ala, 1, a, -z, d, z)  # ala superior

    ops.element("zeroLengthSection", 1, 1, 2, 1)


def momento_curvatura(phi_max: float, n_incr: int = 400,
                      n_ala: int = N_ALA, n_alma: int = N_ALMA) -> tuple:
    """Empuja la sección por control de curvatura y devuelve (φ, M).

    En un `zeroLengthSection` la deformación de la sección *es* el
    desplazamiento relativo de los nodos: `nodeDisp(2, 3)` es la curvatura y
    `sectionForce(1, 1, 2)` el momento.
    """
    _montar(n_ala, n_alma)
    ops.timeSeries("Linear", 1)
    ops.pattern("Plain", 1, 1)
    ops.load(2, 0.0, 0.0, 1.0)

    ops.system("BandGeneral")
    ops.numberer("Plain")
    ops.constraints("Plain")
    ops.test("NormUnbalance", 1e-10, 20)
    ops.algorithm("Newton")
    ops.integrator("DisplacementControl", 2, 3, phi_max / n_incr)
    ops.analysis("Static")

    phis, momentos = [0.0], [0.0]
    for _ in range(n_incr):
        if ops.analyze(1) != 0:
            raise RuntimeError(
                f"El análisis no convergió en φ = {phis[-1]:.5f} 1/m. "
                "¿La malla quedó totalmente plastificada (rigidez tangente nula)?"
            )
        phis.append(ops.nodeDisp(2, 3))
        momentos.append(ops.sectionForce(1, 1, 2))
    return np.array(phis), np.array(momentos)


def momento_ops(phi_objetivo: float, n_ala: int = N_ALA,
                n_alma: int = N_ALMA) -> float:
    """Momento de OpenSees a una curvatura dada, alcanzada en 200 pasos."""
    phis, momentos = momento_curvatura(phi_objetivo, 200, n_ala, n_alma)
    return float(momentos[-1])


# ============================== LA NOTA ===================================
def main() -> None:
    print("# Nota 02 — Mp = Z·Fy es una asíntota\n")
    print(f"Perfil H soldado: ala {BF_ * 1e3:.0f}×{TF_ * 1e3:.0f}, "
          f"alma {TW_ * 1e3:.0f}, alto {H_ * 1e3:.0f} mm — "
          f"Fy = {FY_ / 1e3:.0f} MPa, E = {E_ / 1e6:.0f} GPa\n")
    print(f"Malla del motor: {N_ALA} fibras por ala, {N_ALMA} en el alma.\n")

    # --- 1. La sección: el motor reproduce las propiedades exactas --------
    phis, momentos = momento_curvatura(0.5 * PHI_Y, 20)
    ei_ops = float(momentos[-1] / phis[-1])
    reportar(
        "1. La sección: la malla del motor reproduce lo exacto",
        [
            Fila("Rigidez a flexión EI", "kN·m²", ref=E_ * SEC.I, ops=ei_ops),
            Fila("Momento a la primera fluencia My", "kN·m",
                 ref=MY, ops=momento_ops(PHI_Y)),
        ],
        ref_label="Geometría exacta",
        nota=("EI se mide en el tramo elástico (φ = 0,5 φ_y) y My en la "
              "curvatura de primera fluencia."),
    )

    print("\nPropiedades de la geometría declarada:\n")
    print(f"  Z  = {SEC.Z * 1e9:>12,.0f} mm³        Mp = Fy·Z = {MP:7.1f} kN·m")
    print(f"  S  = {SEC.S * 1e9:>12,.0f} mm³        My = Fy·S = {MY:7.1f} kN·m")
    print(f"  I  = {SEC.I * 1e12:>12,.0f} mm⁴        φ_y = {PHI_Y:.5f} 1/m")
    print(f"  Z/S = {SEC.factor_forma:.4f}   → entre My y Mp queda un "
          f"{(SEC.factor_forma - 1) * 100:.1f} % de momento.")

    # --- 2. La asíntota ---------------------------------------------------
    razones = [1.0, 1.5, 2.0, 5.0, 10.0]
    reportar(
        "2. Mp no se alcanza: se aproxima",
        [
            Fila(f"M/Mp a φ = {r:.1f} φ_y", "", ref=SEC.momento(r * PHI_Y, FY_, E_) / MP,
                 ops=momento_ops(r * PHI_Y) / MP)
            for r in razones
        ],
        ref_label="Fórmula cerrada",
        nota=("El déficit decae como 1/φ²: el núcleo elástico mide c = ε_y/φ y "
              "nunca desaparece, así que Mp es el límite, no un valor que la "
              "sección alcance."),
    )

    # --- El rectángulo, para contraste ------------------------------------
    phi_y_rec = REC.phi_y(FY_, E_)
    mp_rec = FY_ * REC.Z
    print(f"\nEl mismo cálculo en un rectángulo macizo de "
          f"{BF_ * 1e3:.0f} × {H_ * 1e3:.0f} mm, cerrado en las dos secciones:\n")
    print("  φ/φ_y      H soldado    rectángulo")
    for r in (1.0, 2.0, 5.0, 10.0):
        print(f"   {r:4.1f}       {SEC.momento(r * PHI_Y, FY_, E_) / MP:.4f}       "
              f"{REC.momento(r * phi_y_rec, FY_, E_) / mp_rec:.4f}")
    print(f"\n  factor de forma Z/S:  {SEC.factor_forma:.4f}  vs  "
          f"{REC.factor_forma:.4f}")
    print("\nEl rectángulo tarda mucho más porque tiene mucho material cerca del")
    print("eje neutro, que a curvatura baja aporta poca tensión. El I ya lo puso")
    print("en las alas: le queda poco por redistribuir, y por eso llega rápido.")

    # --- 4. Mp sale exacto con una fibra por ala --------------------------
    mallas_par = [(1, 2), (2, 8), (4, 16), (20, 40)]
    reportar(
        "3. Mp de la malla es exacto con una sola fibra por ala",
        [
            Fila(f"Z de la malla {na}×{nw}", "mm³",
                 ref=SEC.Z * 1e9,
                 ops=discretizar_I(SEC, na, nw).Z_fib * 1e9,
                 tol_pct=1e-9, decimales=1)
            for na, nw in mallas_par
        ],
        ref_label="Z exacto",
        ops_label="Suma de fibras",
        nota=("Una fibra rectangular en el centroide de su franja reproduce "
              "`∫y dA` **exactamente**: A·y_c = b(y₂²−y₁²)/2. Como Mp = Fy·Z, "
              "refinar la malla no compra un gramo de resistencia."),
    )

    # --- 4. …salvo que el alma sea impar ----------------------------------
    filas_impar = []
    for nw in (1, 3, 5, 9):
        malla = discretizar_I(SEC, 4, nw)
        fibra = "fibra" if nw == 1 else "fibras"
        filas_impar.append(
            Fila(f"Z con {nw} {fibra} de alma", "mm³",
                 ref=SEC.Z * 1e9, ops=malla.Z_fib * 1e9,
                 tol_pct=100.0, decimales=1)
        )
    reportar(
        "4. …salvo que el alma lleve un número impar de fibras",
        filas_impar,
        ref_label="Z exacto",
        ops_label="Suma de fibras",
        nota=("Acá la tolerancia está abierta a propósito: la tabla mide el "
              "error, no lo acota. Con alma impar la franja central cruza el "
              "eje neutro, y ahí `|y|` no es lineal — la exactitud se pierde. "
              "Con **una** fibra de alma, Mp sale 19 % bajo."),
    )

    # --- La rigidez sí depende de la malla, y la manda el alma ------------
    print("\nLo que la malla sí cambia es la rigidez. A cada franja le falta su")
    print("término de Steiner b·t³/12, así que Σ Aᵢyᵢ² < ∫y² dA siempre:\n")
    print("  malla (ala×alma)     I_malla/I")
    for na, nw in [(1, 2), (20, 2), (1, 8), (1, 40), (20, 40)]:
        print(f"    {na:2d} × {nw:2d}            "
              f"{discretizar_I(SEC, na, nw).I_fib / SEC.I:.5f}")
    print("\nRefinar el ala de 1 a 20 fibras no mueve la aguja; refinar el alma")
    print("de 2 a 40, sí. El déficit lo dominan las franjas más altas.")

    # --- 5. Los dos caminos de fibras, uno contra otro --------------------
    filas_caminos = []
    for na, nw in [(2, 8), (4, 16), (8, 32), (20, 40)]:
        malla = discretizar_I(SEC, na, nw)
        filas_caminos.append(
            Fila(f"M a 5 φ_y con malla {na}×{nw}", "kN·m",
                 ref=malla.momento(5.0 * PHI_Y, FY_, E_),
                 ops=momento_ops(5.0 * PHI_Y, na, nw),
                 tol_pct=1e-6)
        )
    reportar(
        "5. Los dos caminos, uno contra otro",
        filas_caminos,
        ref_label="Fibras en numpy",
        nota=("La suma de fibras en numpy predice lo que da el motor malla por "
              "malla, así que la brecha contra la fórmula cerrada es "
              "discretización y no un problema del motor."),
    )


# ============================== FIGURAS ===================================
def figuras() -> None:
    _fig_asintota()
    _fig_malla()


def _fig_asintota() -> None:
    razones = np.linspace(0.02, 6.0, 240)
    curva_i = [SEC.momento(r * PHI_Y, FY_, E_) / MP for r in razones]

    phi_y_rec = REC.phi_y(FY_, E_)
    mp_rec = FY_ * REC.Z
    curva_rec = [REC.momento(r * phi_y_rec, FY_, E_) / mp_rec for r in razones]

    phis, momentos = momento_curvatura(6.0 * PHI_Y, 240)

    lienzo = svg.Lienzo(
        alto=330,
        titulo="Mp es una asíntota — pero un perfil I la toca casi de inmediato",
        subtitulo="H soldado 400×200, elastoplástico perfecto, flexión pura",
    )
    ejes = lienzo.ejes(
        x=(0.0, 6.0), y=(0.0, 1.1),
        etiqueta_x="curvatura φ/φ_y",
        etiqueta_y="M/Mp",
        ticks_x=6, ticks_y=5,
    )
    ejes.curva([0.0, 6.0], [1.0, 1.0], color=svg.GRIS, ancho=1.5, guion="6 4")
    ejes.curva(razones, curva_rec, color=svg.VERDE, ancho=1.8)
    ejes.curva(razones, curva_i, color=svg.AZUL, ancho=2.4)
    # El motor, muestreado: si cayera fuera de la curva azul se vería.
    for k in range(12, len(phis), 24):
        lienzo.circulo(ejes.x(phis[k] / PHI_Y), ejes.y(momentos[k] / MP), 2.8,
                       color=svg.ROJO)

    m_2 = SEC.momento(2.0 * PHI_Y, FY_, E_) / MP
    ejes.marcar(2.0, m_2, f"{m_2:.3f} Mp", color=svg.AZUL, dx=8, dy=-8)
    m_2r = REC.momento(2.0 * phi_y_rec, FY_, E_) / mp_rec
    ejes.marcar(2.0, m_2r, f"{m_2r:.3f} Mp", color=svg.VERDE, dx=8, dy=16)
    lienzo.texto(ejes.x(6.0), ejes.y(1.0) - 8, "Mp = Z·Fy", tam=10.5,
                 color=svg.TENUE, anclaje="end")

    # Abajo a la derecha: la zona que ninguna de las dos curvas cruza.
    lienzo.leyenda(250, 196, [
        (svg.AZUL, "H soldado, cerrada (Z/S = 1.103)"),
        (svg.VERDE, "rectángulo macizo (Z/S = 1.500)"),
        (svg.ROJO, "OpenSees, sección de fibras"),
    ])
    lienzo.guardar("lab/figs/nota02-asintota.svg")


def _fig_malla() -> None:
    ns = list(range(1, 41))
    z_par = [(n, discretizar_I(SEC, 4, n).Z_fib / SEC.Z) for n in ns if n % 2 == 0]
    z_impar = [(n, discretizar_I(SEC, 4, n).Z_fib / SEC.Z) for n in ns if n % 2]
    inercias = [discretizar_I(SEC, 4, n).I_fib / SEC.I for n in ns]

    lienzo = svg.Lienzo(
        alto=330,
        titulo="La malla no te da resistencia: te quita rigidez",
        subtitulo="propiedades de la malla contra las exactas, 4 fibras por ala",
    )
    ejes = lienzo.ejes(
        x=(0, 40), y=(0.80, 1.02),
        etiqueta_x="fibras en el alma",
        etiqueta_y="valor de la malla / valor exacto",
        ticks_x=8, ticks_y=11,
    )
    ejes.curva([0, 40], [1.0, 1.0], color=svg.GRIS, ancho=1.2, guion="4 4")
    ejes.curva(ns, inercias, color=svg.ROJO, ancho=2.2)
    ejes.curva([n for n, _ in z_par], [v for _, v in z_par], color=svg.AZUL,
               ancho=2.4)
    ejes.curva([n for n, _ in z_impar], [v for _, v in z_impar], color=svg.VERDE,
               ancho=1.6, guion="3 3")
    for n, v in z_impar[:5]:
        lienzo.circulo(ejes.x(n), ejes.y(v), 2.8, color=svg.VERDE)

    ejes.marcar(1, z_impar[0][1], "1 fibra de alma: Mp 19 % bajo",
                color=svg.VERDE, dx=10, dy=4)
    lienzo.leyenda(262, 200, [
        (svg.AZUL, "Z (→ Mp), alma par — exacto siempre"),
        (svg.VERDE, "Z (→ Mp), alma impar"),
        (svg.ROJO, "I (→ rigidez) — nunca exacto"),
    ])
    lienzo.guardar("lab/figs/nota02-malla.svg")


if __name__ == "__main__":
    main()
    figuras()
    print("\nFiguras escritas en lab/figs/nota02-*.svg")
