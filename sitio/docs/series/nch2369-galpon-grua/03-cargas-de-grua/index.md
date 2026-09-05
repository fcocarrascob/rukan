# 03 · Cargas de puente grúa

El empuje lateral de un puente grúa no sale de una fórmula: sale del **mayor de tres reglas**
que AIST impone a la vez, y las tres crecen con magnitudes distintas, así que cuál gobierna
hay que evaluarlo. Y hay dos juegos de factores que se parecen y no son el mismo: el impacto
del 20 % carga al edificio, mientras el `HLF` y el `DLF` de CMAA cargan a la grúa. Este
eslabón fija la clase de servicio, las reacciones de rueda, el impacto vertical, el empuje
lateral y la tracción longitudinal. Fuerzas en kN, longitudes en m.

## El caso

{{ figura('nch2369-galpon-grua/03', 'reacciones-de-rueda', 'Elevación del puente grúa sobre las dos vigas carrileras con el carro en su posición más desfavorable, a 1,20 m del riel: la reacción máxima de rueda de 161,23913 kN en el testero cargado y la mínima de 53,76087 en el opuesto, con la separación de ruedas de 3,40 m') }}

| Dato | Valor |
|---|---|
| Tipo | Puente grúa birriel, **sin cabina**, radio-operado desde el piso (S1) |
| Capacidad nominal | {{ v('nch2369-galpon-grua/03', 'Qn_grua', 2) }} kN (del 01) |
| Luz del puente | {{ v('nch2369-galpon-grua/03', 'Lg_grua', 2) }} m (del 01) |
| Peso del puente | {{ v('nch2369-galpon-grua/03', 'Wb_puente', 2) }} kN (S2) |
| Peso del carro con su equipo de izaje | {{ v('nch2369-galpon-grua/03', 'Wt_carro', 2) }} kN (S2) |
| Ruedas | {{ v('nch2369-galpon-grua/03', 'n_ruedas', 0) }}, dos por testero, **todas motrices** (S2) |
| Separación de ruedas por testero | {{ v('nch2369-galpon-grua/03', 'wb_ruedas', 2) }} m (S2) |
| Aproximación mínima del gancho al riel | {{ v('nch2369-galpon-grua/03', 'a_gancho', 2) }} m (S2) |
| Velocidad de izaje | {{ v('nch2369-galpon-grua/03', 'v_izaje', 2) }} m/min (S3) |
| Velocidad de traslación del puente | {{ v('nch2369-galpon-grua/03', 'v_tras', 2) }} m/min (S3) |
| Régimen de operación | {{ v('nch2369-galpon-grua/03', 'izajes_h', 0) }} izajes/hora · {{ v('nch2369-galpon-grua/03', 'h_dia', 0) }} h/día · {{ v('nch2369-galpon-grua/03', 'dias_ano', 0) }} días/año · {{ v('nch2369-galpon-grua/03', 'vida_grua', 0) }} años (S4) |
| Separación de marcos, luz de la carrilera | {{ v('nch2369-galpon-grua/03', 's_marco', 2) }} m (del 01) |
| Lo que se decide aquí | la clase de servicio, las reacciones de rueda y las tres componentes de carga |

