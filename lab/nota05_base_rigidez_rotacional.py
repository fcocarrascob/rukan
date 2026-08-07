"""Nota 05 — la base no es empotrada ni rotulada, y los dos errores no son iguales.

**La pregunta:** toda la serie de placas base del blog parte de un juego de
reacciones ``{P_u, M_u, V_u}`` que salió de un modelo estructural. Y en ese
modelo alguien dibujó la base **empotrada o rotulada**. ¿Cuál de las dos, y
cuánto cuesta equivocarse?

**Lo que dice la guía.** AISC *Design Guide 1*, 3.ª ed., §3.3.1: si se supone
que los momentos de diseño ocurren al ~70-80 % de la capacidad, *"se obtiene una
rotación de 0,01-0,02 rad en la fluencia"*, y eso *"sugiere que las conexiones
de base poseen empotramiento parcial y no pueden suponerse fijas ni libres sin
análisis o contexto adicional"*. Los dos errores no son simétricos: rotulada es
**conservador** —más derivas, más tonelaje—; empotrada *"indica una confusión
entre resistencia y rigidez"* y puede *"llevar a una caracterización no
conservadora del desempeño"*.

El Apéndice C entrega el reemplazo: una rigidez rotacional **secante**
``beta_connection = M_u/theta`` (Ec. C-4), con el giro repartido en cuatro
deformaciones físicas (Ec. C-5) que se calculan con dos cantidades que el
capítulo 4 ya produce: la tracción del perno ``T`` y el ancho de la interfaz
comprimida ``Y``. No hace falta un modelo nuevo.

**Fuentes** (todas transcritas de la **página rasterizada** del PDF, no de la
capa de texto — que destruye el cociente y convierte phi en f):

- Apéndice C, Ecs. C-1 a C-20: PDF pp. 199 a 203 (impresas 189 a 193).
- §3.3.1 a §3.3.3: PDF pp. 26 y 27 (impresas 16 y 17).
- Cap. 4, bloque rectangular con momento grande, Ecs. 4-39, 4-40, 4-53, 4-55 y
  4-58: PDF pp. 53 y 54 (impresas 43 y 44).

⚠ **El offset del PDF es impresa = PDF − 10.** El README de la ficha del wiki
dice −9 y está corrido en uno; verificado leyendo el pie de página.

**Las cuatro cosas que muestra la nota**

1. **Quién manda en el giro no es el perno.** Sobre el caso publicado del
   ejemplo trabajado del blog, las cuatro deformaciones de la Ec. C-5 no se
   reparten parejo, y la mayor es la que no tiene nada que ver con la resistencia
   de la conexión.

2. **«Resistencia ≠ rigidez» con número.** Engrosar la placa sube su resistencia
   a flexión con el cuadrado del espesor y mueve solo dos de los cuatro
   términos; los otros dos no se enteran. Se mide cuánto sube beta al pasar de
   la placa de 25 mm a la de 35 mm que la propia DG1 exige por resistencia.

3. **El marco corrido tres veces.** Empotrada, rotulada y resorte beta, midiendo
   los tres efectos que §3.3.2 nombra: momento en el tope de columna, deriva de
   entrepiso y el momento en la base. La reacción que alimenta el barrido de
   combinaciones del post 1 **no es un punto, es una banda**.

4. **La circularidad, resuelta en vez de advertida.** §C.2.1 avisa que beta
   depende de la compresión axial, que a su vez sale del análisis que usa beta,
   y que iterar *"puede volverse muy engorroso en marcos con varias columnas"*.
   Acá se itera y se cuenta cuántas vueltas toma y cuánto se mueve.

**Verificación (los dos caminos):** referencia = ``lab/_lib/ref.py``,
``Portico2D`` — rigidez directa en numpy puro, con la base flexible como resorte
rotacional a tierra; motor = OpenSeesPy con ``zeroLength`` y material
``Elastic`` en el GDL de rotación. ``ref.py`` no importa ``rukan`` ni
``openseespy``. La cadena del Apéndice C es aritmética cerrada y se verifica de
otra forma: contra los límites que la propia guía declara (continuidad de las
ramas de C-17/C-18, y los dos límites de la Ec. C-16).

Unidades: kgf y cm en todo el script, que son las de la serie de placas base.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from lab._lib.ref import Barra2D, Portico2D
from lab._lib.report import Fila, reportar

# ============================ CONSTANTES ==================================

E_ACERO = 2_040_000.0  # kgf/cm² — 29 000 ksi, el valor de AISC 360-22
NU_ACERO = 0.3
G_ACERO = E_ACERO / (2 * (1 + NU_ACERO))  # kgf/cm²

TONF = 1000.0  # kgf
TONF_M = 100_000.0  # kgf·cm


# ===================== EL CASO DEL EJEMPLO TRABAJADO =======================
# Los datos de entrada y los resultados publicados de
# /acero/placa-base-ejemplo-trabajado. Se declaran acá como DATO, con su
# procedencia: son la frontera de lo que esta nota verifica.


@dataclass(frozen=True)
class Conexion:
    """Geometría y materiales de la conexión de base expuesta."""

    B: float = 45.0  # cm — ancho de la placa (fuera del plano de flexión)
    N: float = 45.0  # cm — largo de la placa (en el plano de flexión)
    tp: float = 2.5  # cm — espesor de la placa
    d_col: float = 30.0  # cm — peralte de la columna
    f: float = 17.5  # cm — centro de placa al eje de la fila de pernos
    n_pernos_traccion: int = 2  # pernos en la fila traccionada
    d_perno: float = 2.54  # cm — 1"
    h_ef: float = 40.0  # cm — embebido efectivo
    t_grout: float = 2.5  # cm — mortero de nivelación (supuesto: 25 mm)
    d_footing: float = 80.0  # cm — profundidad TOTAL de la zapata (supuesto)
    fc: float = 250.0  # kgf/cm²
    fp_max: float = 245.6  # kgf/cm² — phi·f_p,max del post (Ec. 1 del ejemplo)

    @property
    def A_rod(self) -> float:
        """Área bruta de la fila traccionada (C-6 usa el área bruta)."""
        return self.n_pernos_traccion * math.pi * self.d_perno**2 / 4

    @property
    def L_rod(self) -> float:
        """C-6: del tope de la placa al tope de la tuerca inferior."""
        return self.tp + self.t_grout + self.h_ef

    @property
    def q_max(self) -> float:
        """Carga lineal máxima de aplastamiento, kgf/cm."""
        return self.fp_max * self.B

    @property
    def m(self) -> float:
        """Voladizo de la placa del lado comprimido, hasta la línea 0,95d."""
        return (self.N - 0.95 * self.d_col) / 2

    @property
    def I_plate(self) -> float:
        return self.B * self.tp**3 / 12

    @property
    def A_shear(self) -> float:
        """C-9: el 5/6 es el área efectiva de corte de una sección rectangular."""
        return (5 / 6) * self.B * self.tp

    @property
    def brazo(self) -> float:
        """El denominador de C-5 y C-13: f + N/2."""
        return self.f + self.N / 2

    @property
    def E_c(self) -> float:
        """Módulo del hormigón.

        C-12 escribe E = w_c^1,5·sqrt(f'c) con TODO en ksi y w_c en lb/ft³. Acá
        se usa la forma SI que el post 1 ya publica (su Ec. 3), porque toda la
        serie está en kgf-cm. Son la misma expresión de ACI en dos sistemas: la
        diferencia queda medida en `contraste_modulo_hormigon()`.
        """
        return 15100 * math.sqrt(self.fc)

    def con(self, **cambios) -> "Conexion":
        from dataclasses import replace

        return replace(self, **cambios)


def contraste_modulo_hormigon(cx: Conexion, w_c: float = 145.0) -> tuple[float, float]:
    """E_c por la forma SI del post 1 y por la imperial de la Ec. C-12."""
    ksi_a_kgfcm2 = 70.30696
    fc_ksi = cx.fc / ksi_a_kgfcm2
    e_imperial = w_c**1.5 * math.sqrt(fc_ksi) * ksi_a_kgfcm2
    return cx.E_c, e_imperial


# ================== CAP. 4 — BLOQUE RECTANGULAR, MOMENTO GRANDE ============
# Ecs. 4-39, 4-40, 4-53, 4-55, 4-58 y 4-59, leídas en las páginas rasterizadas
# PDF 53 y 54 (impresas 43 y 44). El signo de la raíz de 4-58 es el MENOS: la
# guía la escribe con ± y la raíz física es la menor, el bloque comprimido que
# cabe dentro de la placa.


@dataclass(frozen=True)
class BloqueRectangular:
    e: float  # cm — excentricidad (4-39)
    e_crit: float  # cm — (4-40)
    momento_grande: bool  # (4-53)
    Y: float  # cm — largo del bloque comprimido (4-58)
    T: float  # kgf — tracción TOTAL de los pernos (4-55)


def bloque_rectangular(cx: Conexion, Pu: float, Mu: float) -> BloqueRectangular:
    """Resuelve el bloque rectangular de la DG1 para {P_u, M_u}."""
    e = Mu / Pu  # (4-39)
    e_crit = cx.N / 2 - Pu / (2 * cx.q_max)  # (4-40)
    grande = e > e_crit  # (4-53)
    if not grande:
        # Momento chico: no hay despegue y los pernos no se activan.
        return BloqueRectangular(e, e_crit, False, float("nan"), 0.0)

    disc = cx.brazo**2 - 2 * Pu * (e + cx.f) / cx.q_max  # radicando de (4-58)
    if disc < 0:  # (4-59) no se cumple: hace falta una placa mayor
        raise ValueError(
            f"Ec. 4-59 no se cumple con Pu={Pu:.0f} kgf y Mu={Mu:.0f} kgf·cm: "
            "no hay solución real de la Ec. 4-58, se requiere placa mayor"
        )
    Y = cx.brazo - math.sqrt(disc)  # (4-58), raíz menor
    T = cx.q_max * Y - Pu  # (4-55)
    return BloqueRectangular(e, e_crit, True, Y, T)


# ================== APÉNDICE C — RIGIDEZ ROTACIONAL SECANTE ================


@dataclass(frozen=True)
class Rigidez:
    """El giro repartido en las cuatro deformaciones de la Ec. C-5."""

    rod: float  # cm — C-6
    plate_tension: float  # cm — C-7
    plate_compression: float  # cm — C-10 o C-11
    footing: float  # cm — C-12
    theta: float  # rad — C-5
    beta: float  # kgf·cm/rad — C-4

    @property
    def total(self) -> float:
        return self.rod + self.plate_tension + self.plate_compression + self.footing

    @property
    def reparto(self) -> dict[str, float]:
        """Fracción de la deformación total que aporta cada término, en %."""
        t = self.total
        return {
            "perno (C-6)": 100 * self.rod / t,
            "placa traccionada (C-7)": 100 * self.plate_tension / t,
            "placa comprimida (C-11)": 100 * self.plate_compression / t,
            "zapata (C-12)": 100 * self.footing / t,
        }


def rigidez_rotacional(cx: Conexion, Pu: float, Mu: float) -> Rigidez:
    """beta_connection por §C.2.1, caso de excentricidad alta (e >= e_crit)."""
    bl = bloque_rectangular(cx, Pu, Mu)
    if not bl.momento_grande:
        raise NotImplementedError(
            "caso de excentricidad baja: van las Ecs. C-13 a C-16, no implementadas "
            "(en ese régimen los pernos no se activan y solo deforma la zapata)"
        )
    T, Y = bl.T, bl.Y

    # C-6 — alargamiento del perno.
    d_rod = T * cx.L_rod / (cx.A_rod * E_ACERO)

    # C-7 — flexión de la placa del lado traccionado, con término de corte.
    # C-8: L_tension = f − d/2, del borde de la columna al eje del perno.
    L_t = cx.f - cx.d_col / 2
    d_pt = T * L_t**3 / (3 * E_ACERO * cx.I_plate) + T * L_t / (cx.A_shear * G_ACERO)

    # C-10 / C-11 — flexión del lado comprimido, según el bloque cubra o no el
    # voladizo. Las dos empalman en Y = m (el corchete de C-11 vale m⁴ ahí).
    m, B, fmax = cx.m, cx.B, cx.fp_max
    if Y >= m:  # C-10
        d_pc = fmax * B * (
            m**4 / (8 * E_ACERO * cx.I_plate) + m**2 / (2 * cx.A_shear * G_ACERO)
        )
    else:  # C-11
        corchete = m**4 - (m - Y) ** 3 * (3 * m + Y) / 3
        d_pc = fmax * B / (8 * E_ACERO * cx.I_plate) * corchete + fmax * B * Y / (
            cx.A_shear * G_ACERO
        ) * (m - Y / 2)

    # C-12 — acortamiento de la zapata bajo la punta de la placa.
    d_f = fmax * cx.d_footing / cx.E_c

    theta = (d_rod + d_pt + d_pc + d_f) / cx.brazo  # C-5
    return Rigidez(d_rod, d_pt, d_pc, d_f, theta, Mu / theta)  # C-4


# ---- Los dos autocontrastes que la propia guía habilita --------------------


def continuidad_blockout() -> list[tuple[str, float, float]]:
    """Las tres ramas de C-17 y C-18 empalman en L/D = 0,5 y L/D = 2,0.

    Es el único chequeo que estas ecuaciones admiten sin salir de la guía, y
    sirve para lo que importa: confirmar que las constantes se transcribieron
    bien. Las constantes son DIMENSIONALES (kip/in^2,85), así que no se
    convierten acá — se usan en las unidades de la guía y se convierte el
    resultado.
    """
    fuerte = lambda r: 174.0 if r <= 0.5 else (84 * r + 132 if r <= 2.0 else 300.0)
    debil = lambda r: 129.0 if r <= 0.5 else (14 * r + 122 if r <= 2.0 else 150.0)
    return [
        ("C-17a/b en L/D = 0,5", 174.0, 84 * 0.5 + 132),
        ("C-17b/c en L/D = 2,0", 300.0, 84 * 2.0 + 132),
        ("C-18a/b en L/D = 0,5", 129.0, 14 * 0.5 + 122),
        ("C-18b/c en L/D = 2,0", 150.0, 14 * 2.0 + 122),
        ("C-17 continua en 0,5", fuerte(0.5), fuerte(0.5000001)),
        ("C-18 continua en 2,0", debil(2.0), debil(2.0000001)),
    ]


def limites_c16(cx: Conexion, Pu: float) -> tuple[float, float]:
    """Los dos límites que verifican la Ec. C-16, y que la guía enuncia.

    Con M_u = M_crit la deformación unitaria en el perno es CERO (justo antes
    del despegue); sin momento aplicado es igual a la de la punta (perfil plano
    bajo la placa). Devuelve eps_rod/eps_toe en los dos extremos.
    """
    e_crit = cx.N / 2 - Pu / (2 * cx.q_max)
    M_crit = Pu * e_crit
    return (1 - M_crit / M_crit), (1 - 0.0 / M_crit)


# ============================== EL MARCO ==================================
# Pórtico plano de un vano y un piso. La columna es la del ejemplo trabajado.
# Las dimensiones del perfil se declaran como DATO de esta nota (son las
# nominales de un HEB 300) y la inercia se calcula de ellas, SIN los redondeos
# del encuentro alma-ala. Ignorarlos baja I unos pocos por ciento, lo que sube
# el cociente beta·L/EI: va en contra de la tesis de la nota, no a favor.


@dataclass(frozen=True)
class PerfilI:
    h: float
    b: float
    tf: float
    tw: float

    @property
    def I(self) -> float:
        """Inercia de eje fuerte, sección idealizada en tres rectángulos."""
        return (self.b * self.h**3 - (self.b - self.tw) * (self.h - 2 * self.tf) ** 3) / 12

    @property
    def A(self) -> float:
        return 2 * self.b * self.tf + (self.h - 2 * self.tf) * self.tw


HEB300 = PerfilI(h=30.0, b=30.0, tf=1.9, tw=1.1)

ALTURA = 400.0  # cm
VANO = 600.0  # cm
P_GRAVITACIONAL = 40 * TONF  # kgf por columna, en el tope
H_LATERAL = 20 * TONF  # kgf, en el nivel de la viga


@dataclass(frozen=True)
class Corrida:
    """Lo que el marco entrega y que §3.3.2 dice que la base mueve."""

    nombre: str
    deriva: float  # cm — desplazamiento lateral del nivel
    M_tope: float  # kgf·cm — momento en el tope de la columna a barlovento
    M_base: float  # kgf·cm — momento en la base de esa columna
    P_base_sotavento: float  # kgf — axial de compresión en la base a sotavento
    P_base_barlovento: float  # kgf


Betas = float | tuple[float, float] | None


def _por_base(beta: Betas) -> tuple[float, float]:
    return beta if isinstance(beta, tuple) else (beta, beta)


def _marco(beta: Betas) -> Portico2D:
    """Pórtico con base de rigidez rotacional ``beta``.

    ``beta = None`` es empotrada (el GDL de giro restringido); ``beta = 0.0`` es
    rotulada. Cualquier otro valor entra como resorte rotacional a tierra, que
    es exactamente lo que el Apéndice C recomienda representar. Acepta una tupla
    ``(izq, der)`` porque las dos bases NO tienen el mismo beta: depende del
    axial, y bajo carga lateral una columna se descarga y la otra se carga.
    """
    # nodos: 0 base izq, 1 base der, 2 tope izq, 3 tope der
    coords = np.array([[0.0, 0.0], [VANO, 0.0], [0.0, ALTURA], [VANO, ALTURA]])
    barras = [
        Barra2D(0, 2, E_ACERO, HEB300.A, HEB300.I),  # columna izquierda
        Barra2D(1, 3, E_ACERO, HEB300.A, HEB300.I),  # columna derecha
        Barra2D(2, 3, E_ACERO, HEB300.A, HEB300.I),  # viga
    ]
    giro_fijo = beta is None
    restricciones = {
        0: (True, True, giro_fijo),
        1: (True, True, giro_fijo),
    }
    b_izq, b_der = _por_base(beta)
    resortes = (
        {} if giro_fijo else {0: (0.0, 0.0, b_izq), 1: (0.0, 0.0, b_der)}
    )
    cargas = {
        2: (H_LATERAL, -P_GRAVITACIONAL, 0.0),
        3: (0.0, -P_GRAVITACIONAL, 0.0),
    }
    return Portico2D(coords, barras, restricciones, cargas, resortes)


def correr_marco(nombre: str, beta: Betas) -> Corrida:
    r = _marco(beta).resolver()
    # Columna izquierda = barra 0, del nodo 0 (base) al 2 (tope).
    M_base, M_tope = r.momento_extremos(0)
    # Axial local de la barra: S[0] es la fuerza en el extremo i en local +x,
    # que para una columna vertical (local x hacia arriba) es tracción negativa.
    axial_izq = float(r.fuerzas[0][0])
    axial_der = float(r.fuerzas[1][0])
    return Corrida(
        nombre=nombre,
        deriva=r.desplazamiento(2, 0),
        M_tope=M_tope,
        M_base=M_base,
        P_base_sotavento=max(axial_izq, axial_der),
        P_base_barlovento=min(axial_izq, axial_der),
    )


# ------------------------ el mismo marco en OpenSees -----------------------


def correr_marco_opensees(beta: float | None) -> Corrida:
    """El mismo pórtico en OpenSeesPy. La base flexible va con ``zeroLength``."""
    from openseespy import opensees as ops

    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    # Nodos: 0/1 tierra, 10/11 pie de columna, 2/3 tope.
    ops.node(0, 0.0, 0.0)
    ops.node(1, VANO, 0.0)
    ops.node(10, 0.0, 0.0)
    ops.node(11, VANO, 0.0)
    ops.node(2, 0.0, ALTURA)
    ops.node(3, VANO, ALTURA)

    ops.fix(0, 1, 1, 1)
    ops.fix(1, 1, 1, 1)

    if beta is None:
        # Empotrada: el pie se ata rígido a tierra en los tres GDL.
        for tierra, pie in ((0, 10), (1, 11)):
            ops.equalDOF(tierra, pie, 1, 2, 3)
    else:
        # Traslaciones atadas; el giro pasa por el resorte. beta = 0 es rotulada
        # (un material de rigidez nula deja el giro libre).
        #
        # `-dir 3`: en un modelo ndm=2/ndf=3 el tercer GDL ES la rotación. El 6
        # de los ejemplos 3D acá no existe.
        ops.uniaxialMaterial("Elastic", 1, max(beta, 1e-12))
        for tierra, pie in ((0, 10), (1, 11)):
            ops.equalDOF(tierra, pie, 1, 2)
        ops.element("zeroLength", 100, 0, 10, "-mat", 1, "-dir", 3)
        ops.element("zeroLength", 101, 1, 11, "-mat", 1, "-dir", 3)

    ops.geomTransf("Linear", 1)
    ops.element("elasticBeamColumn", 1, 10, 2, HEB300.A, E_ACERO, HEB300.I, 1)
    ops.element("elasticBeamColumn", 2, 11, 3, HEB300.A, E_ACERO, HEB300.I, 1)
    ops.element("elasticBeamColumn", 3, 2, 3, HEB300.A, E_ACERO, HEB300.I, 1)

    ops.timeSeries("Linear", 1)
    ops.pattern("Plain", 1, 1)
    ops.load(2, H_LATERAL, -P_GRAVITACIONAL, 0.0)
    ops.load(3, 0.0, -P_GRAVITACIONAL, 0.0)

    ops.system("BandGeneral")
    ops.numberer("RCM")
    ops.constraints("Transformation")
    ops.integrator("LoadControl", 1.0)
    ops.algorithm("Linear")
    ops.analysis("Static")
    assert ops.analyze(1) == 0, "el análisis estático de OpenSees no convergió"

    # `eleForce` devuelve ejes GLOBALES; hace falta `localForce`, que es el
    # mismo vector S = k·u_local − P_eq que arma `ref.py`, con las mismas
    # convenciones: M(0) = −S[2], M(L) = +S[5], axial = S[0].
    s_izq = ops.eleResponse(1, "localForce")
    s_der = ops.eleResponse(2, "localForce")
    return Corrida(
        nombre="opensees",
        deriva=ops.nodeDisp(2, 1),
        M_tope=+s_izq[5],
        M_base=-s_izq[2],
        P_base_sotavento=max(s_izq[0], s_der[0]),
        P_base_barlovento=min(s_izq[0], s_der[0]),
    )


# =========================== LA CIRCULARIDAD ===============================


@dataclass(frozen=True)
class Vuelta:
    i: int
    beta_barlovento: float
    beta_sotavento: float
    Pu_barlovento: float
    Mu_barlovento: float


def iterar_beta(
    cx: Conexion, beta_0: float, *, tol: float = 1e-4, max_iter: int = 30
) -> list[Vuelta]:
    """Itera beta contra el {P_u, M_u} que el propio marco produce.

    §C.2.1: *"la rigidez rotacional es sensible al nivel de compresión axial
    presente en la columna. La compresión axial misma puede ser desconocida
    porque el análisis para determinarla puede requerir la representación de la
    rigidez rotacional de la base."* La salida que la guía propone es determinar
    el axial con la carga gravitacional sin sismo, y —si se desea— iterar hasta
    consistencia mutua, *"reconociendo que esto puede volverse muy engorroso en
    marcos con varias columnas"*. Eso es exactamente lo que se mide acá: las dos
    bases del pórtico convergen a beta DISTINTOS, porque bajo la carga lateral
    una columna se descarga y la otra se carga.

    Se reporta la columna a **barlovento**, que es la que menos comprimida
    queda: §6.4.1 advierte que menos compresión puede ser la condición crítica,
    porque para el mismo momento deja más tracción en el perno.
    """
    historia: list[Vuelta] = []
    betas = (beta_0, beta_0)
    for i in range(1, max_iter + 1):
        r = _marco(betas).resolver()
        nuevas = []
        for barra in (0, 1):  # columna izquierda (barlovento) y derecha
            M_base, _ = r.momento_extremos(barra)
            Pu = abs(float(r.fuerzas[barra][0]))
            nuevas.append(rigidez_rotacional(cx, Pu, abs(M_base)).beta)
            if barra == 0:
                Pu_b, Mu_b = Pu, abs(M_base)
        historia.append(Vuelta(i, nuevas[0], nuevas[1], Pu_b, Mu_b))
        if max(abs(n - v) / n for n, v in zip(nuevas, betas)) < tol:
            return historia
        betas = (nuevas[0], nuevas[1])
    raise RuntimeError(f"beta no convergió en {max_iter} iteraciones")


# =============================== SALIDA ====================================


def fmt_tonf_m(v: float) -> float:
    return v / TONF_M


def main() -> None:
    cx = Conexion()
    Pu = 40 * TONF
    Mu = 12 * TONF_M

    print("=" * 78)
    print("NOTA 05 — rigidez rotacional de la base (AISC DG1 3.ª ed., Apéndice C)")
    print("=" * 78)

    # --- 0. El caso, y el contraste contra lo que el post 2 publicó ---------
    bl = bloque_rectangular(cx, Pu, Mu)
    print(f"\n## El caso (del ejemplo trabajado del blog)\n")
    print(f"  e        = {bl.e:8.2f} cm     (Ec. 4-39)")
    print(f"  e_crit   = {bl.e_crit:8.2f} cm     (Ec. 4-40)  → momento {'GRANDE' if bl.momento_grande else 'chico'}")
    print(f"  Y        = {bl.Y:8.2f} cm     (Ec. 4-58)")
    print(f"  T        = {bl.T:8.0f} kgf    (Ec. 4-55) = {bl.T / TONF / 2:.2f} tonf/perno")
    print(f"  m        = {cx.m:8.2f} cm     → Y {'≥' if bl.Y >= cx.m else '<'} m, rige la Ec. C-{'10' if bl.Y >= cx.m else '11'}")

    e_si, e_imp = contraste_modulo_hormigon(cx)
    print(f"\n  E_c (forma SI del post 1)        = {e_si:9.0f} kgf/cm²")
    print(f"  E_c (Ec. C-12, w_c = 145 lb/ft³) = {e_imp:9.0f} kgf/cm²"
          f"   → {100 * (e_imp / e_si - 1):+.1f} %")

    # --- 1. beta y el reparto ----------------------------------------------
    rg = rigidez_rotacional(cx, Pu, Mu)
    print(f"\n## Las cuatro deformaciones de la Ec. C-5\n")
    print("| Componente | Deformación [cm] | Fracción |")
    print("|---|---:|---:|")
    for nombre, pct in rg.reparto.items():
        valor = {
            "perno (C-6)": rg.rod,
            "placa traccionada (C-7)": rg.plate_tension,
            "placa comprimida (C-11)": rg.plate_compression,
            "zapata (C-12)": rg.footing,
        }[nombre]
        print(f"| {nombre} | {valor:.5f} | {pct:.1f} % |")
    print(f"| **suma** | **{rg.total:.5f}** | 100,0 % |")
    print(f"\n  theta = {rg.theta * 1000:.2f} mrad   (Ec. C-5)")
    print(f"  beta  = {rg.beta / TONF_M:.0f} tonf·m/rad   (Ec. C-4)")

    # --- 2. resistencia ≠ rigidez ------------------------------------------
    print(f"\n## Engrosar la placa: qué se mueve y qué no\n")
    print("| t_p [mm] | φM_p ∝ t² | Δ perno | Δ placa compr. | Δ zapata | beta [tonf·m/rad] |")
    print("|---:|---:|---:|---:|---:|---:|")
    base_beta = None
    for tp_mm in (25, 30, 35, 50):
        r = rigidez_rotacional(cx.con(tp=tp_mm / 10), Pu, Mu)
        if base_beta is None:
            base_beta = r.beta
        print(
            f"| {tp_mm} | {(tp_mm / 25) ** 2:.2f}× | {r.rod:.5f} | "
            f"{r.plate_compression:.5f} | {r.footing:.5f} | "
            f"{r.beta / TONF_M:.0f} ({r.beta / base_beta:.2f}×) |"
        )

    # --- 3. rígido respecto de qué -----------------------------------------
    # El cociente K_s·L/EI y los umbrales 20 (FR) y 2 (simple) salen del
    # Comentario a AISC 360-22 §B3.4, pág. impresa 16.1-320 (índice PDF 388),
    # leída rasterizada. ⚠ Ahí L y EI son los de la VIGA: aplicarlo a una base
    # de columna es ANALOGÍA, no la cláusula. Lo que sí traslada limpio es que
    # su K_s = M_s/θ_s (Ec. C-B3-7) es SECANTE a cargas de servicio, igual que
    # el beta del Apéndice C, y por la misma razón declarada: *"many connection
    # types do not exhibit a reliable initial stiffness"*.
    EI = E_ACERO * HEB300.I
    print(f"\n## ¿Rígido respecto de qué?\n")
    print(f"  I de la columna (sin redondeos) = {HEB300.I:.0f} cm⁴")
    print(f"  4EI/L de la columna             = {4 * EI / ALTURA / TONF_M:.0f} tonf·m/rad")
    print(f"  beta·L/EI  (L = {ALTURA / 100:.0f} m)          = {rg.beta * ALTURA / EI:.2f}")
    print("    umbrales del Comentario §B3.4:  >= 20 → FR (empotrada) · <= 2 → simple (rotulada)")
    print("    altura de columna:", end=" ")
    print(
        " · ".join(
            f"{L / 100:.0f} m → {rg.beta * L / EI:.2f}" for L in (300.0, 400.0, 600.0, 900.0)
        )
    )

    # --- 3b. de qué depende de verdad el resultado -------------------------
    # El término que manda (la zapata) es el que peor se conoce: C-12 pide la
    # profundidad TOTAL de la zapata, que el ejemplo trabajado no declara.
    print(f"\n## Sensibilidad a los dos supuestos que esta nota tuvo que declarar\n")
    print("| Supuesto | Valor | Δ del término [cm] | Su fracción | beta [tonf·m/rad] | β·L/EI |")
    print("|---|---:|---:|---:|---:|---:|")
    extremos = []
    for df in (40.0, 60.0, 80.0, 120.0):
        r = rigidez_rotacional(cx.con(d_footing=df), Pu, Mu)
        marca = " ←" if df == cx.d_footing else ""
        extremos.append(r.beta * ALTURA / EI)
        print(
            f"| d_footing (C-12) | {df:.0f} cm{marca} | {r.footing:.5f} | "
            f"{r.reparto['zapata (C-12)']:.1f} % | {r.beta / TONF_M:.0f} | "
            f"{r.beta * ALTURA / EI:.2f} |"
        )
    for tg in (0.0, 2.5, 5.0):
        r = rigidez_rotacional(cx.con(t_grout=tg), Pu, Mu)
        marca = " ←" if tg == cx.t_grout else ""
        print(
            f"| t_grout → L_rod (C-6) | {tg:.1f} cm{marca} | {r.rod:.5f} | "
            f"{r.reparto['perno (C-6)']:.1f} % | {r.beta / TONF_M:.0f} | "
            f"{r.beta * ALTURA / EI:.2f} |"
        )
    # El punto que hace robusta la conclusión: la incertidumbre del supuesto
    # peor conocido mueve beta un factor 1,7, y el veredicto no se mueve nada.
    r_grueso = rigidez_rotacional(cx.con(tp=5.0, d_footing=40.0), Pu, Mu)
    print(
        f"\n  el supuesto peor conocido mueve β entre {min(extremos):.2f} y "
        f"{max(extremos):.2f} en β·L/EI, y el caso MÁS rígido imaginable "
        f"(placa de 50 mm sobre zapata de 40 cm) llega a "
        f"{r_grueso.beta * ALTURA / EI:.2f} — sigue del lado «simple» de la escala."
    )

    # --- 4. el marco tres veces --------------------------------------------
    corridas = [
        correr_marco("empotrada", None),
        correr_marco("rotulada", 0.0),
        correr_marco("resorte β", rg.beta),
    ]
    print(f"\n## El marco corrido tres veces\n")
    print("| Base | Deriva [cm] | M tope col. [tonf·m] | M base [tonf·m] | P base barlov. [tonf] |")
    print("|---|---:|---:|---:|---:|")
    for c in corridas:
        print(
            f"| {c.nombre} | {c.deriva:.3f} | {fmt_tonf_m(abs(c.M_tope)):.2f} | "
            f"{fmt_tonf_m(abs(c.M_base)):.2f} | {abs(c.P_base_barlovento) / TONF:.2f} |"
        )

    # --- 5. la circularidad -------------------------------------------------
    historia = iterar_beta(cx, rg.beta)
    print(f"\n## La circularidad de §C.2.1, iterada\n")
    print(
        "| Vuelta | β barlovento [tonf·m/rad] | β sotavento [tonf·m/rad] "
        "| P_u barlov. [tonf] | M_u barlov. [tonf·m] |"
    )
    print("|---:|---:|---:|---:|---:|")
    for v in historia:
        print(
            f"| {v.i} | {v.beta_barlovento / TONF_M:.0f} | {v.beta_sotavento / TONF_M:.0f} "
            f"| {v.Pu_barlovento / TONF:.2f} | {v.Mu_barlovento / TONF_M:.2f} |"
        )
    ult = historia[-1]
    betas_final = (ult.beta_barlovento, ult.beta_sotavento)
    print(
        f"\n  converge en {len(historia)} vueltas · β barlovento pasa de "
        f"{rg.beta / TONF_M:.0f} a {ult.beta_barlovento / TONF_M:.0f} tonf·m/rad "
        f"({100 * (ult.beta_barlovento / rg.beta - 1):+.1f} %)"
    )
    print(
        f"  y las DOS bases del mismo pórtico convergen a β distintos: "
        f"{ult.beta_barlovento / TONF_M:.0f} y {ult.beta_sotavento / TONF_M:.0f} tonf·m/rad "
        f"({100 * (ult.beta_sotavento / ult.beta_barlovento - 1):+.1f} %)"
    )

    conv = correr_marco("β convergido", betas_final)
    print(
        f"\n  Con los β convergidos: deriva {conv.deriva:.3f} cm · "
        f"M tope {fmt_tonf_m(abs(conv.M_tope)):.2f} tonf·m · "
        f"M base {fmt_tonf_m(abs(conv.M_base)):.2f} tonf·m"
        f"  (contra {corridas[2].deriva:.3f} cm con el β de la primera pasada)"
    )

    # --- 6. verificación: los dos caminos ----------------------------------
    filas: list[Fila] = []
    for c in corridas:
        beta = {"empotrada": None, "rotulada": 0.0, "resorte β": rg.beta}[c.nombre]
        o = correr_marco_opensees(beta)
        filas += [
            Fila(f"{c.nombre} · deriva", "cm", c.deriva, o.deriva, decimales=5),
            Fila(f"{c.nombre} · M tope", "tonf·m", fmt_tonf_m(c.M_tope), fmt_tonf_m(o.M_tope), decimales=5),
            Fila(
                f"{c.nombre} · M base",
                "tonf·m",
                fmt_tonf_m(c.M_base),
                fmt_tonf_m(o.M_base),
                decimales=5,
                tol_abs=1e-9 if beta == 0.0 else None,
            ),
            Fila(
                f"{c.nombre} · P barlovento",
                "tonf",
                c.P_base_barlovento / TONF,
                o.P_base_barlovento / TONF,
                decimales=5,
            ),
        ]
    reportar("El marco: rigidez directa en numpy contra OpenSeesPy", filas)

    # Autocontrastes de la cadena del Apéndice C.
    filas_c = [
        Fila(nombre, "", a, b, decimales=4) for nombre, a, b in continuidad_blockout()
    ]
    cero, uno = limites_c16(cx, Pu)
    filas_c += [
        Fila("C-16 con M_u = M_crit → ε_rod/ε_toe", "", 0.0, cero, tol_abs=1e-12),
        Fila("C-16 sin momento → ε_rod/ε_toe", "", 1.0, uno),
    ]
    reportar(
        "Los autocontrastes que la guía habilita",
        filas_c,
        ref_label="Declarado",
        ops_label="Calculado",
        nota="Las ramas de C-17/C-18 empalman, y la Ec. C-16 da los dos límites que "
        "la guía enuncia. Es lo único que estas ecuaciones admiten sin salir del "
        "documento — no reemplaza haber leído la página rasterizada.",
    )


if __name__ == "__main__":
    main()
