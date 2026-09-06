# 11 · El arriostramiento continuo de techo

El 01 leyó §12.1.2 como una obligación sin forma: «arriostramiento continuo en el techo», y nada
más. Acá esa palabra adquiere geometría. El tope de esbeltez de §8.8.4 resulta ser la transición
inelástica de AISC escrita en forma cerrada, y con él la diagonal que cruza el agua entera **no
existe en tubo**: el techo se subdivide porque la cláusula no admite otra cosa. Después, las
cuatro demandas que el mismo sistema sirve —y la que gobierna no es la sísmica—. Fuerzas en kN,
longitudes en mm salvo donde se indique.

## El caso

{{ figura('nch2369-galpon-grua/11', 'planta', 'Planta desarrollada del arriostramiento de techo, con las dos aguas abatidas sobre el papel: los cuatro vanos de 7 500 mm entre los cinco marcos, las siete líneas de puntal separadas 4 249,18 mm sobre los 12 747,55 mm de rafter, las X de los 24 paneles con su diagonal de 8 620,07 mm, y en trazos la diagonal del agua entera de 14 790,20 mm, que pediría un radio de giro de 130,35494 y no existe en tubo') }}

| Dato | Valor |
|---|---|
| Elemento | sistema arriostrado horizontal de cubierta, obligatorio por §12.1.2 (del 01 · D2) |
| Luz transversal | {{ v('nch2369-galpon-grua/11', 'L_luz', 2) }} m; media agua {{ v('nch2369-galpon-grua/11', 'L_r', 5) }} m sobre el rafter (del 01, A4) |
| Separación de marcos | {{ v('nch2369-galpon-grua/11', 's_marco', 2) }} m, **{{ v('nch2369-galpon-grua/11', 'n_vanos', 0) }} vanos** y {{ v('nch2369-galpon-grua/11', 'n_marcos_liga', 0) }} marcos (del 01 · S1) |
| Pendiente de cubierta | 1 en {{ v('nch2369-galpon-grua/11', 'S_pend', 2) }}, $\theta = {{ vt('nch2369-galpon-grua/11', 'theta_techo', 5) }}$° (del 02 · C1 y C2) |
| Vanos con arriostramiento vertical | **{{ v('nch2369-galpon-grua/11', 'n_vanos_arr', 0) }}** de {{ v('nch2369-galpon-grua/11', 'n_vanos', 0) }}; los otros dos con portón (del 01 · S2) |
| Traza adoptada | {{ v('nch2369-galpon-grua/11', 'n_pan_agua', 0) }} espacios de {{ v('nch2369-galpon-grua/11', 'b_pan_techo', 2) }} mm por agua, X en los cuatro vanos (C3, C4) |
| Diagonal adoptada | tubo cuadrado {{ v('nch2369-galpon-grua/11', 'B_diag', 0) }} × {{ v('nch2369-galpon-grua/11', 'B_diag', 0) }} × {{ v('nch2369-galpon-grua/11', 't_diag', 0) }}, $A = {{ vt('nch2369-galpon-grua/11', 'A_diag_techo', 0) }}$ mm² (E1) |
| Puntal adoptado | tubo cuadrado {{ v('nch2369-galpon-grua/11', 'B_punt', 0) }} × {{ v('nch2369-galpon-grua/11', 'B_punt', 0) }} × {{ v('nch2369-galpon-grua/11', 't_punt', 0) }}, $A = {{ vt('nch2369-galpon-grua/11', 'A_punt_techo', 0) }}$ mm² (E2) |
| Acero | A572 Gr. 50 en plancha y A500 Gr. C en tubo: $F_y = {{ vt('nch2369-galpon-grua/11', 'Fy', 0) }}$ MPa, $R_y = {{ vt('nch2369-galpon-grua/11', 'Ry', 2) }}$ (S1) |
| Factores | $\phi_c = {{ vt('nch2369-galpon-grua/11', 'phi_c', 2) }}$; el $\phi$ de rigidez del Ap. 6 vale {{ v('nch2369-galpon-grua/11', 'phi_br', 2) }} |
| Lo que se decide aquí | la traza, las dos secciones, y si el sistema sirve las cuatro demandas |

Los supuestos, en una línea cada uno. **S1**, el acero es el del 07 · S5, y que $F_y$ coincida
entre plancha y tubo es lo que hace que un solo tope de esbeltez sirva para todo el sistema.
**S2**, las secciones tubulares se idealizan con **esquinas vivas**, y el ancho plano de la
Tabla 9 se toma en $b = B - 3t$. **S3**, la X va en los 24 paneles con **una de las dos
diagonales continua** en el cruce, que es la condición literal de §8.8.3. **S4**, el corte del
diafragma se reparte entre los seis paneles de un vano **en paralelo**, con puntales y rafters
axialmente rígidos. **S5**, la fuerza sísmica del diafragma se toma como $C_{dis}$ por el peso
del edificio **sin la grúa**. **S6**, el arriostramiento del rafter se resuelve por la vía
**lateral** de §8.7.7 —la que el 07 · E6 publicó— y no por la torsional que la misma cláusula
también admite.

## A · La cláusula que obliga, el tope que subdivide y la que prohíbe

### A1 · «Continuo» tiene contenido geométrico

$$L_{tot} = {{ vt('nch2369-galpon-grua/11', 'L_total', 5) }}\ \text{m} \qquad n_m = {{ vt('nch2369-galpon-grua/11', 'n_marcos_liga', 5) }} \qquad {{ vt('nch2369-galpon-grua/11', 'frac_vanos_arr', 5) }}$$

→ C12.1.2 dice para qué está el sistema: **distribuir cargas laterales concentradas, como las de
grúas, entre varios marcos**. Con sólo la mitad de los vanos arriostrados verticalmente, un
diafragma que se corte en un vano no puede llevar nada de un marco al siguiente. **«Continuo»
significa X en los cuatro vanos**, y eso el 01 no podía verlo porque no tenía la traza.

### A2 · El tope de §8.8.4 es la transición inelástica de AISC, escrita exacta

$$\lambda_{glob} = 1{,}5\,\pi\sqrt{E/F_y} = {{ vt('nch2369-galpon-grua/11', 'lam_glob', 5) }} \qquad 4{,}71\sqrt{E/F_y} = {{ vt('nch2369-galpon-grua/11', 'lam_aisc', 5) }} \qquad {{ vt('nch2369-galpon-grua/11', 'difieren', 5) }}$$

