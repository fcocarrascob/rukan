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
en el propio `SeccionI` a partir de equilibrio y Navier. Las presiones de
contacto bajo zapata rígida excéntrica salen de Das, *Fundamentos de Ingeniería
Geotécnica*, 4.ª ed., §16.7 (ver `presion_zapata_rigida`). El criterio de
rigidez de una fundación superficial —Ec. (25)— y su longitud de cálculo salen
de NCh2369:2025, 3.ª ed., §10.1.4 y Tabla 10 (ver `lambda_l_nch2369`).
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
    "PresionZapata",
    "presion_zapata_rigida",
    "fraccion_apoyada",
    "excentricidad_para_fraccion",
    "k_viga",
    "ResultadoViga",
    "VigaSobreResortes",
    "lambda_l_nch2369",
    "espesor_limite_nch2369",
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


# ==================== ZAPATA RÍGIDA SOBRE SUELO SIN TRACCIÓN ================
# Presiones de contacto bajo una zapata **rígida** con carga excéntrica, en un
# suelo que no toma tracción. La notación es la de Das: `Q` carga vertical, `M`
# momento, `B` el lado en la dirección de la excentricidad y `L` el otro.


@dataclass
class PresionZapata:
    """Reparto de presiones bajo una zapata rígida, con su longitud de contacto."""

    q_max: float
    q_min: float
    a_contacto: float
    e: float
    B: float

    @property
    def despegada(self) -> bool:
        return self.a_contacto < self.B

    @property
    def fraccion_apoyada(self) -> float:
        return self.a_contacto / self.B


def presion_zapata_rigida(Q: float, M: float, B: float, L: float) -> PresionZapata:
    """Presiones de contacto bajo zapata rígida excéntrica, suelo sin tracción.

    Fuente: Das, B. M., *Fundamentos de Ingeniería Geotécnica*, 4.ª ed., §16.7,
    pp. 490-492 (transcritas de la página rasterizada, no de la capa de texto).

    Con ``e = M/Q`` (Ec. 16.19), mientras la resultante cae dentro del núcleo
    central el contacto es total y el reparto es lineal::

        q_máx = Q/(BL)·(1 + 6e/B)        (16.20)
        q_mín = Q/(BL)·(1 − 6e/B)        (16.21)

    En ``e = B/6``, ``q_mín`` se anula. Pasado ese punto la Ec. (16.21) daría
    tracción, y como el suelo no la toma, la zapata **se despega**: el reparto
    pasa a ser un triángulo apoyado sobre parte de la base (Das, Fig. 16.6a)::

        q_máx = 4Q / (3L(B − 2e))        (16.22)

    La **longitud de contacto** no está tabulada en Das, pero sale de su propia
    Ec. (16.22) por estática, sin agregar hipótesis: la resultante del triángulo
    vale ``½·q_máx·a·L`` y tiene que igualar a ``Q``, así que

        a = 2Q/(q_máx·L) = 2Q·3L(B − 2e)/(4Q·L) = 3·(B/2 − e)

    —que es lo mismo que exigir que el centroide del triángulo, a ``a/3`` del
    borde, caiga bajo la línea de acción de ``Q``, a ``B/2 − e`` de ese borde—.

    **El reparto no depende de la rigidez del suelo.** No aparece acá ningún
    módulo de balasto: para una zapata rígida las presiones salen de equilibrio
    y de la hipótesis de contacto lineal. ``k_s`` fija el asentamiento, no el
    reparto.
    """
    if Q <= 0.0:
        raise ValueError("Q debe ser una compresión positiva")
    e = M / Q
    if abs(e) >= B / 2.0:
        raise ValueError(
            f"e = {e:.4g} m cae fuera de la zapata (B/2 = {B / 2:.4g} m): "
            "no hay equilibrio posible, la zapata vuelca"
        )
    e = abs(e)  # el reparto es simétrico; q_máx va al borde que se comprime
    if e <= B / 6.0:
        q_max = Q / (B * L) * (1.0 + 6.0 * e / B)
        q_min = Q / (B * L) * (1.0 - 6.0 * e / B)
        a = B
    else:
        q_max = 4.0 * Q / (3.0 * L * (B - 2.0 * e))
        q_min = 0.0
        a = 3.0 * (B / 2.0 - e)
    return PresionZapata(q_max=q_max, q_min=q_min, a_contacto=a, e=e, B=B)


