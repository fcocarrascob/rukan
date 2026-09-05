# 00 · El modelo: el galpón entero corre por primera vez

Los períodos que once eslabones declararon salen de 965 nudos y no de un oscilador. Este
eslabón corre el modelo tridimensional del galpón, publica los períodos dominantes por
dirección, sus masas participantes y la rigidez lateral bajo dos empujes, y compara cada
número con lo que la serie había supuesto sin modelo. Longitudes en m, fuerzas en kN,
rigideces en kN/m, períodos en s.

## El caso

El galpón es el de la serie: cinco marcos de momento de alma variable separados
{{ v('nch2369-galpon-grua/00', 's_marco', 2) }} m, luz de
{{ v('nch2369-galpon-grua/00', 'L_luz', 2) }} m, alero a
{{ v('nch2369-galpon-grua/00', 'h_libre', 2) }} m, riel a
{{ v('nch2369-galpon-grua/00', 'h_riel', 2) }} m con el asiento de la carrilera a
{{ v('nch2369-galpon-grua/00', 'h_asiento', 5) }} m. Techo arriostrado en los cuatro vanos,
X de muro en los dos extremos. El modelo vive en su propia ficha,
[el galpón con puente grúa](../../../modelos/galpon-grua/), con el archivo de proyecto que lo
genera y la corrida que lo acompaña.

<rukan-visor src="../../../modelos/galpon-grua/galpon-grua.escena.json" vista="iso"></rukan-visor>

Lo que el modelo idealiza, y que hay que tener a la vista al leer sus números:

- **S1 — Las secciones y la geometría entran como dato de proyecto**, no como herencia. Las
  dimensionan los eslabones 07, 10 y 11, que en la cadena van después de este: el modelo es
  la segunda pasada del ciclo dimensionar → analizar, y va primero porque lo que produce, los
  períodos, es lo que el 04 necesita antes que nadie. Por eso este eslabón se escribió último
  y va al principio.
- **S2 — La masa es la del 05, por áreas tributarias**, y no el peso propio de las barras.
  Los seis términos, techo y cubierta sobre las siete líneas del techo, revestimiento sobre
  muros y hastiales, columnas al alero, carrileras y equipos por marco, más la grúa sin carga
  entre los dos marcos que la flanquean, en los 35 nudos de las líneas de techo. Suman
  {{ v('nch2369-galpon-grua/00', 'P_sismico', 5) }} kN.
- **S3 — El alma variable se discretiza en tramos prismáticos** con la sección del punto
  medio: 16 tramos entre cada par de niveles que la serie nombra, base, asiento, riel y
  alero, y 16 por panel de techo. Bajo el asiento va la sección compuesta del 10.
- **S4 — Puntales, diagonales de techo y X de muro son bielas**: momentos liberados en los
  dos extremos. Bases empotradas. Análisis lineal, sin P-Δ.
- **S5 — El empuje se reparte igual en los cinco marcos**, medio a cada alero:
  {{ v('nch2369-galpon-grua/00', 'H_marco', 0) }} kN por marco. Con la misma traslación en
  todos, las X de muro y los puntales no se deforman y lo que se mide es el *sway* del marco
  más el techo arriostrado. Es la rigidez **del galpón**, no la del marco aislado, y es la que
  un modo de traslación tiene.

## A · El modelo que corre es el galpón de la serie

### A1 · La masa sísmica, término a término

La masa del proyecto se suma sobre sus 35 nudos y se compara con el peso sísmico del 05.
Si un término se repartió dos veces o ninguna, esta suma lo dice y nada más lo diría. Los
puntos del visor son esos nudos.

$$m = \frac{P_{sismico}}{g} = \frac{ {{ vt('nch2369-galpon-grua/00', 'P_sismico', 5) }} }{9{,}81} = {{ vt('nch2369-galpon-grua/00', 'm_total', 5) }}\ \text{t}$$

→ **La masa del modelo es la de la serie, sin un término de más ni de menos.**

### A3 · La malla converge a segundo orden

