"""`esfuerzos.py` — los seis esfuerzos a lo largo de la barra.

OpenSees no los entrega: `eleResponse(tag, "sectionX", perc)` devuelve `[]` en un
`elasticBeamColumn`, y lo único que hay son las doce fuerzas de extremo. La
superposición de la carga de vano sobre esas fuerzas es de Rukan, y estos tests
son los que la sostienen:

* los **extremos** valen exactamente lo que `analysis.signo_diagrama` define, que
  es la convención verificada contra SAP2000 en los casos 6, 9 y 10;
* las dos **identidades de equilibrio** ``dMz/dx = +Vy`` y ``dMy/dx = −Vz`` — que
  son las que fijan el signo del corte sin necesidad de SAP2000;
* la **identidad de malla**: un solo elemento entrega, en cualquier `x`, lo mismo
  que los nudos interiores de una malla de dieciséis. Son dos solves distintos
  del mismo campo continuo, y es exacto (no asintótico) porque la solución de
  elementos finitos de una viga prismática con carga uniforme es exacta en los
  nudos — lo que la `nota01` del laboratorio estableció.

La diferencia central de estos tests es exacta: el diagrama es cuadrático, así
que su derivada por diferencia central no tiene error de truncamiento.
"""

from __future__ import annotations

import math

import openseespy.opensees as ops
import pytest

from rukan import analysis, esfuerzos, loads
from rukan.io import COMPONENTES
from rukan.model import FrameElement, Material, Model, Node, Section

L = 6.0
A, E, G, J, Iy, Iz = 1e-2, 2.0e8, 7.7e7, 1e-5, 1e-4, 2e-4
LIBRE = (0, 0, 0, 0, 0, 0)


def _diag(S):
    """Las `localForces` crudas -> los seis esfuerzos del diagrama en el extremo
    i, que es lo que `esfuerzos` toma y lo que la escena publica."""
    return [analysis.signo_diagrama("i", c) * S[k] for k, c in enumerate(COMPONENTES)]


def _barra(w, vecxz=(1.0, 0.0, 0.0), fix_j=LIBRE, n=1, nodal=None):
    """Barra vertical de `L` m mallada en `n` tramos, con carga uniforme local
    ``w = (wx, wy, wz)`` y, si se pide, una carga `nodal` de seis componentes en
    el extremo j. Devuelve la lista de `localForces` por elemento."""
    wx, wy, wz = w
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    for k in range(n + 1):
        ops.node(k + 1, 0.0, 0.0, k * L / n)
    ops.fix(1, 1, 1, 1, 1, 1, 1)
    ops.fix(n + 1, *fix_j)
    ops.geomTransf("Linear", 1, *vecxz)
    for k in range(n):
        ops.element("elasticBeamColumn", k + 1, k + 1, k + 2, A, E, G, J, Iy, Iz, 1)
    ops.timeSeries("Linear", 1)
    ops.pattern("Plain", 1, 1)
    for k in range(n):
        # OpenSees toma la carga uniforme como (Wy, Wz, Wx), no (Wx, Wy, Wz).
        ops.eleLoad("-ele", k + 1, "-type", "-beamUniform", wy, wz, wx)
    if nodal is not None:
        ops.load(n + 1, *nodal)
    ops.system("BandGeneral")
    ops.numberer("Plain")
    ops.constraints("Plain")
    ops.integrator("LoadControl", 1.0)
    ops.algorithm("Linear")
    ops.analysis("Static")
    ops.analyze(1)
    return [list(ops.eleResponse(k + 1, "localForces")) for k in range(n)]


# ===================== los extremos, y nada inventado entre medio =============
@pytest.mark.parametrize("vecxz,fix_j", [((1.0, 0.0, 0.0), LIBRE),
                                         ((0.0, 1.0, 0.0), (0, 1, 1, 0, 0, 0))])
def test_los_extremos_son_los_de_signo_diagrama(vecxz, fix_j):
    """En `x = 0` y `x = L` la fórmula tiene que dar exactamente los valores de
    extremo que las sondas y la escena ya publican: si no, habría dos
    convenciones y el diagrama del visor no empalmaría con el tooltip."""
    w = (-3.0, -10.0, 4.0)
    S = _barra(w, vecxz=vecxz, fix_j=fix_j)[0]
    for k, comp in enumerate(COMPONENTES):
        assert esfuerzos.esfuerzo(_diag(S), w, L, comp, 0.0) == pytest.approx(
            analysis.signo_diagrama("i", comp) * S[k], rel=1e-12, abs=1e-9)
        assert esfuerzos.esfuerzo(_diag(S), w, L, comp, L) == pytest.approx(
            analysis.signo_diagrama("j", comp) * S[k + 6], rel=1e-12, abs=1e-9)


