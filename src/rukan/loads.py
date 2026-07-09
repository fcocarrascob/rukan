"""Rukan — cargas: peso propio, casos de carga y combinaciones.

Todo modelo real es **gravedad + otros casos**. Este módulo agrega el peso
propio y la base para casos de carga y combinaciones lineales.

**Peso propio, dos enfoques** (ver la enseñanza al final):

- ``self_weight_distributed`` — lo aplica como **carga distribuida sobre la
  barra** (``eleLoad -beamUniform``). Es el correcto para los **esfuerzos**
  estáticos: reproduce el momento que la barra toma bajo su propio peso (una viga
  horizontal flecta ``wL²/8``; un dintel inclinado empuja hacia afuera). Como el
  ``beamUniform`` de OpenSees es en **ejes locales**, la gravedad global
  ``(0,0,−w)`` se proyecta a los ejes locales de cada barra.

- ``self_weight_nodal`` — lo **concentra en los nudos** (mitad del peso de cada
  barra a cada extremo). Es el enfoque correcto para la **masa** sísmica (modal),
  pero para esfuerzos estáticos **pierde la flexión** de la barra bajo su peso.

Peso por unidad de largo: ``w = ρ · A · g`` (ρ = densidad de masa del material
[tonne/m³], A = área [m²], g = 9.80665 m/s² → w en kN/m). Peso total de una barra:
``W = w · L``.
"""

from __future__ import annotations

import math
from collections import defaultdict
from typing import Callable

import openseespy.opensees as ops

from .engine import build
from .model import Model, NodalMass

G = 9.80665  # gravedad [m/s²]


# --- Álgebra vectorial mínima (ejes locales de la barra) ---
def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _unit(a):
    n = math.sqrt(_dot(a, a))
    return (a[0] / n, a[1] / n, a[2] / n)


def local_axes(pi, pj, vecxz):
    """Ejes locales de la barra (misma convención que ``geomTransf Linear``).

    ``ex`` a lo largo de la barra (i→j); ``ey = û(vecxz × ex)``; ``ez = ex × ey``.
    """
    ex = _unit(_sub(pj, pi))
    ey = _unit(_cross(vecxz, ex))
    ez = _cross(ex, ey)
    return ex, ey, ez


def _element_geometry(model: Model):
    """Itera ``(elemento, pi, pj, L, w)`` con w = peso por largo [kN/m]."""
    nodes = {n.id: n for n in model.nodes}
    secs = {s.id: s for s in model.sections}
    mats = {m.id: m for m in model.materials}
    for e in model.elements:
        ni, nj = nodes[e.node_i], nodes[e.node_j]
        pi, pj = (ni.x, ni.y, ni.z), (nj.x, nj.y, nj.z)
        L = math.sqrt(_dot(_sub(pj, pi), _sub(pj, pi)))
        w = mats[e.material].rho * secs[e.section].A * G
        yield e, pi, pj, L, w


def element_weights(model: Model) -> dict[int, float]:
    """Peso total de cada barra [kN], indexado por id de elemento."""
    return {e.id: w * L for e, _, _, L, w in _element_geometry(model)}


def total_weight(model: Model) -> float:
    """Peso propio total del modelo [kN]."""
    return sum(element_weights(model).values())


def self_weight_distributed(model: Model, gravity=(0.0, 0.0, -1.0)) -> None:
    """Aplica el peso propio como carga distribuida (``eleLoad -beamUniform``).

    Debe llamarse con un ``ops.pattern`` activo (y tras ``engine.build``). La
    gravedad global se proyecta a los ejes locales de cada barra.
    """
    for e, pi, pj, _L, w in _element_geometry(model):
        ex, ey, ez = local_axes(pi, pj, e.vecxz)
        gvec = (gravity[0] * w, gravity[1] * w, gravity[2] * w)
        Wx, Wy, Wz = _dot(gvec, ex), _dot(gvec, ey), _dot(gvec, ez)
        # OpenSees 3D: eleLoad -beamUniform Wy Wz <Wx> (cargas en ejes locales).
        ops.eleLoad("-ele", e.id, "-type", "-beamUniform", Wy, Wz, Wx)


def self_mass_lumped(model: Model) -> list[NodalMass]:
    """Masa propia **concentrada en los nudos** (mitad de ρ·A·L a cada extremo).

    Es la masa sísmica derivada del peso propio: la misma que SAP2000 arma al
    concentrar la masa de cada barra en sus nudos. Devuelve ``NodalMass``
    traslacionales (Ux, Uy, Uz) para alimentar el análisis modal.
    """
    acc: dict[int, float] = defaultdict(float)
    for e, _pi, _pj, L, w in _element_geometry(model):
        m_half = (w / G) * L / 2.0  # ρ·A·L / 2  [tonne]
        acc[e.node_i] += m_half
        acc[e.node_j] += m_half
    return [NodalMass(nid, (m, m, m, 0.0, 0.0, 0.0)) for nid, m in acc.items()]


