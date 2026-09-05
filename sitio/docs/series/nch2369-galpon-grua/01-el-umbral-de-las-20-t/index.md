# 01 · El umbral de las 20 t: una sola letra de §12.2.1

Una sola letra de §12.2.1 saca al galpón de la cláusula 12.2, y con ella se van el R = 4, el
arriostramiento solo-tracción y el amplificador rebajado de 0,5 R₁. Este eslabón clasifica el
galpón, evalúa las ocho condiciones de admisión del galpón liviano y fija la fila de la
Tabla 7 con su factor de modificación de la respuesta y su amortiguamiento. Es la raíz de la
serie: no hereda de nadie, y once eslabones heredan de él. Longitudes en m, fuerzas en kN.

## El caso

{{ figura('nch2369-galpon-grua/01', 'planta', 'Planta del galpón de 30,00 por 25,00 m con cinco marcos separados 7,50 m, los dos vanos arriostrados de los ejes extremos y los dos vanos libres centrales ocupados por portones, y el recorrido del puente grúa sobre las vigas carrileras') }}

{{ figura('nch2369-galpon-grua/01', 'seccion', 'Sección transversal a dos aguas de 25,00 m de luz, con la altura libre interior de columna de 10,50 m, el nivel superior del riel a 7,50 m y la cumbrera 2,50 m sobre el alero') }}

| Dato | Valor |
|---|---|
| Tipo | Galpón industrial de acero, una nave, un piso, cubierta a dos aguas |
| Luz transversal entre ejes de columnas | {{ v('nch2369-galpon-grua/01', 'L_luz', 2) }} m (S1) |
| Separación de marcos | {{ v('nch2369-galpon-grua/01', 's_marco', 2) }} m, {{ v('nch2369-galpon-grua/01', 'n_vanos', 0) }} vanos (S1) |
| Largo total | {{ v('nch2369-galpon-grua/01', 'L_total', 2) }} m |
| Altura libre interior de columnas laterales | {{ v('nch2369-galpon-grua/01', 'h_libre', 2) }} m (S1) |
| Pendiente de cubierta | {{ v('nch2369-galpon-grua/01', 'pend', 2) }} %, cumbrera {{ v('nch2369-galpon-grua/01', 'h_cumb', 2) }} m sobre el alero (S1) |
| Sistema transversal | Marco de momento a dos aguas, alma variable (S2) |
| Sistema longitudinal | Marcos arriostrados concéntricos en **dos** de los cuatro vanos (S2) |
| Los otros dos vanos | Libres: portones de acceso de camiones (S2) |
| Arriostramiento de techo | Continuo, exigido por §12.1.2 (S2) |
| Puente grúa | Birriel, capacidad nominal {{ v('nch2369-galpon-grua/01', 'Qn_grua', 2) }} kN, **sin cabina** de operación (S3) |
| Luz del puente grúa | {{ v('nch2369-galpon-grua/01', 'Lg_grua', 2) }} m (S3) |
| Nivel superior del riel | {{ v('nch2369-galpon-grua/01', 'h_riel', 2) }} m (S3) |
| Peso propio de la estructura soportante del techo | {{ v('nch2369-galpon-grua/01', 'g_techo', 2) }} kg/m² (S4) |
| Peso de equipos soportados, por marco | {{ v('nch2369-galpon-grua/01', 'P_eq', 2) }} kN (S5) |
| Altillos vinculados a columnas | Ninguno (S5) |
| Zona sísmica y suelo | Zona {{ v('nch2369-galpon-grua/01', 'zona', 0) }}, suelo C (S6) |
| Categoría de ocupación | II (S7) |
| Anclajes | Dúctiles, con el detalle de §8.5.2 (S8) |
| Lo que se decide aquí | si aplica §12.2, la fila de la Tabla 7, el R, el ξ y el amplificador de capacidad |

