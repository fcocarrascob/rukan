# 12 · Los dos vanos libres

El título es engañoso, y el propio memo lo dice en su tercer bloque: los dos vanos arriostrados
son los **extremos**, así que la excentricidad de rigidez es cero y los dos vanos con portón no
producen torsión. La produce **dónde se estaciona la grúa**. Y entonces aparece lo que once
eslabones habían dado por sentado: el método de análisis. La irregularidad torsional cae **entre
las dos lecturas del mismo edificio**, una a cada lado del umbral de §5.2.2, y lo que las separa
no es una hipótesis de carga sino si el modelo tiene o no tiene la otra dirección adentro.
Fuerzas en kN, longitudes en m salvo donde se indique.

## El caso

{{ figura('nch2369-galpon-grua/12', 'planta', 'Planta del galpón con los cuatro vanos de 7,50 m entre los cinco marcos: los vanos extremos con arriostramiento vertical y los dos centrales con portón, el centro de rigidez en 15,00 m por simetría, la grúa estacionada con su centro a 2,00 m del marco extremo y el centro de masa corrido a 12,11692, con la excentricidad de 2,88308 m acotada entre los dos') }}

| Dato | Valor |
|---|---|
| Elemento | el edificio entero, mirado en planta |
| Largo de la nave | {{ v('nch2369-galpon-grua/12', 'L_total', 2) }} m en {{ v('nch2369-galpon-grua/12', 'n_vanos', 0) }} vanos de {{ v('nch2369-galpon-grua/12', 's_marco', 2) }} m (del 01 · S1) |
| Luz transversal | {{ v('nch2369-galpon-grua/12', 'L_luz', 2) }} m; altura de alero {{ v('nch2369-galpon-grua/12', 'h_libre', 2) }} m (del 01 · S1) |
| Vanos arriostrados | los **extremos**; los dos centrales con portón (del 01 · S2) |
| Peso sísmico | {{ v('nch2369-galpon-grua/12', 'P_sismico', 5) }} kN, de los que la grúa aporta {{ v('nch2369-galpon-grua/12', 'pct_grua', 2) }} % (del 05) |
| Rigidez del marco | $k_Y = {{ vt('nch2369-galpon-grua/12', 'k_Y', 5) }}$ kN/m (del 07), $\times\,{{ vt('nch2369-galpon-grua/12', 'k_esc', 5) }}$ por el escalón (del 10) |
| Diafragma de techo | $k_d = {{ vt('nch2369-galpon-grua/12', 'kd_vano', 5) }}$ kN/m por vano (del 11 · D2) |
| Panel longitudinal | **no está diseñado**: es del 13. Acá entra como parámetro (S1) |
| Lo que se decide aquí | si el método estático está habilitado, y con qué modelo |

Los supuestos, en una línea cada uno. **S1**, la rigidez del panel arriostrado longitudinal no
está diseñada; como ilustración se adopta una X del mismo tubo que el 11 puso en la diagonal de
techo. **S2**, el plano de techo se idealiza como panel de corte puro con la rigidez del
11 · D2. **S3**, el centro del puente alcanza {{ v('nch2369-galpon-grua/12', 'x_g_tope', 2) }} m
del eje del marco extremo —media base de ruedas más tope y holgura—. **S4**, la masa del
edificio se distribuye uniformemente en los {{ v('nch2369-galpon-grua/12', 'L_total', 2) }} m.
**S5**, la palabra «altura» de §5.2.2 **no está definida en la norma**: se evalúan las dos
lecturas y ninguna se adopta. **S6**, para las irregularidades de masa y de piso blando la
estructura se idealiza con **dos niveles**, que es la lectura desfavorable. **S7**, los cinco
marcos tienen la misma rigidez, con el `k_esc` aplicado a todos —los de frontón son más rígidos,
así que el supuesto es conservador—. **S8**, la tracción longitudinal de grúa no es concurrente
con el sismo de diseño.

## A · El método de análisis que once eslabones dieron por sentado

### A1 · La altura del galpón depende de dónde se mida, y la cláusula no lo dice

$$h_{cumb} = {{ vt('nch2369-galpon-grua/12', 'h_cumb', 5) }}\ \text{m} \qquad {{ vt('nch2369-galpon-grua/12', 'uso_h_cumb', 5) }} \qquad {{ vt('nch2369-galpon-grua/12', 'uso_h_alero', 5) }}$$

→ §5.2.2 habilita el método estático hasta {{ v('nch2369-galpon-grua/12', 'h_tope', 2) }} m de
altura, y **la norma no dice desde y hasta dónde se mide**. Medida al alero el galpón usa
{{ v('nch2369-galpon-grua/12', 'uso_h_alero', 5) }} del tope y medida a la cumbrera lo pasa en
{{ v('nch2369-galpon-grua/12', 'uso_h_cumb', 5) }}. Ninguna de las dos lecturas se adopta acá:
se declara que el umbral pasa por el medio.