Los supuestos, en una línea cada uno. **S1**, la grúa es birriel, sin cabina y radio-operada;
las dos últimas cosas importan y en direcciones opuestas: «sin cabina» es lo que puso el tope
de §12.2.1 e) en {{ v('nch2369-galpon-grua/01', 'Qn_lim', 0) }} kN en vez de
{{ v('nch2369-galpon-grua/01', 'Qn_lim_cab', 0) }} (el 01), y «radio-operada» hace que AIST
§3.7.2 la trate **como si tuviera cabina** para impacto, empuje lateral y tracción; una grúa
de botonera tendría 10 % / 10 % / 20 % fijos en vez de la Tabla 3.2 y sus tres reglas. **S2**,
los pesos, las ruedas y la aproximación del gancho son declarados, no de una ficha de
fabricante: {{ v('nch2369-galpon-grua/03', 'Wb_puente', 2) }} kN de puente y
{{ v('nch2369-galpon-grua/03', 'Wt_carro', 2) }} kN de carro son valores corrientes para una
birriel de {{ v('nch2369-galpon-grua/03', 'Qn_grua', 2) }} kN y
{{ v('nch2369-galpon-grua/03', 'Lg_grua', 2) }} m de luz, y se declaran cuatro ruedas motrices
porque es la configuración con tracción en ambos testeros. **S3**, las velocidades son
declaradas y corresponden a la Inquiry Data Sheet de CMAA §70-6 para esta capacidad; solo
entran en el `HLF` y el `DLF` de C2 y C3, que son factores de la grúa y no viajan al edificio.
**S4**, el régimen de operación es dato de proceso, y es lo único que decide la clase de
servicio: A3 muestra que un régimen de jornada completa la movería una letra. **S5**, la fila
de la Tabla 3.2 que corresponde es «Motor room maintenance cranes, etc.», con
{{ v('nch2369-galpon-grua/03', 't32_imp', 0, 100) }} % /
{{ v('nch2369-galpon-grua/03', 't32_emp', 0, 100) }} % /
{{ v('nch2369-galpon-grua/03', 't32_tra', 0, 100) }} %; la tabla está escrita para grúas de
acería —cuchara, almeja, imán, foso— y ninguna fila describe un galpón de mantención, así que
se toma la más cercana en régimen. **S6**, el empuje lateral se reparte por igual entre las
dos vigas carrileras, que es lo que §3.7.2 pide «con la debida consideración a la rigidez
lateral de cada estructura que soporta los rieles» cuando las dos líneas de columnas son
iguales por simetría.

## A · La clase de servicio, que no es un atributo de la grúa

### A1 · Los ciclos salen del régimen, no del catálogo

La clasificación de servicio se basa en el espectro de carga que refleja las condiciones
reales de servicio. Los ciclos se agrupan en cuatro rangos, de los que `N1` va de 20 000 a
100 000.

$$N = {{ vt('nch2369-galpon-grua/03', 'izajes_h', 0) }} \cdot {{ vt('nch2369-galpon-grua/03', 'h_dia', 0) }} \cdot {{ vt('nch2369-galpon-grua/03', 'dias_ano', 0) }} \cdot {{ vt('nch2369-galpon-grua/03', 'vida_grua', 0) }} = {{ vt('nch2369-galpon-grua/03', 'N_ciclos', 0) }}$$

→ **{{ v('nch2369-galpon-grua/03', 'N_ciclos', 0) }} ciclos**, dentro de `N1`. Un galpón de
mantención no acumula ciclos: la grúa está detenida la mayor parte del turno.

### A2 · Y la clase de carga, de cuánto se levanta respecto de la nominal

La clase `L3` corresponde a grúas que izan la carga nominal con cierta frecuencia y
habitualmente cargas entre un tercio y dos tercios de la nominal.

$$\frac{1}{3} < 0{,}50 < \frac{2}{3}$$

→ **`L3`.** La carga habitual declarada, la mitad de la nominal, cae dentro del rango de esa
clase y no del de `L2`.

### A3 · El cruce da Clase C, y un turno completo la movería a D

La Tabla 2.8-1 cruza clase de carga con rango de ciclos. La fila `L3` da `C` en `N1`, `D` en
`N2`, `E` en `N3` y `F` en `N4`.

$$N_{\text{jornada}} = 8 \cdot 8 \cdot {{ vt('nch2369-galpon-grua/03', 'dias_ano', 0) }} \cdot {{ vt('nch2369-galpon-grua/03', 'vida_grua', 0) }} = {{ vt('nch2369-galpon-grua/03', 'N_jornada', 0) }}$$

→ **Clase C** con el régimen declarado. Pero 8 izajes por hora en jornada completa dan
{{ v('nch2369-galpon-grua/03', 'N_jornada', 0) }} ciclos, que es `N2`, y la misma fila `L3`
daría **Clase D**. La clase de servicio la fija el uso, no la grúa, y el 09 la va a necesitar
para la fatiga.

## B · Las reacciones de rueda

### B1 · La posición que gobierna es el carro contra el tope

