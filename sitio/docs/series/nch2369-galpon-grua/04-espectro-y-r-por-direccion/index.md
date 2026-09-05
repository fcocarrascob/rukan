# 04 · Espectro y R* por dirección

La Ec. (1b) le devuelve a 4 el R de 5 que el 01 ganó, y **solo en la dirección arriostrada**.
La frontera de la rampa cae en 0,28 s y las dos direcciones del galpón caen a lados distintos
de ella, así que este eslabón no tiene una respuesta sino dos. Se fijan los parámetros de
sitio, se evalúa el espectro de referencia de §5.4.2 y se calcula el factor de reducción de la
Ec. (1b) en las dos direcciones de análisis. Ordenadas en g, períodos en s.

## El caso

{{ figura('nch2369-galpon-grua/04', 'espectros', 'Espectro de referencia de zona 2 y suelo C con su pico en 0,34533 s, el mismo espectro reducido punto a punto por la Ec. 1b, la frontera de la rampa en 0,28 s y los dos períodos de análisis marcados en 0,20 y 0,40 s') }}

| Dato | Valor |
|---|---|
| Estructura | Galpón de acero de una nave, un piso, cubierta a dos aguas (del 01) |
| Dirección **X** | **longitudinal**, marcos arriostrados en 2 de los 4 vanos (del 01 · S2) |
| Dirección **Y** | **transversal**, marco de momento a dos aguas de 25,00 m (del 01 · S2) |
| Zona sísmica | {{ v('nch2369-galpon-grua/04', 'zona', 0) }} (S1) |
| Tipo de suelo | C (S1) |
| Fila de la Tabla 7 | 5.5, $R = {{ vt('nch2369-galpon-grua/04', 'R_T7', 0) }}$, $\xi = {{ vt('nch2369-galpon-grua/04', 'xi', 2) }}$ (del 01) |
| Aceleración efectiva | $A_0 = {{ vt('nch2369-galpon-grua/04', 'A_0', 2) }}$ g |
| Parámetros del suelo C | $S = {{ vt('nch2369-galpon-grua/04', 'S_suelo', 2) }}$; $r = {{ vt('nch2369-galpon-grua/04', 'r_s', 2) }}$; $T_0 = {{ vt('nch2369-galpon-grua/04', 'T_0', 2) }}$ s; $p = {{ vt('nch2369-galpon-grua/04', 'p_suelo', 2) }}$; $q = {{ vt('nch2369-galpon-grua/04', 'q_s', 2) }}$; $T_1 = {{ vt('nch2369-galpon-grua/04', 'T_1', 2) }}$ s |
| Geometría del sistema longitudinal | 4 paneles de {{ v('nch2369-galpon-grua/04', 's_marco', 2) }} m de base y {{ v('nch2369-galpon-grua/04', 'h_libre', 2) }} m de alto (del 01) |
| Base de columnas | empotrada (S3) |
| Períodos de análisis | $T^{*}_X = {{ vt('nch2369-galpon-grua/04', 'T_star_X', 2) }}$ s; $T^{*}_Y = {{ vt('nch2369-galpon-grua/04', 'T_star_Y', 2) }}$ s (S2) |
| Lo que se decide aquí | el espectro de referencia, la rama de la Ec. (1b) de cada dirección y las dos ordenadas de diseño |

Los supuestos, en una línea cada uno. **S1**, la zona sísmica
{{ v('nch2369-galpon-grua/04', 'zona', 0) }} y el suelo C son dato de proyecto, declarados en
el 01 y no reclasificados aquí: la Tabla 2 asigna zona por comuna y la Figura 2 la corrige
cuando el sitio es identificable, y el suelo sale del procedimiento de dos pasos de las notas
al pie de la Tabla 4 —clasificar por $V_{s30}$, ratificar contra $T_g$—; sin comuna ni sondaje
no se recorre ninguno de los dos caminos, y son los dos números de los que **todo** lo que
sigue depende. **S2**, los períodos por dirección son valores declarados, no la salida de un
modelo corrido; **ninguna afirmación de este eslabón depende de que sean exactos**, sí de en
qué rama de la Ec. (1b) caen, y C7 muestra por cuánto margen esa rama resiste. **S3**, base de
columnas empotrada en el modelo que respalda a S2, que es la práctica corriente en un galpón
con puente grúa y es coherente con los anclajes dúctiles que el 01 declaró; con base rotulada
el marco transversal sería del orden de dos veces más flexible y $T^{*}_Y$ se iría sobre
0,79 s, lo que **no** cambiaría su rama. **S4**, no hay falla cortical activa dentro de las
distancias de la Tabla 5, que además solo rige para Categorías III y IV y el galpón es
Categoría II. **S5**, las uniones son soldadas, que es lo que fija
$\xi = {{ vt('nch2369-galpon-grua/04', 'xi', 2) }}$ en la fila 5.5 de la Tabla 7; si el
proyecto se apernara, la misma fila daría 0,03 y toda la demanda bajaría un 15 %.

