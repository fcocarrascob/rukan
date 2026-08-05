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

import numpy as np
import pytest

from lab._lib.ref import k_local, k_viga

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


def test_k_viga_es_el_bloque_de_flexion_de_k_local() -> None:
    """`k_viga` dice en su docstring que es el mismo bloque de flexión que ya
    vive dentro de `k_local`, extraído a 2 GDL por nodo. Si las dos dejaran de
    coincidir habría dos verdades sobre la misma viga en el mismo módulo.
    """
    E, A, I, L = 2.1e8, 0.012, 3.4e-4, 2.5
    gdl = [1, 2, 4, 5]  # (v_i, θ_i, v_j, θ_j) dentro de los 6 GDL de k_local
    np.testing.assert_allclose(
        k_local(E, A, I, L)[np.ix_(gdl, gdl)], k_viga(E * I, L), rtol=1e-12
    )
