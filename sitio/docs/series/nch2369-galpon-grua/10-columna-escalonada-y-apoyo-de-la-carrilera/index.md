# 10 · La columna escalonada y el apoyo de la carrilera

El umbral que descarta la ménsula **es de fatiga**, y ningún chequeo de tensión lo habría
encontrado: el rango en su raíz no depende ni de la reacción ni del voladizo. Lo que entra en su
lugar es la columna escalonada, con su fuste de grúa a un metro del eje. Acá se dimensiona ese
fuste, se resuelve la estabilidad del conjunto y se detalla el asiento de la carrilera. Fuerzas
en kN, longitudes en mm salvo donde se indique.

## El caso

{{ figura('nch2369-galpon-grua/10', 'columna', 'Elevación de la columna escalonada con la escala horizontal exagerada: el fuste del edificio de 1 050 a 750 mm de alma variable, el fuste de grúa de 400 mm a 1 000 del eje, la placa de alma continua de 10 mm entre los dos, el asiento de la carrilera a 6 684,24 mm, el largo del fuste superior de 3 815,76 y el parámetro a_r de 0,36341; a un lado, la ménsula descartada con su reacción de 299,25983 kN igual a 67,27631 kips contra el tope de 50') }}

| Dato | Valor |
|---|---|
| Elemento | la columna del 07, con el fuste que soporta la carrilera |
| Altura libre | {{ v('nch2369-galpon-grua/10', 'H_col_mm', 0) }} mm, alma variable {{ v('nch2369-galpon-grua/10', 'd_col_base', 0) }} → {{ v('nch2369-galpon-grua/10', 'd_col_nudo', 0) }} (del 07) |
| Excentricidad del riel | {{ v('nch2369-galpon-grua/10', 'e_col_riel', 2) }} mm al eje de columna (A2) |
| Cota del asiento | {{ v('nch2369-galpon-grua/10', 'h_asiento', 2) }} mm (A2) |
| Fuste de grúa adoptado | {{ v('nch2369-galpon-grua/10', 'd_fuste_grua', 0) }} × {{ v('nch2369-galpon-grua/10', 'bf_fuste_grua', 0) }}, alas {{ v('nch2369-galpon-grua/10', 'tf_fuste_grua', 0) }}, alma {{ v('nch2369-galpon-grua/10', 'tw_fuste_grua', 0) }} (S2) |
| Placa de alma continua | {{ v('nch2369-galpon-grua/10', 'tp_alma', 0) }} mm (S3) |
| Reacción de la carrilera | {{ v('nch2369-galpon-grua/10', 'Rcol_grua', 5) }} kN (del 07) |
| Acero | ASTM A572 Gr. 50: $F_y = {{ vt('nch2369-galpon-grua/10', 'Fy', 0) }}$ MPa, $R_y = {{ vt('nch2369-galpon-grua/10', 'Ry', 2) }}$ |
| Lo que se decide aquí | el fuste de grúa, la estabilidad del escalón y el asiento |

Los supuestos, en una línea cada uno. **S1**, el acero es el mismo del 07. **S2**, el fuste de
grúa y la placa de alma son los adoptados acá. **S3**, la excentricidad se resuelve como un
**momento aplicado en el escalón**, no como un problema de transferencia: la placa reparte sobre
una longitud que este modelo no ve. **S4**, la carrilera se apoya sobre el fuste de grúa por
contacto, con atiesadores ajustados a tope. **S5**, el marco **no se rehace** con la sección
compuesta: el eslabón mide cuánto vale no hacerlo y publica el factor para que el 12 lo herede.
**S6**, el arriostramiento fuera del plano está en el asiento y no hay uno intermedio.

## A · El umbral que descarta la ménsula, y que resulta ser de fatiga

### A1 · §5.9.2 no dimensiona la ménsula: la admite o no la admite

$$R = {{ vt('nch2369-galpon-grua/10', 'R_u_reob', 5) }}\ \text{kN} \qquad 50\ \text{kips} = {{ vt('nch2369-galpon-grua/10', 'tope_kips', 5) }}\ \text{kN} \qquad {{ vt('nch2369-galpon-grua/10', 'R_kips', 5) }}\ \text{kips} \qquad {{ vt('nch2369-galpon-grua/10', 'uso_mensula', 5) }}$$

→ la reacción, reobtenida desde el 03, cierra contra la del 07 dentro de
{{ v('nch2369-galpon-grua/10', 'cierre_07', 5) }} kN, y **excede el tope de la cláusula en
{{ v('nch2369-galpon-grua/10', 'uso_mensula', 5) }}**. La ménsula no califica.

### A2 y A3 · El tope de 50 kips es de fatiga, y el rango no depende de la reacción

