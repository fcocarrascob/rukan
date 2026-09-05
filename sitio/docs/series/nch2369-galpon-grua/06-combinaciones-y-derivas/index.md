# 06 · Combinaciones y derivas

La componente vertical supera en **1,81** al corte horizontal de diseño que §5.13 acababa de
recortar, y el desplazamiento se calcula como si el corte fuera **R+1 veces mayor**. Acá se
arma el estado sísmico direccionalmente combinado, se escriben las combinaciones de §4.5.1 y
se verifica §6.3 y §6.4. Fuerzas en kN, desplazamientos en mm.

## El caso

{{ figura('nch2369-galpon-grua/06', 'vertical', 'Espectro de diseño vertical de la Ec. 2 contra el período vertical, con su pico de 0,53108 g en 0,20314 s, la recta del coeficiente estático de 0,52920 de §5.7.1 y la ventana angosta entre 0,19051 y 0,21632 s donde la ruta modal lo supera') }}

| Dato | Valor |
|---|---|
| Estructura | galpón de acero de una nave, un piso, cubierta a dos aguas (del 01) |
| Dirección **X** | longitudinal, arriostrada en 2 de los 4 vanos, los **extremos** (del 01) |
| Dirección **Y** | transversal, marco de momento de 25,00 m (del 01) |
| Altura libre de columna | {{ v('nch2369-galpon-grua/06', 'h_libre', 2) }} m (del 01) |
| Nivel superior del riel | {{ v('nch2369-galpon-grua/06', 'h_riel', 2) }} m (del 01) |
| Zona y suelo | 2 y C · $I = {{ vt('nch2369-galpon-grua/06', 'I', 2) }}$ · Categoría II (del 01, del 04) |
| Método | ASD y LRFD en paralelo; el diseño de acero va en LRFD |
| Cubierta y aislación | {{ v('nch2369-galpon-grua/06', 'g_cubierta', 2) }} kN/m² (del 05) |
| Revestimiento de muros y frontones | {{ v('nch2369-galpon-grua/06', 'g_muros', 2) }} kN/m² (del 05) |
| Peso propio de columnas | {{ v('nch2369-galpon-grua/06', 'w_columna', 2) }} kN/m, {{ v('nch2369-galpon-grua/06', 'n_columnas', 0) }} de {{ v('nch2369-galpon-grua/06', 'h_libre', 2) }} m (del 05) |
| Vigas carrileras con sus ménsulas | {{ v('nch2369-galpon-grua/06', 'w_carrilera', 2) }} kN/m, {{ v('nch2369-galpon-grua/06', 'L_carrilera', 2) }} m en total (del 05) |
| Estructura soportante del techo | {{ v('nch2369-galpon-grua/06', 'g_techo', 5) }} kN/m² (del 05) |
| Equipos colgados | {{ v('nch2369-galpon-grua/06', 'P_eq', 2) }} kN por marco, {{ v('nch2369-galpon-grua/06', 'n_marcos', 0) }} marcos (del 05) |
| Amortiguamiento vertical | $\xi_V = {{ vt('nch2369-galpon-grua/06', 'xi_V', 2) }}$ y $R_V = {{ vt('nch2369-galpon-grua/06', 'R_V', 2) }}$, fijos por §5.4 |
| Lo que se decide aquí | la componente vertical, las combinaciones, la deriva y si P-Δ aplica |

Los supuestos, en una línea cada uno. **S1**, el galpón se trata como un **oscilador de un
grado de libertad por dirección**: la masa está en el nivel de techo y el desplazamiento del
alero es el desplazamiento espectral del período declarado en el 04; es lo que permite que la
deriva no sea un número declarado sino una consecuencia de $T^{*}$, y E3 lo comprueba por el
otro camino. **S2**, el peso que genera inercia vertical se toma igual al peso sísmico
horizontal, repartido por componente en las posiciones que C5.7.1 pide; la cláusula advierte
que los dos no tienen por qué coincidir «en cantidad y posición», y con una grúa sobre rieles
esa advertencia es literal. **S3**, se adopta la ruta estática de §5.7.1, que es la que la
cláusula escribe sin condiciones; B5 y B6 miden cuánto decide esa elección, y la respuesta es
que casi nada. **S4**, el peso de la grúa entra como carga permanente en las combinaciones de
§4.5.1, con la grúa sin carga y estacionada en la posición más desfavorable que §12.1.4 exige.
**S5**, $SO = 0$ y $SA = 0$, y el segundo con reserva: C4.5.1 nombra como carga accidental los
«frenajes e impactos por movimientos derivados del sismo», que en un galpón con puente grúa
**no son cero**, y el candidato —el impacto contra el tope— no lo ha calculado ningún eslabón
de la serie. **S6**, el coeficiente de estabilidad $\theta = P\,d/(V\,h)$ no lo da NCh2369:
§6.4 dice *cuándo* considerar P-Δ y no *cómo*, así que se usa como indicador y no como
criterio de aceptación. **S7**, la altura $h$ de §6.3 es la altura libre de columna y el
desplazamiento se mide en el alero; tomar la cumbrera daría un límite 24 % más generoso sobre
un desplazamiento que no está ahí. **S8**, el centro de gravedad de la grúa no está declarado,
así que F2 entrega el umbral sobre el cual §12.1.5 obligaría a dispositivos anticaída, no una
verificación.

## A · Las dos escalas de este eslabón

### A1 · El coeficiente de diseño se reobtiene de los dos números que el 05 publica

El corte basal es el coeficiente sísmico por el peso sobre el nivel basal, y el 05 dejó los
dos cortes de diseño idénticos porque la Ec. (13) usa el $R$ de tabla.

$$\frac{Q_0^{\text{dis}}}{P} = \frac{ {{ vt('nch2369-galpon-grua/06', 'Q0_Y', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'P_sismico', 5) }} } = {{ vt('nch2369-galpon-grua/06', 'C_dis_re', 5) }}$$

→ **$E_x = E_y = {{ vt('nch2369-galpon-grua/06', 'Q0_X', 5) }}$ kN**, y el cociente devuelve el
coeficiente que el 05 publicó, así que los tres números heredados cierran entre sí. Son los
estados **desacoplados**: ninguno de los dos es todavía el $E$ que entra a una combinación.

### A2 · El recorte de §5.13 no toca los desplazamientos, y el factor entre las dos escalas es R+1

§5.13 permite multiplicar todas las fuerzas por el cociente $Q_0^{\text{máx}}/Q_0$, y agrega
que **«esta reducción no se debe aplicar al cálculo de desplazamientos»**. §6.1, a su vez,
estima los desplazamientos con el espectro **elástico de referencia**, corregido por
amortiguamiento y ponderado por $I$, sin dividir por $R^{*}$.

$$V_{\text{desp}} = I\,f_\xi\,S_{aH}(T^{*}_Y)\,P = {{ vt('nch2369-galpon-grua/06', 'I', 2) }} \cdot {{ vt('nch2369-galpon-grua/06', 'f_xi', 5) }} \cdot {{ vt('nch2369-galpon-grua/06', 'Sa_ref_Y', 5) }} \cdot {{ vt('nch2369-galpon-grua/06', 'P_sismico', 5) }} = {{ vt('nch2369-galpon-grua/06', 'V_desp', 5) }}\ \text{kN}$$

$$\frac{ {{ vt('nch2369-galpon-grua/06', 'V_desp', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'Q0_Y', 5) }} } = {{ vt('nch2369-galpon-grua/06', 'escala', 5) }}$$

→ El galpón **se diseña para {{ v('nch2369-galpon-grua/06', 'Q0_X', 2) }} kN y se desplaza
como si le hubieran aplicado {{ v('nch2369-galpon-grua/06', 'V_desp', 2) }} kN**. El factor es
exactamente $R+1 = {{ vt('nch2369-galpon-grua/06', 'escala', 0) }}$, y no por casualidad: las
dos reducciones que separan las escalas son el $R^{*}$ de la Ec. (1a) y el cociente $(R+1)/R$
de la Ec. (13), y acá $R^{*}_Y = R$ y $T^{*}_Y = T_0$, así que el producto se cierra. E4
muestra qué esconde ese 6.

## B · La componente vertical de §5.7

### B1 · El suelo C tiene el mayor coeficiente vertical de la cláusula, y el vertical decrece con la blandura

El efecto sísmico vertical se representa con fuerzas estáticas equivalentes
$F_V = \pm C_V P$, y $C_V$ vale $1{,}2\,I A_r S/g$ para suelos tipo A, B y C,
$1{,}1\,I A_r S/g$ para el D y $I A_r S/g$ para el E.

$$C_V = {{ vt('nch2369-galpon-grua/06', 'cv_ABC', 2) }}\,\frac{I\,A_r\,S}{g} = {{ vt('nch2369-galpon-grua/06', 'cv_ABC', 2) }} \cdot {{ vt('nch2369-galpon-grua/06', 'I', 2) }} \cdot {{ vt('nch2369-galpon-grua/06', 'A_r', 2) }} \cdot {{ vt('nch2369-galpon-grua/06', 'S_suelo', 2) }} = {{ vt('nch2369-galpon-grua/06', 'C_V', 5) }}$$