Los supuestos, en una línea cada uno. **S1**, la geometría es dato de proyecto: ninguna
cláusula la produce. **S2**, la configuración sismorresistente es decisión de proyecto: marco
de momento transversal porque la nave no admite diagonales que crucen el área de trabajo,
arriostrado longitudinal; que solo dos de los cuatro vanos estén arriostrados lo impone la
posición de los portones, y es una irregularidad que evalúa el 12. **S3**, los datos del
puente grúa son declarados; de todos, el único que este eslabón usa es la capacidad nominal,
que es además el único que §12.2.1 e) mide. **S4**, los
{{ v('nch2369-galpon-grua/01', 'g_techo', 2) }} kg/m² del techo son una estimación de
predimensionamiento; §12.2.1 d) acota qué entra en ese peso y deja fuera la cubierta. **S5**,
equipos por marco y ausencia de altillos son datos de proceso. **S6**, zona y suelo entran
declarados para que el 04 los herede. **S7**, la Categoría II es la del galpón por sí mismo;
si alojara un proceso más crítico, la letra a) fallaría también. **S8**, los anclajes se
detallan dúctiles según §8.5.2, y de eso depende que la fila 5.5 esté disponible; lo verifica
el 13.

## A · El sitio, la categoría y qué norma manda

### A1 · La categoría la fija el uso, y el coeficiente de importancia sale de ella

Las estructuras se clasifican en Categorías de ocupación y operación según la naturaleza de
su uso, y a cada una le corresponde un coeficiente de importancia. Categoría II, la del
galpón de bodegaje y mantención por sí mismo.

$$I = {{ vt('nch2369-galpon-grua/01', 'I', 2) }}$$

### A2 · La Categoría también es la primera letra de §12.2.1

La letra a) de las condiciones de admisión del galpón liviano exige Categoría I o II. Se
evalúa aquí porque la decide la misma cláusula que fija I. **Cumple.** Con Categoría III o IV
fallaría, y con IV §8.3.5 cerraría además toda salida por 0,7 R₁.

## B · Las ocho condiciones de §12.2.1, una a una

Las condiciones son acumulativas: la cláusula dice «galpones de acero que cumplan con las
condiciones siguientes», así que basta que una falle para que §12.2 no aplique. Cada paso
mide el margen como el cociente entre lo que el galpón tiene y lo que la letra permite,
donde un valor menor que 1 es cumplimiento.

### B1 · La letra b) no acota nada aquí: una nave es una nave

Un galpón puede consistir en una o varias naves paralelas. Aquí hay una. **Cumple.** La
letra b) no es un límite sino una definición del objeto, y decide de qué columna sale el
límite de luz de la letra c).

### B2 · La altura libre usa menos de la mitad de su techo

La altura libre interior de las columnas laterales debe ser menor o igual a
{{ v('nch2369-galpon-grua/01', 'h_lim', 0) }} m.

$$u_{h} = \frac{h_{\text{libre}}}{ {{ vt('nch2369-galpon-grua/01', 'h_lim', 2) }} } = \frac{ {{ vt('nch2369-galpon-grua/01', 'h_libre', 2) }} }{ {{ vt('nch2369-galpon-grua/01', 'h_lim', 2) }} } = {{ vt('nch2369-galpon-grua/01', 'u_h', 5) }}$$

→ **Cumple** con 54 % de holgura.

### B3 · Y la luz transversal, un tercio del suyo

La luz entre ejes de columnas sismorresistentes adyacentes debe ser menor o igual a
{{ v('nch2369-galpon-grua/01', 'L_lim', 0) }} m para naves individuales, o
{{ v('nch2369-galpon-grua/01', 'L_lim_par', 0) }} m para naves paralelas. Manda la primera
por B1.

$$u_{L} = \frac{L}{ {{ vt('nch2369-galpon-grua/01', 'L_lim', 2) }} } = \frac{ {{ vt('nch2369-galpon-grua/01', 'L_luz', 2) }} }{ {{ vt('nch2369-galpon-grua/01', 'L_lim', 2) }} } = {{ vt('nch2369-galpon-grua/01', 'u_L', 5) }}$$

→ **Cumple.** Es la condición con más holgura de las ocho.

