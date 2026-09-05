"""Nota 07 — El diagrama que la barra no reporta, ahora en 3D y con seis componentes.

**La pregunta:** la `nota01` mostró que el momento del vano no está en la salida
del elemento y que interpolar entre los extremos cambia de signo. Eso era una
viga plana y un solo componente. En 3D hay **seis** —N, Vy, Vz, T, My, Mz—, dos
planos de flexión y una torsión. ¿Cuáles son las funciones, y cómo se sabe que
sus signos están bien sin otro programa contra el cual medirlos?

**Lo que OpenSees entrega, y lo que no.** Sobre un `elasticBeamColumn`,
`eleResponse(tag, "sectionX", perc)`, `"section"` e `"integrationPoints"`
devuelven `[]`. Lo único que hay son las doce fuerzas de extremo (`localForces`)
y las seis básicas. Las respuestas `sectionI` / `sectionC` / `sectionJ` /
`sectionX` que documenta OpenSeesPy pertenecen a `pipe` y `curvedPipe`, no al
elemento de barra elástica. La superposición la tiene que hacer uno.

**El caso:** un rafter inclinado de 7,5 m, empotrado en el extremo i y con una
rótula esférica en el j, bajo carga uniforme en las tres direcciones locales —el
peso propio proyectado a los ejes de la barra da componente axial y transversal;
una fuerza lateral de arrastre da la tercera— más un torsor de montaje en el
extremo libre. Con eso los seis componentes están vivos a la vez.

**Las funciones.** Con `S = eleResponse(tag, "localForces")` —las fuerzas que los
nudos aplican a la barra— y `w = (wx, wy, wz)` en ejes locales::

    N(x)  = −S₀ − wx·x                    Mz(x) = S₅ − S₁·x − wy·x²/2
    Vy(x) = −S₁ − wy·x                    My(x) = S₄ + S₂·x + wz·x²/2
    Vz(x) = −S₂ − wz·x
    T(x)  = −S₃

La asimetría entre `Mz` y `My` —el `−S₁·x` contra el `+S₂·x`— no es un descuido:
los ejes son dextrógiros, `ex × ey = ez` pero `ex × ez = −ey`.

**Los tres caminos.**

1. `rukan.esfuerzos` — la fórmula cerrada, que es lo que se verifica.
2. `lab/_lib/ref.py` · `diagrama_por_integracion` — numpy puro: equilibrio del
   cuerpo libre `[0, x]` con la carga repartida en rebanadas y productos
   cruzados, **sin** escribir el cuadrático ni usar `dM/dx = V`.
3. OpenSees con la barra mallada en dieciséis — otro solve, otro sistema de
   ecuaciones, cuyos nudos interiores muestrean el mismo campo continuo. Es
   exacto y no asintótico, por lo que la `nota01` estableció: la solución de
   elementos finitos de una viga prismática con carga uniforme es exacta en los
   nudos, así que mallar no converge, muestrea.

**El punto que la nota deja escrito.** El signo del corte no se elige por
analogía con la axial. Si `Mz(x)` está anclado en sus dos extremos a una
convención de momento verificada contra SAP2000, entonces `dMz/dx` **determina**
el signo de `Vy`, y `dMy/dx` el de `Vz` con el signo opuesto. Lo único que queda
sin ese anclaje es la **torsión**: no tiene diagrama del cual derivarse.

Correr::

    python -m lab.nota07_esfuerzos_en_el_vano
"""

from __future__ import annotations

import math

import numpy as np
import openseespy.opensees as ops

from lab._lib import svg
from lab._lib.ref import COMPONENTES_LOCALES, diagrama_por_integracion
from lab._lib.report import Fila, reportar
from rukan import esfuerzos
from rukan import units as u

# ============================ DATOS DE ENTRADA ============================
# La frontera Pint: se define con unidades y se baja al sistema interno (kN, m).
PI = (0.0, 0.0, 0.0)
PJ = (6.0, 0.0, 4.5)          # rafter de 20 % de pendiente
L_ = math.dist(PI, PJ)        # 7,50 m
VECXZ = (0.0, 1.0, 0.0)       # el eje local z queda sobre el Y global