→ **52,9 % del peso**, hacia arriba o hacia abajo, y **sin ningún factor de reducción**: la
cláusula no divide por $R$ ni por $R^{*}$. Los tres coeficientes son
{{ v('nch2369-galpon-grua/06', 'cv_ABC', 1) }} ·
{{ v('nch2369-galpon-grua/06', 'cv_D', 1) }} · 1,0, así que el vertical **decrece** con la
blandura del suelo, al revés de lo que la palabra amplificación sugiere, y este galpón está en
la fila más alta de las tres.

### B2 · Y con eso la vertical supera al corte horizontal de diseño en 1,81

$$E_z = C_V\,P = {{ vt('nch2369-galpon-grua/06', 'C_V', 5) }} \cdot {{ vt('nch2369-galpon-grua/06', 'P_sismico', 5) }} = {{ vt('nch2369-galpon-grua/06', 'E_z', 5) }}\ \text{kN}$$

$$\frac{ {{ vt('nch2369-galpon-grua/06', 'E_z', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'Q0_Y', 5) }} } = {{ vt('nch2369-galpon-grua/06', 'Ez_sobre_Q0', 5) }}$$

→ La componente vertical es **{{ v('nch2369-galpon-grua/06', 'Ez_sobre_Q0', 2) }} veces** el
corte horizontal de diseño. Dos cosas se suman para eso: §5.7.1 no divide por $R$ y §5.13 le
recortó un quinto al horizontal **sin tocar al vertical**, porque el recorte se aplica a lo que
sale del análisis sísmico y la fuerza de §5.7.1 no sale de ahí.

### B3 · C5.7.1 pide repartir el vertical por componente, y el ejemplo que da es esta grúa

$P$ son «los valores de los pesos que efectivamente generan fuerzas de inercia verticales,
actuando en las posiciones de los centros de gravedad de los correspondientes componentes».
C5.7.1 advierte que esa suma no es la misma que la del horizontal y da un ejemplo: **«equipos
móviles (sobre ruedas o sobre rieles)»**.

$$E_{z,\text{techo}} = {{ vt('nch2369-galpon-grua/06', 'C_V', 5) }} \cdot {{ vt('nch2369-galpon-grua/06', 'W_techo', 5) }} = {{ vt('nch2369-galpon-grua/06', 'Ez_techo', 5) }}\ \text{kN}$$

$$E_{z,\text{carril}} = {{ vt('nch2369-galpon-grua/06', 'C_V', 5) }} \cdot {{ vt('nch2369-galpon-grua/06', 'W_carril', 5) }} = {{ vt('nch2369-galpon-grua/06', 'Ez_carril', 5) }}\ \text{kN}$$

$$E_{z,\text{muros}} = {{ vt('nch2369-galpon-grua/06', 'C_V', 5) }} \cdot {{ vt('nch2369-galpon-grua/06', 'W_muros', 5) }} = {{ vt('nch2369-galpon-grua/06', 'Ez_muros', 5) }}\ \text{kN}$$

$$ {{ vt('nch2369-galpon-grua/06', 'Ez_techo', 5) }} + {{ vt('nch2369-galpon-grua/06', 'Ez_carril', 5) }} + {{ vt('nch2369-galpon-grua/06', 'Ez_muros', 5) }} = {{ vt('nch2369-galpon-grua/06', 'Ez_suma', 5) }}\ \text{kN}$$

→ El techo se lleva el **41,4 %**, las carrileras con la grúa el 29,1 % y el revestimiento con
las columnas el 29,5 %, que baja por su propio plano y **no pasa por ningún marco**. De los
{{ v('nch2369-galpon-grua/06', 'Ez_carril', 2) }} kN de la línea de carrileras, la grúa sola
aporta {{ v('nch2369-galpon-grua/06', 'Ez_grua', 5) }} kN.

### B4 · El vertical no tiene tope ni impacto que lo cubra, y los dos veintes de AIST no son el mismo veinte

El tope que AIST §3.11.2 le pone a la inercia de la grúa —el que el 05 midió— está escrito
«in the direction of travel for trolley and bridge», así que es **direccional**. Y el 20 % de
impacto vertical con que el 03 cargó la carrilera es de operación, no de sismo.

$$\frac{C_V}{ {{ vt('nch2369-galpon-grua/06', 't32_tra', 2) }} } = \frac{ {{ vt('nch2369-galpon-grua/06', 'C_V', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 't32_tra', 2) }} } = {{ vt('nch2369-galpon-grua/06', 'raz_veintes', 5) }}$$

→ El coeficiente vertical del sismo es
**{{ v('nch2369-galpon-grua/06', 'raz_veintes', 3) }} veces** los dos veintes de AIST, y son
dos veintes distintos: el 20 % de impacto de §3.7.2, que carga a la viga carrilera cuando la
grúa opera, y el 0,20 g de tracción de §3.11.2, que topa la inercia longitudinal cuando no
opera. **Ninguno de los dos cubre al vertical**, y el vertical es el mayor de los tres.

### B5 · La Ec. (4) es la horizontal a 0,7 de amplitud y a T_0/1,7 de período

El espectro de referencia vertical es
$0{,}7\,A_r S\,[1 + r(1{,}7\,T_V/T_0)^{p}]/[1 + (1{,}7\,T_V/T_0)^{q}]$, con los **mismos** seis
parámetros de la Tabla 6 que el horizontal. El $1{,}7$ va **dentro** del paréntesis,
multiplicando a $T_V/T_0$, así que $S_{aV}(T) = 0{,}7\,S_{aH}(1{,}7\,T)$ idénticamente: misma
forma, amplitud a 0,7 y período comprimido 1,7 veces.

$$f_{\xi V} = \left(\frac{ {{ vt('nch2369-galpon-grua/06', 'xi_ref', 2) }} }{ {{ vt('nch2369-galpon-grua/06', 'xi_V', 2) }} }\right)^{0{,}4} = {{ vt('nch2369-galpon-grua/06', 'f_xiV', 5) }}$$

$$T_{V,\text{pico}} = \frac{T_{\text{pico}}}{1{,}7} = \frac{ {{ vt('nch2369-galpon-grua/06', 'T_pico', 5) }} }{1{,}7} = {{ vt('nch2369-galpon-grua/06', 'TV_pico', 5) }}\ \text{s}$$

$$S_{aV}({{ vt('nch2369-galpon-grua/06', 'TV_pico', 5) }}) = 0{,}7\,S_{aH}({{ vt('nch2369-galpon-grua/06', 'T_pico', 5) }}) = 0{,}7 \cdot {{ vt('nch2369-galpon-grua/06', 'Sa_pico', 5) }} = {{ vt('nch2369-galpon-grua/06', 'SaV_pico', 5) }}\ \text{g}$$

$$S_a({{ vt('nch2369-galpon-grua/06', 'TV_pico', 5) }}) = \frac{I\,S_{aV}\,f_{\xi V}}{R_V} = \frac{ {{ vt('nch2369-galpon-grua/06', 'I', 2) }} \cdot {{ vt('nch2369-galpon-grua/06', 'SaV_pico', 5) }} \cdot {{ vt('nch2369-galpon-grua/06', 'f_xiV', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'R_V', 2) }} } = {{ vt('nch2369-galpon-grua/06', 'SaV_dis_pico', 5) }}\ \text{g}$$

→ El pico del espectro **de diseño** vertical vale
**{{ v('nch2369-galpon-grua/06', 'SaV_dis_pico', 5) }} g en
{{ v('nch2369-galpon-grua/06', 'TV_pico', 5) }} s**. El amortiguamiento vertical es
{{ v('nch2369-galpon-grua/06', 'xi_V', 2) }} y no 0,02, así que corrige un 22,7 % y no un
44,3 %; y el $R_V = {{ vt('nch2369-galpon-grua/06', 'R_V', 2) }}$ que §5.4 fija es el único
factor de reducción de toda la dirección vertical.

### B6 · El 1,2 de §5.7.1 es ese pico redondeado, y en el suelo C el redondeo quedó corto

$$\frac{ {{ vt('nch2369-galpon-grua/06', 'SaV_dis_pico', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'C_V', 5) }} } = {{ vt('nch2369-galpon-grua/06', 'raz_pico_modal', 5) }}$$

$$ {{ vt('nch2369-galpon-grua/06', 'T_cru2', 5) }} - {{ vt('nch2369-galpon-grua/06', 'T_cru1', 5) }} = {{ vt('nch2369-galpon-grua/06', 'ancho_ventana', 5) }}\ \text{s}$$