## A · El sitio

### A1 · La zona 2 pone la aceleración un cuarto bajo la de las otras dos series

La Tabla 3 tabula la aceleración efectiva máxima $A_0$ por zona sísmica y la aceleración
máxima de referencia como $A_r = 1{,}4\,A_0$.

$$A_r = 1{,}4\,A_0 = 1{,}4 \cdot {{ vt('nch2369-galpon-grua/04', 'A_0', 2) }} = {{ vt('nch2369-galpon-grua/04', 'A_r', 2) }}\ \text{g}$$

→ **{{ v('nch2369-galpon-grua/04', 'A_r', 2) }} g**. El factor 1,4 es el mismo con el que la
norma industrial se separa de NCh433; lo que cambia respecto de las otras series de este
proyecto es la zona, que acá es {{ v('nch2369-galpon-grua/04', 'zona', 0) }} y allá 3.

### A2 · El suelo C es el que más amplifica de la Tabla 6, y no es el más blando

La Tabla 6 entrega los seis parámetros por tipo de suelo. El $S$ del suelo C vale
{{ v('nch2369-galpon-grua/04', 'S_suelo', 2) }} y es el **mayor de las cinco filas**: ni el
suelo D ni el E, más blandos, llegan a él.

$$S = {{ vt('nch2369-galpon-grua/04', 'S_suelo', 2) }} \qquad r = {{ vt('nch2369-galpon-grua/04', 'r_s', 2) }} \qquad T_0 = {{ vt('nch2369-galpon-grua/04', 'T_0', 2) }}\ \text{s} \qquad p = {{ vt('nch2369-galpon-grua/04', 'p_suelo', 2) }} \qquad q = {{ vt('nch2369-galpon-grua/04', 'q_s', 2) }} \qquad T_1 = {{ vt('nch2369-galpon-grua/04', 'T_1', 2) }}\ \text{s}$$

→ La amplificación **no crece monótonamente con la blandura**. $T_0$ y $q$ desplazan y aplanan
la meseta, así que un suelo más blando puede amplificar menos en período corto y más en
período largo. El suelo entra dos veces: en la amplitud por $S$ y en la frontera de la rampa
por $T_1$.

### A3 · El producto de los dos es la ordenada en período cero

$$A_r S = {{ vt('nch2369-galpon-grua/04', 'A_r', 2) }} \cdot {{ vt('nch2369-galpon-grua/04', 'S_suelo', 2) }} = {{ vt('nch2369-galpon-grua/04', 'ArS', 5) }}\ \text{g}$$

→ **{{ v('nch2369-galpon-grua/04', 'ArS', 3) }} g**, contra los
{{ v('nch2369-galpon-grua/04', 'ArS_harneros', 2) }} g de zona 3 y suelo D de la serie de
harneros: el producto de este sitio es **{{ v('nch2369-galpon-grua/04', 'raz_ArS', 5) }}
veces** el de allá, o sea un 21,25 % menos. B2 muestra que esa ventaja no se mantiene
donde el espectro tiene su pico.

## B · El espectro de referencia

### B1 · El 2 % de amortiguamiento amplifica un 44 % antes de que nada reduzca

La razón de amortiguamiento incorporada en los espectros de referencia es
{{ v('nch2369-galpon-grua/04', 'xi_ref', 2) }}; para razones menores se pondera por
$(0{,}05/\xi)^{0{,}4}$, expresión válida solo entre 0,02 y 0,05.

$$f_\xi = \left(\frac{ {{ vt('nch2369-galpon-grua/04', 'xi_ref', 2) }} }{ {{ vt('nch2369-galpon-grua/04', 'xi', 2) }} }\right)^{0{,}4} = 2{,}5^{0{,}4} = {{ vt('nch2369-galpon-grua/04', 'f_xi', 5) }}$$

→ **+44,27 %**. Es lo primero que la norma le hace al espectro, y va en el sentido contrario
al que la palabra «reducción» sugiere. El galpón está exactamente en el borde inferior de
validez de la expresión.

### B2 · El pico cae en 0,34533 s, y ahí el suelo C recupera lo que su zona no tiene

La Ec. (3) da el espectro de referencia horizontal. Su máximo se obtiene anulando la derivada,
lo que con $p = {{ vt('nch2369-galpon-grua/04', 'p_suelo', 2) }}$ y
$q = {{ vt('nch2369-galpon-grua/04', 'q_s', 2) }}$ deja una cuadrática en
$u = (T/T_0)^{1{,}5}$, con raíz $u = {{ vt('nch2369-galpon-grua/04', 'u_pico', 5) }}$.

