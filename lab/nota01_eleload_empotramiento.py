"""Nota 01 — `eleLoad` y el momento del vano que no está en las fuerzas de extremo.

**La pregunta:** una barra cargada con `eleLoad ... -beamUniform` reporta dos
momentos, uno por extremo. ¿Dónde quedó el momento máximo del vano?

**El caso:** viga apuntalada (empotrada en un extremo, rotulada en el otro) con
carga uniforme `q`. Es hiperestática de grado 1, pero al ser prismática la
redundante no depende de EI: los momentos salen cerrados.

    M_empotramiento = q·L²/8
    M_máx del vano  = 9·q·L²/128,  en x = 3L/8 desde la rótula
    R_rótula        = 3·q·L/8      R_empotramiento = 5·q·L/8
    θ_rótula        = q·L³/(48·E·I)

Fuente: Hibbeler, *Structural Analysis* (viga apuntalada con carga uniforme);
las mismas expresiones están tabuladas en el AISC *Manual*, Tabla 3-22.

**Las tres cosas que muestra la nota**

1. Con **un** elemento, las fuerzas de extremo dan `M_i = qL²/8` y `M_j = 0`.
   Interpolar linealmente entre ambas da, en el punto del máximo, un momento
   *negativo* de −16,9 kN·m donde el real es *positivo* de +25,3 kN·m. El
   máximo del vano no está en la salida: hay que **superponerle la parábola
   simplemente apoyada** `q·x·(L−x)/2`.

2. Mallar más fino **no converge: muestrea**. La solución de elementos finitos
   de una viga Euler-Bernoulli prismática con carga uniforme es *exacta en los
   nodos* (las funciones de forma cúbicas reproducen la homogénea, y las cargas
   consistentes el término particular). O sea: con 4 elementos los momentos
   nodales ya son exactos a precisión de máquina, pero el máximo aparece solo
   si un nodo cae encima de él.

3. Aplicar la carga como **cargas nodales equivalentes** en vez de `eleLoad` da
   *exactamente los mismos desplazamientos* y fuerzas de extremo **distintas**:
   les falta el vector de empotramiento perfecto (`qL/2`, `qL²/12`), que hay
   que devolverle a la barra. Sin eso, el momento de diseño en el apoyo sale
   15 kN·m en vez de 45.

**Verificación (los dos caminos):** referencia = fórmula cerrada + rigidez
directa en numpy (`lab/_lib/ref.py`, sin importar `rukan` ni `openseespy`);
motor = OpenSeesPy.

Correr::

    python -m lab.nota01_eleload_empotramiento
"""

from __future__ import annotations

import numpy as np
import openseespy.opensees as ops

from lab._lib import svg
from lab._lib.ref import Barra2D, Portico2D
from lab._lib.report import Fila, reportar
from rukan import units as u

# ============================ DATOS DE ENTRADA ============================
# La frontera Pint: se define con unidades y se baja al sistema interno (kN, m).
L = 6.0 * u.ureg.m
q = 10.0 * u.ureg.kN / u.ureg.m  # carga uniforme hacia abajo
E = 200 * u.ureg.GPa
I = 10_000 * u.ureg.cm**4
A = 50 * u.ureg.cm**2

L_ = u.length(L)
q_ = u.line_load(q)
E_ = u.stress(E)
I_ = u.inertia(I)
A_ = u.area(A)

# En el eje local +y de la barra (misma convención que `-beamUniform Wy`),
# una carga hacia abajo sobre una barra horizontal es negativa.
W = -q_

# ======================= REFERENCIA: FÓRMULA CERRADA =======================
M_EMPOTRAMIENTO = q_ * L_**2 / 8.0
M_VANO = 9.0 * q_ * L_**2 / 128.0
X_VANO = L_ - 3.0 * L_ / 8.0  # medido desde el empotramiento
R_ROTULA = 3.0 * q_ * L_ / 8.0
R_EMPOTRAMIENTO = 5.0 * q_ * L_ / 8.0
THETA_ROTULA = q_ * L_**3 / (48.0 * E_ * I_)


def momento_exacto(x: float) -> float:
    """Momento flector (tracción abajo positiva) a distancia ``x`` del empotramiento."""
    return R_EMPOTRAMIENTO * x - M_EMPOTRAMIENTO - q_ * x**2 / 2.0


# ============================== OPENSEES ==================================
def _montar(n_elementos: int) -> list[int]:
    """Viga apuntalada mallada en ``n_elementos``; devuelve los tags de barra."""
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    for k in range(n_elementos + 1):
        ops.node(k + 1, k * L_ / n_elementos, 0.0)

    ops.fix(1, 1, 1, 1)  # empotramiento
    ops.fix(n_elementos + 1, 0, 1, 0)  # rodillo (rótula): solo Uy

    ops.geomTransf("Linear", 1)
    tags = []
    for k in range(n_elementos):
        ops.element("elasticBeamColumn", k + 1, k + 1, k + 2, A_, E_, I_, 1)
        tags.append(k + 1)
    return tags


