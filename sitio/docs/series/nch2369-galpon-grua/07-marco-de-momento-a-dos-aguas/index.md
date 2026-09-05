# 07 · El marco de momento a dos aguas

Lo que dimensiona este marco no es ninguna de las dos derivas: es el **período** que el 04
declaró, y que ningún eslabón había presentado como un requisito de rigidez. Y rigidizar no
cuesta nada, porque el techo de §5.13 se arma sin el período adentro. Acá se dimensiona el
marco transversal de alma variable, se reparte el empuje lateral de la grúa entre marcos y se
verifican §8.7 y los dos criterios de deriva. Fuerzas en kN, longitudes en mm salvo donde se
indique.

## El caso

{{ figura('nch2369-galpon-grua/07', 'marco', 'Elevación del marco de momento a dos aguas de 25,00 m de luz, 10,50 m al alero y 13,00 a la cumbrera, con la columna de alma variable de 1 050 mm en la base a 750 en el nudo —más gruesa abajo que arriba— el rafter de 750 a 425 en la cumbrera, el nivel de riel a 7,50 m donde la columna mide 835,71429 mm, el punto de inflexión del modo lateral a 7,74863 m y los 46,40000 kN de empuje de grúa entrando por los dos rieles al mismo lado') }}

| Dato | Valor |
|---|---|
| Elemento | marco de momento transversal, a dos aguas, alma variable soldada (del 01) |
| Luz entre ejes de columnas | {{ v('nch2369-galpon-grua/07', 'L_luz', 2) }} m (del 01) |
| Altura libre de columna | {{ v('nch2369-galpon-grua/07', 'h_libre', 2) }} m (del 01) |
| Pendiente de cubierta | 20 %, cumbrera a {{ v('nch2369-galpon-grua/07', 'h_cumb', 2) }} m (del 02) |
| Separación de marcos | {{ v('nch2369-galpon-grua/07', 's_marco', 2) }} m, {{ v('nch2369-galpon-grua/07', 'n_marcos', 0) }} marcos (del 01) |
| Nivel superior del riel | {{ v('nch2369-galpon-grua/07', 'h_riel', 2) }} m (del 01) |
| Base de columnas | empotrada (del 04) |
| Acero | ASTM A572 Gr. 50 en **plancha**: $F_y = {{ vt('nch2369-galpon-grua/07', 'Fy', 0) }}$ MPa, $R_y = {{ vt('nch2369-galpon-grua/07', 'Ry', 2) }}$, $E = {{ vt('nch2369-galpon-grua/07', 'E_ac', 0) }}$ MPa |
| Columna adoptada | alma variable {{ v('nch2369-galpon-grua/07', 'd_col_base', 0) }} → {{ v('nch2369-galpon-grua/07', 'd_col_nudo', 0) }} mm, alas {{ v('nch2369-galpon-grua/07', 'bf_col', 0) }} × {{ v('nch2369-galpon-grua/07', 'tf_col', 0) }}, alma {{ v('nch2369-galpon-grua/07', 'tw_col', 0) }} |
| Rafter adoptado | alma variable {{ v('nch2369-galpon-grua/07', 'd_raf_nudo', 0) }} → {{ v('nch2369-galpon-grua/07', 'd_raf_cumb', 0) }} mm, alas {{ v('nch2369-galpon-grua/07', 'bf_raf', 0) }} × {{ v('nch2369-galpon-grua/07', 'tf_raf', 0) }}, alma {{ v('nch2369-galpon-grua/07', 'tw_raf', 0) }} |
| Factores de resistencia | $\phi_b = \phi_v = {{ vt('nch2369-galpon-grua/07', 'phi_b', 2) }}$ |
| Lo que se decide aquí | las secciones del marco, el período definitivo, cuál nieve gobierna y §8.7 de miembro |

Los supuestos, en una línea cada uno. **S1**, el marco se resuelve por **rigidez directa**,
discretizando cada miembro de alma variable en 42 segmentos prismáticos con las propiedades de
la sección en el centro de cada uno; los resultados de ese modelo —las dos rigideces laterales,
la rigidez vertical y los momentos de barra— **son valores declarados**, no algo que un paso de
este eslabón produzca, y por eso viven en el `caso` de su ficha y no en un `paso`. **S2**, las
secciones son las adoptadas por este eslabón, con el espesor de alma **constante en cada
miembro**, que es lo que una plancha cortada en cuña permite: la altura varía y el espesor no.
**S3**, el nudo es **a inglete y sin cartela**, así que la columna y el rafter llegan al alero
con la misma altura. **S4**, la viga carrilera es simplemente apoyada en cada vano y el
arriostramiento de techo **no redistribuye** el empuje lateral entre marcos; las dos cosas son
conservadoras y C3 mide cuánto vale la segunda. **S5**, el acero es ASTM A572 Gr. 50 en plancha.
**S6**, la acumulación de nieve del 02 se sitúa en el faldón de sotavento contiguo a la
cumbrera; el 02 dio la intensidad y la extensión pero no de qué lado sopla. **S7**, el axial de
la columna en la base incluye la reacción vertical de la grúa entregada por la carrilera,
**concéntrica**: la excentricidad de la ménsula y su momento son del eslabón 10. **S8**, el ala
interior del rafter se arriostra con tirantes a la costanera en los puntos que E6 fija.

## A · Las dos obligaciones que hereda, y lo que cuesta cumplirlas

### A1 · La rigidez que el 05 le dejó, y de dónde sale que falte un 10 %

El período que el 04 declaró y la masa que el 05 fijó determinan **juntos** la rigidez lateral
del marco: no es una elección. El 05 la calculó y la contrastó contra la sección preliminar con
que el arnés del 04 sostuvo su banda.

$$\alpha = \frac{k_Y^{\text{req}}}{k_Y^{\text{prel}}} = \frac{ {{ vt('nch2369-galpon-grua/07', 'k_req_Y', 5) }} }{ {{ vt('nch2369-galpon-grua/07', 'k_prel_Y', 5) }} } = {{ vt('nch2369-galpon-grua/07', 'alpha', 5) }}$$

→ hacen falta **10,3 % más de rigidez** que la sección preliminar. Es la primera obligación que
este eslabón recibe, y es la única que resultó gobernar.

### A2 · Rigidizar sube la ordenada, porque el período está casi sobre el pico

El 04 dejó la dirección de marcos casi sobre el máximo del espectro de referencia, así que
acortar el período la mueve **hacia** él.

$$\frac{S_{aH}(T^{*}_Y)}{S_{aH}^{\text{máx}}} = \frac{ {{ vt('nch2369-galpon-grua/07', 'Sa_ref_Y', 5) }} }{ {{ vt('nch2369-galpon-grua/07', 'Sa_pico', 5) }} } = {{ vt('nch2369-galpon-grua/07', 'frac_pico_dec', 5) }} \qquad T_\alpha = \frac{ {{ vt('nch2369-galpon-grua/07', 'T_star_Y', 2) }} }{\sqrt{ {{ vt('nch2369-galpon-grua/07', 'alpha', 5) }} }} = {{ vt('nch2369-galpon-grua/07', 'T_alpha', 5) }}\ \text{s}$$

$$S_{aH}(T_\alpha) = {{ vt('nch2369-galpon-grua/07', 'Sa_alpha', 5) }}\ \text{g} \qquad \frac{ {{ vt('nch2369-galpon-grua/07', 'Sa_alpha', 5) }} }{ {{ vt('nch2369-galpon-grua/07', 'Sa_ref_Y', 5) }} } = {{ vt('nch2369-galpon-grua/07', 'sube_ord', 5) }}$$

→ la ordenada de referencia sube **1,11 %**. Es la trampa que el 04 anunció: en una serie
hermana el período estaba a 2,3 veces del pico y rigidizar lo empujaba cuesta arriba por un
tramo largo. Acá el tramo es corto.

### A3 · Y aun así no cuesta nada, porque el techo de §5.13 no depende del período

El corte de diseño de esta dirección no es el del análisis: el 05 tomó el recorte de §5.13, y
la Ec. (13) se arma con $A_r$, $S$, $\xi$ y el $R$ **de tabla**, sin $T$ adentro. Subir la
ordenada sube el corte del análisis y **no mueve el techo**.

