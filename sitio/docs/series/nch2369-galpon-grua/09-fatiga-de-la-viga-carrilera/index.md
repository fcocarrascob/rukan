# 09 · La fatiga de la viga carrilera

El ala que la fatiga castiga es la única de la sección que **no tiene vida infinita**, y el
tamaño del filete alma-ala lo decide una vida útil que nadie fijó. NCh2369 no tiene fatiga y
AIST tampoco da un número: da una dirección —la última edición de AISC— y una tabla que cruza
clase de edificio con ciclos. Tensiones en MPa, fuerzas en kN.

## El caso

{{ figura('nch2369-galpon-grua/09', 'categorias', 'Sección de la viga carrilera con los cuatro puntos de control de fatiga marcados y su categoría: la soldadura alma-ala superior en categoría B con rango 77,04436, la punta del ala superior en categoría A con 134,95682, el pie del atiesador transversal cortado a 346,35032 de la fibra superior en categoría C con 98,95929, y el ala inferior en categoría B con 118,38827, que es la única sobre su umbral de vida indefinida') }}

| Dato | Valor |
|---|---|
| Elemento | la viga carrilera del 08, con su soldadura alma-ala y sus detalles |
| Sección | ala superior {{ v('nch2369-galpon-grua/09', 'bfs_carril', 0) }} × {{ v('nch2369-galpon-grua/09', 'tfs_carril', 0) }}, alma {{ v('nch2369-galpon-grua/09', 'hw_carril', 0) }} × {{ v('nch2369-galpon-grua/09', 'tw_carril', 0) }}, ala inferior {{ v('nch2369-galpon-grua/09', 'bfi_carril', 0) }} × {{ v('nch2369-galpon-grua/09', 'tfi_carril', 0) }} (del 08) |
| Módulos elásticos | $S_{xc} = {{ vt('nch2369-galpon-grua/09', 'Sxc_carril', 0) }}$, $S_{xt} = {{ vt('nch2369-galpon-grua/09', 'Sxt_carril', 0) }}$ mm³ (del 08) |
| Clase de edificio de AIST | **C**, con {{ v('nch2369-galpon-grua/09', 'vida_grua', 0) }} años de vida declarada (del 03) |
| Conteo de fatiga | {{ v('nch2369-galpon-grua/09', 'Nfat_carril', 0) }} ciclos: **dos por grúa**, uno por rueda |
| Acero y electrodo | $F_y = {{ vt('nch2369-galpon-grua/09', 'Fy', 0) }}$ MPa, $F_{EXX} = {{ vt('nch2369-galpon-grua/09', 'Fexx', 0) }}$ MPa |
| Lo que se decide aquí | el filete alma-ala, y qué detalles la cláusula prohíbe y por qué |

Los supuestos, en una línea cada uno. **S1**, la fatiga se resuelve por el Apéndice 3 de AISC
360, que es adonde AIST remite; NCh2369 no tiene cláusula de fatiga. **S2**, la clase de
edificio se adopta **C**, igual que en el 08, y §1.4 dice que la especifica el propietario.
**S3**, el conteo es **por rueda**: cada rueda que pasa produce un ciclo en la soldadura, y son
dos por grúa. **S4**, las tres componentes que llegan a la soldadura alma-ala se suman en su
máximo simultáneo, aunque el flujo de corte máximo y el contacto máximo no ocurran en la misma
posición del tren. **S5**, el par torsor se reparte por igual entre las dos soldaduras del alma.

## A · La fatiga que NCh2369 no tiene, y con cuántos ciclos corre

### A1 · AIST no da un número: da una dirección y una tabla

$$\frac{100\,000}{50 \cdot 365} = {{ vt('nch2369-galpon-grua/09', 'apl_diarias', 5) }} \qquad \frac{3 \cdot 4 \cdot 250}{365} = {{ vt('nch2369-galpon-grua/09', 'regimen_dia', 5) }} \qquad {{ vt('nch2369-galpon-grua/09', 'veces_base', 5) }}$$

→ el régimen que el 03 declaró es {{ v('nch2369-galpon-grua/09', 'veces_base', 5) }} veces la
base con que la Tabla 1.1 describe la clase C. Con la vida útil de
{{ v('nch2369-galpon-grua/09', 'vida_aist', 0) }} años que la misma cláusula recomienda, este
edificio sería clase B.

### A2 y A3 · Los ciclos, y por qué son dos por grúa

$$\frac{N}{100\,000} = {{ vt('nch2369-galpon-grua/09', 'frac_techoC', 5) }} \qquad \frac{N}{20\,000} = {{ vt('nch2369-galpon-grua/09', 'veces_umbral', 5) }} \qquad n_{SR} = 2N = {{ vt('nch2369-galpon-grua/09', 'Nfat_carril', 0) }}$$

