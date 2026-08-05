"""Nota 03 — la zapata que se despega, y el triángulo que no depende del suelo.

**La pregunta:** el suelo no tracciona. Si se le pone momento suficiente a una
zapata, un borde deja de apoyar. ¿Qué presión queda abajo, y cuánto de eso
depende de la rigidez que uno le suponga al suelo?

**El caso:** zapata corrida rígida de ``B = 3,0 m`` en la dirección de la
excentricidad y ``b = 1,0 m`` fuera del plano, con carga vertical ``Q`` y
momento ``M``, sobre una cama de resortes verticales que **no toman tracción**
(``uniaxialMaterial ENT``). Se barre ``e = M/Q``.

**Lo que dice la teoría.** Mientras la resultante cae dentro del núcleo central
el contacto es total y el reparto es lineal; pasado ``e = B/6`` la Ec. (16.21)
daría tracción, el suelo no la toma y la zapata se despega::

    q_máx = Q/(BL)·(1 + 6e/B)      (16.20)   |  e ≤ B/6
    q_mín = Q/(BL)·(1 − 6e/B)      (16.21)   |
    q_máx = 4Q / (3L(B − 2e))      (16.22)   |  e > B/6

Fuente: Das, B. M., *Fundamentos de Ingeniería Geotécnica*, 4.ª ed., §16.7,
pp. 490-492 (ecuaciones transcritas de la página rasterizada del PDF, no de la
capa de texto). La longitud de contacto ``a = 3(B/2 − e)`` sale de la propia
Ec. (16.22) por estática; se deriva en `lab/_lib/ref.py`.

**Las cuatro cosas que muestra la nota**

1. Los resortes ``ENT`` **encuentran solos el eje neutro**: nadie les dice dónde
   termina el contacto, y el reparto que sale es el triángulo cerrado de Das.

2. **El reparto no depende de la rigidez del suelo.** Con ``k_s`` variando en un
   rango de 100 a 1, ``q_máx`` no se mueve: lo que escala —exactamente en la
   misma proporción— es el asentamiento. ``k_s`` decide cuánto baja la zapata,
   no cómo se reparte la presión bajo ella.

3. **Con pocos resortes, ``q_máx`` sale bajo.** El error es siempre del lado
   inseguro y se cierra como ``1/N²``: con 4 resortes falta un 6,5 %.

4. **La superposición se muere.** Analizar dos casos por separado y sumar sus
   presiones no da lo mismo que analizar la combinación. Peor: por casos la
   zapata parece incumplir el área apoyada mínima que exige NCh2369:2025
   §10.1.4, y la combinación real apoya el 100 %.

**Verificación (los dos caminos):** referencia = fórmula cerrada de Das en
`lab/_lib/ref.py` (numpy puro, sin importar `rukan` ni `openseespy`); motor =
OpenSeesPy con resortes ``ENT`` y análisis no lineal.

Correr::

    python -m lab.nota03_zapata_sin_traccion
"""

from __future__ import annotations

import numpy as np
import openseespy.opensees as ops

from lab._lib import svg
from lab._lib.ref import (
    excentricidad_para_fraccion,
    fraccion_apoyada,
    presion_zapata_rigida,
)
from lab._lib.report import Fila, reportar
from rukan import units as u

# ============================ DATOS DE ENTRADA ============================
B = 3.0 * u.ureg.m  # lado en la dirección de la excentricidad
ANCHO = 1.0 * u.ureg.m  # lado fuera del plano (zapata corrida, por metro)
Q = 600.0 * u.ureg.kN  # carga vertical de servicio

# Módulo de balasto. **El valor da igual y ese es medio punto de la nota**: no
# aparece en ninguna de las ecuaciones de Das. Acá solo fija el asentamiento.
KS = 30_000.0 * u.ureg.kN / u.ureg.m**3

# La zapata se idealiza como cuerpo rígido: una viga con EI muy alto. Una zapata
# real de 0,6 m de canto tiene EI ≈ 4,5e5 kN·m², así que esto es unos 2·10³ veces
# más rígido. Es hipótesis del modelo, no una zapata que exista.
E_VIGA = 2.0e8 * u.ureg.kN / u.ureg.m**2
I_VIGA = 5.0 * u.ureg.m**4

N_RESORTES = 256  # divisiones de la base; la convergencia se estudia en la tabla 4

