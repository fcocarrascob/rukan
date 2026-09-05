# El galpón con puente grúa

El modelo tridimensional del galpón de la serie
[`nch2369-galpon-grua`](../../series/nch2369-galpon-grua/): cinco marcos de momento de alma
variable, techo arriostrado, X de muro en los dos vanos extremos y un puente grúa sobre un
riel a 7,50 m. Esta es la ficha del modelo: qué es, cómo se mueve y de dónde sale cada
archivo. Lo que el modelo dice sobre la serie, los períodos, las rigideces y el hallazgo de
la `k_Y`, lo narra [el eslabón 00](../../series/nch2369-galpon-grua/00-el-modelo/).

## El modelo en 3D

Orbita con el ratón, o elige una vista fija. Al pasar el cursor por una barra aparece su
nombre y su sección; por un nudo, su nombre y sus coordenadas.

<rukan-visor src="galpon-grua.escena.json" vista="iso"></rukan-visor>

Es el galpón de `verification/case11_data.py` con la malla del memo 00 de la serie: 16
tramos prismáticos por corte, 965 nudos y 1 044 barras. Los nombres siguen la convención del
caso 11: `K3A_2` es un tramo de la columna del marco 3 en el muro A, `R3_0` el alero A del
marco 3, `DTA2_1` una diagonal de techo del vano 2. Los cubos son los apoyos empotrados y
los puntos, los 35 nudos que llevan masa.

Lo que el modelo idealiza: la masa es la de la serie, por áreas tributarias, en los nudos de
las siete líneas de techo, y no el peso propio de las barras; el alma variable se discretiza
en tramos prismáticos con la sección del punto medio; puntales, diagonales de techo y X de
muro son bielas; bajo el asiento de la carrilera la columna es la sección compuesta; análisis
lineal, sin P-Δ.

## Cómo se mueve

Los períodos dominantes, con la masa que cada modo lleva en su dirección:

| | T* (s) | masa participante |
|---|---:|---:|
| Y, transversal | {{ r('galpon-grua', 'T_star_Y', 5) }} | {{ r('galpon-grua', 'Uy', 1, factor=100) }} % |
| X, longitudinal | {{ r('galpon-grua', 'T_star_X', 5) }} | {{ r('galpon-grua', 'Ux', 1, factor=100) }} % |

En Y un solo modo lleva casi toda la masa: es el marco de momento moviéndose entero. En X la
masa se reparte en dos modos, porque el techo arriostrado y las X de muro trabajan a distinta
rigidez. La masa acumulada en quince modos llega a
{{ r('galpon-grua', 'macum_X', 1, factor=100) }} % en X y
{{ r('galpon-grua', 'macum_Y', 1, factor=100) }} % en Y.

<rukan-visor src="galpon-grua.escena.json" modo="1" vista="transversal" animar></rukan-visor>

## Los casos de carga

Siete casos estáticos: seis empujes y el peso propio. Los empujes son **unitarios**, en la
unidad que el memo 00 fijó —1 000 kN por marco—, y esa decisión es de fondo: ninguna magnitud
de nivel de diseño entra al modelo. La página que necesite un corte basal o una fuerza de
diafragma la escala en un paso a la vista, y las razones que los memos publican —una deriva
contra la promedio, el reparto entre marcos, la razón entre dos momentos— no dependen de la
escala en absoluto.

| Caso | Qué empuja | Resultante |
|---|---|---:|
| `H_alero` | los diez aleros a la vez: el *sway*, la deformada de un modo de traslación | 5 000 kN en Y |
| `H_alero_uno` | **un solo alero**, el del marco 3 | 1 000 kN en Y |
| `H_riel` | los diez nudos de columna al nivel del riel | 5 000 kN en Y |
| `H_riel_uno` | los **dos rieles de un marco**: el empuje de grúa entrando por uno solo | 1 000 kN en Y |
| `E_X` | sismo longitudinal, repartido como la masa sísmica | 5 000 kN en X |
| `E_Y_tope` | lo mismo en la dirección de los marcos, con la grúa contra su tope | 5 000 kN en Y |
| `D` | el peso propio de los perfiles, distribuido a lo largo de cada barra | {{ r('galpon-grua', 'peso_total', 2) }} kN |

`D` **no es la masa sísmica** de la serie, que se fijó por áreas y pesa más. Bajo ese peso la
cumbrera del marco 3 baja {{ r('galpon-grua', 'd_cumbrera_D', 2, factor=-1000) }} mm.

<rukan-visor src="galpon-grua.escena.json" caso="D" vista="transversal"></rukan-visor>

