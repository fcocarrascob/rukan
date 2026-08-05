"""Nota 04 — cuándo la zapata deja de ser rígida, y qué L mide la norma.

**La pregunta:** la nota 03 mostró que el reparto de presiones bajo una zapata
**rígida** no depende del módulo de balasto: sale de equilibrio más la hipótesis
de contacto plano, y con ``k_s`` variando 100 a 1 la presión no se mueve. Pero
esa nota dio la rigidez por supuesta. ¿Dónde deja de valer el reparto plano, y
quién decide si una fundación es rígida?

**Lo que dice la norma.** NCh2369:2025 §10.1.4 clasifica una fundación
superficial como rígida si::

    L · ⁴√( k_v / (4·E·I) )  ≤  1                       (25)

con ``I = e³/12`` la inercia por unidad de longitud de fundación, ``e`` el
espesor, ``E`` el módulo de deformación del hormigón, ``k_v`` la rigidez
vertical sísmica del suelo, y ``L`` la **longitud de cálculo de la Tabla 10**.

Fuente: NCh2369:2025, 3.ª ed., §10.1.4 y Tabla 10 (ecuación y tabla
transcritas de las **páginas rasterizadas** del PDF, pp.125 y 131 del archivo —
impresas 118 y 124—, no de la capa de texto). §10.1.5, en la p.129 del archivo,
es la cláusula que exime a las flexibles del mínimo de área apoyada.

**Ojo con la notación:** la norma llama ``e`` al **espesor**; Das y la nota 03
llaman ``e`` a la **excentricidad**. Acá se llaman ``espesor`` y ``e``.

**Las cuatro cosas que muestra la nota**

1. **El límite rígido cierra.** Con la zapata muy gruesa, los dos caminos
   nuevos reproducen el trapecio y el triángulo cerrados de Das — o sea que la
   nota 03 es el caso ``λL → 0`` de esta.

2. **Con carga centrada la fundación flexible igual se despega.** Excentricidad
   cero, momento cero, y aun así los bordes se levantan: no es volcamiento sino
   curvatura. Con λL = 3 apoya el 46,5 %. El mínimo de área apoyada de §10.1.4
   —pensado para volcamiento de cuerpo rígido— confunde las dos cosas, y por eso
   §10.1.5 **exime** a las flexibles en vez de relajarlo. El fenómeno ya lo
   había encontrado el experimento de 5250 análisis en SAP2000 del blog («bajo
   carga axial pura ya hay casos con apenas 67 % de la base»); acá se reencuentra
   desde otro motor y se pone sobre el eje λL.

3. **El umbral λL = 1 no es donde el reparto plano se rompe.** Ahí el error ya
   vale 31,8 % en la carga centrada. La curva crece como λL⁴ desde el origen,
   sin codo: lo que el umbral separa es qué procedimiento de verificación
   aplica, no «vale / no vale». El criterio calibrado sobre el error —el
   K_r ≥ 1 del experimento, o sea λL ≈ 0,55 acá— es bastante más exigente.

4. **L no es B, y eso da vuelta el veredicto.** Para una zapata aislada, la
   única fila de la Tabla 10 que aplica es «Zarpa»: el voladizo desde la cara de
   la columna al borde. Con ese L la zapata de la nota 03 da λL ≈ 0,46; leyendo
   L como el largo de la zapata da λL ≈ 1,10. Rígida o flexible, según qué se
   midió. (Que la Tabla 10 da una L por **zona** y no por fundación ya está
   mostrado en el ejemplo de losa del blog; acá se usa, no se descubre.)

**Verificación (los dos caminos):** referencia = `lab/_lib/ref.py`,
`VigaSobreResortes` — rigidez directa en numpy puro con el contacto por
conjunto activo, que es el método que §10.1.4 pone **como ejemplo** —la cama de
resortes va con un «por ejemplo»— junto con la precaución que sí ordena («…de
existir resortes traccionados, éstos se deben anular»); motor = OpenSeesPy con
resortes ``ENT`` y análisis no lineal. `ref.py` no importa `rukan` ni
`openseespy`.

Correr::

    python -m lab.nota04_zapata_rigida_flexible
"""

from __future__ import annotations

import numpy as np
import openseespy.opensees as ops