→ **El coeficiente estático de §5.7.1 no es un número redondo: es el máximo de la ruta modal
de §5.7.2 redondeado a un decimal.** En el suelo C ese máximo vale
{{ v('nch2369-galpon-grua/06', 'coef_max_modal', 5) }} veces $A_r S$ y la cláusula escribe
{{ v('nch2369-galpon-grua/06', 'cv_ABC', 1) }}, así que el redondeo quedó **0,36 % del lado
inseguro** —y de las cinco filas de la Tabla 6 el suelo C es **la única** en que eso pasa,
porque el coeficiente es el mismo 1,2 en A, B y C mientras el máximo crece con la fila—. La
ventana donde la ruta modal supera a la estática es de **26 ms**, entre
{{ v('nch2369-galpon-grua/06', 'T_cru1', 5) }} y
{{ v('nch2369-galpon-grua/06', 'T_cru2', 5) }} s de período vertical.

### B7 · Y el factor 2,56 entre las dos rutas que la otra serie publicó no tiene sitio adentro

$$\frac{ {{ vt('nch2369-galpon-grua/06', 'cv_D', 2) }}\,R_V}{0{,}7\,f_{\xi V}} = \frac{ {{ vt('nch2369-galpon-grua/06', 'cv_D', 2) }} \cdot {{ vt('nch2369-galpon-grua/06', 'R_V', 2) }} }{0{,}7 \cdot {{ vt('nch2369-galpon-grua/06', 'f_xiV', 5) }} } = {{ vt('nch2369-galpon-grua/06', 'raz_rutas_D', 5) }}$$

$$\frac{ {{ vt('nch2369-galpon-grua/06', 'cv_ABC', 2) }}\,R_V}{0{,}7\,f_{\xi V}} = {{ vt('nch2369-galpon-grua/06', 'raz_rutas_C', 5) }}$$

→ La serie de harneros midió un **factor 2,56** entre la ruta estática y la modal y concluyó
que esa elección iba a decidir el tamaño de los pernos. El 2,56 se reproduce acá con una
expresión **en la que no aparece el sitio**: es $1{,}1\,R_V/(0{,}7 f_{\xi V})$, el coeficiente
del suelo D dividido por la forma vertical **evaluada en período cero**. Con los coeficientes
de A, B y C el mismo número es {{ v('nch2369-galpon-grua/06', 'raz_rutas_C', 5) }}. Es el
cociente entre el estático y el extremo **rígido** de la curva, no entre las dos rutas: en el
pico las dos coinciden dentro del 0,36 % (B6).

## C · Las combinaciones de §4.5.1

### C1 · El galpón no tiene pisos, así que la carga permanente es el peso sísmico

Las combinaciones sísmicas son, en LRFD, $1{,}2D + aL + SO + SA + E$ y $0{,}9D + SA + E$; $a$
es la fracción de sobrecarga concurrente con el sismo y la Tabla C-2 le asigna **0** a
«pasarelas de mantención y techos», que es la única fila que este galpón podría usar.

$$D = W_{\text{ed}} + W_{\text{grúa}} = {{ vt('nch2369-galpon-grua/06', 'W_edificio', 5) }} + {{ vt('nch2369-galpon-grua/06', 'Wgrua_sc', 5) }} = {{ vt('nch2369-galpon-grua/06', 'D_grav', 5) }}\ \text{kN}$$

→ **$D = P$ exactamente.** En el edificio de harneros separar la masa sísmica de la
gravitacional fue un paso con su propio cierre, porque ahí $P = D + 0{,}25L$; acá la fracción
de §5.1.2 no tiene sobre qué actuar —no hay entrepisos ni plataformas— y el peso sísmico y la
carga permanente son el mismo número. Eso es lo que va a hacer exactas las dos identidades de
C2 y C3.

### C2 · La combinación que comprime agrega exactamente A_r S

La primera combinación LRFD con la tercera ecuación de §4.5.2, el vertical hacia abajo.

$$P_{u,\text{máx}} = 1{,}2\,D + E_z = 1{,}2 \cdot {{ vt('nch2369-galpon-grua/06', 'D_grav', 5) }} + {{ vt('nch2369-galpon-grua/06', 'E_z', 5) }} = {{ vt('nch2369-galpon-grua/06', 'Pu_max', 5) }}\ \text{kN}$$

$$\frac{ {{ vt('nch2369-galpon-grua/06', 'Pu_max', 5) }} }{1{,}2 \cdot {{ vt('nch2369-galpon-grua/06', 'D_grav', 5) }} } = {{ vt('nch2369-galpon-grua/06', 'aporte_vert', 5) }} \qquad 1 + {{ vt('nch2369-galpon-grua/06', 'ArS', 5) }} = {{ vt('nch2369-galpon-grua/06', 'aporte_vert', 5) }}$$

→ El vertical agrega **exactamente $A_r S$**, un 44,1 %, sobre la gravitacional mayorada. La
identidad es $1{,}2D + E_z = 1{,}2(1 + A_r S)\,D$ y sale de que el 1,2 de §5.7.1 y el 1,2 del
LRFD son el mismo número. Vale solo con $D = P$ y solo en los suelos A, B y C: en el suelo D el
coeficiente es {{ v('nch2369-galpon-grua/06', 'cv_D', 1) }} y el incremento baja a
$0{,}91667\,A_r S$.

### C3 · La que descarga: el vertical se lleva cuatro tercios de A_r S, y ningún sitio de Chile levanta el edificio

La segunda combinación LRFD existe para esto: bajar la gravitacional al mínimo creíble antes
de sumar el sismo.

$$P_{u,\text{desc}} = 0{,}9\,D - E_z = 0{,}9 \cdot {{ vt('nch2369-galpon-grua/06', 'D_grav', 5) }} - {{ vt('nch2369-galpon-grua/06', 'E_z', 5) }} = {{ vt('nch2369-galpon-grua/06', 'Pu_desc', 5) }}\ \text{kN}$$

$$\frac{ {{ vt('nch2369-galpon-grua/06', 'E_z', 5) }} }{0{,}9 \cdot {{ vt('nch2369-galpon-grua/06', 'D_grav', 5) }} } = {{ vt('nch2369-galpon-grua/06', 'frac_vert', 5) }} \qquad \frac{4}{3}\cdot {{ vt('nch2369-galpon-grua/06', 'ArS', 5) }} = {{ vt('nch2369-galpon-grua/06', 'frac_vert', 5) }}$$

$$C_V^{\text{máx}} = {{ vt('nch2369-galpon-grua/06', 'cv_ABC', 2) }} \cdot {{ vt('nch2369-galpon-grua/06', 'A_r_z3', 2) }} \cdot {{ vt('nch2369-galpon-grua/06', 'S_suelo', 2) }} = {{ vt('nch2369-galpon-grua/06', 'CV_max_chile', 5) }} \qquad \frac{0{,}90}{ {{ vt('nch2369-galpon-grua/06', 'CV_max_chile', 5) }} } = {{ vt('nch2369-galpon-grua/06', 'margen_09', 5) }}$$

→ El vertical se lleva el **58,8 %** de la gravitacional reducida, y la fracción es exactamente
$\tfrac{4}{3}A_r S$. Quedan {{ v('nch2369-galpon-grua/06', 'Pu_desc', 2) }} kN de compresión,
así que el edificio **no** se levanta como conjunto — y no puede: el mayor $C_V$ que la norma
admite en Chile es el de zona 3 con suelo C,
**{{ v('nch2369-galpon-grua/06', 'CV_max_chile', 5) }}**, un 27,6 % por debajo del 0,9 que
tendría que igualar. Cada columna sí se levanta cuando encima se le suma el vuelco del
horizontal, y eso es del 13.

### C4 · Y el caso peor es la grúa fuera de la nave

§12.1.4 obliga a armar el estado sísmico con las grúas estacionadas en la posición más
desfavorable, pero NCh3171 §9 agrega que se deben usar las combinaciones que produzcan el
efecto más desfavorable y que **«en algunos casos esto puede ocurrir cuando una o más cargas
en la combinación no están presentes»**.

$$(0{,}90 - {{ vt('nch2369-galpon-grua/06', 'C_V', 5) }}) \cdot {{ vt('nch2369-galpon-grua/06', 'W_edificio', 5) }} = {{ vt('nch2369-galpon-grua/06', 'Pu_desc_sg', 5) }}\ \text{kN}$$

$$\frac{ {{ vt('nch2369-galpon-grua/06', 'Pu_desc_sg', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'Pu_desc', 5) }} } = {{ vt('nch2369-galpon-grua/06', 'peor_sg', 5) }}$$

→ Con la grúa fuera de la nave quedan
**{{ v('nch2369-galpon-grua/06', 'Pu_desc_sg', 2) }} kN**, un **22,2 % menos** de compresión
residual. La razón es estructural y no aritmética: el residuo vale $(0{,}9 - C_V)\,D$ y crece
con el peso, así que **para levantamiento el caso crítico es el de peso mínimo**, justo el que
§12.1.4 no describe. Las dos posiciones hay que correrlas.

### C5 · El par ASD/LRFD de §4.5.1 no es equivalente para levantamiento