$$Q_0^{\text{an}}(T_\alpha) = \frac{ {{ vt('nch2369-galpon-grua/07', 'Sa_alpha', 5) }} \cdot {{ vt('nch2369-galpon-grua/07', 'f_xi', 5) }} }{ {{ vt('nch2369-galpon-grua/07', 'R_star_Y', 5) }} } \cdot {{ vt('nch2369-galpon-grua/07', 'P_sismico', 5) }} = {{ vt('nch2369-galpon-grua/07', 'Q0_an_alpha', 5) }}\ \text{kN}$$

$$\left(\frac{ {{ vt('nch2369-galpon-grua/07', 'T_star_Y', 2) }} }{ {{ vt('nch2369-galpon-grua/07', 'Cr_T1', 5) }} }\right)^{2} = {{ vt('nch2369-galpon-grua/07', 'k_frontera', 5) }}$$

→ el corte del análisis supera al techo en {{ v('nch2369-galpon-grua/07', 'sobre_techo_alpha', 5) }}
y el corte de diseño **sigue siendo el mismo**. Rigidizar un 10,3 % cuesta **cero** en fuerza
sísmica. Y la rama de la Ec. (1b) aguanta: el marco tendría que rigidizarse
{{ v('nch2369-galpon-grua/07', 'k_frontera', 5) }} veces para que el período llegara a la
frontera y $R^{*}$ empezara a degradar; hace falta {{ v('nch2369-galpon-grua/07', 'alpha', 5) }}.

## B · El marco: geometría, alma variable y rigidez

### B1 · La geometría sale de la luz, la altura y la razón de pendiente del 02

El símbolo $S$ de NCh431 es la razón horizontal, uno sobre la pendiente, y el 02 lo fijó en
{{ v('nch2369-galpon-grua/07', 'S_pend', 5) }} para el 20 %.

$$f = \frac{L}{2\,S} = \frac{ {{ vt('nch2369-galpon-grua/07', 'L_luz', 2) }} }{2 \cdot {{ vt('nch2369-galpon-grua/07', 'S_pend', 5) }} } = {{ vt('nch2369-galpon-grua/07', 'f_cumb', 2) }}\ \text{m} \qquad L_r = {{ vt('nch2369-galpon-grua/07', 'L_r', 5) }}\ \text{m}$$

→ cumbrera a {{ v('nch2369-galpon-grua/07', 'h_cumb', 2) }} m y
{{ v('nch2369-galpon-grua/07', 'L_r', 5) }} m de rafter por agua, un 2,0 % más que la
proyección horizontal. Los dos números vuelven en E6, donde la separación de arriostramientos
se mide **sobre** el rafter y no sobre su proyección.

### B2 · La conicidad de la columna corre al revés de la del catálogo

El marco de alma variable que un proveedor despacha tiene la columna **poco profunda en la base
y profunda en el nudo**, porque presupone base rotulada, donde el momento en la base vale cero.
El 04 declaró **base empotrada** —y lo declaró justamente porque en un galpón con grúa manda la
deriva de servicio—, así que el momento máximo de la columna no está donde el catálogo lo pone.

$$\left.\frac{M_{\text{base}}}{M_{\text{nudo}}}\right|_{\text{lateral}} = {{ vt('nch2369-galpon-grua/07', 'razon_sway', 5) }} \qquad y_{\text{infl}} = {{ vt('nch2369-galpon-grua/07', 'y_infl', 5) }}\ \text{m} \qquad \frac{ y_{\text{infl}} }{ h_{\text{riel}} } = {{ vt('nch2369-galpon-grua/07', 'y_infl_riel', 5) }}$$

→ bajo carga lateral pura el momento de la base es **2,82 veces** el del nudo, y con las
combinaciones completas la sección crítica de la columna es la **base**, por
{{ v('nch2369-galpon-grua/07', 'razon_criticas', 5) }} sobre el nudo. La conicidad tiene que
abrir hacia abajo. El catálogo no está equivocado: está resolviendo otra condición de apoyo, y
quien copie la sección sin copiar la base pone la plancha ancha donde el momento es menor. Y el
**punto de inflexión** cae a 25 cm del riel: el empuje de la grúa entra prácticamente sobre el
punto de momento nulo del modo lateral, y ésa es la razón mecánica de que produzca tan poca
deriva (C2).

### B3 · Las secciones adoptadas, y la sección en el riel que el 10 va a necesitar

Sección I doblemente simétrica, alas y alma de espesor constante, altura lineal entre los dos
extremos.

$$I_{\text{base}} = {{ vt('nch2369-galpon-grua/07', 'I_base', 0) }}\ \text{mm}^4 \qquad Z_{\text{base}} = {{ vt('nch2369-galpon-grua/07', 'Zx_col_base', 0) }}\ \text{mm}^3 \qquad A_{\text{base}} = {{ vt('nch2369-galpon-grua/07', 'Ag_col_base', 0) }}\ \text{mm}^2$$

$$I_{\text{nudo}}^{\text{col}} = {{ vt('nch2369-galpon-grua/07', 'I_nudo_col', 0) }}\ \text{mm}^4 \qquad Z_{\text{nudo}}^{\text{col}} = {{ vt('nch2369-galpon-grua/07', 'Z_nudo_col', 0) }}\ \text{mm}^3 \qquad A_{\text{nudo}}^{\text{col}} = {{ vt('nch2369-galpon-grua/07', 'Ag_col_nudo', 0) }}\ \text{mm}^2$$

$$I_{\text{nudo}}^{\text{raf}} = {{ vt('nch2369-galpon-grua/07', 'I_nudo_raf', 0) }}\ \text{mm}^4 \qquad Z_{\text{nudo}}^{\text{raf}} = {{ vt('nch2369-galpon-grua/07', 'Zx_raf', 0) }}\ \text{mm}^3 \qquad A_{\text{nudo}}^{\text{raf}} = {{ vt('nch2369-galpon-grua/07', 'Ag_raf_nudo', 0) }}\ \text{mm}^2$$

$$I_y^{\text{raf}} = {{ vt('nch2369-galpon-grua/07', 'Iy_raf', 0) }}\ \text{mm}^4 \qquad r_y^{\text{raf}} = {{ vt('nch2369-galpon-grua/07', 'ry_raf', 5) }}\ \text{mm} \qquad I_{\text{cumb}} = {{ vt('nch2369-galpon-grua/07', 'I_cumb', 0) }}\ \text{mm}^4 \qquad Z_{\text{cumb}} = {{ vt('nch2369-galpon-grua/07', 'Z_cumb', 0) }}\ \text{mm}^3$$

$$d_{\text{riel}} = {{ vt('nch2369-galpon-grua/07', 'd_col_riel', 5) }}\ \text{mm} \qquad A_{\text{riel}} = {{ vt('nch2369-galpon-grua/07', 'Ag_col_riel', 2) }}\ \text{mm}^2$$

→ la columna mide {{ v('nch2369-galpon-grua/07', 'd_col_riel', 5) }} mm **en el nivel del
riel**, un 11,4 % más que en el nudo. La ménsula del 10 se apoya en la parte gruesa de la cuña,
que es lo que esta conicidad compra además de la rigidez.

### B4 · La rigidez que resulta, y que el marco pesa menos que lo que el 05 le asignó

El modelo declarado entrega la rigidez lateral del marco en el alero y en el nivel del riel. La
segunda no es la primera: **el empuje de la grúa no entra por el alero**.

$$k_Y = {{ vt('nch2369-galpon-grua/07', 'k_Y', 5) }}\ \text{kN}/\text{m} \qquad k_{\text{riel}} = {{ vt('nch2369-galpon-grua/07', 'k_riel', 5) }}\ \text{kN}/\text{m} \qquad \frac{k_Y}{k_Y^{\text{req}}} = {{ vt('nch2369-galpon-grua/07', 'margen_k', 5) }}$$

$$w_{\text{presup}} = {{ vt('nch2369-galpon-grua/07', 'w_presup_marco', 5) }}\ \text{kN} \qquad \frac{ {{ vt('nch2369-galpon-grua/07', 'w_marco', 5) }} }{ {{ vt('nch2369-galpon-grua/07', 'w_presup_marco', 5) }} } = {{ vt('nch2369-galpon-grua/07', 'consumo_presup', 5) }}$$