from lab._lib import svg
from lab._lib.ref import (
    VigaSobreResortes,
    espesor_limite_nch2369,
    excentricidad_para_fraccion,
    lambda_l_nch2369,
    presion_zapata_rigida,
)
from lab._lib.report import Fila, reportar
from rukan import units as u

# ============================ DATOS DE ENTRADA ============================
# La misma zapata de la nota 03, para que las dos notas se encadenen.
B = 3.0 * u.ureg.m  # lado en la dirección de la excentricidad
ANCHO = 1.0 * u.ureg.m  # lado fuera del plano (zapata corrida, por metro)
Q = 600.0 * u.ureg.kN  # carga vertical de servicio
KV = 30_000.0 * u.ureg.kN / u.ureg.m**3  # balasto / rigidez vertical del suelo

# Lo que la nota 03 no necesitaba y la Ec. (25) sí: el ancho de la columna
# —porque de ahí sale la L de la Tabla 10— y el espesor de la zapata.
COLUMNA = 0.5 * u.ureg.m
ESPESOR = 0.60 * u.ureg.m

# Módulo de deformación del hormigón. Es **dato de entrada del modelo**, no un
# valor derivado de ninguna norma: la Ec. (25) lo pide y acá se declara.
E_HORMIGON = 2.35e7 * u.ureg.kN / u.ureg.m**2

N_RESORTES = 256  # misma malla que la nota 03: error 0,003 % contra la cerrada

B_ = u.length(B)
ANCHO_ = u.length(ANCHO)
Q_ = u.force(Q)
COLUMNA_ = u.length(COLUMNA)
ESPESOR_ = u.length(ESPESOR)
KV_ = KV.to(u.ureg.kN / u.ureg.m**3).magnitude
E_ = u.stress(E_HORMIGON)

# Tabla 10, fila «Zarpa»: distancia entre el borde de la fundación y el borde
# exterior de la columna. **No es B.** Ese es medio punto de la nota.
L_ZARPA = (B_ - COLUMNA_) / 2.0

# La excentricidad de la nota 03 que deja el 80 % apoyado (§10.1.4, menores).
E_80 = excentricidad_para_fraccion(0.80, B_)

# Los λL del barrido. Incluye el de la zapata real, para que el lector se ubique.
LAMBDA_REAL = lambda_l_nch2369(L_ZARPA, KV_, E_, ESPESOR_)
BARRIDO = (0.25, LAMBDA_REAL, 1.0, 1.5, 2.0, 3.0)

SUELO, RESORTE = 10_000, 20_000


def miles(v: float) -> str:
    """Separador de miles con espacio: en español la coma es el decimal, así que
    ``30,000 kN/m³`` se leería como treinta."""
    return f"{v:,.0f}".replace(",", " ")


def espesor_para(lambda_l: float, L: float = L_ZARPA) -> float:
    """Espesor que hace que la Ec. (25) dé exactamente ``lambda_l``.

    De ``λL ∝ espesor^(−3/4)`` sale ``espesor = espesor_límite / (λL)^(4/3)``,
    con el espesor límite el que da ``λL = 1``. Es solo la manera de mover el
    barrido: el parámetro que manda es λL, no el espesor.
    """
    return espesor_limite_nch2369(L, KV_, E_) / lambda_l ** (4.0 / 3.0)


def ei_para(espesor: float) -> float:
    """``E·I`` de la franja de un metro, con ``I = espesor³/12`` de la Ec. (25)."""
    return E_ * ANCHO_ * espesor**3 / 12.0


