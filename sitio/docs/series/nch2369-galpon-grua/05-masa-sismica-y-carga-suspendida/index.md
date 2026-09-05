# 05 · Masa sísmica y carga suspendida

El 2,75 de la Ec. (13) no es un número: es el espectro de referencia evaluado en $T_0$. Y al
aplicar ese techo, los dos cortes basales que el 04 tardó un eslabón en separar **quedan
idénticos**. Acá se arma el peso sísmico del galpón, se decide qué parte de la grúa entra en
él y se evalúan el corte de cada dirección contra el piso de §5.12 y el techo de §5.13.
Fuerzas en kN, longitudes en m.

## El caso

| Dato | Valor |
|---|---|
| Geometría | luz {{ v('nch2369-galpon-grua/05', 'L_luz', 2) }} m · {{ v('nch2369-galpon-grua/05', 'n_vanos', 0) }} vanos de {{ v('nch2369-galpon-grua/05', 's_marco', 2) }} m · alero {{ v('nch2369-galpon-grua/05', 'h_libre', 2) }} m (del 01) |
| Cubierta y aislación | {{ v('nch2369-galpon-grua/05', 'g_cubierta', 2) }} kN/m² (S1) |
| Revestimiento de muros y frontones | {{ v('nch2369-galpon-grua/05', 'g_muros', 2) }} kN/m² (S1) |
| Peso propio de columnas | {{ v('nch2369-galpon-grua/05', 'w_columna', 2) }} kN/m, {{ v('nch2369-galpon-grua/05', 'n_columnas', 0) }} columnas de {{ v('nch2369-galpon-grua/05', 'h_libre', 2) }} m (S1) |
| Vigas carrileras con sus ménsulas | {{ v('nch2369-galpon-grua/05', 'w_carrilera', 2) }} kN/m, {{ v('nch2369-galpon-grua/05', 'L_carrilera', 2) }} m en total (S1) |
| Estructura soportante del techo | {{ v('nch2369-galpon-grua/05', 'g_techo_kg', 2) }} kg/m² (del 01) |
| Equipos colgados | {{ v('nch2369-galpon-grua/05', 'P_eq', 2) }} kN por marco, {{ v('nch2369-galpon-grua/05', 'n_marcos', 0) }} marcos (del 01) |
| Puente grúa | {{ v('nch2369-galpon-grua/05', 'Wb_puente', 2) }} + {{ v('nch2369-galpon-grua/05', 'Wt_carro', 2) }} kN, **sin carga** (del 03) |
| Sobrecarga de techo en la masa sísmica | 0 (S3) |
| Nieve en la masa sísmica | 0 (S4) |
| Frenos del puente estacionado | aplicados (S5) |
| Lo que se decide aquí | el peso sísmico, los dos cortes basales de diseño y el $R_1$ del diseño por capacidad |

Los supuestos, en una línea cada uno. **S1**, las cargas permanentes que el 01 no declaró se
declaran acá —cubierta y aislación, revestimiento de muros, peso propio de columnas y peso de
las vigas carrileras con sus ménsulas—, con valores de predimensionamiento para la escala del
galpón; los {{ v('nch2369-galpon-grua/05', 'g_techo_kg', 2) }} kg/m² de estructura de techo y
los {{ v('nch2369-galpon-grua/05', 'P_eq', 2) }} kN de equipos por marco vienen del 01 y no se
vuelven a estimar. **S2**, las cargas por metro cuadrado se aplican sobre la proyección
horizontal, que es la misma convención con que el 02 evaluó la nieve; la superficie inclinada
del techo es un 2,0 % mayor y ese 2,0 % está absorbido en los valores declarados. **S3**, la
sobrecarga de techo no entra en la masa sísmica: la lista obligatoria de §5.1.2 no tiene fila
para techos, y la Tabla C-2 de §4.5, informativa, sí la tiene y le asigna $a = 0$; la decisión
se apoya en esa tabla y no en §5.1.2. **S4**, la nieve no entra, y el criterio que lo decide es
**adoptado**: §5.1.2 no la nombra ni le asigna fracción, así que se toma el umbral de
{{ v('nch2369-galpon-grua/05', 'p_nieve_lim', 2) }} kN/m² sobre el cual la práctica
norteamericana incorpora un {{ v('nch2369-galpon-grua/05', 'frac_nieve', 0, 100) }} % de la
nieve de techo al peso sísmico; **esa norma no se abrió**, así que el umbral entra como
supuesto y no como cláusula, y por eso no tiene fila en las referencias. **S5**, los frenos del
puente y del carro están aplicados cuando la grúa está estacionada, que es la condición que
§12.1.4 describe y la que decide, en E2, cuál de los dos topes de AIST §3.11.2 gobierna.
**S6**, hay una sola grúa (del 03), así que §12.1.4 no obliga a combinar posiciones de varias.

## A · Las áreas

### A1 · El largo y la cumbrera no se declaran: salen de lo heredado

El galpón tiene {{ v('nch2369-galpon-grua/05', 'n_vanos', 0) }} vanos entre marcos y una
pendiente de techo cuya razón horizontal $S$ el 02 ya fijó. Ninguno de los dos números
necesita declararse otra vez.

$$L_{\text{largo}} = {{ vt('nch2369-galpon-grua/05', 'n_vanos', 0) }} \cdot {{ vt('nch2369-galpon-grua/05', 's_marco', 2) }} = {{ vt('nch2369-galpon-grua/05', 'L_largo', 2) }}\ \text{m}$$

$$h_{\text{cumb}} = \frac{ {{ vt('nch2369-galpon-grua/05', 'L_luz', 2) }} }{2}\cdot\frac{1}{ {{ vt('nch2369-galpon-grua/05', 'S_pend', 5) }} } = {{ vt('nch2369-galpon-grua/05', 'h_cumb', 5) }}\ \text{m}$$