Con 4, 8 y 16 tramos por corte el período dominante en Y da
{{ v('nch2369-galpon-grua/00', 'T_Y_nsub4', 7) }},
{{ v('nch2369-galpon-grua/00', 'T_Y_nsub8', 7) }} y
{{ v('nch2369-galpon-grua/00', 'T_star_Y', 7) }} s. La razón entre saltos sucesivos mide el
orden de convergencia:

$$\frac{T_8 - T_{16}}{T_4 - T_8} = {{ vt('nch2369-galpon-grua/00', 'razon_conv', 5) }}$$

Un cuarto: segundo orden en el tamaño del tramo. El error que queda con 16 tramos, por
extrapolación de Richardson, es un tercio del último salto:
{{ v('nch2369-galpon-grua/00', 'err_richardson', 7) }} s, una unidad del último decimal que
este eslabón publica; el valor convergido sería
{{ v('nch2369-galpon-grua/00', 'T_Y_conv', 5) }} s. Se publica lo que el modelo emite con la
malla declarada, y los límites cargan el resto.

## B · Dos empujes, y la rigidez del galpón

### B1 · El sway de los aleros

Bajo `H_alero`, quinientos kilonewton en cada uno de los diez aleros, el alero A del marco 3
se desplaza {{ v('nch2369-galpon-grua/00', 'd_alero_H', 7) }} m. Es la deformada que un modo
de traslación tiene: los cinco marcos se mueven juntos.

<rukan-visor src="../../../modelos/galpon-grua/galpon-grua.escena.json" caso="H_alero" vista="transversal"></rukan-visor>

Con {{ v('nch2369-galpon-grua/00', 'H_marco', 0) }} kN por marco:

$$k_{Y,3D} = \frac{H_{marco}}{\delta_{alero}} = \frac{1\,000}{ {{ vt('nch2369-galpon-grua/00', 'd_alero_H', 7) }} } = {{ vt('nch2369-galpon-grua/00', 'k_Y_3D', 5) }}\ \text{kN/m}$$

Contra la `k_Y` = {{ v('nch2369-galpon-grua/00', 'k_Y_07', 5) }} kN/m que el eslabón 07
declaró sin modelo:

$$\frac{k_{Y,3D}}{k_{Y,07}} = {{ vt('nch2369-galpon-grua/00', 'raz_kY_07', 5) }}$$

y contra esa misma rigidez corregida por el escalón que el 10 midió,
{{ v('nch2369-galpon-grua/00', 'k_esc_10', 5) }}:

$$\frac{k_{Y,3D}}{k_{Y,07} \cdot k_{esc}} = {{ vt('nch2369-galpon-grua/00', 'raz_kY_esc', 5) }}$$

Las dos diferencias tienen nombre. La del escalón, el 10 la encontró y decidió no propagarla.
La otra, el 19 % que queda, es la que el caso 11 de la escalera de Rukan explicó: la `k_Y`
del 07 sale de un empuje en **un solo alero**, que incluye la deformación antisimétrica del
marco abriéndose, y un modo de traslación no la tiene. Mira la diferencia:

<rukan-visor src="../../../modelos/galpon-grua/galpon-grua.escena.json" caso="H_alero_uno" vista="transversal"></rukan-visor>

→ **La rigidez transversal del galpón es {{ v('nch2369-galpon-grua/00', 'k_Y_3D', 5) }} kN/m,
y es la que un modo de traslación ve.**

### B2 · El sway del riel

Bajo `H_riel`, el mismo empuje en los diez nudos de columna al nivel del riel, el riel A del
marco 3 se desplaza {{ v('nch2369-galpon-grua/00', 'd_riel_H', 7) }} m:

<rukan-visor src="../../../modelos/galpon-grua/galpon-grua.escena.json" caso="H_riel" vista="transversal"></rukan-visor>

$$k_{riel,3D} = \frac{1\,000}{ {{ vt('nch2369-galpon-grua/00', 'd_riel_H', 7) }} } = {{ vt('nch2369-galpon-grua/00', 'k_riel_3D', 5) }}\ \text{kN/m}$$

