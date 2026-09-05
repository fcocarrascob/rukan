# 02 · Nieve balanceada y desbalanceada

La carga de nieve sobre la cubierta a dos aguas tiene dos distribuciones, y la segunda no es
una versión suavizada de la primera: pesa un 24 % menos en total y aun así lleva el sotavento
a un 68 % sobre la balanceada. Lo que decide esa acumulación es una altura que **solo existe
como gráfico**, y la fórmula que la propia figura de la norma imprime al pie da seis veces
menos que sus curvas, del lado inseguro. Este eslabón fija $p_g$, los cuatro factores, $p_f$,
$p_s$ y las dos distribuciones. Cargas en kN/m², longitudes en m, ángulos en grados.

## El caso

{{ figura('nch2369-galpon-grua/02', 'cargas-de-nieve', 'Sección transversal del galpón con los dos diagramas de carga de nieve superpuestos: la balanceada uniforme de 1,26 kN/m² sobre las dos aguas, y la desbalanceada con 0,378 kN/m² en barlovento y el escalón de acumulación de 2,11807 kN/m² sobre los 4,02993 m contiguos a la cumbrera en sotavento') }}

| Dato | Valor |
|---|---|
| Ubicación | Precordillera de la Región de Ñuble (S1) |
| Latitud geográfica sur | {{ v('nch2369-galpon-grua/02', 'lat', 2) }}° (S1) |
| Altitud | {{ v('nch2369-galpon-grua/02', 'alt', 0) }} m sobre el nivel del mar (S1) |
| Luz transversal | {{ v('nch2369-galpon-grua/02', 'L_luz', 2) }} m (del 01) |
| Separación de marcos | {{ v('nch2369-galpon-grua/02', 's_marco', 2) }} m (del 01) |
| Cumbrera sobre el alero | {{ v('nch2369-galpon-grua/02', 'h_cumbrera', 2) }} m (del 01, S2) |
| Categoría de ocupación | II, $I = {{ vt('nch2369-galpon-grua/02', 'I', 2) }}$ (del 01) |
| Categoría del terreno | C, techo parcialmente expuesto (S3) |
| Condición térmica | Estructura **no calefaccionada** (S4) |
| Cubierta | Panel de acero, superficie lisa, sin obstrucciones (S5) |
| Lo que se decide aquí | $p_g$, los cuatro factores, $p_f$, $p_s$ y las dos distribuciones |

Los supuestos, en una línea cada uno. **S1**, la ubicación es dato de proyecto: precordillera
de Ñuble, {{ v('nch2369-galpon-grua/02', 'lat', 2) }}° de latitud sur y
{{ v('nch2369-galpon-grua/02', 'alt', 0) }} m de altitud; la Tabla 1 entrega $p_g$ por franja
de latitud y de altitud, y este sitio cae en la celda `1 000 a 1 250` × `36° - 38°`. Se eligió
una ubicación donde la nieve compite con el sismo: en la costa de la misma latitud la Tabla 1
daría 0,25 kN/m², seis veces menos. **S2**, la pendiente sale de la geometría del 01 —
{{ v('nch2369-galpon-grua/02', 'h_cumbrera', 2) }} m de cumbrera sobre el alero en un
semiancho de {{ v('nch2369-galpon-grua/02', 'W', 2) }} m — y se vuelve a derivar de las dos
longitudes para no arrastrar el porcentaje redondeado que el 01 declaró. **S3**, el terreno es
categoría C y el techo está parcialmente expuesto; la alternativa «áreas montañosas azotadas
por vientos» daría {{ v('nch2369-galpon-grua/02', 'C_e_mont', 2) }} y bajaría la carga un
20 %, y no se toma porque el sitio es un valle precordillerano, no una cumbre expuesta.
**S4**, el galpón se supone no calefaccionado, que es la lectura literal de la fila
«Estructuras no calefaccionadas y/o mantenidas intencionalmente bajo el punto de
congelamiento» y la conservadora. **S5**, la cubierta es panel de acero, lisa y sin
obstrucciones; solo importa para elegir rama en la Figura 1, y en C3 se ve que con esta
pendiente **las dos ramas dan el mismo valor**. **S6**, la altura de acumulación $h_d$ se
obtiene digitalizando la Figura 4, no leyéndola a ojo ni con la fórmula que la figura imprime
al pie; el contraste de E5 usa la expresión de ASCE 7, que ninguna norma chilena da, y entra
como supuesto para acotar el error de digitalizar un escaneo, no como respaldo normativo.
**S7**, el viento de diseño para la acumulación se supone perpendicular a la cumbrera, que es
la dirección que §8.1 obliga a considerar y la que carga un solo faldón.