→ **{{ v('nch2369-galpon-grua/05', 'L_largo', 2) }} m de largo y
{{ v('nch2369-galpon-grua/05', 'h_cumb', 2) }} m de cumbrera sobre el alero.** El $S$ del 02 es
la razón horizontal —cinco de avance por uno de subida—, así que dividir por él es multiplicar
por la pendiente.

### A2 · Las dos áreas que cargan el peso

La proyección horizontal recibe el techo y la cubierta; el perímetro más los dos triángulos de
frontón reciben el revestimiento.

$$A_{\text{planta}} = {{ vt('nch2369-galpon-grua/05', 'L_luz', 2) }} \cdot {{ vt('nch2369-galpon-grua/05', 'L_largo', 2) }} = {{ vt('nch2369-galpon-grua/05', 'A_planta', 5) }}\ \text{m}^2$$

$$A_{\text{muros}} = 2 \cdot {{ vt('nch2369-galpon-grua/05', 'L_largo', 2) }} \cdot {{ vt('nch2369-galpon-grua/05', 'h_libre', 2) }} + 2 \cdot {{ vt('nch2369-galpon-grua/05', 'L_luz', 2) }} \cdot {{ vt('nch2369-galpon-grua/05', 'h_libre', 2) }} + {{ vt('nch2369-galpon-grua/05', 'L_luz', 2) }} \cdot {{ vt('nch2369-galpon-grua/05', 'h_cumb', 2) }} = {{ vt('nch2369-galpon-grua/05', 'A_muros', 5) }}\ \text{m}^2$$

→ **{{ v('nch2369-galpon-grua/05', 'A_planta', 2) }} y
{{ v('nch2369-galpon-grua/05', 'A_muros', 2) }} m².** Los dos triángulos de cumbrera suman
{{ v('nch2369-galpon-grua/05', 'A_frontones', 2) }} m², un 5,1 % del área de muros, y no se
desprecian porque el frontón es lo que carga el arriostramiento longitudinal.

### A3 · El peso permanente del edificio, sin la grúa

La masa sísmica incluye las cargas permanentes del sistema.

$$g_{\text{techo}} = \frac{ {{ vt('nch2369-galpon-grua/05', 'g_techo_kg', 2) }} \cdot {{ vt('nch2369-galpon-grua/05', 'g_grav', 2) }} }{1\,000} = {{ vt('nch2369-galpon-grua/05', 'g_techo', 5) }}\ \text{kN}/\text{m}^2$$

$$W_{\text{ed}} = {{ vt('nch2369-galpon-grua/05', 'g_techo', 5) }} \cdot A_{\text{planta}} + {{ vt('nch2369-galpon-grua/05', 'g_cubierta', 2) }} \cdot A_{\text{planta}} + {{ vt('nch2369-galpon-grua/05', 'g_muros', 2) }} \cdot A_{\text{muros}} + {{ vt('nch2369-galpon-grua/05', 'w_columna', 2) }} \cdot {{ vt('nch2369-galpon-grua/05', 'h_libre', 2) }} \cdot {{ vt('nch2369-galpon-grua/05', 'n_columnas', 0) }} + {{ vt('nch2369-galpon-grua/05', 'w_carrilera', 2) }} \cdot {{ vt('nch2369-galpon-grua/05', 'L_carrilera', 2) }} + {{ vt('nch2369-galpon-grua/05', 'P_eq', 2) }} \cdot {{ vt('nch2369-galpon-grua/05', 'n_marcos', 0) }} = {{ vt('nch2369-galpon-grua/05', 'W_edificio', 5) }}$$

→ **{{ v('nch2369-galpon-grua/05', 'W_edificio', 3) }} kN**, o 1,076 kN/m² de planta. Los seis
sumandos son, en orden: estructura de techo, cubierta, revestimiento, columnas, vigas
carrileras y equipos colgados.

## B · Las sobrecargas que no entran

### B1 · §5.1.2 copió tres de las cuatro filas de la Tabla C-2, y falta justo la del techo

La fracción mínima de sobrecarga que §5.1.2 obliga a incluir está tabulada para bodegas y
salas de archivo (50 %), zonas de acopio de baja rotación (50 %) y zonas de uso normal y
plataformas de operación (25 %). La Tabla C-2 de §4.5 tiene esas tres filas **y una cuarta**,
«pasarelas de mantención y techos», con $a = 0$.

$$n_{\text{filas}} = 4 - 1 = {{ vt('nch2369-galpon-grua/05', 'n_filas', 0) }}$$

→ La única fila que este galpón necesita es la que la cláusula obligatoria **no tiene**. La
sobrecarga de techo entra con 0, y eso es una decisión apoyada en una tabla informativa, no una
lectura de §5.1.2. Un revisor puede pedir otra cosa y la cláusula no lo desmiente.

### B2 · La nieve tampoco entra, y el umbral que lo decide es de otra norma

§5.1.2 no nombra la nieve ni le asigna fracción, así que el umbral que decide es un criterio
adoptado (S4): {{ v('nch2369-galpon-grua/05', 'frac_nieve', 0, 100) }} % de la nieve de techo
por sobre {{ v('nch2369-galpon-grua/05', 'p_nieve_lim', 2) }} kN/m². Y el sitio sí es de nieve,
porque su carga básica supera con holgura el
{{ v('nch2369-galpon-grua/05', 'p_g_normal', 2) }} kN/m² desde el cual NCh431 la declara
sobrecarga normal.

$$\frac{p_g}{ {{ vt('nch2369-galpon-grua/05', 'p_g_normal', 2) }} } = \frac{ {{ vt('nch2369-galpon-grua/05', 'p_g', 2) }} }{ {{ vt('nch2369-galpon-grua/05', 'p_g_normal', 2) }} } = {{ vt('nch2369-galpon-grua/05', 'raz_normal', 5) }}$$