Las dos combinaciones ASD de §4.5.1 son $D + 0{,}75aL + 0{,}75SO + 0{,}75SA + 0{,}70E$ y
$D + 0{,}75SA + 0{,}70E$: **ninguna reduce la carga permanente**. No hay $0{,}9D$ ni el
$0{,}6D + E$ de la combinación (8) de NCh3171 §9.2.1. C4.5.1 admite que la equivalencia entre
familias es forzada.

$$P_{u,\text{desc}}^{\text{ASD}} = D - 0{,}70\,E_z = {{ vt('nch2369-galpon-grua/06', 'D_grav', 5) }} - 0{,}70 \cdot {{ vt('nch2369-galpon-grua/06', 'E_z', 5) }} = {{ vt('nch2369-galpon-grua/06', 'Pu_desc_ASD', 5) }}\ \text{kN}$$

$$\frac{ {{ vt('nch2369-galpon-grua/06', 'Pu_desc_ASD', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'Pu_desc', 5) }} } = {{ vt('nch2369-galpon-grua/06', 'raz_ASD', 5) }}$$

→ El ASD deja **1,70 veces más** compresión residual que el LRFD, y el factor es exacto e
independiente del peso. Quien verifique el anclaje en ASD encuentra un margen que en LRFD no
existe; el 1,5 de §10.1.6 es el parche que la norma le pone a eso para fundaciones, y no
alcanza a cubrir 1,70. La simultaneidad direccional de §4.5.2, por su parte, son tres
ecuaciones por ocho combinaciones de signo:
{{ v('nch2369-galpon-grua/06', 'n_estados', 0) }} estados sísmicos.

## D · La nieve que ninguna de las dos normas escribe

### D1 · El 20 % de la nieve que el 05 adoptó está escrito, y está en la combinación

§4.5.1 manda las combinaciones sin sismo a NCh3171, y la combinación (5) de §9.1.1 de esa
norma es $1{,}2D + 1{,}4E + L + 0{,}2S$: lleva **un quinto de la nieve concurrente con el
sismo**. AIST §3.11.2.1 (5a) escribe el mismo $0{,}2S$. La excepción d) de §9.1.1 deja tomar
$S$ como la nieve de techo plano o la de techo inclinado.

$$0{,}2\,S = {{ vt('nch2369-galpon-grua/06', 'frac_nieve', 2) }} \cdot {{ vt('nch2369-galpon-grua/06', 'p_s', 5) }} \cdot {{ vt('nch2369-galpon-grua/06', 'A_planta', 5) }} = {{ vt('nch2369-galpon-grua/06', 'S_comb', 5) }}\ \text{kN}$$

→ **{{ v('nch2369-galpon-grua/06', 'S_comb', 2) }} kN**, y son exactamente los que el 05
calculó como «la nieve que entraría si superara el umbral». El 20 % que ese eslabón adoptó de
la práctica norteamericana —sin abrir la norma— **está escrito en una cláusula chilena**, y la
diferencia importa: NCh3171 lo pone en la **combinación**, como carga gravitacional
concurrente, y no en la masa sísmica. Acá
$p_f = {{ vt('nch2369-galpon-grua/06', 'p_f', 5) }} = p_s$ porque el 02 sacó $C_s = 1{,}00$,
así que la excepción d) no llega a decidir nada; con un techo más inclinado o más liso, sí.

### D2 · La obligación de zona montañosa: dos normas la exigen y ninguna la da

NCh3171 §9.1.1 cierra pidiendo que **«en zonas donde la presencia de viento y nieve no es
eventual, por ejemplo, zonas montañosas […] se deben estudiar combinaciones especiales que
reemplacen las combinaciones (3b), (4) y (5) […] pero que no sean menores que las
originales»**. C4.5.1 de NCh2369 dice lo mismo con otras palabras y también delega.

$$P_{u,\text{nieve}} = 1{,}2\,D + E_z + 0{,}2\,S = {{ vt('nch2369-galpon-grua/06', 'Pu_max', 5) }} + {{ vt('nch2369-galpon-grua/06', 'S_comb', 5) }} = {{ vt('nch2369-galpon-grua/06', 'Pu_nieve', 5) }}\ \text{kN}$$

$$\frac{ {{ vt('nch2369-galpon-grua/06', 'S_comb', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'Pu_max', 5) }} } = {{ vt('nch2369-galpon-grua/06', 'aporte_nieve', 5) }}$$

→ La combinación especial que este eslabón construye es la (5) de NCh3171 escrita en la forma
de §4.5.1 —con $E$ a factor 1,0, porque el $E$ de NCh2369 ya está a nivel último y por eso no
lleva el 1,4—, y **no es menor que la original**. La nieve concurrente agrega **10,5 %** sobre
la combinación que comprime. Las dos normas exigen la combinación especial y ninguna la
escribe: lo que cierra la obligación del 02 es que el factor 0,2 sí está tabulado.

### D3 · Lo que queda abierto vale 5,0 %

La otra lectura posible es la de ASCE: además de la carga concurrente, meter el 20 % de la
nieve en la **masa sísmica**, que es el frente que el 05 dejó abierto con un criterio adoptado.

$$P' = {{ vt('nch2369-galpon-grua/06', 'P_sismico', 5) }} + {{ vt('nch2369-galpon-grua/06', 'S_comb', 5) }} = {{ vt('nch2369-galpon-grua/06', 'P_masa', 5) }}\ \text{kN} \qquad \frac{ {{ vt('nch2369-galpon-grua/06', 'P_masa', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'P_sismico', 5) }} } = {{ vt('nch2369-galpon-grua/06', 'sube_todo', 5) }}$$

$$Q_0'^{\text{máx}} = \frac{ {{ vt('nch2369-galpon-grua/06', 'c_max', 2) }} \cdot {{ vt('nch2369-galpon-grua/06', 'I', 2) }} \cdot {{ vt('nch2369-galpon-grua/06', 'A_r', 2) }} \cdot {{ vt('nch2369-galpon-grua/06', 'S_suelo', 2) }} }{ {{ vt('nch2369-galpon-grua/06', 'R_T7', 0) }} + 1} \cdot {{ vt('nch2369-galpon-grua/06', 'f_xi', 5) }} \cdot {{ vt('nch2369-galpon-grua/06', 'P_masa', 5) }} = {{ vt('nch2369-galpon-grua/06', 'Q0_nieve', 5) }}\ \text{kN}$$

$$1{,}2 \cdot {{ vt('nch2369-galpon-grua/06', 'D_grav', 5) }} + {{ vt('nch2369-galpon-grua/06', 'C_V', 5) }} \cdot {{ vt('nch2369-galpon-grua/06', 'P_masa', 5) }} + {{ vt('nch2369-galpon-grua/06', 'S_comb', 5) }} = {{ vt('nch2369-galpon-grua/06', 'Pu_ambas', 5) }}\ \text{kN}$$

$$\frac{ {{ vt('nch2369-galpon-grua/06', 'Pu_ambas', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'Pu_nieve', 5) }} } = {{ vt('nch2369-galpon-grua/06', 'abierto', 5) }}$$

→ Con la nieve también en la masa **todo sube 18,2 %** —el corte de diseño pasa a
{{ v('nch2369-galpon-grua/06', 'Q0_nieve', 2) }} kN, porque el techo de §5.13 es proporcional a
$P$ y el recorte se sigue tomando— y la combinación gobernante queda **5,0 % por encima** de la
que D2 construyó. La mayor incertidumbre que el 05 declaró queda entonces **acotada en 5,0 %,
no cerrada**: la diferencia entre las dos lecturas ya no es un factor
{{ v('nch2369-galpon-grua/06', 'sube_todo', 2) }} sobre todo el diseño sino un 5 % sobre la
combinación que manda.

## E · La deriva de §6.3, y el límite que sí manda

{{ figura('nch2369-galpon-grua/06', 'derivas', 'Los dos desplazamientos sísmicos de 14,56458 y 69,56272 mm y el de 11,59379 que daría el corte de diseño, contra las dos líneas de límite: los 18,75 mm de AIST al nivel del riel, que el desplazamiento de la dirección de marcos supera 3,71 veces, y los 157,50 mm del 0,015h de §6.3, que pasa') }}

### E1 · El límite de §6.3, y que su propio comentario dice que no aplica a equipos

§6.3 fija $d_{\text{máx}} = 0{,}015\,h$ para estructuras en general, con $h$ = altura del nivel
o entre dos puntos sobre una misma línea vertical. C6.1 aclara dos cosas: que **«los
desplazamientos máximos indicados en 6.3 no aplican a equipos»** y que **«esta norma no
establece un límite al desplazamiento relativo en equipos»**.

$$d_{\text{máx}} = {{ vt('nch2369-galpon-grua/06', 'deriva_lim', 3) }}\,h = {{ vt('nch2369-galpon-grua/06', 'deriva_lim', 3) }} \cdot 10\,500 = {{ vt('nch2369-galpon-grua/06', 'd_lim', 2) }}\ \text{mm}$$