→ el umbral del Apéndice 3 son 20 000 ciclos y este régimen lo pasa
{{ v('nch2369-galpon-grua/09', 'veces_umbral', 5) }} veces: **hay que verificar fatiga**. Y
§5.8.1 pide contar **cada rueda**, así que el conteo de diseño es
{{ v('nch2369-galpon-grua/09', 'Nfat_carril', 0) }}. Coincide en número con el
{{ v('nch2369-galpon-grua/09', 'N_50', 0) }} que el 08 calculó para la clase B, y **no son lo
mismo**: uno viene de doblar la vida útil y el otro de doblar el conteo por rueda.

### A4 · La carga de fatiga está tabulada, y no lleva impacto

$$\kappa = {{ vt('nch2369-galpon-grua/09', 'kappa', 5) }} \qquad C_{ds} = {{ vt('nch2369-galpon-grua/09', 'C_ds', 5) }}\ \text{kN} \qquad C_{vs} = {{ vt('nch2369-galpon-grua/09', 'C_vs', 5) }}\ \text{kN} \qquad P_{fat} = {{ vt('nch2369-galpon-grua/09', 'P_fat', 5) }}\ \text{kN}$$

$$H_{fat} = {{ vt('nch2369-galpon-grua/09', 'H_fat', 5) }}\ \text{kN} \qquad {{ vt('nch2369-galpon-grua/09', 'menos_mayorada', 5) }} \qquad {{ vt('nch2369-galpon-grua/09', 'menos_impacto', 5) }}$$

→ la carga de fatiga es la rueda **sin impacto**, y se reconstruye desde sus dos partes
tabuladas —muerta e izada— cerrando contra la reacción del 03 dentro de
{{ v('nch2369-galpon-grua/09', 'cierre_03', 5) }} kN. Es
{{ v('nch2369-galpon-grua/09', 'menos_mayorada', 5) }} veces menor que la rueda mayorada del 08
y exactamente {{ v('nch2369-galpon-grua/09', 'menos_impacto', 5) }} veces menor que la de
servicio con impacto: **ese factor es el impacto**.

## B · El rango de tensiones, que las dos alas no reparten por igual

### B1 y B2 · La fibra que la fatiga castiga es la del módulo menor

Con vano simple el mínimo es cero, así que el rango **es el momento entero**.

$$M_{fat} = P_{fat} \cdot {{ vt('nch2369-galpon-grua/09', 'coef_M', 5) }} = {{ vt('nch2369-galpon-grua/09', 'M_fat', 5) }}\ \text{kN}\cdot\text{m}$$

$$\sigma_{SR,i} = {{ vt('nch2369-galpon-grua/09', 'sr_inf_carril', 5) }}\ \text{MPa} \qquad \sigma_{SR,s} = {{ vt('nch2369-galpon-grua/09', 'sr_sup_carril', 5) }}\ \text{MPa} \qquad \frac{S_{xc}}{S_{xt}} = {{ vt('nch2369-galpon-grua/09', 'razon_modulos', 5) }}$$

→ el momento de fatiga cierra contra el de servicio del 08 dentro de
{{ v('nch2369-galpon-grua/09', 'cierre_08', 5) }} kN·m. Y **el ala superior grande que el 08
adoptó por la flexión débil manda {{ v('nch2369-galpon-grua/09', 'razon_modulos', 5) }} veces
más rango a la fibra de abajo**: la fatiga castiga justamente la que se hizo pequeña para poder
hacer grande la otra.

### B3 · La torsión en carga de fatiga, donde la tolerancia pasa a poner casi la mitad

$$T_{fat} = {{ vt('nch2369-galpon-grua/09', 'T_empuje_fat', 5) }} + {{ vt('nch2369-galpon-grua/09', 'T_exc_fat', 5) }} = {{ vt('nch2369-galpon-grua/09', 'T_fat', 5) }}\ \text{kN}\cdot\text{mm} \qquad {{ vt('nch2369-galpon-grua/09', 'frac_exc_fat', 5) }} \qquad {{ vt('nch2369-galpon-grua/09', 'sube_frac', 5) }}$$

$$F_{par} = {{ vt('nch2369-galpon-grua/09', 'F_par_fat', 5) }}\ \text{kN} \qquad H_{ala} = {{ vt('nch2369-galpon-grua/09', 'H_ala_fat', 5) }}\ \text{kN} \qquad {{ vt('nch2369-galpon-grua/09', 'amplif_fat', 5) }} \qquad \sigma_y = {{ vt('nch2369-galpon-grua/09', 'sigma_y_fat', 5) }}\ \text{MPa}$$