def self_weight_nodal(model: Model, gravity=(0.0, 0.0, -1.0)) -> None:
    """Aplica el peso propio **concentrado en los nudos** (mitad a cada extremo).

    Correcto para la masa sísmica; para esfuerzos estáticos pierde la flexión de
    la barra bajo su peso. Requiere un ``ops.pattern`` activo.
    """
    acc: dict[int, list[float]] = defaultdict(lambda: [0.0, 0.0, 0.0])
    for e, _pi, _pj, L, w in _element_geometry(model):
        W = w * L
        for nid in (e.node_i, e.node_j):
            for k in range(3):
                acc[nid][k] += gravity[k] * W / 2.0
    for nid, (fx, fy, fz) in acc.items():
        ops.load(nid, fx, fy, fz, 0.0, 0.0, 0.0)


# ============================ CASOS DE CARGA ============================
#
# Un caso de carga produce, para cada respuesta de interés, un número. Un caso
# **estático** (D = peso propio, Lr = techo) se resuelve aplicando sus cargas y
# extrayendo respuestas; un caso **modal espectral** (E) se resuelve con
# ``modal.run_directional_spectral`` y se combina por CQC. Todos terminan siendo
# un ``dict {respuesta: valor}``, y una **combinación** es su suma lineal —
# exactamente el patrón de SAP2000: definir casos y luego combinarlos.


def _static_setup() -> None:
    ops.system("BandGeneral")
    ops.numberer("RCM")
    ops.constraints("Transformation")
    ops.integrator("LoadControl", 1.0)
    ops.algorithm("Linear")
    ops.analysis("Static")


def run_static_case(
    model: Model,
    apply_loads: Callable[[], None],
    extractors: dict[str, Callable[[], float]],
    rebuild: bool = True,
) -> dict[str, float]:
    """Corre un caso de carga estático y devuelve ``{respuesta: valor}``.

    ``apply_loads`` es un callable que aplica las cargas del caso (p. ej.
    ``lambda: self_weight_distributed(model)`` o cargas nodales propias) con un
    ``ops.pattern`` ya activo. ``extractors`` es ``{nombre: callable()->float}``,
    invocado tras resolver (con ``ops.reactions()`` calculado). Con
    ``rebuild=True`` re-monta el modelo (dominio limpio por caso).
    """
    if rebuild:
        build(model)
    ops.timeSeries("Linear", 1)
    ops.pattern("Plain", 1, 1)
    apply_loads()
    _static_setup()
    ops.analyze(1)
    ops.reactions()
    return {name: fn() for name, fn in extractors.items()}


def spectral_case(directional_response, names, rule: str = "CQC") -> dict[str, float]:
    """Convierte un ``DirectionalResponse`` (modal espectral) en ``{respuesta: valor}``.

    Combina cada respuesta por ``rule`` (CQC/SRSS). Las respuestas espectrales son
    magnitudes ±; en las combinaciones se usan con signo (±E) para envolver.
    """
    return {n: directional_response.combined(n, rule) for n in names}


def combine(cases: dict[str, dict[str, float]], factors: dict[str, float]) -> dict[str, float]:
    """Combinación lineal de casos: ``r = Σ_c factor_c · r_c`` por respuesta.

    ``cases`` = ``{'D': {...}, 'Lr': {...}, 'E': {...}}``; ``factors`` = ``{'D':
    1.2, 'Lr': 1.6}``. Para el sismo, pasar ``+`` y ``−`` en dos combinaciones
    (o usar ``envelope``) porque la respuesta espectral es ±.
    """
    responses = set().union(*(c.keys() for c in cases.values()))
    return {
        r: sum(f * cases[c].get(r, 0.0) for c, f in factors.items())
        for r in responses
    }


def envelope(combos: list[dict[str, float]], kind: str = "max") -> dict[str, float]:
    """Envolvente (máx o mín por respuesta) de varias combinaciones.

    Útil para el sismo, donde ``±E`` da dos combinaciones y el diseño toma la
    gobernante.
    """
    responses = set().union(*(c.keys() for c in combos))
    pick = max if kind == "max" else min
    return {r: pick(c.get(r, 0.0) for c in combos) for r in responses}