→ **7,6 % sobre lo que el 05 pidió**, con un marco que pesa
{{ v('nch2369-galpon-grua/07', 'w_marco', 5) }} kN y consume el
{{ v('nch2369-galpon-grua/07', 'consumo_presup', 5, 100) }} % de lo que el 05 había asignado a
estructura de techo y columnas por marco. La masa sísmica del 05 no hay que rehacerla.

### B5 · El período definitivo, y la ordenada que sube 0,87 %

$$m_{\text{marco}} = \frac{ {{ vt('nch2369-galpon-grua/07', 'P_sismico', 5) }} }{ {{ vt('nch2369-galpon-grua/07', 'n_marcos', 0) }} \cdot {{ vt('nch2369-galpon-grua/07', 'g_grav', 2) }} } = {{ vt('nch2369-galpon-grua/07', 'm_marco', 5) }} \qquad T^{*}_{Y2} = 2\pi\sqrt{\frac{m_{\text{marco}}}{k_Y}} = {{ vt('nch2369-galpon-grua/07', 'T_star_Y2', 5) }}\ \text{s}$$

$$S_{aH}(T^{*}_{Y2}) = {{ vt('nch2369-galpon-grua/07', 'Sa_Y2', 5) }}\ \text{g} \qquad {{ vt('nch2369-galpon-grua/07', 'subio_ord', 5) }} \qquad {{ vt('nch2369-galpon-grua/07', 'frac_pico_2', 5) }}$$

→ **{{ v('nch2369-galpon-grua/07', 'T_star_Y2', 5) }} s**, y la ordenada sube 0,87 %. El
período pasa del 98,0 % al **98,9 % del pico** del espectro de referencia: la dirección de
marcos se acerca al máximo sin llegar a él.

### B6 · Y el corte de diseño, comprobado con el período nuevo, no se movió

$$Q_0^{\text{an}}(T^{*}_{Y2}) = {{ vt('nch2369-galpon-grua/07', 'Q0_an_2', 5) }}\ \text{kN} \qquad \frac{Q_0^{\text{an}}}{Q_0^{\text{dis}}} = {{ vt('nch2369-galpon-grua/07', 'sobre_techo_2', 5) }}$$

→ el corte del análisis sube y el techo lo sigue mordiendo: el corte de diseño queda en
{{ v('nch2369-galpon-grua/07', 'Q0_Y', 5) }} kN, idéntico al del 05, y con él quedan idénticos
el amplificador de capacidad, la componente vertical y las cuatro combinaciones del 06.
**Ningún número de fuerza de la serie cambia por rigidizar el marco.**

## C · La deriva que manda de verdad

{{ figura('nch2369-galpon-grua/07', 'derivas', 'Las tres demandas laterales del marco a la misma escala contra sus dos límites: los 3,08155 mm que el empuje de grúa produce al nivel del riel contra los 18,75 mm de AIST, los 1,70543 mm que la nieve desbalanceada mueve el mismo riel, y los 65,22861 mm del sismo al alero contra los 157,50 de la cláusula 6.3') }}

### C1 · Cuánto del empuje lateral llega a un marco

AIST pide repartir el empuje transversal total **entre las columnas que soportan las
carrileras, con un análisis global del sistema y según rigidez relativa**. Con la carrilera
simplemente apoyada en cada vano, la posición peor pone una rueda sobre el marco y la otra a la
distancia entre ruedas.

$$R_{\text{carril}} = \frac{ {{ vt('nch2369-galpon-grua/07', 'SS_carril', 5) }} }{2}\left(1 + \frac{ {{ vt('nch2369-galpon-grua/07', 's_marco', 2) }} - {{ vt('nch2369-galpon-grua/07', 'wb_ruedas', 2) }} }{ {{ vt('nch2369-galpon-grua/07', 's_marco', 2) }} }\right) = {{ vt('nch2369-galpon-grua/07', 'R_carril', 5) }}\ \text{kN}$$

$$SS_{\text{marco}} = 2\,R_{\text{carril}} = {{ vt('nch2369-galpon-grua/07', 'SS_marco', 5) }}\ \text{kN} \qquad \frac{SS_{\text{marco}}}{SS_{\text{total}}} = {{ vt('nch2369-galpon-grua/07', 'frac_empuje', 5) }}$$

→ un solo marco recibe el **77,3 %** del empuje lateral de la grúa entera, porque las dos
carrileras entregan su reacción en el **mismo** marco: el puente es perpendicular a los rieles
y sus dos testeros están en la misma posición longitudinal. Repartir el empuje «entre las
cinco» daría 12 kN y sería falso por un factor 3,87.

### C2 · La deriva al nivel del riel, contra el límite de AIST

$$d_{\text{riel}} = \frac{SS_{\text{marco}}}{k_{\text{riel}}} = {{ vt('nch2369-galpon-grua/07', 'd_riel_grua', 5) }}\ \text{mm} \qquad \frac{d_{\text{riel}}}{d_{\text{lim}}^{\text{grúa}}} = {{ vt('nch2369-galpon-grua/07', 'uso_grua', 5) }}$$

→ **{{ v('nch2369-galpon-grua/07', 'd_riel_grua', 5) }} mm contra
{{ v('nch2369-galpon-grua/07', 'dlim_grua', 2) }}**, uso
{{ v('nch2369-galpon-grua/07', 'uso_grua', 5) }}. El límite que el 06 identificó como el que
manda —seis veces más estricto que §6.3— se cumple con el 84 % del margen libre.

### C3 · Y el arriostramiento de techo, que no se contó, dejaría otro factor 3,4

El arriostramiento continuo de techo que §12.1.2 obliga a poner liga los cinco aleros, y su
comentario dice para qué sirve con estas palabras: **«distribuir cargas laterales concentradas,
como las de grúas, entre varios marcos»**. La norma nombra exactamente el reparto que S4 se
niega a contar; esto mide cuánto vale negárselo.

$$d_{\text{riel}}^{\text{inf}} = {{ vt('nch2369-galpon-grua/07', 'd_riel_inf', 5) }}\ \text{mm} \qquad \frac{d_{\text{riel}}}{d_{\text{riel}}^{\text{inf}}} = {{ vt('nch2369-galpon-grua/07', 'redistrib', 5) }} \qquad \frac{d_{\text{riel}}^{\text{inf}}}{d_{\text{lim}}^{\text{grúa}}} = {{ vt('nch2369-galpon-grua/07', 'uso_inf', 5) }}$$

→ con el diafragma de techo infinitamente rígido la deriva del riel cae a
{{ v('nch2369-galpon-grua/07', 'd_riel_inf', 5) }} mm, un factor
{{ v('nch2369-galpon-grua/07', 'redistrib', 5) }}. La verdad está entre los dos usos, y **la
cota alta es la que se adopta**. Lo que decide dónde cae exactamente es la rigidez del
arriostramiento de techo, que es del eslabón 11.

### C4 · El criterio que el 06 llamó «el que manda» toleraría un marco 5,7 veces más flexible

$$k_Y^{\text{tol}} = k_Y \cdot \frac{d_{\text{riel}}}{d_{\text{lim}}^{\text{grúa}}} = {{ vt('nch2369-galpon-grua/07', 'k_tol', 5) }}\ \text{kN}/\text{m} \qquad \frac{k_Y^{\text{req}}}{k_Y^{\text{tol}}} = {{ vt('nch2369-galpon-grua/07', 'mas_flexible', 5) }}$$

→ el límite de servicio de la grúa se satisface con un marco de
{{ v('nch2369-galpon-grua/07', 'k_tol', 5) }} kN/m, y el período declarado en el 04 exige
{{ v('nch2369-galpon-grua/07', 'k_req_Y', 5) }}. El criterio de deriva más estricto de los dos
toleraría un marco **{{ v('nch2369-galpon-grua/07', 'mas_flexible', 5) }} veces más flexible**:
no dimensiona nada.

### C5 · La deriva sísmica rehecha

$$d_{Y2} = \frac{I\,f_\xi\,S_{aH}\,g\,T^{2}}{4\pi^{2}} = {{ vt('nch2369-galpon-grua/07', 'd_Y2', 5) }}\ \text{mm} \qquad \frac{d_{Y2}}{d_{\text{lim}}} = {{ vt('nch2369-galpon-grua/07', 'uso_63', 5) }} \qquad \frac{d_{Y2}}{d_{\text{lim}}^{\text{grúa}}} = {{ vt('nch2369-galpon-grua/07', 'sismo_sobre_grua', 5) }}$$