## A · El sitio y la carga básica

### A1 · La Tabla 1 cruza latitud con altitud, y esta celda vale 1,50

Las cargas básicas de nieve se determinan según la Tabla 1 para las distintas zonas del país.
El sitio cae en la fila de altitud `1 000 a 1 250` m y en la columna de latitud `36° - 38°`
sur.

$$p_g = {{ vt('nch2369-galpon-grua/02', 'p_g', 2) }}\ \text{kN}/\text{m}^2$$

→ **{{ v('nch2369-galpon-grua/02', 'p_g', 2) }} kN/m²**, o 150 kg/m² según la propia tabla.
Es más de lo que muchos galpones llevan de peso propio: el 01 declaró
{{ v('nch2369-galpon-grua/01', 'g_techo', 2) }} kg/m² de estructura de techo.

### A2 · Y la norma la califica de sobrecarga normal, no eventual

En zonas cordilleranas y del extremo sur, y en todos los lugares donde $p_g$ es mayor que
{{ v('nch2369-galpon-grua/02', 'p_g_normal', 2) }} kN/m², la sobrecarga de nieve se considera
**normal**.

$$\frac{p_g}{ {{ vt('nch2369-galpon-grua/02', 'p_g_normal', 2) }} } = \frac{ {{ vt('nch2369-galpon-grua/02', 'p_g', 2) }} }{ {{ vt('nch2369-galpon-grua/02', 'p_g_normal', 2) }} } = {{ vt('nch2369-galpon-grua/02', 'raz_normal', 5) }}$$

→ Seis veces el umbral. La consecuencia no es de esta norma sino de NCh3171 §9: una
sobrecarga normal entra en las combinaciones con su factor pleno, y eso lo cobra el 06.

## B · Los cuatro factores y la carga en techo plano

### B1 · El factor de exposición sale del terreno y de cuán expuesto está el techo

El factor de exposición se determina de la Tabla 4, cruzando categoría del terreno con
exposición del techo.

$$C_e = {{ vt('nch2369-galpon-grua/02', 'C_e', 2) }}$$

→ Terreno C, techo parcialmente expuesto. La casilla «totalmente expuesto» del mismo terreno
daría {{ v('nch2369-galpon-grua/02', 'C_e_exp', 2) }}.

### B2 · El factor térmico premia al techo que pierde calor y castiga al que no

El factor térmico se determina de la Tabla 2 según la condición térmica de la estructura.

$$C_t = {{ vt('nch2369-galpon-grua/02', 'C_t', 2) }}$$

→ Es el **mayor** de la tabla junto con el de invernaderos por el otro lado: una estructura
que no se calefacciona no derrite la nieve que se le posa encima. Con
{{ v('nch2369-galpon-grua/02', 'C_t_cal', 2) }} la carga bajaría un 17 %.

### B3 · El factor de importancia es el mismo I del eslabón 01

El factor de importancia se determina de la Tabla 3 según la Categoría de NCh3171. El 01 fijó
Categoría II.

$$I = {{ vt('nch2369-galpon-grua/02', 'I', 2) }}$$

→ El mismo valor que NCh2369 §4.3.2 asigna a la Categoría II. Las dos normas coinciden en el
número, y no es coincidencia: la Tabla 3 remite a NCh3171.

### B4 · La Ec. (1) multiplica los cuatro por 0,7

