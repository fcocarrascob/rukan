"""Escribe `carrilera.proyecto.json`: la viga carrilera del eslabón 08.

    python sitio/docs/modelos/carrilera/_generar.py [salida]

Un vano de la carrilera del galpón con puente grúa: simplemente apoyado sobre
`s_marco`, con las dos ruedas de un testero encima. AIST §5.8.1 **prohíbe** que
se desarrolle continuidad apreciable entre vanos adyacentes, así que el apoyo
simple no es una simplificación del modelo: es lo que la norma prescribe.

**Cuatro nudos y tres barras**, y eso es a propósito. Las dos posiciones de rueda
que el 08 · D1 fija son nudos, así que las cargas son nodales y la única carga de
vano es el peso propio, uniforme: la fórmula de `rukan.esfuerzos` vale **exacta**
en cada barra y el diagrama que el visor dibuja no está muestreado, está resuelto.
Mallar más no acercaría nada —la solución de una viga Euler-Bernoulli prismática
con carga uniforme es exacta en los nudos, que es lo que la nota 01 del
laboratorio estableció— y taparía justamente lo que esta entrada muestra: que
entre dos nudos hay una parábola que la salida del elemento no reporta.

Es el complemento del galpón, donde con dieciséis tramos por corte cada barra es
corta y la parábola es una corrección pequeña. Acá un miembro entero **es** un
solo elemento.

## La sección y su densidad

La sección es la del 08: monosimétrica, ala superior 350 × 20, alma 650 × 8, ala
inferior 250 × 14. Sale de `case11_data.carrilera_props()`, que reproduce las
cuatro propiedades que el memo publica.

La **densidad no es la del acero**, y hay que decirlo: el `w_carril` del 08 · C4
es la viga **más el riel** ASCE 85 lb/yd que corre encima. El riel no es un
elemento de este modelo, así que su peso entra por la única puerta que el esquema
de proyecto tiene para una carga repartida —el peso propio—, con una densidad
equivalente que hace `ρ·A·g = w_carril`. Es un artificio declarado, no un dato: el
acero de la viga pesa 7,85 t/m³.

## Los ejes locales

La viga corre en X y `vecxz = (0, −1, 0)` pone el eje local **y** hacia arriba, de
modo que la flexión vertical usa `Iz` —la inercia fuerte— y su momento es `Mz`,
que es como el memo lo llama (`M_ux`, el momento en el eje fuerte). El eje local
`z` queda horizontal y `My` es la flexión débil, la del empuje lateral.

El signo es el del diagrama de Rukan, no el de la fibra traccionada: con la carga
hacia abajo, el momento de vano sale **negativo**. La magnitud es la del memo.

## Casos y combinación

`Rv` y `Rw` son la misma pareja de ruedas con las dos cargas que el 03 publica:
con impacto vertical (`Rv_max`, 03 · C1) y sin él (`Rw_max`, 03 · B2). `D` es el
peso propio. La combinación `U` es la de NCh3171 §9.1.1 (2) que el 08 · D2 elige
por sobre la 2c de AIST, y **es la primera combinación que este repositorio
ejerce**: el esquema, el runner y la escena las soportaban desde el caso 8 y
ningún modelo publicado las había usado.

Después: `python -m rukan run` y `python -m rukan escena` sobre el JSON.
"""

from __future__ import annotations

import os
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 4))
sys.path.insert(0, os.path.join(RAIZ, "verification"))

import case11_data as D  # noqa: E402
from rukan import io, loads  # noqa: E402
from rukan.model import FrameElement, Material, Model, Node, Section  # noqa: E402

# Las dos ruedas en la posición de momento máximo (08 · D1): el centro del vano
# bisecta la distancia entre la primera rueda y la resultante de las dos.
X1 = D.SEP / 2.0 - D.WB_RUEDAS / 4.0
X2 = X1 + D.WB_RUEDAS
VECXZ = (0.0, -1.0, 0.0)          # deja el eje local y hacia arriba


