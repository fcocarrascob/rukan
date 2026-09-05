"""`analysis.py` — el runner del proyecto contra lo que se sabe a mano.

Un voladizo con masa en la punta: período `2π·√(mL³/3EI)`, flecha `PL³/3EI`,
momento de empotramiento `P·L` y reacción `P`. Y el mismo modal corrido a mano
con `ops.eigen`, para comprobar que el runner no hace nada distinto.
"""

from __future__ import annotations

import math

import openseespy.opensees as ops
import pytest

from rukan import analysis, engine, io, loads
from rukan.model import FrameElement, Material, Model, NodalMass, Node, Section

E_, I_, A_, L_, m_, P_ = 2.0e8, 1.0e-4, 1.0e-2, 3.0, 1.0, 10.0


@pytest.fixture
def voladizo() -> io.Proyecto:
    model = Model(
        nodes=[Node(1, 0.0, 0.0, 0.0, (True,) * 6, nombre="base"),
               Node(2, 0.0, 0.0, L_, nombre="punta")],
        materials=[Material(1, E_, 0.3, rho=7.85)],
        sections=[Section(1, A_, I_, I_, 2 * I_, nombre="S")],
        elements=[FrameElement(1, 1, 2, 1, 1, vecxz=(1.0, 0.0, 0.0), nombre="COL")],
        masses=[NodalMass(2, (m_, m_, 0.0, 0.0, 0.0, 0.0))])
    return io.Proyecto(
        model=model,
        casos={"P": {"nodales": [{"nudo": "punta", "F": [P_, 0, 0, 0, 0, 0]}]},
               "D": {"peso_propio": "nodal"},
               "Dd": {"peso_propio": "distribuido"}},
        combinaciones={"2P": {"P": 2.0}, "D+P": {"D": 1.0, "P": 1.0}},
        analisis={"modal": {"n_modos": 2}},
        salidas={
            "T1": {"que": "periodo", "modo": 1},
            "T_star_X": {"que": "periodo_dominante", "direccion": "X"},
            "Ux": {"que": "participacion_dominante", "direccion": "X"},
            "macum_X": {"que": "masa_acumulada", "direccion": "X"},
            "d": {"que": "desplazamiento", "nudo": "punta", "gdl": "Ux", "caso": "P"},
            "d2": {"que": "desplazamiento", "nudo": 2, "gdl": "Ux", "caso": "2P"},
            "Rx": {"que": "reaccion", "nudo": "base", "gdl": "Ux", "caso": "P"},
            "Rz": {"que": "reaccion", "nudo": "base", "gdl": "Uz", "caso": "D+P"},
            "Rz_d": {"que": "reaccion", "nudo": "base", "gdl": "Uz", "caso": "Dd"},
            "My_i": {"que": "fuerza", "barra": "COL", "extremo": "i",
                     "componente": "My", "caso": "P"},
            "My_j": {"que": "fuerza", "barra": "COL", "extremo": "j",
                     "componente": "My", "caso": "P"},
            "N_i": {"que": "fuerza", "barra": "COL", "extremo": "i",
                    "componente": "N", "caso": "D"},
            "W": {"que": "peso_total"},
        })


