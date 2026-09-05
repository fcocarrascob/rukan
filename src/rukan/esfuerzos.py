"""Rukan — los esfuerzos **a lo largo** de la barra, no solo en sus extremos.

OpenSees no los entrega. Sobre un ``elasticBeamColumn``,
``eleResponse(tag, "sectionX", perc)``, ``"section"`` e ``"integrationPoints"``
devuelven ``[]``: lo único que hay son las doce fuerzas de extremo
(``localForces``) y las seis básicas. Las respuestas ``sectionI`` / ``sectionC``
/ ``sectionJ`` / ``sectionX`` que documenta OpenSeesPy son de ``pipe`` y
``curvedPipe``. Así que la superposición de la carga de vano sobre las fuerzas
de extremo la hace Rukan, y la hace **acá**: esta es la única definición, y de
ella salen la sonda ``esfuerzo`` del proyecto, la escena y el visor.

La fórmula
----------
Con ``S = eleResponse(tag, "localForces")`` —las fuerzas que los **nudos aplican
a la barra**, en ejes locales— y ``w = (wx, wy, wz)`` la carga uniforme en esos
mismos ejes locales::

    N(x)  = −S₀ − wx·x                    Mz(x) = S₅ − S₁·x − wy·x²/2
    Vy(x) = −S₁ − wy·x                    My(x) = S₄ + S₂·x + wz·x²/2
    Vz(x) = −S₂ − wz·x
    T(x)  = −S₃

No son una elección. Salen del equilibrio del cuerpo libre ``[0, x]`` y son las
**únicas** funciones que valen, en ``x = 0`` y ``x = L``, los valores de extremo
que ``analysis.signo_diagrama`` define y que los casos 6, 9 y 10 verificaron
contra SAP2000. La asimetría entre ``Mz`` y ``My`` —el ``−S₁·x`` contra el
``+S₂·x``— es real: los ejes son dextrógiros, ``ex × ey = ez`` pero
``ex × ez = −ey``.

De ahí caen dos identidades que en `tests/test_esfuerzos.py` son tests y no
comentarios::

    dMz/dx = +Vy(x)          dMy/dx = −Vz(x)

y con ellas, el argumento que fija el signo del corte sin SAP2000: si ``Mz(x)``
está anclado en sus dos extremos a una convención de momento ya verificada, el
signo de ``Vy(x)`` queda **determinado** por la derivada del momento, no elegido
por analogía con la axial. Lo mismo vale para ``Vz`` respecto de ``My``, con el
signo opuesto.

Lo que **no** queda verificado así es la **torsión**: no tiene diagrama del cual
derivarse, sigue la regla análoga a la axial y espera SAP2000 (ver el docstring
de ``analysis`` y el caso de verificación encolado en ``ROADMAP.md``).

Alcance
-------
Vale para carga de vano **uniforme** en ejes locales, que es la que el modelo
usa (``eleLoad -type -beamUniform``, o sea el peso propio distribuido de
``loads.self_weight_distributed``). Cargas puntuales de vano (``-beamPoint``) o
trapezoidales cambiarían las expresiones y hoy no las usa nadie.

Las barras con liberación de momento no son un caso especial: esto es estática
de cuerpo libre, y una diagonal liberada en ambos extremos sale con
``Mz(x) ≡ 0`` por sus propias fuerzas de extremo, sin que nadie se lo diga.

Este módulo es puro: no importa ``openseespy`` ni monta nada. Su gemelo en
JavaScript es ``sitio/docs/visor/esfuerzos.js``, y `tests/test_esfuerzos_js.py`
compara las dos implementaciones número a número.
"""

from __future__ import annotations

from typing import Sequence

# Orden de los componentes: el mismo de `io.COMPONENTES`. No se importa de `io`
# para que este módulo no arrastre el esquema del proyecto: es aritmética.
COMPONENTES = ("N", "Vy", "Vz", "T", "My", "Mz")

# Tolerancia relativa con la que se acepta una estación en el borde de la barra:
# `x = L` calculado como `k·L/n` puede caer un ulp afuera.
_TOL = 1e-9


def esfuerzo(S: Sequence[float], w: Sequence[float] | None, L: float,
             componente: str, x: float) -> float:
    """El esfuerzo `componente` a distancia `x` del extremo i, en ejes locales.

    `S` son las doce ``localForces`` de OpenSees; `w` es ``(wx, wy, wz)`` en
    ejes locales, o ``None`` si la barra no lleva carga de vano en este caso.
    """
    if componente not in COMPONENTES:
        raise ValueError(f"componente {componente!r}: vale "
                         f"{' | '.join(COMPONENTES)}")
    if x < -_TOL * L or x > L * (1.0 + _TOL):
        raise ValueError(f"la estación x = {x!r} cae fuera de la barra "
                         f"(0 a {L!r})")
    wx, wy, wz = (0.0, 0.0, 0.0) if w is None else w
    if componente == "N":
        return -S[0] - wx * x
    if componente == "Vy":
        return -S[1] - wy * x
    if componente == "Vz":
        return -S[2] - wz * x
    if componente == "T":
        return -S[3]
    if componente == "My":
        return S[4] + S[2] * x + wz * x * x / 2.0
    return S[5] - S[1] * x - wy * x * x / 2.0


def estaciones(L: float, n: int) -> list[float]:
    """Las `n` estaciones equiespaciadas de extremo a extremo, con `n ≥ 2`."""
    if n < 2:
        raise ValueError(f"un diagrama necesita al menos dos estaciones, no {n}")
    return [k * L / (n - 1) for k in range(n)]


def diagrama(S: Sequence[float], w: Sequence[float] | None, L: float,
             n: int) -> list[list[float]]:
    """Los seis componentes en `n` estaciones equiespaciadas.

    Devuelve una fila por estación, en el orden de `COMPONENTES`.
    """
    return [[esfuerzo(S, w, L, c, x) for c in COMPONENTES]
            for x in estaciones(L, n)]