El carro y su carga se ubican a la aproximación mínima del gancho, y el puente reparte su
propio peso por igual entre los dos testeros. Las vigas carrileras y su estructura de soporte
se diseñan para las cargas máximas de rueda.

$$R_{\text{test}} = (Q_n + W_t)\frac{L_g - a}{L_g} + \frac{W_b}{2} = 240{,}00 \cdot \frac{21{,}80}{ {{ vt('nch2369-galpon-grua/03', 'Lg_grua', 2) }} } + 95{,}00 = {{ vt('nch2369-galpon-grua/03', 'R_test', 5) }}$$

→ **{{ v('nch2369-galpon-grua/03', 'R_test', 5) }} kN** por testero, el 75 % del peso total
sobre los rieles.

### B2 · Y por rueda, la mitad

Cada testero apoya en dos ruedas.

$$R_{w} = \frac{R_{\text{test}}}{2} = \frac{ {{ vt('nch2369-galpon-grua/03', 'R_test', 5) }} }{2} = {{ vt('nch2369-galpon-grua/03', 'Rw_max', 5) }}$$

→ **{{ v('nch2369-galpon-grua/03', 'Rw_max', 5) }} kN.** Es el número que el 08 va a usar para
la viga carrilera y el 10 para la ménsula.

### B3 · El testero opuesto lleva el resto, y la suma cierra

Con el carro en un extremo, el testero lejano recibe el complemento. La suma de los dos tiene
que dar el peso total sobre los rieles, y es el único control de equilibrio que este paso
admite.

$$R_{\text{test}} + R_{\text{test,mín}} = {{ vt('nch2369-galpon-grua/03', 'R_test', 5) }} + {{ vt('nch2369-galpon-grua/03', 'R_test_min', 5) }} = {{ vt('nch2369-galpon-grua/03', 'R_suma', 5) }}$$

→ **{{ v('nch2369-galpon-grua/03', 'W_tot', 2) }} kN**, que es $Q_n + W_t + W_b$ exactamente.
La rueda descargada queda en {{ v('nch2369-galpon-grua/03', 'Rw_min', 5) }} kN,
{{ v('nch2369-galpon-grua/03', 'raz_ruedas', 2) }} veces menos que la cargada.

## C · El impacto vertical, y los dos factores que no son él

### C1 · El impacto que carga al edificio es el 20 % de la Tabla 3.2

El impacto vertical y las fuerzas de tracción deben ser un porcentaje supuesto de las cargas
máximas de rueda, según la Tabla 3.2.

$$R_{v} = (1 + {{ vt('nch2369-galpon-grua/03', 't32_imp', 2) }})\,R_{w} = 1{,}20 \cdot {{ vt('nch2369-galpon-grua/03', 'Rw_max', 5) }} = {{ vt('nch2369-galpon-grua/03', 'Rv_max', 5) }}$$

→ **{{ v('nch2369-galpon-grua/03', 'Rv_max', 5) }} kN.** Es la reacción con que se dimensiona
la viga carrilera por resistencia.

### C2 · Pero CMAA tiene su propio factor de izaje, y es otro número por otra razón

El factor de carga de izaje `HLF` se aplica a la carga izada en dirección vertical y vale
medio por ciento de la velocidad de izaje en pies por minuto, no menos de 15 % ni más de
50 %.

$$0{,}005 \cdot {{ vt('nch2369-galpon-grua/03', 'v_izaje_fpm', 5) }} = {{ vt('nch2369-galpon-grua/03', 'HLF_bruto', 5) }}$$

→ Cae bajo el piso, así que **`HLF` = {{ v('nch2369-galpon-grua/03', 'HLF', 2) }}**. Y no
reemplaza al {{ v('nch2369-galpon-grua/03', 't32_imp', 0, 100) }} % de C1: el `HLF` dimensiona
**la grúa** y el impacto de AIST dimensiona **el edificio**. Son dos normas distintas
resolviendo dos problemas distintos con nombres parecidos.

### C3 · Y un factor de peso propio, que tampoco viaja

El factor de carga muerta `DLF` cubre solo los pesos propios de la grúa, el carro y su equipo.