### B4 · El peso de techo es la más ajustada de las que se cumplen

El peso propio de la estructura soportante del techo, que **solo** incluye vigas, costaneras,
colgadores, puntales, arriostramientos y conexiones, no debe ser mayor que
{{ v('nch2369-galpon-grua/01', 'g_lim', 0) }} kg/m².

$$u_{d} = \frac{g_{\text{techo}}}{ {{ vt('nch2369-galpon-grua/01', 'g_lim', 2) }} } = \frac{ {{ vt('nch2369-galpon-grua/01', 'g_techo', 2) }} }{ {{ vt('nch2369-galpon-grua/01', 'g_lim', 2) }} } = {{ vt('nch2369-galpon-grua/01', 'u_d', 5) }}$$

→ **Cumple**, y es la más apretada de las siete que pasan. La cubierta no entra en el
cómputo: la cláusula enumera qué incluye y no la nombra.

### B5 · La letra e) es la que falla, y falla por un factor exacto de dos

Los puentes grúa deben tener una capacidad nominal menor o igual a
{{ v('nch2369-galpon-grua/01', 'Qn_lim', 0) }} kN en el caso de grúas sin cabina de
operación, o {{ v('nch2369-galpon-grua/01', 'Qn_lim_cab', 0) }} kN para grúas con cabina.

$$u_{e} = \frac{Q_{n}}{Q_{n,\lim}} = \frac{ {{ vt('nch2369-galpon-grua/01', 'Qn_grua', 2) }} }{ {{ vt('nch2369-galpon-grua/01', 'Qn_lim', 2) }} } = {{ vt('nch2369-galpon-grua/01', 'u_e', 5) }}$$

→ **No cumple.** Y el margen no es estrecho: la grúa tiene **el doble** del máximo. Con
cabina de operación el límite sería {{ v('nch2369-galpon-grua/01', 'Qn_lim_cab', 0) }} kN y
el cociente {{ v('nch2369-galpon-grua/01', 'u_e_cab', 5) }}.

### B6 · Sin estanterías vinculadas

No debe haber estanterías de almacenamiento vinculadas sísmicamente a la estructura. No las
hay. **Cumple.** Es una condición binaria, sin margen que medir.

### B7 · Los equipos por marco usan un cuarto de su límite

Los equipos soportados por la estructura deben tener un peso total por marco menor o igual a
{{ v('nch2369-galpon-grua/01', 'P_eq_lim', 0) }} kN.

$$u_{g} = \frac{P_{\text{eq}}}{ {{ vt('nch2369-galpon-grua/01', 'P_eq_lim', 2) }} } = \frac{ {{ vt('nch2369-galpon-grua/01', 'P_eq', 2) }} }{ {{ vt('nch2369-galpon-grua/01', 'P_eq_lim', 2) }} } = {{ vt('nch2369-galpon-grua/01', 'u_g', 5) }}$$

→ **Cumple.** El puente grúa no entra aquí: la letra e) lo trata aparte, y por eso el galpón
no puede compensar una con la otra.

### B8 · Y no hay altillos que transfieran nada

En caso de tener altillos vinculados a columnas, estos deben transferir una carga sísmica
horizontal menor o igual a {{ v('nch2369-galpon-grua/01', 'H_alt_lim', 0) }} kN por columna.
No hay altillos: {{ v('nch2369-galpon-grua/01', 'u_h_alt', 5) }}.

→ **Cumple** por vacuidad.

## C · Lo que se pierde, y no se pierde solo

### C1 · Una sola letra decide por las ocho

De las ocho condiciones, {{ v('nch2369-galpon-grua/01', 'n_cumplen', 0) }} se cumplen y
{{ v('nch2369-galpon-grua/01', 'n_fallan', 0) }} no.

→ **§12.2 no aplica a este galpón.** Y la letra que falla no es marginal: es la única cuyo
cociente supera 1, y lo supera por {{ v('nch2369-galpon-grua/01', 'u_e', 5) }}.

### C2 · El arriostramiento solo-tracción se pierde en otra cláusula

