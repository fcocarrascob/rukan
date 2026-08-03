"""Referencias numéricas independientes — numpy puro.

**Regla del laboratorio: este módulo no importa `rukan` ni `openseespy`.** Es lo
que hace que la verificación signifique algo: si la referencia compartiera
código con lo verificado, ambas se equivocarían igual y la tabla del post daría
error 0 % sin decir nada.

Crece por demanda: cada nota agrega solo lo que necesita.

Convenciones
------------
GDL por nodo, en orden: ``(u, v, θ)`` — traslación x, traslación y, rotación
antihoraria positiva. Ejes globales x a la derecha, y hacia arriba.

Carga uniforme ``w`` sobre una barra: **en el eje local +y de la barra**, la
misma convención que ``eleLoad -type -beamUniform Wy`` de OpenSees. Una carga
hacia abajo sobre una barra horizontal es ``w < 0``.

Fuerzas de extremo de barra: el vector ``S = k·u_local − P_eq`` son las fuerzas
que los **nodos aplican a la barra**, en direcciones locales. El momento flector
(convención de tracción abajo positiva) se lee de ahí como::

    M(0) = −S[2]        M(L) = +S[5]

Fuente: Cook, Malkus & Plesha, *Concepts and Applications of Finite Element
Analysis* — matriz de rigidez de viga-columna plana y vector de cargas
consistente para carga uniforme.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

__all__ = [
    "Barra2D",
    "Portico2D",
    "Resultado2D",
    "k_local",
    "rotacion",
    "cargas_equivalentes",
]

GDL_POR_NODO = 3


def k_local(E: float, A: float, I: float, L: float) -> np.ndarray:
    """Rigidez 6×6 de una barra plana (Euler-Bernoulli) en ejes locales."""
    ea, ei = E * A / L, E * I
    return np.array(
        [
            [ea, 0, 0, -ea, 0, 0],
            [0, 12 * ei / L**3, 6 * ei / L**2, 0, -12 * ei / L**3, 6 * ei / L**2],
            [0, 6 * ei / L**2, 4 * ei / L, 0, -6 * ei / L**2, 2 * ei / L],
            [-ea, 0, 0, ea, 0, 0],
            [0, -12 * ei / L**3, -6 * ei / L**2, 0, 12 * ei / L**3, -6 * ei / L**2],
            [0, 6 * ei / L**2, 2 * ei / L, 0, -6 * ei / L**2, 4 * ei / L],
        ]
    )


def rotacion(c: float, s: float) -> np.ndarray:
    """Matriz 6×6 que lleva global → local, con ``c = cos α``, ``s = sen α``."""
    t = np.zeros((6, 6))
    bloque = np.array([[c, s, 0.0], [-s, c, 0.0], [0.0, 0.0, 1.0]])
    t[:3, :3] = bloque
    t[3:, 3:] = bloque
    return t


def cargas_equivalentes(w: float, L: float) -> np.ndarray:
    """Vector de cargas nodales consistentes de una carga uniforme local ``w``.

    ``P_eq = ∫ Nᵀ w dx = w·[0, L/2, L²/12, 0, L/2, −L²/12]`` en ejes locales.
    Con la barra empotrada en ambos extremos, las fuerzas de extremo valen
    ``S = −P_eq``, es decir los clásicos ``wL/2`` y ``wL²/12``.
    """
    return w * np.array([0.0, L / 2, L**2 / 12, 0.0, L / 2, -(L**2) / 12])


@dataclass
class Barra2D:
    """Barra plana entre dos nodos, con carga uniforme opcional."""

    i: int
    j: int
    E: float
    A: float
    I: float
    w: float = 0.0  # carga uniforme en el eje local +y


@dataclass
class Resultado2D:
    u: np.ndarray  # (n_nodos, 3) desplazamientos globales
    reacciones: np.ndarray  # (n_nodos, 3) reacciones globales
    fuerzas: list[np.ndarray]  # por barra: S (6,) en ejes locales

    def desplazamiento(self, nodo: int, gdl: int) -> float:
        return float(self.u[nodo, gdl])

    def momento_extremos(self, barra: int) -> tuple[float, float]:
        """Momento flector (tracción abajo positiva) en los extremos i y j."""
        s = self.fuerzas[barra]
        return -float(s[2]), float(s[5])


@dataclass
class Portico2D:
    """Pórtico plano resuelto por rigidez directa, sin dependencias externas.

    ``coords`` es (n_nodos, 2); ``restricciones`` marca con ``True`` los GDL
    fijos; ``cargas`` son cargas nodales globales (Fx, Fy, M).
    """

    coords: np.ndarray
    barras: list[Barra2D]
    restricciones: dict[int, tuple[bool, bool, bool]] = field(default_factory=dict)
    cargas: dict[int, tuple[float, float, float]] = field(default_factory=dict)

    def _geometria(self, b: Barra2D) -> tuple[float, float, float]:
        dx, dy = self.coords[b.j] - self.coords[b.i]
        L = float(np.hypot(dx, dy))
        return L, dx / L, dy / L

    def _gdl(self, nodo: int) -> list[int]:
        base = nodo * GDL_POR_NODO
        return [base, base + 1, base + 2]

    def resolver(self) -> Resultado2D:
        n = len(self.coords) * GDL_POR_NODO
        K = np.zeros((n, n))
        P = np.zeros(n)

        # Cargas nodales aplicadas.
        for nodo, (fx, fy, m) in self.cargas.items():
            P[self._gdl(nodo)] += [fx, fy, m]

        # Ensamble: rigidez y cargas equivalentes de barra, rotadas a global.
        datos = []
        for b in self.barras:
            L, c, s = self._geometria(b)
            T = rotacion(c, s)
            kl = k_local(b.E, b.A, b.I, L)
            peq_l = cargas_equivalentes(b.w, L)
            gdl = self._gdl(b.i) + self._gdl(b.j)
            K[np.ix_(gdl, gdl)] += T.T @ kl @ T
            P[gdl] += T.T @ peq_l
            datos.append((T, kl, peq_l, gdl))

        fijos = [
            g
            for nodo, restr in self.restricciones.items()
            for g, fijo in zip(self._gdl(nodo), restr)
            if fijo
        ]
        libres = [g for g in range(n) if g not in fijos]

        u = np.zeros(n)
        u[libres] = np.linalg.solve(K[np.ix_(libres, libres)], P[libres])

        reacciones = K @ u - P
        reacciones[libres] = 0.0

        fuerzas = [
            kl @ (T @ u[gdl]) - peq_l for (T, kl, peq_l, gdl) in datos
        ]

        return Resultado2D(
            u=u.reshape(-1, GDL_POR_NODO),
            reacciones=reacciones.reshape(-1, GDL_POR_NODO),
            fuerzas=fuerzas,
        )