### A3 y A4 · Las otras dos irregularidades se evitan solas

$$\frac{W_{edificio}}{W_{\text{grúa}}} = {{ vt('nch2369-galpon-grua/12', 'raz_masa', 5) }} \qquad {{ vt('nch2369-galpon-grua/12', 'uso_masa', 5) }} \qquad \frac{k_{riel}}{k_Y} = {{ vt('nch2369-galpon-grua/12', 'raz_piso', 5) }}$$

→ la irregularidad de masa pide que un nivel no tenga más de
{{ v('nch2369-galpon-grua/12', 'tope_masa', 2) }} veces la masa del contiguo, y acá el techo
tiene {{ v('nch2369-galpon-grua/12', 'raz_masa', 5) }} veces la de la grúa **por el otro lado**:
la evita una frase de tres palabras. La de piso blando la evita la columna escalonada del 10, que
hace el nivel del riel más rígido que el del techo por
{{ v('nch2369-galpon-grua/12', 'raz_piso', 5) }}. **Queda una sola puerta, y es la que el modelo
decide.**

## B · El diafragma, que §5.3.3 obliga a clasificar y el 11 midió sin citar la cláusula

### B1 a B4 · El criterio tiene un número, y se invierte

$$GA_{eq} = {{ vt('nch2369-galpon-grua/12', 'GA_eq', 5) }}\ \text{kN} \qquad w_x = {{ vt('nch2369-galpon-grua/12', 'w_x', 5) }}\ \text{kN}/\text{m} \qquad R_{br} = {{ vt('nch2369-galpon-grua/12', 'R_br', 5) }}\ \text{kN}$$

$$\text{MDD} = {{ vt('nch2369-galpon-grua/12', 'MDD', 5) }}\ \text{mm} \qquad k_{br}^{\max} = {{ vt('nch2369-galpon-grua/12', 'kbr_max', 2) }}\ \text{kN}/\text{m}$$

→ un diafragma es flexible cuando su máxima deformación en el plano supera
{{ v('nch2369-galpon-grua/12', 'tope_diaf', 2) }} veces la deriva de los elementos verticales de
los extremos. Es un **factor entre dos deformaciones**, no una razón de rigideces ni una
esbeltez en planta —y la Figura 1 que acompaña la cláusula dibuja exactamente este edificio—. El
plano de techo se deforma {{ v('nch2369-galpon-grua/12', 'MDD', 5) }} mm sobre los
{{ v('nch2369-galpon-grua/12', 'L_diaf', 2) }} m entre vanos arriostrados, y de ahí sale algo que
sorprende: **una rigidez máxima de panel**, no una mínima. El arriostramiento vertical tendría
que llegar a {{ v('nch2369-galpon-grua/12', 'kbr_max', 2) }} kN/m para que este techo se volviera
flexible.

### B5 y B6 · El margen es de once veces, y en la otra dirección ya estaba contestado

$$L_d = {{ vt('nch2369-galpon-grua/12', 'Ld_pan', 2) }}\ \text{mm} \qquad k_{pan} = {{ vt('nch2369-galpon-grua/12', 'k_pan', 2) }}\ \text{kN}/\text{m} \qquad {{ vt('nch2369-galpon-grua/12', 'factor_diaf', 5) }} \qquad {{ vt('nch2369-galpon-grua/12', 'factor_diaf_Y', 5) }}$$

→ contra el panel ilustrativo el diafragma es rígido con factor
{{ v('nch2369-galpon-grua/12', 'factor_diaf', 5) }}, y ninguna sección razonable lo cambia.
**Clasificación emitida: rígido.** Transversalmente la pregunta ya estaba contestada por el 11:
el marco cargado retiene {{ v('nch2369-galpon-grua/12', 'factor_diaf_Y', 5) }} de lo que
retendría con diafragma infinitamente rígido, contra el factor
{{ v('nch2369-galpon-grua/12', 'tope_diaf', 2) }} que la cláusula admite. El número no es nuevo:
es el `f_marco_grua` del 11 leído contra la cláusula que nadie había citado.

## C · La torsión en planta, que es lo único que decide

{{ figura('nch2369-galpon-grua/12', 'razon', 'La razón entre la deriva del marco extremo y la promedio del nivel contra la rigidez relativa del panel longitudinal: la curva baja de 1,38441 en el origen a 1,11962 en el 1,99227 del panel ilustrativo, cruza el umbral de 1,20 de la cláusula 5.2.2 en 0,82985, y las dos lecturas del mismo edificio quedan una a cada lado del umbral') }}