$$F_e = {{ vt('nch2369-galpon-grua/11', 'Fe_tope', 5) }}\ \text{MPa} \qquad F_y/F_e = {{ vt('nch2369-galpon-grua/11', 'razon_tope', 5) }} \qquad F_{cr}^{\min} = {{ vt('nch2369-galpon-grua/11', 'Fcr_min', 5) }}\ \text{MPa} \qquad {{ vt('nch2369-galpon-grua/11', 'frac_fluencia', 5) }}$$

→ los dos números difieren en {{ v('nch2369-galpon-grua/11', 'difieren', 5) }} porque el $4{,}71$
de AISC §E3 **es** $1{,}5\pi$ redondeado a tres cifras. La condición de §8.8.4 equivale
exactamente a $F_y/F_e \le 2{,}25$: lo que la cláusula prohíbe, sin decirlo, es que una diagonal
o un puntal horizontal **pandee elásticamente**. Y en el propio tope la tensión crítica no baja
de {{ v('nch2369-galpon-grua/11', 'frac_fluencia', 5) }} de la fluencia. No es un tope de
esbeltez elegido: es el borde de una fórmula de otra norma.

### A3 · §8.8.2 prohíbe el solo-tracción, y el piso del precio es 2,56

$$F_y/F_{cr}^{\min} = {{ vt('nch2369-galpon-grua/11', 'rinde_menos', 5) }}$$

→ un elemento que sólo trabaja en tracción no tiene tope obligatorio de esbeltez, y la
recomendación de AISC §D1 —$L/r \le 300$— es **más laxa que el tope que §8.8.4 le impone al mismo
elemento** por hacerlo resistir compresión. Y aun **en** ese tope la sección comprimida rinde
$1/{{ vt('nch2369-galpon-grua/11', 'rinde_menos', 5) }}$ de lo que rendiría traccionada. Los dos
factores se multiplican, y ése es el precio de la prohibición.

### A4 · La diagonal que cruza el agua entera no existe

$$f = {{ vt('nch2369-galpon-grua/11', 'f_cumb', 5) }}\ \text{m} \qquad L_r = {{ vt('nch2369-galpon-grua/11', 'L_r', 5) }}\ \text{m} \qquad L_d^{agua} = {{ vt('nch2369-galpon-grua/11', 'Ld_agua', 2) }}\ \text{mm} \qquad {{ vt('nch2369-galpon-grua/11', 'subestima', 5) }}$$

$$r \ge L_d^{agua}/\lambda_{glob} = {{ vt('nch2369-galpon-grua/11', 'r_agua', 5) }}\ \text{mm}$$

→ tomar la proyección horizontal en vez de la longitud sobre el rafter **subestima la diagonal en
{{ v('nch2369-galpon-grua/11', 'subestima', 5) }}**, y el tope pediría un radio de giro de
{{ v('nch2369-galpon-grua/11', 'r_agua', 5) }} mm: un tubo de más de 300 mm de lado. No existe en
catálogo para esta función. **El techo se subdivide porque la cláusula no admite otra cosa**, y
no por preferencia de traza.

## B · La exención, y a cuál de las dos exigencias alcanza

### B1 y B2 · El texto no lo dice y el Comentario sí

$$\lambda_{md} = 0{,}76\sqrt{E/(R_yF_y)} = {{ vt('nch2369-galpon-grua/11', 'lam_md_tubo', 5) }} \qquad {{ vt('nch2369-galpon-grua/11', 'uso_t9_125', 5) }} \qquad {{ vt('nch2369-galpon-grua/11', 'uso_t9_200', 5) }}$$

→ §8.8.4 pone **dos** exigencias —las razones ancho/espesor de la Tabla 9 y la esbeltez global— y
una sola exención. El texto no dice a cuál alcanza; **C8.8.4 sí**, y nombra la «esbeltez local».
La global no se exime. Con las paredes que la Tabla 9 pediría, los dos tubos pasan
—{{ v('nch2369-galpon-grua/11', 'uso_t9_125', 5) }} y
{{ v('nch2369-galpon-grua/11', 'uso_t9_200', 5) }}— y el sistema pesaría
{{ v('nch2369-galpon-grua/11', 'pesa_sin_exencion', 5) }} veces lo que pesa. Ése es el valor de
la exención, en acero.

### B3 · Contra qué mecanismo se toma

$$k_{cap,X} = {{ vt('nch2369-galpon-grua/11', 'kcap_X', 5) }} \qquad {{ vt('nch2369-galpon-grua/11', 'demanda_mas', 5) }} \qquad {{ vt('nch2369-galpon-grua/11', 'fusibles', 5) }}$$

→ la exención se paga con la demanda amplificada por $0{,}7R_1$, que es
{{ v('nch2369-galpon-grua/11', 'demanda_mas', 5) }} veces más. Se toma porque el arriostramiento
de techo **no es fusible de ninguna de las dos direcciones** —el mecanismo vive en los marcos y
en los planos verticales, no acá— y porque §8.8.5 obliga a conectarlo por capacidad esperada de
todos modos. El conteo de fusibles en el plano del techo da
{{ v('nch2369-galpon-grua/11', 'fusibles', 5) }}.

## C · La traza que el tope admite

{{ figura('nch2369-galpon-grua/11', 'panel', 'El panel arriostrado y las dos longitudes de pandeo a la misma escala: la diagonal de 8 620,07 mm sobre un vano de 7 500 y un panel de 4 249,18, el punto de cruce de la cláusula 8.8.3 con una diagonal continua, y las barras de 4 310,04 mm contra 7 500, con las esbelteces de 87,90206 y 94,65151 y los radios de giro de 37,98693 y 66,10201 que el tope de 113,46099 pide') }}

### C1 · El barrido, y por qué manda el vano y no la media luz

$$\text{dos paneles}: {{ vt('nch2369-galpon-grua/11', 'Ld_2', 2) }}\ \text{mm} \qquad \text{cuatro}: {{ vt('nch2369-galpon-grua/11', 'Ld_4', 2) }}\ \text{mm} \qquad r_1 = {{ vt('nch2369-galpon-grua/11', 'r_1', 5) }} \qquad r_2 = {{ vt('nch2369-galpon-grua/11', 'r_2', 5) }}\ \text{mm}$$

