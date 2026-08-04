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

Secciones: el eje de flexión es ``y``, medido desde el centro de gravedad, y el
ancho ``b(y)`` es constante por tramos. Momento positivo = tracción en la fibra
inferior. Ver `SeccionI` para la derivación de M(φ).

Fuente: Cook, Malkus & Plesha, *Concepts and Applications of Finite Element
Analysis* — matriz de rigidez de viga-columna plana y vector de cargas
consistente para carga uniforme. La flexión elastoplástica de sección se deriva
en el propio `SeccionI` a partir de equilibrio y Navier.
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
    "SeccionI",
    "MallaFibras",
    "discretizar_I",
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


# ============================== SECCIONES =================================
# Flexión de una sección doblemente simétrica de material elastoplástico
# perfecto. El eje de flexión es y (medido desde el centro de gravedad) y el
# ancho b(y) es constante por tramos.


@dataclass
class SeccionI:
    """Perfil I doblemente simétrico definido por sus planchas.

    ``bf`` × ``tf`` es cada ala, ``tw`` el espesor del alma y ``h`` la altura
    total (alas incluidas). Un rectángulo macizo de ancho ``bf`` es el caso
    degenerado ``tf = h/2`` (el alma desaparece y ``a = 0``).

    **Propiedades exactas.** Con ``d = h/2`` la semialtura y ``a = d − tf`` el
    borde interior del ala::

        Z = bf(d² − a²) + tw·a²                 (módulo plástico)
        I = (2/3)·[bf·d³ − (bf − tw)·a³]        (inercia)
        S = I/d                                 (módulo elástico)

    **Momento a curvatura φ, material elastoplástico perfecto.** La distribución
    de deformaciones es lineal (Navier), ``ε(y) = φ·y``, y la de tensiones se
    satura en ``±Fy`` fuera del núcleo elástico, cuya semiprofundidad es::

        c = ε_y/φ,   con ε_y = Fy/E

    Conviene escribir M como el **déficit** respecto del bloque totalmente
    plastificado ``Mp = Fy·Z``: dentro del núcleo la tensión vale ``Fy·y/c`` en
    vez de ``Fy``, así que falta ``Fy·(1 − y/c)`` en cada fibra::

        M(φ) = Mp − 2·Fy·∫₀^c (1 − y/c)·y·b(y) dy

    Integrando, con ``b(y) = tw`` para ``y < a`` y ``b(y) = bf`` para ``y > a``:

    * ``c ≥ d`` — todavía elástico::

          M = E·I·φ

    * ``a < c < d`` — la plastificación aún no sale del ala::

          M = Fy·[ Z − 2( tw(a²/2 − a³/3c) + bf((c² − a²)/2 − c²/3 + a³/3c) ) ]

    * ``c ≤ a`` — el ala está toda plastificada y el núcleo vive en el alma::

          M = Fy·[ Z − tw·c²/3 ]

    Los tres tramos empalman: en ``c = a`` el segundo se reduce al tercero, y en
    ``c = d`` se reduce a ``Fy·(2/3)[bf·d² − (bf − tw)a³/d] = Fy·S = My``. Y
    como el núcleo elástico nunca desaparece (``c = ε_y/φ > 0`` para todo φ
    finito), **Mp es una asíntota**: se alcanza solo en el límite ``φ → ∞``, y el
    déficit decae como ``1/φ²``.

    Se deriva acá en vez de citarse porque no es una disposición normativa sino
    mecánica de sección: sale de equilibrio, Navier y la ley constitutiva, y así
    queda auditable sin depender de ningún libro.
    """

    bf: float
    tf: float
    tw: float
    h: float

    @property
    def d(self) -> float:
        """Semialtura de la sección."""
        return self.h / 2.0

    @property
    def a(self) -> float:
        """Borde interior del ala, medido desde el centro de gravedad."""
        return self.d - self.tf

    @property
    def A(self) -> float:
        return 2.0 * self.bf * self.tf + 2.0 * self.a * self.tw

    @property
    def I(self) -> float:  # noqa: E743 - nombre de ingeniería, no ambiguo acá
        return (2.0 / 3.0) * (self.bf * self.d**3 - (self.bf - self.tw) * self.a**3)

    @property
    def S(self) -> float:
        return self.I / self.d

    @property
    def Z(self) -> float:
        return self.bf * (self.d**2 - self.a**2) + self.tw * self.a**2

    @property
    def factor_forma(self) -> float:
        """Z/S — cuánto momento queda por sobre la primera fluencia."""
        return self.Z / self.S

    def phi_y(self, Fy: float, E: float) -> float:
        """Curvatura de primera fluencia: la fibra extrema llega a ``ε_y``."""
        return Fy / E / self.d

    def momento(self, phi: float, Fy: float, E: float) -> float:
        """Momento flector exacto a curvatura ``phi`` (elastoplástico perfecto)."""
        if phi <= 0.0:
            return 0.0
        c = Fy / E / phi  # semiprofundidad del núcleo elástico
        if c >= self.d:
            return E * self.I * phi
        if c <= self.a:
            return Fy * (self.Z - self.tw * c**2 / 3.0)
        a, bf, tw = self.a, self.bf, self.tw
        deficit = 2.0 * (
            tw * (a**2 / 2.0 - a**3 / (3.0 * c))
            + bf * ((c**2 - a**2) / 2.0 - c**2 / 3.0 + a**3 / (3.0 * c))
        )
        return Fy * (self.Z - deficit)