$$\frac{p_f}{ {{ vt('nch2369-galpon-grua/05', 'p_nieve_lim', 2) }} } = \frac{ {{ vt('nch2369-galpon-grua/05', 'p_f', 5) }} }{ {{ vt('nch2369-galpon-grua/05', 'p_nieve_lim', 2) }} } = {{ vt('nch2369-galpon-grua/05', 'raz_nieve', 5) }}$$

$$W_{\text{nieve}} = {{ vt('nch2369-galpon-grua/05', 'frac_nieve', 2) }} \cdot {{ vt('nch2369-galpon-grua/05', 'p_f', 5) }} \cdot {{ vt('nch2369-galpon-grua/05', 'A_planta', 2) }} = {{ vt('nch2369-galpon-grua/05', 'W_nieve', 5) }}$$

→ El techo queda **12,5 % bajo el umbral** y la nieve no entra. Pero el sitio carga **seis
veces** el mínimo de NCh431, y si la nieve entrara pesaría
{{ v('nch2369-galpon-grua/05', 'W_nieve', 2) }} kN, un **18,2 % del peso sísmico**. Es la mayor
incertidumbre de este eslabón y ninguna cláusula chilena la resuelve.

## C · La grúa

### C1 · §12.1.3 remite al régimen de operación, y el del 03 es el que C12.1.3 exime

El análisis sísmico se hace con las magnitudes y alturas de carga suspendida **más probables**
durante el terremoto de diseño, considerando el período de retorno del sismo y la frecuencia
de operación de las grúas. C12.1.3 traduce eso en dos recomendaciones, y la primera cubre a
las grúas de mantención en las que rara vez se levanta la carga máxima y la operación no es
continua.

$$\frac{ {{ vt('nch2369-galpon-grua/05', 'h_turno', 0) }} }{ {{ vt('nch2369-galpon-grua/05', 'h_dia_total', 0) }} } = {{ vt('nch2369-galpon-grua/05', 'frac_turno', 5) }}$$

→ La grúa opera **{{ v('nch2369-galpon-grua/05', 'h_turno', 0) }} h efectivas de
{{ v('nch2369-galpon-grua/05', 'h_dia_total', 0) }}** y su clase de servicio es la C, la de
talleres. **La carga suspendida se desprecia.** La segunda recomendación —carga máxima al nivel
más alto— es para fundiciones metalúrgicas, no para esto.

### C2 · AIST llega a lo mismo por otro criterio, y el criterio importa

La masa sísmica asociada a grúas que soportan una carga suspendida **no necesita** incluir el
peso de esa carga; pero si la carga va **rígidamente asegurada** a la grúa durante el
desplazamiento, entonces sí se debe incluir.

$$n_{\text{condiciones}} = {{ vt('nch2369-galpon-grua/05', 'n_condiciones', 0) }}$$

→ Las dos normas coinciden en el resultado y **no en la pregunta**: NCh2369 mira el **régimen
de operación** y AIST mira la **conexión mecánica**. Un galpón de mantención con una viga de
izaje empernada al gancho cumpliría la de NCh y fallaría la de AIST. Acá la carga cuelga de un
gancho y las dos se cumplen, así que no hay contradicción que resolver.

### C3 · Pero la grúa sin carga sí está, y §12.1.4 la estaciona donde peor convenga

La combinación sísmica se debe armar con todas las grúas **sin carga** estacionadas en la
posición más desfavorable. C12.1.4 dice de dónde viene la regla: es práctica de AIST y se
justifica probabilísticamente.

$$W_{\text{grúa}} = {{ vt('nch2369-galpon-grua/05', 'Wb_puente', 2) }} + {{ vt('nch2369-galpon-grua/05', 'Wt_carro', 2) }} = {{ vt('nch2369-galpon-grua/05', 'Wgrua_sc', 5) }}$$

→ **{{ v('nch2369-galpon-grua/05', 'Wgrua_sc', 2) }} kN** de puente más carro entran enteros en
el peso sísmico. Lo que se desprecia es la carga, no la grúa.

### C4 · El peso sísmico, con la grúa pesando más de un quinto

$$P = {{ vt('nch2369-galpon-grua/05', 'W_edificio', 5) }} + {{ vt('nch2369-galpon-grua/05', 'Wgrua_sc', 5) }} = {{ vt('nch2369-galpon-grua/05', 'P_sismico', 5) }}$$

$$\frac{ {{ vt('nch2369-galpon-grua/05', 'Wgrua_sc', 5) }} }{ {{ vt('nch2369-galpon-grua/05', 'P_sismico', 5) }} } = {{ vt('nch2369-galpon-grua/05', 'frac_grua', 5) }}$$

→ **{{ v('nch2369-galpon-grua/05', 'P_sismico', 3) }} kN**, de los cuales la grúa es el
**22,2 %**. Un galpón sin puente grúa tendría el mismo techo y un corte basal cuatro quintos
del de este.

Ese mismo peso es el que el modelo del galpón lleva como masa. Los puntos que el visor dibuja
son los nudos con masa: están **todos en el rafter**, repartidos del alero a la cumbrera, y
suman —a la precisión con que la escena publica cada uno— el $P$ que acaba de salir de C4. El
modelo no reparte masa en las columnas ni en el nivel del riel: la concentra donde el área
tributaria de A2 la deja. Gira la vista para verlo.

<rukan-visor src="../../../modelos/galpon-grua/galpon-grua.escena.json" vista="iso"></rukan-visor>

## D · El corte basal

### D1 · Los dos cortes del análisis difieren lo que el 04 dijo

El corte basal es el coeficiente sísmico —el espectro de diseño evaluado en $T^{*}$ y dividido
por $g$— por el peso sobre el nivel basal.