$$M_u = {{ vt('nch2369-galpon-grua/10', 'M_u_raiz', 5) }}\ \text{kN}\cdot\text{m} \qquad S_{req} = {{ vt('nch2369-galpon-grua/10', 'S_req', 0) }}\ \text{mm}^3 \qquad \sigma_{SR} = {{ vt('nch2369-galpon-grua/10', 'sr_raiz', 5) }}\ \text{MPa}$$

$${{ vt('nch2369-galpon-grua/10', 'uso_raiz_C', 5) }} \qquad {{ vt('nch2369-galpon-grua/10', 'uso_raiz_E', 5) }} \qquad {{ vt('nch2369-galpon-grua/10', 'uso_raiz_Ep', 5) }}$$

→ y acá está la razón del tope: **el rango en la raíz no depende de la reacción**, porque el
módulo requerido crece con ella en la misma proporción. Da
{{ v('nch2369-galpon-grua/10', 'sr_raiz', 5) }} MPa **con cualquier ménsula dimensionada por
resistencia**, y eso pasa en categoría C, no pasa en E y no pasa en E′. **Ningún chequeo de
tensión habría encontrado ese umbral**: es una cláusula que codifica un resultado de fatiga.

## B · La columna escalonada: geometría y sección compuesta

{{ figura('nch2369-galpon-grua/10', 'seccion', 'Sección compuesta del fuste inferior en la base, con el fuste del edificio de 1 050 mm de alma, la placa de unión de 10 mm de 275 de largo y el fuste de grúa de 400 mm a 1 000 del eje; el centroide compuesto queda a 348,66036 mm hacia la grúa, con 873,66036 a la fibra exterior y 851,33964 a la interior, sobre un ancho total de 1 725 mm') }}

### B1 a B3 · El escalón, la placa y un centroide que ya no está en el eje

$$d_{paso} = {{ vt('nch2369-galpon-grua/10', 'd_paso', 5) }}\ \text{mm} \qquad L_{sup} = {{ vt('nch2369-galpon-grua/10', 'L_sup', 5) }}\ \text{mm} \qquad a_r = {{ vt('nch2369-galpon-grua/10', 'a_r', 5) }} \qquad L_p^{base} = {{ vt('nch2369-galpon-grua/10', 'Lp_base', 5) }}\ \text{mm}$$

$$A = {{ vt('nch2369-galpon-grua/10', 'Ag_comp_base', 5) }}\ \text{mm}^2 \qquad \bar{x} = {{ vt('nch2369-galpon-grua/10', 'xb_comp_base', 5) }}\ \text{mm} \qquad I_x = {{ vt('nch2369-galpon-grua/10', 'Ix_comp_base', 0) }}\ \text{mm}^4 \qquad {{ vt('nch2369-galpon-grua/10', 'multiplica_I', 5) }}$$

→ la sección compuesta **multiplica por {{ v('nch2369-galpon-grua/10', 'multiplica_I', 5) }} la
inercia** que el 07 tenía en la base, y su centroide ya no está en el eje de la columna: se corre
{{ v('nch2369-galpon-grua/10', 'xb_comp_base', 5, -1) }} mm hacia la grúa. Todo lo que sigue
depende de eso.

### B4 y B5 · El parámetro B, y el peso que vuelve a crecer

$$B = \frac{I_x}{I_{sup}} = {{ vt('nch2369-galpon-grua/10', 'B_param', 5) }} \qquad w_{07} = {{ vt('nch2369-galpon-grua/10', 'w_07', 5) }}\ \text{kN}/\text{m} \qquad w_{add} = {{ vt('nch2369-galpon-grua/10', 'w_add', 5) }}\ \text{kN}/\text{m}$$

$$w_{10} = {{ vt('nch2369-galpon-grua/10', 'w_col_10', 5) }}\ \text{kN}/\text{m} \qquad {{ vt('nch2369-galpon-grua/10', 'supera_05', 5) }} \qquad w_{marco} = {{ vt('nch2369-galpon-grua/10', 'w_marco_10', 2) }}\ \text{kN}$$

→ la línea de columnas pesa {{ v('nch2369-galpon-grua/10', 'w_col_10', 5) }} kN/m,
{{ v('nch2369-galpon-grua/10', 'supera_05', 5) }} veces lo que el 05 declaró, y **el marco se
pasa de su presupuesto**: {{ v('nch2369-galpon-grua/10', 'w_marco_10', 2) }} kN contra los
{{ v('nch2369-galpon-grua/10', 'w_marco_07', 5) }} que el 07 tenía. Es la segunda corrección de
peso que la serie acumula sin rehacerse, después de la carrilera del 08.

## C · Por dónde bajan los {{ v('nch2369-galpon-grua/10', 'Rcol_grua', 2) }} kN

### C1 y C2 · El momento neto es la mitad del de la grúa sola