No se permiten sistemas de arriostramiento con elementos que solo resisten tracción,
**excepto** en los galpones livianos que se rigen por 12.2. La excepción no vive en §12.2
sino en §8.6.1, la cláusula que la nombra, y al dejar de regirse por 12.2 el galpón deja de
estar exceptuado.

→ Las diagonales longitudinales deben resistir **compresión**, y con ello aparecen la
esbeltez y la razón ancho/espesor de §8.6.3 y §8.6.4. Lo dimensiona el 13.

### C3 · Y el amplificador de capacidad vuelve a 0,7 R₁

El diseño de galpones livianos cumple la cláusula 8 reemplazando el factor de amplificación
0,7 R₁ por 0,5 R₁. Ese reemplazo es privativo de §12.2.2.

$$k_{\text{amp}} = {{ vt('nch2369-galpon-grua/01', 'k_amp', 2) }}$$

→ Vuelve el factor general. Cuánto cuesta se mide en D3 y D4.

## D · La fila que queda, y qué cuesta

### D1 · La fila 5.5 es la única del bloque industrial que admite puente grúa

La Tabla 7 tiene tres filas de edificios industriales de un piso. La 5.7 es la de galpones
livianos y se cayó en C1. La 5.6 dice **sin** puente grúa en su propio texto, así que no
describe a este galpón. Queda la 5.5, que pide arriostramiento continuo de techo y anclajes
dúctiles.

$$R = {{ v('nch2369-galpon-grua/01', 'R_T7', 0) }} \qquad \xi = {{ vt('nch2369-galpon-grua/01', 'xi', 2) }}$$

→ Fila **5.5**, con ξ = {{ v('nch2369-galpon-grua/01', 'xi', 2) }} para uniones soldadas.
El R **sube** respecto del galpón liviano, que tenía
{{ v('nch2369-galpon-grua/01', 'R_liv', 0) }}.

### D2 · Y el requisito que la fila 5.5 cobra ya era obligatorio

Los edificios con marcos transversales deben tener un sistema de arriostramiento continuo en
el techo. La excepción de §12.1.2 alcanza a los edificios **sin** puente grúa cuyas cargas
permanentes solo provienen del peso propio, y este galpón tiene puente grúa.

→ El arriostramiento de techo **no es opcional**, así que la mitad del precio de la fila 5.5
ya estaba pagada. C12.1.2 agrega la razón funcional: distribuir las cargas laterales
concentradas de las grúas entre varios marcos, que es justo lo que los dos vanos libres
necesitan. Lo diseña el 11.

### D3 · El amplificador sube 75 %

El galpón liviano habría amplificado por 0,5 R₁ con R = {{ v('nch2369-galpon-grua/01', 'R_liv', 0) }};
el galpón de la fila 5.5 amplifica por 0,7 R₁ con R = {{ v('nch2369-galpon-grua/01', 'R_T7', 0) }}.
Se comparan sin degradación de la Ec. (1b) ni recorte de §5.14, es decir con R₁ = R.

$$\frac{0{,}7 \cdot 5}{0{,}5 \cdot 4} = \frac{ {{ vt('nch2369-galpon-grua/01', 'amp_55', 5) }} }{ {{ vt('nch2369-galpon-grua/01', 'amp_liv', 5) }} } = {{ vt('nch2369-galpon-grua/01', 'raz_amp', 5) }}$$

→ El multiplicador del diseño por capacidad crece **75 %**.

### D4 · Pero la demanda amplificada sube 40 %, no 75 %

El elemento que no es fusible ve la carga sísmica ya reducida por R* y después amplificada.
Con R₁ = R* = R ese par de operaciones deja una fracción de la demanda elástica que no
depende del R: vale 0,5 para el liviano y 0,7 para la fila 5.5. El R mayor ya había bajado
la demanda antes de que el amplificador la subiera.

$$\frac{\alpha_{\text{gr}}}{\alpha_{\text{liv}}} = \frac{0{,}70000}{0{,}50000} = {{ vt('nch2369-galpon-grua/01', 'raz_no_fusible', 5) }}$$