def fraccion_apoyada(e: float, B: float) -> float:
    """Fracción de la base en compresión, para excentricidad ``e``.

    Derivada de la longitud de contacto ``a = 3(B/2 − e)`` de
    `presion_zapata_rigida`, saturada en 1 dentro del núcleo central::

        a/B = mín(1, 3/2 − 3·e/B)

    Es la magnitud que NCh2369:2025 §10.1.4 acota (80 % en fundaciones estándar
    menores, 50 % en mayores). **La norma pide área apoyada, no excentricidad**:
    la traducción a ``e/B`` es esta derivación, no texto normativo.
    """
    if abs(e) >= B / 2.0:
        return 0.0
    return min(1.0, 1.5 - 3.0 * abs(e) / B)


def excentricidad_para_fraccion(f: float, B: float) -> float:
    """Excentricidad que deja apoyada exactamente la fracción ``f`` de la base.

    Inversa de `fraccion_apoyada` en la rama despegada: ``e/B = (3/2 − f)/3``.
    Para ``f = 1`` devuelve ``B/6`` —el núcleo central—, y es lo que permite
    poner el 80 % y el 50 % de NCh2369 §10.1.4 en la misma escala.
    """
    if not 0.0 < f <= 1.0:
        raise ValueError("la fracción apoyada vive en (0, 1]")
    return (1.5 - f) / 3.0 * B


# ================ VIGA SOBRE RESORTES QUE NO TOMAN TRACCIÓN =================
# La zapata rígida de `presion_zapata_rigida` es el caso límite EI → ∞. Cuando
# la fundación es flexible el reparto ya no es plano y hay que resolver la viga
# sobre la cama de resortes. Esto es rigidez directa en numpy puro, con el
# contacto tratado por **conjunto activo**.
#
# El algoritmo no es una elección de estilo: es el que NCh2369:2025 §10.1.4
# prescribe en palabras para una fundación que no clasifica como rígida —«el
# análisis estructural de la losa requiere la utilización de métodos o análisis
# numéricos, que incorporen, por ejemplo, una cama de resortes, teniendo la
# precaución de verificar que en el análisis no resulten resortes traccionados.
# De existir resortes traccionados, éstos se deben anular»— (leído en la página
# rasterizada, PDF p.126, impresa 119).

GDL_VIGA = 2  # (v, θ) por nodo: flexión pura, sin axial


def k_viga(EI: float, L: float) -> np.ndarray:
    """Rigidez 4×4 de flexión de una barra Euler-Bernoulli: GDL ``(v_i, θ_i, v_j, θ_j)``.

    Es el mismo bloque de flexión que ya vive dentro de `k_local`, extraído a
    2 GDL por nodo porque acá no hay axial: la viga no se estira y los resortes
    no dan rigidez horizontal. `test_lab.py` verifica que los dos coincidan
    término a término, así que este atajo no introduce una segunda verdad.
    """
    return EI * np.array(
        [
            [12 / L**3, 6 / L**2, -12 / L**3, 6 / L**2],
            [6 / L**2, 4 / L, -6 / L**2, 2 / L],
            [-12 / L**3, -6 / L**2, 12 / L**3, -6 / L**2],
            [6 / L**2, 2 / L, -6 / L**2, 4 / L],
        ]
    )


@dataclass
class ResultadoViga:
    """Reparto de presiones bajo una viga sobre resortes sin tracción.

    Las claves calcan las del ``modelo()`` de OpenSees de la nota 03, para que
    las dos rutas se comparen término a término sin traducción intermedia.
    """

    x: np.ndarray  # coordenada de cada nodo
    q: np.ndarray  # presión de contacto, positiva en compresión
    activos: np.ndarray  # máscara booleana: resortes que quedaron comprimidos
    v: np.ndarray  # descenso de cada nodo (positivo hacia arriba)
    trib: np.ndarray  # longitud tributaria de cada resorte
    ancho: float
    iteraciones: int

    @property
    def q_max(self) -> float:
        return float(self.q.max())

    @property
    def q_borde(self) -> float:
        """Presión en el borde x = B. Con e > 0 coincide con `q_max` en el caso
        rígido, pero es un punto fijo y por lo tanto comparable entre casos."""
        return float(self.q[-1])

    @property
    def a_contacto(self) -> float:
        return float(self.trib[self.activos].sum())

    @property
    def fraccion_apoyada(self) -> float:
        return self.a_contacto / float(self.trib.sum())

    @property
    def reaccion(self) -> float:
        """Resultante de las presiones. Debe dar la carga vertical aplicada."""
        return float((self.q * self.trib * self.ancho).sum())