$$Q_{0X} = {{ vt('nch2369-galpon-grua/05', 'Sa_dis_X_pub', 5) }} \cdot {{ vt('nch2369-galpon-grua/05', 'P_sismico', 5) }} = {{ vt('nch2369-galpon-grua/05', 'Q0_X_an', 5) }}$$

$$Q_{0Y} = {{ vt('nch2369-galpon-grua/05', 'Sa_dis_Y_pub', 5) }} \cdot {{ vt('nch2369-galpon-grua/05', 'P_sismico', 5) }} = {{ vt('nch2369-galpon-grua/05', 'Q0_Y_an', 5) }}$$

→ **{{ v('nch2369-galpon-grua/05', 'Q0_X_an', 2) }} y
{{ v('nch2369-galpon-grua/05', 'Q0_Y_an', 2) }} kN.** La dirección arriostrada pide 4,7 % más
que la de marcos, que es exactamente la razón de ordenadas que el 04 publicó: manda el $R^{*}$
degradado.

### D2 · El piso de §5.12 queda tres veces abajo

Si el corte del análisis es menor que $Q_0^{\text{mín}}$, todas las fuerzas se escalan. Esta
norma **no permite** diseñar por debajo de ese valor.

$$Q_0^{\text{mín}} = {{ vt('nch2369-galpon-grua/05', 'c_min', 2) }} \cdot {{ vt('nch2369-galpon-grua/05', 'I', 2) }} \cdot {{ vt('nch2369-galpon-grua/05', 'A_r', 2) }} \cdot {{ vt('nch2369-galpon-grua/05', 'S_suelo', 2) }} \cdot {{ vt('nch2369-galpon-grua/05', 'P_sismico', 5) }} = {{ vt('nch2369-galpon-grua/05', 'Q0_min', 5) }}$$

$$\frac{ {{ vt('nch2369-galpon-grua/05', 'Q0_Y_an', 5) }} }{ {{ vt('nch2369-galpon-grua/05', 'Q0_min', 5) }} } = {{ vt('nch2369-galpon-grua/05', 'holgura_Y', 5) }}$$

→ **{{ v('nch2369-galpon-grua/05', 'Q0_min', 2) }} kN**, y la dirección más floja lo supera
**{{ v('nch2369-galpon-grua/05', 'holgura_Y', 2) }} veces**; la arriostrada,
{{ v('nch2369-galpon-grua/05', 'holgura_X', 5) }}. El piso no gobierna en ninguna de las dos, y
eso es lo que va a dejar $R_1 = R^{*}$ en F1.

### D3 · El 2,75 de la Ec. (13) no es un número: es el espectro evaluado en T_0

El techo del corte basal vale $2{,}75\,I A_r S (0{,}05/\xi)^{0{,}4} P / (g(R+1))$. Evaluando la
Ec. (3) en $T = T_0$ el cociente de formas vale $(1+r)/2$, y con el
$r = {{ vt('nch2369-galpon-grua/05', 'r_s', 2) }}$ del suelo C eso da **exactamente 2,75**.

$$\frac{1 + {{ vt('nch2369-galpon-grua/05', 'r_s', 2) }} }{2} = {{ vt('nch2369-galpon-grua/05', 'forma_T0_C', 5) }}$$

$$Q_0^{\text{máx}} = \frac{ {{ vt('nch2369-galpon-grua/05', 'c_max', 2) }} \cdot {{ vt('nch2369-galpon-grua/05', 'I', 2) }} \cdot {{ vt('nch2369-galpon-grua/05', 'A_r', 2) }} \cdot {{ vt('nch2369-galpon-grua/05', 'S_suelo', 2) }} }{ {{ vt('nch2369-galpon-grua/05', 'R_T7', 0) }} + 1} \cdot {{ vt('nch2369-galpon-grua/05', 'f_xi_pub', 5) }} \cdot {{ vt('nch2369-galpon-grua/05', 'P_sismico', 5) }} = {{ vt('nch2369-galpon-grua/05', 'Q0_max', 5) }}$$

→ **El techo de §5.13 es el espectro de diseño evaluado en $T_0$ con $R+1$ en vez de $R$**, y
la cláusula no lo dice. La identidad es exacta en los suelos A, B y C —los tres con
$r = {{ vt('nch2369-galpon-grua/05', 'r_s', 2) }}$— y falsa en los otros dos. El coeficiente
que ese techo deja es $C = {{ vt('nch2369-galpon-grua/05', 'C_dis', 5) }}$.

### D4 · Y en el suelo D de la otra serie el mismo techo queda 22 % más flojo

$$\frac{ {{ vt('nch2369-galpon-grua/05', 'c_max', 2) }} }{(1 + {{ vt('nch2369-galpon-grua/05', 'r_D', 2) }})/2} = \frac{ {{ vt('nch2369-galpon-grua/05', 'c_max', 2) }} }{ {{ vt('nch2369-galpon-grua/05', 'forma_T0_D', 2) }} } = {{ vt('nch2369-galpon-grua/05', 'exceso_D', 5) }}$$

→ Con $r = {{ vt('nch2369-galpon-grua/05', 'r_D', 2) }}$ el espectro en $T_0$ vale
{{ v('nch2369-galpon-grua/05', 'forma_T0_D', 2) }} veces $A_r S$ y la Ec. (13) sigue usando
{{ v('nch2369-galpon-grua/05', 'c_max', 2) }}: el techo queda **22,2 % por encima** del
espectro y muerde menos. En el suelo E la diferencia sube a 37,5 %. El mismo edificio en otro
suelo recibe un techo con otra holgura, y eso no está escrito en ninguna parte.

### D5 · Ninguna de las cinco excepciones aplica, y al tomar el recorte los dos cortes quedan iguales

