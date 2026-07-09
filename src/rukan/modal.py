"""Rukan — análisis modal espectral (combinación CQC/SRSS **propia**).

OpenSees resuelve el problema de autovalores (``eigen``) pero **no** hace el
análisis de respuesta espectral "de un botón": la aplicación del espectro modo a
modo y la combinación modal (CQC / SRSS) se implementan y validan aquí. Es el
riesgo técnico del peldaño 5 de la escalera de verificación.

El módulo asume que el modelo ya fue montado con ``engine.build(model)`` y opera
sobre el dominio activo de OpenSees. Trabaja con **masas concentradas** tomadas
del ``Model`` (no de una matriz de masa consistente), que es como se definen las
masas sísmicas de piso en la práctica.

Convenciones y fórmulas (Chopra, *Dynamics of Structures*, cap. 12-13):

- Vector de influencia ``ι = 1`` en el GDL de la dirección analizada (sismo
  como movimiento uniforme de la base).
- Factor de participación:   ``Γ_i = L_i / M_i``   con
  ``L_i = Σ_k m_k φ_{i,k}``  y  ``M_i = Σ_k m_k φ_{i,k}²``.
- Masa modal efectiva:        ``M*_i = L_i² / M_i``  (Σ_i M*_i = masa total).
- Pseudo-aceleración modal:   ``A_i = (S_a/g)(T_i) · g``.
- Corte basal modal:          ``V_i = M*_i · A_i``  (siempre ≥ 0).
- Respuesta modal de un GDL:  ``r_{d,i} = Γ_i · φ_{i,d} · S_d,i`` con
  ``S_d,i = A_i / ω_i²``  (p. ej. desplazamiento de un nudo).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import openseespy.opensees as ops

from .model import Model
from .spectra import Spectrum

G = 9.80665  # aceleración de gravedad [m/s²] (idéntica al factor de escala en SAP2000)

# Índice de GDL de OpenSees (1-based) por dirección; orden DOF del modelo.
_DIR_DOF = {"Ux": 1, "Uy": 2, "Uz": 3}


@dataclass
class ModeContribution:
    """Datos de un modo para la dirección analizada."""

    index: int          # 1-based
    period: float       # T_i [s]
    omega: float        # ω_i [rad/s]
    gamma: float        # factor de participación Γ_i
    eff_mass: float     # masa modal efectiva M*_i [tonne]
    eff_mass_ratio: float  # M*_i / masa total
    sa_over_g: float    # ordenada espectral en T_i
    base_shear: float   # corte basal modal V_i [kN]


def cqc_rho(wi: float, wj: float, xi: float) -> float:
    """Coeficiente de correlación CQC entre dos modos (amortiguamiento igual ξ).

    Der Kiureghian (1981). Para ``i == j`` da 1; para modos bien separados
    tiende a 0 (y CQC → SRSS).
    """
    r = wj / wi
    num = 8.0 * xi * xi * (1.0 + r) * r**1.5
    den = (1.0 - r * r) ** 2 + 4.0 * xi * xi * r * (1.0 + r) ** 2
    return num / den


def _combine(responses: list[float], omegas: list[float], xi: float, rule: str) -> float:
    """Combina respuestas modales (con signo) por SRSS o CQC."""
    if rule == "SRSS":
        return math.sqrt(sum(r * r for r in responses))
    if rule == "CQC":
        total = 0.0
        for i, ri in enumerate(responses):
            for j, rj in enumerate(responses):
                total += cqc_rho(omegas[i], omegas[j], xi) * ri * rj
        return math.sqrt(total)
    raise ValueError(f"Regla de combinación desconocida: {rule!r}")


@dataclass
class SpectralResult:
    """Resultado del análisis espectral en una dirección."""

    modes: list[ModeContribution]
    total_mass: float
    damping: float

    @property
    def periods(self) -> list[float]:
        return [m.period for m in self.modes]

    @property
    def omegas(self) -> list[float]:
        return [m.omega for m in self.modes]

    def base_shear(self, rule: str) -> float:
        """Corte basal combinado [kN] (todas las contribuciones modales ≥ 0)."""
        return _combine([m.base_shear for m in self.modes], self.omegas, self.damping, rule)


def run_spectral(
    model: Model,
    spectrum: Spectrum,
    direction: str = "Ux",
    damping: float = 0.03,
    n_modes: int = 4,
) -> SpectralResult:
    """Corre eigen + respuesta espectral en ``direction`` sobre el modelo montado.

    Requiere que ``engine.build(model)`` ya se haya llamado. Devuelve las
    contribuciones modales listas para combinar (ver ``SpectralResult``).
    """
    dof = _DIR_DOF[direction]
    di = dof - 1  # índice 0-based en NodalMass.values

    # Masas concentradas activas en la dirección analizada.
    mass_entries = [(nm.node, nm.values[di]) for nm in model.masses if nm.values[di] > 0.0]
    total_mass = sum(m for _, m in mass_entries)

    eigenvalues = ops.eigen("-fullGenLapack", n_modes)
    modes: list[ModeContribution] = []
    for k, lam in enumerate(eigenvalues, start=1):
        omega = math.sqrt(lam)
        period = 2.0 * math.pi / omega

        phi = [ops.nodeEigenvector(node, k, dof) for node, _ in mass_entries]
        L = sum(m * p for (_, m), p in zip(mass_entries, phi))
        M = sum(m * p * p for (_, m), p in zip(mass_entries, phi))
        gamma = L / M
        eff_mass = L * L / M

        sa_g = spectrum.sa_over_g(period)
        A = sa_g * G
        modes.append(
            ModeContribution(
                index=k,
                period=period,
                omega=omega,
                gamma=gamma,
                eff_mass=eff_mass,
                eff_mass_ratio=eff_mass / total_mass,
                sa_over_g=sa_g,
                base_shear=eff_mass * A,
            )
        )
    return SpectralResult(modes=modes, total_mass=total_mass, damping=damping)


def modal_displacement(
    result: SpectralResult,
    node: int,
    direction: str,
    rule: str,
) -> float:
    """Desplazamiento combinado de un nudo en ``direction`` [m].

    Reconstruye la respuesta modal con signo ``r_i = Γ_i φ_{i,d} S_d,i`` y la
    combina. Debe llamarse con los mismos autovectores activos (tras
    ``run_spectral``), sin re-montar el modelo.
    """
    dof = _DIR_DOF[direction]
    responses = []
    for m in result.modes:
        phi_d = ops.nodeEigenvector(node, m.index, dof)
        Sd = (m.sa_over_g * G) / (m.omega**2)
        responses.append(m.gamma * phi_d * Sd)
    return _combine(responses, result.omegas, result.damping, rule)


# --- Respuesta espectral general (fuerzas estáticas equivalentes modo a modo) ---
#
# Para una respuesta cualquiera (reacción, fuerza de barra, desplazamiento) el
# corte basal no basta: hay que resolver la estructura bajo las fuerzas
# inerciales de cada modo. Para el modo i y la dirección sísmica d, el vector de
# fuerzas equivalentes es  s_i = Γ_{i,d} · A_i · M · φ_i  (Chopra ec. 13.2.5),
# es decir, en cada GDL con masa:  F_c = Γ_{i,d} · A_i · m_c · φ_{i,c}. Se aplican
# como carga estática, se resuelve, y se guarda la respuesta modal r_i; luego se
# combinan las r_i (con signo) por CQC/SRSS.


class DirectionalResponse:
    """Respuestas modales (con signo) de varias cantidades en una dirección."""

    def __init__(self, per_mode: dict[str, list[float]], omegas: list[float],
                 periods: list[float], damping: float):
        self.per_mode = per_mode
        self.omegas = omegas
        self.periods = periods
        self.damping = damping

    def combined(self, name: str, rule: str = "CQC") -> float:
        return _combine(self.per_mode[name], self.omegas, self.damping, rule)


def _static_setup() -> None:
    ops.system("BandGeneral")
    ops.numberer("RCM")
    ops.constraints("Transformation")
    ops.integrator("LoadControl", 1.0)
    ops.algorithm("Linear")
    ops.analysis("Static")


def run_directional_spectral(
    model: Model,
    spectrum: Spectrum,
    direction: str,
    extractors: dict,
    damping: float = 0.03,
    n_modes: int = 6,
) -> DirectionalResponse:
    """Respuesta espectral en ``direction`` para cantidades arbitrarias.

    ``extractors`` es un dict ``{nombre: callable() -> float}``; cada callable se
    invoca tras resolver la estructura bajo las fuerzas equivalentes de cada
    modo (con ``ops.reactions()`` ya calculado) y debe devolver la respuesta de
    interés (una reacción, una fuerza de barra, un desplazamiento…). Devuelve un
    ``DirectionalResponse`` para combinar por CQC o SRSS.

    Requiere ``engine.build(model)`` previo. La masa se toma del ``Model`` (todas
    las direcciones), coherente con masas concentradas.
    """
    dof_d = _DIR_DOF[direction]
    # (node, (mx,my,mz)) para todas las masas activas.
    masses = [(nm.node, nm.values[:3]) for nm in model.masses if any(nm.values[:3])]

    eigenvalues = ops.eigen("-fullGenLapack", n_modes)
    omegas = [math.sqrt(lam) for lam in eigenvalues]
    periods = [2.0 * math.pi / w for w in omegas]

    per_mode: dict[str, list[float]] = {name: [] for name in extractors}

    for k, T in enumerate(periods, start=1):
        # Masa modal generalizada (todas las direcciones) y participación en d.
        M_gen, L_d = 0.0, 0.0
        for node, mvals in masses:
            for c, mc in enumerate(mvals):
                if mc:
                    phi_c = ops.nodeEigenvector(node, k, c + 1)
                    M_gen += mc * phi_c * phi_c
                    if c + 1 == dof_d:
                        L_d += mc * phi_c
        gamma = L_d / M_gen
        A = spectrum.sa_over_g(T) * G

        # Fuerzas estáticas equivalentes del modo k para el sismo en 'direction'.
        ops.reset()
        ops.timeSeries("Constant", 900 + k)
        ops.pattern("Plain", 900 + k, 900 + k)
        for node, mvals in masses:
            fx = [0.0] * 6
            for c, mc in enumerate(mvals):
                if mc:
                    phi_c = ops.nodeEigenvector(node, k, c + 1)
                    fx[c] = gamma * A * mc * phi_c
            ops.load(node, *fx)

        _static_setup()
        ops.analyze(1)
        ops.reactions()
        for name, fn in extractors.items():
            per_mode[name].append(fn())

        ops.remove("loadPattern", 900 + k)
        ops.remove("timeSeries", 900 + k)
        ops.wipeAnalysis()

    return DirectionalResponse(per_mode, omegas, periods, damping)


def directional_combination(rx: float, ry: float, factor: float = 0.3) -> float:
    """Combinación direccional tipo 100/30 (NCh2369 / ASCE): valor de diseño.

    Devuelve ``max(|rx| + f·|ry|, f·|rx| + |ry|)`` — el mayor entre 100 % de una
    dirección más 30 % de la ortogonal, y viceversa.
    """
    a, b = abs(rx), abs(ry)
    return max(a + factor * b, factor * a + b)
