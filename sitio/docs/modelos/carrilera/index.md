# La viga carrilera

Un vano de la carrilera del [galpón con puente grúa](../galpon-grua/): una viga soldada
monosimétrica, simplemente apoyada entre dos marcos, con las dos ruedas de un testero encima.
Es el modelo del eslabón 08 de la serie
[`nch2369-galpon-grua`](../../series/nch2369-galpon-grua/), y está aquí y no dentro del galpón
porque el galpón no la tiene: allá el riel entrega su reacción directamente en la columna.

Cuatro nudos y tres barras. La entrada más pequeña del sitio, y la que mejor muestra lo que el
motor hace entre dos nudos.

## El modelo

<rukan-visor src="carrilera.escena.json" vista="longitudinal"></rukan-visor>

`A` y `B` son los apoyos; `W1` y `W2`, las dos ruedas. La sección viene de
`verification/case11_data.carrilera_props()` —ala superior 350 × 20, alma 650 × 8, ala inferior
250 × 14— con el eje neutro donde lo pone el equilibrio de áreas y no en el medio del canto. La
viga corre en X y los ejes locales están puestos de modo que la flexión vertical use la inercia
fuerte: su momento es `Mz`, que es como el memo lo llama.

Que sean **tres barras y no treinta** es la decisión de fondo de esta entrada. Las dos posiciones
de rueda son nudos, así que la única carga de vano es el peso propio, uniforme, y la fórmula con
que Rukan superpone el vano sobre las fuerzas de extremo vale **exacta** en cada barra: el
diagrama que se dibuja abajo no está muestreado, está resuelto. Mallar más no acercaría nada —la
solución de una viga Euler-Bernoulli prismática con carga uniforme es exacta en los nudos, que es
lo que la nota 01 del laboratorio estableció— y taparía justamente lo que hay que ver.

Dos cosas que este modelo idealiza y conviene tener presentes. La primera: **la densidad no es la
del acero**. El peso lineal de la carrilera es la viga más el riel ASCE que corre encima, y el
riel no es un elemento de este modelo; su peso entra por la única puerta que el archivo de
proyecto tiene para una carga repartida —el peso propio— con una densidad equivalente que hace
`ρ·A·g` igual al peso lineal del memo. El control es directo: el peso del vano sale
{{ r('carrilera', 'peso_total', 4) }} kN sobre los 7,50 m de luz, que es el `w_carril` del 08.
La segunda: el apoyo simple **no es una simplificación**. AIST §5.8.1 prohíbe que se desarrolle
continuidad apreciable entre vanos adyacentes, y el 08 lo discute.

## Los casos

Tres casos y una combinación.

| Caso | Qué es |
|---|---|
| `D` | el peso propio, distribuido: {{ r('carrilera', 'peso_total', 3) }} kN en el vano |
| `Rv` | las dos ruedas con impacto vertical, la carga que el eslabón 03 publica |
| `Rw` | las mismas dos ruedas **sin** impacto, que es con lo que se miran servicio y fatiga |
| `U` | la combinación de NCh3171 §9.1.1 (2): `1,2 D + 1,6 Rv` |

`U` es **la primera combinación que este repositorio publica**. El archivo de proyecto, el
runner y la escena las soportaban desde que el caso 8 las verificó contra SAP2000, y ningún
modelo del sitio las había usado todavía.

<rukan-visor src="carrilera.escena.json" caso="U" vista="longitudinal"></rukan-visor>

## El diagrama

Elige `Mz` y el visor dibuja el momento a lo largo de la viga.

<rukan-visor src="carrilera.escena.json" caso="U" esfuerzo="Mz" filtro="CAR_*" vista="longitudinal"></rukan-visor>

El máximo cae **bajo la primera rueda**, no en el centro, y vale
{{ r('carrilera', 'M_ux', 5, factor=-1) }} kN·m. El signo que el visor dibuja es el del diagrama
de Rukan, no el de la fibra traccionada: con la carga hacia abajo el momento de vano sale
negativo, y lo que se compara con el memo es la magnitud.