{{ figura('nch2369-galpon-grua/05', 'corte-basal', 'Los dos cortes basales del análisis, 379,91535 kN en la dirección arriostrada y 362,90715 en la de marcos, contra el piso de 114,33862 kN y el techo de 302,41994, y las dos flechas de recorte que los llevan al mismo corte de diseño') }}

§5.13 no se puede aplicar en cinco casos: diseño por tiempo-historia, sistema con $R \le 2$,
sitio Tipo F, cláusula 13 en Categoría III o IV, y componentes de instalaciones generadoras de
energía. Este galpón es Categoría II, suelo C,
$R = {{ vt('nch2369-galpon-grua/05', 'R_T7', 0) }}$ y análisis modal espectral.

$$\frac{ {{ vt('nch2369-galpon-grua/05', 'Q0_X_an', 5) }} }{ {{ vt('nch2369-galpon-grua/05', 'Q0_max', 5) }} } = {{ vt('nch2369-galpon-grua/05', 'super_X', 5) }} \qquad \frac{ {{ vt('nch2369-galpon-grua/05', 'Q0_Y_an', 5) }} }{ {{ vt('nch2369-galpon-grua/05', 'Q0_max', 5) }} } = {{ vt('nch2369-galpon-grua/05', 'super_Y', 5) }}$$

→ Las dos direcciones superan el techo —25,6 % la arriostrada y 20,0 % la de marcos— y **el
recorte se toma**. Los dos cortes de diseño quedan en
**{{ v('nch2369-galpon-grua/05', 'Q0_X', 5) }} kN**, idénticos —la dirección de marcos publica
exactamente el mismo {{ v('nch2369-galpon-grua/05', 'Q0_Y', 5) }}—, porque la Ec. (13) usa el
$R$ de tabla y no el $R^{*}$, y la fila 5.5 le dio un solo $R$ al edificio. El techo borra la
diferencia entre direcciones que el 04 tardó un eslabón en construir.

## E · Cuánto de la grúa llega de verdad

### E1 · AIST acota la inercia de la grúa por el contacto rueda-riel

La grúa no está fija al edificio: se apoya en ruedas. Las cargas sísmicas asociadas al carro y
al puente están limitadas, en la dirección de traslación, por la máxima fuerza de tracción de
sus ruedas; y si los frenos están aplicados fuera de operación, por el coeficiente de roce
entre rueda y riel, que AIST estima conservadoramente en
{{ v('nch2369-galpon-grua/05', 'mu_roce', 1) }}.

$$F_{\text{grúa}} = {{ vt('nch2369-galpon-grua/05', 'C_dis_pub', 5) }} \cdot {{ vt('nch2369-galpon-grua/05', 'Wgrua_sc', 5) }} = {{ vt('nch2369-galpon-grua/05', 'F_grua', 5) }}$$

$$T_{\text{trac}} = {{ vt('nch2369-galpon-grua/05', 't32_tra', 2) }} \cdot {{ vt('nch2369-galpon-grua/05', 'Wgrua_sc', 5) }} = {{ vt('nch2369-galpon-grua/05', 'T_trac', 5) }} \qquad T_{\text{roce}} = {{ vt('nch2369-galpon-grua/05', 'mu_roce', 2) }} \cdot {{ vt('nch2369-galpon-grua/05', 'Wgrua_sc', 5) }} = {{ vt('nch2369-galpon-grua/05', 'T_roce', 5) }}$$

→ El sismo le pide a la grúa **{{ v('nch2369-galpon-grua/05', 'C_dis', 3) }} g**; sus ruedas
motrices solo pueden empujarla con **{{ v('nch2369-galpon-grua/05', 't32_tra', 2) }} g** y el
roce con **{{ v('nch2369-galpon-grua/05', 'mu_roce', 2) }} g**. Los dos topes están a los dos
lados de la demanda, así que cuál gobierna no lo decide la norma sino el estado de los frenos.

### E2 · Con frenos aplicados no gobierna ninguno, y con frenos sueltos la grúa aportaría 45 % menos

$$\frac{ {{ vt('nch2369-galpon-grua/05', 'F_grua', 5) }} }{ {{ vt('nch2369-galpon-grua/05', 'T_trac', 5) }} } = {{ vt('nch2369-galpon-grua/05', 'exc_trac', 5) }} \qquad \frac{ {{ vt('nch2369-galpon-grua/05', 'F_grua', 5) }} }{ {{ vt('nch2369-galpon-grua/05', 'T_roce', 5) }} } = {{ vt('nch2369-galpon-grua/05', 'uso_roce', 5) }}$$

→ Con los frenos aplicados (S5) el tope de roce queda **más del doble** por encima de la
demanda y **no recorta nada**: la grúa aporta sus
{{ v('nch2369-galpon-grua/05', 'F_grua', 2) }} kN enteros. Con los frenos sueltos gobernaría la
tracción y el aporte caería a {{ v('nch2369-galpon-grua/05', 'T_trac', 2) }} kN, un factor
{{ v('nch2369-galpon-grua/05', 'exc_trac', 5) }}, lo que bajaría el corte basal longitudinal un
**7,0 %**. Es un dato de operación decidiendo una fuerza de diseño, y NCh2369 no tiene la
cláusula.

## F · R1 y lo que la masa le pide al marco

### F1 · R1 es igual a R* porque el piso no gobierna

El factor de modificación de la respuesta efectivo es $R^{*}$ por el menor entre
$Q_0/Q_0^{\text{mín}}$ y 1. El recorte de §5.13 no entra en esta ecuación: la Ec. (14) solo
compara contra el **piso**.

$$R_{1X} = {{ vt('nch2369-galpon-grua/05', 'R_star_X', 5) }} \cdot \min({{ vt('nch2369-galpon-grua/05', 'holgura_X', 5) }} ; 1) = {{ vt('nch2369-galpon-grua/05', 'R1_X', 5) }}$$