$$1{,}05 + \frac{ {{ vt('nch2369-galpon-grua/03', 'v_tras_fpm', 5) }} }{2000} = {{ vt('nch2369-galpon-grua/03', 'DLF_bruto', 5) }}$$

→ Cae bajo su piso de {{ v('nch2369-galpon-grua/03', 'DLF_piso', 2) }}, así que
**`DLF` = {{ v('nch2369-galpon-grua/03', 'DLF', 2) }}**. Con la velocidad de traslación
declarada, los dos factores de CMAA quedan **en su valor mínimo**: la grúa es lenta.

## D · El empuje lateral: tres reglas simultáneas

### D1 · AIST impone tres, y hay que evaluarlas todas

El empuje lateral total debe ser el mayor de: el de la Tabla 3.2; el 20 % del peso combinado
de la carga izada y el carro; y el 10 % del peso combinado de la carga izada y el peso total
de la grúa.

$$SS_1 = {{ vt('nch2369-galpon-grua/03', 't32_emp', 2) }}\,Q_n = {{ vt('nch2369-galpon-grua/03', 't32_emp', 2) }} \cdot {{ vt('nch2369-galpon-grua/03', 'Qn_grua', 2) }} = {{ vt('nch2369-galpon-grua/03', 'SS_1', 5) }}$$

→ La primera rama, la de la fila «Motor room maintenance», da
**{{ v('nch2369-galpon-grua/03', 'SS_1', 2) }} kN**. Las otras dos:
$0{,}20 \cdot 240{,}00 = {{ vt('nch2369-galpon-grua/03', 'SS_2', 2) }}$ y
$0{,}10 \cdot {{ vt('nch2369-galpon-grua/03', 'W_tot', 2) }} = {{ vt('nch2369-galpon-grua/03', 'SS_3', 2) }}$.

### D2 · Gobierna la primera, y por un margen que no es evidente

$$\frac{SS_1}{SS_2} = \frac{ {{ vt('nch2369-galpon-grua/03', 'SS_1', 5) }} }{ {{ vt('nch2369-galpon-grua/03', 'SS_2', 5) }} } = {{ vt('nch2369-galpon-grua/03', 'raz_SS12', 5) }}$$

→ La rama de la Tabla 3.2 supera a la del carro un **25 %**, y a la del peso total un 39,5 %:
ese segundo cociente vale {{ v('nch2369-galpon-grua/03', 'raz_SS13', 5) }}. Pero las tres
crecen con cosas distintas —la
nominal, el carro, la grúa entera—, así que **cuál manda no se puede anticipar**: un carro más
pesado o un puente más pesado invierten el orden sin cambiar la capacidad. El total es el
máximo de las tres: **{{ v('nch2369-galpon-grua/03', 'SS_total', 5) }} kN**.

### D3 · Y se reparte entre las dos carrileras

$$SS_{\text{carril}} = \frac{ {{ vt('nch2369-galpon-grua/03', 'SS_total', 5) }} }{2} = {{ vt('nch2369-galpon-grua/03', 'SS_carril', 5) }}$$

→ **{{ v('nch2369-galpon-grua/03', 'SS_carril', 2) }} kN por carrilera** y 15,00 kN por rueda,
aplicados horizontalmente en la cabeza del riel. Es lo que el 08 combina con la flexión
vertical y lo que el 12 lleva al arriostramiento.

## E · La tracción longitudinal

### E1 · Es el 20 % de lo que cargan las ruedas motrices

La fuerza de tracción es un porcentaje de la carga máxima sobre las ruedas motrices, según la
Tabla 3.2.

$$T = {{ vt('nch2369-galpon-grua/03', 't32_tra', 2) }}\,(Q_n + W_t + W_b) = {{ vt('nch2369-galpon-grua/03', 't32_tra', 2) }} \cdot {{ vt('nch2369-galpon-grua/03', 'W_tot', 2) }} = {{ vt('nch2369-galpon-grua/03', 'T_long', 5) }}$$