$$\frac{\text{uso del límite de la grúa}}{\text{uso del límite sísmico}} = {{ vt('nch2369-galpon-grua/07', 'razon_usos', 5) }}$$

→ el desplazamiento sísmico baja {{ v('nch2369-galpon-grua/07', 'bajo_vs_06', 5) }} al
rigidizar, hasta **{{ v('nch2369-galpon-grua/07', 'd_Y2', 5) }} mm**, y §6.3 queda en uso
{{ v('nch2369-galpon-grua/07', 'uso_63', 5) }}. Y ahí está el resultado que el 06 no podía ver:
**el límite seis veces más estricto se usa a {{ v('nch2369-galpon-grua/07', 'uso_grua', 5) }} y
el que su propio comentario declara inaplicable se usa a
{{ v('nch2369-galpon-grua/07', 'uso_63', 5) }}**. La estrictez del límite no dice nada sobre
cuál gobierna mientras no aparezca la demanda, y las dos demandas están en escalas distintas.
La consecuencia que el comentario de §6.1 obliga a informar sigue en pie —el sismo de diseño
deja la carrilera fuera de alineación por un factor
{{ v('nch2369-galpon-grua/07', 'sismo_sobre_grua', 5) }}— pero ya no es un criterio de
dimensionamiento.

### C6 · P-Δ sigue sin ser obligatorio

$$\theta_{Y2} = \frac{P\,d_{Y2}}{Q_0\,h} = {{ vt('nch2369-galpon-grua/07', 'theta_Y2', 5) }} \qquad \frac{1}{1 - \theta_{Y2}} = {{ vt('nch2369-galpon-grua/07', 'f_PDelta_Y2', 5) }} \qquad \frac{ {{ vt('nch2369-galpon-grua/07', 'f_PDelta_Y2', 5) }} }{ {{ vt('nch2369-galpon-grua/07', 'f_PDelta_Y', 5) }} } = {{ vt('nch2369-galpon-grua/07', 'bajo_PDelta', 5) }}$$

→ **no aplica**: el desplazamiento no excede el umbral de §6.3, que es el mismo de §6.4. El
amplificador indicativo baja a {{ v('nch2369-galpon-grua/07', 'f_PDelta_Y2', 5) }}, un 0,15 %,
porque el numerador y el denominador cambian casi lo mismo.

### C7 · Y hay un tercer criterio de servicio que nadie había leído: la trocha de la grúa

Un marco a dos aguas bajo carga gravitacional **se abre**: los dos aleros se separan y con
ellos los dos rieles. AIST lo acota en el mismo párrafo que la deriva, con un límite asimétrico
—abrir tolera el doble que cerrar— y con una **rebaja de la nieve reservada a esta
verificación**: 50 % si la nieve no pasa de 30 psf y 25 % si la pasa.

$$p_s = {{ vt('nch2369-galpon-grua/07', 'p_s_psf', 5) }}\ \text{psf} \qquad \frac{30\ \text{psf}}{p_s} = {{ vt('nch2369-galpon-grua/07', 'margen_30psf', 5) }}$$

$$\Delta_{\text{trocha}} = {{ vt('nch2369-galpon-grua/07', 'trocha_D', 5) }} + {{ vt('nch2369-galpon-grua/07', 'reb_50', 2) }} \cdot {{ vt('nch2369-galpon-grua/07', 'trocha_S', 5) }} = {{ vt('nch2369-galpon-grua/07', 'trocha_50', 5) }}\ \text{mm} \qquad \frac{\Delta_{\text{trocha}}}{\Delta_{\text{lim}}} = {{ vt('nch2369-galpon-grua/07', 'uso_trocha', 5) }}$$

$$\text{sin rebaja } {{ vt('nch2369-galpon-grua/07', 'trocha_sin', 5) }}\ \text{mm} \to {{ vt('nch2369-galpon-grua/07', 'uso_sin', 5) }} \qquad \text{con la del 25 } \% \ {{ vt('nch2369-galpon-grua/07', 'trocha_25', 5) }}\ \text{mm} \to {{ vt('nch2369-galpon-grua/07', 'uso_25', 5) }}$$

→ la trocha se abre {{ v('nch2369-galpon-grua/07', 'trocha_50', 5) }} mm contra el límite de
{{ v('nch2369-galpon-grua/07', 'trocha_lim', 2) }} mm, uso
**{{ v('nch2369-galpon-grua/07', 'uso_trocha', 5) }}**. La carga permanente sola abre
{{ v('nch2369-galpon-grua/07', 'trocha_D', 5) }} mm y la nieve balanceada, entera, otros
{{ v('nch2369-galpon-grua/07', 'trocha_S', 5) }}: **es la nieve la que gobierna esta
verificación**, y la rebaja del 50 % es lo que la hace holgada. Es el único número del eslabón
que depende de un umbral escrito en unidades imperiales.

## D · Cuál de las dos nieves del 02 gobierna el marco

### D1 · Las dos distribuciones, llevadas al marco

$$w_{\text{bal}} = {{ vt('nch2369-galpon-grua/07', 'w_bal', 5) }}\ \text{kN}/\text{m} \qquad w_{\text{bar}} = {{ vt('nch2369-galpon-grua/07', 'w_bar', 5) }}\ \text{kN}/\text{m} \qquad w_{\text{pico}} = {{ vt('nch2369-galpon-grua/07', 'w_pico', 5) }}\ \text{kN}/\text{m}$$

→ el faldón de sotavento lleva {{ v('nch2369-galpon-grua/07', 'w_pico', 5) }} kN/m en los
{{ v('nch2369-galpon-grua/07', 'L_ac', 5) }} m contiguos a la cumbrera y
{{ v('nch2369-galpon-grua/07', 'w_bal', 5) }} en los
{{ v('nch2369-galpon-grua/07', 'L_sin_ac', 5) }} m restantes; el de barlovento,
{{ v('nch2369-galpon-grua/07', 'w_bar', 5) }} parejos.

### D2 · La balanceada gobierna el nudo, y por 5,5 %

$$F_{\text{bal}} = {{ vt('nch2369-galpon-grua/07', 'F_bal', 5) }}\ \text{kN} \qquad F_{\text{desb}} = {{ vt('nch2369-galpon-grua/07', 'F_desb', 5) }}\ \text{kN} \qquad \frac{F_{\text{desb}}}{F_{\text{bal}}} = {{ vt('nch2369-galpon-grua/07', 'menos_pesa', 5) }}$$

$$\frac{M_{\text{nudo}}^{\text{bal}}}{M_{\text{nudo}}^{\text{desb}}} = \frac{ {{ vt('nch2369-galpon-grua/07', 'M_nudo_bal', 5) }} }{ {{ vt('nch2369-galpon-grua/07', 'M_nudo_des', 5) }} } = {{ vt('nch2369-galpon-grua/07', 'mas_momento', 5) }}$$

→ **gobierna la balanceada**, y por {{ v('nch2369-galpon-grua/07', 'mas_momento', 5) }} en el
momento del nudo. El 02 había dejado la pregunta abierta con el argumento correcto —la
desbalanceada pesa 24 % menos y aun así puede gobernar por asimetría— y la respuesta para
**este** marco es que no gobierna: la asimetría se descarga en desplazamiento lateral y no en
momento, porque las dos bases están empotradas. Con bases rotuladas el reparto sería otro.

### D3 · Y la desbalanceada es la única que desplaza el marco de lado

El desplazamiento lateral del marco es la **media** de los dos aleros: la parte simétrica es
apertura de trocha y no deriva. Bajo la balanceada esa media vale cero por simetría.

$$\frac{d_{\text{riel}}^{\text{desb}}}{d_{\text{riel}}^{\text{grúa}}} = \frac{ {{ vt('nch2369-galpon-grua/07', 'd_riel_des', 5) }} }{ {{ vt('nch2369-galpon-grua/07', 'd_riel_grua', 5) }} } = {{ vt('nch2369-galpon-grua/07', 'des_sobre_grua', 5) }} \qquad \frac{ {{ vt('nch2369-galpon-grua/07', 'd_alero_des', 5) }} }{ {{ vt('nch2369-galpon-grua/07', 'd_riel_des', 5) }} } = {{ vt('nch2369-galpon-grua/07', 'crece_riel_alero', 5) }}$$