La carga de nieve en un techo con pendiente menor o igual que 5° se calcula con la Ec. (1).

$$p_f = 0{,}7 \cdot C_e \cdot C_t \cdot I \cdot p_g = 0{,}7 \cdot {{ vt('nch2369-galpon-grua/02', 'C_e', 2) }} \cdot {{ vt('nch2369-galpon-grua/02', 'C_t', 2) }} \cdot {{ vt('nch2369-galpon-grua/02', 'I', 2) }} \cdot {{ vt('nch2369-galpon-grua/02', 'p_g', 2) }} = {{ vt('nch2369-galpon-grua/02', 'p_f', 5) }}$$

→ **{{ v('nch2369-galpon-grua/02', 'p_f', 5) }} kN/m².** El 0,7 es el que convierte la carga
de suelo en carga de techo.

### B5 · El mínimo de §5.2 ni siquiera llega a aplicar

Los valores mínimos se aplican a techos triangulares con pendientes menores que el mayor valor
entre {{ v('nch2369-galpon-grua/02', 'theta_min', 2) }}° y $21{,}3/W + 0{,}5$, con $W$ en
metros. Acá $W$ es el semiancho.

$$\theta_{\lim} = \frac{21{,}3}{W} + 0{,}5 = \frac{21{,}3}{ {{ vt('nch2369-galpon-grua/02', 'W', 2) }} } + 0{,}5 = {{ vt('nch2369-galpon-grua/02', 'theta_lim', 5) }}$$

→ El umbral que manda es el **mayor** entre
{{ v('nch2369-galpon-grua/02', 'theta_min', 2) }} y
{{ v('nch2369-galpon-grua/02', 'theta_lim', 3) }}, o sea
**{{ v('nch2369-galpon-grua/02', 'theta_min', 2) }}°**. C1 muestra que la pendiente del
galpón lo supera casi cinco veces, así que la cláusula de mínimos no se aplica y el $p_f$ de
B4 queda como está.

## C · La pendiente, y el factor que no depende de qué rama se elija

### C1 · La pendiente sale de las dos longitudes, no del porcentaje redondeado

La cumbrera está {{ v('nch2369-galpon-grua/02', 'h_cumbrera', 2) }} m sobre el alero en un
semiancho de {{ v('nch2369-galpon-grua/02', 'W', 2) }} m.

$$\tan\theta = \frac{h_{\text{cumbrera}}}{W} = \frac{ {{ vt('nch2369-galpon-grua/02', 'h_cumbrera', 2) }} }{ {{ vt('nch2369-galpon-grua/02', 'W', 2) }} } = {{ vt('nch2369-galpon-grua/02', 'tan_theta', 5) }}$$

→ $\theta = {{ vt('nch2369-galpon-grua/02', 'theta_techo', 5) }}°$, que es el
{{ v('nch2369-galpon-grua/01', 'pend', 2) }} % que el 01 declaró. Supera el umbral de
{{ v('nch2369-galpon-grua/02', 'theta_min', 2) }}° de B5 por un factor
{{ v('nch2369-galpon-grua/02', 'raz_theta', 2) }}.

### C2 · Y S es la inversa de esa pendiente, no su ángulo

$S$ es la distancia horizontal del techo inclinado que se tiene al elevar en 1 unidad. Es el
símbolo que entra en la acumulación de §8.2, y **no** es el ángulo ni la pendiente.

$$S = \frac{W}{h_{\text{cumbrera}}} = \frac{ {{ vt('nch2369-galpon-grua/02', 'W', 2) }} }{ {{ vt('nch2369-galpon-grua/02', 'h_cumbrera', 2) }} } = {{ vt('nch2369-galpon-grua/02', 'S_pend', 5) }}$$

→ Pendiente 1:5. Confundir $S$ con $\tan\theta$ invertiría el efecto, y con unidades
correctas: la acumulación crece con $\sqrt{S}$ en su extensión y decrece con $\sqrt{S}$ en su
intensidad, así que el error se paga dos veces y en sentidos opuestos.