→ **{{ v('nch2369-galpon-grua/03', 'T_long', 2) }} kN** longitudinales, repartidos entre las
dos carrileras. Con las {{ v('nch2369-galpon-grua/03', 'n_ruedas', 0) }} ruedas motrices, la
carga sobre las motrices es el peso total sobre los rieles.

### E2 · Y va al mismo sistema que ya tiene dos vanos menos

La tracción es longitudinal, o sea paralela a la carrilera, y termina en el mismo
arriostramiento vertical que el 01 dejó reducido a dos vanos de cuatro.

$$\frac{T}{SS_{\text{total}}} = \frac{ {{ vt('nch2369-galpon-grua/03', 'T_long', 5) }} }{ {{ vt('nch2369-galpon-grua/03', 'SS_total', 5) }} } = {{ vt('nch2369-galpon-grua/03', 'raz_TS', 5) }}$$

→ La longitudinal es **{{ v('nch2369-galpon-grua/03', 'raz_TS', 2) }} veces** la transversal, y
entra a un sistema con la mitad de los vanos arriostrados. El 12 lo evalúa.

## F · Lo que CMAA no cubre, y NCh2369 sí

### F1 · CMAA declara en su propio texto que no considera el sismo

Las fuerzas sísmicas no se consideran en esa especificación de diseño; si se requieren, las
aceleraciones deben ser especificadas al nivel del riel por el propietario o el especificador.

$$n_{\text{cláusulas sísmicas de CMAA}} = {{ vt('nch2369-galpon-grua/03', 'n_sismo_cmaa', 0) }}$$

→ La norma que diseña la grúa **se declara incompetente** en sismo y devuelve la pelota. En
Chile quien la recoge es NCh2369 §12.1.3 a §12.1.5.

### F2 · Y las tres cláusulas que la recogen no están en el mismo lugar

§12.1.3 fija con qué carga suspendida se hace el análisis sísmico; §12.1.4 obliga a considerar
todas las grúas sin carga estacionadas en la posición más desfavorable; §12.1.5 exige
dispositivos anticaída si el análisis como equipo móvil de §11.6 indica levantamientos.

$$n_{\text{cláusulas}} = {{ vt('nch2369-galpon-grua/03', 'n_clausulas', 0) }}$$

→ **Tres**, y ninguna produce un número que este eslabón pueda publicar: la primera la
resuelve el 05 con la masa sísmica, y las otras dos son requisitos de combinación y de
detallamiento.

## Veredicto

La rueda más cargada entrega **{{ v('nch2369-galpon-grua/03', 'Rw_max', 5) }} kN**, que con el
{{ v('nch2369-galpon-grua/03', 't32_imp', 0, 100) }} % de impacto de la Tabla 3.2 suben a
**{{ v('nch2369-galpon-grua/03', 'Rv_max', 5) }}**; la descargada queda en
{{ v('nch2369-galpon-grua/03', 'Rw_min', 5) }}. El empuje lateral total vale
**{{ v('nch2369-galpon-grua/03', 'SS_total', 5) }} kN**, o sea
{{ v('nch2369-galpon-grua/03', 'SS_carril', 5) }} por carrilera, y lo fija la primera de las
tres reglas que AIST §3.7.2 impone simultáneamente, con 25 % de margen sobre la segunda; como
las tres crecen con magnitudes distintas, cuál gobierna hay que evaluarlo y no se puede
suponer. La tracción longitudinal, **{{ v('nch2369-galpon-grua/03', 'T_long', 5) }} kN**, es
{{ v('nch2369-galpon-grua/03', 'raz_TS', 2) }} veces la transversal y descarga en el sistema
arriostrado que el 01 dejó con dos vanos de cuatro.

Lo que este eslabón separa y conviene no volver a mezclar: **el
{{ v('nch2369-galpon-grua/03', 't32_imp', 0, 100) }} % de impacto de AIST carga al edificio; el
`HLF` de {{ v('nch2369-galpon-grua/03', 'HLF', 2) }} y el `DLF` de
{{ v('nch2369-galpon-grua/03', 'DLF', 2) }} de CMAA cargan a la grúa**. Y el
{{ v('nch2369-galpon-grua/03', 'cmaa_lat', 0, 100) }} % de CMAA §1.4.6, que es un tercio del
{{ v('nch2369-galpon-grua/03', 't32_emp', 0, 100) }} % de AIST, no es una tercera opinión sobre
la misma fuerza: es la fuerza de **servicio** con que se comprueba la flecha lateral, contra la
de **resistencia** con que se dimensiona.