$$R_{1Y} = {{ vt('nch2369-galpon-grua/05', 'R_star_Y', 5) }} \cdot \min({{ vt('nch2369-galpon-grua/05', 'holgura_Y', 5) }} ; 1) = {{ vt('nch2369-galpon-grua/05', 'R1_Y', 5) }}$$

→ Los dos $R_1$ quedan iguales a sus $R^{*}$. Que el recorte máximo no toque a $R_1$ tiene
consecuencia: las fuerzas bajan un 20-25 % y el multiplicador del diseño por capacidad no baja
nada.

### F2 · El amplificador de capacidad, y sobre qué fuerzas actúa

Los elementos que no son fusible se diseñan para la carga sísmica amplificada por $0{,}7R_1$,
con el $k_{\text{amp}}$ que el 01 fijó y este eslabón hereda.

$$ {{ vt('nch2369-galpon-grua/05', 'k_amp', 2) }} \cdot {{ vt('nch2369-galpon-grua/05', 'R1_X', 5) }} = {{ vt('nch2369-galpon-grua/05', 'kcap_X', 5) }} \qquad {{ vt('nch2369-galpon-grua/05', 'k_amp', 2) }} \cdot {{ vt('nch2369-galpon-grua/05', 'R1_Y', 5) }} = {{ vt('nch2369-galpon-grua/05', 'kcap_Y', 5) }}$$

$$ {{ vt('nch2369-galpon-grua/05', 'kcap_Y', 5) }} \cdot {{ vt('nch2369-galpon-grua/05', 'Q0_dis_pub', 5) }} = {{ vt('nch2369-galpon-grua/05', 'Q_amp_Y', 5) }}$$

→ **{{ v('nch2369-galpon-grua/05', 'kcap_X', 2) }} y
{{ v('nch2369-galpon-grua/05', 'kcap_Y', 2) }}**, aplicados sobre el corte ya recortado. En la
dirección de marcos el corte amplificado vale
{{ v('nch2369-galpon-grua/05', 'Q_amp_Y', 2) }} kN, tres veces y media el de diseño. Y como el
piso de §8.4.1 se mide contra la capacidad esperada del fusible y **no** contra la demanda,
recortar el corte hace que ese piso gobierne más seguido.

### F3 · La masa que este eslabón fija le pide al marco 10 % más de rigidez que la sección preliminar del 04

El período declarado en el 04, la masa fijada acá y la rigidez del marco son tres cosas que
tienen que cerrar entre sí. Con $P$ repartido en
{{ v('nch2369-galpon-grua/05', 'n_marcos', 0) }} marcos, el
$T^{*}_Y = {{ vt('nch2369-galpon-grua/05', 'T_star_Y', 2) }}$ s exige una rigidez lateral por
marco de:

$$k_Y = \frac{ {{ vt('nch2369-galpon-grua/05', 'P_sismico', 5) }} }{ {{ vt('nch2369-galpon-grua/05', 'n_marcos', 0) }} \cdot {{ vt('nch2369-galpon-grua/05', 'g_grav', 2) }} }\left(\frac{2 \cdot \pi}{ {{ vt('nch2369-galpon-grua/05', 'T_star_Y', 2) }} }\right)^{2} = {{ vt('nch2369-galpon-grua/05', 'k_req_Y', 5) }}\ \text{kN}/\text{m}$$

$$\frac{ {{ vt('nch2369-galpon-grua/05', 'k_req_Y', 5) }} }{ {{ vt('nch2369-galpon-grua/05', 'k_prel_Y', 5) }} } = {{ vt('nch2369-galpon-grua/05', 'raz_k', 5) }}$$

→ **10,3 % más** que los {{ v('nch2369-galpon-grua/05', 'k_prel_Y', 2) }} kN/m del marco
preliminar con que el arnés del 04 sostuvo la banda. El 07 tiene que entregar esa rigidez; si
no lo hace, el período sube a 0,42008 s, que sigue 1,50 veces sobre la frontera de
{{ v('nch2369-galpon-grua/05', 'Cr_T1', 2) }} s —así que la rama no cambia— y la ordenada de
referencia baja 1,6 %, del lado seguro.

El modelo del galpón, en cambio, ya está armado y da su propio período. Su modo dominante en la
dirección transversal es este; pulsa **Animar** para verlo moverse:

<rukan-visor src="../../../modelos/galpon-grua/galpon-grua.escena.json" modo="1" vista="transversal" animar></rukan-visor>

Su período es bastante menor que los {{ v('nch2369-galpon-grua/05', 'T_star_Y', 2) }} s
declarados, lo que quiere decir que el marco que el modelo lleva es **más rígido** que el que
esta cuenta pide. Cuál de los dos manda lo decide la cascada, y esta página todavía no la
toma: ver los límites.

## Veredicto

El peso sísmico vale **{{ v('nch2369-galpon-grua/05', 'P_sismico', 3) }} kN** y la grúa sin
carga, {{ v('nch2369-galpon-grua/05', 'Wgrua_sc', 2) }} kN, es el 22,2 % de él. La carga
suspendida queda fuera, y las dos normas llegan a eso por preguntas distintas: NCh2369 por el
régimen de operación, AIST por si la carga va rígidamente asegurada. No se contradicen; se
complementan, y un caso puede cumplir una y fallar la otra.