→ **40 %** más carga en columnas, conexiones, puntales y anclajes. Y el saldo cierra con D3:
1,75 · 0,80 = 1,40.

### D5 · Y el fusible ve 20 % menos

El fusible, diagonal o perno de anclaje, ve la demanda reducida y **no** el amplificador. Ahí
el R que sube de 4 a 5 actúa sin nada que lo compense.

$$\frac{1/5}{1/4} = {{ vt('nch2369-galpon-grua/01', 'raz_fusible', 5) }}$$

→ **20 % menos.** El saldo de perder §12.2 tiene los dos signos: alivia al fusible y encarece
todo lo demás.

### D6 · Si además faltaran los anclajes dúctiles, el que paga es el fusible

Sin el detalle de §8.5.2 la fila 5.5 no está disponible y el sistema cae a las filas
genéricas 5.2 o 5.4, ambas con R = {{ v('nch2369-galpon-grua/01', 'R_gen', 0) }}. Para el
elemento no fusible eso es indiferente, 0,7 R₁/R vale 0,70 con cualquier R sin degradar;
para el fusible no.

$$\frac{1/3}{1/5} = {{ vt('nch2369-galpon-grua/01', 'raz_sin_ductil', 5) }}$$

→ El fusible vería **67 %** más demanda por un detalle de 250 mm de vástago. Es la decisión
más cara del proyecto y se toma en la placa base.

## Veredicto

Gobierna la letra e) de §12.2.1: con {{ v('nch2369-galpon-grua/01', 'Qn_grua', 2) }} kN de
capacidad nominal contra un tope de {{ v('nch2369-galpon-grua/01', 'Qn_lim', 2) }} kN, el
galpón no se rige por §12.2 y pierde en el mismo acto el R = 4 de la fila 5.7, la excepción
de arriostramiento solo-tracción de §8.6.1 y el amplificador rebajado de §12.2.2. Queda en la
fila 5.5 con R = {{ v('nch2369-galpon-grua/01', 'R_T7', 0) }} y
ξ = {{ v('nch2369-galpon-grua/01', 'xi', 2) }}, que le es alcanzable porque §12.1.2 ya le
obligaba el arriostramiento continuo de techo. El saldo no es de un solo signo: el fusible ve
20 % menos demanda y todo lo que no es fusible, 40 % más.

Para volver a §12.2 habría que bajar la grúa a {{ v('nch2369-galpon-grua/01', 'Qn_lim', 2) }} kN,
que es la mitad de la capacidad que el proceso pide. No es una decisión de estructura.

## Límites

- **No hay modelo.** No se calculan períodos, cortes ni fuerzas de barra. Las comparaciones
  de D3 a D6 usan R₁ = R* = R, sin la degradación de la Ec. (1b) ni el recorte de §5.14. Son
  cotas de referencia, no la relación que el proyecto verá. Lo resuelve el 04, y hasta que lo
  haga ningún número de ese bloque debe usarse para dimensionar.
- **La irregularidad de los dos vanos libres no se evalúa aquí.** Lo evalúa el 12.
- **Del puente grúa solo se usa la capacidad nominal.** Pesos, ruedas, velocidades y clase de
  servicio los declara el 03.
- **El peso de techo no se verifica contra un despiece.** Si el dimensionamiento posterior lo
  llevara sobre {{ v('nch2369-galpon-grua/01', 'g_lim', 0) }} kg/m², la letra d) fallaría
  también, cosa que no cambiaría este veredicto.
- **No se verifica que los anclajes cumplan §8.5.2.** Lo verifica el 13.
- **La clasificación de sitio no se recorre.** Zona 2 y suelo C entran declarados.

## Ficha

{{ ficha('nch2369-galpon-grua/01') }}

## Referencias

