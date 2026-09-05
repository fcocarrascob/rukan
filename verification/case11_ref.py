"""Caso 11 — el camino independiente: rigidez directa 2D en numpy puro.

**No importa `rukan` ni `openseespy`.** Es la regla que el laboratorio de este
repo no negocia (`CLAUDE.md` § «Las dos líneas de contenido», regla 2): si la
referencia compartiera código con lo verificado, los dos se equivocarían igual y
la tabla daría error 0 % sin decir nada. Acá hace falta más que nunca, porque el
patrón de referencia habitual de `verification/` —SAP2000— no está disponible en
este equipo, así que el contraste se sostiene sobre dos patas: los números que la
serie de memos ya publica, y esta formulación.

Lo único que comparte con el modelo de OpenSees es `case11_data`, que es
**geometría y secciones**, no análisis — el mismo contrato que `case10_data`.

La formulación es otra: pórtico plano de tres GDL por nudo (u, v, θ) ensamblado a
mano, en el plano Y-Z, contra el dominio 3D de seis GDL que arma `rukan.engine`.
Las dos discretizan el alma variable igual —un tramo prismático con la sección de
su punto medio—, porque eso es un dato del caso y no del método.
"""

from __future__ import annotations

import math

import numpy as np

import case11_data as D


def _k_barra(p1, p2, E, A, I):
    """Rigidez de una barra de pórtico plano: `(k_global, T, k_local)`."""
    L = math.dist(p1, p2)
    c, s = (p2[0] - p1[0]) / L, (p2[1] - p1[1]) / L
    ea, ei = E * A / L, E * I / L ** 3
    kl = np.array([
        [ea, 0, 0, -ea, 0, 0],
        [0, 12 * ei, 6 * ei * L, 0, -12 * ei, 6 * ei * L],
        [0, 6 * ei * L, 4 * ei * L * L, 0, -6 * ei * L, 2 * ei * L * L],
        [-ea, 0, 0, ea, 0, 0],
        [0, -12 * ei, -6 * ei * L, 0, 12 * ei, -6 * ei * L],
        [0, 6 * ei * L, 2 * ei * L * L, 0, -6 * ei * L, 4 * ei * L * L],
    ])
    R = np.array([[c, s, 0.0], [-s, c, 0.0], [0.0, 0.0, 1.0]])
    T = np.zeros((6, 6))
    T[:3, :3] = R
    T[3:, 3:] = R
    return T.T @ kl @ T, T, kl


class Marco2D:
    """Marco plano en (y, z), ensamblado y resuelto a mano."""

    def __init__(self, E: float = D.E_STEEL) -> None:
        self.E = E
        self.xy: list[tuple[float, float]] = []
        self.bar: list[tuple[int, int, float, float]] = []
        self.u = np.zeros(0)

    def nodo(self, y: float, z: float) -> int:
        self.xy.append((y, z))
        return len(self.xy) - 1

    def barra(self, i: int, j: int, A: float, I: float) -> int:
        self.bar.append((i, j, A, I))
        return len(self.bar) - 1

    def resolver(self, fijos: set[int], cargas: dict[tuple[int, int], float]):
        n = len(self.xy)
        K = np.zeros((3 * n, 3 * n))
        for (i, j, A, I) in self.bar:
            ke, _, _ = _k_barra(self.xy[i], self.xy[j], self.E, A, I)
            g = [3 * i, 3 * i + 1, 3 * i + 2, 3 * j, 3 * j + 1, 3 * j + 2]
            K[np.ix_(g, g)] += ke
        F = np.zeros(3 * n)
        for (nd, d), v in cargas.items():
            F[3 * nd + d] += v
        libres = [k for k in range(3 * n) if k not in fijos]
        u = np.zeros(3 * n)
        u[libres] = np.linalg.solve(K[np.ix_(libres, libres)], F[libres])
        self.u = u
        return u

    def fuerzas(self, b: int) -> np.ndarray:
        """Fuerzas de extremo de la barra `b` en ejes locales: `[N,V,M, N,V,M]`."""
        i, j, A, I = self.bar[b]
        _, T, kl = _k_barra(self.xy[i], self.xy[j], self.E, A, I)
        g = [3 * i, 3 * i + 1, 3 * i + 2, 3 * j, 3 * j + 1, 3 * j + 2]
        return kl @ (T @ self.u[g])


