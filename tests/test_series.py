"""`sitio/serie.py` — el andamiaje de una serie: el esquema `rukan/valores@1`, la
cadena entre eslabones y el oráculo de migración.

Primera familia: sobre una serie sintética en `tmp_path`, armada con la misma
API que usa un `_calculo.py`. Segunda familia: sobre las series publicadas en
`sitio/docs/series/`, eslabón por eslabón.
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
SITIO = RAIZ / "sitio"
SERIES = SITIO / "docs" / "series"
ENV = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}


def _mod(nombre: str):
    spec = importlib.util.spec_from_file_location(f"sitio_{nombre}", SITIO / f"{nombre}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[f"sitio_{nombre}"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def serie():
    return _mod("serie")


@pytest.fixture
def raiz(tmp_path, serie) -> Path:
    """`sitio/` de mentira: un modelo `m1` corrido y una serie `s1` con dos
    eslabones, el 01 raíz y el 02 que hereda del 01 y del modelo."""
    m = tmp_path / "docs" / "modelos" / "m1"
    m.mkdir(parents=True)
    (m / "m1.resultados.json").write_text(json.dumps({
        "esquema": "rukan/resultados@1", "proyecto": "m1.proyecto.json",
        "sha256_proyecto": "0" * 64, "rukan": "0.1.0", "commit": "abc1234",
        "openseespy": "3.7.1", "generado": "2026-09-05T10:00:00",
        "unidades": {"T_star_Y": "s", "d_alero": "m"},
        "valores": {"T_star_Y": 0.248784, "d_alero": 0.0664559}}), encoding="utf-8")

    c1 = tmp_path / "docs" / "series" / "s1" / "01-raiz"
    c1.mkdir(parents=True)
    E1 = serie.Eslabon("s1", orden=1, slug="raiz", titulo="La raíz", normas=["NCh2369:2025"],
                       carpeta=c1)
    L = E1.caso("L_luz", 25.0, "m")
    R = E1.paso("A1", "R", 5.0, "—")
    E1.sale("L_luz", L, "m", paso="S1", heredan=["02"])
    E1.sale("R", R, "—", paso="A1", heredan=["02"])
    E1.sale("xi", 0.02, "—", paso="A1", heredan=[])
    E1.publicado({"L_luz": "25,00", "R": "5,00000", "xi": "0,02"})
    E1.escribir()

    c2 = tmp_path / "docs" / "series" / "s1" / "02-hijo"
    c2.mkdir()
    E2 = serie.Eslabon("s1", orden=2, slug="hijo", titulo="El hijo", normas=["NCh2369:2025"],
                       carpeta=c2)
    L = E2.entra("L_luz", de="01", paso="S1")
    R = E2.entra("R", de="01", paso="A1")
    d = E2.entra("d_alero", de="modelo:m1", paso="M2")
    k = E2.paso("B1", "k_Y", 1000.0 / d, "kN/m")
    E2.sale("k_Y", k, "kN/m", paso="B1", heredan=[])
    E2.sale("LR", L * R, "m", paso="B2", heredan=[])
    E2.publicado({"k_Y": "15047,57290", "LR": "125,00"})
    E2.escribir()
    return tmp_path


# ============================ el esquema ==============================
def test_escribir_deja_el_esquema_valores_1(raiz):
    d = json.loads((raiz / "docs/series/s1/02-hijo/02-hijo.valores.json").read_text("utf-8"))
    assert d["esquema"] == "rukan/valores@1"
    assert (d["serie"], d["orden"], d["slug"], d["titulo"]) == ("s1", 2, "hijo", "El hijo")
    assert d["hereda_de"] == ["01"]
    assert d["entra"]["L_luz"] == {"valor": 25.0, "unidad": "m", "de": "01", "paso": "S1"}
    assert d["entra"]["d_alero"] == {"valor": 0.0664559, "unidad": "m", "de": "modelo:m1",
                                     "paso": "M2"}
    assert d["pasos"]["B1"]["k_Y"]["unidad"] == "kN/m"
    assert d["sale"]["k_Y"]["valor"] == pytest.approx(15047.5729, abs=5e-6)
    assert d["sale"]["k_Y"]["paso"] == "B1" and d["sale"]["k_Y"]["heredan"] == []
    assert d["publicado"]["k_Y"] == "15047,57290"
    assert d["rukan"] and "generado" in d


def test_entra_lee_del_origen_y_falla_nombrando(raiz, serie):
    c = raiz / "docs/series/s1/03-nieto"
    c.mkdir()
    E = serie.Eslabon("s1", orden=3, slug="nieto", titulo="t", carpeta=c)
    assert E.entra("L_luz", de="01", paso="S1") == 25.0
    with pytest.raises(KeyError, match="R_inventado.*01"):
        E.entra("R_inventado", de="01", paso="A1")
    with pytest.raises(FileNotFoundError, match="09"):
        E.entra("L_luz", de="09", paso="S1")
    with pytest.raises(KeyError, match="T_x.*m1"):
        E.entra("T_x", de="modelo:m1", paso="M1")


def test_publicado_atrapa_una_unidad_del_ultimo_decimal(raiz, serie):
    c = raiz / "docs/series/s1/03-nieto"
    c.mkdir()
    E = serie.Eslabon("s1", orden=3, slug="nieto", titulo="t", carpeta=c)
    E.sale("a", 1.23456, "m", paso="A1")
    E.publicado({"a": "1,2346"})           # a media unidad del 4.º decimal: pasa
    E.escribir()
    E.publicado({"a": "1,2345"})           # una unidad del último decimal: falla
    with pytest.raises(ValueError, match="a.*1,2345"):
        E.escribir()
    E.publicado({"a": "1,2346", "b": "3"})  # publicado sin sale: falla
    with pytest.raises(ValueError, match="b"):
        E.escribir()


def test_decimales_y_tolerancia(serie):
    assert serie.decimales("15047,57290") == 5
    assert serie.decimales("5,00000") == 5
    assert serie.decimales("25") == 0
    assert serie.decimales("0,0664559") == 7
    assert serie.num("15047,57290") == pytest.approx(15047.5729)
    assert serie.num("-142,87") == pytest.approx(-142.87)


# ============================ la cadena ===============================
def test_la_cadena_sana_no_tiene_hallazgos(raiz, serie):
    assert serie.verificar_cadena(raiz, "s1") == []
    es = serie.eslabones(raiz, "s1")
    assert [e["orden"] for e in es] == [1, 2]
    assert serie.cargar(raiz, "s1", "02")["slug"] == "hijo"


def _reescribir(raiz, nn_slug, mutar):
    ruta = raiz / "docs/series/s1" / nn_slug / f"{nn_slug}.valores.json"
    d = json.loads(ruta.read_text("utf-8"))
    mutar(d)
    ruta.write_text(json.dumps(d), encoding="utf-8")


def test_la_cadena_delata_el_valor_que_cambio_sin_recorrer(raiz, serie):
    _reescribir(raiz, "01-raiz", lambda d: d["sale"]["L_luz"].__setitem__("valor", 26.0))
    h = serie.verificar_cadena(raiz, "s1")
    assert len(h) == 1 and "L_luz" in h[0] and "01" in h[0] and "02" in h[0]


def test_la_cadena_delata_unidad_distinta_y_herencia_no_reciproca(raiz, serie):
    _reescribir(raiz, "01-raiz", lambda d: d["sale"]["R"].__setitem__("unidad", "rad"))
    assert any("R" in x and "unidad" in x for x in serie.verificar_cadena(raiz, "s1"))
    _reescribir(raiz, "01-raiz", lambda d: d["sale"]["R"].__setitem__("unidad", "—"))
    _reescribir(raiz, "01-raiz", lambda d: d["sale"]["xi"].__setitem__("heredan", ["02"]))
    assert any("xi" in x and "02" in x for x in serie.verificar_cadena(raiz, "s1"))


def test_la_cadena_delata_orden_repetido_y_origen_posterior(raiz, serie):
    _reescribir(raiz, "02-hijo", lambda d: d.__setitem__("orden", 1))
    assert any("orden" in x for x in serie.verificar_cadena(raiz, "s1"))
    _reescribir(raiz, "02-hijo", lambda d: d.__setitem__("orden", 2))
    _reescribir(raiz, "01-raiz", lambda d: d.__setitem__("orden", 3))
    assert any("anterior" in x or "posterior" in x for x in serie.verificar_cadena(raiz, "s1"))


def test_la_cadena_delata_hereda_de_incompleto(raiz, serie):
    _reescribir(raiz, "02-hijo", lambda d: d.__setitem__("hereda_de", []))
    assert any("hereda_de" in x for x in serie.verificar_cadena(raiz, "s1"))


# ============================ las citas ===============================
MD = """# Título