B_ = u.length(B)
ANCHO_ = u.length(ANCHO)
Q_ = u.force(Q)
KS_ = KS.to(u.ureg.kN / u.ureg.m**3).magnitude  # kN/m³: no hay helper, va a mano
E_ = u.stress(E_VIGA)
I_ = u.inertia(I_VIGA)
EI_ = E_ * I_

# Las cuatro excentricidades de la nota, elegidas para que cada una signifique
# algo: dentro del núcleo, el borde exacto del núcleo, y los dos porcentajes de
# área apoyada que pide NCh2369:2025 §10.1.4 (80 % menores, 50 % mayores).
E_TRAPECIO = 0.10 * B_
E_NUCLEO = B_ / 6.0
E_80 = excentricidad_para_fraccion(0.80, B_)
E_50 = excentricidad_para_fraccion(0.50, B_)
CASOS = [
    (E_TRAPECIO, "dentro del núcleo"),
    (E_NUCLEO, "borde del núcleo"),
    (E_80, "80 % apoyado — §10.1.4 menores"),
    (E_50, "50 % apoyado — §10.1.4 mayores"),
]

# Tags: los nodos de la zapata van de 1 a N+1, así que el suelo y los resortes
# arrancan bien arriba para que no colisionen ni con N grande.
SUELO, RESORTE = 10_000, 20_000


# ============================== OPENSEES ==================================
def modelo(Q_kn: float, e: float, *, n: int = N_RESORTES, ks: float = KS_,
           ei: float = EI_, sin_traccion: bool = True) -> dict:
    """Zapata rígida sobre resortes verticales, con carga vertical y momento.

    Los resortes son ``zeroLength`` entre un nodo de suelo fijo y el nodo de la
    zapata, en dirección 2. El orden de nodos importa: con el suelo primero, la
    deformación del elemento es el descenso de la zapata, y un descenso es
    **compresión** —que es lo único que el material ``ENT`` resiste—.

    La rigidez de cada resorte es ``k_s`` por su **área tributaria**, que en los
    dos nodos de borde vale la mitad. Con rigidez uniforme, la reacción total no
    daría ``Q``.
    """
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    h = B_ / n
    xs = np.array([k * h for k in range(n + 1)])
    trib = np.full(n + 1, h)
    trib[0] = trib[-1] = h / 2.0

    for k, x in enumerate(xs):
        ops.node(k + 1, float(x), 0.0)
        ops.node(SUELO + k, float(x), 0.0)
        ops.fix(SUELO + k, 1, 1, 1)
        rigidez = ks * float(trib[k]) * ANCHO_
        # ENT: elástico en compresión, rigidez nula en tracción.
        ops.uniaxialMaterial(
            "ENT" if sin_traccion else "Elastic", RESORTE + k, rigidez
        )
        ops.element("zeroLength", RESORTE + k, SUELO + k, k + 1,
                    "-mat", RESORTE + k, "-dir", 2)

    ops.geomTransf("Linear", 1)
    for k in range(n):
        ops.element("elasticBeamColumn", k + 1, k + 1, k + 2, 1.0, ei, 1.0, 1)

    centro = n // 2 + 1
    ops.fix(centro, 1, 0, 0)  # los resortes no dan rigidez horizontal

    # Q en el centro más el momento que la lleva a excentricidad e: una carga
    # −Q ĵ desplazada +e x̂ equivale a (−Q ĵ, M_z = −Q·e) en el centro.
    ops.timeSeries("Constant", 1)
    ops.pattern("Plain", 1, 1)
    ops.load(centro, 0.0, -Q_kn, -Q_kn * e)

    ops.system("BandGeneral")
    ops.numberer("Plain")
    ops.constraints("Plain")
    ops.test("NormDispIncr", 1e-12, 500, 0)
    ops.algorithm("Newton")  # es no lineal: el ENT cambia de rigidez
    ops.integrator("LoadControl", 0.1)
    ops.analysis("Static")
    if ops.analyze(10) != 0:
        raise RuntimeError(f"no convergió: Q = {Q_kn}, e = {e}, n = {n}")

    # force = [Fx_i, Fy_i, Mz_i, Fx_j, Fy_j, Mz_j]. Fy_i es lo que la zapata
    # apoya sobre el suelo: positivo = compresión.
    fuerza = np.array(
        [ops.eleResponse(RESORTE + k, "force")[1] for k in range(n + 1)]
    )
    q = fuerza / (trib * ANCHO_)
    en_contacto = q > 1e-9
    return {
        "x": xs,
        "q": q,
        "q_max": float(q.max()),
        "q_min": float(q.min()),
        # Presión en el borde comprimido. Con e > 0 coincide con q_máx, pero es
        # un punto fijo: `q.max()` de un reparto uniforme cae en un nodo
        # cualquiera, y entonces dos casos dejan de ser comparables término a
        # término.
        "q_borde": float(q[-1]),
        "a_contacto": float(trib[en_contacto].sum()),
        "reaccion": float(fuerza.sum()),
        "asentamiento": ops.nodeDisp(centro, 2),
        "rotacion": ops.nodeDisp(centro, 3),
    }


