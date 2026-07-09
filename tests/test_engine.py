"""Verificación del ensamblador engine.build contra solución analítica.

Reconstruye el voladizo del Caso 1 pero en 3D y a través del `Model`
(dataclasses) + `engine.build`, y comprueba que el período fundamental coincide
con 2π·√(mL³/3EI). Valida que el engine arma correctamente un modelo 3D:
nodos, restricciones, elemento flexo-axial, transformación geométrica y masas.

Se usa una sección simétrica (Iy = Iz) para que el modo lateral en X e Y sean
degenerados y no dependan de la orientación de la sección; la verificación de
inercia direccional queda para un caso posterior.
"""

import math

import openseespy.opensees as ops

from rukan import engine
from rukan import units as u
from rukan.model import FrameElement, Material, Model, NodalMass, Node, Section


def test_cantilever_3d_via_engine():
    # Datos en el sistema interno (kN, m, tonne).
    E_ = u.stress(200 * u.ureg.GPa)
    I_ = u.inertia(1.0e-4 * u.ureg.m**4)
    A_ = u.area(1.0e-2 * u.ureg.m**2)
    L_ = u.length(3.0 * u.ureg.m)
    m_ = u.mass(1000 * u.ureg.kg)
    nu = 0.3
    J_ = 2.0 * I_  # el modo con torsión no tiene masa; su valor no afecta

    model = Model(
        nodes=[
            Node(1, 0.0, 0.0, 0.0, (True,) * 6),  # base empotrada
            Node(2, 0.0, 0.0, L_),                # punta libre
        ],
        materials=[Material(1, E_, nu)],
        sections=[Section(1, A_, I_, I_, J_)],
        elements=[FrameElement(1, 1, 2, 1, 1, vecxz=(1.0, 0.0, 0.0))],
        masses=[NodalMass(2, (m_, m_, 0.0, 0.0, 0.0, 0.0))],  # masa lateral X, Y
    )

    engine.build(model)

    eigenvalues = ops.eigen("-fullGenLapack", 2)
    T1 = 2.0 * math.pi / math.sqrt(eigenvalues[0])

    T_hand = 2.0 * math.pi * math.sqrt(m_ * L_**3 / (3.0 * E_ * I_))

    assert abs(T1 - T_hand) / T_hand < 1e-4