### C1 a C3 · El centro de rigidez no se mueve, y la excentricidad la produce la grúa

$$\sum (x_i - x_{CR})^{2} = {{ vt('nch2369-galpon-grua/12', 'sum_x2', 5) }}\ \text{m}^{2} \qquad \sum (y_j - y_{CR})^{2} = {{ vt('nch2369-galpon-grua/12', 'sum_y2', 5) }}\ \text{m}^{2}$$

$$x_{CM} = {{ vt('nch2369-galpon-grua/12', 'x_CM', 5) }}\ \text{m} \qquad e = {{ vt('nch2369-galpon-grua/12', 'e_tors', 5) }}\ \text{m} \qquad {{ vt('nch2369-galpon-grua/12', 'e_rel', 5) }}$$

→ los cinco marcos aportan {{ v('nch2369-galpon-grua/12', 'sum_x2', 2) }} m² de rigidez torsional
y los cuatro paneles longitudinales {{ v('nch2369-galpon-grua/12', 'sum_y2', 2) }} m². **El
segundo término es el que un modelo plano no tiene**: en un modelo de la dirección de marcos los
paneles longitudinales no existen, y su aporte desaparece con ellos. Todo lo que sigue depende de
si ese término está o no. Y con la grúa contra su tope el centro de masa se corre
{{ v('nch2369-galpon-grua/12', 'e_tors', 5) }} m, el
{{ v('nch2369-galpon-grua/12', 'e_rel', 5) }} del largo de la nave: la posición desfavorable no
hay que buscarla, es el tope de recorrido.

### C4 y C5 · Las dos lecturas del mismo edificio, una a cada lado del umbral

$$\rho = {{ vt('nch2369-galpon-grua/12', 'rho_pan', 5) }} \qquad \frac{\delta_{\text{máx}}}{\delta_{\text{prom}}} = 1 + \frac{{'{'}}{{ vt('nch2369-galpon-grua/12', 'brazo_Y', 2) }} \cdot {{ vt('nch2369-galpon-grua/12', 'e_tors', 5) }}{{'}'}}{{'{'}}\Sigma x^{2} + \Sigma y^{2}\rho{{'}'}} = {{ vt('nch2369-galpon-grua/12', 'raz_tors_Y', 5) }}$$

$$\text{sin los paneles} \Rightarrow {{ vt('nch2369-galpon-grua/12', 'raz_tors_plano', 5) }}$$

→ **{{ v('nch2369-galpon-grua/12', 'raz_tors_Y', 5) }} contra el umbral de
{{ v('nch2369-galpon-grua/12', 'tope_tors', 2) }}**: no hay irregularidad torsional y el método
estático queda habilitado. Con modelos planos por dirección la misma razón vale
{{ v('nch2369-galpon-grua/12', 'raz_tors_plano', 5) }} y **sí la hay**. §5.3.2 admite modelos
planos «en los casos en que el comportamiento se puede estimar adecuadamente», y éste es
exactamente un caso en que no se puede.

#### Y esto es lo que el modelo hace con la grúa en su tope

<rukan-visor src="../../../modelos/galpon-grua/galpon-grua.escena.json" caso="E_Y_tope" vista="iso"></rukan-visor>

El caso `E_Y_tope` es un empuje transversal de **5 000 kN** repartido como la masa, con la grúa
en `x_g_tope`. Los cinco nudos de alero de la línea A dan la deformada del nivel, marco por
marco.

| Marco | δ del alero, bajo `E_Y_tope` |
|---|---:|
| M1, el que la grúa carga | {{ r('galpon-grua', 'dY_m1', 2, factor=1000) }} mm |
| M2 | {{ r('galpon-grua', 'dY_m2', 2, factor=1000) }} mm |
| M3, el central | {{ r('galpon-grua', 'dY_m3', 2, factor=1000) }} mm |
| M4 | {{ r('galpon-grua', 'dY_m4', 2, factor=1000) }} mm |
| M5, el opuesto | {{ r('galpon-grua', 'dY_m5', 2, factor=1000) }} mm |
| **δ₁/δ₅ del modelo** | **{{ razon('galpon-grua', 'dY_m1', 'dY_m5', 5) }}** |
| δ₁/δ₅ que implica C4 | {{ v('nch2369-galpon-grua/12', 'raz_extremos', 5) }} |