# ============================== LA NOTA ===================================
def main() -> None:
    print("# Nota 03 — la zapata que se despega\n")
    print(f"Zapata corrida rígida: B = {B_:.1f} m, b = {ANCHO_:.1f} m, "
          f"Q = {Q_:.0f} kN, k_s = {KS_:,.0f} kN/m³")
    print(f"Núcleo central: B/6 = {B_ / 6:.4f} m. "
          f"Idealización de cuerpo rígido: EI = {EI_:.1e} kN·m² "
          f"({EI_ / 4.5e5:.0f}× la de una zapata de 0,6 m de canto).\n")

    # --- 1. el reparto, en cuatro excentricidades -------------------------
    resultados = {e: modelo(Q_, e) for e, _ in CASOS}
    referencias = {e: presion_zapata_rigida(Q_, Q_ * e, B_, ANCHO_) for e, _ in CASOS}

    reportar(
        "1. La presión máxima, en cuatro excentricidades",
        [
            Fila(f"q_máx con e/B = {e / B_:.4f} ({etiqueta})", "kPa",
                 ref=referencias[e].q_max, ops=resultados[e]["q_max"])
            for e, etiqueta in CASOS
        ],
        ref_label="Fórmula cerrada (Das §16.7)",
        ops_label="Resortes ENT",
        nota=("Las dos últimas filas usan la Ec. (16.22), la del triángulo. "
              "Nadie le dijo al modelo dónde termina el contacto."),
    )

    # --- 2. dónde termina el contacto -------------------------------------
    reportar(
        "2. …y hasta dónde llega el contacto",
        [
            Fila(f"Fracción apoyada con e/B = {e / B_:.4f}", "—",
                 ref=fraccion_apoyada(e, B_),
                 ops=resultados[e]["a_contacto"] / B_,
                 tol_pct=0.5)
            for e, etiqueta in CASOS
        ],
        ref_label="a/B = 3/2 − 3e/B",
        ops_label="Resortes en compresión",
        nota=("Tolerancia 0,5 %: la longitud de contacto del modelo está "
              "**cuantizada** al paso de los resortes (B/256 = "
              f"{B_ / N_RESORTES * 1000:.1f} mm), así que no puede caer en "
              "cualquier lado."),
    )

    # --- 3. el reparto no sabe cuánto vale k_s ----------------------------
    e_ref = E_80
    ref_80 = referencias[e_ref]
    escalas = (0.1, 1.0, 10.0)
    invariancia = {f: modelo(Q_, e_ref, ks=KS_ * f) for f in escalas}

    reportar(
        "3. El mismo reparto, con el suelo 100 veces más blando y más rígido",
        [
            Fila(f"q_máx con k_s × {f:g}", "kPa",
                 ref=ref_80.q_max, ops=invariancia[f]["q_max"])
            for f in escalas
        ],
        ref_label="Fórmula cerrada",
        ops_label="Resortes ENT",
        nota=("La fórmula cerrada **no tiene k_s adentro**, y el modelo, que sí "
              "lo tiene, da lo mismo en todo el rango."),
    )

    print("\nLo que sí escala con el suelo es cuánto baja la zapata:\n")
    for f in escalas:
        r = invariancia[f]
        print(f"  k_s × {f:>4g}    asentamiento {-r['asentamiento'] * 1000:8.3f} mm"
              f"    giro {-r['rotacion'] * 1000:8.4f} mrad")
    razon = invariancia[0.1]["asentamiento"] / invariancia[1.0]["asentamiento"]
    print(f"\n  Dividir k_s por 10 multiplica el asentamiento por "
          f"{razon:.4f} y la presión por "
          f"{invariancia[0.1]['q_max'] / invariancia[1.0]['q_max']:.4f}.")
    print("  El extremo blando es un suelo en el que nadie fundaría —62 mm de "
          "asentamiento\n  y 4° de giro— y ni aun ahí la presión se mueve.")

    # --- 4. con pocos resortes, q_máx sale bajo ---------------------------
    mallas = (4, 8, 16, 32, 64)
    reportar(
        "4. Con pocos resortes la presión sale baja",
        [
            Fila(f"q_máx con {n} divisiones", "kPa",
                 ref=ref_80.q_max, ops=modelo(Q_, e_ref, n=n)["q_max"],
                 tol_pct=10.0)
            for n in mallas
        ],
        ref_label="Fórmula cerrada",
        ops_label="Resortes ENT",
        nota=("Tolerancia 10 %: acá el error **es** el resultado. Siempre "
              "negativo —del lado inseguro— y se cierra como 1/N²."),
    )

    # --- 5. la superposición se muere -------------------------------------
    Q_a, e_a = 400.0, 0.0  # peso propio, centrado
    Q_b, e_b = 200.0, 0.9  # una carga excéntrica, sola
    Q_c = Q_a + Q_b
    e_c = (Q_a * e_a + Q_b * e_b) / Q_c

    caso_a, caso_b, caso_c = (
        modelo(Q_a, e_a), modelo(Q_b, e_b), modelo(Q_c, e_c)
    )
    ref_a = presion_zapata_rigida(Q_a, Q_a * e_a, B_, ANCHO_)
    ref_b = presion_zapata_rigida(Q_b, Q_b * e_b, B_, ANCHO_)
    ref_c = presion_zapata_rigida(Q_c, Q_c * e_c, B_, ANCHO_)

    reportar(
        "5. Dos casos y su combinación, cada uno bien resuelto",
        [
            Fila(f"Caso A — Q = {Q_a:.0f} kN, e = {e_a:.2f} m", "kPa",
                 ref=ref_a.q_max, ops=caso_a["q_max"]),
            Fila(f"Caso B — Q = {Q_b:.0f} kN, e = {e_b:.2f} m", "kPa",
                 ref=ref_b.q_max, ops=caso_b["q_max"]),
            Fila(f"Combinación A+B — Q = {Q_c:.0f} kN, e = {e_c:.2f} m", "kPa",
                 ref=ref_c.q_max, ops=caso_c["q_max"]),
        ],
        ref_label="Fórmula cerrada",
        ops_label="Resortes ENT",
        nota="Los tres análisis cierran. El problema aparece al sumarlos.",
    )

    suma = caso_a["q_max"] + caso_b["q_max"]
    print("\nLa presión de la combinación, por los dos caminos que un ingeniero "
          "usaría:\n")
    print(f"  sumando las presiones de cada caso    {suma:8.2f} kPa")
    print(f"  analizando la combinación             {caso_c['q_max']:8.2f} kPa")
    print(f"  la suma se pasa en                    "
          f"{suma / caso_c['q_max'] * 100 - 100:8.2f} %")
    print("\nY el área apoyada da vuelta el veredicto normativo:\n")
    print(f"  caso B solo          {caso_b['a_contacto'] / B_ * 100:5.1f} % apoyado"
          "   → no cumple el 80 % de §10.1.4")
    print(f"  combinación A+B      {caso_c['a_contacto'] / B_ * 100:5.1f} % apoyado"
          "   → cumple con holgura")

    # --- lo que NCh2369 §10.1.4 pide, puesto en escala de e/B -------------
    # La norma acota **área apoyada**, no excentricidad. La conversión es la
    # inversa de a/B = 3/2 − 3e/B, o sea derivación propia y no texto normativo;
    # se imprime acá para que el número del post no sea una cuenta a mano.
    print("\n### La conversión área apoyada ↔ e/B (derivada, no normativa)\n")
    print("| Criterio | Área apoyada | e/B |")
    print("|---|---|---|")
    for frac, criterio in (
        (1.00, "Contacto total (tercio central)"),
        (0.80, "NCh2369 §10.1.4, estándar menores"),
        (0.50, "NCh2369 §10.1.4, estándar mayores"),
    ):
        e = excentricidad_para_fraccion(frac, B_)
        assert abs(fraccion_apoyada(e, B_) - frac) < 1e-12, "la inversa no cierra"
        e_rel = f"{e / B_:.3f}".replace(".", ",")  # coma decimal: va en prosa
        print(f"| {criterio} | {frac * 100:.0f} % | {e_rel} |")

    # --- 6. el control: con resortes elásticos, todo esto desaparece ------
    lin_a = modelo(Q_a, e_a, sin_traccion=False)
    lin_b = modelo(Q_b, e_b, sin_traccion=False)
    lin_c = modelo(Q_c, e_c, sin_traccion=False)
    reportar(
        "6. El control: con resortes que sí traccionan, la suma cierra",
        [
            Fila("Presión en el borde comprimido", "kPa",
                 ref=lin_a["q_borde"] + lin_b["q_borde"], ops=lin_c["q_borde"],
                 tol_pct=1e-9),
        ],
        ref_label="Suma de casos",
        ops_label="Combinación analizada",
        nota=("Mismo modelo, cambiando `ENT` por `Elastic`: la superposición "
              "vuelve a valer a precisión de máquina. Lo que la rompe no es la "
              "zapata ni la malla — es que el suelo no tracciona."),
    )