→ la desbalanceada desplaza el riel {{ v('nch2369-galpon-grua/07', 'd_riel_des', 5) }} mm y el
alero {{ v('nch2369-galpon-grua/07', 'd_alero_des', 5) }}; la balanceada, **cero**. La que
pierde en flexión es la única que existe en deriva. Los dos estados hay que correrlos igual,
porque el que gobierna cada verificación es distinto.

## E · §8.7 a nivel de miembro, sobre un alma que varía

### E1 · Un alma en cuña no es una discontinuidad abrupta

$$\frac{d_{\text{base}} - d_{\text{nudo}}}{h} = {{ vt('nch2369-galpon-grua/07', 'conic_col', 5) }} \qquad \frac{d_{\text{nudo}} - d_{\text{cumb}}}{L_r} = {{ vt('nch2369-galpon-grua/07', 'conic_raf', 5) }}$$

→ la conicidad vale **1 en 35** en la columna y **1 en 39** en el rafter. La comparación que la
cláusula sí admite es la de la sección reducida de viga, que quita sección en 1 en 3 y
**tampoco** cuenta como abrupta; una cuña treinta y cinco veces más suave, menos.

### E2 · El alma de 8 mm que la tipología usaría no pasa la Tabla 9

$$\lambda_{md}^{\text{ala}} = {{ vt('nch2369-galpon-grua/07', 'c_ala', 2) }}\sqrt{\frac{E}{R_y F_y}} = {{ vt('nch2369-galpon-grua/07', 'lam_ala', 5) }} \qquad \frac{(b_f - t_w)/2}{t_f} \Big/ \lambda_{md}^{\text{ala}} = {{ vt('nch2369-galpon-grua/07', 'uso_ala_raf', 5) }}$$

$$C_a = {{ vt('nch2369-galpon-grua/07', 'Ca_raf', 5) }} \qquad \lambda_{md}^{\text{alma}} = {{ vt('nch2369-galpon-grua/07', 'lam_alma_raf', 5) }} \qquad \text{con } {{ vt('nch2369-galpon-grua/07', 'tw_raf', 0) }}\ \text{mm}: {{ vt('nch2369-galpon-grua/07', 'uso_alma_raf12', 5) }} \qquad \text{con } {{ vt('nch2369-galpon-grua/07', 'tw_raf_tip', 0) }}: {{ vt('nch2369-galpon-grua/07', 'uso_alma_raf8', 5) }}$$

→ con el alma de {{ v('nch2369-galpon-grua/07', 'tw_raf', 0) }} mm el uso es
{{ v('nch2369-galpon-grua/07', 'uso_alma_raf12', 5) }}; con la de
{{ v('nch2369-galpon-grua/07', 'tw_raf_tip', 0) }} mm que un rafter de esta luz llevaría
normalmente, **{{ v('nch2369-galpon-grua/07', 'uso_alma_raf8', 5) }}: no pasa**. El alma sube un
50 % de espesor por **ductilidad**, no por resistencia. Y la exención de §8.7.3 **no se toma**:
el rafter de un marco de un piso es el único fusible que el sistema tiene, y tomarla lo
convertiría en un elemento diseñado elásticamente.

### E3 · La columna no está obligada por NCh y sí por AISC 341

$$R_{\text{col}} = {{ vt('nch2369-galpon-grua/07', 'Rv_max', 5) }}\left(1 + \frac{ {{ vt('nch2369-galpon-grua/07', 's_marco', 2) }} - {{ vt('nch2369-galpon-grua/07', 'wb_ruedas', 2) }} }{ {{ vt('nch2369-galpon-grua/07', 's_marco', 2) }} }\right) = {{ vt('nch2369-galpon-grua/07', 'Rcol_grua', 5) }}\ \text{kN}$$

$$N_u^{\text{base}} = {{ vt('nch2369-galpon-grua/07', 'N_grav', 5) }} + {{ vt('nch2369-galpon-grua/07', 'Rcol_grua', 5) }} = {{ vt('nch2369-galpon-grua/07', 'Nbase_u', 5) }}\ \text{kN} \qquad C_a = {{ vt('nch2369-galpon-grua/07', 'Ca_col', 5) }} \qquad \lambda_{md}^{\text{alma}} = {{ vt('nch2369-galpon-grua/07', 'lam_alma_col', 5) }}$$

$$\text{con } {{ vt('nch2369-galpon-grua/07', 'tw_col', 0) }}\ \text{mm}: {{ vt('nch2369-galpon-grua/07', 'uso_alma_col14', 5) }} \qquad V_u = {{ vt('nch2369-galpon-grua/07', 'Vu_col', 5) }}\ \text{kN} \qquad \phi V_n = {{ vt('nch2369-galpon-grua/07', 'phiVn_base', 5) }}\ \text{kN} \qquad {{ vt('nch2369-galpon-grua/07', 'uso_corte', 5) }}$$

→ el alma de la columna sube de {{ v('nch2369-galpon-grua/07', 'tw_col_tip', 0) }} a
**{{ v('nch2369-galpon-grua/07', 'tw_col', 0) }} mm** y queda en uso
{{ v('nch2369-galpon-grua/07', 'uso_alma_col14', 5) }} contra la Tabla 9. Y el corte que esa
misma alma tiene que resistir la usa en **{{ v('nch2369-galpon-grua/07', 'uso_corte', 5) }}**:
el espesor lo pone la ductilidad y lo paga la plancha, veinticinco veces por encima de lo que
la resistencia pide. **La sismorresistencia de esta norma se cobra en dimensiones que la
estática no explica.**

### E4 · Columna fuerte-viga débil pasa por 2,7 %, y contarle la grúa lo voltearía

$$M_{pe}^{\text{col}} = {{ vt('nch2369-galpon-grua/07', 'Mpe_col', 5) }}\ \text{kN}\cdot\text{m} \qquad M_{pe}^{\text{raf}} = {{ vt('nch2369-galpon-grua/07', 'Mpe_raf', 5) }}\ \text{kN}\cdot\text{m} \qquad P_{ye} = {{ vt('nch2369-galpon-grua/07', 'Pye_col', 5) }}\ \text{kN}$$

$$M_{pc}^{*} = {{ vt('nch2369-galpon-grua/07', 'Mpc_red', 5) }}\ \text{kN}\cdot\text{m} \qquad {{ vt('nch2369-galpon-grua/07', 'c_scwb', 2) }}\,M_{pe}^{\text{raf}} = {{ vt('nch2369-galpon-grua/07', 'dem_874', 5) }}\ \text{kN}\cdot\text{m} \qquad {{ vt('nch2369-galpon-grua/07', 'uso_874', 5) }}$$

→ **se cumple**, por 2,7 %, y solo porque el nudo es a inglete y la columna lleva alas más
gruesas que el rafter en la misma altura. Y el número frágil no es el margen sino **cuál axial
entra**: contarle la reacción de la grúa, que se descarga
{{ v('nch2369-galpon-grua/07', 'h_riel', 2) }} m más abajo, lo lleva a
{{ v('nch2369-galpon-grua/07', 'uso_874_grua', 5) }}.

### E5 · Las dos normas lo dejan pasar por puertas distintas

$$0{,}30\,P_{yc} = {{ vt('nch2369-galpon-grua/07', 'umbral_aisc', 5) }}\ \text{kN} \qquad \frac{N^{\text{nudo}}}{0{,}30\,P_{yc}} = {{ vt('nch2369-galpon-grua/07', 'usa_umbral', 5) }}$$

→ el axial de la columna en el nudo es el **10,5 %** del umbral, así que la excepción de AISC
aplica con holgura y el criterio no obliga bajo ninguna de las dos normas. Las dos puertas
dicen cosas distintas: NCh dice que el amplificador ya protege a la columna, AISC dice que en
un edificio de un piso el mecanismo de piso blando que la ecuación previene **no existe**,
porque no hay un piso de arriba que quede colgando.

### E6 · El arriostramiento lateral, y por qué la sección variable no cambia la separación