La deformada **cae monótonamente del marco cargado al opuesto**, que es la forma que C4 supone y
no calcula: el modelo la produce sin que nadie se la haya pedido, y con ella confirma que la
grúa en su tope torsiona la planta. La magnitud es mayor —el modelo separa los dos extremos
{{ razon('galpon-grua', 'dY_m1', 'dY_m5', 5) }} donde la forma cerrada implica
{{ v('nch2369-galpon-grua/12', 'raz_extremos', 5) }}— y la razón está declarada en el propio
memo: **C4 supone el diafragma infinitamente rígido**, y el modelo tiene el techo arriostrado
real, con sus {{ v('nch2369-galpon-grua/11', 'A_diag_techo', 0) }} mm² de diagonal y su
flexibilidad de cordón adentro. El memo clasificó el diafragma como rígido en B5 con factor
{{ v('nch2369-galpon-grua/12', 'factor_diaf', 5) }} —contra el criterio de deformaciones de
§5.3.3, que es otra pregunta— y acá se ve lo que esa idealización cuesta en el reparto.

Es contraste y no verificación, y hay una segunda razón para leerlo así: **cómo se reparte la
cuota de la grúa entre los marcos es una decisión de Rukan que ningún memo tomó**, y está
declarada en `## Límites`.

### C6 a C9 · La cota que el 13 hereda, el `k_esc` que empeora, y la accidental que no se exige

$$\rho_{lim} = {{ vt('nch2369-galpon-grua/12', 'rho_lim', 5) }} \qquad k_{br}^{lim} = {{ vt('nch2369-galpon-grua/12', 'kbr_lim', 5) }}\ \text{kN}/\text{m} \qquad {{ vt('nch2369-galpon-grua/12', 'uso_kbr', 5) }}$$

$$\text{sin } k_{esc} \Rightarrow {{ vt('nch2369-galpon-grua/12', 'raz_sin_esc', 5) }} \qquad {{ vt('nch2369-galpon-grua/12', 'crece_esc', 5) }} \qquad e_{acc} = {{ vt('nch2369-galpon-grua/12', 'e_acc', 5) }}\ \text{m} \qquad {{ vt('nch2369-galpon-grua/12', 'raz_tors_acc', 5) }}$$

→ tres consecuencias. La primera: como la razón depende de $\rho$, el umbral se despeja en la
rigidez del panel y sale una **cota inferior** de
{{ v('nch2369-galpon-grua/12', 'kbr_lim', 5) }} kN/m — el 13 recibe una restricción de rigidez
que ninguna de sus cláusulas de resistencia le va a imponer. La segunda: **el `k_esc` del 10 es
acá desfavorable**. Sin él la razón sería {{ v('nch2369-galpon-grua/12', 'raz_sin_esc', 5) }}, y
con él el exceso sobre 1 crece {{ v('nch2369-galpon-grua/12', 'crece_esc', 5) }} veces —
rigidizar el marco transversal, que el 07 celebró por deriva, empeora la irregularidad
torsional—. La tercera: la torsión **accidental** de NCh433 §6.2.8, que NCh2369 no exige y su
Comentario sólo sugiere, vale {{ v('nch2369-galpon-grua/12', 'veces_acc', 5) }} veces la real, y
sumada lleva la razón a {{ v('nch2369-galpon-grua/12', 'raz_tors_acc', 5) }}: **irregular
también por la vía tridimensional**. El verbo de la cláusula es «pueden», y la decisión queda
entera del lado del proyectista.

$$x_g^{crit} = {{ vt('nch2369-galpon-grua/12', 'x_g_crit', 5) }}\ \text{m} \qquad {{ vt('nch2369-galpon-grua/12', 'nave_prohibida', 5) }}$$

→ con modelos planos bastaría con que la grúa entrara en los
{{ v('nch2369-galpon-grua/12', 'x_g_crit', 2) }} m extremos de cualquiera de los dos lados —el
{{ v('nch2369-galpon-grua/12', 'nave_prohibida', 5) }} de la nave— para disparar la
irregularidad. Con el modelo tridimensional esa posición crítica ni siquiera existe dentro del
edificio, y por eso el tope de recorrido de S3 no es un supuesto crítico.

### C10 · Lo que la torsión le hace a las dos derivas que la serie ya había publicado

$$\delta_{ext} = {{ vt('nch2369-galpon-grua/12', 'd_ext', 5) }}\ \text{mm} \qquad {{ vt('nch2369-galpon-grua/12', 'uso_deriva_ext', 5) }} \qquad \delta_{riel} = {{ vt('nch2369-galpon-grua/12', 'd_riel_ext', 5) }}\ \text{mm} \qquad {{ vt('nch2369-galpon-grua/12', 'uso_riel_tors', 5) }}$$