$$S_{aH}({{ vt('nch2369-galpon-grua/04', 'T_pico', 5) }}) = {{ vt('nch2369-galpon-grua/04', 'ArS', 5) }} \cdot \frac{1 + {{ vt('nch2369-galpon-grua/04', 'r_s', 2) }} \cdot ({{ vt('nch2369-galpon-grua/04', 'T_pico', 5) }}/{{ vt('nch2369-galpon-grua/04', 'T_0', 2) }})^{1{,}50}}{1 + ({{ vt('nch2369-galpon-grua/04', 'T_pico', 5) }}/{{ vt('nch2369-galpon-grua/04', 'T_0', 2) }})^{3{,}00}} = {{ vt('nch2369-galpon-grua/04', 'Sa_pico', 5) }}\ \text{g}$$

→ **{{ v('nch2369-galpon-grua/04', 'Sa_pico', 5) }} g** en
{{ v('nch2369-galpon-grua/04', 'T_pico', 5) }} s. En
{{ v('nch2369-galpon-grua/04', 'T_star_X', 2) }} s este sitio da
{{ v('nch2369-galpon-grua/04', 'Sa_ref_X', 5) }} g contra los
{{ v('nch2369-galpon-grua/04', 'Sa_h_020', 5) }} g de zona 3 y suelo D: su cociente vale
{{ v('nch2369-galpon-grua/04', 'raz_Sa_020', 5) }}, o sea **11 % menos** de ordenada con
**21 % menos** de $A_r S$. La forma del suelo C se come la mitad de la ventaja de estar en
zona {{ v('nch2369-galpon-grua/04', 'zona', 0) }}.

## C · Las dos direcciones

### C1 · La fila 5.5 le da un solo R al edificio, y el análisis devuelve dos R*

La fila 5.5 de la Tabla 7 clasifica **edificios industriales de un piso con o sin puente
grúa**, sin distinguir sistema resistente ni dirección; las filas 5.1 a 5.4, en cambio,
clasifican por sistema. Y $R^{*}$ se calcula para el período del modo con mayor masa de
traslación equivalente **en la dirección de análisis**.

$$R_X = R_Y = {{ vt('nch2369-galpon-grua/04', 'R_T7', 0) }}$$

→ El mismo $R$ de tabla entra a las dos direcciones aunque una sea arriostrada y la otra un
marco de momento. Lo que las separa no es la tipología sino el período, y eso es lo que C4 y
C5 evalúan.

### C2 · La frontera de la rampa cae por debajo del pico del espectro

La Ec. (1b) fija $C_r = 0{,}16\,R$ y la rampa de período corto termina en $C_r T_1$.

$$C_r T_1 = 0{,}16 \cdot {{ vt('nch2369-galpon-grua/04', 'R_T7', 0) }} \cdot {{ vt('nch2369-galpon-grua/04', 'T_1', 2) }} = {{ vt('nch2369-galpon-grua/04', 'Cr_T1', 5) }}\ \text{s}$$

$$\frac{ {{ vt('nch2369-galpon-grua/04', 'T_pico', 5) }} }{ {{ vt('nch2369-galpon-grua/04', 'Cr_T1', 5) }} } = {{ vt('nch2369-galpon-grua/04', 'raz_pico_frontera', 5) }}$$

→ **{{ v('nch2369-galpon-grua/04', 'Cr_T1', 2) }} s**, un 23 % por debajo del período donde el
espectro de referencia tiene su máximo. Toda estructura que caiga en la rampa paga dos veces:
ve un $R^{*}$ degradado y está subiendo hacia el pico.

### C3 · Los dos períodos, y qué los separa

La dirección longitudinal la resisten cuatro paneles arriostrados de
{{ v('nch2369-galpon-grua/04', 's_marco', 2) }} m de base y
{{ v('nch2369-galpon-grua/04', 'h_libre', 2) }} m de alto; la transversal, cinco marcos de
momento de 25,00 m de luz. Los períodos son valores declarados.

$$\frac{T^{*}_Y}{T^{*}_X} = \frac{ {{ vt('nch2369-galpon-grua/04', 'T_star_Y', 2) }} }{ {{ vt('nch2369-galpon-grua/04', 'T_star_X', 2) }} } = {{ vt('nch2369-galpon-grua/04', 'raz_T', 5) }}$$

→ El marco de momento es **el doble de flexible** en período y cuatro veces en flexibilidad.
Es la separación normal entre las dos direcciones de un galpón, y es lo que hace que este
eslabón tenga dos respuestas y no una.

### C4 · La dirección arriostrada cae en la rampa y sale con R* = 4,00

