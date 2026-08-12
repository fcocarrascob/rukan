"""Rukan — espectros de diseño sísmico.

Puerto a Python del espectro **NCh2369** (diseño sísmico de estructuras e
instalaciones industriales), reimplementado desde el port de referencia en
``struct_pad`` (`nch2369-spectrum.ts`). La curva es adimensional (Sa/g): la
aceleración espectral se obtiene multiplicando por g en el análisis.

La tabla ``(T, Sa/g)`` que genera este módulo es la **fuente única** de demanda:
se alimenta idéntica a SAP2000 (función de espectro de usuario) y al método de
combinación modal de Rukan, de modo que ambos motores ven exactamente el mismo
espectro. Esa es la condición para que el caso 5 sea una verificación limpia.

Referencia normativa: **NCh2369:2025 (3.ª ed., 2025.05.28)**, cláusula 5.4
(espectro de diseño), Ec. (1a) y Ec. (1b) (factor de reducción R y su
modificación por período corto R*), Tabla 3 (aceleración máxima de referencia
A_r) y Tabla 6 (parámetros que dependen del tipo de suelo).

Los valores de ``AR_BY_ZONE`` y ``SOIL_PARAMS`` se contrastaron contra las
páginas rasterizadas de las Tablas 3 y 6 de la edición 2025 el 2026-08-12 y
coinciden exactamente. La referencia anterior de este módulo apuntaba a la
NCh2369.Of2003, que ya no es la edición vigente.
"""

from __future__ import annotations

from dataclasses import dataclass

# Aceleración máxima de referencia A_r/g por zona sísmica.
# NCh2369:2025, Tabla 3 (pág. 57): A_r = 1,4·A_0, con A_0 = 0,20 / 0,30 / 0,40 g.
AR_BY_ZONE: dict[int, float] = {1: 0.28, 2: 0.42, 3: 0.56}


@dataclass(frozen=True)
class SoilParams:
    """Parámetros del suelo de fundación (NCh2369:2025, Tabla 6, pág. 60)."""

    S: float
    r: float
    T0: float
    p: float
    q: float
    T1: float


# Tipos de suelo A..E de la Tabla 6. La norma define además el tipo F ("sitios
# singulares"), que no tiene fila de parámetros y exige estudio específico.
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
    """R* — reducción corregida por período corto, Ec. (1b).

    La rama ``R <= 1`` es la primera de la ecuación y **no** es un caso
    degenerado del resto: son las estructuras diseñadas para permanecer
    elásticas (Tabla 7, primera fila), donde no se reduce nada. Sin ella la
    interpolación arranca en 1,5 y devuelve hasta 1,5 en T → 0, o sea que
    divide el espectro por 1,5 justo donde la norma lo prohíbe: 33 % menos de
    demanda, en silencio y del lado inseguro. Portada desde
    ``src/lib/nch2369-spectrum.ts`` de struct_pad, que ya la tenía.
    """
    if R <= 1:
        return 1.0
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


def r_star_for(t_star: float, R: float, soil: str) -> float:
    """R* **constante** de una dirección, evaluado con su T\\* dominante.

    Es la forma en que la Ec. (1b) se usa para el análisis: un solo R* por
    dirección, calculado con el período del modo dominante de esa dirección.
    Ver ``nch2369_spectrum(..., r_fixed=...)``.
    """
    return _r_star(t_star, R, SOIL_PARAMS[soil].T1)


def nch2369_spectrum(
    zone: int,
    soil: str,
    importance: float = 1.0,
    R: float = 5.0,
    damping: float = 0.03,
    t_max: float = 5.0,
    t_step: float = 0.01,
    r_fixed: float | None = None,
) -> Spectrum:
    """Espectro horizontal de diseño NCh2369 (Sa/g), reducido por R* y amortiguamiento.

    - ``importance`` factor I (categoría de la estructura).
    - ``R`` factor de modificación de la respuesta.
    - ``damping`` razón de amortiguamiento ξ; la ordenada se escala por el
      factor (0.05/ξ)^0.4 respecto del 5% de referencia, Ec. (1a).
    - ``r_fixed``: **R\\* constante** para toda la curva. Es lo que la norma pide
      para el análisis, porque la Ec. (1b) se evalúa con el ``T*`` del modo
      dominante **de la dirección analizada**, no período a período.

    Sobre ``r_fixed`` — importa y es contraintuitivo:

    * Con ``r_fixed=None`` (por defecto) el R* se evalúa **en cada T**. Eso
      dibuja la *familia* de reducciones y sirve para figuras didácticas, pero
      **no es el espectro de análisis**: produce una curva de forma distinta a
      la normativa en la zona ``T < 0,16·R·T1``.
    * Para correr un modal espectral se calcula primero el modal, se toma el
      ``T*`` del modo dominante de cada dirección, se obtiene su R* con
      :func:`r_star_for`, y se genera **un espectro por dirección** con
      ``r_fixed``. Es el flujo obligatorio de dos pasadas.

    Ese es el mismo defecto que arrastra ``scripts/modelo_base`` de Skills_SAP,
    y sin corregirlo dos motores no pueden calzar a 1e-4.
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
        r_eff = r_fixed if r_fixed is not None else _r_star(T, R, sp.T1)
        periods.append(T)
        accels.append(importance * sa * damping_scale / r_eff)
    return Spectrum(periods=periods, accels=accels)