@dataclass
class MallaFibras:
    """Una sección discretizada en fibras: centroide ``y`` y área de cada una.

    Reproduce lo que hace una ``section('Fiber', …)`` de OpenSees, pero en numpy,
    para poder predecir *qué va a dar una malla* sin ejecutar el motor.

    El punto de la nota 02 vive acá: con fibras rectangulares al centroide de su
    franja, ``Σ Aᵢ·|yᵢ|`` reproduce **exactamente** ``∫|y| dA`` —y por lo tanto
    ``Z`` y ``Mp``—, pero ``Σ Aᵢ·yᵢ²`` **no** reproduce ``∫y² dA``: a cada franja
    le falta su término de Steiner ``b·t³/12``. La malla acierta la resistencia y
    subestima la rigidez.
    """

    y: np.ndarray
    area: np.ndarray

    @property
    def Z_fib(self) -> float:
        return float(np.sum(self.area * np.abs(self.y)))

    @property
    def I_fib(self) -> float:
        return float(np.sum(self.area * self.y**2))

    def momento(self, phi: float, Fy: float, E: float) -> float:
        """``M = Σ Aᵢ·σ(φ·yᵢ)·yᵢ`` con σ elastoplástica perfecta."""
        sigma = np.clip(E * phi * self.y, -Fy, Fy)
        return float(np.sum(self.area * sigma * self.y))


def _franjas(y0: float, y1: float, ancho: float, n: int) -> tuple[np.ndarray, np.ndarray]:
    """Parte ``[y0, y1]`` en ``n`` franjas: centroides y áreas.

    Es la partición de ``patch('rect', mat, n, 1, yI, zI, yJ, zJ)`` de OpenSees.
    """
    bordes = np.linspace(y0, y1, n + 1)
    centros = 0.5 * (bordes[:-1] + bordes[1:])
    areas = np.full(n, ancho * (y1 - y0) / n)
    return centros, areas


def discretizar_I(sec: SeccionI, n_ala: int, n_alma: int) -> MallaFibras:
    """Discretiza un ``SeccionI`` en tres patches: ala inferior, alma, ala superior.

    La partición calca la de los ``patch('rect', …)`` que usa la nota en
    OpenSees. Si las dos no coinciden franja a franja, la comparación
    fibras-numpy vs fibras-OpenSees deja de significar algo.
    """
    d, a = sec.d, sec.a
    tramos = [
        _franjas(-d, -a, sec.bf, n_ala),
        _franjas(-a, a, sec.tw, n_alma),
        _franjas(a, d, sec.bf, n_ala),
    ]
    y = np.concatenate([t[0] for t in tramos])
    area = np.concatenate([t[1] for t in tramos])
    return MallaFibras(y=y, area=area)