E_ = u.stress(200 * u.ureg.GPa)
G_ = u.stress(77 * u.ureg.GPa)
A_ = u.area(120 * u.ureg.cm**2)
IY_ = u.inertia(4_500 * u.ureg.cm**4)
IZ_ = u.inertia(48_000 * u.ureg.cm**4)
J_ = u.inertia(95 * u.ureg.cm**4)

# Carga de vano en **ejes locales**, kN/m. La axial y la transversal en el plano
# del faldón son el peso propio proyectado; la tercera, un arrastre lateral.
W_LOCAL = (-0.72, 0.96, 0.35)
T_J = 4.8      # kN·m, torsor de montaje en el extremo libre

# Estaciones donde se compara, y una interior arbitraria para la tabla.
N_EST = 9
XS = [k * L_ / (N_EST - 1) for k in range(N_EST)]
X_INT = 0.35 * L_
N_MALLA = 16


# ============================== OPENSEES ==================================
def _montar(n_elementos: int) -> None:
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    for k in range(n_elementos + 1):
        t = k / n_elementos
        ops.node(k + 1, *[a + t * (b - a) for a, b in zip(PI, PJ)])
    ops.fix(1, 1, 1, 1, 1, 1, 1)                 # empotramiento
    ops.fix(n_elementos + 1, 1, 1, 1, 0, 0, 0)   # rótula esférica
    ops.geomTransf("Linear", 1, *VECXZ)
    for k in range(n_elementos):
        ops.element("elasticBeamColumn", k + 1, k + 1, k + 2,
                    A_, E_, G_, J_, IY_, IZ_, 1)


def modelo(n_elementos: int = 1) -> list[list[float]]:
    """Corre el rafter mallado en ``n_elementos`` y devuelve sus `localForces`.

    La carga de vano va como `eleLoad -beamUniform`, que OpenSees toma en el
    orden ``(Wy, Wz, Wx)`` y no ``(Wx, Wy, Wz)``.
    """
    _montar(n_elementos)
    wx, wy, wz = W_LOCAL
    ops.timeSeries("Constant", 1)
    ops.pattern("Plain", 1, 1)
    for k in range(n_elementos):
        ops.eleLoad("-ele", k + 1, "-type", "-beamUniform", wy, wz, wx)
    # El torsor va sobre el eje local x, que en esta barra apunta (0,8; 0; 0,6).
    ex = [(b - a) / L_ for a, b in zip(PI, PJ)]
    ops.load(n_elementos + 1, 0.0, 0.0, 0.0, *[T_J * c for c in ex])
    ops.system("BandGeneral")
    ops.numberer("Plain")
    ops.constraints("Plain")
    ops.integrator("LoadControl", 1.0)
    ops.algorithm("Linear")
    ops.analysis("Static")
    ops.analyze(1)
    return [list(ops.eleResponse(k + 1, "localForces")) for k in range(n_elementos)]


def cerrada(S: list[float], componente: str, x: float) -> float:
    return esfuerzos.esfuerzo(S, W_LOCAL, L_, componente, x)


def _recta(S: list[float], componente: str, x: float) -> float:
    """Lo que uno dibujaría creyendo que la salida del elemento es el diagrama:
    la recta entre los dos valores de extremo."""
    a = cerrada(S, componente, 0.0)
    b = cerrada(S, componente, L_)
    return a + (b - a) * x / L_


# ============================== LA NOTA ===================================
def main() -> None:
    print("# Nota 07 — El diagrama que la barra no reporta, en 3D\n")
    print(f"Rafter inclinado: L = {L_:.2f} m, "
          f"w local = ({W_LOCAL[0]:+.2f}, {W_LOCAL[1]:+.2f}, {W_LOCAL[2]:+.2f}) kN/m, "
          f"torsor en el extremo = {T_J:.1f} kN·m\n")

    S = modelo(1)[0]
    ref = diagrama_por_integracion(S, W_LOCAL, L_, XS)
    malla = modelo(N_MALLA)

    _tabla_extremos(S)
    _tabla_campo(S, ref)
    _tabla_malla(S, malla)
    _tabla_identidades(S)
    _tabla_recta(S)