$$e_1 = {{ vt('nch2369-galpon-grua/10', 'e_1', 5) }}\ \text{mm} \qquad e_2 = {{ vt('nch2369-galpon-grua/10', 'e_2', 5) }}\ \text{mm} \qquad M_1 = {{ vt('nch2369-galpon-grua/10', 'M_1', 5) }} \qquad M_2 = {{ vt('nch2369-galpon-grua/10', 'M_2', 5) }}\ \text{kN}\cdot\text{m}$$

$$M = {{ vt('nch2369-galpon-grua/10', 'Mecc_10', 5) }}\ \text{kN}\cdot\text{m} \qquad {{ vt('nch2369-galpon-grua/10', 'cancela', 5) }} \qquad {{ vt('nch2369-galpon-grua/10', 'sobrestima', 5) }}$$

→ el axial del techo y la reacción de la grúa caen a **lados opuestos** del centroide compuesto,
así que sus momentos se restan: el neto es
{{ v('nch2369-galpon-grua/10', 'cancela', 5, 100) }} % del de la grúa sola. Contar sólo la grúa
lo sobrestimaría por {{ v('nch2369-galpon-grua/10', 'sobrestima', 5) }}.

## D · La estabilidad, por la ruta que §5.9.4 nombra

### D0 · Lo que dimensiona el fuste de grúa es la Tabla 9, y por tercera vez en la serie

$$\lambda_{md} = {{ vt('nch2369-galpon-grua/10', 'lam_md', 5) }} \qquad \frac{(b_f - t_w)/2}{t_f} = {{ vt('nch2369-galpon-grua/10', 'lam_ala_fuste', 5) }} \to {{ vt('nch2369-galpon-grua/10', 'uso_ala_fuste', 5) }} \qquad \text{con } {{ vt('nch2369-galpon-grua/10', 'tf_fuste_14', 0) }}\ \text{mm}: {{ vt('nch2369-galpon-grua/10', 'uso_ala_14', 5) }}$$

$$C_a = {{ vt('nch2369-galpon-grua/10', 'Ca_comp', 5) }} \qquad \lambda_{md}^{alma} = {{ vt('nch2369-galpon-grua/10', 'lam_alma_md', 5) }} \qquad \text{alma del 07: } {{ vt('nch2369-galpon-grua/10', 'uso_alma_07', 5) }} \qquad \text{alma del fuste: } {{ vt('nch2369-galpon-grua/10', 'uso_alma_fuste', 5) }}$$

→ **el ala de {{ v('nch2369-galpon-grua/10', 'tf_fuste_grua', 0) }} mm la pone la Tabla 9, en uso
{{ v('nch2369-galpon-grua/10', 'uso_ala_fuste', 5) }}**; con
{{ v('nch2369-galpon-grua/10', 'tf_fuste_14', 0) }} no pasaría. Y hay una consecuencia de vuelta:
con el área compuesta, el uso del alma de la columna del 07 —el número que aquel eslabón llamó el
más frágil— baja a {{ v('nch2369-galpon-grua/10', 'uso_alma_07', 5) }}.

### D4 y D5 · Los largos efectivos, y que no gobierna ninguno

$$K_L = {{ vt('nch2369-galpon-grua/10', 'K_L', 5) }} \qquad K_U = {{ vt('nch2369-galpon-grua/10', 'K_U', 5) }} \qquad L_{ef}^{inf} = {{ vt('nch2369-galpon-grua/10', 'L_ef_inf', 5) }} \qquad L_{ef}^{sup} = {{ vt('nch2369-galpon-grua/10', 'L_ef_sup', 5) }}\ \text{mm}$$

$$\frac{L_{ef}^{inf}}{r_x} = {{ vt('nch2369-galpon-grua/10', 'esb_plano_Lef', 5) }} \qquad \frac{h_{as}}{r_y} = {{ vt('nch2369-galpon-grua/10', 'esb_fuera', 5) }} \qquad {{ vt('nch2369-galpon-grua/10', 'mas_esbelto', 5) }}$$

→ las cuatro Comm Tablas del largo efectivo, que la serie temía tener que buscar fuera del
corpus, **están y no gobiernan nada**: el eje débil es
{{ v('nch2369-galpon-grua/10', 'mas_esbelto', 5) }} veces más esbelto, y el propio Comentario lo
anuncia en una frase.

### D6 · La columna escalonada cruza la frontera que el 07 puso de techo, y no cuesta nada

$$k_{esc} = {{ vt('nch2369-galpon-grua/10', 'k_esc', 5) }} \qquad k_Y k_{esc} = {{ vt('nch2369-galpon-grua/10', 'k_esc_marco', 5) }}\ \text{kN}/\text{m} \qquad T = {{ vt('nch2369-galpon-grua/10', 'T_esc', 5) }}\ \text{s} \qquad {{ vt('nch2369-galpon-grua/10', 'cruza_techo', 5) }}$$