→ el radio pedido baja con la subdivisión, pero **tiene un piso**: con infinitos paneles la
diagonal tiende al vano de {{ v('nch2369-galpon-grua/11', 'vano_mm', 0) }} mm y el tope sigue
pidiendo esa cifra. De tres a cuatro paneles se gana poco y se pagan ocho diagonales más. **Lo
que manda la traza es el vano, no la media luz.**

### C2 · §8.8.3 vale exactamente 2 en la diagonal y cero en el puntal

$$KL = {{ vt('nch2369-galpon-grua/11', 'KL_diag', 2) }}\ \text{mm} \qquad {{ vt('nch2369-galpon-grua/11', 'vale_cruce', 5) }}$$

→ el punto de cruce se puede tomar fijo **en la dirección perpendicular al plano de las
diagonales** cuando una de las dos es continua y la otra está traccionada. Vale exactamente 2 en
la diagonal, y **cero en el puntal**, que no tiene cruce: por eso el puntal termina siendo el
miembro grueso del sistema pese a llevar la séptima parte de fuerza.

### C3 y C4 · La traza adoptada ya estaba fijada por otra cláusula, y el despiece

$$b_p = {{ vt('nch2369-galpon-grua/11', 'b_pan_techo', 2) }}\ \text{mm} \qquad {{ vt('nch2369-galpon-grua/11', 'uso_sep_rafter', 5) }} \qquad L_d = {{ vt('nch2369-galpon-grua/11', 'L_diag_techo', 2) }}\ \text{mm} \qquad r \ge {{ vt('nch2369-galpon-grua/11', 'r_req', 5) }}\ \text{mm}$$

$$n_{lin} = {{ vt('nch2369-galpon-grua/11', 'n_lin', 5) }} \qquad n_{pan} = {{ vt('nch2369-galpon-grua/11', 'n_pan', 5) }} \qquad n_{diag} = {{ vt('nch2369-galpon-grua/11', 'n_diag', 5) }} \qquad L_{diag} = {{ vt('nch2369-galpon-grua/11', 'L_diag_tot', 5) }}\ \text{m}$$

→ los {{ v('nch2369-galpon-grua/11', 'b_pan_techo', 2) }} mm del panel usan
{{ v('nch2369-galpon-grua/11', 'uso_sep_rafter', 5) }} de la separación máxima que §8.7.7 le pone
al arriostramiento lateral del rafter: **la traza ya estaba fijada por otra cláusula**, y los
puntos donde el techo se arriostra son exactamente los que el 07 · E6 necesitaba. Salen
{{ v('nch2369-galpon-grua/11', 'n_lin', 0) }} líneas de puntal,
{{ v('nch2369-galpon-grua/11', 'n_pan', 0) }} paneles y
{{ v('nch2369-galpon-grua/11', 'n_diag', 0) }} diagonales: casi el doble de metros de diagonal
que de puntal, y aun así en E4 los dos pesan casi lo mismo, porque a la diagonal la subdivide el
cruce y al puntal no.

## D · Las cuatro demandas que el mismo sistema sirve

{{ figura('nch2369-galpon-grua/11', 'demandas', 'Las cuatro demandas de fuerza sobre la diagonal del vano extremo, a la misma escala: los 47,33782 kN del diafragma sísmico longitudinal, los 161,02133 del arriostramiento del rafter en un punto, los 2,51638 del fuste superior de 3 815,76 mm y los 347,00299 de la acumulación del Apéndice 6, contra los 423,43911 kN de capacidad de la diagonal') }}

### D1 · El diafragma sísmico longitudinal, y el colector que el alero tiene que ser

$$F_{diaf} = C_{dis}\,W = {{ vt('nch2369-galpon-grua/11', 'F_diaf_sin', 5) }}\ \text{kN} \qquad \times\,k_{cap,X} = {{ vt('nch2369-galpon-grua/11', 'F_diaf_X', 5) }}\ \text{kN}$$

$$V_z = {{ vt('nch2369-galpon-grua/11', 'V_z', 5) }}\ \text{kN} \qquad \cos\alpha = {{ vt('nch2369-galpon-grua/11', 'cos_diag', 5) }} \qquad N_{diag} = {{ vt('nch2369-galpon-grua/11', 'N_diag_sismo', 5) }}\ \text{kN} \qquad F_{col} = {{ vt('nch2369-galpon-grua/11', 'F_col_alero', 5) }}\ \text{kN}$$

→ el plano del techo recoge la inercia longitudinal y la lleva a los dos planos de alero.
{{ v('nch2369-galpon-grua/11', 'V_z', 2) }} kN cruzan la banda de alero de cada agua en cada
vano, y en la diagonal son {{ v('nch2369-galpon-grua/11', 'N_diag_sismo', 5) }} kN. El puntal de
alero, en cambio, es un **colector**: recoge la mitad de la fuerza de un agua y la arrastra hasta
el vano arriostrado, {{ v('nch2369-galpon-grua/11', 'F_col_alero', 5) }} kN. Es la primera vez en
la serie que un elemento se dimensiona por recoger y no por resistir.

#### Y esto es lo que el modelo hace con el mismo empuje

<rukan-visor src="../../../modelos/galpon-grua/galpon-grua.escena.json" caso="E_X" esfuerzo="N" filtro="PUN1_0,PUN2_0,PUN3_0,PUN4_0" vista="planta"></rukan-visor>

El caso `E_X` del modelo es un empuje longitudinal de **5 000 kN** repartido como la masa —no la
demanda de diseño, sino la unidad de empuje con que la serie mide—. La vista es la planta del
techo con sus {{ v('nch2369-galpon-grua/11', 'n_pan', 0) }} paneles en X, y el diagrama se dibuja
sobre **la línea de puntales del alero A**: los cuatro tramos que el colector de D1 recorre. El
resto del techo se pinta con la rampa y queda casi incoloro, que es la primera cosa que hay que
leer —la rampa la normaliza el máximo del **modelo entero**, y el máximo lo pone una X de muro,
no el techo—.

| Magnitud | Del modelo, con 5 000 kN | Cuánto es del empuje |
|---|---:|---:|
| Diagonal `DTA1_0`, vano 1 | {{ r('galpon-grua', 'N_dta1', 2) }} kN | 1 en {{ cociente('galpon-grua', 5000, 'N_dta1', 2) }} |
| Diagonal `DTA2_0`, vano 2 | {{ r('galpon-grua', 'N_dta2', 2) }} kN | 1 en {{ cociente('galpon-grua', 5000, 'N_dta2', 2) }} |
| Puntal de alero, vano 1 | {{ r('galpon-grua', 'N_pun1', 2) }} kN | 1 en {{ cociente('galpon-grua', 5000, 'N_pun1', 2) }} |
| Puntal de alero, vano 2 | {{ r('galpon-grua', 'N_pun2', 2) }} kN | 1 en {{ cociente('galpon-grua', 5000, 'N_pun2', 2) }} |
| Puntal de alero, vano 3 | {{ r('galpon-grua', 'N_pun3', 2) }} kN | — |
| Puntal de alero, vano 4 | {{ r('galpon-grua', 'N_pun4', 2) }} kN | — |