### C3 · Con esta pendiente las dos ramas de la Figura 1 dan el mismo número

La Figura 1 c) —techos fríos con $C_t = 1{,}2$— tiene dos ramas: la punteada, para superficies
lisas sin obstrucciones, arranca a bajar en 15°; la continua, para todas las demás superficies,
en 45°. La pendiente del galpón queda a la izquierda de **ambos** quiebres.

$$C_s = {{ vt('nch2369-galpon-grua/02', 'C_s', 2) }}$$

→ El supuesto S5 sobre si la cubierta es lisa y sin obstrucciones **no gobierna nada**: con
{{ v('nch2369-galpon-grua/02', 'theta_techo', 5) }}° las dos ramas valen
{{ v('nch2369-galpon-grua/02', 'C_s', 2) }}. Es el mejor caso posible para un supuesto, y
conviene notarlo porque en un techo de 30° la elección de rama valdría un factor 2.

### C4 · Y la Ec. (2) deja la carga inclinada igual a la plana

Para las cargas de nieve sobre una superficie inclinada se asume que actúan en la proyección
horizontal. La carga en techos inclinados se obtiene multiplicando la de techos planos por
$C_s$.

$$p_s = C_s \cdot p_f = {{ vt('nch2369-galpon-grua/02', 'C_s', 2) }} \cdot {{ vt('nch2369-galpon-grua/02', 'p_f', 5) }} = {{ vt('nch2369-galpon-grua/02', 'p_s', 5) }}$$

→ **{{ v('nch2369-galpon-grua/02', 'p_s', 5) }} kN/m² en proyección horizontal.** La pendiente
no descuenta nada: para eso habría que pasar de 15° con superficie lisa, o de 45° sin ella.

## D · La distribución desbalanceada

### D1 · La desbalanceada aplica, porque la pendiente cae entre los dos umbrales

Para techos triangulares con pendientes mayores que
{{ v('nch2369-galpon-grua/02', 'theta_max', 0) }}°, o menores que el mayor valor entre
{{ v('nch2369-galpon-grua/02', 'theta_min', 2) }}° y $21{,}3/W + 0{,}5$, las cargas sin
balancear **no requieren ser aplicadas**.

$$\frac{\theta}{\theta_{\lim}} = \frac{ {{ vt('nch2369-galpon-grua/02', 'theta_techo', 5) }} }{ {{ vt('nch2369-galpon-grua/02', 'theta_min', 5) }} } = {{ vt('nch2369-galpon-grua/02', 'raz_theta', 5) }}$$

→ La pendiente supera el umbral inferior {{ v('nch2369-galpon-grua/02', 'raz_theta', 2) }}
veces y está muy por debajo de {{ v('nch2369-galpon-grua/02', 'theta_max', 0) }}°, así que la
distribución desbalanceada **sí** se debe verificar.

### D2 · El peso específico de la nieve sale de su propia carga básica

La intensidad máxima de la sobrecarga por acumulación es $h_d \gamma$, con el peso específico
definido por la Ec. (3), topado en {{ v('nch2369-galpon-grua/02', 'gamma_tope', 1) }} kN/m³.

$$\gamma = 0{,}426 \cdot p_g + 2{,}2 = 0{,}426 \cdot {{ vt('nch2369-galpon-grua/02', 'p_g', 2) }} + 2{,}2 = {{ vt('nch2369-galpon-grua/02', 'gamma_nieve', 5) }}$$

→ **{{ v('nch2369-galpon-grua/02', 'gamma_nieve', 3) }} kN/m³**, holgadamente bajo el tope de
{{ v('nch2369-galpon-grua/02', 'gamma_tope', 1) }}. La nieve de diseño pesa menos de un tercio
que el agua: la acumulación es un problema de volumen, no de densidad.

### D3 · La acumulación ocupa una franja contigua a la cumbrera

La sobrecarga se extiende horizontalmente desde la cumbrera una longitud
$8\sqrt{S}\,h_d/3$, con $h_d$ del bloque E.