## Referencias

| Clave | Norma y edición | Cláusula | Leída en | Cita textual |
|---|---|---|---|---|
| NCh-p1 | NCh2369:2025 (3.ª ed.) | §5.3.2, el modelo | `Normas/NCh 2369 - 3°Edición 2025.05.28.pdf`, p. 30 | «se debe usar un modelo tridimensional» |
| NCh-p2 | NCh2369:2025 (3.ª ed.) | §5.4 | PDF ídem, pp. 34-35 | «respuesta estructural, calculado para el período» |
| W-1 | AISC 360-22 | §F2 | `referencias/AISC360-22/F2.md` | — |
"""


def test_citas_parsea_la_tabla_de_referencias(serie):
    c = serie.citas(MD)
    assert [x["clave"] for x in c] == ["NCh-p1", "NCh-p2", "W-1"]
    assert c[0]["nivel"] == "fuente" and c[0]["pdf"].endswith(".pdf") and c[0]["paginas"] == [30]
    assert c[1]["pdf"] == c[0]["pdf"] and c[1]["paginas"] == [34, 35]
    assert c[1]["cita"].startswith("respuesta estructural")
    assert c[2]["nivel"] == "wiki" and c[2]["cita"] == ""


# ============================ las series publicadas ==================
def _publicadas() -> list[tuple[str, Path]]:
    if not SERIES.exists():
        return []
    out = []
    for s in sorted(d for d in SERIES.iterdir() if d.is_dir()):
        for e in sorted(d for d in s.iterdir() if d.is_dir() and re.match(r"\d\d-", d.name)):
            out.append((s.name, e))
    return out


@pytest.mark.parametrize("serie_id", sorted({s for s, _ in _publicadas()}))
def test_la_serie_publicada_cierra(serie, serie_id):
    assert serie.verificar_cadena(SITIO, serie_id) == []


@pytest.mark.parametrize("serie_id,carpeta", _publicadas(), ids=lambda x: getattr(x, "name", x))
def test_el_calculo_reproduce_los_valores_versionados(serie, serie_id, carpeta, tmp_path):
    salida = tmp_path / f"{carpeta.name}.valores.json"
    r = subprocess.run([sys.executable, str(carpeta / "_calculo.py"), str(salida)],
                       cwd=RAIZ, env=ENV, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    assert r.returncode == 0, "\n".join([r.stdout, r.stderr])
    esperado = json.loads((carpeta / f"{carpeta.name}.valores.json").read_text("utf-8"))
    obtenido = json.loads(salida.read_text("utf-8"))
    for k in ("generado", "commit"):
        esperado.pop(k, None); obtenido.pop(k, None)
    assert obtenido == esperado


@pytest.mark.parametrize("serie_id,carpeta", _publicadas(), ids=lambda x: getattr(x, "name", x))
def test_el_eslabon_publica_lo_que_sale_y_cita_con_pagina(serie, serie_id, carpeta):
    md = (carpeta / "index.md").read_text("utf-8")
    d = json.loads((carpeta / f"{carpeta.name}.valores.json").read_text("utf-8"))
    nn = carpeta.name[:2]
    for simbolo in d["sale"]:
        assert re.search(rf"v\(\s*'{serie_id}/{nn}'\s*,\s*'{simbolo}'", md), \
            f"{simbolo} sale del {nn} y ninguna cifra de index.md lo publica"
    for tex in re.findall(r"\$\$(.+?)\$\$", md, flags=re.S):
        assert not re.search(r"\d\.\d", re.sub(r"\\text\{[^}]*\}", "", tex)), \
            f"punto decimal dentro de LaTeX en {carpeta.name}: {tex[:60]}"
    for c in serie.citas(md):
        if c["nivel"] == "fuente":
            assert c["paginas"], f"{c['clave']}: cita a la fuente sin página"
            assert len(serie.canon(c["cita"])) >= 12, f"{c['clave']}: cita demasiado corta"
    for svg in sorted((carpeta / "figs").glob("*.svg")) if (carpeta / "figs").exists() else []:
        faltan = serie.cotas_sin_respaldo(svg.read_text("utf-8"), d)
        assert not faltan, f"{svg.name}: cotas sin respaldo en los valores: {faltan[:8]}"


# ============================ los macros de serie =====================
def test_v_inyecta_desde_valores_y_busca_en_sale_pasos_entra_caso(raiz):
    m = _mod("main")
    assert m.v(raiz, "s1/02", "k_Y", 2) == "15 047,57"           # sale
    assert m.v(raiz, "s1/02", "L_luz", 2, unidad=True) == "25,00 m"   # entra
    assert m.v(raiz, "s1/01", "R", 0) == "5"                       # paso y sale
    assert m.v(raiz, "s1/02", "d_alero", 2, factor=1000) == "66,46"
    with pytest.raises(KeyError, match="nada.*02"):
        m.v(raiz, "s1/02", "nada", 2)
    with pytest.raises(FileNotFoundError, match="07"):
        m.v(raiz, "s1/07", "k_Y", 2)


def test_ficha_lista_entra_y_sale_con_enlaces(raiz):
    m = _mod("main")
    f = m.ficha(raiz, "s1/02")
    assert "| `L_luz` | 25,00 | m | [01](../01-raiz/) · S1 |" in f
    assert "| `d_alero` | 0,0664559 | m | modelo [m1](../../../modelos/m1/) · M2 |" in f
    assert "| `k_Y` | 15 047,57290 | kN/m | B1 | — |" in f
    assert "| `LR` | 125,00 | m | B2 | — |" in f
    f1 = m.ficha(raiz, "s1/01")
    assert "| `L_luz` | 25,00 | m | S1 | [02](../02-hijo/) |" in f1
    assert "valores@1" in f1 and "abc1234" not in f1


def test_tabla_serie_y_grafo_serie(raiz):
    m = _mod("main")
    t = m.tabla_serie(raiz, "s1")
    assert "| 1 | [La raíz](01-raiz/) | NCh2369:2025 | 3 |" in t
    assert "| 2 | [El hijo](02-hijo/) | NCh2369:2025 | 2 |" in t
    g = m.grafo_serie(raiz, "s1")
    assert g.startswith("```mermaid\ngraph TD") and g.rstrip().endswith("```")
    assert 'E01["01 · La raíz"]' in g and "E01 -->|L_luz, R| E02" in g


def test_figura_exige_que_el_svg_exista(raiz):
    m = _mod("main")
    c = raiz / "docs/series/s1/02-hijo/figs"
    c.mkdir()
    (c / "marco.svg").write_text("<svg/>", encoding="utf-8")
    assert m.figura(raiz, "s1/02", "marco", "El marco") == "![El marco](figs/marco.svg)"
    with pytest.raises(FileNotFoundError, match="planta"):
        m.figura(raiz, "s1/02", "planta", "x")