def _resolver() -> None:
    ops.system("BandGeneral")
    ops.numberer("Plain")
    ops.constraints("Plain")
    ops.integrator("LoadControl", 1.0)
    ops.algorithm("Linear")
    ops.analysis("Static")
    ops.analyze(1)
    ops.reactions()


def modelo_eleload(n_elementos: int = 1) -> dict:
    """El modelo correcto: la carga va sobre el elemento con `eleLoad`."""
    tags = _montar(n_elementos)
    ops.timeSeries("Constant", 1)
    ops.pattern("Plain", 1, 1)
    for t in tags:
        ops.eleLoad("-ele", t, "-type", "-beamUniform", W)
    _resolver()

    # localForce = [N_i, V_i, M_i, N_j, V_j, M_j] en ejes locales.
    fuerzas = [np.array(ops.eleResponse(t, "localForce")) for t in tags]
    n_nodo_final = n_elementos + 1
    return {
        "fuerzas": fuerzas,
        "R_empotramiento": ops.nodeReaction(1)[1],
        "M_empotramiento": ops.nodeReaction(1)[2],
        "R_rotula": ops.nodeReaction(n_nodo_final)[1],
        "theta_rotula": ops.nodeDisp(n_nodo_final, 3),
    }


def modelo_cargas_nodales() -> dict:
    """La trampa: la misma carga repartida a los nodos como cargas equivalentes.

    El vector consistente de una carga uniforme local ``w`` es
    ``w·[0, L/2, L²/12, 0, L/2, −L²/12]``. Acá se aplica tal cual a los nodos.
    """
    _montar(1)
    ops.timeSeries("Constant", 1)
    ops.pattern("Plain", 1, 1)
    ops.load(1, 0.0, W * L_ / 2.0, W * L_**2 / 12.0)
    ops.load(2, 0.0, W * L_ / 2.0, -W * L_**2 / 12.0)
    _resolver()
    return {
        "fuerzas": [np.array(ops.eleResponse(1, "localForce"))],
        "theta_rotula": ops.nodeDisp(2, 3),
    }


# =================== REFERENCIA: RIGIDEZ DIRECTA EN NUMPY ==================
def referencia_numpy(n_elementos: int = 1) -> "object":
    coords = np.array([[k * L_ / n_elementos, 0.0] for k in range(n_elementos + 1)])
    barras = [
        Barra2D(i=k, j=k + 1, E=E_, A=A_, I=I_, w=W) for k in range(n_elementos)
    ]
    portico = Portico2D(
        coords=coords,
        barras=barras,
        restricciones={
            0: (True, True, True),
            n_elementos: (False, True, False),
        },
    )
    return portico.resolver()