# ============================== FIGURAS ===================================
def figuras() -> None:
    _fig_regimenes()
    _fig_qmax()


def _fig_regimenes() -> None:
    """Tres regímenes de contacto, dibujados con el reparto que da el motor.

    El perfil es ``q`` del modelo de resortes ``ENT`` **nodo por nodo**, no la
    fórmula cerrada: en una serie cuya tesis son los dos caminos separados, una
    figura rotulada como el motor tiene que salir del motor. Sale casi idéntica
    —la Tabla 1 dice que difieren menos de 0,01 %— y esa es justamente la
    afirmación que la nota hace.
    """
    paneles = [
        (E_TRAPECIO, "e/B = 0,10"),
        (E_80, "e/B = 0,233"),
        (E_50, "e/B = 0,333"),
    ]
    corridas = {e: modelo(Q_, e) for e, _ in paneles}
    escala = 92.0 / max(r["q_max"] for r in corridas.values())
    media = 68.0  # medio ancho de la zapata en píxeles
    y_base = 118.0

    lienzo = svg.Lienzo(
        alto=290,
        titulo="Pasado el núcleo central, la zapata se despega",
        subtitulo=f"B = {B_:.0f} m, Q = {Q_:.0f} kN — presión de contacto bajo "
                  "zapata rígida, del modelo de resortes ENT",
    )

    for (e, etiqueta), cx in zip(paneles, (105.0, 280.0, 455.0)):
        r = corridas[e]
        izq, der = cx - media, cx + media
        fraccion = r["a_contacto"] / B_
        despegada = fraccion < 0.999
        x_ini = der - fraccion * (2 * media)

        # La zapata.
        lienzo.rect(izq, y_base - 13, 2 * media, 13, color="#d7dee6", radio=1)
        lienzo.linea(izq, y_base, der, y_base, color=svg.TINTA, ancho=1.2)

        # La resultante, en su punto de aplicación.
        x_q = cx + e / B_ * (2 * media)
        lienzo.linea(x_q, y_base - 48, x_q, y_base - 15, color=svg.ROJO, ancho=1.6)
        lienzo.poligono(
            [(x_q, y_base - 13), (x_q - 3.5, y_base - 21), (x_q + 3.5, y_base - 21)],
            relleno=svg.ROJO, borde=svg.ROJO, ancho=0.5,
        )
        lienzo.texto(x_q, y_base - 53, "Q", tam=10.5, color=svg.ROJO,
                     anclaje="middle", negrita=True)

        # El bloque de presión: el perfil que reportan los resortes, cerrado
        # contra la base. La zona despegada entra sola, con q = 0.
        perfil = [
            (izq + x / B_ * (2 * media), y_base + q * escala)
            for x, q in zip(r["x"], r["q"])
        ]
        puntos = [(izq, y_base)] + perfil + [(der, y_base)]
        lienzo.poligono(puntos, relleno=svg.AZUL, borde="none", ancho=0,
                        opacidad=0.30)
        lienzo.polilinea(perfil, color=svg.AZUL, ancho=1.6)
        # Los dos cantos verticales del bloque: el de la izquierda mide q_mín
        # (cero, y por lo tanto invisible, cuando la zapata está despegada).
        for x_borde, q_borde in ((izq, r["q"][0]), (der, r["q"][-1])):
            lienzo.linea(x_borde, y_base, x_borde, y_base + q_borde * escala,
                         color=svg.AZUL, ancho=1.6)

        if despegada:
            lienzo.linea(izq, y_base, x_ini, y_base, color=svg.GRIS,
                         ancho=1.4, guion="3 3")
            lienzo.texto((izq + x_ini) / 2, y_base - 20, "despegado", tam=9,
                         color=svg.GRIS, anclaje="middle")

        # Rótulos.
        lienzo.texto(cx, y_base + 128, etiqueta, tam=11.5, color=svg.TINTA,
                     anclaje="middle", negrita=True)
        lienzo.texto(cx, y_base + 145, f"q máx = {r['q_max']:.0f} kPa", tam=10.5,
                     color=svg.AZUL, anclaje="middle")
        lienzo.texto(cx, y_base + 160, f"apoyado {fraccion * 100:.0f} %",
                     tam=10.5, color=svg.ROJO if despegada else svg.GRIS,
                     anclaje="middle")

    lienzo.guardar("lab/figs/nota03-regimenes.svg")


