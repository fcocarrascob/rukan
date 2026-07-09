"""Rukan — ensamblador: Model (dataclasses) → dominio de OpenSees.

`build(model)` toma un `Model` 3D y lo arma en el dominio de OpenSees
(``ndm=3, ndf=6``), dejándolo listo para análisis (estático, modal, …). Es la
frontera entre la representación pura de datos (``model.py``) y el motor.

Los elementos de barra flexo-axial se crean como ``elasticBeamColumn``, que
toma E y G directamente de los materiales (no usa ``uniaxialMaterial``). Todo
lo que entra aquí ya está en el sistema interno consistente (kN, m, s, tonne);
la conversión de unidades ocurrió antes, en la frontera Pint (ver ``units.py``).
"""

from __future__ import annotations

import openseespy.opensees as ops

from .model import Model


def build(model: Model) -> None:
    """Ensambla ``model`` en un dominio nuevo de OpenSees (3D, 6 GDL por nodo).

    Hace ``wipe`` del dominio previo. Tras la llamada, el modelo queda montado
    (nodos, restricciones, elementos, masas) pero sin cargas ni análisis: eso
    lo define quien llame, según el tipo de estudio.
    """
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)

    mats = {m.id: m for m in model.materials}
    secs = {s.id: s for s in model.sections}

    # Nodos y restricciones (6 GDL: Ux, Uy, Uz, Rx, Ry, Rz).
    for n in model.nodes:
        ops.node(n.id, n.x, n.y, n.z)
        if any(n.restraints):
            ops.fix(n.id, *(1 if r else 0 for r in n.restraints))

    # Elementos frame. Cada uno lleva su propia transformación geométrica, cuyo
    # tag vive en un espacio de nombres distinto al de los elementos.
    for transf_tag, e in enumerate(model.elements, start=1):
        mat = mats[e.material]
        sec = secs[e.section]
        ops.geomTransf("Linear", transf_tag, *e.vecxz)

        # Liberación de momentos en extremos. En 3D OpenSees usa ``-releasez`` /
        # ``-releasey`` (¡``-release`` a secas se ignora en 3D!). Código por eje:
        # 0=ninguno, 1=extremo i, 2=extremo j, 3=ambos.
        release_args: list = []
        code_z = (1 if e.release_z_i else 0) + (2 if e.release_z_j else 0)
        code_y = (1 if e.release_y_i else 0) + (2 if e.release_y_j else 0)
        if code_z:
            release_args += ["-releasez", code_z]
        if code_y:
            release_args += ["-releasey", code_y]

        ops.element(
            "elasticBeamColumn",
            e.id,
            e.node_i,
            e.node_j,
            sec.A,
            mat.E,
            mat.G,
            sec.J,
            sec.Iy,
            sec.Iz,
            transf_tag,
            *release_args,
        )

    # Masas concentradas por nodo (6 componentes, orden de GDL).
    for nm in model.masses:
        ops.mass(nm.node, *nm.values)