def _tabla_extremos(S: list[float]) -> None:
    """Los extremos: la fórmula no inventa nada y empalma con lo publicado."""
    filas = []
    for k, c in enumerate(COMPONENTES_LOCALES):
        unidad = "kN" if c in ("N", "Vy", "Vz") else "kN·m"
        for extremo, x, idx, signo in (("i", 0.0, k, 1.0), ("j", L_, k + 6, -1.0)):
            # El signo del diagrama: i: −, j: + para fuerzas; al revés para los
            # momentos flectores. Es la convención verificada contra SAP2000.
            flector = c in ("My", "Mz")
            s = (1.0 if flector else -1.0) if extremo == "i" else (-1.0 if flector else 1.0)
            filas.append(Fila(f"{c} en el extremo {extremo}", unidad,
                              ref=s * S[idx], ops=cerrada(S, c, x),
                              tol_abs=1e-9 if abs(s * S[idx]) < 1e-6 else None))
    reportar(
        "1. En los extremos, la fórmula da lo que el elemento ya publicaba",
        filas,
        ref_label="Fuerza de extremo × signo del diagrama",
        ops_label="La fórmula en x = 0 y x = L",
        nota=("Es el ancla: la convención de extremo está verificada contra "
              "SAP2000 en los casos 6, 9 y 10, y el diagrama tiene que empalmar "
              "con ella o habría dos convenciones conviviendo."),
    )


def _tabla_campo(S: list[float], ref: np.ndarray) -> None:
    """El campo continuo: la cerrada contra el equilibrio integrado en numpy."""
    k_int = min(range(len(XS)), key=lambda k: abs(XS[k] - X_INT))
    filas = []
    for c, comp in enumerate(COMPONENTES_LOCALES):
        unidad = "kN" if comp in ("N", "Vy", "Vz") else "kN·m"
        filas.append(Fila(f"{comp} en x = {XS[k_int]:.3f} m", unidad,
                          ref=float(ref[k_int, c]),
                          ops=cerrada(S, comp, XS[k_int])))
    peor = max(abs(ref[k, c] - cerrada(S, comp, XS[k]))
               for k in range(len(XS)) for c, comp in enumerate(COMPONENTES_LOCALES))
    reportar(
        "2. Entre los extremos: la cerrada contra el equilibrio, integrado en numpy",
        filas,
        ref_label="Equilibrio del cuerpo libre (numpy)",
        ops_label="La fórmula cerrada",
        nota=(f"La referencia no usa el cuadrático ni `dM/dx = V`: corta la barra "
              f"en `x`, reparte la carga en rebanadas y suma fuerzas y momentos "
              f"con productos cruzados. Sobre las {len(XS)} estaciones y los seis "
              f"componentes, la mayor diferencia es {peor:.2e}."),
    )


def _tabla_malla(S: list[float], malla: list[list[float]]) -> None:
    """La identidad de malla: un elemento contra dieciséis."""
    k = N_MALLA // 3                      # un nudo interior cualquiera
    x = k * L_ / N_MALLA
    filas = []
    for c, comp in enumerate(COMPONENTES_LOCALES):
        unidad = "kN" if comp in ("N", "Vy", "Vz") else "kN·m"
        flector = comp in ("My", "Mz")
        s = 1.0 if flector else -1.0      # extremo i del elemento k
        filas.append(Fila(f"{comp} en x = {x:.3f} m", unidad,
                          ref=s * malla[k][c], ops=cerrada(S, comp, x)))
    reportar(
        f"3. Un elemento contra una malla de {N_MALLA}: el mismo campo continuo",
        filas,
        ref_label=f"Malla de {N_MALLA} (otro solve)",
        ops_label="Un elemento + la fórmula",
        nota=("Es el camino más independiente que hay sin SAP2000: otra malla, "
              "otro sistema de ecuaciones, y sus nudos interiores caen encima "
              "del diagrama del elemento único. Exacto, no asintótico."),
    )


def _tabla_identidades(S: list[float]) -> None:
    """`dMz/dx = +Vy` y `dMy/dx = −Vz`, que es lo que fija el signo del corte."""
    h = L_ / 8.0
    filas = []
    for x in (h, L_ / 2.0, L_ - h):
        dMz = (cerrada(S, "Mz", x + h) - cerrada(S, "Mz", x - h)) / (2 * h)
        dMy = (cerrada(S, "My", x + h) - cerrada(S, "My", x - h)) / (2 * h)
        filas.append(Fila(f"dMz/dx en x = {x:.3f} m", "kN",
                          ref=cerrada(S, "Vy", x), ops=dMz))
        filas.append(Fila(f"−dMy/dx en x = {x:.3f} m", "kN",
                          ref=cerrada(S, "Vz", x), ops=-dMy))
    reportar(
        "4. El signo del corte no se elige: lo fija la derivada del momento",
        filas,
        ref_label="El corte del diagrama",
        ops_label="La derivada del momento",
        nota=("La diferencia central es exacta sobre un cuadrático, así que esto "
              "no tiene error de truncamiento. Con `Mz` anclado en sus extremos a "
              "una convención verificada contra SAP2000, el signo de `Vy` queda "
              "determinado, no elegido por analogía con la axial. La **torsión** "
              "es el único componente sin diagrama del cual derivarse."),
    )