@dataclass
class VigaSobreResortes:
    """Viga sobre cama de resortes verticales que **no toman tracción**.

    Rigidez directa (2 GDL por nodo) más **conjunto activo** iterativo: se
    resuelve con todos los resortes puestos, se apagan los que quedaron
    traccionados, y se repite hasta que el conjunto de resortes comprimidos deja
    de cambiar. Es el método que NCh2369:2025 §10.1.4 describe en palabras (ver
    el comentario del bloque).

    Convenciones, heredadas del resto del módulo: ``v`` positivo **hacia
    arriba**, así que un resorte comprimido es el de un nodo que baja (``v < 0``)
    y su presión vale ``q = −k_v·v``.

    La rigidez de cada resorte es ``k_v`` por su **área tributaria**, que en los
    dos nodos de borde vale la mitad. Con rigidez uniforme la resultante de las
    presiones no daría la carga aplicada — el mismo gotcha que la nota 03 pagó
    del lado de OpenSees.

    Este solver **no comparte una línea con OpenSees**: ensamble propio,
    contacto por conjunto activo en vez de un material ``ENT`` con Newton. Esa
    es la condición para que la comparación signifique algo.
    """

    B: float  # largo de la viga
    n: int  # divisiones (deja n+1 nodos y n+1 resortes)
    EI: float
    k_v: float  # módulo de balasto, F/L³
    ancho: float = 1.0  # ancho fuera del plano

    MAX_ITER = 100

    def malla(self) -> tuple[np.ndarray, np.ndarray]:
        """Coordenadas nodales y longitud tributaria de cada resorte."""
        h = self.B / self.n
        xs = np.arange(self.n + 1) * h
        trib = np.full(self.n + 1, h)
        trib[0] = trib[-1] = h / 2.0
        return xs, trib

    def resolver(self, fuerzas: np.ndarray, momentos: np.ndarray | None = None) -> ResultadoViga:
        """Resuelve con cargas nodales ``fuerzas`` (positivas hacia arriba) y ``momentos``.

        Una carga vertical hacia abajo entra como ``fuerzas < 0``, igual que en
        el resto del módulo.
        """
        xs, trib = self.malla()
        n_nodos = self.n + 1
        if fuerzas.shape != (n_nodos,):
            raise ValueError(f"`fuerzas` debe tener {n_nodos} valores, uno por nodo")
        if momentos is None:
            momentos = np.zeros(n_nodos)

        h = self.B / self.n
        k_resorte = self.k_v * trib * self.ancho
        k_barra = k_viga(self.EI, h)

        # Rigidez de la viga sola: se ensambla una vez, no cambia al iterar.
        n_gdl = n_nodos * GDL_VIGA
        K_viga = np.zeros((n_gdl, n_gdl))
        for k in range(self.n):
            gdl = [2 * k, 2 * k + 1, 2 * k + 2, 2 * k + 3]
            K_viga[np.ix_(gdl, gdl)] += k_barra

        P = np.zeros(n_gdl)
        P[0::2] = fuerzas
        P[1::2] = momentos

        activos = np.ones(n_nodos, dtype=bool)
        vistos: list[tuple[bool, ...]] = []

        for iteracion in range(1, self.MAX_ITER + 1):
            if activos.sum() < 2:
                raise RuntimeError(
                    "quedan menos de 2 resortes comprimidos: la viga es un "
                    "mecanismo (la fundación vuelca, no hay equilibrio posible)"
                )
            K = K_viga.copy()
            K[np.arange(n_nodos) * 2, np.arange(n_nodos) * 2] += np.where(
                activos, k_resorte, 0.0
            )
            try:
                u = np.linalg.solve(K, P)
            except np.linalg.LinAlgError as err:  # pragma: no cover - guarda
                raise RuntimeError(
                    f"matriz singular con {activos.sum()} resortes activos"
                ) from err

            v = u[0::2]
            # Un resorte solo trabaja si su nodo bajó. `v <= 0` reactiva los que
            # habían quedado apagados y vuelven a apoyar, así que el conjunto no
            # es monótono decreciente y hace falta la detección de ciclo.
            nuevos = v <= 0.0
            if np.array_equal(nuevos, activos):
                q = np.where(activos, -self.k_v * v, 0.0)
                return ResultadoViga(
                    x=xs, q=q, activos=activos, v=v, trib=trib,
                    ancho=self.ancho, iteraciones=iteracion,
                )
            firma = tuple(bool(b) for b in nuevos)
            if firma in vistos:
                raise RuntimeError(
                    f"el conjunto activo entró en ciclo en la iteración {iteracion}: "
                    "el contacto no se estabiliza con esta malla"
                )
            vistos.append(firma)
            activos = nuevos

        raise RuntimeError(
            f"el conjunto activo no convergió en {self.MAX_ITER} iteraciones"
        )


