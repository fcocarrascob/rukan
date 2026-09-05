"""El sitio (`sitio/`) — los macros que inyectan cifras desde la corrida y la
atadura de cada modelo publicado a su proyecto.

Dos familias. La primera prueba `sitio/main.py` sobre un modelo de fixture: que
una cifra salga de `resultados.json` con coma decimal, que un símbolo que no
existe rompa el build nombrándolo, y que la procedencia falle si el hash del
proyecto no es el de la corrida. La segunda recorre `sitio/docs/modelos/` y
comprueba, modelo por modelo, que lo versionado sea lo corrido.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import runpy
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from rukan import io

RAIZ = Path(__file__).resolve().parent.parent
SITIO = RAIZ / "sitio"
MODELOS = SITIO / "docs" / "modelos"


def _main():
    spec = importlib.util.spec_from_file_location("sitio_main", SITIO / "main.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def raiz(tmp_path) -> Path:
    """Un `sitio/` de mentira con un modelo `m1` corrido: proyecto, resultados y
    escena con el hash correcto."""
    d = tmp_path / "docs" / "modelos" / "m1"
    d.mkdir(parents=True)
    proyecto = d / "m1.proyecto.json"
    proyecto.write_text('{"esquema": "rukan/proyecto@1"}\n', encoding="utf-8")
    sha = hashlib.sha256(proyecto.read_bytes()).hexdigest()
    cab = {"proyecto": "m1.proyecto.json", "sha256_proyecto": sha, "rukan": "0.1.0",
           "commit": "abc1234", "openseespy": "3.7.1", "generado": "2026-09-05T10:00:00"}
    (d / "m1.resultados.json").write_text(json.dumps({
        "esquema": "rukan/resultados@1", **cab,
        "unidades": {"T_star_Y": "s", "d_alero": "m", "k": "kN/m"},
        "valores": {"T_star_Y": 0.248784, "d_alero": 6.6459e-05, "k": 15047.5712}}),
        encoding="utf-8")
    (d / "m1.escena.json").write_text(json.dumps({
        "esquema": "rukan/escena@1", **cab, "titulo": "m1",
        "modos": [{"n": 1, "T": 0.248784, "participacion": {"X": 0.0, "Y": 0.8312, "Z": 0.0}},
                  {"n": 2, "T": 0.206025, "participacion": {"X": 0.9, "Y": 0.0, "Z": 0.0}},
                  {"n": 3, "T": 0.1, "participacion": {"X": 0.01, "Y": 0.02, "Z": 0.5}}]}),
        encoding="utf-8")
    return tmp_path


# ============================ los macros ==============================
def test_r_inyecta_la_cifra_con_coma_decimal(raiz):
    m = _main()
    assert m.r(raiz, "m1", "T_star_Y", 5) == "0,24878"
    assert m.r(raiz, "m1", "T_star_Y", 3) == "0,249"
    assert m.r(raiz, "m1", "k", 2) == "15 047,57"
    assert m.r(raiz, "m1", "d_alero") == "6,6459e-05"          # sin cifras: tal cual
    assert m.r(raiz, "m1", "T_star_Y", 5, unidad=True) == "0,24878 s"


def test_r_con_factor_y_cociente_para_los_pasos_del_memo(raiz):
    m = _main()
    assert m.r(raiz, "m1", "d_alero", 3, factor=1000) == "0,066"      # a mm
    assert m.r(raiz, "m1", "T_star_Y", 1, factor=100) == "24,9"       # a %
    assert m.cociente(raiz, "m1", 1.0, "d_alero", 2) == "15 046,87"   # k = H/δ


def test_r_con_un_simbolo_que_no_existe_rompe_el_build_nombrandolo(raiz):
    m = _main()
    with pytest.raises(KeyError, match="T_inventado"):
        m.r(raiz, "m1", "T_inventado", 3)
    with pytest.raises(FileNotFoundError, match="m9"):
        m.r(raiz, "m9", "T_star_Y", 3)


def test_procedencia_lee_la_corrida_y_exige_el_hash(raiz):
    m = _main()
    linea = m.procedencia(raiz, "m1")
    assert "rukan 0.1.0" in linea and "abc1234" in linea and "openseespy 3.7.1" in linea
    proyecto = raiz / "docs" / "modelos" / "m1" / "m1.proyecto.json"
    proyecto.write_text('{"esquema": "rukan/proyecto@1", "x": 1}\n', encoding="utf-8")
    with pytest.raises(ValueError, match="m1.proyecto.json"):
        m.procedencia(raiz, "m1")


def test_tabla_modos_es_markdown_desde_la_escena(raiz):
    m = _main()
    t = m.tabla_modos(raiz, "m1", 2)
    filas = [f for f in t.strip().splitlines() if f.startswith("|")]
    assert len(filas) == 4                      # cabecera, separador, dos modos
    assert "| 1 | 0,2488 | 0,0 | 83,1 | 0,0 |" in t
    assert "| 2 | 0,2060 | 90,0 | 0,0 | 0,0 |" in t


def test_define_env_registra_los_macros(raiz):
    m = _main()

    class Env:
        project_dir = str(raiz)
        variables: dict = {}
        macros: dict = {}

        def macro(self, fn, name=None):
            self.macros[name or fn.__name__] = fn
            return fn
    env = Env()
    m.define_env(env)
    assert set(env.macros) >= {"r", "tabla_modos", "procedencia"}
    assert env.macros["r"]("m1", "T_star_Y", 5) == "0,24878"


# ============================ los modelos publicados ==================
def _modelos() -> list[Path]:
    if not MODELOS.exists():
        return []
    return sorted(d for d in MODELOS.iterdir() if d.is_dir() and not d.name.startswith("_"))


@pytest.mark.parametrize("carpeta", _modelos(), ids=lambda d: d.name)
def test_el_modelo_publicado_es_el_corrido(carpeta):
    slug = carpeta.name
    proyecto = carpeta / f"{slug}.proyecto.json"
    io.load(proyecto)
    sha = io.sha256(proyecto)
    for cual in ("resultados", "escena"):
        doc = json.loads((carpeta / f"{slug}.{cual}.json").read_text(encoding="utf-8"))
        assert doc["sha256_proyecto"] == sha, f"{slug}.{cual}.json no es de este proyecto"


@pytest.mark.parametrize("carpeta", _modelos(), ids=lambda d: d.name)
def test_el_generador_reproduce_el_proyecto_versionado(carpeta, tmp_path):
    """El modelo del sitio es el del caso de verificación, no una copia que se aleja."""
    slug = carpeta.name
    salida = tmp_path / f"{slug}.proyecto.json"
    subprocess.run([sys.executable, str(carpeta / "_generar.py"), str(salida)],
                   check=True, cwd=RAIZ)
    esperado = json.loads((carpeta / f"{slug}.proyecto.json").read_text(encoding="utf-8"))
    assert json.loads(salida.read_text(encoding="utf-8")) == esperado


@pytest.mark.skipif(shutil.which("mkdocs") is None, reason="mkdocs no está instalado")
def test_mkdocs_build_estricto(tmp_path):
    subprocess.run(["mkdocs", "build", "--strict", "-f", str(SITIO / "mkdocs.yml"),
                    "-d", str(tmp_path / "build")], check=True, cwd=SITIO)
    assert (tmp_path / "build" / "index.html").exists()