def _tabla_recta(S: list[float]) -> None:
    """Lo que se pierde al creer que la salida del elemento es el diagrama.

    El máximo de ``|Mz|`` cae en el empotramiento y ese sí está en la salida. El
    que no está es el **máximo del vano**, donde el corte se anula: ahí la recta
    entre los extremos no se queda corta, tiene el signo cambiado.
    """
    x_vano = -S[1] / W_LOCAL[1]                      # donde Vy(x) = 0
    assert 0.0 < x_vano < L_, "el corte no se anula dentro de la barra"
    real = cerrada(S, "Mz", x_vano)
    recta = _recta(S, "Mz", x_vano)
    print(f"\nEn x = {x_vano:.3f} m, donde el corte se anula y el momento del "
          f"vano es máximo:\n")
    print(f"  recta entre las fuerzas de extremo   {recta:+9.4f} kN·m")
    print(f"  diagrama real                        {real:+9.4f} kN·m")
    print(f"  lo que la recta no ve                {real - recta:+9.4f} kN·m")
    if real * recta < 0.0:
        print("\nNo es que la recta se quede corta: tiene el signo cambiado.")
    # Los planos de flexión de una barra prismática están desacoplados: en el
    # plano local x-y esta barra **es** la viga apuntalada de la `nota01` con
    # `q = wy`, así que valen sus fórmulas cerradas (Hibbeler; AISC, Tabla 3-22).
    q = W_LOCAL[1]
    reportar(
        "5. Lo que falta en la recta es la parábola de la carga de vano",
        [Fila("Momento en el empotramiento", "kN·m",
              ref=-q * L_**2 / 8.0, ops=cerrada(S, "Mz", 0.0)),
         Fila("Posición del máximo del vano", "m",
              ref=5.0 * L_ / 8.0, ops=x_vano),
         Fila("Máximo del vano", "kN·m",
              ref=9.0 * q * L_**2 / 128.0, ops=real),
         Fila("Diferencia con la recta", "kN·m",
              ref=q * x_vano * (L_ - x_vano) / 2.0, ops=real - recta)],
        ref_label="Fórmula cerrada de la viga apuntalada",
        ops_label="Diagrama",
        nota=("Los planos de flexión de una barra prismática están desacoplados: "
              "en su plano local x-y esta barra **es** la viga apuntalada de la "
              "`nota01`, con `q = wy`, y le valen sus fórmulas. La recta y el "
              "diagrama difieren exactamente en la parábola simplemente apoyada "
              "`wy·x(L−x)/2`."),
    )


# ============================== FIGURAS ===================================
def figuras() -> None:
    S = modelo(1)[0]
    malla = modelo(N_MALLA)
    _fig_diagrama(S, malla)
    _fig_cortes(S)