Bajo la frontera, $R^{*}$ interpola linealmente entre
{{ v('nch2369-galpon-grua/04', 'R_piso', 1) }} y $R$.

$$R^{*}_X = 1{,}5 + ({{ vt('nch2369-galpon-grua/04', 'R_T7', 0) }} - 1{,}5)\frac{ {{ vt('nch2369-galpon-grua/04', 'T_star_X', 2) }} }{ {{ vt('nch2369-galpon-grua/04', 'Cr_T1', 5) }} } = {{ vt('nch2369-galpon-grua/04', 'R_star_X', 5) }}$$

$$S_{aH}({{ vt('nch2369-galpon-grua/04', 'T_star_X', 2) }}) = {{ vt('nch2369-galpon-grua/04', 'ArS', 5) }} \cdot \frac{1 + {{ vt('nch2369-galpon-grua/04', 'r_s', 2) }} \cdot ({{ vt('nch2369-galpon-grua/04', 'T_star_X', 2) }}/{{ vt('nch2369-galpon-grua/04', 'T_0', 2) }})^{1{,}50}}{1 + ({{ vt('nch2369-galpon-grua/04', 'T_star_X', 2) }}/{{ vt('nch2369-galpon-grua/04', 'T_0', 2) }})^{3{,}00}} = {{ vt('nch2369-galpon-grua/04', 'Sa_ref_X', 5) }}\ \text{g}$$

→ **$R^{*}_X = {{ vt('nch2369-galpon-grua/04', 'R_star_X', 2) }}$**, que es exactamente el $R$
de tabla que la fila 5.7 le daba al galpón liviano. El 01 celebró subir de 4 a 5 y la Ec. (1b)
lo devuelve a 4 en esta dirección. La penalización vale
{{ v('nch2369-galpon-grua/04', 'pena_rampa', 5) }}. La coincidencia con el 4 es de la cifra
declarada —la sensibilidad es de {{ v('nch2369-galpon-grua/04', 'sens_R', 2) }} por segundo, o
sea $R^{*}$ pasa de 3,75 a 4,25 entre 0,18 y 0,22 s—, pero la penalización no lo es.

### C5 · La de marcos conserva el 5 entero, y queda casi sobre el pico

Pasada la frontera, $R^{*} = R$.

$$S_{aH}({{ vt('nch2369-galpon-grua/04', 'T_star_Y', 2) }}) = {{ vt('nch2369-galpon-grua/04', 'ArS', 5) }} \cdot \frac{1 + {{ vt('nch2369-galpon-grua/04', 'r_s', 2) }} \cdot ({{ vt('nch2369-galpon-grua/04', 'T_star_Y', 2) }}/{{ vt('nch2369-galpon-grua/04', 'T_0', 2) }})^{1{,}50}}{1 + ({{ vt('nch2369-galpon-grua/04', 'T_star_Y', 2) }}/{{ vt('nch2369-galpon-grua/04', 'T_0', 2) }})^{3{,}00}} = {{ vt('nch2369-galpon-grua/04', 'Sa_ref_Y', 5) }}\ \text{g}$$

$$\frac{ {{ vt('nch2369-galpon-grua/04', 'Sa_ref_Y', 5) }} }{ {{ vt('nch2369-galpon-grua/04', 'Sa_pico', 5) }} } = {{ vt('nch2369-galpon-grua/04', 'frac_pico', 5) }}$$

→ $R^{*}_Y = {{ vt('nch2369-galpon-grua/04', 'R_star_Y', 2) }}$ y la ordenada de referencia
queda en el **98,0 % del máximo** del espectro. La dirección flexible no paga degradación pero
está sentada sobre el pico, así que rigidizarla —lo que el 07 va a querer hacer por deriva— la
mueve hacia la rampa por los dos lados a la vez.

### C6 · Las dos ordenadas de diseño, y la rígida ve más pese a tener el espectro menor

La Ec. (1a) arma el espectro de diseño con $I$, $f_\xi$ y $R^{*}$.

$$S_a(T^{*}_X) = \frac{ {{ vt('nch2369-galpon-grua/04', 'I', 2) }} \cdot {{ vt('nch2369-galpon-grua/04', 'Sa_ref_X', 5) }} \cdot {{ vt('nch2369-galpon-grua/04', 'f_xi', 5) }} }{ {{ vt('nch2369-galpon-grua/04', 'R_star_X', 5) }} } = {{ vt('nch2369-galpon-grua/04', 'Sa_dis_X', 5) }}\ \text{g}$$

