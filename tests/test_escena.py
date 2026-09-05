"""`escena.py` — el esquema `rukan/escena@1`: lo que un visor necesita para
dibujar, con la misma procedencia que los resultados.

No compara dibujos: comprueba que cada cantidad de la escena sea **la misma**
que el runner reporta por su sonda, que los modos sean los de `analysis.modal`
y que el JSON no pierda nada en el camino.
"""

from __future__ import annotations

import json
import math

import pytest

from rukan import analysis, engine, escena, io, loads
from rukan.model import FrameElement, Material, Model, NodalMass, Node, Section


@pytest.fixture
def portico() -> io.Proyecto:
    """Pórtico plano de un vano, dos columnas empotradas y una viga, con masa
    en las esquinas; un empuje lateral `P`, el peso propio `D` y dos combos."""
    fijo, libre = (True,) * 6, (False,) * 6
    nodos = [Node(1, 0.0, 0.0, 0.0, fijo, nombre="A"), Node(2, 0.0, 6.0, 0.0, fijo, nombre="B"),
             Node(3, 0.0, 0.0, 4.0, libre, nombre="C"), Node(4, 0.0, 6.0, 4.0, libre, nombre="D")]
    sec = Section(1, A=1e-2, Iy=1e-4, Iz=1e-4, J=1e-5, nombre="COL")
    els = [FrameElement(1, 1, 3, 1, 1, (1.0, 0.0, 0.0), nombre="c1"),
           FrameElement(2, 2, 4, 1, 1, (1.0, 0.0, 0.0), nombre="c2"),
           FrameElement(3, 3, 4, 1, 1, (1.0, 0.0, 0.0), nombre="v")]
    model = Model(nodes=nodos, materials=[Material(1, E=2.0e8, nu=0.3, rho=7.85)],
                  sections=[sec], elements=els,
                  masses=[NodalMass(3, (1.0,) * 3 + (0.0,) * 3),
                          NodalMass(4, (1.0,) * 3 + (0.0,) * 3)])
    return io.Proyecto(
        model=model, titulo="pórtico",
        casos={"P": {"nodales": [{"nudo": "C", "F": [0, 10, 0, 0, 0, 0]}]},
               "D": {"peso_propio": "distribuido"}},
        combinaciones={"1.2D+P": {"D": 1.2, "P": 1.0}},
        analisis={"modal": {"n_modos": 3}},
        salidas={"d": {"que": "desplazamiento", "nudo": "C", "gdl": "Uy", "caso": "P"},
                 "dc": {"que": "desplazamiento", "nudo": "D", "gdl": "Uy", "caso": "1.2D+P"},
                 "N_i": {"que": "fuerza", "barra": "c1", "extremo": "i",
                         "componente": "N", "caso": "D"},
                 "M_j": {"que": "fuerza", "barra": "c1", "extremo": "j",
                         "componente": "Mz", "caso": "P"},
                 "Ry": {"que": "reaccion", "nudo": "A", "gdl": "Uy", "caso": "P"}})


@pytest.fixture
def doc(portico, tmp_path) -> dict:
    ruta = tmp_path / "portico.proyecto.json"
    io.save(portico, ruta)
    return escena.armar(io.load(ruta), ruta)


def _idx(doc, coleccion, nombre):
    return next(k for k, x in enumerate(doc[coleccion]) if x["nombre"] == nombre)


def test_cabecera_y_geometria(doc, portico):
    assert doc["esquema"] == "rukan/escena@1"
    assert doc["proyecto"] == "portico.proyecto.json"
    assert len(doc["sha256_proyecto"]) == 64
    assert doc["rukan"] and "generado" in doc and "openseespy" in doc
    assert doc["titulo"] == "pórtico"
    assert doc["unidades"] == io.UNIDADES_INTERNAS
    assert [n["id"] for n in doc["nudos"]] == [1, 2, 3, 4]
    assert doc["nudos"][3] == {"id": 4, "nombre": "D", "xyz": [0.0, 6.0, 4.0]}
    assert doc["nudos"][0]["fijo"] == [1, 1, 1, 1, 1, 1]
    assert doc["barras"][2] == {"id": 3, "nombre": "v", "i": 3, "j": 4, "seccion": "COL"}
    assert doc["masas"] == [{"nudo": 3, "m": [1.0, 1.0, 1.0]}, {"nudo": 4, "m": [1.0, 1.0, 1.0]}]