→ en carga de fatiga la **excentricidad del riel pone
{{ v('nch2369-galpon-grua/09', 'frac_exc_fat', 5, 100) }} % del par**, contra el 35 % que ponía
en carga mayorada: la tolerancia de montaje pesa más cuando el empuje lateral baja, porque el
empuje se reduce a la mitad y la carga vertical no. En la punta del ala superior el rango total
sube a {{ v('nch2369-galpon-grua/09', 'sr_punta', 5) }} MPa.

### B4 · El tope de tensión de pico, que es lo único que la carga muerta toca

$$M_{pp} = {{ vt('nch2369-galpon-grua/09', 'M_pp', 5) }}\ \text{kN}\cdot\text{m} \qquad \sigma_{\max} = {{ vt('nch2369-galpon-grua/09', 'sigma_max', 5) }}\ \text{MPa} \qquad {{ vt('nch2369-galpon-grua/09', 'c_pico', 2) }}\,F_y = {{ vt('nch2369-galpon-grua/09', 'tope_pico', 5) }}\ \text{MPa} \qquad {{ vt('nch2369-galpon-grua/09', 'uso_pico', 5) }}$$

→ el peso propio no entra en el **rango** —no varía— pero sí en el **pico**, que es lo único
del Apéndice 3 que lo mira.

## C · Las categorías, y el ala que no tiene vida infinita

{{ figura('nch2369-galpon-grua/09', 'curvas', 'Curvas S-N de las categorías B, C, E y F contra el número de ciclos, con los umbrales de vida indefinida en 110, 69, 31 y 55 MPa, los tres conteos de 75 000, 150 000 y 300 000 marcados, el admisible de 298,24835 sobre la curva B a los 150 000 ciclos, y el rango de 118,38827 del ala inferior cruzando la curva B a los 2 404 941 ciclos') }}

### C2 y C3 · El ala inferior está sobre el umbral: esta viga tiene vida finita

$$\frac{\sigma_{SR,i}}{F_{TH}} = {{ vt('nch2369-galpon-grua/09', 'uso_umbral_inf', 5) }} \qquad n = {{ vt('nch2369-galpon-grua/09', 'n_agota_B', 0) }}\ \text{ciclos} \qquad {{ vt('nch2369-galpon-grua/09', 'veces_conteo', 5) }}$$

$$\frac{\sigma_{SR,s}}{F_{TH}} = {{ vt('nch2369-galpon-grua/09', 'uso_umbral_sup', 5) }} \qquad \frac{\sigma_{punta}}{F_{TH}^{A}} = {{ vt('nch2369-galpon-grua/09', 'uso_umbral_punta', 5) }}$$

→ el ala inferior **supera su umbral de vida indefinida por 7,6 %**, así que su soldadura no
dura para siempre: se agota a los {{ v('nch2369-galpon-grua/09', 'n_agota_B', 0) }} ciclos,
{{ v('nch2369-galpon-grua/09', 'veces_conteo', 5) }} veces el conteo de diseño. Arriba, en
cambio, **las dos comprobaciones quedan bajo su umbral** y duran indefinidamente. La misma
sección tiene dos puntos de comportamiento opuesto.

### C4 y C5 · El uso, y el único número que gobierna toda la sensibilidad

$$F_{SR}^{B} = {{ vt('nch2369-galpon-grua/09', 'FSR_B150', 5) }}\ \text{MPa} \qquad {{ vt('nch2369-galpon-grua/09', 'uso_inf', 5) }} \qquad {{ vt('nch2369-galpon-grua/09', 'uso_sup', 5) }}$$

$$\text{clase B: } {{ vt('nch2369-galpon-grua/09', 'FSR_B300', 5) }}\ \text{MPa} \to {{ vt('nch2369-galpon-grua/09', 'uso_inf_B', 5) }} \qquad 2^{0{,}333} = {{ vt('nch2369-galpon-grua/09', 'factor_sens', 5) }} \qquad {{ vt('nch2369-galpon-grua/09', 'razon_usos', 5) }}$$

→ **la fatiga no gobierna**: el ala inferior usa
{{ v('nch2369-galpon-grua/09', 'uso_inf', 5) }} contra el
{{ v('nch2369-galpon-grua/09', 'uso_inf_B', 5) }} que usaría con la clase B. Y ahí está el
número que gobierna toda la sensibilidad de este eslabón: **duplicar los ciclos divide el
admisible por {{ v('nch2369-galpon-grua/09', 'factor_sens', 5) }} en las siete categorías a la
vez**, porque el exponente de la ecuación no depende de la categoría.

## D · La soldadura alma-ala superior, dimensionada