| Clave | Norma y edición | Cláusula | Leída en | Cita textual |
|---|---|---|---|---|
| NCh-p1 | NCh2369:2025 (3.ª ed.) | §12.1.2, el arriostramiento continuo de techo y el alcance de su excepción | `Normas/NCh 2369 - 3°Edición 2025.05.28.pdf`, p. 150 | «Los edificios con marcos transversales deben tener un sistema de arriostramiento continuo en el techo» |
| NCh-p2 | NCh2369:2025 (3.ª ed.) | §12.1.2, a quién alcanza la excepción | PDF ídem, p. 150 | «Se exceptúan los edificios sin puente-grúa en que las cargas permanentes sólo provienen del peso propio» |
| NCh-p3 | NCh2369:2025 (3.ª ed.) | C12.1.2, la razón funcional del arriostramiento de techo | PDF ídem, p. 150 | «distribuir cargas laterales concentradas, como las de grúas, entre varios marcos» |
| NCh-p4 | NCh2369:2025 (3.ª ed.) | §12.2, la fila de la Tabla 7 que el galpón liviano usa | PDF ídem, p. 151 | «La demanda sísmica para galpones livianos se debe evaluar utilizando los parámetros indicados en» |
| NCh-p5 | NCh2369:2025 (3.ª ed.) | §12.2.1, el carácter acumulativo de las ocho condiciones | PDF ídem, p. 151 | «Estas disposiciones se aplican a galpones de acero que cumplan con las condiciones siguientes» |
| NCh-p6 | NCh2369:2025 (3.ª ed.) | §12.2.1 c), los dos límites de altura y de luz | PDF ídem, p. 151 | «La altura libre interior de las columnas laterales debe ser menor o igual a 23 m» |
| NCh-p7 | NCh2369:2025 (3.ª ed.) | §12.2.1 d), y qué incluye ese peso | PDF ídem, p. 151 | «no debe ser mayor que 70 kg/m» |
| NCh-p8 | NCh2369:2025 (3.ª ed.) | §12.2.1 e), **la letra que falla** | PDF ídem, p. 151 | «Los puentes grúas deben tener una capacidad nominal menor o igual a 100 kN, en el caso de grúas sin cabina de operación, o 50 kN para grúas con cabina de operación» |
| NCh-p9 | NCh2369:2025 (3.ª ed.) | §12.2.1 g) y h), equipos por marco y altillos | PDF ídem, p. 152 | «deben tener un peso total por marco menor o igual a 50 kN» |
| NCh-p10 | NCh2369:2025 (3.ª ed.) | §12.2.2, el amplificador rebajado que se pierde | PDF ídem, p. 152 | «reemplazando el factor de amplificación de la carga sísmica horizontal (0,7R1) por 0,5R1» |
| NCh-p11 | NCh2369:2025 (3.ª ed.) | §8.6.1, dónde vive la excepción del solo-tracción | PDF ídem, p. 94 | «No se permiten sistemas de arriostramiento con elementos que solo resisten tracción, excepto en los casos de galpones livianos de acero que se rigen por las disposiciones de 12.2» |
| NCh-p12 | NCh2369:2025 (3.ª ed.) | §4.3.2, el coeficiente de importancia de la Categoría II | PDF ídem, p. 20 | «Categoría de ocupación II: I = 1,00» |
| NCh-p13 | NCh2369:2025 (3.ª ed.) | Tabla 7 filas 5.5, 5.6 y 5.7, **mirada en PNG**, no extraída | PDF ídem, p. 68 | «Edificios industriales de un piso, con o sin puente grúa, con arriostramiento continuo de techo, y con anclajes dúctiles» |
| NCh-p14 | NCh2369:2025 (3.ª ed.) | Tabla 7 fila 5.6, el «sin puente grúa» que la excluye, **mirada en PNG** | PDF ídem, p. 68 | «Edificios industriales de un piso, sin puente grúa, sin arriostramiento continuo de techo, y con anclajes dúctiles» |
| NCh-p15 | NCh2369:2025 (3.ª ed.) | Tabla 7 filas 5.2 y 5.4, las genéricas con R = 3, **mirada en PNG** | PDF ídem, p. 67 | «Edificios y estructuras de marcos arriostrados sin anclajes dúctiles» |
