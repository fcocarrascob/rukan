"""Cada nota del laboratorio es, además, un test de regresión.

Descubre los módulos `lab/notaNN_*.py`, corre su `main()` y falla si algún
`assert` de la comparación se rompe. Así una nota publicada queda protegida:
si el motor cambia y un número se mueve, `pytest` lo delata antes de que el post
quede mintiendo.

No se generan figuras acá — eso lo hace `figuras()`, que solo corre al ejecutar
el script directamente.
"""

from __future__ import annotations

import importlib
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
NOTAS = sorted(p.stem for p in (RAIZ / "lab").glob("nota*.py"))


@pytest.mark.parametrize("nombre", NOTAS)
def test_nota_corre_y_verifica(nombre: str) -> None:
    modulo = importlib.import_module(f"lab.{nombre}")
    assert hasattr(modulo, "main"), f"lab/{nombre}.py debe exponer main()"
    modulo.main()


def test_hay_notas_descubiertas() -> None:
    """Si el glob deja de encontrar notas, el parametrize queda vacío y los
    tests 'pasan' sin correr nada. Este test lo hace visible."""
    assert NOTAS, "No se encontró ninguna lab/nota*.py"