$$L_{\text{ac}} = \frac{8\sqrt{S}\,h_d}{3} = \frac{8 \cdot 2{,}236068 \cdot {{ vt('nch2369-galpon-grua/02', 'h_d', 5) }} }{3} = {{ vt('nch2369-galpon-grua/02', 'L_ac', 5) }}$$

→ **{{ v('nch2369-galpon-grua/02', 'L_ac', 2) }} m** de los
{{ v('nch2369-galpon-grua/02', 'W', 2) }} m del faldón de sotavento, o sea el
{{ v('nch2369-galpon-grua/02', 'frac_faldon', 1, 100) }} % de su ancho. Cabe entera en el
faldón, así que no hay que truncarla.

### D4 · Y su intensidad es la altura por el peso específico, repartida en la pendiente

La sobrecarga rectangular tiene magnitud $h_d \gamma / \sqrt{S}$.

$$p_d = \frac{h_d\,\gamma}{\sqrt{S}} = \frac{ {{ vt('nch2369-galpon-grua/02', 'h_d', 5) }} \cdot {{ vt('nch2369-galpon-grua/02', 'gamma_nieve', 5) }} }{2{,}236068} = {{ vt('nch2369-galpon-grua/02', 'p_d', 5) }}$$

→ **{{ v('nch2369-galpon-grua/02', 'p_d', 3) }} kN/m²** que se suman a la balanceada. El
$\sqrt{S}$ del denominador es lo que hace que un techo más tendido acumule más alto pero
reparta menos intensidad.

### D5 · El sotavento llega a 1,68 veces la carga balanceada

En la zona de sotavento la carga es $p_s$ más la sobrecarga de acumulación; en la de
barlovento, $0{,}3\,p_s$.

$$\frac{p_s + p_d}{p_s} = \frac{ {{ vt('nch2369-galpon-grua/02', 'p_s', 5) }} + {{ vt('nch2369-galpon-grua/02', 'p_d', 5) }} }{ {{ vt('nch2369-galpon-grua/02', 'p_s', 5) }} } = {{ vt('nch2369-galpon-grua/02', 'raz_pico', 5) }}$$

→ El peak vale **{{ v('nch2369-galpon-grua/02', 'p_pico', 5) }} kN/m²**, un **68 %** sobre la
balanceada. Y el barlovento cae a
{{ v('nch2369-galpon-grua/02', 'p_bar', 5) }} kN/m².

### D6 · Pero la desbalanceada pesa menos en total: lo que cambia es la simetría

Se comparan las dos distribuciones integrando sobre el ancho completo del marco, con el área
tributaria de una crujía de {{ v('nch2369-galpon-grua/02', 's_marco', 2) }} m.

$$\frac{F_{\text{desb}}}{F_{\text{bal}}} = \frac{ {{ vt('nch2369-galpon-grua/02', 'F_des', 5) }} }{ {{ vt('nch2369-galpon-grua/02', 'F_bal', 5) }} } = {{ vt('nch2369-galpon-grua/02', 'raz_des', 5) }}$$

→ La desbalanceada pesa **24 % menos**. No la gobierna la magnitud sino la **asimetría**: un
faldón con {{ v('nch2369-galpon-grua/02', 'p_bar', 3) }} y el otro con hasta
{{ v('nch2369-galpon-grua/02', 'p_pico', 5) }} meten momento en el marco que la balanceada no
mete. Cuál de las dos controla lo decide el 07, no este eslabón.

## E · La Figura 4, y la fórmula que no reproduce sus propias curvas

### E1 · La altura de acumulación solo existe como gráfico

Para acarreos de sotavento, la altura $h_d$ se determina directamente de la Figura 4, usando
$I_u$ igual a la distancia del alero a la cumbrera en la porción de sotavento, o sea $W$.

$$I_u = W = \frac{L}{2} = \frac{ {{ vt('nch2369-galpon-grua/02', 'L_luz', 2) }} }{2} = {{ vt('nch2369-galpon-grua/02', 'I_u', 5) }}$$