Hacia adelante: el 05 hereda {{ v('nch2369-galpon-grua/03', 'Wb_puente', 2) }} y
{{ v('nch2369-galpon-grua/03', 'Wt_carro', 2) }} para la masa sísmica, el 06 la separación de
ruedas {{ v('nch2369-galpon-grua/03', 'wb_ruedas', 2) }} m, y el 09 los
{{ v('nch2369-galpon-grua/03', 'N_ciclos', 0) }} ciclos de los
{{ v('nch2369-galpon-grua/03', 'vida_grua', 0) }} años para la fatiga.

## Límites

- **No hay ficha de fabricante.** Pesos de puente y carro, número y separación de ruedas,
  aproximación del gancho y velocidades son declarados (S2, S3). Los que gobiernan resultados
  son los pesos: cambiarlos mueve las reacciones de rueda proporcionalmente y puede invertir
  cuál de las tres ramas del empuje lateral gobierna. Una ficha real los reemplaza sin cambiar
  ningún paso de este eslabón.
- **La fila de la Tabla 3.2 es una elección, no una lectura.** AIST TR-13 es una guía de
  *mill buildings* y su Tabla 3.2 lista grúas de acería. «Motor room maintenance cranes» es la
  más cercana a un galpón de mantención, pero no lo describe. «Mill cranes» daría
  {{ v('nch2369-galpon-grua/03', 'mill_imp', 0, 100) }} % de impacto y
  {{ v('nch2369-galpon-grua/03', 'mill_emp', 0, 100) }} % de empuje lateral: un 33 % más de
  empuje, que sí cambiaría el resultado.
- **El *skewing* de CMAA §3.3.2.2.2 no se evalúa.** Su coeficiente sale de un gráfico contra la
  razón luz/base de ruedas, que acá vale
  {{ v('nch2369-galpon-grua/03', 'raz_luz_base', 5) }}, y es una carga sobre la **grúa**, no
  sobre el edificio. No entra en la ficha.
- **Nada de lo sísmico se resuelve acá.** §12.1.3 —con qué carga suspendida se analiza— lo
  decide el 05; §12.1.4 —todas las grúas sin carga en la posición más desfavorable— es una
  combinación del 06; §12.1.5 —anticaída si §11.6 indica levantamiento— no tiene eslabón
  asignado todavía.
- **Las flechas admisibles se publican como criterio, no como verificación.** `L/600` y `L/400`
  sobre la luz de la carrilera dan {{ v('nch2369-galpon-grua/03', 'flecha_v', 2) }} y
  {{ v('nch2369-galpon-grua/03', 'flecha_l', 2) }} mm, y la fuerza lateral de servicio de CMAA,
  {{ v('nch2369-galpon-grua/03', 'lat_servicio', 5) }} kN, es
  {{ v('nch2369-galpon-grua/03', 'raz_aist_cmaa', 0) }} veces menor que el empuje de AIST; pero
  comprobarlas necesita la sección de la viga, que es del 08. ICHA Tabla 15.3.1 ofrece además
  `1/1000` para portagrúas citando AISE Std. 13; ese contraste lo resuelve el 08.
- **Una sola grúa.** §12.1.4 contempla varias en una nave o en naves paralelas; acá hay una,
  así que no hay combinación de posiciones que armar.
- **No hay modelo en este eslabón.** Las cargas se entregan como fuerzas; ponerlas sobre la
  carrilera y sobre el marco es del 07 y del 08, y los esfuerzos que producen se verán sobre el
  modelo cuando exista la segunda versión de la escena.

## Ficha

{{ ficha('nch2369-galpon-grua/03') }}

## Referencias