→ el marco extremo se lleva la amplificación entera, así que **los dos números que el 07 y el 11
publicaron describen el marco central y no el que gobierna**. Ninguno de los dos criterios cambia
de signo —{{ v('nch2369-galpon-grua/12', 'uso_deriva_ext', 5) }} del límite de §6.3 y
{{ v('nch2369-galpon-grua/12', 'uso_riel_tors', 5) }} del de servicio de grúa— pero los dos
números había que corregirlos.

## D · El colector que cruza el portón

### D1 y D2 · El máximo cae fuera del vano libre, y la excentricidad longitudinal la produce el carro

$$w_{al} = {{ vt('nch2369-galpon-grua/12', 'w_al', 5) }}\ \text{kN}/\text{m} \qquad {{ vt('nch2369-galpon-grua/12', 'N_col_vano', 5) }}\ \text{kN} \qquad {{ vt('nch2369-galpon-grua/12', 'N_col_ext', 5) }}\ \text{kN}$$

$$y_{CM} = {{ vt('nch2369-galpon-grua/12', 'y_CM', 5) }}\ \text{m} \qquad e_x = {{ vt('nch2369-galpon-grua/12', 'e_x', 5) }}\ \text{m} \qquad {{ vt('nch2369-galpon-grua/12', 'menor_que_Y', 5) }}$$

→ al entrar al vano arriostrado el colector lleva
{{ v('nch2369-galpon-grua/12', 'N_col_vano', 2) }} kN y sale del extremo de la nave con
{{ v('nch2369-galpon-grua/12', 'N_col_ext', 2) }}: **los dos vanos con portón son la mitad más
floja del recorrido**, y el colector se dimensiona dentro del vano arriostrado, no cruzándolo.
Es lo contrario de lo que el nombre del eslabón sugiere. Longitudinalmente lo que descentra la
masa no es dónde está el puente sino **dónde queda el carro**, y la excentricidad resultante es
{{ v('nch2369-galpon-grua/12', 'menor_que_Y', 5) }} veces menor que la transversal.

### D3 a D6 · La amplificación longitudinal, y una palabra que la norma usa una sola vez

$$\frac{\delta_{\text{máx}}}{\delta_{\text{prom}}}\Big|_X = {{ vt('nch2369-galpon-grua/12', 'raz_tors_X', 5) }} \qquad F_{col} = {{ vt('nch2369-galpon-grua/12', 'F_col_12', 5) }}\ \text{kN} \qquad {{ vt('nch2369-galpon-grua/12', 'veces_traccion', 5) }}$$

$$\phi P_n = {{ vt('nch2369-galpon-grua/12', 'phiPn_punt', 5) }}\ \text{kN} \qquad {{ vt('nch2369-galpon-grua/12', 'uso_colector', 5) }}$$

→ en esta dirección los dos términos de la rigidez torsional intercambian su papel, la razón cae
a {{ v('nch2369-galpon-grua/12', 'raz_tors_X', 5) }} —muy por debajo del umbral— y el colector
del alero más cargado sube a {{ v('nch2369-galpon-grua/12', 'F_col_12', 5) }} kN: los
{{ v('nch2369-galpon-grua/11', 'F_col_alero', 5) }} kN que el 11 publicó son el **promedio de los
dos aleros**. La tracción longitudinal de grúa del 03 llega
{{ v('nch2369-galpon-grua/12', 'veces_traccion', 5) }} veces por debajo y no gobierna, pero deja
dicho el camino: **entre el riel y el alero no hay ningún miembro longitudinal declarado en once
eslabones**, y esa fuerza lo recorre en cada frenada. El puntal del 11 sirve con uso
{{ v('nch2369-galpon-grua/12', 'uso_colector', 5) }}. Y la palabra «colector» aparece **una sola
vez** en toda la norma, en el capítulo de diafragmas de madera, que sí remite a ASCE 7.

## E · El período con que se calcula R*, que resulta no decidir nada

{{ figura('nch2369-galpon-grua/12', 'espectro', 'El espectro de diseño horizontal contra el período, con el recorte de la cláusula 5.13 dibujado como una recta horizontal en 0,29161: dentro de la rampa de la Ec. 1b la ordenada cae de 0,42415 en el origen a un mínimo local de 0,35404, sube a un máximo local de 0,36680 en 0,18600 y vuelve a caer en la frontera de 0,28000 s, y la curva corta el recorte en 0,55049 s con los dos períodos de la serie dentro del tramo gobernado por el recorte') }}

### E2 y E2b · El espectro no es monótono, y la única regla está en el Comentario