$$R^{*} = {{ vt('nch2369-galpon-grua/10', 'R_deg', 5) }} \qquad 0{,}7R^{*} = {{ vt('nch2369-galpon-grua/10', 'kcap_nuevo', 5) }} \qquad Q_0^{an} = {{ vt('nch2369-galpon-grua/10', 'Q0_esc', 5) }}\ \text{kN} \qquad {{ vt('nch2369-galpon-grua/10', 'supera_techo', 5) }}$$

$$d = {{ vt('nch2369-galpon-grua/10', 'd_esc', 5) }}\ \text{mm} \qquad {{ vt('nch2369-galpon-grua/10', 'uso_63', 5) }}$$

→ la columna escalonada rigidiza el marco {{ v('nch2369-galpon-grua/10', 'k_esc', 5) }} veces y
**cruza por {{ v('nch2369-galpon-grua/10', 'cruza_techo', 5) }} la frontera de la rampa** que el
07 había puesto de techo: $R^{*}$ degrada. Y aun así las cuatro consecuencias son favorables o
nulas: el corte de diseño no se mueve porque el techo de §5.13 lo sigue mordiendo, el
amplificador de capacidad baja de {{ v('nch2369-galpon-grua/10', 'kcap_Y', 2) }} a
{{ v('nch2369-galpon-grua/10', 'kcap_nuevo', 5) }}, y la deriva sísmica cae a
{{ v('nch2369-galpon-grua/10', 'uso_63', 5) }} de su límite.

El modelo del sitio **sí** lleva esa columna. El visor la muestra con su cambio de sección en el
asiento, y el axial creciendo hacia la base:

<rukan-visor src="../../../modelos/galpon-grua/galpon-grua.escena.json" caso="D" esfuerzo="N" filtro="COL3A_*,COL3B_*" vista="transversal"></rukan-visor>

## E · Las resistencias de los dos fustes

$$\phi P_n = {{ vt('nch2369-galpon-grua/10', 'phiPn_inf', 5) }}\ \text{kN} \to {{ vt('nch2369-galpon-grua/10', 'uso_axial_inf', 5) }} \qquad \phi M_n = {{ vt('nch2369-galpon-grua/10', 'phiMn_inf', 5) }}\ \text{kN}\cdot\text{m} \to {{ vt('nch2369-galpon-grua/10', 'uso_flex_inf', 5) }}$$

$$M_u = {{ vt('nch2369-galpon-grua/10', 'M_u_inf', 5) }}\ \text{kN}\cdot\text{m} \qquad \text{H1-1b} = {{ vt('nch2369-galpon-grua/10', 'interaccion', 5) }} \qquad {{ vt('nch2369-galpon-grua/10', 'multiplica_cap', 5) }}$$

→ la interacción cierra en {{ v('nch2369-galpon-grua/10', 'interaccion', 5) }} y la capacidad
flexural de la base es {{ v('nch2369-galpon-grua/10', 'multiplica_cap', 5) }} veces la que el 07
tenía. **Ni la compresión ni la flexión deciden nada**: lo que dimensionó el fuste fue la Tabla 9.

## F · El apoyo de la carrilera sobre el fuste de grúa

{{ figura('nch2369-galpon-grua/10', 'apoyo', 'Detalle del asiento de la carrilera sobre el fuste de grúa: atiesadores de apoyo de 110 por 12 con destalonado de 25 mm ajustados a tope contra el ala inferior, el riel de 131,76 mm con sus grapas en pares opuestos a 750 mm sin ganchos de riel, y el tirante empernado al ala superior, admisible ahí con uso 0,57246 en categoría E y no al ala inferior, donde daría 0,87966') }}

$$R_u = {{ vt('nch2369-galpon-grua/10', 'R_u_apoyo', 5) }}\ \text{kN} \qquad \phi P_n^{st} = {{ vt('nch2369-galpon-grua/10', 'phiPn_st', 5) }}\ \text{kN} \to {{ vt('nch2369-galpon-grua/10', 'uso_st_col', 5) }} \qquad \phi R_n^{pb} = {{ vt('nch2369-galpon-grua/10', 'phiRn_pb', 5) }} \to {{ vt('nch2369-galpon-grua/10', 'uso_st_contacto', 5) }}$$

$$\text{tirante al ala superior: } {{ vt('nch2369-galpon-grua/10', 'uso_tir_E', 5) }} \qquad \text{al ala inferior: } {{ vt('nch2369-galpon-grua/10', 'uso_inf_E', 5) }} \qquad {{ vt('nch2369-galpon-grua/10', 'razon_alas', 5) }}$$

$$\text{grúa} = {{ vt('nch2369-galpon-grua/10', 'cap_short_tons', 5) }}\ \text{short tons} \qquad \text{tope} = 20 \qquad {{ vt('nch2369-galpon-grua/10', 'uso_tope_20', 5) }}$$

