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

Cuatro casos estáticos. `H_alero` empuja los diez aleros con 500 kN cada uno, 1 000 kN por
marco: es el *sway* del marco, la deformada que un modo de traslación tiene. `H_alero_uno`
pone los 1 000 kN en **un solo alero**. `H_riel` empuja los diez nudos de columna al nivel
del riel. `D` es el peso propio de los perfiles, distribuido a lo largo de cada barra: suma
{{ r('galpon-grua', 'peso_total', 2) }} kN, y no es la masa sísmica de la serie, que se fijó
por áreas y pesa más. Bajo ese peso la cumbrera del marco 3 baja
{{ r('galpon-grua', 'd_cumbrera_D', 2, factor=-1000) }} mm.

<rukan-visor src="galpon-grua.escena.json" caso="D" vista="transversal"></rukan-visor>

Al pasar el cursor por una barra en un caso aparecen sus fuerzas de extremo con el signo del
diagrama: axial y momentos están verificados contra SAP2000 en la escalera de Rukan; corte y
torsión siguen la misma convención y todavía no.

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