Los dos cortes del análisis difieren lo que el 04
anticipó —{{ v('nch2369-galpon-grua/05', 'Q0_X_an', 2) }} y
{{ v('nch2369-galpon-grua/05', 'Q0_Y_an', 2) }} kN— pero los dos superan el techo de §5.13 y,
al tomar el recorte, **quedan idénticos en
{{ v('nch2369-galpon-grua/05', 'Q0_X', 2) }} kN** (así lo publican
$Q_{0X} = {{ vt('nch2369-galpon-grua/05', 'Q0_X', 5) }}$ y
$Q_{0Y} = {{ vt('nch2369-galpon-grua/05', 'Q0_Y', 5) }}$). La razón es de estructura y no de
aritmética: la Ec. (13) usa el $R$ de tabla, y la fila 5.5 le dio un solo $R$ al edificio
entero. Y ese techo esconde una identidad que la cláusula no declara: su 2,75 es el espectro
de referencia evaluado en $T_0$, exacto en los suelos A, B y C y 22 % flojo en el D.

El piso de §5.12 no gobierna por {{ v('nch2369-galpon-grua/05', 'holgura_Y', 2) }}, así que
$R_1 = R^{*}$ —{{ v('nch2369-galpon-grua/05', 'R1_X', 2) }} y
{{ v('nch2369-galpon-grua/05', 'R1_Y', 2) }}— y el amplificador de capacidad vale
{{ v('nch2369-galpon-grua/05', 'kcap_X', 2) }} y
{{ v('nch2369-galpon-grua/05', 'kcap_Y', 2) }}. Lo que queda abierto para el 07 es una rigidez:
la masa fijada acá le pide al marco {{ v('nch2369-galpon-grua/05', 'k_req_Y', 2) }} kN/m,
10,3 % más que los {{ v('nch2369-galpon-grua/05', 'k_prel_Y', 2) }} kN/m de la sección
preliminar del 04. El 06 hereda además las áreas
({{ v('nch2369-galpon-grua/05', 'A_planta', 2) }} y
{{ v('nch2369-galpon-grua/05', 'A_muros', 2) }} m²), el peso del edificio
({{ v('nch2369-galpon-grua/05', 'W_edificio', 2) }} kN) y el coeficiente
{{ v('nch2369-galpon-grua/05', 'C_dis', 5) }}.

## Límites

- **Cuatro cargas permanentes son declaradas** (S1): cubierta, revestimiento, columnas y vigas
  carrileras. Juntas son el 58,6 % del peso del edificio, así que un despiece real las puede
  mover y con ellas todo lo que este eslabón publica. Lo que **no** se mueve es la estructura
  del resultado: el techo de §5.13 y el piso de §5.12 son proporcionales a $P$, igual que los
  cortes, así que las razones de D2 y D5 son invariantes.
- **La nieve en la masa sísmica es la mayor incertidumbre abierta** (S4). NCh2369 no la nombra
  y el umbral de {{ v('nch2369-galpon-grua/05', 'p_nieve_lim', 2) }} kN/m² que este eslabón
  adopta viene de la práctica norteamericana, **cuya norma no se abrió**: entra como supuesto y
  no como cláusula. Si la nieve entrara, sumaría
  {{ v('nch2369-galpon-grua/05', 'W_nieve', 2) }} kN —un 18,2 %— y todos los cortes subirían en
  esa proporción. La obligación de NCh3171 §9.1.1 que el 02 dejó abierta sigue abierta y es del
  06.
- **El período no se recalcula acá, y el modelo ya tiene el suyo.** F3 mide la incoherencia
  entre la masa de este eslabón y la sección preliminar del arnés del 04, y la deja como
  obligación del 07. El [00](../00-el-modelo/) publica además el período del modelo corrido,
  bastante menor que el declarado; tomarlo es la **cascada**, que se aplica como un cambio
  explícito después de migrar la serie completa. Hasta entonces esta página reproduce lo que el
  memo original publicó.
- **El recorte de §5.13 no se aplica a los desplazamientos**, y la cláusula lo dice con esas
  palabras. El 06 calcula la deriva con el corte **sin** recortar, así que fuerzas y
  desplazamientos van a estar en escalas distintas a propósito.
- **El tope de AIST §3.11.2 no se toma** (S5). Con frenos sueltos recortaría el corte
  longitudinal un 7,0 %, y la decisión depende de un dato de operación que ninguna de las dos
  normas pide documentar.
- **No se reparte el corte en altura.** El galpón es de un nivel y §5.5.2 no tiene qué
  distribuir; el reparto entre marcos —que es lo que la posición más desfavorable de la grúa
  decide— es del 11 y del 12, con el arriostramiento de techo como diafragma.
- **No se evalúa el péndulo.** C12.1.3 advierte que la carga suspendida tiene período propio y
  puede acoplarse con los modos del edificio; despreciar la carga (C1) también desprecia ese
  acoplamiento. Con la grúa descargada la mayor parte del turno, el caso no se construye, pero
  la advertencia queda escrita.
- **Un dígito del memo original no reproduce.** El memo imprimió
  `k_req_Y = 5 216,93102` kN/m donde el valor es
  {{ v('nch2369-galpon-grua/05', 'k_req_Y', 5) }}: el último decimal está truncado en vez de
  redondeado. El arnés del repo de memos comparaba con tolerancia **relativa** y no lo veía;
  acá la tolerancia es absoluta, media unidad del último decimal, así que el oráculo de esta
  página se escribe con los cuatro decimales que el memo sí acertó. No cambia nada del
  resultado y se deja anotado.

## Ficha

{{ ficha('nch2369-galpon-grua/05') }}

## Referencias