Los dos casos sísmicos reparten su resultante **con las mismas masas del modal**, así que caen
donde la serie puso su centro de masa. `E_X` cae en el centro de la nave; `E_Y_tope` mueve la
grúa a su tope de recorrido y la resultante se corre hacia ese extremo. Esa excentricidad no la
decidió este modelo: sale de repartir la grúa entre los dos marcos que la flanquean, que es lo
que el eslabón 05 ya hacía, y cuánto vale lo publica el eslabón 12. Bajo ella el galpón no solo
se traslada: gira en planta, y los cinco marcos se mueven distinto.

<rukan-visor src="galpon-grua.escena.json" caso="E_Y_tope" vista="planta"></rukan-visor>

## Los esfuerzos sobre el modelo

Elige un esfuerzo y el galpón entero se pinta con él: frío lo negativo, acento lo positivo, y
el rótulo dice cuánto vale el máximo, en qué barra cae y con qué rampa se está leyendo. Sobre
las barras que el filtro selecciona —aquí, el marco 3— se dibuja además el diagrama normal al
eje, con la ordenada sobre el eje local que le corresponde al componente y con su signo tal
cual, no sobre la cara traccionada.

<rukan-visor src="galpon-grua.escena.json" caso="D" esfuerzo="Mz" filtro="RAF3_*,COL3A_*,COL3B_*" vista="transversal"></rukan-visor>

Lo que se dibuja **no** es la recta entre las dos fuerzas de extremo. Entre los extremos de una
barra cargada hay una parábola que la salida del elemento no reporta, y el visor la superpone:
en el punto medio del primer tramo de rafter junto al alero el momento vale
{{ r('galpon-grua', 'Mz_raf3', 2) }} kN·m, y a media altura del primer tramo de columna el
axial vale {{ r('galpon-grua', 'N_col3', 2) }} kN — dos cifras que no están en ninguna de las
doce fuerzas de extremo de esas barras. Al pasar el cursor por una barra, el visor da el valor
en la estación exacta bajo el puntero.

Con la malla del memo, dieciséis tramos por corte, cada barra es corta y esa parábola es una
corrección pequeña: el diagrama se parece mucho a la poligonal por los nudos. La superposición
manda donde un miembro **es** un solo elemento, y eso se ve en la entrada de al lado: la
[viga carrilera](../carrilera/) del eslabón 08, con sus dos ruedas sobre un vano de un tramo.

## Límites

Al pasar el cursor por una barra aparecen sus fuerzas de extremo con el signo del diagrama, y
el diagrama a lo largo de la barra usa esa misma convención. Axial y momentos están verificados
contra SAP2000 en la escalera de Rukan. El signo del **corte** no está contrastado contra otro
programa, pero tampoco es una elección: con el momento anclado en sus dos extremos a una
convención verificada, `dMz/dx = +Vy` y `dMy/dx = −Vz` lo determinan, y eso está probado en la
nota 07 del laboratorio contra dos caminos independientes. La **torsión** es el único componente
sin diagrama del cual derivarse: sigue la regla análoga a la axial y **espera SAP2000**. No
firmes un `T` leído de aquí.

Los seis empujes son unitarios y **ninguno es una hipótesis de diseño**. El modelo no tiene
casos de nieve —el esquema de proyecto todavía no declara cargas distribuidas que no sean el
peso propio— ni cargas de rueda de grúa aplicadas donde de verdad entran, porque la viga
carrilera **no está en este modelo**: vive en [su propia entrada](../carrilera/), un vano
simple de un solo tramo con las dos ruedas encima. Los dos casos sísmicos son estáticos
equivalentes repartidos por masa; el análisis espectral con T\* y R\* por dirección es del esquema v2 del archivo de
proyecto y todavía no existe.

## Procedencia

{{ procedencia('galpon-grua') }}

Todo lo que esta página dibuja y escribe sale de tres archivos que viven junto a ella:
[`galpon-grua.proyecto.json`](galpon-grua.proyecto.json), el modelo con sus casos y sus
salidas; [`galpon-grua.resultados.json`](galpon-grua.resultados.json), lo que `python -m rukan run`
reportó; y [`galpon-grua.escena.json`](galpon-grua.escena.json), lo que el visor dibuja. Para
regenerarlos:

```bash
python sitio/docs/modelos/galpon-grua/_generar.py
python -m rukan run    sitio/docs/modelos/galpon-grua/galpon-grua.proyecto.json
python -m rukan escena sitio/docs/modelos/galpon-grua/galpon-grua.proyecto.json
```

El generador importa la geometría de `verification/case11_data.py`, y un test del repo
comprueba que lo que produce es, byte a byte, el proyecto versionado aquí.