$$L_b = \frac{ {{ vt('nch2369-galpon-grua/07', 'c_Lb', 2) }}\,r_y\,E}{R_y F_y} = {{ vt('nch2369-galpon-grua/07', 'Lb_raf', 2) }}\ \text{mm} \qquad \frac{L_r}{L_b} = {{ vt('nch2369-galpon-grua/07', 'caben_Lb', 5) }} \qquad b_{\text{pan}} = {{ vt('nch2369-galpon-grua/07', 'b_pan', 2) }}\ \text{mm}$$

$$\frac{r_y^{\text{cumb}}}{r_y^{\text{nudo}}} = {{ vt('nch2369-galpon-grua/07', 'crece_ry', 5) }} \qquad P_{br} = \frac{ {{ vt('nch2369-galpon-grua/07', 'Pbr_mom', 5) }} }{h_o} = {{ vt('nch2369-galpon-grua/07', 'Pbr_raf', 5) }}\ \text{kN} \qquad \frac{P_{br}}{P_{br}^{\text{AISC}}} = {{ vt('nch2369-galpon-grua/07', 'razon_lecturas', 5) }}$$

→ **tres espacios de {{ v('nch2369-galpon-grua/07', 'b_pan', 2) }} mm por agua**, o sea dos
tirantes intermedios al ala interior por faldón. La separación la fija el extremo **profundo** y
no el delgado, que es contraintuitivo: $r_y$ crece un
{{ v('nch2369-galpon-grua/07', 'crece_ry', 5) }} hacia la cumbrera porque las alas no cambian y
el área sí, así que el $r_y$ mínimo está en el nudo. Los dos máximos coinciden ahí: **la
separación más corta y la fuerza de arriostramiento más grande caen en la misma sección**. Y la
razón exacta {{ v('nch2369-galpon-grua/07', 'razon_lecturas', 5) }} contra la lectura de AISC
respalda que la cláusula chilena escribe un momento donde AISC escribe una fuerza.

## F · El vertical del techo, y las resistencias

### F1 · El período vertical cae fuera de la ventana que el 06 dejó abierta

$$T_V = 2\pi\sqrt{\frac{\delta_{\text{cumb}}}{g}} = {{ vt('nch2369-galpon-grua/07', 'T_V', 5) }}\ \text{s} \qquad \frac{T_V}{T_{\text{fin}}} = {{ vt('nch2369-galpon-grua/07', 'pasa_ventana', 5) }} \qquad S_{aV}(T_V) = {{ vt('nch2369-galpon-grua/07', 'SaV_dis', 5) }}\ \text{g} \qquad \frac{S_{aV}}{C_V} = {{ vt('nch2369-galpon-grua/07', 'modal_vs_est', 5) }}$$

→ **{{ v('nch2369-galpon-grua/07', 'T_V', 5) }} s**, un 25 % pasado el fin de la ventana. El
techo **sí** es verticalmente flexible y correr la ruta modal daría 7,0 % menos demanda vertical
que el coeficiente estático. Se mantiene la estática, que es la conservadora: la elección de
ruta no cambia ninguna sección, y la que no se tomó es la que habría aliviado.

### F2 · Y las resistencias

$$\phi M_n^{\text{raf}} = {{ vt('nch2369-galpon-grua/07', 'phiMn_raf', 5) }}\ \text{kN}\cdot\text{m} \to {{ vt('nch2369-galpon-grua/07', 'uso_raf', 5) }} \qquad \phi M_n^{\text{base}} = {{ vt('nch2369-galpon-grua/07', 'phiMn_base', 5) }} \to {{ vt('nch2369-galpon-grua/07', 'uso_base', 5) }}$$

$$\phi M_n^{\text{nudo}} = {{ vt('nch2369-galpon-grua/07', 'phiMn_nudo', 5) }} \to {{ vt('nch2369-galpon-grua/07', 'uso_nudo', 5) }} \qquad \phi M_n^{\text{cumb}} = {{ vt('nch2369-galpon-grua/07', 'phiMn_cumb', 5) }} \to {{ vt('nch2369-galpon-grua/07', 'uso_cumb', 5) }}$$

→ el uso mayor del marco en flexión es **{{ v('nch2369-galpon-grua/07', 'uso_raf', 5) }}**, en
el rafter junto al nudo y bajo gravedad; la base de la columna, que es la sección crítica bajo
sismo con {{ v('nch2369-galpon-grua/07', 'Mbase_u', 5) }} kN·m, usa
{{ v('nch2369-galpon-grua/07', 'uso_base', 5) }}. Ninguna sección está gobernada por
resistencia: **el marco entero está dimensionado por la rigidez de A1**, y esos usos son la
medida de cuánto se paga por ella.

## Sobre el modelo: las dos convenciones de rigidez que el memo mezcla

Hasta aquí el eslabón reproduce el memo. Lo que sigue es lo que el sitio agrega, y no cambia
ninguna cifra de arriba: correr el marco y mirar de qué caso de carga salen los tres números
que S1 declara.

El modelo plano de rigidez directa del repositorio —el del caso 11, con 84 tramos por columna—
reobtiene la rigidez del alero con **un empuje en un solo alero**, y así sale 5 612,22 kN/m, que
es la $k_Y$ que este eslabón publica. Con los **dos** aleros empujados a la vez —que es lo que
un modo de traslación hace— sale 6 152,89, un 9,6 % más. Y la $k_{\text{riel}}$ que el mismo
memo publica, 15 057,34, **solo** se reobtiene con los dos rieles: con uno solo daría 12 055,64.

Son **dos convenciones distintas en el mismo memo**, y la del alero no es una rigidez lateral:
incluye la parte antisimétrica —el marco abriéndose— que ningún modo de traslación tiene. Es la
misma distinción que D3 hace entre deriva y trocha, aplicada a la rigidez y no al
desplazamiento. La razón $M_{\text{base}}/M_{\text{nudo}}$ y el punto de inflexión heredan la
convención del alero: con el sway valdrían 3,64 y 8,24 m en vez de
{{ v('nch2369-galpon-grua/07', 'razon_sway', 5) }} y
{{ v('nch2369-galpon-grua/07', 'y_infl', 5) }}.

<rukan-visor src="../../../modelos/galpon-grua/galpon-grua.escena.json" caso="H_alero_uno" vista="transversal"></rukan-visor>

Arriba, el empuje en un solo alero sobre el galpón entero. Debajo, el momento a lo largo de las
dos columnas del marco central bajo el *sway* de los diez aleros: la ordenada cruza el cero en
el punto de inflexión, y **ahí está la diferencia que el modelo tridimensional agrega**.

<rukan-visor src="../../../modelos/galpon-grua/galpon-grua.escena.json" caso="H_alero" esfuerzo="Mz" filtro="COL3A_*,COL3B_*" vista="transversal"></rukan-visor>

En el galpón de la serie la columna es **escalonada** —la del eslabón 10, con la sección
compuesta bajo el asiento de la carrilera— y los cinco marcos están ligados por el techo
arriostrado. Bajo el sway, el momento en la base de una columna del marco central vale
{{ r('galpon-grua', 'Mz_base_sway', 2) }} kN·m y en el nudo
{{ r('galpon-grua', 'Mz_nudo_sway', 2) }}: la razón entre los dos no es
{{ v('nch2369-galpon-grua/07', 'razon_sway', 5) }} ni 3,64 sino cerca de 8, porque una base
mucho más rígida atrae mucho más momento. El punto de inflexión sube con ella. Ninguna de esas
tres cifras es un error de la otra: son tres estructuras distintas —un marco plano empujado en
un alero, el mismo empujado en dos, y un galpón de cinco marcos con la columna del 10—, y el
mérito de tenerlas juntas es que la diferencia deja de ser invisible.

## Veredicto

**El marco cierra, y lo que lo dimensiona no es ninguna de las dos derivas.** La columna de alma
variable y el rafter entregan {{ v('nch2369-galpon-grua/07', 'k_Y', 5) }} kN/m, un
{{ v('nch2369-galpon-grua/07', 'margen_k', 5) }} sobre lo que el período declarado en el 04 y la
masa fijada en el 05 implican juntos. Ése es el criterio que manda: **el período era un
requisito de rigidez y nadie lo había presentado como tal.**

El 06 entregó el límite de servicio de la grúa y lo llamó el que manda. Con la demanda adentro
se invierte: a un marco le llegan {{ v('nch2369-galpon-grua/07', 'SS_marco', 5) }} kN de empuje
lateral y el límite queda en uso {{ v('nch2369-galpon-grua/07', 'uso_grua', 5) }}, contra
{{ v('nch2369-galpon-grua/07', 'uso_63', 5) }} del sísmico, que la propia norma declara
inaplicable a equipos. Lo que sí queda en pie del 06 es la obligación de informar.

