"""`analysis.py` — el runner del proyecto contra lo que se sabe a mano.

Un voladizo con masa en la punta: período `2π·√(mL³/3EI)`, flecha `PL³/3EI`,
momento de empotramiento `P·L` y reacción `P`. Y el mismo modal corrido a mano
con `ops.eigen`, para comprobar que el runner no hace nada distinto.
"""

from __future__ import annotations

import math

import openseespy.opensees as ops
import pytest

from rukan import analysis, engine, io
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
    assert u["My_i"] == "kN·m" and u["Ux"] == "-" and u["W"] == "kN"