{{ figura('nch2369-galpon-grua/09', 'historial', 'Historial de tensiones bajo el paso de las dos ruedas: el de contacto son dos pulsos aislados porque el largo efectivo de 303,52 mm es mucho menor que los 3 400 de separación entre ruedas, mientras que el de flexión no baja a cero entre las dos, con un ciclo del rango completo y otro del 8,6 por ciento') }}

### D1 a D5 · Las tres componentes, y cuál manda

$$q_s = {{ vt('nch2369-galpon-grua/09', 'q_s', 5) }}\ \text{N}/\text{mm} \qquad w_{loc} = {{ vt('nch2369-galpon-grua/09', 'w_loc', 5) }}\ \text{N}/\text{mm} \qquad {{ vt('nch2369-galpon-grua/09', 'supera_contacto', 5) }} \qquad q_t = {{ vt('nch2369-galpon-grua/09', 'q_t', 5) }}\ \text{N}/\text{mm}$$

$$R = {{ vt('nch2369-galpon-grua/09', 'R_result', 5) }}\ \text{N}/\text{mm} \qquad \frac{R}{2} = {{ vt('nch2369-galpon-grua/09', 'R_soldadura', 5) }}\ \text{N}/\text{mm} \qquad {{ vt('nch2369-galpon-grua/09', 'frac_par', 5) }}$$

→ **la que manda no es el flujo de corte: es la fuerza de contacto de la rueda**, repartida en
el largo efectivo que AIST define él mismo, y la supera en
{{ v('nch2369-galpon-grua/09', 'supera_contacto', 5) }}. El par torsor, que en el 08 valía casi
diez puntos de la interacción, acá vale el
{{ v('nch2369-galpon-grua/09', 'frac_par', 5, 100) }} % de la resultante: se derrama sobre
{{ v('nch2369-galpon-grua/09', 'lef_carril', 2) }} mm de soldadura en vez de concentrarse en una
sección.

### D6 y D7 · La garganta, y las tres puertas que piden un tamaño

$$F_{SR}^{F} = {{ vt('nch2369-galpon-grua/09', 'FSR_F150', 5) }}\ \text{MPa} \qquad a_{fat} = {{ vt('nch2369-galpon-grua/09', 'a_fat_C', 5) }}\ \text{mm} \qquad \text{clase B: } {{ vt('nch2369-galpon-grua/09', 'a_fat_B', 5) }}\ \text{mm}$$

$$\tau_{SR} = {{ vt('nch2369-galpon-grua/09', 'tau_SR', 5) }}\ \text{MPa} \qquad {{ vt('nch2369-galpon-grua/09', 'uso_garg_C', 5) }} \qquad {{ vt('nch2369-galpon-grua/09', 'uso_garg_B', 5) }} \qquad \text{con } {{ vt('nch2369-galpon-grua/09', 'a_min_J24', 0) }}\ \text{mm}: {{ vt('nch2369-galpon-grua/09', 'uso_min_J24', 5) }}$$

$$a_{\text{resistencia}} = {{ vt('nch2369-galpon-grua/09', 'a_resistencia', 5) }}\ \text{mm} \qquad {{ vt('nch2369-galpon-grua/09', 'uso_estatico', 5) }}$$

→ tres puertas piden un tamaño: la resistencia estática
{{ v('nch2369-galpon-grua/09', 'a_resistencia', 5) }} mm, la fatiga con la clase adoptada
{{ v('nch2369-galpon-grua/09', 'a_fat_C', 5) }}, y el mínimo de tabla
{{ v('nch2369-galpon-grua/09', 'a_min_J24', 0) }}. Con la clase C **gobierna el mínimo de tabla
y no hay cálculo que valga**; con la clase B la fatiga pide
{{ v('nch2369-galpon-grua/09', 'a_fat_B', 5) }} mm y ese mínimo **falla**. Se adoptan
**{{ v('nch2369-galpon-grua/09', 'a_alma_ala', 0) }} mm** para que el detalle no dependa de una
decisión que no es del calculista.

## E · Los detalles que la cláusula prohíbe, y la aritmética que los prohíbe

$$F_{SR}^{E} = {{ vt('nch2369-galpon-grua/09', 'FSR_catE', 5) }}\ \text{MPa} \to {{ vt('nch2369-galpon-grua/09', 'uso_acc_C', 5) }} \qquad \text{clase B: } {{ vt('nch2369-galpon-grua/09', 'uso_acc_B', 5) }}$$