**Rigidizar no costó nada.** La ordenada sube 0,87 %, el corte del análisis sube con ella y el
de diseño **no se mueve**, porque el techo de §5.13 se arma sin el período adentro.

Tres cosas que la tipología habría hecho al revés. La **conicidad** corre hacia abajo. El
**alma** de los dos miembros sube por la Tabla 9 y no por corte, que la usa en
{{ v('nch2369-galpon-grua/07', 'uso_corte', 5) }}. Y **columna fuerte-viga débil** pasa por
2,7 %, con la advertencia de que el axial que entra es el del nudo y no el de la base:
{{ v('nch2369-galpon-grua/07', 'Nbase_u', 5) }} kN con la grúa contra
{{ v('nch2369-galpon-grua/07', 'N_grav', 5) }} sin ella.

De la nieve del 02 gobierna la **balanceada** —y también en un criterio que ningún eslabón había
leído: la variación de trocha de la grúa bajo gravedad, uso
{{ v('nch2369-galpon-grua/07', 'uso_trocha', 5) }}—. La desbalanceada, en cambio, es la única
que desplaza el marco de lado.

## Límites

- **El marco no se resuelve dentro del eslabón.** Las dos rigideces laterales, la rigidez
  vertical y todos los momentos de barra son resultados de un modelo de rigidez directa que el
  memo describe y no ejecuta, y que acá entran como datos. La sección «Sobre el modelo» los
  contrasta, que es cosa distinta de producirlos.
- **Tres filas del `## Resumen` del memo no reproducen, y el hallazgo es del memo.** En
  $Q_0^{\text{an}}(T_\alpha)$ el memo imprime una ordenada y multiplica por otra, una unidad más
  en el último dígito; la fila del corte y la de cuánto supera al techo heredan esa diferencia.
  En el uso del alma de columna con {{ v('nch2369-galpon-grua/07', 'tw_col_tip', 0) }} mm pasa
  lo mismo con el $C_a$. Acá se usa **la cifra impresa**, que es la correcta y la que la regla
  de la serie manda sustituir, y las tres filas quedan fuera del oráculo. El arnés del memo las
  dejaba pasar porque comparaba con tolerancia relativa.
- **Lo que sale de la nieve desbalanceada es sensible a la malla, y lo demás no.** La
  distribución del 02 tiene un salto de intensidad, y el modelo declarado lo muestrea por
  elemento mientras el arnés del memo lo integra exacto: las dos formulaciones coinciden dentro
  del 0,01 % en todo salvo en los estados desbalanceados, donde difieren 1 % en el momento de
  nudo y 5 % en la deriva. Ese 5 % es de origen aritmético: la deriva por nieve es la **media de
  dos desplazamientos cinco veces mayores y de signo contrario**, así que hereda su error
  amplificado.
- **La zona panel y la conexión de momento no se verifican.** §8.7.5 pide diseñar la conexión
  para la capacidad esperada en flexión de la viga y §8.7.6 obliga a atiesadores de continuidad.
  Con {{ v('nch2369-galpon-grua/07', 'Mpe_raf', 5) }} kN·m sobre un alma de columna de
  {{ v('nch2369-galpon-grua/07', 'tw_col', 0) }} mm, el comentario anticipa que el alma no
  resistirá el corte del nudo. Acá no tiene eslabón asignado.
- **La ménsula y su excentricidad son del 10.** Este eslabón mete la reacción vertical de la
  grúa en la columna como un axial **concéntrico** de
  {{ v('nch2369-galpon-grua/07', 'Rcol_grua', 5) }} kN.
- **El empuje lateral no se redistribuye entre marcos.** C3 acota lo que eso vale, un factor
  {{ v('nch2369-galpon-grua/07', 'redistrib', 5) }}. Dónde cae exactamente lo decide el 11.
- **La carrilera se supone simplemente apoyada por vano.** Con carrilera continua la reacción de
  un apoyo interior sube, y el 08 puede cambiar el
  {{ v('nch2369-galpon-grua/07', 'R_carril', 5) }} kN que C1 usa.
- **No se verifica pandeo lateral-torsional del rafter ni interacción axial-flexión.** F2 compara
  momento contra la plastificación de la sección. El tratamiento riguroso de un miembro de
  altura variable está en el Apéndice 6 de AISC 360 y en la Design Guide 25, y ninguno de los
  dos está en el corpus.
- **El $C_a$ de la Tabla 9 usa el axial de una combinación y no el envolvente.** Con el axial de
  la combinación que comprime del 06 el $\lambda_{md}$ del alma de la columna bajaría y el uso de
  {{ v('nch2369-galpon-grua/07', 'uso_alma_col14', 5) }} se acercaría a 1. El margen es de 3,6 %
  y es el número más frágil del eslabón.
- **La exención de §8.7.3 no se toma y eso es una decisión.** Con ella el rafter podría llevar
  {{ v('nch2369-galpon-grua/07', 'tw_raf_tip', 0) }} mm y ahorrar el 33 % del alma. Se rechaza
  porque en un marco de un piso el rafter es el único fusible del sistema.
- **El período vertical es una estimación de Rayleigh sobre un modo supuesto.** Un techo con
  costaneras flexibles vibrando entre marcos tiene modos locales más altos que este número no
  ve, y el comentario de §5.7.1 habla de la flexibilidad de los **componentes**.
- **No se verifican los estados de servicio de gravedad.** NCh2369 no fija límite de flecha de
  techo y NCh1537 no está en el corpus.

## Ficha

{{ ficha('nch2369-galpon-grua/07') }}

## Referencias