$$S_a(T^{*}_Y) = \frac{ {{ vt('nch2369-galpon-grua/04', 'I', 2) }} \cdot {{ vt('nch2369-galpon-grua/04', 'Sa_ref_Y', 5) }} \cdot {{ vt('nch2369-galpon-grua/04', 'f_xi', 5) }} }{ {{ vt('nch2369-galpon-grua/04', 'R_star_Y', 5) }} } = {{ vt('nch2369-galpon-grua/04', 'Sa_dis_Y', 5) }}\ \text{g}$$

$$\frac{ {{ vt('nch2369-galpon-grua/04', 'Sa_dis_X', 5) }} }{ {{ vt('nch2369-galpon-grua/04', 'Sa_dis_Y', 5) }} } = {{ vt('nch2369-galpon-grua/04', 'raz_Sa_dis', 5) }}$$

→ La dirección arriostrada ve **4,7 % más** demanda que la de marcos aunque su espectro de
referencia sea un 16 % menor. Manda $R^{*}$, no la forma.

### C7 · La rama aguanta aunque el período declarado esté mal por un factor 1,4

El valor de $T^{*}$ es declarado; la **rama** de la Ec. (1b) en que cae, no. Un período se
mueve con la raíz de la masa, así que el margen de rama se mide en masa.

$$\left(\frac{ {{ vt('nch2369-galpon-grua/04', 'Cr_T1', 5) }} }{ {{ vt('nch2369-galpon-grua/04', 'T_star_X', 2) }} }\right)^{2} = {{ vt('nch2369-galpon-grua/04', 'marg_X', 5) }} \qquad \left(\frac{ {{ vt('nch2369-galpon-grua/04', 'Cr_T1', 5) }} }{ {{ vt('nch2369-galpon-grua/04', 'T_star_Y', 2) }} }\right)^{2} = {{ vt('nch2369-galpon-grua/04', 'marg_Y', 5) }}$$

→ La dirección arriostrada tendría que **casi duplicar** su masa para salir de la rampa, y la
de marcos tendría que perder **más de la mitad** para entrar en ella. Agregar la grúa entera a
la masa sísmica —lo que el 05 decide— cambiaría los períodos un 15 % y ninguna de las dos
ramas.

## D · Las cotas del 01, ahora con la degradación adentro

### D1 · El galpón liviano también degrada, y su frontera es otra

{{ figura('nch2369-galpon-grua/04', 'rampa-r', 'Las dos rampas de la Ec. 1b sobre el mismo eje de períodos: la del galpón de la fila 5.5 sube hasta 5 en la frontera de 0,280 s y la del galpón liviano hasta 4 en la de 0,224 s, con los cuatro valores de R estrella que producen los dos períodos de análisis') }}

Las tres comparaciones del 01 se hicieron con $R_1 = R^{*} = R$, es decir sin degradación.
Pero $C_r = 0{,}16\,R$ mueve la frontera junto con el $R$, así que el galpón liviano de la
fila 5.7 tiene la suya.

$$C_r T_1\big|_{R=4} = 0{,}16 \cdot {{ vt('nch2369-galpon-grua/04', 'R_liv', 0) }} \cdot {{ vt('nch2369-galpon-grua/04', 'T_1', 2) }} = {{ vt('nch2369-galpon-grua/04', 'Cr_T1_liv', 5) }}\ \text{s}$$

$$R^{*}_{X,\text{liv}} = 1{,}5 + ({{ vt('nch2369-galpon-grua/04', 'R_liv', 0) }} - 1{,}5)\frac{ {{ vt('nch2369-galpon-grua/04', 'T_star_X', 2) }} }{ {{ vt('nch2369-galpon-grua/04', 'Cr_T1_liv', 5) }} } = {{ vt('nch2369-galpon-grua/04', 'R_star_X_liv', 5) }}$$

→ Con $T^{*}_X = {{ vt('nch2369-galpon-grua/04', 'T_star_X', 2) }}$ s el galpón liviano
**también** está en su rampa, y sale con {{ v('nch2369-galpon-grua/04', 'R_star_X_liv', 2) }}
en vez de {{ v('nch2369-galpon-grua/04', 'R_liv', 0) }}. La comparación honesta no es 5 contra
4: es {{ v('nch2369-galpon-grua/04', 'R_star_X', 2) }} contra
{{ v('nch2369-galpon-grua/04', 'R_star_X_liv', 2) }}.

### D2 · Y así el alivio del fusible se cae a un tercio en la dirección arriostrada

El fusible —diagonal y perno de anclaje— ve la demanda reducida por $R^{*}$ y no ve el
amplificador.

$$\frac{1/{{ vt('nch2369-galpon-grua/04', 'R_star_X', 5) }} }{1/{{ vt('nch2369-galpon-grua/04', 'R_star_X_liv', 5) }} } = {{ vt('nch2369-galpon-grua/04', 'alivio_X', 5) }}$$