def test_los_modos_son_los_del_runner(doc, portico):
    engine.build(portico.model)
    mr = analysis.modal(portico.model, 3)
    assert [m["n"] for m in doc["modos"]] == [1, 2, 3]
    for m, T, part in zip(doc["modos"], mr.periodos, mr.participacion):
        assert m["T"] == pytest.approx(T, rel=1e-6)
        assert m["participacion"] == pytest.approx(part, rel=1e-6, abs=1e-9)
        assert len(m["phi"]) == 4 and all(len(v) == 3 for v in m["phi"])
        assert max(abs(c) for v in m["phi"] for c in v) == pytest.approx(1.0)
        assert m["phi"][0] == [0.0, 0.0, 0.0]        # empotrado: no se mueve


def test_los_desplazamientos_son_los_de_la_sonda(doc, portico):
    r = analysis.run(portico)
    c, d = _idx(doc, "nudos", "C"), _idx(doc, "nudos", "D")
    assert doc["casos"]["P"]["u"][c][1] == pytest.approx(r["d"], rel=1e-6)
    assert doc["combinaciones"]["1.2D+P"]["u"][d][1] == pytest.approx(r["dc"], rel=1e-6)
    assert len(doc["casos"]["P"]["u"]) == 4 and len(doc["casos"]["P"]["u"][c]) == 6


def test_las_fuerzas_llevan_el_signo_del_diagrama(doc, portico):
    r = analysis.run(portico)
    c1 = _idx(doc, "barras", "c1")
    assert doc["casos"]["D"]["fuerzas"][c1][0] == pytest.approx(r["N_i"], rel=1e-6)
    assert doc["casos"]["P"]["fuerzas"][c1][11] == pytest.approx(r["M_j"], rel=1e-6)
    assert len(doc["casos"]["P"]["fuerzas"][c1]) == 12


def test_las_reacciones_solo_en_apoyos_y_cierran_con_el_peso(doc, portico):
    r = analysis.run(portico)
    assert set(doc["casos"]["P"]["reacciones"]) == {"1", "2"}
    assert doc["casos"]["P"]["reacciones"]["1"][1] == pytest.approx(r["Ry"], rel=1e-6)
    Rz = sum(v[2] for v in doc["casos"]["D"]["reacciones"].values())
    assert Rz == pytest.approx(loads.total_weight(portico.model), rel=1e-6)


def test_la_combinacion_es_lineal_en_todo(doc):
    D, P, C = doc["casos"]["D"], doc["casos"]["P"], doc["combinaciones"]["1.2D+P"]
    for k in range(4):
        for g in range(6):
            assert C["u"][k][g] == pytest.approx(1.2 * D["u"][k][g] + P["u"][k][g],
                                                 rel=1e-5, abs=1e-12)
    for b in range(3):
        for g in range(12):
            assert C["fuerzas"][b][g] == pytest.approx(1.2 * D["fuerzas"][b][g] + P["fuerzas"][b][g],
                                                       rel=1e-5, abs=1e-9)
    for n in ("1", "2"):
        assert C["reacciones"][n][2] == pytest.approx(1.2 * D["reacciones"][n][2]
                                                      + P["reacciones"][n][2], rel=1e-5, abs=1e-9)


def test_sin_modal_ni_casos_la_escena_es_solo_geometria(portico, tmp_path):
    p = io.Proyecto(model=portico.model)
    ruta = tmp_path / "geo.proyecto.json"
    io.save(p, ruta)
    d = escena.armar(io.load(ruta), ruta)
    assert d["modos"] == [] and d["casos"] == {} and d["combinaciones"] == {}
    assert len(d["barras"]) == 3


def test_el_json_es_plano_y_no_pierde_nada(doc, tmp_path):
    ruta = tmp_path / "portico.escena.json"
    escena.escribir(doc, ruta)
    leido = json.loads(ruta.read_text(encoding="utf-8"))
    assert leido == doc
    assert all(math.isfinite(c) for v in doc["casos"]["P"]["u"] for c in v)


def test_ruta_escena():
    assert io.ruta_escena("x/g.proyecto.json").name == "g.escena.json"
    assert io.ruta_escena("x/g.json").name == "g.escena.json"