def test_voladizo_contra_la_mano(voladizo):
    r = analysis.run(voladizo)
    T_mano = 2.0 * math.pi * math.sqrt(m_ * L_ ** 3 / (3.0 * E_ * I_))
    assert r["T1"] == pytest.approx(T_mano, rel=1e-4)
    assert r["T_star_X"] == pytest.approx(T_mano, rel=1e-4)
    assert r["Ux"] == pytest.approx(1.0, abs=1e-6)       # una sola masa: todo el modo
    assert r["macum_X"] == pytest.approx(1.0, abs=1e-6)
    assert r["d"] == pytest.approx(P_ * L_ ** 3 / (3.0 * E_ * I_), rel=1e-6)
    assert r["d2"] == pytest.approx(2.0 * r["d"], rel=1e-9)   # la combinación es lineal
    assert r["Rx"] == pytest.approx(-P_, rel=1e-9)
    W = 7.85 * A_ * L_ * 9.80665
    assert r["W"] == pytest.approx(W, rel=1e-9)
    assert r["Rz"] == pytest.approx(W, rel=1e-6)               # D + P: P no da Rz
    assert r["Rz_d"] == pytest.approx(W, rel=1e-6)             # distribuido, igual total
    assert r["N_i"] == pytest.approx(-W / 2.0, rel=1e-6)       # nodal: media barra a la base
    # Momento de empotramiento P·L, con la convención verificada en los casos 6 y 10.
    assert abs(r["My_i"]) == pytest.approx(P_ * L_, rel=1e-6)
    assert abs(r["My_j"]) < 1e-9 * P_ * L_


def test_el_modal_es_el_mismo_eigen(voladizo):
    engine.build(voladizo.model)
    lam = ops.eigen("-fullGenLapack", 2)
    T_ops = [2 * math.pi / math.sqrt(x) for x in lam]
    res = analysis.modal(voladizo.model, 2)
    assert res.periodos == pytest.approx(T_ops, rel=1e-9)
    assert res.dominante("X") == 0
    assert res.participacion[0]["X"] == pytest.approx(1.0, abs=1e-6)


def test_solo_lo_que_se_pide(voladizo):
    """Sin `analisis.modal` ni casos, un proyecto de solo `peso_total` corre."""
    p = io.Proyecto(model=voladizo.model, salidas={"W": {"que": "peso_total"}})
    assert set(analysis.run(p)) == {"W"}


def test_las_unidades_de_cada_salida(voladizo):
    u = analysis.unidades(voladizo)
    assert u["T1"] == "s" and u["d"] == "m" and u["Rx"] == "kN"
    assert u["My_i"] == "kN·m" and u["Ux"] == "—" and u["W"] == "kN"


# ==================== la sonda `esfuerzo` y la carga de vano ==================
LV, AV, IV = 8.0, 2.0e-2, 5.0e-4


@pytest.fixture
def viga() -> io.Proyecto:
    """Viga horizontal **apuntalada** bajo su peso propio distribuido.

    `vecxz = (0,1,0)` pone el eje local y en la vertical, así que la carga de
    vano cae sobre `wy` y la parábola aparece en `Mz`.

    Apuntalada y no biempotrada: con un solo elemento y los dos nudos empotrados
    el modelo no tiene ningún GDL libre y OpenSees se cae sin mensaje.
    """
    model = Model(
        nodes=[Node(1, 0.0, 0.0, 0.0, (True,) * 6, nombre="izq"),
               Node(2, LV, 0.0, 0.0, (True, True, True, False, False, False),
                    nombre="der")],
        materials=[Material(1, E_, 0.3, rho=7.85)],
        sections=[Section(1, AV, IV, IV, 2 * IV, nombre="S")],
        elements=[FrameElement(1, 1, 2, 1, 1, vecxz=(0.0, 1.0, 0.0), nombre="V")])
    return io.Proyecto(
        model=model,
        casos={"D": {"peso_propio": "distribuido"},
               "Dn": {"peso_propio": "nodal"},
               "P": {"nodales": [{"nudo": "der", "F": [1.0, 0, 0, 0, 0, 0]}]}},
        combinaciones={"1.4D": {"D": 1.4}},
        salidas={
            "Mz_i": {"que": "fuerza", "barra": "V", "extremo": "i",
                     "componente": "Mz", "caso": "D"},
            "Mz_0": {"que": "esfuerzo", "barra": "V", "componente": "Mz",
                     "x_rel": 0.0, "caso": "D"},
            "Mz_med": {"que": "esfuerzo", "barra": "V", "componente": "Mz",
                       "x_rel": 0.5, "caso": "D"},
            "Mz_med_x": {"que": "esfuerzo", "barra": "V", "componente": "Mz",
                         "x": LV / 2, "caso": "D"},
            "Mz_med_14": {"que": "esfuerzo", "barra": "V", "componente": "Mz",
                          "x_rel": 0.5, "caso": "1.4D"},
            "Vy_cuarto": {"que": "esfuerzo", "barra": "V", "componente": "Vy",
                          "x_rel": 0.25, "caso": "D"},
        })