# ===================== las dos identidades de equilibrio ======================
def test_la_derivada_del_momento_es_el_corte():
    """``dMz/dx = +Vy`` y ``dMy/dx = −Vz``. No son un comentario: son lo que fija
    el signo del corte contra una convención de momento ya verificada contra
    SAP2000, en vez de dejarlo por analogía con la axial.

    La diferencia central es exacta sobre un cuadrático, así que esto no tolera
    error de truncamiento: si un signo está cambiado, falla.
    """
    w = (1.5, 2.5, -7.0)
    S = _barra(w, vecxz=(0.0, 1.0, 0.0), fix_j=(0, 1, 1, 0, 0, 0))[0]
    h = L / 8.0
    for x in (h, L / 2.0, L - h):
        dMz = (esfuerzos.esfuerzo(_diag(S), w, L, "Mz", x + h)
               - esfuerzos.esfuerzo(_diag(S), w, L, "Mz", x - h)) / (2 * h)
        dMy = (esfuerzos.esfuerzo(_diag(S), w, L, "My", x + h)
               - esfuerzos.esfuerzo(_diag(S), w, L, "My", x - h)) / (2 * h)
        assert dMz == pytest.approx(esfuerzos.esfuerzo(_diag(S), w, L, "Vy", x), rel=1e-9)
        assert dMy == pytest.approx(-esfuerzos.esfuerzo(_diag(S), w, L, "Vz", x), rel=1e-9)


# ===================== contra la fórmula cerrada ==============================
def test_la_viga_apuntalada_da_la_formula_cerrada():
    """Viga empotrada-rotulada con carga uniforme: ``qL²/8`` en el empotramiento
    y ``9qL²/128`` en el vano, a ``3L/8`` de la rótula. Es el caso de la
    `nota01`, donde interpolar entre los extremos no se queda corto sino que
    cambia de signo.

    El diagrama de Rukan es el opuesto al de tracción-abajo, así que el momento
    del vano sale **negativo**: lo que se compara es la magnitud y el signo
    declarado, no un valor absoluto.
    """
    q = 10.0
    w = (0.0, -q, 0.0)
    # La barra es vertical con `vecxz = (1,0,0)`: su eje local z cae sobre el
    # X global, así que la rótula del plano local x-y se libera soltando Rx.
    S = _barra(w, fix_j=(1, 1, 1, 0, 1, 1))[0]
    assert esfuerzos.esfuerzo(_diag(S), w, L, "Mz", 0.0) == pytest.approx(q * L**2 / 8.0)
    assert esfuerzos.esfuerzo(_diag(S), w, L, "Mz", L) == pytest.approx(0.0, abs=1e-9)
    assert esfuerzos.esfuerzo(_diag(S), w, L, "Mz", 5 * L / 8) == pytest.approx(
        -9.0 * q * L**2 / 128.0)
    assert esfuerzos.esfuerzo(_diag(S), w, L, "Vy", 0.0) == pytest.approx(-5.0 * q * L / 8)
    assert esfuerzos.esfuerzo(_diag(S), w, L, "Vy", L) == pytest.approx(3.0 * q * L / 8)


# ===================== la identidad de malla ==================================
def test_un_elemento_da_lo_mismo_que_una_malla_de_dieciseis():
    """El campo continuo que un elemento describe es el que dieciséis muestrean.

    Es el segundo camino más fuerte que hay sin SAP2000: la malla fina es otro
    solve, con otro sistema de ecuaciones, y sus nudos interiores tienen que caer
    encima del diagrama del elemento único. Exacto, no asintótico.
    """
    w = (-3.0, -10.0, 4.0)
    vecxz = (0.0, 1.0, 0.0)
    S1 = _barra(w, vecxz=vecxz)[0]
    n = 16
    Sn = _barra(w, vecxz=vecxz, n=n)
    for k in range(n):
        x = k * L / n
        for c, comp in enumerate(COMPONENTES):
            assert esfuerzos.esfuerzo(_diag(S1), w, L, comp, x) == pytest.approx(
                analysis.signo_diagrama("i", comp) * Sn[k][c], rel=1e-7, abs=1e-7), \
                f"{comp} en x = {x}"


# ===================== casos degenerados ======================================
def test_sin_carga_de_vano_el_corte_es_constante_y_el_momento_lineal():
    """Voladizo con una carga en la punta: sin carga de vano el corte no varía y
    el momento es una recta. La carga nodal no es un adorno — sin ella `S` sale
    todo cero y el test pasaría sin comprobar nada."""
    S = _barra((0.0, 0.0, 0.0), nodal=(0.0, 25.0, 0.0, 0.0, 0.0, 0.0))[0]
    for w in (None, (0.0, 0.0, 0.0)):
        vs = [esfuerzos.esfuerzo(_diag(S), w, L, "Vy", x) for x in (0.0, L / 3, L)]
        assert vs[0] != pytest.approx(0.0, abs=1e-6)
        assert vs[0] == pytest.approx(vs[1]) == pytest.approx(vs[2])
        medio = esfuerzos.esfuerzo(_diag(S), w, L, "Mz", L / 2)
        extremos = (esfuerzos.esfuerzo(_diag(S), w, L, "Mz", 0.0)
                    + esfuerzos.esfuerzo(_diag(S), w, L, "Mz", L)) / 2
        assert medio == pytest.approx(extremos, abs=1e-9)