→ {{ v('nch2369-galpon-grua/02', 'I_u', 2) }} m, entre las curvas dibujadas de 7,5 m y 15 m.
La figura no trae una curva para este valor y la norma no da fórmula utilizable: hay que
leerla.

### E2 · La fórmula que la figura imprime al pie da seis veces menos

Al pie de la Figura 4 aparece una fórmula, anunciada para $I_u > 180$ m.

$$h_{d,\text{pie}} = 0{,}132 \cdot \sqrt[3]{I_u} \cdot (p_g + 10)^{1/4} - 0{,}46 = {{ vt('nch2369-galpon-grua/02', 'hd_pie', 5) }}$$

→ **{{ v('nch2369-galpon-grua/02', 'hd_pie', 5) }} m**, contra los
{{ v('nch2369-galpon-grua/02', 'h_d', 5) }} que sus propias curvas dan en el mismo punto. La
fórmula no es una extensión del gráfico: **lo contradice**, y del lado inseguro.

### E3 · Digitalizada, la curva da 0,67584 m

Se digitalizó la Figura 4 sobre la página rasterizada, calibrando los ejes con el marco del
gráfico, y se interpoló entre las curvas vecinas en $\sqrt[3]{I_u}$, que es la variable en que
la familia de curvas es lineal.

$$h_d = {{ vt('nch2369-galpon-grua/02', 'hd_c75', 5) }} + {{ vt('nch2369-galpon-grua/02', 't_int', 5) }} \cdot ( {{ vt('nch2369-galpon-grua/02', 'hd_c15', 5) }} - {{ vt('nch2369-galpon-grua/02', 'hd_c75', 5) }} ) = {{ vt('nch2369-galpon-grua/02', 'h_d', 5) }}$$

→ **{{ v('nch2369-galpon-grua/02', 'h_d', 5) }} m.** Las curvas leídas en
$p_g = {{ vt('nch2369-galpon-grua/02', 'p_g', 2) }}$ son
{{ v('nch2369-galpon-grua/02', 'hd_c75', 5) }} m para $I_u = 7{,}5$ m y
{{ v('nch2369-galpon-grua/02', 'hd_c15', 5) }} m para 15 m.

### E4 · Y el cociente entre las dos lecturas mide lo que costaría creerle al pie

$$\frac{h_d}{h_{d,\text{pie}}} = \frac{ {{ vt('nch2369-galpon-grua/02', 'h_d', 5) }} }{ {{ vt('nch2369-galpon-grua/02', 'hd_pie', 5) }} } = {{ vt('nch2369-galpon-grua/02', 'raz_pie', 5) }}$$

→ **{{ v('nch2369-galpon-grua/02', 'raz_pie', 2) }} veces.** Usar la fórmula del pie dejaría
la acumulación en 0,132 kN/m² en vez de {{ v('nch2369-galpon-grua/02', 'p_d', 3) }}, y el peak
de sotavento en 1,39 en vez de {{ v('nch2369-galpon-grua/02', 'p_pico', 2) }} kN/m². Es un
error que ningún arnés de aritmética detectaría, porque las cuentas cierran igual con
cualquiera de los dos valores.

### E5 · Las curvas digitalizadas son ASCE 7 convertido, y eso explica la discrepancia

Se contrastaron las seis curvas digitalizadas en
$p_g = {{ vt('nch2369-galpon-grua/02', 'p_g', 2) }}$ contra la expresión de ASCE 7 evaluada en
unidades imperiales y devuelta a metros. La mayor discrepancia entre ambas, descontada la
curva más baja, es la de $I_u = {{ vt('nch2369-galpon-grua/02', 'Iu_asce', 0) }}$ m.

$$\frac{ {{ vt('nch2369-galpon-grua/02', 'hd_asce_120', 5) }} }{ {{ vt('nch2369-galpon-grua/02', 'hd_c120', 5) }} } = {{ vt('nch2369-galpon-grua/02', 'raz_asce', 5) }}$$