→ el tirante va al ala superior y **no al ala inferior**, y la diferencia es exactamente la razón
de módulos que el ala grande del 08 creó:
{{ v('nch2369-galpon-grua/10', 'razon_alas', 5) }}. Y las grapas van en pares opuestos a
{{ v('nch2369-galpon-grua/10', 'sep_grapas_adopt', 0) }} mm **sin ganchos de riel**, porque esta
grúa son {{ v('nch2369-galpon-grua/10', 'cap_short_tons', 5) }} short tons contra un tope de 20.
Es el tercer umbral de admisión que este galpón no pasa, **y el único que se cruza por leer el
número en el sistema de unidades equivocado**: en toneladas métricas son
{{ v('nch2369-galpon-grua/10', 'cap_metricas', 5) }}, que sí cabrían.

## Veredicto

**La ménsula no se descarta por cálculo sino por cláusula**, y este eslabón muestra por qué tenía
que ser así: el rango de fatiga en su raíz no depende ni de la reacción ni del voladizo. Lo que
entra en su lugar es la columna escalonada, cuyo ala **la dimensiona la Tabla 9** en
{{ v('nch2369-galpon-grua/10', 'uso_ala_fuste', 5) }} mientras el axial la usa en
{{ v('nch2369-galpon-grua/10', 'uso_axial_inf', 5) }}.

**Las cuatro Comm Tablas del largo efectivo están en el corpus y no gobiernan nada.** La columna
escalonada rigidiza el marco {{ v('nch2369-galpon-grua/10', 'k_esc', 5) }} veces y cruza la
frontera de la rampa, pero las cuatro consecuencias son favorables o nulas.

Del asiento salen cuatro detalles y una prohibición, y la prohibición es la interesante: **sin
ganchos de riel**, por un umbral escrito en short tons.

## Límites

- **Tres filas del `## Resumen` del memo no reproducen**, y son la misma especie que las del 07 y
  el 08: el memo imprime un dígito que su propia aritmética sobre las cifras impresas no da. La
  mayor es la esbeltez en el plano del fuste superior, donde dividir las dos cifras publicadas da
  28,75747 y el memo escribe 28,75752. Ninguna se propaga.
- **El marco no se rehace, y la descripción que la serie arrastra queda desfasada.** El
  Comentario dice que la inercia de la sección compuesta **puede** usarse en el análisis del
  marco; este eslabón no la usa y mide el error. El sentido del desfase es favorable en los
  cuatro frentes que la serie verifica, pero eso es una consecuencia medida, no una propiedad
  general. **El 12 hereda `k_esc` justamente para no repetir el error.**
- **El factor de rigidización sale de correr dos veces el mismo modelo**, y eso es lo único que
  lo hace legítimo: ninguno de los dos valores absolutos es un resultado de este eslabón; el
  cociente sí, porque sólo cambia la sección del tramo inferior.
- **El modelo 3D del sitio tiene la columna escalonada, y su constante de torsión está mal.** La
  `J` de la sección compuesta se calcula en el repositorio con el lado largo como espesor, lo que
  la infla unas cinco mil veces en el término del alma. Corregirla mueve todos los resultados del
  modelo entre 10⁻⁹ y 10⁻⁵ relativo —nada cambia de signo ni de conclusión— pero **saca una cifra
  publicada del eslabón 00 de su tolerancia**, así que es un cambio de la clase de la cascada y
  se hace aparte, no dentro de este lote. El mismo defecto en la viga carrilera **sí** se
  corrigió, porque ahí el memo 08 publica un `J` contra el cual comprobarlo.
- **La excentricidad se resuelve como un momento aplicado en el escalón**, no como un problema de
  transferencia: hay una longitud sobre la que la placa reparte, y concentraciones cerca del
  escalón que este modelo no ve. El Comentario lo dice para la ménsula y vale igual acá.
- **La sección compuesta no es una de las formas del Capítulo F de AISC.** La capacidad flexural
  se toma como el momento de fluencia de la fibra extrema, sin verificar pandeo lateral-torsional
  ni pandeo local.
- **Los dos métodos de estabilidad se corren y ninguno decide.** Si el arriostramiento fuera del
  plano estuviera donde el supuesto lo pone y hubiera uno intermedio, el eje débil dejaría de
  gobernar y la elección pasaría a importar.
- **La interpolación en la Comm Tabla es lineal y la tabla no lo es.**

## Ficha

{{ ficha('nch2369-galpon-grua/10') }}

## Referencias