$$S_a({{ vt('nch2369-galpon-grua/12', 'T_estac_max', 5) }}) = {{ vt('nch2369-galpon-grua/12', 'Sa_max', 5) }}\ \text{g} \qquad S_a({{ vt('nch2369-galpon-grua/12', 'T_estac_min', 5) }}) = {{ vt('nch2369-galpon-grua/12', 'Sa_min', 5) }}\ \text{g} \qquad {{ vt('nch2369-galpon-grua/12', 'sube_del_min', 5) }}$$

$$S_a(T^{*}_X) = {{ vt('nch2369-galpon-grua/12', 'Sa_TX', 5) }}\ \text{g} \qquad {{ vt('nch2369-galpon-grua/12', 'cerca_max', 5) }} \qquad S_a(0) = {{ vt('nch2369-galpon-grua/12', 'Sa_cero', 5) }}\ \text{g} \qquad {{ vt('nch2369-galpon-grua/12', 'frac_del_origen', 5) }}$$

→ la frase que dice cómo elegir el período **no está en la columna normativa**: es C5.4.1, y pide
que el período adoptado «maximice la respuesta». Dentro de la rampa el $R^{*}$ crece linealmente
y el espectro de referencia no, así que el cociente tiene **dos puntos estacionarios
interiores**: un mínimo y un máximo. El período adoptado de
{{ v('nch2369-galpon-grua/12', 'T_star_X', 2) }} s cae pasado el máximo y entrega
{{ v('nch2369-galpon-grua/12', 'cerca_max', 5) }} de él, así que **sí maximiza la respuesta en el
único sentido que tiene contenido**: es el máximo de su rama. Leída como un máximo global la
exigencia empujaría el período a cero, y ese extremo no es un resultado físico sino el valor de
$R^{*}$ en su cota de {{ v('nch2369-galpon-grua/12', 'R_min', 2) }}.

### E3 y E4 · La exigencia se cumple sola, y la ventana tiene un borde

$$S_a(0{,}50) = {{ vt('nch2369-galpon-grua/12', 'Sa_05', 5) }}\ \text{g} \qquad {{ vt('nch2369-galpon-grua/12', 'sobre_recorte', 5) }} \qquad T_{borde} = {{ vt('nch2369-galpon-grua/12', 'T_borde', 5) }}\ \text{s}$$

$${{ vt('nch2369-galpon-grua/12', 'margen_Y', 5) }} \qquad {{ vt('nch2369-galpon-grua/12', 'margen_X', 5) }}$$

→ el corte de diseño de esta estructura no es el del análisis sino el techo de §5.13, y ese techo
no depende de $T^{*}$. A medio segundo el espectro todavía está
{{ v('nch2369-galpon-grua/12', 'sobre_recorte', 5) }} sobre el coeficiente recortado, así que
**mientras el recorte gobierne el período no cambia ningún número que se diseñe**. El recorte
suelta en {{ v('nch2369-galpon-grua/12', 'T_borde', 5) }} s, a un factor
{{ v('nch2369-galpon-grua/12', 'margen_Y', 5) }} del período más largo de la serie. Es el número
que hay que volver a mirar si el peso propio real —que tres eslabones ya piden reconciliar— hace
crecer la masa.

## Veredicto

**Los dos vanos libres no producen torsión**, y el título del eslabón es engañoso a propósito:
los vanos arriostrados son los extremos, la distribución de rigidez es simétrica y el centro de
rigidez cae en el centro de la nave. Lo que produce torsión es **dónde se estaciona la grúa**,
que corre el centro de masa {{ v('nch2369-galpon-grua/12', 'e_tors', 5) }} m.

**La irregularidad torsional cae entre las dos lecturas del mismo edificio**:
{{ v('nch2369-galpon-grua/12', 'raz_tors_Y', 5) }} con el modelo tridimensional y
{{ v('nch2369-galpon-grua/12', 'raz_tors_plano', 5) }} con modelos planos, una a cada lado del
umbral de {{ v('nch2369-galpon-grua/12', 'tope_tors', 2) }}. La diferencia no es una hipótesis de
carga ni una sección: es si el modelo tiene o no tiene la otra dirección adentro. Y si se suma la
torsión accidental que NCh2369 no exige, la lectura tridimensional también se vuelve irregular,
en {{ v('nch2369-galpon-grua/12', 'raz_tors_acc', 5) }}.

De ahí salen dos cosas para el 13: una **cota inferior de rigidez** para el panel longitudinal,
{{ v('nch2369-galpon-grua/12', 'kbr_lim', 5) }} kN/m, que ninguna cláusula de resistencia le
impone; y un colector de {{ v('nch2369-galpon-grua/12', 'F_col_12', 5) }} kN, que es el del 11
con la torsión adentro. Y una advertencia hacia atrás: **el `k_esc` del 10 empeora la
irregularidad torsional**, y es su primera consecuencia con el signo desfavorable.