Tres cosas, y las tres son contraste y no verificación. **Primera**: el arrastre del puntal de
alero **existe y tiene la forma que D1 describe** —crece del extremo hacia el centro y cambia de
signo en el marco central, que es exactamente lo que hace un colector—. Los vanos 3 y 4 son la
imagen especular de los vanos 2 y 1 con el signo cambiado, y el modelo lo reproduce a la última
cifra sin que nadie se lo haya pedido. **Segunda**: la magnitud es bastante menor que la que D1
asigna. El memo hace pasar por el plano del techo **todo** $C_{dis}W$ (su S5), y el modelo pone
la masa donde está: la mitad inferior de columnas y muros descarga directo a la fundación sin
tocar el diafragma. El propio `## Límites` del memo lo declara conservador, y acá se ve cuánto.
**Tercera**: D1 reparte el corte entre los seis paneles de un vano en paralelo (S4), y el modelo
lo reparte según la rigidez real de una retícula con cordones flexibles, así que las dos
diagonales sondeadas no llevan lo mismo.

Nada de esto cambia una sección, porque lo que dimensiona la diagonal no es esta demanda sino la
del D6.

### D2 · El reparto del empuje de grúa, que cierra la banda que el 07 dejó abierta

$$k_{pan} = \frac{2EA\,b_p^{2}}{L_d^{3}} = {{ vt('nch2369-galpon-grua/11', 'k_pan', 5) }}\ \text{N}/\text{mm} \qquad \cos^{2}\theta = {{ vt('nch2369-galpon-grua/11', 'cos2_pend', 5) }} \qquad k_d = {{ vt('nch2369-galpon-grua/11', 'kd_vano', 5) }}\ \text{kN}/\text{m}$$

$$\rho = {{ vt('nch2369-galpon-grua/11', 'rho_diaf', 5) }} \qquad f = \frac{1 + 3\rho + \rho^{2}}{1 + 5\rho + 5\rho^{2}} = {{ vt('nch2369-galpon-grua/11', 'f_marco_grua', 5) }}$$

$$\chi^{2} = {{ vt('nch2369-galpon-grua/11', 'chi2', 5) }} \qquad d_{riel} = {{ vt('nch2369-galpon-grua/11', 'd_riel_real', 5) }}\ \text{mm} \qquad {{ vt('nch2369-galpon-grua/11', 'uso_grua_real', 5) }}$$

→ el 07 · C3 acotó lo que el arriostramiento redistribuye entre dos cotas y dijo que dónde cae lo
decide la rigidez de este sistema. Ya se puede decir: el diafragma es
{{ v('nch2369-galpon-grua/11', 'rho_diaf', 5) }} veces más rígido que el marco, y el marco
cargado retiene {{ v('nch2369-galpon-grua/11', 'f_marco_grua', 5) }} del empuje. La deriva del
riel cae en {{ v('nch2369-galpon-grua/11', 'uso_grua_real', 5) }} de su límite de servicio,
apenas {{ v('nch2369-galpon-grua/11', 'sobre_cota_baja', 5) }} veces la cota baja que el 07 dejó
abierta. **La banda se cierra prácticamente en su extremo favorable.**

### D3 · Y acá entra `k_esc`, la primera vez que la serie lo consume

$$\rho' = {{ vt('nch2369-galpon-grua/11', 'rho_esc', 5) }} \qquad f' = {{ vt('nch2369-galpon-grua/11', 'f_esc', 5) }} \qquad {{ vt('nch2369-galpon-grua/11', 'baja_cuota', 5) }}$$

→ con la columna escalonada adentro el marco es más rígido, el diafragma pesa relativamente menos
y el marco cargado **retiene más**: la cuota que el arriostramiento redistribuye baja
{{ v('nch2369-galpon-grua/11', 'baja_cuota', 5) }}. Es el {{ v('nch2369-galpon-grua/11', 'k_esc', 5) }}
que el 10 publicó justamente para esto, y mueve el reparto un dos por ciento.

### D4 y D5 · El rafter y el fuste superior, con resistencia y con rigidez

$$P_{br} = \frac{0{,}06\,R_yF_yZ_x}{h_o} = {{ vt('nch2369-galpon-grua/11', 'Pbr_raf', 5) }}\ \text{kN} \qquad \beta_{br} = \frac{10\,M_{pe}}{\phi L_b h_o} = {{ vt('nch2369-galpon-grua/11', 'beta_raf', 5) }}\ \text{N}/\text{mm}$$

$$k_{nudo} = \frac{4EA\,L^{2}}{L_d^{3}} = {{ vt('nch2369-galpon-grua/11', 'k_nudo', 5) }}\ \text{N}/\text{mm} \qquad {{ vt('nch2369-galpon-grua/11', 'factor_rig_raf', 5) }}$$

$$P_r = {{ vt('nch2369-galpon-grua/11', 'P_r_col', 5) }}\ \text{kN} \qquad L_{br} = {{ vt('nch2369-galpon-grua/11', 'L_br_col', 2) }}\ \text{mm} \qquad P_{br}^{col} = {{ vt('nch2369-galpon-grua/11', 'Pbr_col', 5) }}\ \text{kN} \qquad {{ vt('nch2369-galpon-grua/11', 'pide_col', 5) }}$$

→ el arriostramiento del rafter pide {{ v('nch2369-galpon-grua/11', 'Pbr_raf', 5) }} kN de
resistencia en cada punto y {{ v('nch2369-galpon-grua/11', 'beta_raf', 5) }} N/mm de rigidez, y el
nudo entrega {{ v('nch2369-galpon-grua/11', 'factor_rig_raf', 5) }} veces esa rigidez: **la
rigidez no es el problema; la resistencia sí**. El fuste superior que el 10 apoyó acá pide
{{ v('nch2369-galpon-grua/11', 'pide_col', 5) }} de lo que pide el rafter, y se sostiene con
holgura: el supuesto del 10 queda verificado.