| Clave | Norma y edición | Cláusula | Leída en | Cita textual |
|---|---|---|---|---|
| AIST-59 | AIST TR-13:2021 | §5.9, los tres esquemas de columna que el documento reconoce | `Normas/aist-tr-no13-2021-3.pdf`, p. 34 | «Common approaches are to use built-up stepped columns, crane girders supported on brackets attached to building columns, and independent crane columns» |
| AIST-591 | AIST TR-13:2021 | §5.9.1, la columna escalonada armada y el comportamiento integral que B2 exige | PDF ídem, p. 35 | «shall have the connecting segments and their connections designed to provide integral behavior of the combined column section» |
| AIST-591b | AIST TR-13:2021 | §5.9.1, la flexión por excentricidad de la reacción sobre la placa de tope, que es lo que C1 y C2 calculan | PDF ídem, p. 35 | «Bending of the columns due to eccentricity of crane girder reaction on the column cap plate shall be included» |
| AIST-591c | AIST TR-13:2021 | §5.9.1, los diafragmas intermitentes y la celosía, que `## Límites` deja fuera | PDF ídem, p. 35 | «the column shafts between panel points and the intermediate web members shall be designed for forces» |
| AIST-592 | AIST TR-13:2021 | §5.9.2, **el umbral que descarta la ménsula**, que A1 mide | PDF ídem, p. 35 | «Brackets should only be used to support crane runway girders when the total girder reactions at the column are less than 50 kips» |
| AIST-592b | AIST TR-13:2021 | §5.9.2, que el impacto entra al diseño de la ménsula y de su conexión | PDF ídem, p. 35 | «impact shall be included in the bracket design and its connection to the column» |
| AIST-592c | AIST TR-13:2021 | §5.9.2, los atiesadores de apoyo en el extremo de la viga que F1 adopta | PDF ídem, p. 35 | «it is recommended that bearing stiffeners in the girder be positioned at or near the end of the girder» |
| AIST-593 | AIST TR-13:2021 | §5.9.3, la columna de grúa independiente que A4 descarta | PDF ídem, p. 35 | «These columns are designed to only support vertical loads from the crane girders» |
| AIST-594 | AIST TR-13:2021 | §5.9.4, la flexión biaxial y la remisión de la estabilidad al Capítulo C de AISC | PDF ídem, p. 35 | «Stability calculations for buckling shall meet the requirements of Chapter C of Ref. 1» |
| AIST-594b | AIST TR-13:2021 | §5.9.4, que todos los detalles de conexión consideren fatiga por cargas de grúa | PDF ídem, p. 35 | «All connection details should incorporate appropriate consideration for fatigue with regards to crane loads» |
| AIST-595 | AIST TR-13:2021 | §5.9.5, la base sobre el nivel de piso y la protección contra daño que `## Límites` recoge | PDF ídem, p. 35 | «Column bases should be above grade and designed to avoid trapping moisture and dirt» |
| AIST-512 | AIST TR-13:2021 | §5.12, el espesor mínimo de material que fija el piso de la placa de alma | PDF ídem, p. 36 | «The minimum thickness of material exclusive of secondary members such as purlins and girts shall be» |
| AIST-513 | AIST TR-13:2021 | §5.13, el deslizamiento crítico obligatorio por carga cíclica que G1 usa | PDF ídem, p. 36 | «slip critical-type high-strength bolted connections shall be used for members subjected to fatigue cyclic loading or vibrations» |
| AIST-513b | AIST TR-13:2021 | §5.13, que todo perno estructural vaya pretensado | PDF ídem, p. 36 | «All bolted structural connections shall be made with pre-tensioned high-strength bolts» |
| AIST-514 | AIST TR-13:2021 | §5.14, la separación de pernos del diafragma horizontal que G2 mide y no aplica | PDF ídem, p. 36 | «the bolt spacing shall be no greater than required for full transfer of shear» |
| AIST-514b | AIST TR-13:2021 | §5.14, la soldadura continua arriba y abajo si el diafragma va soldado | PDF ídem, p. 36 | «Where a horizontal diaphragm is used and the connection is welded, the weld must be continuous top and bottom» |
| AIST-515 | AIST TR-13:2021 | §5.15, las cinco consideraciones de selección del riel | PDF ídem, p. 36 | «In the selection of crane rail type and size, consideration shall be given to the following» |
| AIST-5151 | AIST TR-13:2021 | §5.15.1, la luz máxima de la junta apernada que F5 mide | PDF ídem, p. 36 | «Bolted rail joints should be supplied as "tight fit" joints to limit the gap between rail ends» |
| AIST-5152 | AIST TR-13:2021 | §5.15.2, la junta soldada que reduce el impacto de la rueda | PDF ídem, p. 37 | «Continuously welded rail joints minimize impact forces as crane wheels pass over the joints» |
| AIST-5153 | AIST TR-13:2021 | §5.15.3, las grapas en pares opuestos y su separación máxima, que F4 adopta | PDF ídem, p. 37 | «Crane rail clips or clamps shall be placed in opposing pairs, spaced not over 30 in. on centers» |
| AIST-5153b | AIST TR-13:2021 | §5.15.3, **el tope de 20 tons que prohíbe los ganchos de riel**, que F4 mide | PDF ídem, p. 37 | «Hook bolts should not be used in Class A and B buildings or for crane runways supporting cranes with lifting capacities more than 20 tons» |
| AIST-5153c | AIST TR-13:2021 | §5.15.3, que la separación baje a 18-24 in con empuje alto y ciclos frecuentes | PDF ídem, p. 37 | «spacing in the 18 to 24 in. range should be considered» |
| AIST-581 | AIST TR-13:2021 | §5.8.1, las conexiones independientes al final y al tope de cada viga, que F1 y F3 diseñan | PDF ídem, p. 30 | «Independent connections to the column at the end and top of each girder shall be provided» |
| AIST-581b | AIST TR-13:2021 | §5.8.1, el detalle que minimiza la restricción al giro de extremo | PDF ídem, p. 30 | «designed and detailed to minimize restraint of girder end rotations» |
| AIST-581c | AIST TR-13:2021 | §5.8.1, **la prohibición absoluta de accesorios soldados al ala inferior**, que F2 aplica | PDF ídem, p. 31 | «There shall be no welded attachments to the bottom flange of the crane girder» |
| AIST-583 | AIST TR-13:2021 | §5.8.3, los atiesadores de apoyo que el 08 · E5 dejó para este eslabón | PDF ídem, p. 33 | «Bearing stiffeners shall be used where required to transmit end reactions» |
| AIST-589 | AIST TR-13:2021 | §5.8.9, que no haya accesorios ni dispositivos fuera de los indicados en los planos | PDF ídem, p. 34 | «There shall be no attachments or fixtures of any kind, other than those designated on the design drawings» |
| AIST-c59 | AIST TR-13:2021 | Comm 5.9, los tres métodos de estabilidad que Ref. 1 admite | PDF ídem, p. 54 | «Ref. 1 permits three methods for stability analysis/design» |
| AIST-c59b | AIST TR-13:2021 | Comm 5.9, **que las costaneras y los elementos secundarios no cuentan como arriostramiento**, que es el supuesto S6 | PDF ídem, p. 54 | «Secondary members such as girts, walkways, stairs, etc., may not provide adequate restraint» |
| AIST-c591 | AIST TR-13:2021 | Comm 5.9.1, que con placa de alma continua se puede usar la inercia de la sección completa en el análisis del marco — es el permiso que D6 no toma | PDF ídem, p. 54 | «the moment of inertia of the complete solid section may be used in the frame analysis» |
| AIST-c591b | AIST TR-13:2021 | Comm 5.9.1, la definición de los tres parámetros $a_r$, $B$ y $P_1/P_2$ — **mirada en PNG**, no extraída | PDF ídem, p. 55 | «The equivalent length factor will be evaluated in terms of three parameters» |
| AIST-c591c | AIST TR-13:2021 | Comm 5.9.1, que las tablas se aplican estrictamente a la unión por placa de alma longitudinal continua | PDF ídem, p. 55 | «They are strictly applicable to columns for which the crane column segment is connected to the building column by a continuous longitudinal web plate» |
| AIST-c591d | AIST TR-13:2021 | Comm 5.9.1, la Ec. 5.9.1 que pasa de $K_L$ a $K_U$ — **mirada en PNG**; la cita es la prosa que la sigue | PDF ídem, p. 55 | «The equivalent length factors are applied to the total column length L to determine the equivalent length of each segment» |
| AIST-c591e | AIST TR-13:2021 | Comm 5.9.1, **cuál tabla corresponde a cada condición de borde**, que es lo que fija la Comm Tabla 2 | PDF ídem, p. 55 | «Comm Table 1 assumes a hinge at the base, C, and Comm Tables 2 through 4 assume the base fully fixed» |
| AIST-c591f | AIST TR-13:2021 | Comm 5.9.1, **que las costaneras no dan soporte longitudinal y que $P_c$ probablemente lo fije el eje débil**, que es el hallazgo de D5 | PDF ídem, p. 55 | «Exterior wall girts are not assumed to provide longitudinal support in mill buildings» |
| AIST-c591g | AIST TR-13:2021 | Comm 5.9.1, el $K$ de 0,8 para el eje débil con base empotrada que `## Límites` no toma | PDF ídem, p. 55 | «If the base at C can be considered fully fixed by the footing for bending about the (y-y) axis, then K should be taken as 0.8» |
| AIST-t2 | AIST TR-13:2021 | Comm Tabla 2, $K_L$ del segmento inferior con nudo restringido al giro y libre de desplazarse y base empotrada — **mirada en PNG**, no extraída | PDF ídem, p. 62 | «Column ABC Rotation Restrained but Permitted to Sway at Top A and Fixed at Base C» |
| AIST-c592 | AIST TR-13:2021 | Comm 5.9.2, **de dónde sale el tope de 50 kips**, que es lo que A3 recoge | PDF ídem, p. 72 | «to limit the effects of bracket rotation on the performance of the crane runway and to address observed fatigue issues at the base of the bracket support» |
| AIST-c592b | AIST TR-13:2021 | Comm 5.9.2, las concentraciones de tensión por la carga excéntrica que `## Límites` declara | PDF ídem, p. 72 | «stress concentrations due to the offset loading must be accounted for in the design of the bracket and column assembly» |
| AIST-fig | AIST TR-13:2021 | Fig. Comm 5.9.1, la nomenclatura de la columna escalonada y el eje $x$-$x$ de la sección compuesta — **mirada en PNG** | PDF ídem, p. 72 | «Nomenclature for stepped columns as used in Comm Tables 1 through 4» |
| AISC-C1 | ANSI/AISC 360-22 | §C1, los requisitos generales de estabilidad a los que §5.9.4 remite | `Normas/A360-22W-ewr.pdf`, p. 94 | «Stability shall be provided for the structure as a whole and for each of its elements» |
| AISC-C22 | ANSI/AISC 360-22 | §C2.2, las imperfecciones iniciales por modelado directo o por cargas nocionales | PDF ídem, p. 96 | «by direct modeling of these imperfections in the analysis as specified in Section C2.2a or by the application of notional loads» |
| AISC-C22b | ANSI/AISC 360-22 | §C2.2b, la carga nocional de 0,002 y el umbral de 1,7 que D2 y D3 usan | PDF ídem, p. 97 | «Notional loads shall be applied as lateral loads at all levels» |
| AISC-A8 | ANSI/AISC 360-22 | Ap. §8.1, la amplificación de dos análisis de primer orden que D3 corre | PDF ídem, p. 351 | «Second-order effects in structures may be approximated by amplifying the required strengths determined by two first-order elastic analyses» |
| AISC-A8b | ANSI/AISC 360-22 | Ap. §8.1, el $B_2$ de piso que D3 arma con el coeficiente de estabilidad del 07 | PDF ídem, p. 351 | «multiplier to account for P-∆ effects, determined for each story of the structure» |
| AISC-J10 | ANSI/AISC 360-22 | §J10.2, la fluencia local del alma que F2 usa para justificar los atiesadores | PDF ídem, p. 219 | «This section applies to single-concentrated forces and both components of double-concentrated forces» |
| AISC-J10b | ANSI/AISC 360-22 | §J10.2 (b) y la Ec. J10-3, la rama del extremo con el $2{,}5k$ que F2 aplica | PDF ídem, p. 219 | «applied at a distance from the member end that is less than or equal to the full nominal depth of the member» |
| AISC-w | ANSI/AISC 360-22 | §C2.3, la rigidez reducida a $0{,}80\tau_b EI$ del análisis directo que D2 evalúa | `referencias/AISC360-22/capC-estabilidad.md` | |
| AISC-w2 | ANSI/AISC 360-22 | §E3 y §E1, el pandeo por flexión con que E1 y E3 miden los dos fustes | `referencias/AISC360-22/capE-compresion.md` | |
| AISC-w3 | ANSI/AISC 360-22 | §H1.1 y la Ec. H1-1b, la interacción con que E2 cierra el fuste inferior | `referencias/AISC360-22/capH-fuerzas-combinadas.md` | |
| AISC-w4 | ANSI/AISC 360-22 | §B4 y §F, las propiedades de sección y el momento de fluencia de B3 y E2 | `referencias/AISC360-22/capB-requisitos-de-diseno.md` | |
| AISC-w5 | ANSI/AISC 360-22 | §J2.4, §J3.5, §J3.6, §J3.8 y §J10.8, los filetes, la separación de pernos, el deslizamiento crítico y el atiesador de apoyo | `referencias/AISC360-22/capJ-conexiones.md` | |
| AISC341-w | ANSI/AISC 341-22 | §E3.5a, las columnas de un marco de momento especial como miembros altamente dúctiles, que D0 aplica al fuste de grúa | `referencias/AISC341-22/capE3-marcos-momento-especiales.md` | |
| NCh-w | NCh2369:2025 (3.ª ed.) | §5.4 y Ecs. (1a), (1b) y (3); §5.13 y la Ec. (13); §6.1, §6.3 y §6.4, que D6 recorre | `referencias/NCh2369-2025/cap05-analisis-sismico.md` | |
| NCh-w2 | NCh2369:2025 (3.ª ed.) | Tabla 9 y §8.4.1, el $\lambda_{md}$ del ala y del alma y el amplificador de capacidad | `referencias/NCh2369-2025/cap08-estructuras-de-acero.md` | |
| N3171-w | NCh3171:2017 | §9.1.1 (2), la combinación con que se mayoran la reacción y el empuje de la grúa | `referencias/NCh3171-2017/cap09-combinaciones-de-carga.md` | |