def _w_propio(model) -> float:
    """`w = ρ·A·g` de la viga, en kN/m."""
    return model.materials[0].rho * model.sections[0].A * loads.G


def test_la_sonda_esfuerzo_en_el_extremo_es_la_sonda_fuerza(viga):
    r = analysis.run(viga)
    assert r["Mz_0"] == pytest.approx(r["Mz_i"], rel=1e-9)


def test_la_sonda_esfuerzo_da_la_formula_cerrada_de_la_apuntalada(viga):
    """Viga empotrada-rotulada con carga uniforme: `qL²/8` en el empotramiento,
    `qL²/16` al centro del vano y `5qL/8` de corte en el apoyo empotrado
    (Hibbeler; AISC, Tabla 3-22). Con el signo del diagrama de Rukan, que es el
    opuesto al de tracción abajo.

    El punto de la sonda está en `Mz_med`: ese valor **no existe** en las fuerzas
    de extremo de la barra, sale de superponerles la carga de vano.
    """
    r = analysis.run(viga)
    q = _w_propio(viga.model)
    assert r["Mz_i"] == pytest.approx(-q * LV**2 / 8.0, rel=1e-6)
    assert r["Mz_med"] == pytest.approx(q * LV**2 / 16.0, rel=1e-6)
    assert r["Mz_med_x"] == pytest.approx(r["Mz_med"], rel=1e-12)
    assert r["Vy_cuarto"] == pytest.approx(3.0 * q * LV / 8.0, rel=1e-6)


def test_una_combinacion_que_cita_un_esfuerzo_es_lineal(viga):
    r = analysis.run(viga)
    assert r["Mz_med_14"] == pytest.approx(1.4 * r["Mz_med"], rel=1e-9)


def test_las_unidades_de_la_sonda_esfuerzo(viga):
    u = analysis.unidades(viga)
    assert u["Mz_med"] == "kN·m" and u["Vy_cuarto"] == "kN"


def test_cargas_de_vano_solo_las_tiene_el_peso_propio_distribuido(viga):
    m = viga.model
    assert analysis.cargas_de_vano(viga, viga.casos["Dn"]) == {}
    assert analysis.cargas_de_vano(viga, viga.casos["P"]) == {}
    w = analysis.cargas_de_vano(viga, viga.casos["D"])
    assert set(w) == {1}
    assert w[1] == pytest.approx((0.0, _w_propio(m), 0.0), abs=1e-12)


def test_uniform_local_loads_es_el_peso_propio_proyectado(viga):
    """Rotada de vuelta a ejes globales, la carga de vano de cada barra tiene
    que ser la gravedad: `(0, 0, −ρAg)`. Es la misma proyección que
    `self_weight_distributed` le pasa a `eleLoad`, ahora devuelta en vez de
    aplicada."""
    m = viga.model
    nodos = {n.id: n for n in m.nodes}
    for eid, (wx, wy, wz) in loads.uniform_local_loads(m).items():
        e = next(x for x in m.elements if x.id == eid)
        ni, nj = nodos[e.node_i], nodos[e.node_j]
        ex, ey, ez = loads.local_axes((ni.x, ni.y, ni.z), (nj.x, nj.y, nj.z), e.vecxz)
        g = [wx * a + wy * b + wz * c for a, b, c in zip(ex, ey, ez)]
        assert g == pytest.approx([0.0, 0.0, -_w_propio(m)], abs=1e-12)