def _fig_diagrama(S: list[float], malla: list[list[float]]) -> None:
    xs = np.linspace(0.0, L_, 241)
    reales = [cerrada(S, "Mz", float(x)) for x in xs]
    rectas = [_recta(S, "Mz", float(x)) for x in xs]
    nodales_x = [k * L_ / N_MALLA for k in range(N_MALLA)] + [L_]
    nodales_y = [malla[k][5] for k in range(N_MALLA)] + [-malla[-1][11]]

    lo = min(min(reales), min(rectas), 0.0)
    hi = max(max(reales), max(rectas), 0.0)
    margen = 0.12 * (hi - lo)
    lienzo = svg.Lienzo(
        alto=340,
        titulo="El momento del vano no está en las fuerzas de extremo",
        subtitulo=f"rafter de {L_:.2f} m con carga de vano — Mz con el signo del "
                  f"diagrama de Rukan",
    )
    ejes = lienzo.ejes(
        x=(0.0, L_), y=(lo - margen, hi + margen),
        etiqueta_x="x desde el extremo i [m]", etiqueta_y="Mz [kN·m]",
        ticks_x=5, ticks_y=5,
    )
    ejes.curva([0.0, L_], [0.0, 0.0], color=svg.GRIS, ancho=0.8)
    ejes.curva(xs, rectas, color=svg.GRIS, ancho=2.0, guion="6 4")
    ejes.curva(xs, reales, color=svg.AZUL, ancho=2.4)
    for x, y in zip(nodales_x, nodales_y):
        lienzo.circulo(ejes.x(x), ejes.y(y), 2.8, color=svg.ROJO)
    # Se marca el **máximo del vano**, que es el que no está en la salida del
    # elemento, y lo que la recta dice en ese mismo punto.
    x_vano = -S[1] / W_LOCAL[1]
    ejes.marcar(x_vano, cerrada(S, "Mz", x_vano),
                f"{cerrada(S, 'Mz', x_vano):+.2f}", color=svg.AZUL, dx=-24, dy=-12)
    ejes.marcar(x_vano, _recta(S, "Mz", x_vano),
                f"{_recta(S, 'Mz', x_vano):+.2f}", color=svg.GRIS, dx=8, dy=16)
    lienzo.linea(ejes.x(x_vano), ejes.y(cerrada(S, "Mz", x_vano)),
                 ejes.x(x_vano), ejes.y(_recta(S, "Mz", x_vano)),
                 color=svg.ROJO, ancho=1.0, guion="3 3")
    # Abajo a la derecha: la única zona que no cruzan ni la curva ni la recta.
    lienzo.leyenda(268, 214, [
        (svg.GRIS, "recta entre las fuerzas de extremo"),
        (svg.AZUL, "el diagrama (fórmula cerrada)"),
        (svg.ROJO, f"nudos de una malla de {N_MALLA} (otro solve)"),
    ])
    lienzo.guardar("lab/figs/nota07-diagrama.svg")


def _fig_cortes(S: list[float]) -> None:
    """El corte y la derivada del momento, encima uno del otro."""
    xs = np.linspace(0.0, L_, 241)
    vy = [cerrada(S, "Vy", float(x)) for x in xs]
    vz = [cerrada(S, "Vz", float(x)) for x in xs]
    h = L_ / 40.0
    xd = np.linspace(h, L_ - h, 13)
    dmz = [(cerrada(S, "Mz", float(x) + h) - cerrada(S, "Mz", float(x) - h)) / (2 * h)
           for x in xd]
    dmy = [-(cerrada(S, "My", float(x) + h) - cerrada(S, "My", float(x) - h)) / (2 * h)
           for x in xd]

    lo, hi = min(min(vy), min(vz)), max(max(vy), max(vz))
    margen = 0.18 * (hi - lo)
    lienzo = svg.Lienzo(
        alto=330,
        titulo="El signo del corte lo fija la derivada del momento",
        subtitulo="las curvas son Vy y Vz; los puntos, dMz/dx y −dMy/dx",
    )
    ejes = lienzo.ejes(
        x=(0.0, L_), y=(lo - margen, hi + margen),
        etiqueta_x="x desde el extremo i [m]", etiqueta_y="corte [kN]",
        ticks_x=5, ticks_y=5,
    )
    ejes.curva([0.0, L_], [0.0, 0.0], color=svg.GRIS, ancho=0.8)
    ejes.curva(xs, vy, color=svg.AZUL, ancho=2.2)
    ejes.curva(xs, vz, color=svg.VERDE, ancho=2.2)
    for x, y in zip(xd, dmz):
        lienzo.circulo(ejes.x(float(x)), ejes.y(y), 2.6, color=svg.ROJO)
    for x, y in zip(xd, dmy):
        lienzo.circulo(ejes.x(float(x)), ejes.y(y), 2.6, color=svg.ROJO)
    lienzo.leyenda(300, 78, [
        (svg.AZUL, "Vy  (los puntos son dMz/dx)"),
        (svg.VERDE, "Vz  (los puntos son −dMy/dx)"),
    ])
    lienzo.guardar("lab/figs/nota07-cortes.svg")


if __name__ == "__main__":
    main()
    figuras()
    print("\nFiguras escritas en lab/figs/nota07-*.svg")