El período, en cambio, **no decide nada** mientras el recorte de §5.13 gobierne, y gobierna hasta
{{ v('nch2369-galpon-grua/12', 'T_borde', 5) }} s.

## Límites

- **Dos cifras de la prosa del memo no reproducen.** El mínimo local de la rampa está en
  0,0764878 s, que redondea a {{ v('nch2369-galpon-grua/12', 'T_estac_min', 5) }}; el memo
  publica 0,07650. La ordenada es la misma a cinco decimales, así que no cambia nada. Y la deriva
  del riel que este eslabón consume del 11 —0,93897 mm— es la cifra que aquel publicó; la
  aritmética del 11 sobre sus propias cifras impresas da 0,93896. Se consume la impresa, como
  manda la regla, y el hallazgo está anotado en el `## Límites` del 11.
- **Cómo se reparte la cuota de la grúa entre los marcos es una decisión de Rukan.** El caso
  `E_Y_tope` del modelo pone el 22 % del peso sísmico que corresponde a la grúa en los nudos de
  riel de los marcos que un puente en `x_g_tope` carga, y el resto proporcional a la masa de cada
  nudo. **Ningún memo de la serie tomó esa decisión**, porque ninguno corrió el caso. El reparto
  se declara acá y no se ajusta para acercarse a la forma cerrada de C4.
- **El modelo tiene diafragma flexible y la fórmula de C4 lo supone rígido.** La diferencia entre
  {{ razon('galpon-grua', 'dY_m1', 'dY_m5', 5) }} y
  {{ v('nch2369-galpon-grua/12', 'raz_extremos', 5) }} es esa idealización, y es un hallazgo, no
  un error: las dos cifras responden preguntas distintas. La clasificación de B5 —rígido con
  factor {{ v('nch2369-galpon-grua/12', 'factor_diaf', 5) }}— es contra el criterio de
  deformaciones de §5.3.3, que no es el mismo que el reparto entre marcos.
- **La rigidez del panel longitudinal no está diseñada.** Todo el bloque C cuelga de un valor
  ilustrativo, y lo único que el eslabón publica de él es la **cota** que el 13 tiene que
  respetar.
- **La palabra «altura» de §5.2.2 no está definida en la norma**, y las dos lecturas caen una a
  cada lado del tope de {{ v('nch2369-galpon-grua/12', 'h_tope', 2) }} m. Este eslabón declara el
  problema y no lo resuelve.
- **La torsión accidental es una decisión del proyectista.** El Comentario de §5.6.4 —que la
  norma rotula C5.4.6, cruzando dos dígitos frente a su propia cláusula— dice que «pueden»
  utilizarse las metodologías de NCh433 «en aquellos casos en que se estime necesario». La ruta
  modal de NCh433 usa la mitad del ancho y con ella la razón quedaría bajo el umbral.
- **Los dos niveles de S6 son una idealización.** Un galpón de un piso con una grúa colgada no
  tiene «entrepiso», y las cláusulas de masa y de piso blando no tienen a qué compararse sin ese
  artificio.
- **El colector no tiene cláusula.** NCh2369 obliga a poner un diafragma de techo y no dimensiona
  su colector: la única cláusula que lo hace es la de diafragmas de madera, y remite a ASCE 7. Es
  el tercer elemento de la serie que la norma obliga a poner y no dimensiona.
- **La torsión del modelo no está contrastada contra SAP2000.** El repositorio verificó axiales y
  momentos; corte y torsión de barra siguen la regla análoga y esperan su caso.

## Ficha

{{ ficha('nch2369-galpon-grua/12') }}

## Referencias