def modelo() -> Model:
    A, i_fuerte, i_debil, J = D.carrilera_props()
    # `ρ·A·g = w_carril`: la viga más el riel que corre encima (08 · C4).
    w_carril = (A * D.RHO_STEEL + D.M_RIEL_LIN) * D.G_MEMO
    rho_eq = w_carril / (A * loads.G)
    nudos = [
        Node(1, 0.0, 0.0, 0.0, (True, True, True, True, False, False), "A"),
        Node(2, X1, 0.0, 0.0, nombre="W1"),
        Node(3, X2, 0.0, 0.0, nombre="W2"),
        Node(4, D.SEP, 0.0, 0.0, (False, True, True, False, False, False), "B"),
    ]
    barras = [FrameElement(k, k, k + 1, 1, 1, VECXZ, nombre="CAR_%d" % k)
              for k in (1, 2, 3)]
    return Model(
        nodes=nudos,
        materials=[Material(1, E=D.E_STEEL, nu=D.NU, rho=rho_eq)],
        sections=[Section(1, A=A, Iy=i_debil, Iz=i_fuerte, J=J, nombre="CARRILERA")],
        elements=barras,
        masses=[])


def proyecto() -> io.Proyecto:
    ruedas = lambda P: {"nodales": [{"nudo": n, "F": [0, 0, -P, 0, 0, 0]}
                                    for n in ("W1", "W2")]}
    return io.Proyecto(
        model=modelo(),
        titulo="Viga carrilera — nch2369-galpon-grua",
        origen={"script": "sitio/docs/modelos/carrilera/_generar.py",
                "generador": "case11_data.carrilera_props() sobre un vano de s_marco"},
        casos={"D": {"peso_propio": "distribuido"},
               "Rv": ruedas(D.RV_MAX),
               "Rw": ruedas(D.RW_MAX)},
        combinaciones={"U": {"D": 1.2, "Rv": 1.6}},
        salidas={
            # El momento de diseño del 08 · D2, en la rueda de momento máximo.
            "M_ux": {"que": "esfuerzo", "barra": "CAR_1", "componente": "Mz",
                     "x_rel": 1.0, "caso": "U"},
            # El de servicio del 08 · D1: las ruedas sin impacto y sin peso propio.
            "M_serv": {"que": "esfuerzo", "barra": "CAR_1", "componente": "Mz",
                       "x_rel": 1.0, "caso": "Rw"},
            # Los tres cuartos de vano. El del centro **no** es el máximo: entre
            # las dos ruedas el diagrama baja. Son los tres que el 08 · E2 mete
            # en su `C_b`, así que contrastan el diagrama entero y no un punto.
            "M_L4": {"que": "esfuerzo", "barra": "CAR_1", "componente": "Mz",
                     "x": D.SEP / 4.0, "caso": "U"},
            "M_centro": {"que": "esfuerzo", "barra": "CAR_2", "componente": "Mz",
                         "x": D.SEP / 2.0 - X1, "caso": "U"},
            "M_3L4": {"que": "esfuerzo", "barra": "CAR_2", "componente": "Mz",
                      "x": 3.0 * D.SEP / 4.0 - X1, "caso": "U"},
            # La parábola sola: el momento del peso propio en el centro del vano,
            # `wL²/8`, que es lo único que separa el diagrama de la poligonal por
            # los nudos. El 09 lo publica.
            "M_D_centro": {"que": "esfuerzo", "barra": "CAR_2", "componente": "Mz",
                           "x": D.SEP / 2.0 - X1, "caso": "D"},
            # El corte y la reacción de apoyo, que cierran el equilibrio.
            "V_ux": {"que": "esfuerzo", "barra": "CAR_1", "componente": "Vy",
                     "x_rel": 0.0, "caso": "U"},
            "R_izq": {"que": "reaccion", "nudo": "A", "gdl": "Uz", "caso": "U"},
            "R_der": {"que": "reaccion", "nudo": "B", "gdl": "Uz", "caso": "U"},
            # La flecha bajo la primera rueda con la carga de servicio.
            "d_W1": {"que": "desplazamiento", "nudo": "W1", "gdl": "Uz",
                     "caso": "Rw"},
            # El peso del vano: dividido por la luz da el `w_carril` del 08 · C4.
            "peso_total": {"que": "peso_total"},
        })


def main(argv: list[str]) -> int:
    salida = argv[1] if len(argv) > 1 else \
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "carrilera.proyecto.json")
    p = proyecto()
    io.save(p, salida)
    print(f"escrito {salida}: {len(p.model.nodes)} nudos, {len(p.model.elements)} barras, "
          f"{len(p.casos)} casos, {len(p.combinaciones)} combinaciones, "
          f"{len(p.salidas)} salidas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