→ **{{ v('nch2369-galpon-grua/06', 'd_lim', 2) }} mm** para la estructura, y **nada** para el
puente grúa. Un galpón de un nivel tiene un solo entrepiso y el límite se mide sobre la altura
libre de columna (S7); tomarlo sobre la cumbrera daría 195,00 mm, un 24 % más, sobre un
desplazamiento que se produce en el alero.

### E2 · Los desplazamientos de §6.1 son el desplazamiento espectral, y no se dividen por R estrella

Con la masa en un solo nivel (S1), el desplazamiento que §6.1 pide es el de un oscilador de un
grado de libertad bajo el espectro de referencia corregido:
$d = I f_\xi S_{aH}(T^{*})\,g\,T^{*2}/4\pi^{2}$.

$$d_X = \frac{ {{ vt('nch2369-galpon-grua/06', 'I', 2) }} \cdot {{ vt('nch2369-galpon-grua/06', 'f_xi', 5) }} \cdot {{ vt('nch2369-galpon-grua/06', 'Sa_ref_X', 5) }} \cdot {{ vt('nch2369-galpon-grua/06', 'g_grav', 2) }} \cdot {{ vt('nch2369-galpon-grua/06', 'T_star_X', 2) }}^{2}}{4\cdot\pi^{2}}\cdot 10^{3} = {{ vt('nch2369-galpon-grua/06', 'd_X', 5) }}\ \text{mm}$$

$$d_Y = \frac{ {{ vt('nch2369-galpon-grua/06', 'I', 2) }} \cdot {{ vt('nch2369-galpon-grua/06', 'f_xi', 5) }} \cdot {{ vt('nch2369-galpon-grua/06', 'Sa_ref_Y', 5) }} \cdot {{ vt('nch2369-galpon-grua/06', 'g_grav', 2) }} \cdot {{ vt('nch2369-galpon-grua/06', 'T_star_Y', 2) }}^{2}}{4\cdot\pi^{2}}\cdot 10^{3} = {{ vt('nch2369-galpon-grua/06', 'd_Y', 5) }}\ \text{mm}$$

$$\frac{ {{ vt('nch2369-galpon-grua/06', 'd_X', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'd_lim', 2) }} } = {{ vt('nch2369-galpon-grua/06', 'uso_X', 5) }} \qquad \frac{ {{ vt('nch2369-galpon-grua/06', 'd_Y', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'd_lim', 2) }} } = {{ vt('nch2369-galpon-grua/06', 'uso_Y', 5) }}$$

→ **0,09 y 0,44**: las dos direcciones pasan, y la de marcos con más de la mitad del límite
libre. La deriva vale {{ v('nch2369-galpon-grua/06', 'frac_altura', 3, 100) }} % de la altura
contra el 1,5 % admitido. Es el resultado contrario al del edificio de harneros, que en la dirección
de marcos usaba 1,74: ahí el período era 0,95 s y acá
{{ v('nch2369-galpon-grua/06', 'T_star_Y', 2) }}, y el desplazamiento espectral va con
$S_{aH}\,T^{*2}$.

Sobre el modelo, esa deformada es la del empuje transversal en los diez aleros. El visor la
dibuja a la escala que su propio rótulo declara —no es la del sismo—, y lo que interesa mirar
es la **forma**: el alero se corre y el rafter la acompaña, que es exactamente el modo de un
grado de libertad que el supuesto S1 asume.

<rukan-visor src="../../../modelos/galpon-grua/galpon-grua.escena.json" caso="H_alero" vista="transversal"></rukan-visor>

### E3 · El mismo número sale de la rigidez que el período implica, y es la que el 05 le pidió al 07

El desplazamiento también es la fuerza sobre la rigidez, y la rigidez no es libre: el período
declarado en el 04 y la masa fijada en el 05 la determinan. El numerador es el corte
equivalente de A2.

$$K_Y = \frac{ {{ vt('nch2369-galpon-grua/06', 'P_sismico', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'g_grav', 2) }} }\cdot\left(\frac{2\cdot\pi}{ {{ vt('nch2369-galpon-grua/06', 'T_star_Y', 2) }} }\right)^{2} = {{ vt('nch2369-galpon-grua/06', 'K_Y', 5) }}\ \text{kN}/\text{m}$$

$$d_Y = \frac{ {{ vt('nch2369-galpon-grua/06', 'V_desp', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'K_Y', 5) }} }\cdot 10^{3} = {{ vt('nch2369-galpon-grua/06', 'd_Y_por_K', 5) }}\ \text{mm}$$

$$\frac{ {{ vt('nch2369-galpon-grua/06', 'K_Y', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'n_marcos', 0) }} } = {{ vt('nch2369-galpon-grua/06', 'K_Y_marco', 5) }}\ \text{kN}/\text{m}$$

→ El mismo {{ v('nch2369-galpon-grua/06', 'd_Y', 5) }}, por un camino que no comparte ni una
operación con el de E2. Y la rigidez por marco que sale son **los mismos
{{ v('nch2369-galpon-grua/06', 'K_Y_marco', 2) }} kN/m que el 05 le dejó como obligación al
07**, así que las dos afirmaciones son la misma vista de dos lados. La consecuencia de fondo es
que **la deriva no depende de $R^{*}$ ni del recorte de §5.13**: los dos se cancelan entre la
Ec. (1a) y §6.1, y el 04 y el 05 gastaron un eslabón cada uno en cosas que §6.1 ignora.

### E4 · La regla 100/30 sobre desplazamientos no cambia nada, y la planta simétrica es la razón

§6.1 exige que la acción sísmica de los desplazamientos considere la regla de simultaneidad
direccional de §4.5.2. Las tres ecuaciones combinan **respuestas de tres análisis
independientes**, no desplazamientos de direcciones distintas en un mismo punto.

$$\frac{ {{ vt('nch2369-galpon-grua/06', 'd_Y', 5) }} + {{ vt('nch2369-galpon-grua/06', 'f_30', 2) }} \cdot {{ vt('nch2369-galpon-grua/06', 'd_X', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'd_lim', 2) }} } = {{ vt('nch2369-galpon-grua/06', 'uso_10030', 5) }}$$

→ Los dos vanos arriostrados están en los **ejes extremos** (del 01), así que el centro de
rigidez longitudinal coincide con el de masa y el término cruzado de la 2.ª ecuación vale cero:
la deriva no se mueve. Y aun sumando el $0{,}3\,d_X$ como si los dos desplazamientos ocurrieran
en el mismo punto y en la misma dirección —que no es lo que la cláusula dice— el uso sube a
**{{ v('nch2369-galpon-grua/06', 'uso_10030', 2) }}** y sigue pasando. Lo que el 12 tiene que
mirar no es excentricidad en planta sino el diafragma que salva los dos vanos de portón.

### E5 · El límite que sí manda es de la grúa, y es seis veces más estricto por una razón que no depende de la altura

AIST §5.3: «Building frame lateral drift at the top of the crane girders shall be no greater
than 1/400 of the height from column base or 2 in., whichever is less», para las fuerzas
laterales de la grúa y para el viento de 10 años de recurrencia.

$$2 \cdot {{ vt('nch2369-galpon-grua/06', 'pulgada', 2) }} = {{ vt('nch2369-galpon-grua/06', 'dos_pulgadas', 2) }}\ \text{mm}$$

$$\frac{7\,500}{ {{ vt('nch2369-galpon-grua/06', 'grua_lim', 0) }} } = {{ vt('nch2369-galpon-grua/06', 'dlim_grua', 2) }}\ \text{mm} \qquad \frac{ {{ vt('nch2369-galpon-grua/06', 'dos_pulgadas', 2) }} }{ {{ vt('nch2369-galpon-grua/06', 'dlim_grua', 2) }} } = {{ vt('nch2369-galpon-grua/06', 'flojo_2in', 5) }}$$

$$d_{\text{lím}}^{\text{grúa}} = \min\left(\frac{7\,500}{ {{ vt('nch2369-galpon-grua/06', 'grua_lim', 0) }} } ; {{ vt('nch2369-galpon-grua/06', 'dos_pulgadas', 2) }}\right) = {{ vt('nch2369-galpon-grua/06', 'dlim_grua', 2) }}\ \text{mm}$$

$$\frac{ {{ vt('nch2369-galpon-grua/06', 'deriva_lim', 3) }} \cdot 7\,500}{ {{ vt('nch2369-galpon-grua/06', 'dlim_grua', 2) }} } = {{ vt('nch2369-galpon-grua/06', 'mas_estricto', 5) }} \qquad {{ vt('nch2369-galpon-grua/06', 'dos_pulgadas', 2) }} \cdot {{ vt('nch2369-galpon-grua/06', 'grua_lim', 0) }} = {{ vt('nch2369-galpon-grua/06', 'h_gobierna_2in', 0) }}\ \text{mm}$$