# ===================== EC. (25) DE NCh2369:2025 §10.1.4 =====================


def lambda_l_nch2369(L: float, k_v: float, E: float, espesor: float) -> float:
    """``λ·L`` de la Ec. (25): una fundación superficial es **rígida** si vale ≤ 1.

    Fuente: NCh2369:2025, 3.ª ed., §10.1.4, Ec. (25) — transcrita de la **página
    rasterizada** del PDF (p.125 del archivo, impresa 118), no de la capa de
    texto::

        L · ⁴√( k_v / (4·E·I) )  ≤  1                    (25)

    en que, con las palabras de la norma:

    * ``I = e³/12``, momento de inercia **por unidad de longitud** de fundación (m³);
    * ``e`` = altura o espesor de la fundación (m);
    * ``E`` = módulo de deformación del material constitutivo de la fundación (tonf/m²);
    * ``k_v`` = rigidez vertical **sísmica** del suelo para efectos de este cálculo (tonf/m³);
    * ``L`` = **longitud de cálculo, definida en la Tabla 10** (p.131 del archivo,
      impresa 124) — y no es el largo de la fundación: para una zapata aislada
      la fila que aplica es «Zarpa», o sea la distancia entre el borde de la
      fundación y el borde exterior de la columna o muro.

    Dos advertencias de notación, ambas trampas reales:

    * La norma llama ``e`` al **espesor**; Das y la nota 03 llaman ``e`` a la
      **excentricidad**. Acá el argumento se llama ``espesor`` a propósito.
    * La norma la escribe en tonf, pero la expresión es **homogénea
      dimensionalmente** (``k_v/(E·I)`` tiene unidades de 1/L⁴), así que sirve
      cualquier sistema consistente. Este módulo trabaja en kN y m.
    """
    if min(L, k_v, E, espesor) <= 0.0:
        raise ValueError("L, k_v, E y el espesor deben ser positivos")
    I = espesor**3 / 12.0
    return L * (k_v / (4.0 * E * I)) ** 0.25


def espesor_limite_nch2369(L: float, k_v: float, E: float) -> float:
    """Espesor al que la Ec. (25) da exactamente ``λ·L = 1``: el umbral rígido/flexible.

    Se despeja de `lambda_l_nch2369`: con ``λL = 1`` es ``EI = k_v·L⁴/4``, y con
    ``I = e³/12`` queda ``e = ∛(12·k_v·L⁴/(4E)) = ∛(3·k_v·L⁴/E)``.

    Crece como ``L^(4/3)`` —por eso la fila de Tabla 10 que se elija cambia el
    veredicto tanto— y como ``k_v^(1/3)``.
    """
    if min(L, k_v, E) <= 0.0:
        raise ValueError("L, k_v y E deben ser positivos")
    return (3.0 * k_v * L**4 / E) ** (1.0 / 3.0)
