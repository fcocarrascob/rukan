"""Rukan — espectros de diseño sísmico.

Puerto a Python del espectro **NCh2369** (diseño sísmico de estructuras e
instalaciones industriales), reimplementado desde el port de referencia en
``struct_pad`` (`nch2369-spectrum.ts`). La curva es adimensional (Sa/g): la
aceleración espectral se obtiene multiplicando por g en el análisis.

La tabla ``(T, Sa/g)`` que genera este módulo es la **fuente única** de demanda:
se alimenta idéntica a SAP2000 (función de espectro de usuario) y al método de
combinación modal de Rukan, de modo que ambos motores ven exactamente el mismo
espectro. Esa es la condición para que el caso 5 sea una verificación limpia.

Referencia normativa: NCh2369.Of2003, cláusula 5.4 (espectro de diseño) y 5.5
(factor de reducción R y su modificación por período corto R*).
"""

from __future__ import annotations

from dataclasses import dataclass

# Aceleración efectiva máxima A0/g por zona sísmica (NCh2369 Tabla 5.2).
AR_BY_ZONE: dict[int, float] = {1: 0.28, 2: 0.42, 3: 0.56}


@dataclass(frozen=True)
class SoilParams:
    """Parámetros del suelo de fundación (NCh2369 Tabla 5.3)."""

    S: float
    r: float
    T0: float
    p: float
    q: float
    T1: float


# Tipos de suelo I..IV en la norma; aquí con las claves A..E del port de struct_pad.
SOIL_PARAMS: dict[str, SoilParams] = {
    "A": SoilParams(S=0.90, r=4.5, T0=0.15, p=1.85, q=3.0, T1=0.15),
    "B": SoilParams(S=1.00, r=4.5, T0=0.30, p=1.60, q=3.0, T1=0.27),
    "C": SoilParams(S=1.05, r=4.5, T0=0.40, p=1.50, q=3.0, T1=0.35),
    "D": SoilParams(S=1.00, r=3.5, T0=0.60, p=1.00, q=2.5, T1=0.41),
    "E": SoilParams(S=1.00, r=3.0, T0=1.20, p=1.00, q=2.7, T1=0.79),
}


def _shape(ar: float, sp: SoilParams, T: float) -> float:
    """Forma espectral base (sin reducción por R), NCh2369 ec. 5.5."""
    if T == 0.0:
        return ar * sp.S
    ratio = T / sp.T0 if sp.T0 > 0 else 0.0
    num = 1.0 + sp.r * ratio**sp.p
    den = 1.0 + ratio**sp.q
    return ar * sp.S * num / den


def _r_star(T: float, R: float, T1: float) -> float:
    """R* — reducción corregida por período corto (interpolación 1.5 → R)."""
    limit = 0.16 * R * T1
    if limit <= 0 or T >= limit:
        return R
    return 1.5 + (R - 1.5) * (T / limit)


@dataclass(frozen=True)
class Spectrum:
    """Espectro de diseño tabulado: períodos [s] y ordenadas Sa/g [adimensional]."""

    periods: list[float]
    accels: list[float]

    def sa_over_g(self, T: float) -> float:
        """Interpola linealmente Sa/g en el período ``T`` (mismo criterio que SAP)."""
        ps = self.periods
        if T <= ps[0]:
            return self.accels[0]
        if T >= ps[-1]:
            return self.accels[-1]
        # Búsqueda lineal (la tabla es corta y esto no es camino crítico).
        for i in range(1, len(ps)):
            if T <= ps[i]:
                t0, t1 = ps[i - 1], ps[i]
                a0, a1 = self.accels[i - 1], self.accels[i]
                return a0 + (a1 - a0) * (T - t0) / (t1 - t0)
        return self.accels[-1]


def nch2369_spectrum(
    zone: int,
    soil: str,
    importance: float = 1.0,
    R: float = 5.0,
    damping: float = 0.03,
    t_max: float = 5.0,
    t_step: float = 0.01,
) -> Spectrum:
    """Espectro horizontal de diseño NCh2369 (Sa/g), reducido por R* y amortiguamiento.

    - ``importance`` factor I (categoría de la estructura).
    - ``R`` factor de modificación de la respuesta; se aplica corregido por
      período corto (R*).
    - ``damping`` razón de amortiguamiento ξ; la ordenada se escala por el
      factor (0.05/ξ)^0.4 respecto del 5% de referencia.
    """
    ar = AR_BY_ZONE[zone]
    sp = SOIL_PARAMS[soil]
    damping_scale = (0.05 / damping) ** 0.4

    n = round(t_max / t_step)
    periods: list[float] = []
    accels: list[float] = []
    for i in range(n + 1):
        T = round(i * t_step, 4)
        sa = _shape(ar, sp, T)
        r_eff = _r_star(T, R, sp.T1)
        periods.append(T)
        accels.append(importance * sa * damping_scale / r_eff)
    return Spectrum(periods=periods, accels=accels)
