"""`python -m rukan` — dos subcomandos y ninguna opción de análisis: todo lo que
el análisis necesita está en el archivo de proyecto."""

from __future__ import annotations

import json

import pytest

from rukan import __main__ as cli
from rukan import io
from rukan.model import FrameElement, Material, Model, NodalMass, Node, Section


@pytest.fixture
def ruta_proyecto(tmp_path):
    model = Model(
        nodes=[Node(1, 0.0, 0.0, 0.0, (True,) * 6, nombre="base"),
               Node(2, 0.0, 0.0, 3.0, nombre="punta")],
        materials=[Material(1, 2.0e8, 0.3, rho=7.85)],
        sections=[Section(1, 1e-2, 1e-4, 1e-4, 2e-4)],
        elements=[FrameElement(1, 1, 2, 1, 1, nombre="COL")],
        masses=[NodalMass(2, (1.0, 1.0, 0.0, 0.0, 0.0, 0.0))])
    p = io.Proyecto(model=model, titulo="voladizo",
                    casos={"P": {"nodales": [{"nudo": "punta", "F": [10, 0, 0, 0, 0, 0]}]}},
                    analisis={"modal": {"n_modos": 1}},
                    salidas={"T1": {"que": "periodo", "modo": 1},
                             "d": {"que": "desplazamiento", "nudo": "punta",
                                   "gdl": "Ux", "caso": "P"}})
    ruta = tmp_path / "voladizo.proyecto.json"
    io.save(p, ruta)
    return ruta


def test_run_escribe_resultados_junto_al_proyecto(ruta_proyecto, capsys):
    assert cli.main(["run", str(ruta_proyecto)]) == 0
    salida = ruta_proyecto.with_name("voladizo.resultados.json")
    assert salida.exists()
    doc = json.loads(salida.read_text(encoding="utf-8"))
    assert doc["esquema"] == io.ESQUEMA_RESULTADOS
    assert doc["proyecto"] == "voladizo.proyecto.json"
    assert doc["sha256_proyecto"] == io.sha256(ruta_proyecto)
    assert set(doc["valores"]) == {"T1", "d"}
    assert doc["unidades"] == {"T1": "s", "d": "m"}
    assert doc["rukan"] and "generado" in doc
    texto = capsys.readouterr().out
    assert "T1" in texto and "d" in texto


def test_run_con_salida_explicita(ruta_proyecto, tmp_path):
    otra = tmp_path / "otro.json"
    assert cli.main(["run", str(ruta_proyecto), "--salida", str(otra)]) == 0
    assert otra.exists()


def test_validar_no_corre_nada(ruta_proyecto):
    assert cli.main(["validar", str(ruta_proyecto)]) == 0
    assert not ruta_proyecto.with_name("voladizo.resultados.json").exists()


def test_un_proyecto_roto_devuelve_1_y_nombra_el_campo(ruta_proyecto, capsys):
    d = json.loads(ruta_proyecto.read_text(encoding="utf-8"))
    d["salidas"]["d"]["nudo"] = "Z9"
    ruta_proyecto.write_text(json.dumps(d), encoding="utf-8")
    assert cli.main(["validar", str(ruta_proyecto)]) == 1
    assert "Z9" in capsys.readouterr().err


def test_escena_escribe_la_escena_junto_al_proyecto(ruta_proyecto, capsys):
    assert cli.main(["escena", str(ruta_proyecto)]) == 0
    salida = ruta_proyecto.with_name("voladizo.escena.json")
    assert salida.exists()
    doc = json.loads(salida.read_text(encoding="utf-8"))
    assert doc["esquema"] == "rukan/escena@1"
    assert doc["sha256_proyecto"] == io.sha256(ruta_proyecto)
    assert len(doc["modos"]) == 1 and set(doc["casos"]) == {"P"}
    assert "escrito" in capsys.readouterr().out


def test_escena_con_salida_explicita(ruta_proyecto, tmp_path):
    otra = tmp_path / "otra.escena.json"
    assert cli.main(["escena", str(ruta_proyecto), "--salida", str(otra)]) == 0
    assert otra.exists()