→ **6,7 % menos**, no el 20 % que el 01 anunció. Dos tercios del alivio se los comió la
Ec. (1b), y se los comió porque la frontera se corre con $R$: subir el $R$ de tabla también
sube el período a partir del cual ese $R$ se puede usar.

### D3 · En la dirección de marcos la cota del 01 vale entera

$$R^{*}_{Y,\text{liv}} = {{ vt('nch2369-galpon-grua/04', 'R_star_Y_liv', 5) }} \qquad \frac{1/{{ vt('nch2369-galpon-grua/04', 'R_star_Y', 5) }} }{1/{{ vt('nch2369-galpon-grua/04', 'R_star_Y_liv', 5) }} } = {{ vt('nch2369-galpon-grua/04', 'alivio_Y', 5) }}$$

→ **20 % menos**, exactamente lo que el 01 dijo. Con
$T^{*}_Y = {{ vt('nch2369-galpon-grua/04', 'T_star_Y', 2) }}$ s las dos configuraciones están
en su meseta y ninguna degrada.

### D4 · El elemento no fusible no se entera de la degradación

El no fusible ve la carga ya reducida por $R^{*}$ y después amplificada por $0{,}7R_1$. Con
$R_1 = R^{*}$ el par de operaciones deja la fracción de demanda elástica $\alpha$, que **no
depende de cuánto haya degradado**.

$$\frac{\alpha_{\text{gr}}}{\alpha_{\text{liv}}} = \frac{ {{ vt('nch2369-galpon-grua/04', 'k_amp', 5) }} }{ {{ vt('nch2369-galpon-grua/04', 'k_amp_liv', 5) }} } = {{ vt('nch2369-galpon-grua/04', 'sobre_nofusible', 5) }}$$

→ **40 % más**, idéntico en las dos direcciones e idéntico a lo que el 01 calculó sin
degradar. La Ec. (1b) se cancela consigo misma porque el mismo $R^{*}$ está en el denominador
de la reducción y en el numerador del amplificador. Es el único de los cuatro números del 01
que la degradación deja intacto.

### D5 · Y el amplificador sube 50 % en la arriostrada y 75 % en la de marcos

El multiplicador del diseño por capacidad es $k_{\text{amp}} R_1$, con $R_1 = R^{*}$ mientras
§5.12 no lo levante.

$$\frac{ {{ vt('nch2369-galpon-grua/04', 'k_amp', 2) }} \cdot {{ vt('nch2369-galpon-grua/04', 'R_star_X', 5) }} }{ {{ vt('nch2369-galpon-grua/04', 'k_amp_liv', 2) }} \cdot {{ vt('nch2369-galpon-grua/04', 'R_star_X_liv', 5) }} } = \frac{ {{ vt('nch2369-galpon-grua/04', 'amp_X', 5) }} }{ {{ vt('nch2369-galpon-grua/04', 'amp_X_liv', 5) }} } = {{ vt('nch2369-galpon-grua/04', 'alza_X', 5) }}$$

$$\frac{ {{ vt('nch2369-galpon-grua/04', 'k_amp', 2) }} \cdot {{ vt('nch2369-galpon-grua/04', 'R_star_Y', 5) }} }{ {{ vt('nch2369-galpon-grua/04', 'k_amp_liv', 2) }} \cdot {{ vt('nch2369-galpon-grua/04', 'R_star_Y_liv', 5) }} } = \frac{ {{ vt('nch2369-galpon-grua/04', 'amp_Y', 5) }} }{ {{ vt('nch2369-galpon-grua/04', 'amp_Y_liv', 5) }} } = {{ vt('nch2369-galpon-grua/04', 'alza_Y', 5) }}$$

→ **50 % en la arriostrada y 75 % en la de marcos**, contra el 75 % único que el 01 había
anunciado para todo el galpón. El precio de perder §12.2 no es un número: es dos, y el más
caro está en la dirección que el 01 no podía distinguir.

## Veredicto

La frontera de la Ec. (1b) cae en **{{ v('nch2369-galpon-grua/04', 'Cr_T1', 2) }} s** y las
dos direcciones del galpón caen a lados distintos: la arriostrada degrada hasta
$R^{*} = {{ vt('nch2369-galpon-grua/04', 'R_star_X', 2) }}$ y la de marcos conserva el
{{ v('nch2369-galpon-grua/04', 'R_star_Y', 0) }}. Las ordenadas de diseño son
**{{ v('nch2369-galpon-grua/04', 'Sa_dis_X', 5) }} g** y
**{{ v('nch2369-galpon-grua/04', 'Sa_dis_Y', 5) }} g**, y la rígida es la mayor pese a tener
un espectro de referencia 16 % menor.

