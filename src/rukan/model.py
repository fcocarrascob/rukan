"""Rukan — modelo de datos estructural (**3D desde el día 1**).

El modelo es 3D siempre: los nodos tienen ``(x, y, z)`` y 6 GDL. El caso 2D es
simplemente ``z = 0`` con los GDL fuera de plano restringidos. Nunca se modela
2D-only para luego "subir" a 3D.

Las cantidades se guardan como *floats* en el sistema interno (ver
``units.py``): longitud en m, fuerza en kN, masa en tonne, etc. La conversión
desde unidades Pint ocurre en la frontera (constructores / carga de archivos),
no aquí.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Orden de GDL en todo el modelo: (Ux, Uy, Uz, Rx, Ry, Rz).
DOF = ("Ux", "Uy", "Uz", "Rx", "Ry", "Rz")


@dataclass
class Node:
    id: int
    x: float
    y: float
    z: float
    # True = GDL restringido (fijo). Orden según DOF.
    restraints: tuple[bool, bool, bool, bool, bool, bool] = (
        False,
        False,
        False,
        False,
        False,
        False,
    )


@dataclass
class Material:
    id: int
    E: float          # módulo de elasticidad [kN/m²]
    nu: float         # razón de Poisson
    rho: float = 0.0  # densidad de masa [tonne/m³]

    @property
    def G(self) -> float:
        """Módulo de corte, derivado de E y nu."""
        return self.E / (2.0 * (1.0 + self.nu))


@dataclass
class Section:
    id: int
    A: float   # área [m²]
    Iy: float  # inercia respecto al eje local y [m⁴]
    Iz: float  # inercia respecto al eje local z [m⁴]
    J: float   # constante torsional [m⁴]


@dataclass
class FrameElement:
    id: int
    node_i: int
    node_j: int
    material: int
    section: int
    # Vector que define el plano local x-z (geomTransf de OpenSees). El default
    # sirve para columnas verticales; se ajusta por elemento en el ensamble.
    vecxz: tuple[float, float, float] = (1.0, 0.0, 0.0)
    # Liberación de momento flector en los extremos (rótulas / conexiones a
    # corte). ``z`` = flexión en el plano local x-y (eje fuerte Iz); ``y`` =
    # fuera de ese plano (Iy). Liberar ambos extremos en z convierte la barra en
    # una biela axial en su plano — así se modela una diagonal de arriostramiento.
    release_z_i: bool = False
    release_z_j: bool = False
    release_y_i: bool = False
    release_y_j: bool = False


@dataclass
class NodalMass:
    node: int
    # Masa por GDL, orden según DOF [tonne / tonne·m²].
    values: tuple[float, float, float, float, float, float]


@dataclass
class Model:
    nodes: list[Node] = field(default_factory=list)
    materials: list[Material] = field(default_factory=list)
    sections: list[Section] = field(default_factory=list)
    elements: list[FrameElement] = field(default_factory=list)
    masses: list[NodalMass] = field(default_factory=list)