→ **{{ v('nch2369-galpon-grua/06', 'dlim_grua', 2) }} mm** al nivel del riel, contra los
112,50 mm que §6.3 daría a esa misma altura: **exactamente
{{ v('nch2369-galpon-grua/06', 'mas_estricto', 0) }} veces más estricto, y el 6 no depende de
la altura** —es $0{,}015$ dividido por $1/400$—. El tope de 2 in solo empieza a gobernar sobre
{{ v('nch2369-galpon-grua/06', 'h_gobierna_2in', 0) }} mm de columna, y esta tiene 10 500. Las
dos medidas **no son la misma pregunta**: la de AIST es servicio bajo empuje de grúa y viento
frecuente, la de §6.3 es control de daño bajo el sismo de diseño.

$$\frac{ {{ vt('nch2369-galpon-grua/06', 'd_Y', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'dlim_grua', 2) }} } = {{ vt('nch2369-galpon-grua/06', 'sismo_sobre_grua', 5) }}$$

→ Y por eso el resultado de §6.3 no cierra la pregunta: el desplazamiento del sismo de diseño
es **{{ v('nch2369-galpon-grua/06', 'sismo_sobre_grua', 2) }} veces** la tolerancia de servicio
de la carrilera. No es un incumplimiento —son estados de carga distintos y el límite de AIST no
es sísmico— pero sí dice que después del sismo de diseño la carrilera queda **fuera de
alineación por un factor 3,7**, y de eso NCh2369 no se desentiende: C6.1 pide que, cuando la
operación se vea afectada, «las condiciones se deben informar, indicando las consecuencias
directas causadas por el desplazamiento relativo». **La norma no fija el límite y sí obliga a
declarar la consecuencia**, que es lo contrario de un vacío.

### E6 · El error que §6.1 evita queda justo debajo de ese límite

$$d_Y^{\text{ing}} = \frac{ {{ vt('nch2369-galpon-grua/06', 'd_Y', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'R_T7', 0) }} + 1} = {{ vt('nch2369-galpon-grua/06', 'd_Y_ing', 5) }}\ \text{mm} \qquad \frac{ {{ vt('nch2369-galpon-grua/06', 'd_Y_ing', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'dlim_grua', 2) }} } = {{ vt('nch2369-galpon-grua/06', 'uso_ing_grua', 5) }}$$

→ Quien tome los desplazamientos del análisis con el espectro de **diseño** y el corte ya
recortado obtiene **{{ v('nch2369-galpon-grua/06', 'd_Y_ing', 2) }} mm**, un factor
$R+1 = {{ vt('nch2369-galpon-grua/06', 'escala', 0) }}$ abajo (A2). Y el número equivocado no se
ve raro: queda en el **62 %** del límite de la grúa y en el 7 % del de §6.3, o sea holgado por
los dos criterios a la vez. C6.1 explica por qué la norma cerró esa puerta: la resistencia se
evaluó favorable en los terremotos chilenos y **la estimación del desplazamiento, deficiente**.

## F · P-Δ y el vuelco de la grúa

### F1 · P-Δ no llega a ser obligatorio, y el coeficiente dice cuánto pesa

§6.4 exige considerar el efecto P-Δ cuando las deformaciones sísmicas excedan $0{,}015\,h$ —el
mismo umbral de §6.3—. C6.4 anticipa que rara vez importa en estructuras arriostradas y sí
puede importar en marcos a momento.

$$\theta_Y = \frac{P\,d_Y}{Q_0^{\text{dis}}\,h} = \frac{ {{ vt('nch2369-galpon-grua/06', 'P_sismico', 5) }} \cdot {{ vt('nch2369-galpon-grua/06', 'd_Y', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'Q0_Y', 5) }} \cdot 10\,500} = {{ vt('nch2369-galpon-grua/06', 'theta_Y', 5) }}$$

$$\frac{1}{1 - {{ vt('nch2369-galpon-grua/06', 'theta_Y', 5) }} } = {{ vt('nch2369-galpon-grua/06', 'f_PDelta_Y', 5) }} \qquad \theta_X = {{ vt('nch2369-galpon-grua/06', 'theta_X', 5) }}$$

→ **No aplica**: {{ v('nch2369-galpon-grua/06', 'd_Y', 2) }} mm no exceden los
{{ v('nch2369-galpon-grua/06', 'd_lim', 2) }}. El indicador dice cuánto se está dejando fuera:
**+2,3 % en la dirección de marcos y +0,5 % en la arriostrada**, contra el +12,9 % que el
edificio de harneros tenía en su marco. C6.4 acierta otra vez, y el $\theta$ está calculado con
el corte de diseño y el desplazamiento de §6.1, o sea mezclando las dos escalas de A2 a
propósito, del lado conservador.

### F2 · El umbral de vuelco de la grúa, y cuánto lo mueve la regla 100/30

§12.1.5 obliga a contemplar dispositivos de seguridad para evitar la caída del puente grúa «en
aquellos casos en que los análisis como equipos móviles (ver 11.6) indiquen potenciales
levantamientos». La grúa se levanta cuando el vuelco del horizontal supera al momento
restitutivo del peso ya aliviado por el vertical, sobre una trocha de
{{ v('nch2369-galpon-grua/06', 'wb_ruedas', 2) }} m.

$$h_{cg}^{\text{lím}} = \frac{(1 - {{ vt('nch2369-galpon-grua/06', 'f_30', 2) }} \cdot {{ vt('nch2369-galpon-grua/06', 'C_V', 5) }})\cdot {{ vt('nch2369-galpon-grua/06', 'wb_ruedas', 2) }}/2}{ {{ vt('nch2369-galpon-grua/06', 'C_dis', 5) }} } = {{ vt('nch2369-galpon-grua/06', 'umb_ec1', 5) }}\ \text{m}$$

$$\frac{(1 - {{ vt('nch2369-galpon-grua/06', 'C_V', 5) }})\cdot {{ vt('nch2369-galpon-grua/06', 'wb_ruedas', 2) }}/2}{ {{ vt('nch2369-galpon-grua/06', 'f_30', 2) }} \cdot {{ vt('nch2369-galpon-grua/06', 'C_dis', 5) }} } = {{ vt('nch2369-galpon-grua/06', 'umb_ec3', 5) }}\ \text{m} \qquad \frac{(1 - {{ vt('nch2369-galpon-grua/06', 'C_V', 5) }})\cdot {{ vt('nch2369-galpon-grua/06', 'wb_ruedas', 2) }}/2}{ {{ vt('nch2369-galpon-grua/06', 'C_dis', 5) }} } = {{ vt('nch2369-galpon-grua/06', 'umb_pleno', 5) }}\ \text{m}$$

$$\frac{ {{ vt('nch2369-galpon-grua/06', 'umb_ec1', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'umb_pleno', 5) }} } = {{ vt('nch2369-galpon-grua/06', 'sube_10030', 5) }} \qquad \frac{ {{ vt('nch2369-galpon-grua/06', 'umb_ec1', 5) }} }{ {{ vt('nch2369-galpon-grua/06', 'wb_ruedas', 2) }} } = {{ vt('nch2369-galpon-grua/06', 'sobre_trocha', 5) }}$$

→ Gobierna la **1.ª ecuación** de §4.5.2 —horizontal pleno con 30 % de vertical— y da un umbral
de **{{ v('nch2369-galpon-grua/06', 'umb_ec1', 2) }} m** sobre el riel; la 3.ª, con el vertical
pleno y 30 % de horizontal, pide {{ v('nch2369-galpon-grua/06', 'umb_ec3', 2) }} m. Sumar las
dos componentes plenas, que **no** es una combinación de la norma, daría
{{ v('nch2369-galpon-grua/06', 'umb_pleno', 2) }} m: la regla 100/30 **sube el umbral un
78,7 %**, y es la primera vez en la serie que esa regla decide un resultado en vez de
multiplicar {{ v('nch2369-galpon-grua/06', 'n_estados', 0) }} estados. El umbral gobernante es
**{{ v('nch2369-galpon-grua/06', 'sobre_trocha', 2) }} veces la trocha misma**: un puente grúa
tendría que ser vez y media más alto que largo entre ruedas, así que el levantamiento no se
construye con estos números. La verificación formal es de §11.6 y necesita el centro de
gravedad del puente (S8).

## Veredicto

**La componente vertical es lo que gobierna este eslabón.** §5.7.1 le da al suelo C el mayor de
sus tres coeficientes, $C_V = 1{,}2\,A_r S = {{ vt('nch2369-galpon-grua/06', 'C_V', 5) }}$, sin
ninguna reducción, y con eso los {{ v('nch2369-galpon-grua/06', 'E_z', 2) }} kN de vertical
superan en **{{ v('nch2369-galpon-grua/06', 'Ez_sobre_Q0', 2) }}** al corte horizontal que
§5.13 acababa de recortar. En la combinación que comprime el vertical agrega **exactamente
$A_r S$**, un 44,1 % —{{ v('nch2369-galpon-grua/06', 'Pu_max', 2) }} kN—, porque el 1,2 de la
cláusula y el 1,2 del LRFD se cancelan y este galpón no tiene pisos:
$D = {{ vt('nch2369-galpon-grua/06', 'D_grav', 5) }}$ kN es el peso sísmico. En la que descarga
se lleva cuatro tercios de $A_r S$, el 58,8 %, y quedan
{{ v('nch2369-galpon-grua/06', 'Pu_desc', 2) }} kN: el edificio no se levanta como conjunto **ni
podría**. El caso crítico de levantamiento no es el que §12.1.4 describe sino **la grúa fuera de
la nave**, con 22,2 % menos de compresión residual. Del vertical, el techo se lleva
{{ v('nch2369-galpon-grua/06', 'Ez_techo', 2) }} kN y la línea de carrileras con la grúa,
{{ v('nch2369-galpon-grua/06', 'Ez_carril', 2) }}.