# ======================= LA CARGA, IGUAL PARA LOS DOS =======================
def cargas_columna(n: int, Q_kn: float, e: float) -> tuple[np.ndarray, np.ndarray]:
    """Cargas nodales de una columna de ancho ``COLUMNA`` centrada en la zapata.

    ``Q`` se reparte sobre la **huella real de la columna** por solape
    tributario, no como carga puntual: hace falta un ancho de columna para leer
    la Tabla 10, así que la geometría que define ``L`` y la que aplica la carga
    tienen que ser la misma. El momento ``M = Q·e`` va como momento concentrado
    en el nodo central, que es la idealización habitual de un pedestal.

    Devuelve ``(fuerzas, momentos)`` nodales con la convención del laboratorio:
    positivo hacia arriba, así que una carga que baja entra negativa. **Los dos
    caminos reciben este mismo vector** — es dato de entrada, no método.
    """
    h = B_ / n
    xs = np.arange(n + 1) * h
    izq, der = B_ / 2.0 - COLUMNA_ / 2.0, B_ / 2.0 + COLUMNA_ / 2.0

    # Cada nodo posee [x − h/2, x + h/2], recortado a la zapata. La fracción de
    # Q que le toca es la de su tramo que cae bajo la columna.
    lo = np.clip(xs - h / 2.0, 0.0, B_)
    hi = np.clip(xs + h / 2.0, 0.0, B_)
    solape = np.clip(np.minimum(hi, der) - np.maximum(lo, izq), 0.0, None)
    if not np.isclose(solape.sum(), COLUMNA_):
        raise RuntimeError("el solape con la huella de la columna no suma su ancho")

    fuerzas = -Q_kn * solape / solape.sum()
    momentos = np.zeros(n + 1)
    momentos[n // 2] = -Q_kn * e  # una carga −Q ĵ corrida +e x̂ da M_z = −Q·e
    return fuerzas, momentos


# ============================== OPENSEES ==================================
def modelo(Q_kn: float, e: float, espesor: float, *, n: int = N_RESORTES,
           kv: float = KV_) -> dict:
    """Zapata sobre resortes ``ENT``, con el espesor como parámetro.

    Es el modelo de la nota 03 con dos cambios: el ``EI`` sale del espesor por
    la ``I = e³/12`` de la Ec. (25) en vez de ser el de un cuerpo rígido, y la
    carga entra repartida sobre la huella de la columna.

    Los gotchas de la nota 03 siguen valiendo y están puestos: el ``zeroLength``
    va con el **nodo de suelo primero** (así el descenso de la zapata es
    compresión, lo único que el ``ENT`` resiste), la presión se lee de
    ``eleResponse(tag, "force")[1]``, y el área tributaria de los **dos resortes
    de borde es la mitad** o la reacción total no da ``Q``.
    """
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    h = B_ / n
    xs = np.arange(n + 1) * h
    trib = np.full(n + 1, h)
    trib[0] = trib[-1] = h / 2.0

    for k, x in enumerate(xs):
        ops.node(k + 1, float(x), 0.0)
        ops.node(SUELO + k, float(x), 0.0)
        ops.fix(SUELO + k, 1, 1, 1)
        rigidez = kv * float(trib[k]) * ANCHO_
        ops.uniaxialMaterial("ENT", RESORTE + k, rigidez)
        ops.element("zeroLength", RESORTE + k, SUELO + k, k + 1,
                    "-mat", RESORTE + k, "-dir", 2)

    ops.geomTransf("Linear", 1)
    ei = ei_para(espesor)
    for k in range(n):
        ops.element("elasticBeamColumn", k + 1, k + 1, k + 2, 1.0, ei, 1.0, 1)

    centro = n // 2 + 1
    ops.fix(centro, 1, 0, 0)  # los resortes no dan rigidez horizontal

    fuerzas, momentos = cargas_columna(n, Q_kn, e)
    ops.timeSeries("Constant", 1)
    ops.pattern("Plain", 1, 1)
    for k in range(n + 1):
        if fuerzas[k] or momentos[k]:
            ops.load(k + 1, 0.0, float(fuerzas[k]), float(momentos[k]))

    ops.system("BandGeneral")
    ops.numberer("Plain")
    ops.constraints("Plain")
    ops.test("NormDispIncr", 1e-12, 500, 0)
    ops.algorithm("Newton")  # es no lineal: el ENT cambia de rigidez
    ops.integrator("LoadControl", 0.1)
    ops.analysis("Static")
    if ops.analyze(10) != 0:
        # Con la zapata muy flexible el contacto cambia mucho por paso; se
        # reintenta con pasos más chicos antes de rendirse.
        ops.algorithm("KrylovNewton")
        ops.integrator("LoadControl", 0.01)
        if ops.analyze(100) != 0:
            raise RuntimeError(
                f"no convergió: Q = {Q_kn}, e = {e}, espesor = {espesor}, n = {n}"
            )

    fuerza = np.array(
        [ops.eleResponse(RESORTE + k, "force")[1] for k in range(n + 1)]
    )
    q = fuerza / (trib * ANCHO_)
    en_contacto = q > 1e-9
    return {
        "x": xs,
        "q": q,
        "q_max": float(q.max()),
        "a_contacto": float(trib[en_contacto].sum()),
        "reaccion": float(fuerza.sum()),
        "asentamiento": ops.nodeDisp(centro, 2),
    }


# ============================= REFERENCIA =================================
def referencia(Q_kn: float, e: float, espesor: float, *, n: int = N_RESORTES,
               kv: float = KV_):
    """El mismo problema por rigidez directa en numpy, con conjunto activo."""
    viga = VigaSobreResortes(B=B_, n=n, EI=ei_para(espesor), k_v=kv, ancho=ANCHO_)
    fuerzas, momentos = cargas_columna(n, Q_kn, e)
    return viga.resolver(fuerzas, momentos)


# ============================== LA NOTA ===================================
def main() -> None:
    print("# Nota 04 — cuándo la zapata deja de ser rígida\n")
    print(f"Zapata corrida: B = {B_:.1f} m, b = {ANCHO_:.1f} m, "
          f"Q = {Q_:.0f} kN, k_v = {miles(KV_)} kN/m³, {N_RESORTES} resortes")
    print(f"Columna de {COLUMNA_:.2f} m, espesor {ESPESOR_:.2f} m, "
          f"E = {E_:.3g} kN/m²")
    print(f"\nTabla 10, fila «Zarpa»: L = (B − c)/2 = {L_ZARPA:.3f} m "
          f"(**no** B = {B_:.1f} m).")
    print(f"Ec. (25) con ese L: λL = {LAMBDA_REAL:.4f} → "
          f"{'RÍGIDA' if LAMBDA_REAL <= 1 else 'FLEXIBLE'}.")
    print(f"Espesor al que λL = 1: {espesor_limite_nch2369(L_ZARPA, KV_, E_):.3f} m.\n")

    # Qué espesor tiene cada punto del barrido. Se imprime porque el extremo
    # flexible **no es una zapata que exista** con esta geometría: se llega ahí
    # adelgazando hasta el absurdo. La lectura útil de ese extremo es por
    # analogía con la losa, que alcanza el mismo λL con 0,60 m y luz de 6 m.
    print("El barrido, y con qué espesor se llega a cada λL con L de zarpa:\n")
    for lam in BARRIDO:
        print(f"  λL = {lam:>4.2f}   espesor {espesor_para(lam):6.3f} m")
    print()

    # --- 1. el límite rígido: la nota 03 es el caso λL → 0 -----------------
    espesor_rigido = espesor_para(0.05)  # zapata absurdamente gruesa, a propósito
    casos_rigidos = [
        (0.0, "centrada"),
        (E_80, "e/B = 0,233"),
    ]
    ref_rig = {e: referencia(Q_, e, espesor_rigido) for e, _ in casos_rigidos}
    ops_rig = {e: modelo(Q_, e, espesor_rigido) for e, _ in casos_rigidos}
    das = {e: presion_zapata_rigida(Q_, Q_ * e, B_, ANCHO_) for e, _ in casos_rigidos}

    reportar(
        "1. El límite rígido: los dos caminos nuevos reproducen a Das",
        [
            Fila(f"q_máx, carga {etiqueta} — OpenSees", "kPa",
                 ref=das[e].q_max, ops=ops_rig[e]["q_max"], tol_pct=0.5)
            for e, etiqueta in casos_rigidos
        ] + [
            Fila(f"q_máx, carga {etiqueta} — numpy", "kPa",
                 ref=das[e].q_max, ops=ref_rig[e].q_max, tol_pct=0.5)
            for e, etiqueta in casos_rigidos
        ],
        ref_label="Fórmula cerrada (Das §16.7)",
        ops_label="Viga sobre resortes, λL = 0,05",
        nota=("λL = 0,05 no es un espesor de zapata: es la **idealización de "
              "cuerpo rígido** de la nota 03 escrita en la escala de esta nota. "
              "Ahí la viga sobre resortes vuelve al trapecio y al triángulo "
              "cerrados, o sea que **la nota 03 es el caso límite de esta**."),
    )

    # --- 2. carga centrada: el reparto plano se rompe sin despegue ---------
    centrada_ref = {lam: referencia(Q_, 0.0, espesor_para(lam)) for lam in BARRIDO}
    centrada_ops = {lam: modelo(Q_, 0.0, espesor_para(lam)) for lam in BARRIDO}

    reportar(
        "2. Carga centrada — los dos caminos, a lo largo del barrido",
        [
            Fila(f"q_máx con λL = {lam:.2f}", "kPa",
                 ref=centrada_ref[lam].q_max, ops=centrada_ops[lam]["q_max"],
                 tol_pct=0.5)
            for lam in BARRIDO
        ],
        ref_label="numpy (conjunto activo)",
        ops_label="OpenSees (resortes ENT)",
        nota=("Esta tabla es la **verificación**: dos solvers distintos, mismo "
              "número. El hallazgo viene en la tabla 4."),
    )

    q_plano_centrada = Q_ / (B_ * ANCHO_)
    print("\nY acá aparece lo que el reparto plano no puede ni nombrar. La carga\n"
          "está en el centro exacto: excentricidad cero, momento cero.\n")
    for lam in BARRIDO:
        r = centrada_ref[lam]
        marca = ""
        if r.fraccion_apoyada < 0.80:
            marca = "  ← no cumple el 80 % de §10.1.4"
        if r.fraccion_apoyada < 0.50:
            marca = "  ← no cumple ni el 50 %"
        print(f"  λL = {lam:>4.2f}   apoyado {r.fraccion_apoyada * 100:5.1f} %"
              f"   q_máx {r.q_max:7.2f} kPa"
              f"  ({r.q_max / q_plano_centrada:.2f}× el Q/A de "
              f"{q_plano_centrada:.0f} kPa){marca}")
    print("\n  Sin excentricidad ninguna, la zapata flexible **igual se despega**.\n"
          "  No es volcamiento: es la zapata que se curva y levanta los bordes.\n"
          "  El área apoyada de §10.1.4 no distingue las dos cosas, y reprobaría\n"
          "  una fundación perfectamente centrada. Por eso §10.1.5 se lo saca de\n"
          "  encima a las flexibles y lo cambia por tolerancia al levantamiento.")

    # --- 3. carga excéntrica: el triángulo se deforma ----------------------
    exc_ref = {lam: referencia(Q_, E_80, espesor_para(lam)) for lam in BARRIDO}
    exc_ops = {lam: modelo(Q_, E_80, espesor_para(lam)) for lam in BARRIDO}

    reportar(
        "3. Carga excéntrica (e/B = 0,2333) — los dos caminos",
        [
            Fila(f"q_máx con λL = {lam:.2f}", "kPa",
                 ref=exc_ref[lam].q_max, ops=exc_ops[lam]["q_max"], tol_pct=0.5)
            for lam in BARRIDO
        ],
        ref_label="numpy (conjunto activo)",
        ops_label="OpenSees (resortes ENT)",
        nota="La excentricidad es la misma de la nota 03: el 80 % de §10.1.4.",
    )

    print("\nLa fracción apoyada, que es lo que §10.1.4 acota:\n")
    for lam in BARRIDO:
        print(f"  λL = {lam:>4.2f}   apoyado "
              f"{exc_ref[lam].fraccion_apoyada * 100:5.1f} % (numpy), "
              f"{exc_ops[lam]['a_contacto'] / B_ * 100:5.1f} % (OpenSees)")

    # --- 4. el hallazgo: cuánto se equivoca el reparto plano ---------------
    q_plano_exc = presion_zapata_rigida(Q_, Q_ * E_80, B_, ANCHO_).q_max
    reportar(
        "4. El hallazgo: lo que el reparto plano deja de ver",
        [
            Fila(f"q_máx centrada, λL = {lam:.2f}", "kPa",
                 ref=q_plano_centrada, ops=centrada_ref[lam].q_max, tol_pct=500.0)
            for lam in BARRIDO
        ],
        ref_label="Reparto plano (Q/A)",
        ops_label="Viga sobre resortes",
        nota=("Tolerancia enorme a propósito: acá el error **es** el resultado. "
              "La columna «Error» es cuánto subestima el reparto plano."),
    )
    reportar(
        "4b. Lo mismo, con la carga excéntrica",
        [
            Fila(f"q_máx excéntrica, λL = {lam:.2f}", "kPa",
                 ref=q_plano_exc, ops=exc_ref[lam].q_max, tol_pct=500.0)
            for lam in BARRIDO
        ],
        ref_label="Triángulo de Das",
        ops_label="Viga sobre resortes",
        nota=("Acá el error **no** es monótono, y el signo hay que leerlo en la "
              "columna del medio: alrededor de λL = 1 la zapata flexible alivia "
              "el pico del triángulo y el reparto plano queda del lado seguro. "
              "Pasado eso se da vuelta."),
    )

    print("\nDónde el reparto plano deja de ser conservador, en la carga "
          "excéntrica:\n")
    for lam in BARRIDO:
        q = exc_ref[lam].q_max
        lado = "seguro (sobrestima)" if q < q_plano_exc else "INSEGURO (subestima)"
        print(f"  λL = {lam:>4.2f}   q_máx {q:8.2f} kPa   vs {q_plano_exc:.0f} "
              f"del triángulo   → del lado {lado}")

    # --- 5. Ec. (25): quién es L, y cuánto pesa k_v ------------------------
    print("\n### 5. La Ec. (25) sobre esta zapata, según qué L se lea\n")
    print("| Lectura de L | L [m] | λL | Ec. (25) | Espesor que exigiría |")
    print("|---|---|---|---|---|")
    for etiqueta, L in (
        ("Tabla 10, fila «Zarpa» — la que aplica", L_ZARPA),
        ("El largo de la zapata (lectura equivocada)", B_),
    ):
        lam = lambda_l_nch2369(L, KV_, E_, ESPESOR_)
        veredicto = "≤ 1 → **rígida**" if lam <= 1.0 else "> 1 → **flexible**"
        print(f"| {etiqueta} | {L:.2f} | {lam:.4f} | {veredicto} "
              f"| {espesor_limite_nch2369(L, KV_, E_):.3f} m |")
    print("\nMisma zapata, mismo suelo, veredicto opuesto. La última columna es "
          "el espesor\nal que cada lectura daría λL = 1: leer mal la L pide una "
          "zapata "
          f"{espesor_limite_nch2369(B_, KV_, E_) / espesor_limite_nch2369(L_ZARPA, KV_, E_):.1f}×\n"
          "más gruesa, porque λL va con L a la primera y con el espesor a la −3/4.")

    print("\n### 5b. Y el balasto, que no cambia el reparto rígido, sí cambia esto\n")
    print("| k_v | λL (L de zarpa) | Ec. (25) | Espesor al que λL = 1 |")
    print("|---|---|---|---|")
    for f in (0.1, 1.0, 10.0):
        kv = KV_ * f
        lam = lambda_l_nch2369(L_ZARPA, kv, E_, ESPESOR_)
        veredicto = "rígida" if lam <= 1.0 else "flexible"
        e_lim = espesor_limite_nch2369(L_ZARPA, kv, E_)
        print(f"| k_v × {f:g} = {miles(kv)} kN/m³ | {lam:.4f} | {veredicto} "
              f"| {e_lim:.3f} m |")

    # --- 6. Tabla 10 sobre geometrías típicas -----------------------------
    print("\n### 6. Las filas de la Tabla 10, sobre geometrías corrientes\n")
    print(f"(espesor {ESPESOR_:.2f} m, k_v = {miles(KV_)} kN/m³, E = {E_:.3g} kN/m²)\n")
    print("| Elemento (Tabla 10) | L [m] | λL | Ec. (25) |")
    print("|---|---|---|---|")
    for etiqueta, L in (
        (f"Zarpa — zapata B = {B_:.0f} m, columna {COLUMNA_:.2f} m", L_ZARPA),
        ("Losa entre columnas con luz libre de 6 m", 6.0),
        ("Paño de losa con 3 muros, lx = 5 m → L = 1,2 lx", 1.2 * 5.0),
        ("Paño de losa cerrado, lx = 5 m → L = 0,95 lx", 0.95 * 5.0),
    ):
        lam = lambda_l_nch2369(L, KV_, E_, ESPESOR_)
        veredicto = "rígida" if lam <= 1.0 else "**flexible**"
        print(f"| {etiqueta} | {L:.2f} | {lam:.3f} | {veredicto} |")
    print("\nEl criterio no está escrito para la zapata aislada: para volverla\n"
          "flexible habría que adelgazarla hasta un espesor que nadie construye.\n"
          "Está escrito para la losa, que es donde λL se pasa de 1 sola.")

    # --- equilibrio: la guarda que atrapa el área tributaria mal puesta ----
    for lam in BARRIDO:
        for r, nombre in ((centrada_ref[lam], "centrada"), (exc_ref[lam], "excéntrica")):
            assert abs(r.reaccion - Q_) / Q_ < 1e-6, (
                f"la resultante de las presiones ({nombre}, λL = {lam}) no da Q: "
                f"{r.reaccion:.4f} vs {Q_:.4f}"
            )
    print(f"\n> Equilibrio verificado en las {2 * len(BARRIDO)} corridas de "
          "referencia: la resultante de las presiones da Q.")


# ============================== FIGURAS ===================================
def figuras() -> None:
    _fig_perfiles()
    _fig_error()


PANELES = (0.25, 1.0, 2.0, 3.0)


def _fig_perfiles() -> None:
    """El reparto plano deformándose, en las dos cargas.

    Los perfiles salen del **motor** nodo por nodo, no de la referencia: en una
    serie cuya tesis son los dos caminos separados, una figura rotulada como
    OpenSees tiene que salir de OpenSees. La tabla 2 dice que difieren menos de
    0,5 %.
    """
    centrada = {lam: modelo(Q_, 0.0, espesor_para(lam)) for lam in PANELES}
    excentrica = {lam: modelo(Q_, E_80, espesor_para(lam)) for lam in PANELES}
    q_plano_c = Q_ / (B_ * ANCHO_)
    das_exc = presion_zapata_rigida(Q_, Q_ * E_80, B_, ANCHO_)

    tope = max(
        max(r["q_max"] for r in centrada.values()),
        max(r["q_max"] for r in excentrica.values()),
    )
    tope = float(np.ceil(tope / 200.0) * 200.0)

    lienzo = svg.Lienzo(
        alto=352,
        titulo="Al ablandarse la zapata, el reparto plano se vuelve joroba",
        subtitulo=f"presión de contacto del modelo de resortes ENT — B = {B_:.0f} m, "
                  f"Q = {Q_:.0f} kN, columna de {COLUMNA_:.2f} m",
    )

    colores = (svg.AZUL, "#4a90c2", "#c98a2e", svg.ROJO)
    cajas = ((58, 100, 268, 258), (330, 100, 540, 258))
    datos = (
        ("carga centrada", centrada, [q_plano_c, q_plano_c]),
        ("e/B = 0,233", excentrica, None),
    )

    for (titulo, corridas, plano), caja in zip(datos, cajas):
        ejes = lienzo.ejes(
            x=(0.0, B_), y=(0.0, tope), caja=caja,
            etiqueta_x="x [m]", ticks_x=3, ticks_y=4,
        )
        for color, lam in zip(colores, PANELES):
            r = corridas[lam]
            ejes.curva(r["x"], r["q"], color=color, ancho=1.9)
        # El reparto plano va **último** para que quede encima: en los λL
        # chicos coincide con la curva y si no, no se vería.
        if plano is not None:
            ejes.curva([0.0, B_], plano, color=svg.GRIS, ancho=1.8, guion="6 4")
        else:
            a = das_exc.a_contacto
            ejes.curva([0.0, B_ - a, B_], [0.0, 0.0, das_exc.q_max],
                       color=svg.GRIS, ancho=1.8, guion="6 4")
        lienzo.texto((caja[0] + caja[2]) / 2, 92, titulo, tam=11.5,
                     color=svg.TINTA, anclaje="middle", negrita=True)

    lienzo.texto(6, 84, "q [kPa]", tam=11, color=svg.TENUE)
    lienzo.leyenda(58, 320, [(c, f"λL = {lam:g}") for c, lam in
                             zip(colores[:2], PANELES[:2])])
    lienzo.leyenda(188, 320, [(c, f"λL = {lam:g}") for c, lam in
                              zip(colores[2:], PANELES[2:])])
    lienzo.leyenda(318, 320, [(svg.GRIS, "reparto plano: Q/A a la izquierda,")])
    lienzo.texto(342, 336, "triángulo de Das a la derecha", tam=10.5,
                 color=svg.TEXTO)
    lienzo.guardar("lab/figs/nota04-perfiles.svg")


def _fig_error() -> None:
    """Cuánto subestima el reparto plano, contra λL, con el umbral de la norma."""
    lams = np.geomspace(0.15, 4.0, 60)
    q_plano_c = Q_ / (B_ * ANCHO_)
    q_plano_e = presion_zapata_rigida(Q_, Q_ * E_80, B_, ANCHO_).q_max

    err_c = [referencia(Q_, 0.0, espesor_para(l)).q_max / q_plano_c * 100 - 100
             for l in lams]
    err_e = [referencia(Q_, E_80, espesor_para(l)).q_max / q_plano_e * 100 - 100
             for l in lams]
    tope = float(np.ceil(max(max(err_c), max(err_e)) / 50.0) * 50.0)
    # El caso excéntrico se mete en negativo alrededor de λL = 1 —ahí la zapata
    # flexible alivia el pico del triángulo—, así que el eje tiene que bajar.
    piso = float(np.floor(min(min(err_c), min(err_e)) / 50.0) * 50.0)

    lienzo = svg.Lienzo(
        alto=360,
        titulo="Cuánto se aparta el reparto plano, y dónde lo corta la norma",
        subtitulo="q máx real contra la hipótesis de distribución plana",
    )
    ejes = lienzo.ejes(
        x=(0.0, 4.0), y=(piso, tope), caja=(62, 96, 505, 264),
        etiqueta_x="λL de la Ec. (25) — NCh2369:2025 §10.1.4",
        etiqueta_y="q máx real / q máx plano − 1  [%]",
        ticks_x=8, ticks_y=int((tope - piso) / 50),
    )

    # El umbral de la norma: a la izquierda vale la hipótesis plana.
    lienzo.rect(ejes.x(0.0), 96, ejes.x(1.0) - ejes.x(0.0), 264 - 96,
                color=svg.VERDE, radio=0, opacidad=0.07)
    lienzo.linea(ejes.x(1.0), 96, ejes.x(1.0), 264, color=svg.VERDE,
                 ancho=1.6, guion="4 3")
    lienzo.texto(ejes.x(1.0) - 6, 110, "λL = 1  ·  rígida", tam=10,
                 color=svg.VERDE, anclaje="end", negrita=True)

    ejes.curva(lams, err_c, color=svg.AZUL, ancho=2.4)
    ejes.curva(lams, err_e, color=svg.ROJO, ancho=2.4)

    # Los puntos del motor encima de la curva de la referencia: los dos caminos.
    for lam in BARRIDO:
        if lam > 4.0:
            continue
        ejes.marcar(lam, modelo(Q_, 0.0, espesor_para(lam))["q_max"] / q_plano_c
                    * 100 - 100, "", color=svg.AZUL, dx=0, dy=0)
        ejes.marcar(lam, modelo(Q_, E_80, espesor_para(lam))["q_max"] / q_plano_e
                    * 100 - 100, "", color=svg.ROJO, dx=0, dy=0)

    # La zapata real, con la L que corresponde y con la que no.
    lam_mal = lambda_l_nch2369(B_, KV_, E_, ESPESOR_)
    for lam, etiqueta, color, dy in (
        (LAMBDA_REAL, f"zarpa: λL = {LAMBDA_REAL:.2f}", svg.TINTA, 30),
        (lam_mal, f"si L fuera B: {lam_mal:.2f}", svg.TENUE, 44),
    ):
        px = ejes.x(lam)
        lienzo.linea(px, 264, px, 272, color=color, ancho=1.2)
        lienzo.texto(px, 264 + dy, etiqueta, tam=9.5, color=color,
                     anclaje="middle")

    lienzo.leyenda(80, 130, [
        (svg.AZUL, "carga centrada (e = 0)"),
        (svg.ROJO, "e/B = 0,233 (80 % apoyado si es rígida)"),
    ])
    lienzo.texto(80, 168, "· puntos = OpenSees, curva = numpy", tam=9.5,
                 color=svg.TENUE)
    lienzo.guardar("lab/figs/nota04-error.svg")


if __name__ == "__main__":
    main()
    figuras()
    print("\nFiguras escritas en lab/figs/nota04-*.svg")
