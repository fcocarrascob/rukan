"""`esfuerzos.js` contra `rukan/esfuerzos.py` — que las dos implementaciones de
la misma fórmula no se separen.

El diseño de `escena@2` pone la fórmula del diagrama en dos lugares: Python, que
la evalúa para las sondas del proyecto, y JavaScript, que la evalúa en el visor
para dibujar. Es el riesgo central del lote C, y esto es su mitigación: `node`
carga el módulo del visor —que por eso no tiene ningún `import`— y se comparan
número a número sobre entradas aleatorias con semilla fija.

Se compara también `ejesLocales` contra `loads.local_axes`, que es donde una
divergencia sería más difícil de ver a ojo: un diagrama dibujado sobre el eje
equivocado se ve perfectamente razonable.

Si no hay `node` en el `PATH`, el test se salta, como el de `mkdocs`.
"""

from __future__ import annotations

import json
import math
import random
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from rukan import esfuerzos, loads
from rukan.io import COMPONENTES

RAIZ = Path(__file__).resolve().parent.parent
MODULO = RAIZ / "sitio" / "docs" / "visor" / "esfuerzos.js"

pytestmark = pytest.mark.skipif(shutil.which("node") is None,
                                reason="node no está en el PATH")

DRIVER = """
import {{ esfuerzo, estaciones, diagrama, ejesLocales, COMPONENTES }} from {modulo};
import {{ readFileSync }} from 'node:fs';

const casos = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const salida = {{ componentes: COMPONENTES, esfuerzo: [], diagrama: [],
                 estaciones: [], ejes: [], errores: [] }};
for (const c of casos.esfuerzo) {{
  salida.esfuerzo.push(esfuerzo(c.di, c.w, c.L, c.componente, c.x));
}}
for (const c of casos.diagrama) {{
  salida.diagrama.push(diagrama(c.di, c.w, c.L, c.n));
  salida.estaciones.push(estaciones(c.L, c.n));
}}
for (const c of casos.ejes) {{
  salida.ejes.push(ejesLocales(c.pi, c.pj, c.vecxz));
}}
for (const c of casos.errores) {{
  try {{
    esfuerzo(c.di, c.w, c.L, c.componente, c.x);
    salida.errores.push(null);
  }} catch (e) {{
    salida.errores.push(String(e.message));
  }}
}}
process.stdout.write(JSON.stringify(salida));
"""


def _entradas(n: int = 40) -> dict:
    """Entradas aleatorias con semilla fija: barras, cargas y estaciones."""
    rng = random.Random(20260906)

    def vec(a=-10.0, b=10.0):
        return [rng.uniform(a, b) for _ in range(3)]

    esf, diag, ejes, errores = [], [], [], []
    for k in range(n):
        L = rng.uniform(0.5, 20.0)
        di = [rng.uniform(-500.0, 500.0) for _ in range(6)]
        w = None if k % 7 == 0 else vec(-5.0, 5.0)
        esf.append({"di": di, "w": w, "L": L, "x": rng.uniform(0.0, L),
                    "componente": COMPONENTES[k % 6]})
        if k % 5 == 0:
            diag.append({"di": di, "w": w, "L": L, "n": rng.randint(2, 9)})
    # Ejes locales: barras en direcciones cualesquiera, con `vecxz` no paralelo.
    for _ in range(12):
        pi, pj = vec(-30.0, 30.0), vec(-30.0, 30.0)
        if math.dist(pi, pj) < 1e-6:
            pj = [c + 1.0 for c in pj]
        ejes.append({"pi": pi, "pj": pj, "vecxz": [0.0, 0.0, 1.0]})
    for pi, pj in (([0, 0, 0], [0, 0, 5]), ([0, 0, 0], [4, 3, 0])):
        ejes.append({"pi": pi, "pj": pj, "vecxz": [1.0, 0.0, 0.0]})
        ejes.append({"pi": pi, "pj": pj, "vecxz": [0.0, 1.0, 0.0]})
    errores = [{"di": [0.0] * 6, "w": None, "L": 6.0, "componente": "M3", "x": 0.0},
               {"di": [0.0] * 6, "w": None, "L": 6.0, "componente": "Mz", "x": 9.0},
               {"di": [0.0] * 6, "w": None, "L": 6.0, "componente": "Mz", "x": -1.0}]
    return {"esfuerzo": esf, "diagrama": diag, "ejes": ejes, "errores": errores}


@pytest.fixture(scope="module")
def resultado(tmp_path_factory) -> tuple[dict, dict]:
    """Corre el módulo del visor en `node` y devuelve `(entradas, salida)`."""
    assert MODULO.exists(), f"falta {MODULO}"
    d = tmp_path_factory.mktemp("js")
    entradas = _entradas()
    (d / "casos.json").write_text(json.dumps(entradas), encoding="utf-8")
    (d / "driver.mjs").write_text(DRIVER.format(modulo=json.dumps(MODULO.as_uri())),
                                  encoding="utf-8")
    r = subprocess.run(["node", str(d / "driver.mjs"), str(d / "casos.json")],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    assert r.returncode == 0, r.stdout + r.stderr
    return entradas, json.loads(r.stdout)


def test_el_orden_de_los_componentes_es_el_mismo(resultado):
    _, out = resultado
    assert out["componentes"] == list(COMPONENTES)


def test_el_esfuerzo_es_el_mismo_numero_en_los_dos_lenguajes(resultado):
    entradas, out = resultado
    assert len(out["esfuerzo"]) == len(entradas["esfuerzo"])
    for c, v in zip(entradas["esfuerzo"], out["esfuerzo"]):
        esperado = esfuerzos.esfuerzo(c["di"], c["w"], c["L"], c["componente"], c["x"])
        assert v == pytest.approx(esperado, rel=1e-12, abs=1e-12)


def test_el_diagrama_y_sus_estaciones_son_los_mismos(resultado):
    entradas, out = resultado
    assert entradas["diagrama"]
    for c, filas, xs in zip(entradas["diagrama"], out["diagrama"], out["estaciones"]):
        assert xs == pytest.approx(esfuerzos.estaciones(c["L"], c["n"]), rel=1e-12)
        esperado = esfuerzos.diagrama(c["di"], c["w"], c["L"], c["n"])
        assert len(filas) == len(esperado)
        for a, b in zip(filas, esperado):
            assert a == pytest.approx(b, rel=1e-12, abs=1e-12)


def test_los_ejes_locales_son_los_de_loads(resultado):
    """Donde una divergencia sería invisible: un diagrama dibujado sobre el eje
    equivocado se ve perfectamente razonable."""
    entradas, out = resultado
    for c, ejes in zip(entradas["ejes"], out["ejes"]):
        esperado = loads.local_axes(tuple(c["pi"]), tuple(c["pj"]), tuple(c["vecxz"]))
        for a, b in zip(ejes, esperado):
            assert a == pytest.approx(list(b), rel=1e-12, abs=1e-12)


def test_los_dos_rechazan_las_mismas_entradas(resultado):
    entradas, out = resultado
    for c, msg in zip(entradas["errores"], out["errores"]):
        with pytest.raises(ValueError):
            esfuerzos.esfuerzo(c["di"], c["w"], c["L"], c["componente"], c["x"])
        assert msg, f"JavaScript aceptó lo que Python rechaza: {c}"