| Clave | Norma y edición | Cláusula | Leída en | Cita textual |
|---|---|---|---|---|
| NCh-p1 | NCh2369:2025 (3.ª ed.) | §8.7.1, que las uniones de momento deben ser totalmente rígidas | `Normas/NCh 2369 - 3°Edición 2025.05.28.pdf`, p. 99 | «Las uniones de momento de marcos resistentes a momento sismorresistentes deben ser del tipo totalmente rígidas» |
| NCh-p2 | NCh2369:2025 (3.ª ed.) | §8.7.2, la prohibición de discontinuidades geométricas abruptas en la zona de rótula | PDF ídem, p. 99 | «No se permiten discontinuidades geométricas abruptas en las potenciales zonas de formación de rótulas plásticas en la viga» |
| NCh-p2b | NCh2369:2025 (3.ª ed.) | C8.7.2, que la reducción de sección de AISC 358 tampoco cuenta como abrupta | PDF ídem, p. 99 | «no se considera como una discontinuidad geométrica abrupta» |
| NCh-p3 | NCh2369:2025 (3.ª ed.) | §8.7.3, la Tabla 9 para las vigas de MRM | PDF ídem, p. 99 | «Las secciones transversales de vigas de marcos resistentes a momento sismorresistentes deben contar con razones ancho/espesor» |
| NCh-p3b | NCh2369:2025 (3.ª ed.) | §8.7.3, la exención por $0{,}7R_1 \ge 1{,}0$ que E2 decide no tomar | PDF ídem, p. 99 | «Se pueden exceptuar de esta exigencia aquellos elementos en que la resistencia requerida para todos los esfuerzos sea determinada» |
| NCh-p4 | NCh2369:2025 (3.ª ed.) | §8.7.4, la recomendación de columna fuerte-viga débil y **su alcance a estructuras de varios niveles** | PDF ídem, p. 100 | «En estructuras de varios niveles, se recomienda que la suma de las capacidades flexurales esperadas reducidas por carga axial» |
| NCh-p5 | NCh2369:2025 (3.ª ed.) | C8.7.4, por qué dejó de ser obligatorio= el $0{,}7R_1$ ya protege a toda columna | PDF ídem, p. 100 | «el requisito tradicional se hace innecesario desde un punto de vista obligatorio» |
| NCh-p5b | NCh2369:2025 (3.ª ed.) | C8.7.4, la sugerencia que sí queda en pie | PDF ídem, p. 100 | «se sugiere que una potencial plastificación del sistema sea estable» |
| NCh-p6 | NCh2369:2025 (3.ª ed.) | §8.7.7, la separación máxima entre arriostramientos laterales de vigas de MRM | PDF ídem, p. 102 | «Los arriostramientos deben estar separados a una distancia no mayor a» |
| NCh-p6b | NCh2369:2025 (3.ª ed.) | §8.7.7, la resistencia requerida del arriostramiento lateral | PDF ídem, p. 102 | «La resistencia requerida de los arriostramientos laterales debe ser de» |
| NCh-p7 | NCh2369:2025 (3.ª ed.) | §8.7.7, la rigidez requerida, que remite al Anexo 6 de NCh427/1 | PDF ídem, p. 102 | «La rigidez requerida de los arriostramientos laterales debe cumplir los requisitos de NCh427/1» |
| NCh-p8 | NCh2369:2025 (3.ª ed.) | Tabla 9, la fila del ala de perfiles I y H soldados, con su $0{,}40\sqrt{E/(R_yF_y)}$ — **mirada en PNG**, no extraída | PDF ídem, p. 104 | «Alas de perfiles soldados o laminados tipos I, H» |
| NCh-p8b | NCh2369:2025 (3.ª ed.) | Tabla 9, la fila del alma en flexo-compresión con las dos ramas de $C_a$ — **mirada en PNG**, no extraída | PDF ídem, p. 106 | «Almas de perfiles soldados, laminados o plegados en frío tipos I, H o C» |
| NCh-p9 | NCh2369:2025 (3.ª ed.) | §8.3.1, las capacidades esperadas $M_{pe} = R_y F_y Z$ y $T_{ye} = R_y F_y A_g$ | PDF ídem, p. 86 | «Capacidad flexural esperada» |
| NCh-p10 | NCh2369:2025 (3.ª ed.) | §5.13 y la Ec. (13), el techo del corte basal que no lleva el período adentro | PDF ídem, p. 56 | «Esta reducción no se debe aplicar al cálculo de desplazamientos» |
| NCh-p11 | NCh2369:2025 (3.ª ed.) | C5.7.1, la recomendación de análisis dinámico si la flexibilidad vertical importa | PDF ídem, p. 42 | «es preferible hacer análisis dinámico considerando los requisitos de 5.7.2» |
| NCh-p12 | NCh2369:2025 (3.ª ed.) | C6.1, la obligación de informar cuando el desplazamiento relativo afecta la operación del equipo | PDF ídem, p. 75 | «las condiciones se deben informar, indicando las consecuencias directas causadas por el desplazamiento relativo» |
| NCh-p13 | NCh2369:2025 (3.ª ed.) | §12.1.2, el arriostramiento continuo de techo obligatorio en edificios con marcos transversales | PDF ídem, p. 150 | «Los edificios con marcos transversales deben tener un sistema de arriostramiento continuo en el techo» |
| NCh-p14 | NCh2369:2025 (3.ª ed.) | C12.1.2, que ese arriostramiento reparte las cargas de grúa entre varios marcos | PDF ídem, p. 150 | «distribuir cargas laterales concentradas, como las de grúas, entre varios marcos» |
| AIST-1 | AIST TR-13:2021 | §5.3, la deriva del marco al nivel de las carrileras, $1/400$ o 2 in, el menor | `Normas/aist-tr-no13-2021-3.pdf`, p. 29 | «shall be no greater than 1/400 of the height from column base or 2 in., whichever is less» |
| AIST-2 | AIST TR-13:2021 | §5.3, el reparto del empuje transversal entre columnas según rigidez relativa, que es lo que C1 hace | PDF ídem, p. 29 | «shall be distributed between crane runway support columns based upon an overall analysis of the system, accounting for relative stiffness» |
| AIST-2b | AIST TR-13:2021 | §3.7.2, el mismo reparto en la cláusula que genera la fuerza | PDF ídem, p. 19 | «The total side thrust should be distributed with due regard for the lateral stiffness of each structure supporting the rails» |
| AIST-3 | AIST TR-13:2021 | §5.3, que el límite de deriva sólo se puede exceder demostrando que no afecta la operación | PDF ídem, p. 29 | «These drift limits may be exceeded only when it can be shown that the total drift will not adversely affect the durability of the building and the operation of equipment» |
| AIST-3b | AIST TR-13:2021 | §5.3, la variación de trocha bajo gravedad, sus dos límites asimétricos y la rebaja de nieve que C7 usa | PDF ídem, p. 29 | «the variation of crane rail gauge due to gravity loads shall be within +1 in. and –1/2 in. of the specified gauge» |
| AIST-3c | AIST TR-13:2021 | §5.3, el umbral de 30 psf que separa las dos rebajas | PDF ídem, p. 29 | «Snow loads of 30 psf or less may be reduced by 50%» |
| AIST-4 | AIST TR-13:2021 | §3.11.2.1, las combinaciones que llevan la carga de grúa junto a la nieve | PDF ídem, p. 23 | «1.2D+1.2Cdm+1.0E+Cvs+L+0.2S» |
| NCh431-1 | NCh431:2010 | §8.2, la carga sin balancear en las dos zonas y su extensión desde la cumbrera — **PDF escaneado, leído a ojo** | `Normas/nch-431-2010.pdf`, p. 16 | «Para el resto de los techos triangulares, la carga sin balancear debe ser considerada 0,3 x ps en la zona de barlovento» |
| AISC341-1 | ANSI/AISC 341-22 | §A3.1, el techo de 345 MPa al $F_y$ especificado de un miembro con incursión inelástica | `referencias/AISC341-22/capA-requisitos-generales.md` | — |
| AISC341-2 | ANSI/AISC 341-22 | Tabla A3.2, $R_y = 1{,}1$ y $R_t = 1{,}2$ para plancha ASTM A572 Gr. 50 | `referencias/AISC341-22/capA-requisitos-generales.md` | — |
| AISC341-3 | ANSI/AISC 341-22 | §E3.4a y Ecs. E3-1 a E3-4= columna fuerte-viga débil obligatoria y la excepción (a)(1) del edificio de un piso | `referencias/AISC341-22/capE3-marcos-momento-especiales.md` | — |
| AISC341-4 | ANSI/AISC 341-22 | §E3.5a, las columnas de un SMF como miembros altamente dúctiles | `referencias/AISC341-22/capE3-marcos-momento-especiales.md` | — |
| AISC341-5 | ANSI/AISC 341-22 | §D1.2a, la resistencia requerida $0{,}02\,M_r/h_o$ del arriostramiento lateral de vigas | `referencias/AISC341-22/capD-miembros-y-conexiones.md` | — |
| AISC360-1 | ANSI/AISC 360-22 | §B4, las propiedades de sección de un perfil I soldado | `referencias/AISC360-22/capB-requisitos-de-diseno.md` | — |
| AISC360-2 | ANSI/AISC 360-22 | §F2 y §F4, la capacidad flexural y el momento plástico $M_p = F_y Z$ | `referencias/AISC360-22/capF-flexion.md` | — |
| AISC360-3 | ANSI/AISC 360-22 | §G2.1, la resistencia de corte del alma de un perfil soldado | `referencias/AISC360-22/capG-corte.md` | — |
| NCh-8 | NCh2369:2025 (3.ª ed.) | §8.3.4 y §8.4.1; §8.7.5 y §8.7.6 con C8.7.5 y C8.7.6 | `referencias/NCh2369-2025/cap08-estructuras-de-acero.md` | — |
| NCh-5 | NCh2369:2025 (3.ª ed.) | §5.4 y Ecs. (1a), (1b), (2), (3) y (4); §5.7.1 y §5.7.2; §5.12 a §5.14 | `referencias/NCh2369-2025/cap05-analisis-sismico.md` | — |
| NCh-6 | NCh2369:2025 (3.ª ed.) | §6.1, §6.3 y §6.4 con C6.1 y C6.4 | `referencias/NCh2369-2025/cap06-07-desplazamientos-y-equipos.md` | — |
| NCh-12 | NCh2369:2025 (3.ª ed.) | §12.1.3 a §12.1.5, los otros requisitos del galpón con puente grúa | `referencias/NCh2369-2025/cap12-estructuras-especificas.md` | — |
| N3171-w | NCh3171:2017 | §9.1.1, las combinaciones mayoradas con nieve y sobrecarga de grúa | `referencias/NCh3171-2017/cap09-combinaciones-de-carga.md` | — |