→ **4,5 %**, dentro del error de digitalizar un escaneo. La conclusión es que la Figura 4 es
la de ASCE 7 con los ejes convertidos y la **fórmula del pie no se convirtió con ellos**: sus
coeficientes 0,132 y 0,46 son los 0,43 y 1,5 imperiales mal trasladados. Se usa el gráfico,
que es lo que la cláusula manda leer.

## Veredicto

La nieve balanceada vale **{{ v('nch2369-galpon-grua/02', 'p_s', 5) }} kN/m²** y la
desbalanceada de §8.2 pesa 24 % menos en total pero lleva el sotavento a
**{{ v('nch2369-galpon-grua/02', 'p_pico', 5) }} kN/m²** en los
{{ v('nch2369-galpon-grua/02', 'L_ac', 5) }} m contiguos a la cumbrera, un 68 % sobre la
balanceada, mientras deja el barlovento en
{{ v('nch2369-galpon-grua/02', 'p_bar', 5) }}. Cuál gobierna el marco lo decide la asimetría y
no la magnitud, y eso lo resuelve el 07. Hacia adelante, el 05 hereda
{{ v('nch2369-galpon-grua/02', 'p_g', 2) }} y
{{ v('nch2369-galpon-grua/02', 'p_f', 5) }} para decidir si la nieve participa del peso
sísmico, el 06 las combina, y el 11 usa la pendiente
{{ v('nch2369-galpon-grua/02', 'theta_techo', 5) }}° y su razón horizontal
{{ v('nch2369-galpon-grua/02', 'S_pend', 5) }} para el techo arriostrado.

Lo que este eslabón deja advertido para cualquier otro cálculo de nieve en Chile: **la fórmula
impresa al pie de la Figura 4 de NCh431 no reproduce las curvas de esa misma figura**. Acá da
{{ v('nch2369-galpon-grua/02', 'raz_pie', 2) }} veces menos, del lado inseguro. Sus
coeficientes son los de ASCE 7 sin convertir de unidades imperiales.

## Límites

- **No hay combinaciones acá.** Este eslabón entrega $S$ como carga nominal; combinarla con
  $D$, $L_r$, $W$ y $E$ es del 06. En particular no se resuelve la **obligación abierta de
  NCh3171 §9.1.1 y §9.2.1**: en zonas montañosas se deben estudiar combinaciones especiales de
  viento más nieve «que no sean menores que las originales», y la norma **exige la combinación
  y no la da**. Este sitio es precordillera, así que la obligación aplica.
- **La nieve y la masa sísmica no se tocan acá.** Si la nieve participa o no del peso sísmico
  de NCh2369 §4.5 lo decide el 05. Este eslabón no lo supone en ningún sentido.
- **$h_d$ es el único número leído de un gráfico**, con la incertidumbre de digitalizar un
  escaneo. El contraste contra ASCE 7 la acota en torno al 4,5 %, y la interpolación entre
  curvas vecinas agrega lo suyo. Un 5 % en $h_d$ mueve el peak de sotavento un 2 %.
- **La elección de $C_e$ y $C_t$ no se justifica con datos del sitio**, sino con la
  descripción de las tablas (S3, S4). Tomar «áreas montañosas azotadas por vientos» bajaría la
  carga 20 % y {{ v('nch2369-galpon-grua/02', 'C_t_cal', 2) }} otro 17 %; entre el caso
  adoptado y el más suave hay un factor 1,50. Un informe meteorológico del sitio cerraría esa
  horquilla.
- **La acumulación por arrastre desde estructuras vecinas no se evalúa** (§9.3), ni las
  proyecciones de techo (§10), ni la nieve caída por deslizamiento (§11): el galpón es una
  nave aislada de un solo nivel, sin techos más bajos adyacentes.
- **La carga de lluvia sobre la nieve de §12 no aplica** y no se calcula: esa cláusula rige
  para $p_g \le {{ vt('nch2369-galpon-grua/02', 'p_g_lluvia', 2) }}$ kN/m², y acá vale
  {{ v('nch2369-galpon-grua/02', 'p_g', 2) }}.
