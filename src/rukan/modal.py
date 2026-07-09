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