| Clave | Norma y edición | Cláusula | Leída en | Cita textual |
|---|---|---|---|---|
| NCh-p1 | NCh2369:2025 (3.ª ed.) | §5.2.2 (1), las dos puertas previas a las irregularidades que A1 y A2 leen | `Normas/NCh 2369 - 3°Edición 2025.05.28.pdf`, p. 27 | «solamente para estructuras de Categoría I y II, de hasta 4 niveles y altura no mayor a 12 m» |
| NCh-p2 | NCh2369:2025 (3.ª ed.) | §5.2.2, el umbral de la irregularidad torsional que C4 y C5 comparan | PDF ídem, p. 27 | «es mayor a 1,2 veces la deformación lateral promedio del nivel» |
| NCh-p3 | NCh2369:2025 (3.ª ed.) | §5.2.2, la exención del último nivel que A3 usa | PDF ídem, p. 27 | «Esta definición no aplica al último nivel» |
| NCh-p4 | NCh2369:2025 (3.ª ed.) | §5.2.2, el umbral de piso blando de A4 | PDF ídem, p. 27 | «menor al 70% de la rigidez lateral del nivel superior» |
| NCh-p5 | NCh2369:2025 (3.ª ed.) | C5.2.2, la obligación de posición desfavorable que C3 aplica | PDF ídem, p. 27 | «deben prever distribuciones de sobrecarga desfavorables en términos de maximizar la torsión en planta» |
| NCh-p6 | NCh2369:2025 (3.ª ed.) | §3.1.29, la definición que cierra el hallazgo 7 en E1 | PDF ídem, p. 14 | «período del modo normal de vibración con mayor masa de traslación equivalente en la dirección de análisis» |
| NCh-p7 | NCh2369:2025 (3.ª ed.) | §5.3.2, el modelo tridimensional y su excepción, que A5 y C5 invocan | PDF ídem, p. 30 | «se debe usar un modelo tridimensional, excepto en los casos en que el comportamiento se puede estimar adecuadamente usando modelos planos» |
| NCh-p8 | NCh2369:2025 (3.ª ed.) | §5.3.3, la obligación de clasificar el diafragma que B1 recoge | PDF ídem, p. 30 | «los diafragmas se deben clasificar como flexibles o rígidos» |
| NCh-p9 | NCh2369:2025 (3.ª ed.) | §5.3.3 y Figura 1, el criterio numérico de B2 | PDF ídem, p. 31 | «cuando la máxima deformación en el plano del diafragma debido a cargas laterales es mayor a dos veces el desplazamiento de entrepiso promedio de los elementos verticales» |
| NCh-p10 | NCh2369:2025 (3.ª ed.) | §5.3.6, la obligación de considerar la torsión que C3 aplica | PDF ídem, p. 32 | «Los efectos de la torsión en planta debido a variaciones de la distribución de cargas de operación, ubicación de sobrecargas y peso propio se deben considerar en el diseño estructural» |
| NCh-p11 | NCh2369:2025 (3.ª ed.) | §5.4, la definición de T\* que E1 confronta con §3.1.29 | PDF ídem, p. 34 | «período fundamental en la dirección horizontal de análisis sísmico, evaluado mediante un procedimiento teórico o empírico fundamentado» |
| NCh-p12 | NCh2369:2025 (3.ª ed.) | C5.4.1, la única indicación sobre el período de R\*, y está en el Comentario, que E2 y E3 verifican | PDF ídem, p. 35 | «es necesario verificar que el período de vibración adoptado para el cálculo de R \*, sea representativo y maximice la respuesta» |
| NCh-p13 | NCh2369:2025 (3.ª ed.) | §5.6.4, la remisión a §5.3.3 desde la cláusula de torsión, que B1 usa | PDF ídem, p. 41 | «Para efectos de esta norma, los diafragmas se deben clasificar como flexibles o rígidos, de acuerdo con 5.3.3» |
| NCh-p14 | NCh2369:2025 (3.ª ed.) | el Comentario de §5.6.4 —rotulado **C5.4.6** en el propio documento—, la torsión accidental opcional de C8 | PDF ídem, p. 41 | «En aquellos casos en que se estime necesario la incorporación de torsión accidental, pueden utilizarse las metodologías establecidas en NCh433» |
| NCh-p15 | NCh2369:2025 (3.ª ed.) | §12.4.1 y C12.4.1, la única remisión a colectores de toda la norma, que D6 encuentra | PDF ídem, p. 153 | «se debe utilizar ASCE/SEI 7-16, secciones 12.3 y 12.10 en lo referente al diseño y verificación de diafragmas, colectores, cuerdas y sus conexiones» |
| N433-p1 | NCh433:2026 (5.ª ed.) | §6.2.8, la excentricidad accidental del método estático que C8 cuantifica | `Normas/NCh 433 - 5°Edición 2026.03.26.pdf`, p. 44 | «La torsión accidental se debe analizar aplicando momentos de torsión en cada nivel, calculados como el producto de las fuerzas estáticas, que actúan sobre ese nivel, por una excentricidad dada por» |
| N433-p2 | NCh433:2026 (5.ª ed.) | §6.3.3, la ruta modal con la mitad de la excentricidad, que C8 cita | PDF ídem, p. 45 | «desplazando transversalmente la ubicación de los centros de masas del modelo en» |
| AISC360-w | ANSI/AISC 360-22 | §E3, el pandeo por flexión con que B5 y D5 dimensionan | `referencias/AISC360-22/capE-compresion.md` | |
| AIST-w | AIST TR-13:2021 | §5.3, el límite de servicio del riel que C10 usa; §3.7.2, la tracción longitudinal de D4 | `referencias/AIST-TR13-2021/cap03-cargas-de-grua.md` | |