def _malla(cortes: list[float], nsub: int) -> list[float]:
    out = [cortes[0]]
    for a, b in zip(cortes[:-1], cortes[1:]):
        out += [a + (b - a) * (i + 1) / nsub for i in range(nsub)]
    return out


def marco(nsub: int = 28, escalonada: bool = False):
    """El marco transversal del caso. Devuelve `(m, idx, fijos, zc, ncol)`.

    `idx` trae los nudos que los contrastes nombran: las dos bases, los dos
    aleros y los dos nudos del nivel del riel.
    """
    m = Marco2D()
    idx: dict[str, int] = {}
    zc = _malla([0.0, D.H_ASIENTO, D.Z_RIEL, D.H_ALERO], nsub)
    for l, y in (("A", 0.0), ("B", D.LUZ)):
        ns = [m.nodo(y, z) for z in zc]
        idx["base" + l], idx["alero" + l] = ns[0], ns[-1]
        idx["riel" + l] = ns[zc.index(D.Z_RIEL)]
        for k in range(len(ns) - 1):
            zm = 0.5 * (zc[k] + zc[k + 1])
            if escalonada and zm < D.H_ASIENTO:
                A, _, ix, _, _ = D.comp_props(zm)
            else:
                A, ix, _, _ = D.i_props(D.d_col(zm), D.COL_BF, D.COL_TF, D.COL_TW)
            m.barra(ns[k], ns[k + 1], A, ix)
    ncol = len(zc) - 1
    sj = _malla([j * D.B_PAN_TECHO for j in range(D.NJ + 1)], nsub)
    nr = [idx["aleroA"]] + [m.nodo(*D.yz_raf(s)) for s in sj[1:-1]] + [idx["aleroB"]]
    for k in range(len(sj) - 1):
        sm = 0.5 * (sj[k] + sj[k + 1])
        A, ix, _, _ = D.i_props(D.d_raf(min(sm, 2 * D.L_RAFTER - sm)),
                                D.RAF_BF, D.RAF_TF, D.RAF_TW)
        m.barra(nr[k], nr[k + 1], A, ix)
    fijos: set[int] = set()
    for l in "AB":
        b = idx["base" + l]
        fijos |= {3 * b, 3 * b + 1, 3 * b + 2}
    return m, idx, fijos, zc, ncol


def rigidez(nodos: list[str], nsub: int = 28, escalonada: bool = False) -> float:
    """Rigidez lateral `H / δ` con `H = 1` repartido entre `nodos`, medida en el primero.

    Con `nodos = ["aleroA", "aleroB"]` es la rigidez de **sway**, que es la que
    un modo lateral tiene. Con `["aleroA"]` es la rigidez **puntual** de ese
    alero, que incluye la parte antisimétrica —el marco abriéndose— y no es una
    rigidez lateral. La diferencia entre las dos es lo que este caso mide.
    """
    m, idx, fijos, _, _ = marco(nsub, escalonada)
    u = m.resolver(fijos, {(idx[n], 0): 1.0 / len(nodos) for n in nodos})
    return 1.0 / u[3 * idx[nodos[0]]]


def diagrama_columna(nodos: list[str], nsub: int = 28):
    """`(M_base/M_nudo, y_inflexión)` de la columna A bajo el empuje dado."""
    m, idx, fijos, zc, ncol = marco(nsub)
    m.resolver(fijos, {(idx[n], 0): 1.0 / len(nodos) for n in nodos})
    Ms = [m.fuerzas(k)[2] for k in range(ncol)]
    m_nudo = m.fuerzas(ncol - 1)[5]
    y = float("nan")
    for i in range(ncol - 1):
        if Ms[i] * Ms[i + 1] < 0.0:
            y = zc[i] + (zc[i + 1] - zc[i]) * abs(Ms[i]) / (abs(Ms[i]) + abs(Ms[i + 1]))
    return abs(Ms[0] / m_nudo), y


def sa_h(T: float) -> float:
    """Espectro de referencia horizontal de NCh2369, con los parámetros del 04."""
    return D.AR_S * (1.0 + D.R_S * (T / D.T_0) ** D.P_SUELO) / (1.0 + (T / D.T_0) ** D.Q_S)