### D6 · La acumulación, que es lo que de verdad dimensiona la diagonal

$$P_{acum} = 2P_{br} + 0{,}5\,P_{br} = {{ vt('nch2369-galpon-grua/11', 'Pbr_acum', 5) }}\ \text{kN} \qquad 1{,}5\,P_{acum} = {{ vt('nch2369-galpon-grua/11', 'P_vano_extremo', 5) }}\ \text{kN}$$

$$N_{diag} = {{ vt('nch2369-galpon-grua/11', 'N_diag_acum', 5) }}\ \text{kN} \qquad \Sigma\,\text{Ap. 6.1} = {{ vt('nch2369-galpon-grua/11', 'suma_ap61', 5) }}\ \text{kN} \qquad {{ vt('nch2369-galpon-grua/11', 'veces_Q0', 5) }}$$

→ el Ap. §6.1 de AISC manda que la resistencia del arriostramiento se base en la **suma** de las
resistencias requeridas de todos los miembros que estabiliza. Con eso la diagonal recibe
{{ v('nch2369-galpon-grua/11', 'N_diag_acum', 5) }} kN, **{{ v('nch2369-galpon-grua/11', 'supera_sismica', 5) }}
veces** la demanda sísmica. Y la suma sobre los cinco marcos y las dos aguas entrega
{{ v('nch2369-galpon-grua/11', 'suma_ap61', 5) }} kN al sistema longitudinal,
{{ v('nch2369-galpon-grua/11', 'veces_Q0', 5) }} veces el corte basal de diseño. Ese número es
inaplicable, y `## Límites` dice por qué y a quién le queda.

## E · Las dos secciones, sus conexiones y lo que pesan

### E1 y E2 · La diagonal que la acumulación dimensiona, y el puntal que dimensiona la esbeltez

$$A = {{ vt('nch2369-galpon-grua/11', 'A_diag_techo', 5) }}\ \text{mm}^2 \qquad r = {{ vt('nch2369-galpon-grua/11', 'r_diag', 5) }}\ \text{mm} \qquad {{ vt('nch2369-galpon-grua/11', 'esb_diag', 5) }} \qquad {{ vt('nch2369-galpon-grua/11', 'uso_esb_diag', 5) }}$$

$$F_{cr} = {{ vt('nch2369-galpon-grua/11', 'Fcr_diag', 5) }}\ \text{MPa} \qquad \phi P_n = {{ vt('nch2369-galpon-grua/11', 'phiPn_diag', 5) }}\ \text{kN} \qquad {{ vt('nch2369-galpon-grua/11', 'uso_ax_diag', 5) }} \qquad {{ vt('nch2369-galpon-grua/11', 'uso_ax_diag_4', 5) }}$$

$$A = {{ vt('nch2369-galpon-grua/11', 'A_punt_techo', 5) }}\ \text{mm}^2 \qquad {{ vt('nch2369-galpon-grua/11', 'esb_punt', 5) }} \qquad {{ vt('nch2369-galpon-grua/11', 'uso_esb_punt', 5) }} \qquad \phi P_n = {{ vt('nch2369-galpon-grua/11', 'phiPn_punt', 5) }}\ \text{kN} \qquad {{ vt('nch2369-galpon-grua/11', 'uso_ax_punt', 5) }}$$

→ **las dos secciones las dimensionan criterios distintos.** La diagonal, un tubo de
{{ v('nch2369-galpon-grua/11', 'B_diag', 0) }} × {{ v('nch2369-galpon-grua/11', 'B_diag', 0) }} ×
{{ v('nch2369-galpon-grua/11', 't_diag', 0) }} con
$A = {{ vt('nch2369-galpon-grua/11', 'A_diag_techo', 0) }}$ mm², la usa el axial acumulado en
{{ v('nch2369-galpon-grua/11', 'uso_ax_diag', 5) }} y la esbeltez en
{{ v('nch2369-galpon-grua/11', 'uso_esb_diag', 5) }}; bajar la pared a 4 mm la deja en
{{ v('nch2369-galpon-grua/11', 'uso_ax_diag_4', 5) }} y no pasa. El puntal, con
$A = {{ vt('nch2369-galpon-grua/11', 'A_punt_techo', 0) }}$ mm², lo usa la **esbeltez** en
{{ v('nch2369-galpon-grua/11', 'uso_esb_punt', 5) }} y el axial en apenas
{{ v('nch2369-galpon-grua/11', 'uso_ax_punt', 5) }}: un tubo de 150 falla el tope en
{{ v('nch2369-galpon-grua/11', 'uso_esb_150', 5) }} **sin que ninguna resistencia lo explique**.

### E3 y E4 · Las conexiones, el tope que las salva, y lo que pesa

$$T_{ye} = {{ vt('nch2369-galpon-grua/11', 'Tye_diag', 5) }}\ \text{kN} \qquad m_d = {{ vt('nch2369-galpon-grua/11', 'm_diag', 5) }}\ \text{kg}/\text{m} \qquad m_p = {{ vt('nch2369-galpon-grua/11', 'm_punt', 5) }}\ \text{kg}/\text{m}$$

$$W_{arr} = {{ vt('nch2369-galpon-grua/11', 'W_arr', 2) }}\ \text{kg} \qquad g_{arr} = {{ vt('nch2369-galpon-grua/11', 'g_arr', 5) }}\ \text{kg}/\text{m}^2 \qquad {{ vt('nch2369-galpon-grua/11', 'uso_presup_techo', 5) }} \qquad {{ vt('nch2369-galpon-grua/11', 'sobre_presup', 5) }}$$

→ §8.8.5 obliga a conectar por la capacidad esperada **en tracción y en compresión**, y la
tracción esperada de la diagonal vale {{ v('nch2369-galpon-grua/11', 'Tye_diag', 5) }} kN. El
segundo miembro de la misma frase —«la máxima carga que el sistema puede transferir»— la divide
por el factor que D6 dejó. Y el peso: el arriostramiento de techo se lleva
{{ v('nch2369-galpon-grua/11', 'uso_presup_techo', 5) }} del presupuesto que el 01 declaró para
la cubierta, **antes de contar una sola costanera**, y con él adentro el acero de un marco llega
a {{ v('nch2369-galpon-grua/11', 'sobre_presup', 5) }} veces lo que el 05 asignó.

## Veredicto