# ============================== LA NOTA ===================================
def main() -> None:
    print("# Nota 01 — eleLoad y el momento del vano\n")
    print(f"Viga apuntalada: L = {L_:.1f} m, q = {q_:.1f} kN/m, "
          f"EI = {E_ * I_:.0f} kN·m²\n")

    ops_1 = modelo_eleload(1)
    ref_1 = referencia_numpy(1)
    M_i_ops, M_j_ops = ops_1["fuerzas"][0][2], ops_1["fuerzas"][0][5]
    M_i_ref, M_j_ref = -ref_1.momento_extremos(0)[0], ref_1.momento_extremos(0)[1]

    # --- 1. El modelo correcto reproduce la fórmula cerrada ---------------
    reportar(
        "1. Un elemento con `eleLoad`: los extremos salen exactos",
        [
            Fila("Momento en el empotramiento", "kN·m",
                 ref=M_EMPOTRAMIENTO, ops=M_i_ops),
            Fila("Momento en la rótula", "kN·m",
                 ref=0.0, ops=M_j_ops, tol_abs=1e-9),
            Fila("Reacción en el empotramiento", "kN",
                 ref=R_EMPOTRAMIENTO, ops=ops_1["R_empotramiento"]),
            Fila("Reacción en la rótula", "kN",
                 ref=R_ROTULA, ops=ops_1["R_rotula"]),
            # La viga apoya sagando: el extremo rotulado gira antihorario (+).
            Fila("Rotación de la rótula", "mrad",
                 ref=THETA_ROTULA * 1000, ops=ops_1["theta_rotula"] * 1000),
        ],
        ref_label="Fórmula cerrada",
        nota="Los extremos están perfectos. El problema es lo que hay *entre* ellos.",
    )

    # --- 2. El máximo del vano no está en la salida -----------------------
    M_lineal = _interpolacion_lineal(-M_i_ops, M_j_ops, X_VANO)
    M_super = M_lineal + q_ * X_VANO * (L_ - X_VANO) / 2.0
    M_leido = max(-M_i_ops, M_j_ops, 0.0)
    print(f"\nEn x = {X_VANO:.2f} m, donde está el máximo del vano:\n")
    print(f"  recta entre las fuerzas de extremo   {M_lineal:+9.4f} kN·m")
    print(f"  + parábola simplemente apoyada       "
          f"{q_ * X_VANO * (L_ - X_VANO) / 2.0:+9.4f} kN·m")
    print(f"  = diagrama real                      {M_super:+9.4f} kN·m")
    print(f"\nY el máximo positivo que un elemento reporta en sus extremos: "
          f"{M_leido:.1f} kN·m.")

    reportar(
        "2. El momento del vano aparece al superponer la parábola",
        [
            Fila("Momento máximo del vano", "kN·m", ref=M_VANO, ops=M_super),
        ],
        ref_label="Fórmula cerrada (9qL²/128)",
        ops_label="Superposición",
        nota=("La recta sola da −16,9 kN·m donde el real es +25,3: no es que se "
              "quede corta, es que tiene el signo cambiado."),
    )

    # --- 3. Mallar no converge: muestrea ---------------------------------
    ops_4 = modelo_eleload(4)
    filas_malla = []
    for k in range(1, 4):  # nodos interiores de la malla de 4
        x = k * L_ / 4
        # Momento en el nodo k, leído del extremo j del elemento k.
        M_nodo = ops_4["fuerzas"][k - 1][5]
        M_ref = momento_exacto(x)
        # En x = L/4 el diagrama cruza por cero (raíz exacta de 5x²−37,5x+45):
        # ahí el error relativo no significa nada y se compara en absoluto.
        criterio = (
            {"tol_abs": 1e-9} if abs(M_ref) < 1e-6 else {"tol_pct": 1e-6}
        )
        filas_malla.append(
            Fila(f"Momento en x = {x:.2f} m", "kN·m",
                 ref=M_ref, ops=M_nodo, **criterio)
        )
    reportar(
        "3. Con 4 elementos, los momentos nodales ya son exactos",
        filas_malla,
        ref_label="M(x) exacto",
        nota=("Tolerancia 1e-6 %: la solución de EF de una viga prismática con "
              "carga uniforme es *exacta en los nodos*. Mallar más fino no "
              "converge — muestrea una solución que ya era exacta."),
    )

    # --- 4. Cargas nodales equivalentes: mismos u, otras fuerzas ----------
    ops_nodal = modelo_cargas_nodales()
    M_i_nodal = ops_nodal["fuerzas"][0][2]
    V_i_nodal = ops_nodal["fuerzas"][0][1]
    reportar(
        "4. Cargas nodales equivalentes: los desplazamientos coinciden",
        [
            Fila("Rotación de la rótula", "mrad",
                 ref=ops_1["theta_rotula"] * 1000,
                 ops=ops_nodal["theta_rotula"] * 1000, tol_pct=1e-9),
        ],
        ref_label="Con `eleLoad`",
        ops_label="Con cargas nodales",
        nota="Idénticos. Por eso la trampa no se nota mirando deformaciones.",
    )

    print(f"\nPero el momento en el empotramiento sale {M_i_nodal:.1f} kN·m, "
          f"no {M_EMPOTRAMIENTO:.1f}: un "
          f"{(1 - M_i_nodal / M_EMPOTRAMIENTO) * 100:.0f} % menos que el de "
          "diseño. Y lo que falta no es un error numérico:")

    reportar(
        "5. …pero a las fuerzas de extremo les falta el empotramiento perfecto",
        [
            Fila("Lo que falta en el momento", "kN·m",
                 ref=q_ * L_**2 / 12.0, ops=M_i_ops - M_i_nodal),
            Fila("Lo que falta en el corte", "kN",
                 ref=q_ * L_ / 2.0, ops=ops_1["fuerzas"][0][1] - V_i_nodal),
        ],
        ref_label="Empotramiento perfecto",
        ops_label="Diferencia observada",
        nota=("La diferencia es *exactamente* el vector de empotramiento "
              "perfecto qL/2 y qL²/12: lo que `eleLoad` le pone a la barra y "
              "las cargas nodales le sacaron."),
    )

    # --- coherencia entre los dos caminos independientes ------------------
    reportar(
        "6. Los dos caminos, uno contra otro",
        [
            Fila("Momento en el empotramiento", "kN·m", ref=M_i_ref, ops=M_i_ops),
            Fila("Momento en la rótula", "kN·m",
                 ref=M_j_ref, ops=M_j_ops, tol_abs=1e-9),
            Fila("Rotación de la rótula", "mrad",
                 ref=ref_1.desplazamiento(1, 2) * 1000,
                 ops=ops_1["theta_rotula"] * 1000),
        ],
        ref_label="Rigidez directa (numpy)",
    )