$$\frac{k_{riel,3D}}{k_{riel,07}} = {{ vt('nch2369-galpon-grua/00', 'raz_kriel_07', 5) }}$$

El 07 sí midió el riel con sway, lo delató que su `k_riel` calzara a partes en cien mil con
el marco sin escalón, así que este factor es el escalón del 10 medido al nivel del riel,
donde la sección compuesta está entera bajo el punto de carga.

→ **{{ v('nch2369-galpon-grua/00', 'k_riel_3D', 5) }} kN/m al nivel del riel,
{{ v('nch2369-galpon-grua/00', 'raz_kriel_07', 5) }} veces el valor sin escalón.**

## C · Los períodos y las masas participantes

### C1 · La dirección de marcos

El modo con mayor masa de traslación en Y es el **primero**, con
{{ v('nch2369-galpon-grua/00', 'Uy_star', 5) }} de la masa, y su período es
**{{ v('nch2369-galpon-grua/00', 'T_star_Y', 5) }} s**. Pulsa **Animar**: es el sway del marco
con el rafter.

<rukan-visor src="../../../modelos/galpon-grua/galpon-grua.escena.json" modo="1" vista="transversal" animar></rukan-visor>

Contra los {{ v('nch2369-galpon-grua/00', 'T_Y_10', 5) }} s que el 10 obtuvo con el oscilador
y la rigidez escalonada:

$$\frac{T^{*}_{Y}}{T_{Y,10}} = {{ vt('nch2369-galpon-grua/00', 'raz_TY_10', 5) }}$$

→ **El 10 tenía razón en la rama y erraba 3,3 % en el número**: el período queda bajo el codo
de 0,28 s de la Ec. (1b), como el 10 encontró, y el 04 recalculará R*_Y con él.

### C2 · La dirección arriostrada

En X la masa se reparte en dos modos: el **cuarto** lleva
{{ v('nch2369-galpon-grua/00', 'Ux_star', 5) }} y es el dominante, con período
**{{ v('nch2369-galpon-grua/00', 'T_star_X', 5) }} s**; el resto va a un modo de techo. Son
los dos vanos arriostrados trabajando.

<rukan-visor src="../../../modelos/galpon-grua/galpon-grua.escena.json" modo="4" vista="longitudinal" animar></rukan-visor>

Contra los {{ v('nch2369-galpon-grua/00', 'T_X_04', 2) }} s que el 04 declaró:

$$\frac{T^{*}_{X}}{T_{X,04}} = {{ vt('nch2369-galpon-grua/00', 'raz_TX_04', 5) }}$$

→ **El 04 declaró bien a 3,0 %, y ahora tiene con qué reemplazar su supuesto por un modelo.**

### C3 · El 90 % de §5.6.2, y los modos mirados

Con 15 modos la masa acumulada es {{ v('nch2369-galpon-grua/00', 'macum_X', 5) }} en X,
{{ v('nch2369-galpon-grua/00', 'macum_Y', 5) }} en Y y
{{ v('nch2369-galpon-grua/00', 'macum_Z', 5) }} en Z. §5.6.2 exige al menos el 90 % en cada
dirección de análisis horizontal:

$$\frac{ {{ vt('nch2369-galpon-grua/00', 'macum_X', 5) }} }{0{,}90} = {{ vt('nch2369-galpon-grua/00', 'raz_macum_X', 5) }} \qquad \frac{ {{ vt('nch2369-galpon-grua/00', 'macum_Y', 5) }} }{0{,}90} = {{ vt('nch2369-galpon-grua/00', 'raz_macum_Y', 5) }}$$

La vertical no llega, y no tiene que llegar aquí: el 06 la trata con el coeficiente estático
de §5.7.1, y un modelo con la masa en las líneas de techo no representa la flexibilidad
vertical de la cubierta. Y C5.6.2 pide algo que ningún número da: que los modos sean
coherentes con la estructura. Por eso las dos deformadas de arriba, y por eso la tabla:

{{ tabla_modos('galpon-grua', 15) }}