def _fig_qmax() -> None:
    """q_máx real contra la recta del trapecio, que sigue de largo."""
    # Se corta en e/B = 0,35 para que la curva no se salga del marco: pasado ese
    # punto la Ec. (16.22) se dispara y aplasta toda la zona interesante.
    E_TOPE = 0.35
    es = np.linspace(0.0, E_TOPE * B_, 241)
    real = [presion_zapata_rigida(Q_, Q_ * e, B_, ANCHO_).q_max for e in es]
    trapecio = [Q_ / (B_ * ANCHO_) * (1.0 + 6.0 * e / B_) for e in es]

    lienzo = svg.Lienzo(
        alto=360,
        titulo="La fórmula del trapecio, pasado el núcleo, subestima",
        subtitulo=f"presión máxima bajo zapata rígida, B = {B_:.0f} m, "
                  f"Q = {Q_:.0f} kN",
    )
    ejes = lienzo.ejes(
        x=(0.0, E_TOPE), y=(0.0, 900.0),
        caja=(62, 92, 505, 274),
        etiqueta_x="e/B",
        etiqueta_y="q máx [kPa]",
        ticks_x=7, ticks_y=6,
    )
    ejes.curva([e / B_ for e in es], trapecio, color=svg.GRIS, ancho=2.0,
               guion="6 4")
    ejes.curva([e / B_ for e in es], real, color=svg.AZUL, ancho=2.4)

    # Los tres umbrales, rotulados arriba para no pisar los ticks del eje x.
    for frac, etiqueta, color in (
        (1.00, "núcleo central", svg.TENUE),
        (0.80, "80 % apoyado", svg.ROJO),
        (0.50, "50 %", svg.ROJO),
    ):
        e = excentricidad_para_fraccion(frac, B_)
        px = ejes.x(e / B_)
        lienzo.linea(px, ejes.y(0.0), px, 100, color=color, ancho=1.0, guion="3 3")
        lienzo.texto(px, 88, etiqueta, tam=10, color=color, anclaje="middle")

    # El hueco entre las dos curvas donde la norma pone el límite inferior.
    p_50 = presion_zapata_rigida(Q_, Q_ * E_50, B_, ANCHO_)
    q_trapecio_50 = Q_ / (B_ * ANCHO_) * (1.0 + 6.0 * E_50 / B_)
    px = ejes.x(E_50 / B_)
    lienzo.linea(px, ejes.y(q_trapecio_50), px, ejes.y(p_50.q_max),
                 color=svg.ROJO, ancho=2.2)
    lienzo.circulo(px, ejes.y(p_50.q_max), 3.5, color=svg.AZUL)
    lienzo.circulo(px, ejes.y(q_trapecio_50), 3.5, color=svg.GRIS)
    lienzo.texto(px + 9, ejes.y(p_50.q_max) + 4, f"{p_50.q_max:.0f}", tam=10.5,
                 color=svg.AZUL, negrita=True)
    lienzo.texto(px + 9, ejes.y(q_trapecio_50) + 10, f"{q_trapecio_50:.0f}",
                 tam=10.5, color=svg.GRIS, negrita=True)
    lienzo.texto(
        px - 9, ejes.y((p_50.q_max + q_trapecio_50) / 2) + 4,
        f"−{(1 - q_trapecio_50 / p_50.q_max) * 100:.0f} %",
        tam=11.5, color=svg.ROJO, anclaje="end", negrita=True,
    )

    # Arriba a la izquierda: la zona sobre la curva y antes del núcleo central,
    # la única que no cruzan ni las curvas ni las verticales de los umbrales.
    lienzo.leyenda(74, 128, [
        (svg.GRIS, "Q/(BL)·(1 + 6e/B) de largo"),
        (svg.AZUL, "q máx real (Das 16.20/16.22)"),
    ])
    lienzo.guardar("lab/figs/nota03-qmax.svg")


if __name__ == "__main__":
    main()
    figuras()
    print("\nFiguras escritas en lab/figs/nota03-*.svg")