En el centro del vano el momento **baja** a {{ r('carrilera', 'M_centro', 5, factor=-1) }} kN·m:
entre las dos ruedas el diagrama no crece, y por eso la posición de momento máximo del 08 · D1
no es la rueda al centro. Los cuartos de vano valen
{{ r('carrilera', 'M_L4', 5, factor=-1) }} y {{ r('carrilera', 'M_3L4', 5, factor=-1) }} kN·m —
con el del centro y el máximo, las cuatro cifras que el eslabón 08 mete en su `C_b`. Lo que
cierra contra el memo no es un punto: es el diagrama entero.

El equilibrio cierra a mano: la reacción izquierda vale
{{ r('carrilera', 'R_izq', 5) }} kN y el corte en el apoyo,
{{ r('carrilera', 'V_ux', 5, factor=-1) }} kN.

### Y la parábola, que aquí es chica y hay que decirlo

Entre `W1` y `W2` el tramo es **una sola barra** de 3,40 m, así que si el diagrama fuera la recta
entre las dos fuerzas de extremo —que es todo lo que la salida del elemento entrega— faltaría la
parábola del peso propio. Rukan la superpone. Pero conviene mirar cuánto vale antes de celebrarla:
el peso propio solo, sobre el vano entero, da {{ r('carrilera', 'M_D_centro', 5, factor=-1) }}
kN·m en el centro, contra los {{ r('carrilera', 'M_ux', 5, factor=-1) }} kN·m del máximo. A esa
escala no se ve, y el diagrama de arriba se parece mucho a la poligonal por los nudos.

Que sea chica no la hace despreciable ni la hace visible: es una cifra que el motor calcula y que
no está en ninguna de las doce fuerzas de extremo de esa barra. Donde el mismo mecanismo **sí**
cambia el signo del resultado es en una viga empotrada-apoyada bajo carga repartida, que es lo
que la nota 01 del laboratorio midió: allá interpolar linealmente da −16,9 kN·m donde el real es
+25,3.

## Límites

**Sin impacto, sin empuje lateral, sin torsión.** El modelo carga las ruedas verticalmente sobre
el eje de la viga. El empuje lateral, la excentricidad del riel sobre el alma y el par torsor que
esa excentricidad introduce —que es lo que dimensiona la viga en el 08 · E4— **no están aquí**:
son flexión débil y torsión, y se resuelven a mano en el memo. La torsión de barra de Rukan,
además, sigue sin contraste contra SAP2000.

**Este vano no es el de flecha máxima.** La flecha que reporta,
{{ r('carrilera', 'd_W1', 3, factor=-1000) }} mm bajo la primera rueda con la carga de servicio,
es la de la posición de **momento** máximo. La posición de flecha máxima es otra y el 08 la
calcula aparte; este modelo no la corre.

**Una viga, no la carrilera.** Son 7,50 m de los 30 que corren por cada lado de la nave. Lo que
pasa en el apoyo —la ménsula, el asiento, el atiesador— es del eslabón 10.

## Procedencia

{{ procedencia('carrilera') }}

Los tres archivos viven junto a esta página:
[`carrilera.proyecto.json`](carrilera.proyecto.json), el modelo con sus casos y sus salidas;
[`carrilera.resultados.json`](carrilera.resultados.json), lo que `python -m rukan run` reportó; y
[`carrilera.escena.json`](carrilera.escena.json), lo que el visor dibuja. Para regenerarlos:

```bash
python sitio/docs/modelos/carrilera/_generar.py
python -m rukan run    sitio/docs/modelos/carrilera/carrilera.proyecto.json
python -m rukan escena sitio/docs/modelos/carrilera/carrilera.proyecto.json
```

El generador importa la sección de `verification/case11_data.py`, y un test del repo comprueba
que lo que produce es, byte a byte, el proyecto versionado aquí.
