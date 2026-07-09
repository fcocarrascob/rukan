"""Rukan — capa de unidades (Pint **en la frontera**).

Regla de oro: Pint solo en la frontera (entrada/salida y validación
dimensional). El núcleo numérico y OpenSees reciben *floats* en el
**sistema interno consistente**:

    longitud = m,  fuerza = kN,  tiempo = s

De ahí se derivan, por consistencia F = m·a:

    masa    = tonne (Mg = 1000 kg)     [kN·s²/m]
    tensión = kN/m² (= kPa)
    inercia = m⁴

Nunca dejes que un ``pint.Quantity`` entre a un bucle numérico ni a una
llamada de openseespy: conviértelo a magnitud en el borde con las funciones
``length()``, ``force()``, ``mass()``, etc. de este módulo.
"""

from __future__ import annotations

import pint

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity

# Unidades chilenas de fuerza (mismas que el worksheet de struct_pad).
# 1 tonf = 1000 kgf ≈ 9.80665 kN.
ureg.define("tonf = 1000 * kgf")  # tonelada-fuerza
ureg.define("tf = tonf")          # alias

# --- Sistema interno (unidades consistentes: kN, m, s) ---
U_LENGTH = ureg.m
U_FORCE = ureg.kN
U_TIME = ureg.s
U_MASS = ureg.tonne             # kN·s²/m
U_STRESS = ureg.kN / ureg.m**2  # = kPa
U_INERTIA = ureg.m**4
U_AREA = ureg.m**2


def _mag(q, unit):
    """Convierte una cantidad Pint al ``unit`` dado y devuelve su magnitud float.

    Falla ruidosamente si ``q`` no trae unidades: el objetivo de esta capa es
    justamente impedir que un número sin unidades entre al núcleo por accidente.
    """
    if not isinstance(q, ureg.Quantity):
        raise TypeError(
            f"Se esperaba una cantidad con unidades, se recibió {q!r}. "
            "Define el valor con unidades, p. ej. 3 * u.ureg.m."
        )
    return q.to(unit).magnitude


def length(q):
    return _mag(q, U_LENGTH)


def force(q):
    return _mag(q, U_FORCE)


def time(q):
    return _mag(q, U_TIME)


def mass(q):
    return _mag(q, U_MASS)


def stress(q):
    return _mag(q, U_STRESS)


def inertia(q):
    return _mag(q, U_INERTIA)


def area(q):
    return _mag(q, U_AREA)