$$F_{SR}^{E'} = {{ vt('nch2369-galpon-grua/09', 'FSR_catEp', 5) }}\ \text{MPa} \to {{ vt('nch2369-galpon-grua/09', 'uso_acc_Ep', 5) }} \qquad \text{filete intermitente: } {{ vt('nch2369-galpon-grua/09', 'costo_intermitente', 5) }}$$

→ un accesorio soldado al ala inferior en categoría E pasa **por poco** con la clase adoptada y
**falla** con la clase B: la prohibición es absoluta justamente porque el margen desaparece con
un dato que el diseñador no controla. En categoría E′ falla ya con la clase adoptada. Y el
filete intermitente costaría un factor
{{ v('nch2369-galpon-grua/09', 'costo_intermitente', 5) }} de admisible, con su excepción
inaplicable porque esta grúa es radio-operada y no de botonera: **una letra que el 03 declaró
pensando en el impacto y que reaparece seis eslabones después decidiendo un detalle de taller**.

### E4 · El atiesador transversal, y por qué se corta antes de llegar al ala

$$F_{SR}^{C} = {{ vt('nch2369-galpon-grua/09', 'FSR_catC', 5) }}\ \text{MPa} \qquad y_{st} = {{ vt('nch2369-galpon-grua/09', 'y_st', 5) }}\ \text{mm} \qquad \sigma_{st} = {{ vt('nch2369-galpon-grua/09', 'sigma_st', 5) }}\ \text{MPa}$$

$${{ vt('nch2369-galpon-grua/09', 'uso_atiesador', 5) }} \qquad \text{si llegara al ala: } {{ vt('nch2369-galpon-grua/09', 'uso_si_llega', 5) }} \qquad \frac{\sigma_{st}}{F_{TH}^{C}} = {{ vt('nch2369-galpon-grua/09', 'uso_umbral_pie', 5) }}$$

→ cortar el atiesador antes de llegar al ala rebaja la tensión en
{{ v('nch2369-galpon-grua/09', 'rebaja_cortar', 5) }}, y por eso la nota de usuario de AISC lo
pide. Y hay un detalle que conviene mirar: **el pie del atiesador está más sobre su umbral que
el ala inferior** —{{ v('nch2369-galpon-grua/09', 'uso_umbral_pie', 5) }} contra
{{ v('nch2369-galpon-grua/09', 'uso_umbral_inf', 5) }}— **con menos tensión**. Lo que decide no
es cuánto ve el detalle sino de qué categoría es.

## F · Lo que la fatiga le devuelve a la serie

$$F_{SR}^{B}(N) = {{ vt('nch2369-galpon-grua/09', 'FSR_B75', 5) }}\ \text{MPa} \to {{ vt('nch2369-galpon-grua/09', 'uso_sin_rueda', 5) }} \qquad {{ vt('nch2369-galpon-grua/09', 'razon_conteos', 5) }} \qquad a = {{ vt('nch2369-galpon-grua/09', 'a_sin_rueda', 5) }}\ \text{mm}$$

$$F_{SR}^{B'} = {{ vt('nch2369-galpon-grua/09', 'FSR_Bp150', 5) }}\ \text{MPa} \to {{ vt('nch2369-galpon-grua/09', 'uso_respaldo', 5) }} \qquad {{ vt('nch2369-galpon-grua/09', 'parecido_B', 5) }}$$

→ contar por grúa en vez de por rueda mueve **exactamente el mismo factor** que subir una clase
de edificio, y **casi exactamente el mismo** que dejar el respaldo de la penetración completa en
sitio. Tres decisiones sin nada en común, con el mismo precio.

## Veredicto

**La fatiga no gobierna esta carrilera, y el margen entero lo pone que el galpón sea de
mantención.** El ala traccionada usa {{ v('nch2369-galpon-grua/09', 'uso_inf', 5) }} del
admisible, la comprimida {{ v('nch2369-galpon-grua/09', 'uso_sup', 5) }}, la garganta del filete
{{ v('nch2369-galpon-grua/09', 'uso_garg_C', 5) }} y el atiesador cortado
{{ v('nch2369-galpon-grua/09', 'uso_atiesador', 5) }}. Nada se acerca a la interacción biaxial
que el 08 encontró.

**Pero ese mismo rango supera el umbral de vida indefinida de su propia categoría**, y ése es el
resultado que hay que decir en voz alta: la soldadura del ala inferior **no tiene vida
infinita**. La sección tiene dos puntos de comportamiento opuesto —arriba dura
indefinidamente, abajo la vida está contada—, y el cuarto punto de control, el pie del
atiesador, está **más** sobre su umbral con **menos** tensión.

**La soldadura alma-ala se resuelve con filete continuo de
{{ v('nch2369-galpon-grua/09', 'a_alma_ala', 0) }} mm, y lo que la dimensiona no es lo que se
esperaría**: de las tres componentes que llegan a esa garganta manda la fuerza de contacto de la
rueda y no el flujo de corte.

**Un solo número gobierna toda la sensibilidad**: duplicar los ciclos divide el admisible por
{{ v('nch2369-galpon-grua/09', 'factor_sens', 5) }} en todas las categorías a la vez.

## Límites

- **La clase de edificio se adopta y no se deriva**, igual que en el 08. La fatiga **no cambia
  de signo** con ese dato —el uso pasa de {{ v('nch2369-galpon-grua/09', 'uso_inf', 5) }} a
  {{ v('nch2369-galpon-grua/09', 'uso_inf_B', 5) }}— pero **dos cosas sí**: el filete alma-ala,
  que con la clase B ya no cabe en el mínimo de la Tabla J2.4, y la flecha vertical del 08.
- **El conteo por rueda es exacto para la soldadura y conservador por dos para la flexión.** El
  historial de contacto son dos pulsos aislados, porque el largo efectivo mide
  {{ v('nch2369-galpon-grua/09', 'lef_carril', 2) }} mm y las ruedas van a
  {{ v('nch2369-galpon-grua/09', 'wb_ruedas', 2) }} m; el de flexión **no baja a cero** entre las
  dos ruedas. Con el conteo estricto el uso del ala inferior sería
  {{ v('nch2369-galpon-grua/09', 'uso_sin_rueda', 5) }}. Se mantiene el conservador, porque la
  cláusula no distingue entre detalles y porque la regla de acumulación de daño que haría falta
  para distinguirlos no está en el Apéndice 3, que sólo da amplitud constante.
- **Las tres componentes de la soldadura se suman en su máximo simultáneo.** El flujo de corte
  máximo ocurre con una rueda sobre el apoyo y el contacto máximo bajo la rueda: no son la misma
  posición. El reparto por igual entre las dos soldaduras ignora además que la excentricidad del
  riel carga una más que la otra.
- **La torsión llega a la soldadura como una fuerza repartida y no como un alabeo.** El
  tratamiento riguroso está en una guía que no está en el corpus, igual que en el 08.
- **Este eslabón no tiene visor.** Lo que decide acá son curvas S-N y categorías de detalle, que
  son información de norma y no de modelo. El momento de fatiga es el mismo que el modelo de
  [la carrilera](../../../modelos/carrilera/) dibuja bajo la carga de servicio.

## Ficha

{{ ficha('nch2369-galpon-grua/09') }}

## Referencias

| Clave | Norma y edición | Cláusula | Leída en | Cita textual |
|---|---|---|---|---|
| AISC-A3 | ANSI/AISC 360-22 | Ap. §3.1, el alcance del apéndice y el umbral de 20 000 ciclos | `Normas/A360-22W-ewr.pdf`, p. 272 | «The fatigue resistance of members consisting of shapes or plate shall be determined when the number of cycles of application of live load exceeds 20,000» |
| AISC-A3b | ANSI/AISC 360-22 | Ap. §3.1, el tope de tensión de pico de B4 | PDF ídem, p. 272 | «The maximum permitted stress due to peak cyclic loads shall be 0.66Fy» |
| AISC-A3c | ANSI/AISC 360-22 | Ap. §3.1, el rango como suma numérica en caso de reversión | PDF ídem, p. 272 | «the stress range shall be computed as the numerical sum of maximum repeated tensile and compressive stresses» |
| AISC-A3d | ANSI/AISC 360-22 | Ap. §3.1, las condiciones de corrosión y temperatura que `## Límites` declara | PDF ídem, p. 272 | «applicable to structures with suitable corrosion protection or subjected only to mildly corrosive atmospheres» |
| AISC-A3e | ANSI/AISC 360-22 | Ap. §3.2, análisis elástico y sin factores de concentración | PDF ídem, p. 273 | «Calculated stresses shall be based upon elastic analysis» |
| AISC-A3f | ANSI/AISC 360-22 | Ap. §3.3 y la Ec. A-3-1M, el admisible de las categorías A a E′ — **mirada en PNG**, no extraída | PDF ídem, p. 273 | «the allowable stress range, FSR, shall be determined by Equation A-3-1 or A-3-1M» |
| AISC-A3g | ANSI/AISC 360-22 | Ap. §3.3 y la Ec. A-3-2M, el admisible de la categoría F — **mirada en PNG** | PDF ídem, p. 273 | «For stress category F, the allowable stress range, FSR, shall be determined by Equation A-3-2 or A-3-2M» |
| AISC-A3h | ANSI/AISC 360-22 | Ap. §3.3, la definición del umbral como vida indefinida | PDF ídem, p. 273 | «threshold allowable stress range, maximum stress range for indefinite design life from Table A-3.1» |
| AISC-T1 | ANSI/AISC 360-22 | Tabla A-3.1, caso 1.1, el metal base lejos de toda soldadura, categoría A — **mirada en PNG** | PDF ídem, p. 278 | «Base metal, except noncoated weathering steel, with as-rolled or cleaned surfaces» |
| AISC-T3 | ANSI/AISC 360-22 | Tabla A-3.1, caso 3.1, la soldadura longitudinal alma-ala, categoría B — **mirada en PNG** | PDF ídem, p. 282 | «built up of plates or shapes connected by continuous longitudinal CJP groove welds, back gouged, and welded from second side, or by continuous fillet welds» |
| AISC-T3b | ANSI/AISC 360-22 | Tabla A-3.1, caso 3.2, la caída a B′ con respaldo dejado en sitio — **mirada en PNG** | PDF ídem, p. 282 | «with left-in-place continuous steel backing, or by continuous PJP groove welds» |
| AISC-T3c | ANSI/AISC 360-22 | Tabla A-3.1, caso 3.4, los extremos de filete intermitente, categoría E — **mirada en PNG** | PDF ídem, p. 282 | «Base metal at ends of longitudinal intermittent fillet weld segments» |
| AISC-T5 | ANSI/AISC 360-22 | Tabla A-3.1, caso 5.8, el pie del filete de un atiesador transversal, categoría C — **mirada en PNG** | PDF ídem, p. 288 | «at toe of transverse fillet welds adjacent to welded transverse stiffeners» |
| AISC-T7 | ANSI/AISC 360-22 | Tabla A-3.1, caso 7.1, los accesorios cortos y sus cuatro categorías — **mirada en PNG** | PDF ídem, p. 294 | «where the detail embodies no transition radius» |
| AISC-T7b | ANSI/AISC 360-22 | Tabla A-3.1, nota [a], qué es un accesorio y por qué degrada | PDF ídem, p. 294 | «is defined as any steel detail welded to a member that causes a deviation in the stress flow in the member» |
| AISC-T8 | ANSI/AISC 360-22 | Tabla A-3.1, caso 8.2, el corte en la garganta de cualquier filete, categoría F — **mirada en PNG** | PDF ídem, p. 296 | «Shear on throat of any fillet weld, continuous or intermittent, longitudinal or transverse» |
| AISC-J24 | ANSI/AISC 360-22 | §J2.2b (a), que el filete no baje del mínimo de la Tabla J2.4 — la cláusula **se derrama** a la página siguiente, donde está la tabla | PDF ídem, p. 195 | «The minimum size of fillet welds shall be not less than the size required to transmit calculated forces nor the size as shown in Table J2.4» |
| AISC-J24t | ANSI/AISC 360-22 | Tabla J2.4, que el mínimo se mide sobre la parte **más delgada**, que acá es el alma — **mirada en PNG** | PDF ídem, p. 196 | «Material Thickness of Thinner Part Joined» |
| AISC-J24b | ANSI/AISC 360-22 | §J2.2b, la nota de usuario que detiene el atiesador antes del ala | PDF ídem, p. 196 | «are stopped 4 to 6 times the web thickness from the web toe of the flange-to web fillet weld» |
| AIST-1 | AIST TR-13:2021 | Tabla 1.1, los cuatro rangos de ciclos y su base de 50 años — **mirada en PNG** | `Normas/aist-tr-no13-2021-3.pdf`, p. 11 | «About 5 applications per day for 50 years» |
| AIST-1b | AIST TR-13:2021 | §1.4.3, la clase C de edificio entre 20 000 y 100 000 repeticiones | PDF ídem, p. 10 | «Buildings in this category are those buildings in which members experience 20,000 to 100,000 repetitions of a specific loading» |
| AIST-1c | AIST TR-13:2021 | §1.4, que la clasificación la especifica el propietario | PDF ídem, p. 10 | «the owner shall specify the classification for all or any portion of a building» |
| AIST-3 | AIST TR-13:2021 | §3.11.2.3, la carga de fatiga y los ciclos atados a la clasificación de edificio | PDF ídem, p. 23 | «The number of cycles used as the basis for fatigue design shall be consistent with the building classification» |
| AIST-3b | AIST TR-13:2021 | §3.11.2.3, que el propietario debe designar un aumento de repeticiones si el uso lo justifica | PDF ídem, p. 23 | «The owner shall designate an increase in the estimated number of load repetitions» |
| AIST-5 | AIST TR-13:2021 | §5.7, que la fatiga se resuelve con la última edición de AISC y la Tabla 1.1 | PDF ídem, p. 30 | «shall be designed in accordance with the fatigue requirements of the latest edition of AISC Specification for Structural Steel Buildings» |
| AIST-5b | AIST TR-13:2021 | §5.7, la remisión a la Tabla 1.1 para cruzar clase con ciclos | PDF ídem, p. 30 | «See Table 1.1 cross-referencing Building Classification from Chapter 1 to load cycles» |
| AIST-58 | AIST TR-13:2021 | §5.8.1, la penetración completa con filetes contorneados por defecto | PDF ídem, p. 31 | «a full-penetration weld with contoured fillets shall be used between the web and top flange» |
| AIST-58b | AIST TR-13:2021 | §5.8.1, la excepción de filete continuo para las clases C y D | PDF ídem, p. 31 | «For building classes C and D, continuous fillet welds may be used provided that the welds are designed to carry the full applied loading» |
| AIST-58c | AIST TR-13:2021 | §5.8.1, que el diseño de esa soldadura considere el contacto de la rueda y la torsión | PDF ídem, p. 31 | «This weld design shall consider contact forces due to vertical crane wheel loads and potential out-of-plane forces and torsional moments» |
| AIST-58d | AIST TR-13:2021 | §5.8.1, el conteo de ciclos por cada rueda individual | PDF ídem, p. 31 | «the load cycles on this weld should account for additional stress variations when each individual crane wheel passes the location in question» |
| AIST-58e | AIST TR-13:2021 | §5.8.1, el filete admitido en el ala inferior, continuo y diseñado para resistencia y fatiga | PDF ídem, p. 31 | «provided they are continuous welds on both sides of the web and designed for both strength and fatigue limit states» |
| AIST-58f | AIST TR-13:2021 | §5.8.1, el filete intermitente prohibido y su excepción de botonera | PDF ídem, p. 31 | «except for cover plate and stiffener welds on girders for pendant controlled cranes operating in Building Classes C and D» |
| AIST-58g | AIST TR-13:2021 | §5.8.1, la prohibición absoluta de accesorios soldados al ala inferior | PDF ídem, p. 31 | «There shall be no welded attachments to the bottom flange of the crane girder» |
| AIST-58h | AIST TR-13:2021 | §5.8.2, la torsión de la carga vertical con el riel desalineado del alma | PDF ídem, p. 31 | «Torsional moments are also generated by crane vertical wheel loads if the centerline of rail does not align with the centerline of the crane girder web» |
| AIST-58i | AIST TR-13:2021 | §5.8.2, que la solución exacta de la torsión queda fuera del alcance del documento | PDF ídem, p. 31 | «is complex and beyond the scope of this document» |
| AIST-58j | AIST TR-13:2021 | §5.8.4, el largo efectivo de alma bajo la rueda, que D3 vuelve a usar | PDF ídem, p. 33 | «the effective length of web beneath the wheel load shall be equal to two times the combined depth of the crane rail and girder flange thickness» |
| AIST-58k | AIST TR-13:2021 | §5.8.3, los atiesadores de apoyo cuya categoría E4 fija y el 10 dimensiona | PDF ídem, p. 33 | «Bearing stiffeners shall be used where required to transmit end reactions» |
| AIST-59 | AIST TR-13:2021 | §5.8.9, que no haya accesorios ni dispositivos fuera de los indicados en los planos | PDF ídem, p. 34 | «There shall be no attachments or fixtures of any kind, other than those designated on the design drawings» |
| AIST-517 | AIST TR-13:2021 | §5.17.6, la excentricidad máxima del riel que B3 vuelve a usar | PDF ídem, p. 40 | «In no case shall the rail eccentricity be greater than three-fourths of the girder web thickness» |
| AIST-311 | AIST TR-13:2021 | §3.11.2.1, la combinación 2c, que separa la carga muerta de la grúa de la izada | PDF ídem, p. 23 | «Load and Resistance Factor Design (LRFD) Load Combinations» |
| N3171-w | NCh3171:2017 | §9.1.1 (2), la combinación con que D7 mayora la carga de grúa | `referencias/NCh3171-2017/cap09-combinaciones-de-carga.md` | |
| NCh-w | NCh2369:2025 (3.ª ed.) | §5.1.2, la carga permanente con que B4 arma la tensión de pico | `referencias/NCh2369-2025/cap05-analisis-sismico.md` | |
| AISC-w | ANSI/AISC 360-22 | §B4 y §F11, las propiedades de sección y el módulo del ala en su plano que B2 y B3 reusan | `referencias/AISC360-22/capB-requisitos-de-diseno.md` | |
| AISC-w2 | ANSI/AISC 360-22 | §G2.1, el primer momento y el flujo de corte con que D2 reparte a la soldadura | `referencias/AISC360-22/capG-corte.md` | |
| AISC-w3 | ANSI/AISC 360-22 | §J2.4, la resistencia de diseño de un filete que D7 usa | `referencias/AISC360-22/capJ-conexiones.md` | |