- **No hay modelo en este eslabón.** Las dos distribuciones se entregan como carga; ponerlas
  sobre el marco y ver qué momento meten es del 07.

## Ficha

{{ ficha('nch2369-galpon-grua/02') }}

## Referencias

| Clave | Norma y edición | Cláusula | Leída en | Cita textual |
|---|---|---|---|---|
| N431-1 | NCh431:2010 | §4 y Tabla 1, la carga básica por latitud y altitud — **tabla mirada en PNG**, no extraída | `Normas/nch-431-2010.pdf`, p. 7 | «Las cargas básicas de nieve, que se deben usar para determinar la carga de nieve de diseño para techos, se determina según lo indicado en Tabla 1 para las distintas zonas del país» |
| N431-2 | NCh431:2010 | §4, el umbral que separa sobrecarga normal de eventual | PDF ídem, p. 8 | «la carga básica de nieve, es mayor que 0,25 kN/m2 la sobrecarga de nieve se considera normal» |
| N431-3 | NCh431:2010 | §5.1, Ec. (1) y sus cuatro factores | PDF ídem, p. 8 | «La carga de nieve, en un techo con una pendiente menor o igual que 5 grados, debe ser calculada en kilonewton por metro cuadrado» |
| N431-4 | NCh431:2010 | §5.2, a qué techos se aplican los mínimos | PDF ídem, p. 10 | «con pendientes menores que el mayor valor entre 2,38 grados y 21,3/W + 0,5, con W en metros» |
| N431-5 | NCh431:2010 | Tablas 2, 3 y 4 — **miradas en PNG**, no extraídas | PDF ídem, p. 9 | «Estructuras no calefaccionadas y/o mantenidas intencionalmente bajo el punto de congelamiento» |
| N431-6 | NCh431:2010 | §6.1 y Ec. (2), la proyección horizontal | PDF ídem, p. 10 | «se debe asumir que éstas actúan en la proyección horizontal a esa superficie» |
| N431-7 | NCh431:2010 | §6.3 y Figura 1 c), las dos ramas del factor de pendiente — **mirada en PNG**; el texto en la primera página y la figura en la siguiente | PDF ídem, pp. 11-12 | «Para el resto de los techos fríos con superficies lisas sin obstrucciones» |
| N431-8 | NCh431:2010 | §8.1, las dos distribuciones se analizan por separado | PDF ídem, p. 15 | «Las cargas de nieve balanceadas y desbalanceadas deben ser analizadas por separado» |
| N431-9 | NCh431:2010 | §8.2, la carga sin balancear de un techo a dos aguas y su exención | PDF ídem, p. 16 | «la carga sin balancear debe ser considerada 0,3 x p en la zona de barlovento» |
| N431-10 | NCh431:2010 | §8.2, la extensión de la sobrecarga desde la cumbrera | PDF ídem, p. 16 | «y una extensión horizontal desde la cumbrera de» |
| N431-11 | NCh431:2010 | Figura 4, las curvas y la fórmula del pie — **digitalizada**, ver bloque E | PDF ídem, p. 16 | «Si Iu < 7,5 m, usar Iu = 7,5 m» |
| N431-12 | NCh431:2010 | §9.2 y Ec. (3), el peso específico de la nieve | PDF ídem, p. 20 | «pero no mayor que 4,7 kN/m3» |
| N431-13 | NCh431:2010 | §12, cuándo se agrega lluvia sobre la nieve | PDF ídem, p. 21 | «Para zonas donde se tenga que sea 0,96 kN/m2 o menor, pero no cero» |
| NCh-4 | NCh2369:2025 (3.ª ed.) | §4.3.2, el coeficiente de importancia de la Categoría II | `Normas/NCh 2369 - 3°Edición 2025.05.28.pdf`, p. 20 | «Categoría de ocupación II: I = 1,00» |
| N3171 | NCh3171:2017 | §9.1.1 y §9.2.1, la obligación abierta de viento más nieve en zona montañosa | `referencias/NCh3171-2017/cap09-combinaciones-de-carga.md` | — |
