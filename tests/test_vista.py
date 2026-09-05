"""`vista.py` — que el SVG salga bien formado y cumpla lo que el consumidor exige.

No compara dibujos: comprueba las cuatro reglas que vienen del repo de memos que
consume estas figuras, y que son las que se rompen sin que nadie lo note.
"""

from __future__ import annotations

import re

import pytest

from rukan.model import FrameElement, Material, Model, NodalMass, Node, Section
from rukan import vista


@pytest.fixture
def portico() -> Model:
    """Pórtico plano de un vano: dos columnas empotradas y una viga."""
    fijo, libre = (True,) * 6, (False,) * 6
    nodos = [Node(1, 0.0, 0.0, 0.0, fijo), Node(2, 0.0, 6.0, 0.0, fijo),
             Node(3, 0.0, 0.0, 4.0, libre), Node(4, 0.0, 6.0, 4.0, libre)]
    sec = Section(1, A=1e-2, Iy=1e-4, Iz=1e-4, J=1e-5)
    els = [FrameElement(1, 1, 3, 1, 1, (1.0, 0.0, 0.0)),
           FrameElement(2, 2, 4, 1, 1, (1.0, 0.0, 0.0)),
           FrameElement(3, 3, 4, 1, 1, (1.0, 0.0, 0.0))]
    return Model(nodes=nodos, materials=[Material(1, E=2.0e8, nu=0.3)],
                 sections=[sec], elements=els,
                 masses=[NodalMass(3, (1.0,) * 3 + (0.0,) * 3),
                         NodalMass(4, (1.0,) * 3 + (0.0,) * 3)])


VISTAS = ["planta", "XZ", "YZ", "iso"]


def _render(model, cual, **kw):
    if cual == "iso":
        return vista.isometrica(model, **kw)
    if cual == "planta":
        return vista.planta(model, **kw)
    return vista.elevacion(model, cual, **kw)


@pytest.mark.parametrize("cual", VISTAS)
def test_svg_bien_formado_y_con_viewbox(portico, cual):
    """Sin `viewBox`, `render_figura.py` omite la figura y nadie la mira."""
    s = _render(portico, cual, titulo="t", alt="a")
    assert s.startswith("<svg") and s.rstrip().endswith("</svg>")
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
    assert m, "falta el viewBox"
    w, h = float(m.group(1)), float(m.group(2))
    assert w > 0 and h > 0
    assert f'width="{m.group(1)}"' in s and f'height="{m.group(2)}"' in s


@pytest.mark.parametrize("cual", VISTAS)
def test_sin_texto_rotado(portico, cual):
    """`verify_figura.py` no revisa los `<text>` con `transform`: no se usan."""
    s = _render(portico, cual, titulo="t", alt="a",
                cotas=[((3.0, -0.5), "6,00")])
    for t in re.findall(r"<text\b[^>]*>", s):
        assert "transform" not in t


@pytest.mark.parametrize("cual", VISTAS)
def test_fondo_propio_y_sin_marker(portico, cual):
    """Fondo claro para el tema oscuro, y flechas como polígono y no `<marker>`."""
    s = _render(portico, cual, titulo="t", alt="a")
    assert "<rect width=" in s and "fill=\"#fcfcfa\"" in s
    assert "<marker" not in s and "marker-end" not in s


def test_solo_las_cotas_que_pidio_quien_llama(portico):
    """Ningún número nace en la capa de dibujo: sin `cotas` no hay cifras."""
    s = vista.planta(portico, titulo="Planta", alt="a")
    textos = re.findall(r"<text\b[^>]*>(.*?)</text>", s, re.S)
    for t in textos:
        assert not re.search(r"\d\d", t), f"cifra no pedida en el dibujo: {t!r}"

    s2 = vista.planta(portico, titulo="Planta", alt="a",
                      cotas=[((3.0, -0.6), "6,00")])
    assert ">6,00<" in s2


def test_filtro_recorta_barras_y_nudos(portico):
    """El filtro es lo que evita que una barra tape a otra en una elevación."""
    todo = vista.escena(portico, vista.PROYECCIONES["YZ"])
    una = vista.escena(portico, vista.PROYECCIONES["YZ"], filtro={3})
    assert len(todo.barras) == 3 and len(una.barras) == 1
    assert set(una.puntos) == {3, 4}
    assert una.apoyos == []            # la viga no toca ninguna base
    assert set(una.masas) == {3, 4}


def test_modo_dibuja_deformada_y_geometria_sin_deformar(portico):
    """La deformada va con la geometría original punteada, o no se lee nada."""
    vec = {1: (0, 0, 0), 2: (0, 0, 0), 3: (0, 0.05, 0), 4: (0, 0.05, 0)}
    s = vista.modo(portico, vec, proy="YZ", titulo="m", alt="a")
    assert 'stroke-dasharray="3 3"' in s
    assert s.count("<line") == 2 * len(portico.elements)


def test_la_escala_es_la_misma_en_los_dos_ejes(portico):
    """Una figura a escala real es un chequeo del cálculo: no se deforma."""
    e = vista.escena(portico, vista.PROYECCIONES["YZ"])
    s = vista.svg(e, ancho=400, margen=10)
    w, h = (float(x) for x in
            re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups())
    # el pórtico mide 6,0 x 4,0; con margen 10 y sin título ni pie
    k = (400 - 20) / 6.0
    assert h == pytest.approx(round(4.0 * k + 20 + 6 + 8), abs=1.0)