Lo que este eslabón le corrige al 01 no es un número sino una asimetría. **El alivio del
fusible vale 20 % en la dirección de marcos y 6,7 % en la arriostrada**, porque el galpón
liviano también degrada y su frontera es {{ v('nch2369-galpon-grua/04', 'Cr_T1_liv', 5) }} s
en vez de {{ v('nch2369-galpon-grua/04', 'Cr_T1', 2) }}. **El sobrecosto del no fusible, en
cambio, sale {{ v('nch2369-galpon-grua/04', 'sobre_nofusible', 2) }} en las dos**: el
amplificador y la reducción usan el mismo $R_1$ y la degradación se cancela consigo misma. Y
el amplificador de capacidad sube 50 % en una dirección y 75 % en la otra, contra el 75 %
único que el 01 había anunciado.

Para cerrar el eslabón hace falta la masa sísmica, que es el 05: si §12.1.3 obliga a agregar
la carga suspendida, los períodos suben un 15 % y ninguna de las dos ramas cambia. El 06
hereda además $T_0 = {{ vt('nch2369-galpon-grua/04', 'T_0', 2) }}$ s,
$p = {{ vt('nch2369-galpon-grua/04', 'p_suelo', 2) }}$,
$q = {{ vt('nch2369-galpon-grua/04', 'q_s', 2) }}$,
$r = {{ vt('nch2369-galpon-grua/04', 'r_s', 2) }}$, el pico
({{ v('nch2369-galpon-grua/04', 'T_pico', 5) }} s,
{{ v('nch2369-galpon-grua/04', 'Sa_pico', 5) }} g), $A_r S$, $A_r$, $S$, $f_\xi$, los dos
$T^{*}$, los dos $R^{*}$ y las dos ordenadas de referencia
({{ v('nch2369-galpon-grua/04', 'Sa_ref_X', 5) }} y
{{ v('nch2369-galpon-grua/04', 'Sa_ref_Y', 5) }} g) para armar la componente vertical y las
combinaciones; el 05 hereda además $T_1 = {{ vt('nch2369-galpon-grua/04', 'T_1', 2) }}$ s,
$C_r T_1$ y las dos ordenadas de diseño.

## Límites

- **Los períodos son declarados** (S2). No hay modelo corrido en este eslabón, no hay masas
  participantes y no hay verificación de que el modo de mayor masa de traslación sea el
  fundamental. Lo que este eslabón sostiene es la **rama** de cada dirección, y C7 la mide en
  margen de masa: {{ v('nch2369-galpon-grua/04', 'marg_X', 2) }} y
  {{ v('nch2369-galpon-grua/04', 'marg_Y', 2) }}.
- **El [00](../00-el-modelo/) ya publica los períodos del modelo corrido, y este eslabón
  todavía no los hereda.** El modelo tridimensional da 0,24878 s en Y y 0,20602 s en X, contra
  los {{ v('nch2369-galpon-grua/04', 'T_star_Y', 2) }} y
  {{ v('nch2369-galpon-grua/04', 'T_star_X', 2) }} declarados. Tomarlos cambia de rama en Y y
  de ahí bajan $R_1$, el amplificador, la componente vertical del 06 y el anclaje: es la
  cascada, y se aplica como un cambio explícito **después** de migrar la serie completa, para
  que el test de cadena la delate eslabón por eslabón. Hasta entonces, esta página reproduce
  lo que el memo original publicó.
- **$T^{*}$ y el período de $R^{*}$ no son la misma definición en la norma.** §5.4 define
  $T^{*}$ como el período **fundamental** en la dirección y $R^{*}$ como el factor calculado
  para el período del modo con **mayor masa de traslación equivalente**. En un galpón con dos
  de cuatro vanos arriostrados y un diafragma de techo flexible los dos pueden no coincidir, y
  C5.4.1 exige verificar que el período adoptado maximice la respuesta. Este eslabón los supone
  iguales y no lo verifica: es el 12, con la irregularidad en planta, el que puede desmentirlo.
- **La masa que los períodos suponen es la permanente, sin carga suspendida.** La contradicción
  entre AIST §3.6 y NCh2369 §12.1.3 la resuelve el 05.
- **La componente vertical no se evalúa acá.** Las Ecs. (2) y (4), con $R_V = 2{,}0$ y
  $\xi_V = 0{,}03$ fijos, y el coeficiente estático de §5.7.1 son del 06, junto con las
  combinaciones. Este eslabón no publica ninguna ordenada vertical.
- **No se clasifica el sitio** (S1). Zona y suelo entran como dato heredado del 01, no por
  falta de regla sino de comuna y de sondaje. Son los dos números de los que todo depende: con
  suelo D en vez de C la frontera se iría a 0,328 s y la dirección de marcos caería **también**
  en la rampa.