| Clave | Norma y edición | Cláusula | Leída en | Cita textual |
|---|---|---|---|---|
| NCh-p1 | NCh2369:2025 (3.ª ed.) | §5.1.2, qué incluye la masa sísmica | `Normas/NCh 2369 - 3°Edición 2025.05.28.pdf`, p. 26 | «debe incluir las cargas permanentes del sistema y una fracción de las sobrecargas, de acuerdo con el valor esperado, o su probabilidad de ocurrencia simultánea, con el sismo de diseño» |
| NCh-p2 | NCh2369:2025 (3.ª ed.) | §5.1.2, la lista de tres filas — sin fila para techos | PDF ídem, p. 26 | «Bodegas, salas de archivo y similares: 50%» |
| NCh-p3 | NCh2369:2025 (3.ª ed.) | C5.4.1, la obligación de que el período adoptado maximice la respuesta — la que F3 mide | PDF ídem, p. 35 | «es necesario verificar que el período de vibración adoptado para el cálculo de R *, sea representativo y maximice la respuesta de la estructura» |
| NCh-p4 | NCh2369:2025 (3.ª ed.) | §5.4.2 y Ec. (3), el espectro de referencia cuya forma en $T_0$ es el 2,75 de D3 — **mirada en PNG**, no extraída | PDF ídem, p. 36 | «Se define el siguiente espectro de referencia para la dirección horizontal» |
| NCh-p5 | NCh2369:2025 (3.ª ed.) | §5.5.1 y Ec. (5), el corte basal y la definición del coeficiente sísmico | PDF ídem, p. 38 | «coeficiente sísmico calculado como el valor del espectro de diseño para la dirección horizontal» |
| NCh-p6 | NCh2369:2025 (3.ª ed.) | §5.12 y Ec. (12), el piso del corte basal y que el aumento no va a desplazamientos | PDF ídem, p. 55 | «Este aumento no se debe aplicar al cálculo de desplazamientos» |
| NCh-p7 | NCh2369:2025 (3.ª ed.) | C5.12.1, que ningún método permite bajar del mínimo | PDF ídem, p. 55 | «no permite el diseño de estructuras cuya resistencia lateral sea inferior al valor de» |
| NCh-p8 | NCh2369:2025 (3.ª ed.) | §5.13 y Ec. (13), el techo opcional — **mirada en PNG**, no extraída | PDF ídem, p. 56 | «se pueden multiplicar por el cociente» |
| NCh-p9 | NCh2369:2025 (3.ª ed.) | §5.13, las cinco condiciones en que la cláusula no aplica | PDF ídem, p. 56 | «cuyo sistema sismorresistente se diseñe con R menor o igual a 2» |
| NCh-p10 | NCh2369:2025 (3.ª ed.) | §5.14 y Ec. (14), la definición de $R_1$ | PDF ídem, p. 56 | «Factor de modificación de la respuesta estructural efectivo» |
| NCh-p11 | NCh2369:2025 (3.ª ed.) | Tabla 6, las filas de los suelos C y D que D3 y D4 contrastan — **mirada en PNG**, no extraída | PDF ídem, p. 67 | «C 1,05 4,50 0,40 1,50 3,00 0,35» |
| NCh-p12 | NCh2369:2025 (3.ª ed.) | §8.3.4, la amplificación de la carga sísmica horizontal por $0{,}7R_1$ | PDF ídem, p. 88 | «La resistencia requerida de las columnas se debe determinar utilizando las combinaciones de cargas definidas en 4.5» |
| NCh-p13 | NCh2369:2025 (3.ª ed.) | §12.1.3, con qué carga suspendida se hace el análisis sísmico | PDF ídem, p. 150 | «considerando las magnitudes y alturas de carga suspendida más probables durante el terremoto de diseño» |
| NCh-p14 | NCh2369:2025 (3.ª ed.) | C12.1.3, la exención de las grúas de mantención y la advertencia del péndulo | PDF ídem, p. 150 | «rara vez se levanta la carga máxima y la operación no es continua, se puede despreciar la carga suspendida para el análisis sísmico» |
| NCh-p15 | NCh2369:2025 (3.ª ed.) | §12.1.4 y C12.1.4, todas las grúas sin carga en la posición más desfavorable y de dónde viene la regla | PDF ídem, p. 151 | «una combinación de cargas sísmicas con todas las grúas sin carga estacionadas en la posición más desfavorable» |
| AIST-1 | AIST TR-13:2021 | §3.6, la masa sísmica de la grúa y la condición de la carga rígidamente asegurada | `Normas/aist-tr-no13-2021-3.pdf`, p. 19 | «The seismic mass associated with cranes supporting a suspended load need not include the weight of the suspended load» |
| AIST-2 | AIST TR-13:2021 | §3.6, la condición que invierte el resultado | PDF ídem, p. 19 | «if the lifted load is rigidly secured to the crane during crane travel, the lifted load shall be included in the seismic mass» |
| AIST-3 | AIST TR-13:2021 | §3.11.2, qué entra en la carga muerta sísmica y una sola grúa por nave | PDF ídem, p. 22 | «include dead weight of building structure, supported equipment, the dead load of a single crane in each crane aisle positioned to generate the worst-case effect» |
| AIST-4 | AIST TR-13:2021 | §3.11.2, el tope por tracción de las ruedas | PDF ídem, p. 22 | «limited in the direction of travel for trolley and bridge by the maximum tractive force associated with the crane/bridge wheels» |
| AIST-5 | AIST TR-13:2021 | §3.11.2, el tope por roce con los frenos aplicados y el 0,6 | PDF ídem, p. 22 | «limited by the coefficient of friction between the crane wheel and rail» |
| N431 | NCh431:2010 | §4, el umbral desde el que la nieve es sobrecarga normal — **PDF escaneado, leído a ojo** | `Normas/nch-431-2010.pdf`, p. 8 | «la carga básica de nieve, es mayor que 0,25 kN/m2 la sobrecarga de nieve se considera normal» |
| NCh-4 | NCh2369:2025 (3.ª ed.) | §4.5 y Tabla C-2, el factor $a$ con su fila de pasarelas y techos, que es la que S3 usa | `referencias/NCh2369-2025/cap04-disposiciones-generales.md` | — |
