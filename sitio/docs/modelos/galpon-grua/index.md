# El galpón con puente grúa

Un galpón industrial de acero a dos aguas, el de la serie de memos
[`nch2369-galpon-grua`](https://github.com/fcocarrascob/Guias_Interactivas/tree/master/memos/estructural)
del repositorio de guías. Doce eslabones lo diseñan, un memo lo corre
([el 00, «el modelo»](https://github.com/fcocarrascob/Guias_Interactivas/blob/master/memos/estructural/nch2369-galpon-grua-00-el-modelo.md)),
y el caso 11 de la escalera de verificación de Rukan lo contrasta contra rigidez directa en
numpy puro. Esta entrada es el mismo modelo, puesto en pantalla.

## Qué es este galpón

Cinco marcos de momento de alma variable, con bases empotradas, separados a 7,50 m: una nave
de 25,00 m de luz y 30,00 m de largo, alero a 10,50 m y cumbrera a 13,00 m. El techo lleva
arriostramiento continuo, puntales y diagonales en X en los cuatro vanos, y dos de los cuatro
vanos, los extremos, llevan las X de muro que resisten en la dirección longitudinal. El puente
grúa corre sobre un riel a 7,50 m, apoyado en una viga carrilera que a su vez se asienta en
un fuste adosado a la columna. Los datos vienen del caso de la serie; cada constante del
generador lleva el eslabón que la publica.

Lo que el modelo idealiza, y que el memo 00 declara en sus supuestos:

- **La masa es la de la serie, por áreas tributarias**, repartida en los nudos de las siete
  líneas de techo. No es el peso propio de las barras: el peso propio se corre aparte, más
  abajo, para mirar la deformada de gravedad.
- **El alma variable se discretiza en tramos prismáticos** con la sección del punto medio.
  Aquí son cuatro tramos por nivel, la malla del caso 11; el memo usa dieciséis, y la
  diferencia entre las dos está medida y es de partes en diez mil.
- **Puntales, diagonales de techo y X de muro son bielas**: momentos liberados en los dos
  extremos. Bajo el asiento de la carrilera la columna es la sección compuesta, el escalón que
  el eslabón 10 dimensiona.
- Análisis lineal, sin P-Δ.

## El modelo en 3D

Orbita con el ratón, o elige una vista fija. Al pasar el cursor por una barra aparece su
nombre y su sección; por un nudo, su nombre y sus coordenadas.

<rukan-visor src="galpon-grua.escena.json" vista="iso"></rukan-visor>

Los nombres siguen la convención del caso 11: `K3A_2` es el segundo tramo de la columna del
marco 3 en el muro A, `R3_0` el alero A del marco 3, `R3_3` su cumbrera, `DTA2_1` una
diagonal de techo del vano 2. Los cubos son los apoyos empotrados y los puntos, los nudos
que llevan masa.

## Cómo se mueve

El modo dominante en la dirección transversal, la de los marcos de momento, y el dominante en
la longitudinal, la arriostrada. La forma está normalizada: el desplazamiento máximo se dibuja
como un 5 % de la diagonal del modelo, y el deslizador lo escala. Pulsa **Animar**.

<rukan-visor src="galpon-grua.escena.json" modo="1" vista="transversal" animar></rukan-visor>

<rukan-visor src="galpon-grua.escena.json" modo="4" vista="longitudinal" animar></rukan-visor>

Los períodos dominantes, con la masa que cada modo lleva en su dirección:

| | T* (s) | masa participante |
|---|---:|---:|
| Y, transversal | {{ r('galpon-grua', 'T_star_Y', 5) }} | {{ r('galpon-grua', 'Uy', 1, factor=100) }} % |
| X, longitudinal | {{ r('galpon-grua', 'T_star_X', 5) }} | {{ r('galpon-grua', 'Ux', 1, factor=100) }} % |

En Y un solo modo lleva casi toda la masa: es el marco de momento moviéndose entero. En X
la masa se reparte en dos modos, porque el techo arriostrado y las X de muro trabajan a
distinta rigidez. Los quince modos que se corrieron:

{{ tabla_modos('galpon-grua', 15) }}

La masa acumulada llega a {{ r('galpon-grua', 'macum_X', 1, factor=100) }} % en X y
{{ r('galpon-grua', 'macum_Y', 1, factor=100) }} % en Y. En Z queda en
{{ r('galpon-grua', 'macum_Z', 1, factor=100) }} % y no tiene por qué llegar más arriba: la
masa va en las líneas de techo y el modelo no representa la flexibilidad vertical de la
cubierta. El sismo vertical se trata aparte, con el espectro de §5.7.1.

Lo que NCh2369 lee de aquí es el período dominante de cada dirección, que entra en el factor
de reducción R* de la Ec. (1b) y decide en qué rama del espectro cae cada dirección. Ese
cálculo lo hace el
[eslabón 04](https://github.com/fcocarrascob/Guias_Interactivas/blob/master/memos/estructural/nch2369-galpon-grua-04-espectro-y-r-por-direccion.md)
de la serie y no se rehace aquí.

## Los empujes, y el hallazgo del caso 11

Tres casos estáticos de 1 kN por marco, para medir rigideces. `H_alero` empuja los diez
aleros con la misma fuerza, medio kilonewton a cada lado: es el *sway* del marco, la
deformada que un modo de traslación tiene. `H_alero_uno` empuja **un solo alero** con el
kilonewton entero. `H_riel` empuja los diez nudos de columna al nivel del riel.

<rukan-visor src="galpon-grua.escena.json" caso="H_alero" vista="transversal"></rukan-visor>

<rukan-visor src="galpon-grua.escena.json" caso="H_alero_uno" vista="transversal"></rukan-visor>

Las dos deformadas no se parecen, y ahí está lo que el caso 11 encontró. El eslabón 07 de la
serie declaraba una rigidez transversal `k_Y` sin decir de qué caso de carga salía, y el caso
11 la reprodujo a partes en cien mil **solo con el empuje en un alero**: el desplazamiento del
alero A del marco 3 bajo `H_alero_uno` es
{{ r('galpon-grua', 'd_alero_uno', 4, factor=1000) }} mm, y bajo `H_alero`, el sway, es
{{ r('galpon-grua', 'd_alero', 4, factor=1000) }} mm. Con un alero cargado la otra columna
apenas se mueve y el rafter trabaja de puntal; con los dos, el marco entero se traslada.

La rigidez es un paso, no una salida del análisis, y se escribe como en el memo:
con H = 1 kN por marco,

- `k_Y = H / d_alero` = **{{ cociente('galpon-grua', 1.0, 'd_alero', 2) }} kN/m**, la del
  galpón bajo sway. Es del galpón y no del marco aislado: las diagonales de techo unen líneas
  distintas del rafter en marcos vecinos y toman algo de carga, unas partes en diez mil.
- `k_riel = H / d_riel` = **{{ cociente('galpon-grua', 1.0, 'd_riel', 2) }} kN/m**, al nivel
  del riel, con `d_riel` = {{ r('galpon-grua', 'd_riel', 4, factor=1000) }} mm.

<rukan-visor src="galpon-grua.escena.json" caso="H_riel" vista="transversal"></rukan-visor>

## La gravedad

El peso propio de los perfiles, distribuido a lo largo de cada barra, suma
{{ r('galpon-grua', 'peso_total', 2) }} kN. No es la masa sísmica del memo, que se fijó por
áreas y pesa más; es lo que pesan las barras de este modelo. Bajo ese peso la cumbrera del
marco 3 baja {{ r('galpon-grua', 'd_cumbrera_D', 2, factor=-1000) }} mm, y la deformada
muestra el rafter flectando entre alero y cumbrera y las columnas abriéndose.

<rukan-visor src="galpon-grua.escena.json" caso="D" vista="transversal"></rukan-visor>

Al pasar el cursor por una barra en este caso aparecen sus fuerzas de extremo con el signo
del diagrama: axial y momentos están verificados contra SAP2000 en la escalera de Rukan;
corte y torsión siguen la misma convención y todavía no.

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