| Clave | Norma y edición | Cláusula | Leída en | Cita textual |
|---|---|---|---|---|
| AIST-1 | AIST TR-13:2021 | §3.7.1, de dónde salen las cargas de rueda y para qué se diseña la carrilera | `Normas/aist-tr-no13-2021-3.pdf`, p. 19 | «Crane runway girders and supporting framework shall be designed for the maximum crane wheel loads» |
| AIST-2 | AIST TR-13:2021 | §3.7.2, el impacto y la tracción como porcentaje de la Tabla 3.2 | PDF ídem, p. 19 | «Vertical impact and tractive forces shall be an assumed percentage of the maximum wheel loads as specified in Table 3.2» |
| AIST-3 | AIST TR-13:2021 | §3.7.2, las tres reglas del empuje lateral y el criterio del mayor | PDF ídem, p. 19 | «The total side thrust should be distributed with due regard for the lateral stiffness of each structure supporting the rails and shall be the greater of» |
| AIST-4 | AIST TR-13:2021 | §3.7.2, la segunda y tercera rama | PDF ídem, p. 19 | «20% of the combined weight of the lifted load and trolley» |
| AIST-5 | AIST TR-13:2021 | §3.7.2, cómo se tratan las radio-operadas | PDF ídem, p. 19 | «Radio-operated cranes, as well as fully autonomous cranes, shall be considered the same as cab-operated cranes» |
| AIST-6 | AIST TR-13:2021 | §3.7.2, qué incluye la carga izada | PDF ídem, p. 19 | «a total weight lifted by the hoist mechanism, including working load, all hooks, lifting beams» |
| AIST-7 | AIST TR-13:2021 | Tabla 3.2, la fila de mantención — **mirada en PNG**, no extraída | PDF ídem, p. 20 | «Note 2: Side thrust should be distributed with due regard for lateral stiffness of the structure supporting the rail» |
| CMAA-1 | CMAA 70:2010 | §2.1.2 y §2.8 con la Tabla 2.8-1 — **mirada en PNG** | `Normas/cmaa-70.pdf`, pp. 13-14 | «The crane service classification is based on the load spectrum reflecting the actual service conditions as closely as possible» |
| CMAA-2 | CMAA 70:2010 | §2.4, la definición de la Clase C | PDF ídem, p. 13 | «This service covers cranes which may be used in machine shops or paper mill machine rooms» |
| CMAA-3 | CMAA 70:2010 | §2.8, las clases de carga L3 y los rangos de ciclos | PDF ídem, p. 14 | «Cranes which hoist the rated load fairly frequently and normally, loads between» |
| CMAA-4 | CMAA 70:2010 | §3.3.2, el alcance de las cargas y la exclusión del sismo | PDF ídem, p. 15 | «Seismic forces are not considered in this design Specification» |
| CMAA-5 | CMAA 70:2010 | §3.3.2.1.4.2, el factor de carga de izaje y sus dos topes | PDF ídem, p. 16 | «shall be 0.5 percent of the hoisting speed in feet per minute, but not less than 15 percent nor more than 50 percent» |
| CMAA-6 | CMAA 70:2010 | §3.3.2.1.4.1, el factor de carga muerta | PDF ídem, p. 16 | «This factor covers only the dead loads of the crane, trolley and its associated equipment» |
| CMAA-7 | CMAA 70:2010 | §1.4.6, las flechas admisibles de la carrilera y el 10 % de servicio | PDF ídem, p. 8 | «The lateral deflection should not exceed» |
| CMAA-8 | CMAA 70:2010 | §3.3.2.2.2, el *skewing* que este memo no evalúa | PDF ídem, p. 17 | «When two wheels (or two bogies) roll along a rail the horizontal forces normal to the rail» |
| NCh-12 | NCh2369:2025 (3.ª ed.) | §12.1.3, §12.1.4 y §12.1.5, lo sísmico que CMAA devuelve | `referencias/NCh2369-2025/cap12-estructuras-especificas.md` | — |
| ICHA | ICHA 2010, Manual de Diseño para Estructuras de Acero | Tabla 15.3.1, las flechas de portagrúas y su procedencia | `referencias/ICHA-2010/cap15-servicio-deformaciones-y-vibraciones.md` | — |