→ **{{ v('nch2369-galpon-grua/00', 'raz_macum_X', 5) }} y
{{ v('nch2369-galpon-grua/00', 'raz_macum_Y', 5) }} sobre el mínimo, y las dos deformadas son
las que la estructura tiene que tener.**

## D · Lo que un oscilador de un grado de libertad habría dicho

### D1 · En Y, con la rigidez del galpón

Es el método del 07 con la rigidez de B1, y es la banda de sensatez de C1: misma carga, el
sway, y otra formulación.

$$m_{marco} = \frac{ {{ vt('nch2369-galpon-grua/00', 'P_sismico', 5) }} }{5 \cdot 9{,}81} = {{ vt('nch2369-galpon-grua/00', 'm_marco', 5) }}\ \text{t}$$

$$T_{1} = 2\pi\sqrt{\frac{m_{marco}}{k_{Y,3D}}} = {{ vt('nch2369-galpon-grua/00', 'T1_Y', 5) }}\ \text{s} \qquad \frac{T^{*}_{Y}}{T_{1}} = {{ vt('nch2369-galpon-grua/00', 'raz_T1_Y', 5) }}$$

→ **El oscilador queda 5,6 % abajo del modelo**: concentrar la masa en el alero sobrestima la
rigidez efectiva, porque parte de la masa cuelga del rafter, que en el modo 1 flecta. Es el
matiz que importa: los dos errores del 07, una rigidez baja y un oscilador rígido, se
cancelaban en parte, y por eso su período quedó a 1 % del modelo sin escalón. Corregir uno
solo empeora; la corrección es que el período salga del modelo. Y la regla que este eslabón
deja para toda la serie: el oscilador con la `k_Y` del 07, la de un solo alero, habría dado
{{ v('nch2369-galpon-grua/00', 'T1_Y_07', 5) }} s y parecido razonable. Era el caso de carga
equivocado.

### D2 · En X, con los cuatro paneles del 12

La rigidez del panel ilustrativo del 12, tubo 125 × 125 × 5 en tensión-compresión sobre el
vano de {{ v('nch2369-galpon-grua/00', 's_marco', 2) }} × {{ v('nch2369-galpon-grua/00', 'h_libre', 2) }} m,
cuatro veces, dos vanos por dos muros, contra la masa entera:

$$k_{pan} = \frac{2 \cdot E \cdot A \cdot \cos^{2}\theta}{L_{d}} = \frac{2 \cdot 200\,000 \cdot 2\,400 \cdot {{ vt('nch2369-galpon-grua/00', 'cos2_panel', 5) }} }{ {{ vt('nch2369-galpon-grua/00', 'L_diag_panel', 2) }} } = {{ vt('nch2369-galpon-grua/00', 'k_pan', 2) }}\ \text{kN/m}$$

$$T_{1} = 2\pi\sqrt{\frac{m}{4\,k_{pan}}} = {{ vt('nch2369-galpon-grua/00', 'T1_X', 5) }}\ \text{s} \qquad \frac{T^{*}_{X}}{T_{1}} = {{ vt('nch2369-galpon-grua/00', 'raz_T1_X', 5) }}$$

→ **1,1 % de diferencia**: en la dirección arriostrada el oscilador sí describe al galpón,
porque la rigidez está en cuatro paneles idénticos y la masa se mueve entera con el techo.

## Veredicto

**El modelo confirma la cadena por los dos lados y no la contradice.** El período transversal
queda a 3,3 % del que el 10 encontró con la columna escalonada, y en la misma rama de la
Ec. (1b); el longitudinal a 3,0 % del que el 04 declaró; y las masas acumuladas cumplen el
90 % de §5.6.2 que el 04 decía no poder verificar.

Lo que cambia es **de dónde salen los números**. La rigidez transversal del galpón bajo un
empuje uniforme en los aleros vale {{ v('nch2369-galpon-grua/00', 'k_Y_3D', 5) }} kN/m,
{{ v('nch2369-galpon-grua/00', 'raz_kY_07', 5) }} veces la que el 07 declaró:
{{ v('nch2369-galpon-grua/00', 'k_esc_10', 5) }} de esas veces son el escalón que el 10 midió
y no propagó, y el {{ v('nch2369-galpon-grua/00', 'raz_kY_esc', 5) }} restante es que la
`k_Y` del 07 salía de un empuje en un solo alero, que no es una rigidez lateral.