Ese 1,2 no es un número redondo: es el **máximo del espectro de diseño vertical de §5.7.2
redondeado a un decimal**, y de las cinco filas de la Tabla 6 el suelo C es la única donde el
redondeo quedó corto, un 0,36 %. Por lo mismo el «factor 2,56 entre las dos rutas» que la serie
de harneros publicó no describe las dos rutas: es el estático dividido por el extremo rígido de
la curva, y se calcula sin que el sitio aparezca.

En deriva la asimetría es de §6.1: el desplazamiento se estima con el espectro de referencia,
sin dividir por $R^{*}$, y §5.13 excluye los desplazamientos del recorte. El galpón se diseña
para {{ v('nch2369-galpon-grua/06', 'Q0_X', 2) }} kN y se desplaza como si le hubieran aplicado
**{{ v('nch2369-galpon-grua/06', 'V_desp', 2) }} kN**, un factor exactamente $R+1$. Con eso
$d_Y = {{ vt('nch2369-galpon-grua/06', 'd_Y', 2) }}$ mm contra
{{ v('nch2369-galpon-grua/06', 'd_lim', 2) }} de límite —**uso 0,44**— y P-Δ no llega a ser
obligatorio, con una amplificación de solo
{{ v('nch2369-galpon-grua/06', 'f_PDelta_Y', 5) }}.

**Pero §6.3 no es el criterio que manda.** C6.1 dice que ese límite no aplica a equipos y que la
norma no fija ninguno para el desplazamiento relativo de un equipo; el de servicio lo pone AIST
§5.3 en **{{ v('nch2369-galpon-grua/06', 'dlim_grua', 2) }} mm** al nivel del riel, seis veces
más estricto y por una razón que no depende de la altura. Los
{{ v('nch2369-galpon-grua/06', 'd_Y', 2) }} mm del sismo lo superan
**{{ v('nch2369-galpon-grua/06', 'sismo_sobre_grua', 2) }} veces**: no es un incumplimiento,
porque son estados de carga distintos, pero sí es la consecuencia que C6.1 obliga a
**informar**. El 07 recibe el número y la verificación, no el resultado, junto con la nieve
concurrente ({{ v('nch2369-galpon-grua/06', 'S_comb', 2) }} kN) y la combinación que la lleva
({{ v('nch2369-galpon-grua/06', 'Pu_nieve', 2) }} kN).

## Límites

- **La deriva no es un valor declarado, pero el período sí** (S1). Todo el bloque E cuelga de
  los $T^{*}$ que el 04 declaró y de tratar al galpón como un oscilador de un grado de libertad.
  Con un diafragma de techo flexible el alero no se mueve como un cuerpo rígido y los dos vanos
  de portón lo hacen probable: el 12 puede desmentirlo. Lo que **no** cambia con el modelo es la
  estructura del resultado: $d \propto S_{aH}(T^{*})\,T^{*2}$ y el factor $R+1$ entre las dos
  escalas.
- **La cascada sigue pendiente.** El [00](../00-el-modelo/) publica el período del modelo
  corrido, bastante menor que los {{ v('nch2369-galpon-grua/06', 'T_star_Y', 2) }} s que este
  eslabón hereda; con él, $d_Y$ bajaría con el cuadrado del período. Se aplica como un cambio
  explícito después de migrar la serie completa, para que el test de cadena lo delate eslabón
  por eslabón.
- **No se verifica la deriva bajo las fuerzas de la grúa** (S7). El límite de AIST §5.3 se
  publica; comprobarlo exige el empuje lateral del 03 repartido entre marcos según rigidez
  relativa, que es del 07 y del 10. Este eslabón entrega los
  {{ v('nch2369-galpon-grua/06', 'dlim_grua', 2) }} mm y la advertencia de que el criterio de
  deriva del 07 no es §6.3.
- **$SA = 0$ con reserva** (S5). El impacto contra el tope del puente —el `Cbs` de AIST— no lo
  ha calculado ningún eslabón de la serie, y C4.5.1 lo nombra como carga accidental.
- **Un dígito del memo original no reproduce.** El memo publicó el corte con la nieve en la masa
  como 357,53340 kN; esta página evalúa la fórmula tal como está escrita —con el
  $f_\xi = {{ vt('nch2369-galpon-grua/06', 'f_xi', 5) }}$ que la propia fórmula imprime— y da
  {{ v('nch2369-galpon-grua/06', 'Q0_nieve', 5) }}. La diferencia, dos centésimas de milésima de
  kN, viene de que el memo evaluó esa línea con la corrección por amortiguamiento sin redondear.
  No cambia nada y se deja anotado.

## Ficha

{{ ficha('nch2369-galpon-grua/06') }}

## Referencias