**El tope de esbeltez de §8.8.4 no es un número elegido: es el borde de la fórmula de compresión
de AISC escrito en forma cerrada.** Vale {{ v('nch2369-galpon-grua/11', 'lam_glob', 5) }} y
difiere del $4{,}71\sqrt{E/F_y}$ de AISC §E3 en
{{ v('nch2369-galpon-grua/11', 'difieren', 5) }}, porque $4{,}71$ es $1{,}5\pi$ redondeado. Lo
que prohíbe, sin decirlo, es que una diagonal o un puntal horizontal pandee elásticamente.

Con ese tope la diagonal del agua entera no existe, y la traza adoptada son tres espacios de
{{ v('nch2369-galpon-grua/11', 'b_pan_techo', 2) }} mm por agua —exactamente los puntos donde el
07 · E6 arriostró el rafter— con diagonales de
{{ v('nch2369-galpon-grua/11', 'L_diag_techo', 2) }} mm y **X en los cuatro vanos**, que es la
palabra «continuo» de §12.1.2.

**La exención por $0{,}7R_1$ alcanza sólo a la Tabla 9, y lo decide el Comentario y no el texto.**
Las dos secciones las dimensionan criterios distintos: la diagonal
—$A = {{ vt('nch2369-galpon-grua/11', 'A_diag_techo', 0) }}$ mm²— la gobierna la acumulación del
Apéndice 6, y el puntal —$A = {{ vt('nch2369-galpon-grua/11', 'A_punt_techo', 0) }}$ mm²— la
gobierna la esbeltez sola. El diafragma resulta con
{{ v('nch2369-galpon-grua/11', 'kd_vano', 5) }} kN/m de rigidez de corte por vano, el marco
cargado retiene {{ v('nch2369-galpon-grua/11', 'f_marco_grua', 5) }} del empuje de grúa, y la
banda que el 07 dejó abierta se cierra en su extremo favorable.

Y queda un número que este eslabón no puede cerrar: la regla de suma del Ap. §6.1 entrega
{{ v('nch2369-galpon-grua/11', 'Pbr_acum', 5) }} kN por marco y agua, y
{{ v('nch2369-galpon-grua/11', 'veces_Q0', 5) }} veces el corte basal al sistema longitudinal. Es
lo que el 13 recibiría si el arriostramiento del rafter se resuelve por la vía lateral.

## Límites

- **Dieciséis de las 118 filas del `## Resumen` del memo no reproducen**, y son la misma especie
  que las del 07, el 08 y el 10 —el memo imprime un dígito que su propia aritmética sobre las
  cifras impresas no da— pero acá son muchas más, y hay una causa: **el arnés del memo 11 compara
  los bloques D y E con 10⁻⁴ absoluto**, así que su quinto decimal nunca se verificó. Las dos
  mayores son el espesor que la Tabla 9 pediría —$200/(17{,}44708+3)$ da 9,78135 y el memo
  publica 9,78229, que corresponde a un $\lambda_{md}$ de 17,44506 y no al que el mismo renglón
  imprime— y la capacidad esperada en compresión de la diagonal, 489,09470 contra los 489,08276
  publicados. Ninguna de las dieciséis cambia una sección, una traza ni una conclusión, y la
  única que se propaga —la razón entre las dos rigideces del 07— se consume con la cifra impresa,
  como manda la regla. Están enumeradas en el encabezado de `_calculo.py`.
- **La acumulación del Ap. §6.1 no tiene regla en NCh y el número que sale es inaplicable** (S6).
  §8.7.7 fija la resistencia de un arriostramiento lateral y no dice qué pasa cuando un mismo
  sistema arriostra cinco marcos; el Ap. §6.1 manda sumar y sólo deja la salida de «unless
  analysis indicates that smaller values are justified». La salida física existe y es la del
  primer guión de §8.7.7: un arriostramiento **torsional** —el par costanera más tirante del
  07 · S8— cierra el par dentro del marco y el diafragma no lo ve. Este eslabón no la calcula
  porque el 07 publicó la vía lateral; el 13 recibe el problema con su número.
- **La rigidez que el nudo entrega es una cota superior.** Los
  {{ v('nch2369-galpon-grua/11', 'k_nudo', 5) }} N/mm de D4 suponen fijos los extremos de las
  cuatro diagonales que concurren al nudo, y no lo están. El arnés del memo resuelve la retícula
  completa y obtiene un tercio de esa cifra: el margen real sobre lo que el rafter pide es tres
  veces menor que el que D4 escribe.
- **La retícula del techo no se resuelve dentro del memo** (S4), y **el modelo del sitio sí la
  tiene**. Por eso el contraste de D1 no es una verificación: el memo reparte el corte entre seis
  paneles en paralelo con cordones rígidos, y el modelo lo reparte según rigidez. Las dos cosas
  responden preguntas distintas y las dos están declaradas.
- **La flexibilidad cruzada del marco se despeja de un resultado del 07, no se calcula.** El
  $\chi^{2} = {{ vt('nch2369-galpon-grua/11', 'chi2', 5) }}$ sale de exigir que la expresión de D2
  reproduzca la deriva que el 07 · C3 obtuvo con diafragma rígido, así que hereda entera la
  incertidumbre de aquel modelo declarado.
- **La demanda sísmica del diafragma se estima con el peso del edificio sin la grúa** (S5), y el
  caso `E_X` del modelo muestra que hacer pasar todo ese peso por el plano del techo es
  conservador. Queda fuera, en cambio, la inercia longitudinal de la grúa, que §12.1.3 y AIST
  §3.11.2 tratan aparte.
- **El caso `E_X` es un empuje declarado, no un análisis sísmico.** Se reparte como la masa
  porque el esquema `rukan/proyecto@1` no tiene todavía análisis espectral por dirección, y las
  cifras que sirve son fracciones del empuje —invariantes de escala—, nunca demandas de diseño.
- **Las secciones tubulares se idealizan con esquinas vivas** (S2): la esbeltez queda del lado
  seguro y el peso del lado inseguro, y un catálogo real hay que consultarlo.
- **La componente de gravedad en el plano del faldón no se calcula.** Un techo al 20 % descarga el
  $\sin\theta$ de su peso y de su nieve **dentro** del plano del arriostramiento, y la práctica
  corriente lo resuelve con tensores de costanera que este eslabón no diseña.