def test_la_torsion_es_constante_a_lo_largo_de_la_barra():
    """No hay torsor distribuido: `T` es el mismo en toda la barra, y por eso es
    el único componente que no tiene diagrama del cual derivar su signo.

    La barra es vertical, así que el eje local x cae sobre el Z global: el
    torsor se aplica como un momento nodal en Rz. Sin él la torsión sería cero y
    el test pasaría en vacío.
    """
    w = (-3.0, -10.0, 4.0)
    S = _barra(w, vecxz=(0.0, 1.0, 0.0),
               nodal=(0.0, 0.0, 0.0, 0.0, 0.0, 18.0))[0]
    T0 = esfuerzos.esfuerzo(_diag(S), w, L, "T", 0.0)
    # Con la regla `i: −, j: +` que la torsión toma prestada de la axial, un
    # torsor de +18 aplicado en el extremo j da un diagrama de +18 en toda la
    # barra. Que ese sea el signo correcto es justo lo que no está verificado
    # contra otro programa: acá se fija, y SAP2000 lo confirmará.
    assert T0 == pytest.approx(18.0)
    for x in (L / 4, L / 2, L):
        assert esfuerzos.esfuerzo(_diag(S), w, L, "T", x) == pytest.approx(T0)


def test_una_diagonal_liberada_no_tiene_momento_en_ningun_punto():
    """La fórmula es estática de cuerpo libre: a una barra con los dos extremos
    liberados le sale `Mz(x) ≡ 0` por sus propias fuerzas de extremo, sin que
    nadie tenga que decírselo."""
    fijo = (True,) * 6
    m = Model(
        # Con las cuatro liberaciones las dos barras son bielas: el nudo 2 no
        # tiene rigidez rotacional, y fuera del plano x-z tampoco axial. Se
        # restringen esos GDL o el sistema queda singular y el solve miente.
        nodes=[Node(1, 0.0, 0.0, 0.0, fijo),
               Node(2, 4.0, 0.0, 3.0, (False, True, False, True, True, True)),
               Node(3, 8.0, 0.0, 0.0, fijo)],
        materials=[Material(1, E=E, nu=0.3, rho=7.85)],
        sections=[Section(1, A=A, Iy=Iy, Iz=Iz, J=J)],
        elements=[FrameElement(1, 1, 2, 1, 1, (0.0, 1.0, 0.0),
                               release_z_i=True, release_z_j=True,
                               release_y_i=True, release_y_j=True),
                  FrameElement(2, 2, 3, 1, 1, (0.0, 1.0, 0.0),
                               release_z_i=True, release_z_j=True,
                               release_y_i=True, release_y_j=True)])
    r = loads.run_static_case(
        m, lambda: ops.load(2, 0.0, 0.0, -50.0, 0.0, 0.0, 0.0),
        {"S": lambda: list(ops.eleResponse(1, "localForces"))})
    S = r["S"]
    largo = math.dist((0.0, 0.0, 0.0), (4.0, 0.0, 3.0))
    for x in (0.0, largo / 3, largo / 2, largo):
        assert esfuerzos.esfuerzo(_diag(S), None, largo, "Mz", x) == pytest.approx(0.0, abs=1e-9)
        assert esfuerzos.esfuerzo(_diag(S), None, largo, "My", x) == pytest.approx(0.0, abs=1e-9)
    assert esfuerzos.esfuerzo(_diag(S), None, largo, "N", 0.0) != pytest.approx(0.0, abs=1e-6)


# ===================== el diagrama muestreado =================================
def test_diagrama_muestrea_las_estaciones_y_coincide_con_esfuerzo():
    w = (-3.0, -10.0, 4.0)
    S = _barra(w, vecxz=(0.0, 1.0, 0.0))[0]
    n = 5
    d = esfuerzos.diagrama(_diag(S), w, L, n)
    assert len(d) == n and all(len(fila) == 6 for fila in d)
    for k, fila in enumerate(d):
        x = k * L / (n - 1)
        for c, comp in enumerate(COMPONENTES):
            assert fila[c] == pytest.approx(esfuerzos.esfuerzo(_diag(S), w, L, comp, x))


def test_estaciones_reparte_de_extremo_a_extremo():
    assert esfuerzos.estaciones(L, 5) == pytest.approx([0.0, 1.5, 3.0, 4.5, 6.0])
    assert esfuerzos.estaciones(L, 2) == pytest.approx([0.0, 6.0])


# ===================== errores ================================================
def test_un_componente_inexistente_falla_nombrandolo():
    with pytest.raises(ValueError, match="M3"):
        esfuerzos.esfuerzo(_diag([0.0] * 12), None, L, "M3", 0.0)


def test_una_estacion_fuera_de_la_barra_falla_en_vez_de_extrapolar():
    with pytest.raises(ValueError, match="fuera"):
        esfuerzos.esfuerzo(_diag([0.0] * 12), None, L, "Mz", 1.5 * L)
    with pytest.raises(ValueError, match="fuera"):
        esfuerzos.esfuerzo(_diag([0.0] * 12), None, L, "Mz", -0.1)