Este eslabón **abre la cascada y no la cierra**. El 04 recalculará R*_X y R*_Y con estos
períodos, cambiará de rama en Y, y de ahí bajan R_1, el amplificador de capacidad, la
componente vertical del 06, los M_pe del 07 y el anclaje del 13. Hasta que eso se escriba,
ninguna salida de este eslabón la hereda nadie.

## Límites

- **Es la segunda pasada del ciclo dimensionar → analizar, y va primero aunque se escribió
  último** (S1). Consume las secciones que el 07, el 10 y el 11 dimensionan con los períodos
  que el 04 declaró; lo que produce son los períodos con que el 04 debería haber empezado. La
  circularidad se corta declarando las secciones como dato de proyecto, no como herencia: si
  la cascada las cambia, este eslabón se corre de nuevo y el hash del proyecto delata
  cualquier versión vieja.
- **El error de discretización es una unidad del último decimal publicado** (A3). Con 16
  tramos el período transversal se publica en {{ v('nch2369-galpon-grua/00', 'T_star_Y', 5) }} s
  y el convergido sería {{ v('nch2369-galpon-grua/00', 'T_Y_conv', 5) }}; en X la malla no
  pesa, porque la rigidez está en bielas.
- **La rigidez de B1 es la del galpón, no la del marco aislado** (S5). El techo arriostrado
  endurece el sway unas partes en diez mil, porque las diagonales unen líneas distintas del
  rafter; la capa E del caso 11 lo midió.
- **La masa es por áreas y va en las líneas de techo** (S2). No hay peso propio de barras ni
  masa al nivel del riel; la masa acumulada vertical de
  {{ v('nch2369-galpon-grua/00', 'macum_Z', 5) }} es consecuencia de eso y no describe la
  cubierta.
- **Sin P-Δ ni no linealidad** (S4). Los períodos son los elásticos.
- **Corte y torsión de barra no se publican.** Rukan verificó contra SAP2000 la axial y los
  momentos; corte y torsión siguen la regla análoga y no se han verificado.

## Ficha

{{ ficha('nch2369-galpon-grua/00') }}

## Referencias

| Clave | Norma y edición | Cláusula | Leída en | Cita textual |
|---|---|---|---|---|
| NCh-p1 | NCh2369:2025 (3.ª ed.) | §5.3.2, el modelo tridimensional que este eslabón corre y la excepción con que los once anteriores usaron modelos planos | `Normas/NCh 2369 - 3°Edición 2025.05.28.pdf`, p. 30 | «se debe usar un modelo tridimensional, excepto en los casos en que el comportamiento se puede estimar adecuadamente usando modelos planos» |
| NCh-p2 | NCh2369:2025 (3.ª ed.) | §5.4, la definición de R* por el modo con mayor masa de traslación, que C1 y C2 usan para elegir el modo | PDF ídem, p. 34 | «respuesta estructural, calculado para el período del modo con mayor masa de traslación equivalente, en la dirección de análisis» |
| NCh-p3 | NCh2369:2025 (3.ª ed.) | §3.1.29, la definición del período que C1 y C2 publican | PDF ídem, p. 14 | «período del modo normal de vibración con mayor masa de traslación equivalente en la dirección de análisis» |
| NCh-p4 | NCh2369:2025 (3.ª ed.) | §5.6.2, el 90 % de masa que C3 verifica | PDF ídem, p. 39 | «suficientes modos de vibrar para que la suma de las masas modales (equivalentes), en cada dirección de análisis, sea mayor o igual al 90% de la masa total» |
| NCh-p5 | NCh2369:2025 (3.ª ed.) | C5.6.2, la verificación de coherencia de los modos para la que existen las dos deformadas de C3 | PDF ídem, p. 40 | «siempre se debe verificar que los modos de vibrar de la estructura sean coherentes con la estructura que se desea diseñar» |