- **§8.8 no tiene el §8.6.7 del sistema vertical.** El puntal horizontal aparece en §8.8.4 y en
  §8.8.5 y **nunca recibe una regla de resistencia**. Aplicar §8.6.7 por analogía sí cambiaría la
  sección. Se declara y no se aplica.
- **Las conexiones no se diseñan como piezas**, y C8.6.4 advierte que una plancha de cruce
  demasiado esbelta invalida el propio §8.8.3 del que C2 depende.
- **El peso propio sigue sin propagarse hacia atrás**, y ahora el marco pasa el presupuesto:
  rehacer el 05 y el 06 con el despiece real lo piden ya tres eslabones —el 08, el 10 y éste— y
  ninguno tiene lote asignado.
- **No se verifica el estado de servicio del propio diafragma.** Ninguna cláusula de NCh2369 le
  pone un límite de deformación en su plano.

## Ficha

{{ ficha('nch2369-galpon-grua/11') }}

## Referencias

| Clave | Norma y edición | Cláusula | Leída en | Cita textual |
|---|---|---|---|---|
| NCh-p1 | NCh2369:2025 (3.ª ed.) | §8.8.1, la función del sistema arriostrado horizontal que A1 recoge | `Normas/NCh 2369 - 3°Edición 2025.05.28.pdf`, p. 102 | «cuya función es transferir cargas sísmicas y/o proveer redundancia estructural» |
| NCh-p2 | NCh2369:2025 (3.ª ed.) | §8.8.2, **la prohibición del solo-tracción** que A3 aplica | PDF ídem, p. 102 | «No se permiten sistemas de arriostramiento de piso o cubierta con elementos que solo resisten tracción» |
| NCh-p2b | NCh2369:2025 (3.ª ed.) | §8.8.2, la excepción que el 01 cerró con §12.2.1 e) | PDF ídem, p. 102 | «excepto en los casos de galpones livianos de acero que se rigen por las disposiciones de 12.2» |
| NCh-p3 | NCh2369:2025 (3.ª ed.) | §8.8.3, **el punto de cruce y en qué dirección se puede tomar fijo**, que es lo que C2 mide | PDF ídem, p. 102 | «Dicho punto se puede considerar fijo en la dirección perpendicular al plano de las diagonales» |
| NCh-p3b | NCh2369:2025 (3.ª ed.) | §8.8.3, la condición de continuidad de una de las dos diagonales, que es el supuesto S3 | PDF ídem, p. 102 | «cuando la otra esté traccionada y una de las diagonales sea continua en el cruce» |
| NCh-p4 | NCh2369:2025 (3.ª ed.) | §8.8.4, la primera exigencia= las razones ancho/espesor de la Tabla 9 | PDF ídem, p. 103 | «Las diagonales y puntales de sistemas de arriostramiento de piso o de cubierta deben tener razones ancho/espesor» |
| NCh-p4b | NCh2369:2025 (3.ª ed.) | §8.8.4, **la segunda exigencia**, que es la que A2 identifica con la transición de AISC | PDF ídem, p. 103 | «La esbeltez global de estos elementos debe ser menor que» |
| NCh-p4c | NCh2369:2025 (3.ª ed.) | §8.8.4, la exención y su segunda puerta, que §8.6.3 no tiene | PDF ídem, p. 103 | «Se pueden exceptuar de esta exigencia aquellos elementos cuya resistencia requerida sea determinada» |
| NCh-p4d | NCh2369:2025 (3.ª ed.) | C8.8.4, **a cuál de las dos exigencias alcanza la exención**, que es lo que B1 resuelve | PDF ídem, p. 103 | «no es necesario cumplir con los requisitos de esbeltez local indicados en Tabla 9» |
| NCh-p4e | NCh2369:2025 (3.ª ed.) | C8.8.4, el mecanismo que la Tabla 9 protege= pandeo local y fatiga de bajo ciclaje | PDF ídem, p. 103 | «los ciclos de pandeo de las diagonales no generen fatiga de bajo ciclaje» |
| NCh-p5 | NCh2369:2025 (3.ª ed.) | §8.8.5, la conexión por capacidad esperada en tracción y en compresión que E3 usa | PDF ídem, p. 103 | «se deben diseñar para resistir tanto la capacidad esperada en tracción como la capacidad esperada en compresión del elemento» |
| NCh-p5b | NCh2369:2025 (3.ª ed.) | §8.8.5, el tope que divide la demanda de conexión por 2,62 | PDF ídem, p. 103 | «o que la máxima carga que el sistema puede transferir a la conexión» |
| NCh-p6 | NCh2369:2025 (3.ª ed.) | §8.6.3, la cláusula gemela del plano vertical, con la misma esbeltez global y una exención más corta | PDF ídem, p. 94 | «Las diagonales sismorresistentes de planos verticales que trabajen en compresión» |
| NCh-p7 | NCh2369:2025 (3.ª ed.) | C8.6.4, **la advertencia que C8.8.3 hereda**, y que este sistema no dispara y el del 13 sí | PDF ídem, p. 95 | «la disposición no es directamente aplicable y se debe considerar una longitud de pandeo mayor» |
| NCh-p7b | NCh2369:2025 (3.ª ed.) | C8.6.4, la plancha de cruce esbelta que invalidaría el propio §8.8.3 | PDF ídem, p. 95 | «se recomienda atiesar la conexión del cruce para mejorar este comportamiento» |
| NCh-p8 | NCh2369:2025 (3.ª ed.) | §8.6.7, **la regla de resistencia del puntal que §8.8 no tiene**, y que E2 declara | PDF ídem, p. 96 | «Las vigas o puntales horizontales que unen los extremos de las diagonales se deben diseñar» |
| NCh-p9 | NCh2369:2025 (3.ª ed.) | §8.7.7, la separación máxima del arriostramiento lateral del rafter, que C3 usa | PDF ídem, p. 102 | «Los arriostramientos deben estar separados a una distancia no mayor a» |
| NCh-p9b | NCh2369:2025 (3.ª ed.) | §8.7.7, la resistencia requerida que D4 reobtiene | PDF ídem, p. 102 | «La resistencia requerida de los arriostramientos laterales debe ser de» |
| NCh-p9c | NCh2369:2025 (3.ª ed.) | §8.7.7, la rigidez requerida, que remite al Anexo 6 de NCh427/1 — o sea al Apéndice 6 de AISC 360 | PDF ídem, p. 102 | «La rigidez requerida de los arriostramientos laterales debe cumplir los requisitos de NCh427/1» |
| NCh-p9d | NCh2369:2025 (3.ª ed.) | §8.7.7, **la alternativa torsional** del primer guión, que `## Límites` reserva para el 13 | PDF ídem, p. 102 | «ambas alas se deben arriostrar lateralmente o la sección transversal debe ser arriostrada torsionalmente» |
| NCh-p10 | NCh2369:2025 (3.ª ed.) | Tabla 9, la fila de paredes de tubo conformado en frío usado como arriostramiento, con su $0{,}76\sqrt{E/(R_yF_y)}$ — **mirada en PNG**, no extraída | PDF ídem, p. 105 | «Paredes de perfiles rectangulares conformados en frío (HSS) o plegados en frío usados como arriostramientos» |
| NCh-p11 | NCh2369:2025 (3.ª ed.) | §12.1.2, el arriostramiento continuo de techo obligatorio, que el 01 · D2 dejó sin geometría | PDF ídem, p. 150 | «Los edificios con marcos transversales deben tener un sistema de arriostramiento continuo en el techo» |
| NCh-p12 | NCh2369:2025 (3.ª ed.) | C12.1.2, **la función que A1 convierte en una exigencia geométrica** | PDF ídem, p. 150 | «distribuir cargas laterales concentradas, como las de grúas, entre varios marcos» |
| NCh-p13 | NCh2369:2025 (3.ª ed.) | §12.2.1 e), la letra que el 01 midió en 2,00000 y que arrastró la excepción de §8.8.2 | PDF ídem, p. 151 | «Los puentes grúas deben tener una capacidad nominal menor o igual a 100 kN, en el caso de grúas sin cabina de operación» |
| AISC-1 | ANSI/AISC 360-22 | Ap. §6.1, **la regla de suma sobre los miembros arriostrados**, que es lo que D6 aplica | `Normas/A360-22W-ewr.pdf`, p. 339 | «the strength and stiffness of the bracing shall be based on the sum of the required strengths of all members being braced» |
| AISC-1b | ANSI/AISC 360-22 | Ap. §6.1, la única salida que la regla deja, y que `## Límites` recoge | PDF ídem, p. 339 | «unless analysis indicates that smaller values are justified» |
| AISC-2 | ANSI/AISC 360-22 | Ap. §6.2.2, el arriostramiento puntual de columna con que D5 verifica el supuesto del 10 | PDF ídem, p. 341 | «In the direction perpendicular to the longitudinal axis of the column, the required strength of end and intermediate point braces is» |
| AISC-2b | ANSI/AISC 360-22 | Ap. §6.2.2, que $L_{br}$ no necesita tomarse menor que el largo efectivo máximo admisible | PDF ídem, p. 341 | «need not be taken as less than the maximum effective length» |
| AISC-3 | ANSI/AISC 360-22 | Ap. §6.3.1b, el arriostramiento puntual de viga y la nota del $L_b$ máximo que D4 usa | PDF ídem, p. 343 | «For intermediate point bracing of an individual beam» |
| AISC-4 | ANSI/AISC 360-22 | Comm 6.1, **que la costanera con tirante es un arriostramiento torsional y no lateral**, que es la salida que `## Límites` deja al 13 | PDF ídem, p. 702 | «restrains twist (not lateral displacement) of the beams at that particular location» |
| AISC-4b | ANSI/AISC 360-22 | Comm 6.1, que la rigidez pedida es el doble de la ideal, que es de dónde sale el 8 y el 10 de las ecuaciones | PDF ídem, p. 702 | «Lateral bracing systems for columns and beams require at least twice the ideal stiffness» |
| AIST-1 | AIST TR-13:2021 | §5.3, el reparto del empuje transversal entre columnas según rigidez relativa, que D2 y D3 resuelven | `Normas/aist-tr-no13-2021-3.pdf`, p. 29 | «shall be distributed between crane runway support columns based upon an overall analysis of the system, accounting for relative stiffness» |
| AIST-2 | AIST TR-13:2021 | Comm 5.9, **que los elementos secundarios no cuentan como arriostramiento**, que es lo que D5 verifica | PDF ídem, p. 54 | «Secondary members such as girts, walkways, stairs, etc., may not provide adequate restraint» |
| AIST-3 | AIST TR-13:2021 | Comm 5.9.1, que el eje débil del fuste es el que gobierna, y por eso su arriostramiento importa | PDF ídem, p. 55 | «Exterior wall girts are not assumed to provide longitudinal support in mill buildings» |
| NCh431-1 | NCh431:2010 | §8.2, la razón horizontal de pendiente con que A4 arma el agua — **PDF escaneado, leído a ojo** | `Normas/nch-431-2010.pdf`, p. 16 | «Para el resto de los techos triangulares, la carga sin balancear debe ser considerada 0,3 x ps en la zona de barlovento» |
| AISC360-w | ANSI/AISC 360-22 | §E3 y §E1, el pandeo por flexión y la frontera $F_y/F_e = 2{,}25$ que A2 identifica | `referencias/AISC360-22/capE-compresion.md` | |
| AISC360-w2 | ANSI/AISC 360-22 | §D1, la esbeltez recomendada de un elemento traccionado que A3 usa de contraste | `referencias/AISC360-22/capD-traccion.md` | |
| AISC360-w3 | ANSI/AISC 360-22 | §B4 y §B4.1b (d), las propiedades de sección y el ancho plano de una pared de tubo | `referencias/AISC360-22/capB-requisitos-de-diseno.md` | |
| AISC341-w | ANSI/AISC 341-22 | §F2, los marcos arriostrados concéntricos especiales, de donde viene la lógica de fusible que B3 aplica | `referencias/AISC341-22/capF-marcos-arriostrados-concentricos.md` | |
| AISC341-w2 | ANSI/AISC 341-22 | §D1.2a, la resistencia requerida del arriostramiento lateral que el 07 · E6 usó de contraste | `referencias/AISC341-22/capD-miembros-y-conexiones.md` | |
| NCh-w | NCh2369:2025 (3.ª ed.) | §8.3.1 y §8.4.1, la capacidad esperada y el amplificador de capacidad que B3 y E3 usan | `referencias/NCh2369-2025/cap08-estructuras-de-acero.md` | |
| NCh-w2 | NCh2369:2025 (3.ª ed.) | §5.1.2, §5.13 y §6.1, el peso sísmico, el corte de diseño y el desplazamiento que D1, D2 y E4 consumen | `referencias/NCh2369-2025/cap05-analisis-sismico.md` | |