def _interpolacion_lineal(M_0: float, M_L: float, x: float) -> float:
    """Recta entre los momentos flectores de extremo — lo que uno dibujaría
    si creyera que la salida del elemento es el diagrama."""
    return M_0 * (1.0 - x / L_) + M_L * (x / L_)


# ============================== FIGURAS ===================================
def figuras() -> None:
    _fig_diagrama()
    _fig_muestreo()


def _fig_diagrama() -> None:
    ops_1 = modelo_eleload(1)
    M_i, M_j = ops_1["fuerzas"][0][2], ops_1["fuerzas"][0][5]

    xs = np.linspace(0.0, L_, 121)
    exacto = [momento_exacto(x) for x in xs]
    recta = [_interpolacion_lineal(-M_i, M_j, x) for x in xs]

    lienzo = svg.Lienzo(
        alto=330,
        titulo="El diagrama que la barra reporta y el que la viga tiene",
        subtitulo="viga apuntalada, q = 10 kN/m, L = 6 m — momento flector "
                  "(tracción abajo positiva)",
    )
    ejes = lienzo.ejes(
        x=(0.0, L_), y=(-50.0, 30.0),
        etiqueta_x="x desde el empotramiento [m]",
        etiqueta_y="M [kN·m]",
        ticks_x=6, ticks_y=4,
    )
    ejes.curva(xs, recta, color=svg.GRIS, ancho=2.0, guion="6 4")
    ejes.curva(xs, exacto, color=svg.AZUL, ancho=2.4)
    ejes.marcar(X_VANO, M_VANO, f"+{M_VANO:.1f}", color=svg.ROJO, dx=-52, dy=-10)
    ejes.marcar(X_VANO, _interpolacion_lineal(-M_i, M_j, X_VANO),
                f"{_interpolacion_lineal(-M_i, M_j, X_VANO):.1f}",
                color=svg.GRIS, dx=8, dy=16)
    ejes.marcar(0.0, -M_EMPOTRAMIENTO, f"−{M_EMPOTRAMIENTO:.1f}",
                color=svg.AZUL, dx=12, dy=4)
    lienzo.linea(ejes.x(X_VANO), ejes.y(M_VANO),
                 ejes.x(X_VANO), ejes.y(_interpolacion_lineal(-M_i, M_j, X_VANO)),
                 color=svg.ROJO, ancho=1.0, guion="3 3")
    # Abajo a la derecha: la única zona que no cruzan ni la curva ni la recta.
    lienzo.leyenda(268, 226, [
        (svg.GRIS, "recta entre las fuerzas de extremo"),
        (svg.AZUL, "diagrama real (+ parábola qx(L−x)/2)"),
    ])
    lienzo.guardar("lab/figs/nota01-diagrama.svg")


def _fig_muestreo() -> None:
    """Máximo positivo del vano leído de los momentos nodales, según la malla."""
    ns = list(range(1, 17))
    leidos = []
    for n in ns:
        res = modelo_eleload(n)
        momentos = [-res["fuerzas"][0][2]]
        momentos += [f[5] for f in res["fuerzas"]]
        leidos.append(max(momentos))

    lienzo = svg.Lienzo(
        alto=320,
        titulo="Mallar no converge: muestrea",
        subtitulo="máximo positivo del vano leído de los momentos nodales, "
                  "según el número de elementos",
    )
    ejes = lienzo.ejes(
        x=(1, 16), y=(0.0, 30.0),
        etiqueta_x="elementos por barra",
        etiqueta_y="M máx del vano leído [kN·m]",
        ticks_x=5, ticks_y=6,
    )
    ejes.curva([1, 16], [M_VANO, M_VANO], color=svg.ROJO, ancho=1.5, guion="6 4")
    ejes.curva(ns, leidos, color=svg.AZUL, ancho=2.0)
    for n, v in zip(ns, leidos):
        lienzo.circulo(ejes.x(n), ejes.y(v), 2.6, color=svg.AZUL)
    lienzo.texto(ejes.x(16), ejes.y(M_VANO) - 8,
                 f"exacto 9qL²/128 = {M_VANO:.2f}", tam=10.5, color=svg.ROJO,
                 anclaje="end")
    lienzo.texto(ejes.x(1) + 8, ejes.y(1.5),
                 "con 1 elemento el vano no aparece: 0", tam=10.5, color=svg.TENUE)
    lienzo.guardar("lab/figs/nota01-muestreo.svg")


if __name__ == "__main__":
    main()
    figuras()
    print("\nFiguras escritas en lab/figs/nota01-*.svg")