- **No se toma el recorte de §5.13 ni el piso de §5.12.** Este eslabón usa $R_1 = R^{*}$ para
  las comparaciones de D4 y D5, que es cota. La banda de $R_1$ la fija el 05.
- **No se cubre el espectro de sitio de §5.4.3 ni el tiempo-historia de §5.10.** La NOTA de la
  Tabla 6 los recomienda desde períodos de 4 s, y este galpón está un orden de magnitud por
  debajo.

## Ficha

{{ ficha('nch2369-galpon-grua/04') }}

## Referencias

| Clave | Norma y edición | Cláusula | Leída en | Cita textual |
|---|---|---|---|---|
| NCh-p1 | NCh2369:2025 (3.ª ed.) | §5.4, la definición de $T^{*}$ como período fundamental de la dirección, evaluado por procedimiento teórico o empírico | `Normas/NCh 2369 - 3°Edición 2025.05.28.pdf`, p. 34 | «período fundamental en la dirección horizontal de análisis sísmico, evaluado mediante un procedimiento teórico o empírico fundamentado» |
| NCh-p2 | NCh2369:2025 (3.ª ed.) | §5.4, la definición de $R^{*}$, que no es el período fundamental sino el del modo con mayor masa de traslación | PDF ídem, p. 34 | «respuesta estructural, calculado para el período del modo con mayor masa de traslación equivalente, en la dirección de análisis» |
| NCh-p3 | NCh2369:2025 (3.ª ed.) | §5.4.1, Ec. (1a) y Ec. (1b) con sus tres ramas y $C_r = 0{,}16R$ — **mirada en PNG**, no extraída | PDF ídem, p. 35 | «Se define el siguiente espectro de diseño para la dirección horizontal» |
| NCh-p4 | NCh2369:2025 (3.ª ed.) | C5.4.1, la obligación de verificar que el período adoptado para $R^{*}$ maximice la respuesta | PDF ídem, p. 35 | «es necesario verificar que el período de vibración adoptado para el cálculo de R *, sea representativo y maximice la respuesta de la estructura» |
| NCh-p5 | NCh2369:2025 (3.ª ed.) | §5.4.2, Ec. (3) y la validez de la corrección por amortiguamiento sólo entre 0,02 y 0,05 | PDF ídem, p. 36 | «Esta expresión es válida sólo para valores de ξ entre 0,02 y 0,05» |
| NCh-p6 | NCh2369:2025 (3.ª ed.) | §5.4.2, el nivel de demanda de los espectros de referencia | PDF ídem, p. 36 | «Los espectros de referencia para la dirección horizontal y vertical corresponden a demandas asociadas a nivel último» |
| NCh-p7 | NCh2369:2025 (3.ª ed.) | Tabla 3, la fila de la zona 2 — **mirada en PNG**, no extraída | PDF ídem, p. 64 | «1 0,20 g 0,28 g 2 0,30 g 0,42 g 3 0,40 g 0,56 g» |
| NCh-p8 | NCh2369:2025 (3.ª ed.) | Tabla 4, el suelo C y su clasificación por $V_{s30}$ y $T_g$ | PDF ídem, p. 64 | «Suelo denso o firme» |
| NCh-p9 | NCh2369:2025 (3.ª ed.) | Tabla 6, la fila del suelo C con sus seis parámetros — **mirada en PNG**, no extraída | PDF ídem, p. 67 | «C 1,05 4,50 0,40 1,50 3,00 0,35» |
| NCh-p10 | NCh2369:2025 (3.ª ed.) | Tabla 6, la fila del suelo D, que es la de la serie de harneros y con la que se contrasta | PDF ídem, p. 67 | «D 1,00 3,50 0,60 1,00 2,50 0,41» |
| NCh-p11 | NCh2369:2025 (3.ª ed.) | Tabla 6, la NOTA que remite a §5.4.3 y §5.10 desde 4 s | PDF ídem, p. 67 | «para todos los tipos de suelos cuando se diseñen estructuras con período fundamental de 4 s o más» |
| NCh-5 | NCh2369:2025 (3.ª ed.) | §5.4 completo, §5.12 a §5.14 y §5.7 | `referencias/NCh2369-2025/cap05-analisis-sismico.md` | — |
| NCh-8 | NCh2369:2025 (3.ª ed.) | §8.3.4 (amplificación por $0{,}7R_1$), §8.5.2 y §8.6.2 | `referencias/NCh2369-2025/cap08-estructuras-de-acero.md` | — |
| NCh-12 | NCh2369:2025 (3.ª ed.) | §12.1.3 y §12.2.2, que el 01 ya recorrió | `referencias/NCh2369-2025/cap12-estructuras-especificas.md` | — |