| Clave | Norma y edición | Cláusula | Leída en | Cita textual |
|---|---|---|---|---|
| NCh-p1 | NCh2369:2025 (3.ª ed.) | §4.5.1, las cuatro combinaciones con sismo y el reenvío de las demás a NCh3171 | `Normas/NCh 2369 - 3°Edición 2025.05.28.pdf`, p. 22 | «Las combinaciones de cargas que no incorporen la acción sísmica se deben definir según los criterios indicados en NCh3171» |
| NCh-p2 | NCh2369:2025 (3.ª ed.) | §4.5.1, la combinación ASD completa, que no reduce la carga permanente | PDF ídem, p. 22 | «D + 0,75 aL + 0,75 SO + 0,75 SA + 0,70 E» |
| NCh-p3 | NCh2369:2025 (3.ª ed.) | C4.5.1, la carga accidental que S5 declara en cero y no debería | PDF ídem, p. 22 | «Frenajes e impactos por movimientos derivados del sismo» |
| NCh-p4 | NCh2369:2025 (3.ª ed.) | C4.5.1 y Tabla C-2, la fila de pasarelas y techos con $a = 0$ que C1 usa | PDF ídem, p. 22 | «Pasarelas de mantención y techos» |
| NCh-p5 | NCh2369:2025 (3.ª ed.) | C4.5.1, la delegación de alta montaña que D2 recoge | PDF ídem, p. 22 | «y especialmente la forma en que dichos efectos se deben combinar con el evento sísmico definido en esta norma» |
| NCh-p6 | NCh2369:2025 (3.ª ed.) | §4.5.2 y C4.5.2, las tres ecuaciones de simultaneidad y que no son una elección | PDF ídem, p. 23 | «E = ± 0,3 Ex ± 0,3 Ey ± 1,0 Ez» |
| NCh-p7 | NCh2369:2025 (3.ª ed.) | C4.5.2, que las tres se evalúan de manera independiente | PDF ídem, p. 23 | «tres ecuaciones que deben ser evaluadas de manera independiente, con sus respectivos cambios de signos» |
| NCh-p8 | NCh2369:2025 (3.ª ed.) | §5.4, la definición de $R_V = 2{,}0$ que la Ec. (2) usa | PDF ídem, p. 34 | «factor de modificación de la respuesta vertical, igual a 2,0» |
| NCh-p9 | NCh2369:2025 (3.ª ed.) | §5.4.1 y Ec. (2), el espectro de diseño vertical, y $\xi_V = 0{,}03$ — **mirada en PNG**, no extraída | PDF ídem, p. 35 | «Se define el siguiente espectro de diseño para la dirección vertical» |
| NCh-p10 | NCh2369:2025 (3.ª ed.) | §5.4.1, el $\xi_V$ fijo en 0,03 | PDF ídem, p. 35 | «vertical, igual a 0,03, salvo que se muestre por medio de métodos reconocidos por la práctica la validez de valores mayores» |
| NCh-p11 | NCh2369:2025 (3.ª ed.) | §5.4.2 y Ec. (4), el espectro de referencia vertical con el 1,7 **dentro** del paréntesis — **mirada en PNG**, no extraída | PDF ídem, p. 36 | «Se define el siguiente espectro de referencia para la dirección vertical» |
| NCh-p12 | NCh2369:2025 (3.ª ed.) | §5.4.2, que sobre 0,03 en vertical hay que fundamentar | PDF ídem, p. 36 | «El uso de razones de amortiguamiento mayores que 0,03 en la dirección vertical se debe fundamentar mediante un análisis racional» |
| NCh-p13 | NCh2369:2025 (3.ª ed.) | §5.7.1, el $C_V$ de 1,2 para los suelos A, B y C, y qué pesos entran | PDF ídem, p. 42 | «El valor de CV debe ser 1,2 I⋅Ar⋅S/g para suelos tipo A, B y C» |
| NCh-p14 | NCh2369:2025 (3.ª ed.) | §5.7.1, los pesos en los centros de gravedad de los componentes, que es el reparto de B3 | PDF ídem, p. 42 | «los valores de los pesos que efectivamente generan fuerzas de inercia verticales, actuando en las posiciones de los centros de gravedad» |
| NCh-p15 | NCh2369:2025 (3.ª ed.) | C5.7.1, el ejemplo de los equipos móviles sobre rieles, que es esta grúa | PDF ídem, p. 42 | «Un ejemplo es el caso de equipos móviles (sobre ruedas o sobre rieles)» |
| NCh-p16 | NCh2369:2025 (3.ª ed.) | C5.7.1, la recomendación de análisis dinámico si la flexibilidad vertical importa | PDF ídem, p. 42 | «es preferible hacer análisis dinámico considerando los requisitos de 5.7.2» |
| NCh-p17 | NCh2369:2025 (3.ª ed.) | §5.7.2, la ruta modal alternativa con el espectro vertical | PDF ídem, p. 42 | «Alternativamente, se puede desarrollar un análisis modal espectral utilizando el espectro de diseño para la dirección vertical» |
| NCh-p18 | NCh2369:2025 (3.ª ed.) | §5.13, que el recorte **no** se aplica a los desplazamientos | PDF ídem, p. 56 | «Esta reducción no se debe aplicar al cálculo de desplazamientos» |
| NCh-p19 | NCh2369:2025 (3.ª ed.) | §6.1, el espectro elástico de referencia y la simultaneidad direccional en desplazamientos | PDF ídem, p. 75 | «Los desplazamientos sísmicos se deben estimar utilizando el espectro elástico de referencia» |
| NCh-p20 | NCh2369:2025 (3.ª ed.) | C6.1, que los límites de §6.3 no aplican a equipos | PDF ídem, p. 75 | «Los desplazamientos máximos indicados en 6.3 no aplican a equipos» |
| NCh-p21 | NCh2369:2025 (3.ª ed.) | §6.1, que la norma no fija límite al desplazamiento relativo de un equipo | PDF ídem, p. 75 | «Esta norma no establece un límite al desplazamiento relativo en equipos» |
| NCh-p22 | NCh2369:2025 (3.ª ed.) | C6.1, la deficiencia en la estimación del desplazamiento que E6 cita | PDF ídem, p. 75 | «deficiencias en la estimación del desplazamiento sísmico horizontal» |
| NCh-p22b | NCh2369:2025 (3.ª ed.) | C6.1, la obligación de informar cuando el desplazamiento relativo afecta la operación del equipo | PDF ídem, p. 75 | «las condiciones se deben informar, indicando las consecuencias directas causadas por el desplazamiento relativo» |
| NCh-p23 | NCh2369:2025 (3.ª ed.) | §6.3, el $0{,}015\,h$ de estructuras en general y la definición de $h$ — **mirada en PNG**, no extraída | `Normas/NCh 2369 - 3°Edición 2025.05.28.pdf`, pp. 76-77 | «altura del nivel o entre dos puntos ubicados sobre una misma línea vertical» |
| NCh-p24 | NCh2369:2025 (3.ª ed.) | §6.4, cuándo hay que considerar P-Δ, y C6.4 sobre marcos a momento | PDF ídem, p. 77 | «El efecto P-Delta se debe considerar cuando las deformaciones sísmicas excedan el valor» |
| NCh-p25 | NCh2369:2025 (3.ª ed.) | §7.1, que los equipos móviles no están cubiertos por la cláusula 7 y remiten a §11.6 | PDF ídem, p. 77 | «En el caso de grandes equipos móviles debe considerarse lo expuesto en 11.6» |
| NCh-p26 | NCh2369:2025 (3.ª ed.) | §12.1.4, todas las grúas sin carga en la posición más desfavorable | PDF ídem, p. 151 | «todas las grúas sin carga estacionadas en la posición más desfavorable» |
| NCh-p27 | NCh2369:2025 (3.ª ed.) | §12.1.5, el anticaída cuando el análisis como equipo móvil indique levantamiento | PDF ídem, p. 151 | «para evitar la caída de los puentes grúa en aquellos casos en que los análisis como equipos móviles» |
| NCh-p28 | NCh2369:2025 (3.ª ed.) | Tabla 3, la fila de zona 3 con la que C3 arma el mayor $C_V$ de Chile — **mirada en PNG**, no extraída | PDF ídem, p. 64 | «1 0,20 g 0,28 g 2 0,30 g 0,42 g 3 0,40 g 0,56 g» |
| AIST-1 | AIST TR-13:2021 | §3.11.2.1, la combinación sísmica 5a con la carga izada y el $0{,}2S$ | `Normas/aist-tr-no13-2021-3.pdf`, p. 23 | «1.2D+1.2Cdm+1.0E+Cvs+L+0.2S» |
| AIST-2 | AIST TR-13:2021 | §3.11.1, la definición de `Cvs` como carga izada y no como carga vertical | PDF ídem, p. 22 | «Crane lifted load for a single crane with crane trolley positioned to produce the maximum load effect» |
| AIST-3 | AIST TR-13:2021 | §3.11.2, que el tope de la inercia de la grúa es direccional | PDF ídem, p. 22 | «limited in the direction of travel for trolley and bridge by the maximum tractive force» |
| AIST-4 | AIST TR-13:2021 | §5.3, la deriva del marco al nivel de las carrileras, $1/400$ o 2 in, el menor | PDF ídem, p. 29 | «shall be no greater than 1/400 of the height from column base or 2 in., whichever is less» |
| AIST-5 | AIST TR-13:2021 | §5.3, que los dos estados de carga del límite son de servicio y no de sismo | PDF ídem, p. 29 | «Crane lateral forces identified in this report» |
| AIST-6 | AIST TR-13:2021 | §5.8.7, la flecha lateral de $1/400$ de la carrilera, que es del 08 y no de acá | PDF ídem, p. 34 | «Maximum lateral deflection of a girder caused by a side thrust load from one crane shall not exceed 1/400 of the span length» |
| N3171-1 | NCh3171:2017 | §9, que las combinaciones de las normas sísmicas prevalecen — **PDF escaneado, leído a ojo** | `Normas/NCh 3171_2017.pdf`, p. 13 | «Cuando las normas de diseño sísmico consideren otras combinaciones para casos particulares de cargas, éstas prevalecen» |
| N3171-2 | NCh3171:2017 | §9, que el efecto más desfavorable puede ocurrir con cargas ausentes, que es C4 — **escaneado** | PDF ídem, p. 13 | «En algunos casos esto puede ocurrir cuando una o más cargas en la combinación no están presentes» |
| N3171-3 | NCh3171:2017 | §9.1.1, la combinación **(5) $1{,}2D + 1{,}4E + L + 0{,}2S$**, la sísmica con su quinto de nieve — **escaneado** | PDF ídem, p. 13 | «resistencia de diseño sea mayor o igual que el efecto de las cargas mayoradas en las combinaciones siguientes» |
| N3171-4 | NCh3171:2017 | §9.1.1 d), que $S$ se toma como $p_f$ o como $p_s$ — **escaneado** | PDF ídem, p. 14 | «la carga concurrente S se debe tomar ya sea como la carga de nieve para techo plano» |
| N3171-5 | NCh3171:2017 | §9.1.1, la obligación de combinaciones especiales en zona montañosa — **escaneado** | PDF ídem, p. 14 | «se deben estudiar combinaciones especiales que reemplacen las combinaciones (3b), (4) y (5), anteriormente indicadas, pero que no sean menores que las originales» |
| N3171-6 | NCh3171:2017 | §9.2.1, la combinación **(8) $0{,}6D + E$**, la de carga permanente reducida que NCh2369 no tiene — **escaneado** | PDF ídem, p. 15 | «resistencia admisible sea mayor o igual que el efecto de las cargas nominales en las combinaciones siguientes» |
| NCh-5 | NCh2369:2025 (3.ª ed.) | §5.1.2, §5.5.1 y §5.12 a §5.14, que el 05 ya recorrió | `referencias/NCh2369-2025/cap05-analisis-sismico.md` | — |
| NCh-6 | NCh2369:2025 (3.ª ed.) | §6.2.1 y el $\kappa$; §5.9 y los desplazamientos relativos | `referencias/NCh2369-2025/cap06-07-desplazamientos-y-equipos.md` | — |
| NCh-10 | NCh2369:2025 (3.ª ed.) | §10.1.6, el factor 1,5 entre ASD y LRFD que C5 nombra | `referencias/NCh2369-2025/cap10-fundaciones.md` | — |
| N3171-w | NCh3171:2017 | §9 completo, con las diez combinaciones ASD y las seis excepciones de §9.1.1 | `referencias/NCh3171-2017/cap09-combinaciones-de-carga.md` | — |