"""Tests de la capa de unidades: conversiones al sistema interno y guardas."""

import pytest

from rukan import units as u


def test_conversiones_al_sistema_interno():
    assert u.length(3 * u.ureg.m) == pytest.approx(3.0)
    assert u.length(300 * u.ureg.cm) == pytest.approx(3.0)
    assert u.force(1 * u.ureg.kN) == pytest.approx(1.0)
    assert u.force(1000 * u.ureg.N) == pytest.approx(1.0)
    assert u.mass(1000 * u.ureg.kg) == pytest.approx(1.0)   # 1 tonne
    assert u.stress(1 * u.ureg.kPa) == pytest.approx(1.0)   # kN/m²
    assert u.stress(200 * u.ureg.GPa) == pytest.approx(2.0e8)
    assert u.inertia(1.0e4 * u.ureg.cm**4) == pytest.approx(1.0e-4)


def test_unidades_chilenas_de_fuerza():
    # 1 tonf = 1000 kgf
    assert u.force(1 * u.ureg.tonf) == pytest.approx(u.force(1000 * u.ureg.kgf))
    # y ≈ 9.80665 kN
    assert u.force(1 * u.ureg.tonf) == pytest.approx(9.80665, rel=1e-4)
    # alias tf
    assert u.force(1 * u.ureg.tf) == pytest.approx(u.force(1 * u.ureg.tonf))


def test_exige_unidades():
    # Un float pelado debe fallar ruidosamente en la frontera.
    with pytest.raises(TypeError):
        u.force(5.0)
