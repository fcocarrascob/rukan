# 13 · Las diagonales longitudinales y el anclaje

El tubo que doce eslabones vinieron arrastrando como «parámetro ilustrativo» no pasa ninguno
de los dos límites de §8.6.3, y el anclaje dúctil del que cuelga el `R = 5` de toda la serie
se dimensiona aquí, trece eslabones después de haberlo usado. Este eslabón cierra los tres
encargos que el 11 y el 12 le dejaron, dimensiona la X del panel longitudinal y fija el
momento con que se diseña la base. Fuerzas en kN, longitudes en mm.

## El caso

| Dato | Valor |
|---|---|
| Sistema | Panel arriostrado en X, en los **dos vanos extremos** de los cuatro (del 01 · S2) |
| Líneas resistentes | 2 muros longitudinales, 2 paneles cada uno (del 12 · C4) |
| Geometría del panel | base {{ v('nch2369-galpon-grua/13', 's_marco', 2) }} m × alto {{ v('nch2369-galpon-grua/13', 'h_libre', 2) }} m |
| Diagonal | {{ v('nch2369-galpon-grua/13', 'L_diag', 2) }} mm, a {{ v('nch2369-galpon-grua/13', 'ang_diag', 3) }}° de la horizontal |
| Sección heredada | cajón {{ v('nch2369-galpon-grua/13', 'B_ilus', 0) }} × {{ v('nch2369-galpon-grua/13', 'B_ilus', 0) }} × {{ v('nch2369-galpon-grua/13', 't_ilus', 0) }}, `A` = {{ v('nch2369-galpon-grua/13', 'A_ilus', 0) }} mm² (S1) |
| Acero | $F_y = {{ vt('nch2369-galpon-grua/13', 'Fy', 0) }}$ MPa, $R_y = {{ vt('nch2369-galpon-grua/13', 'Ry', 2) }}$ (S2) |
| Base de columna | **empotrada** (del 01 · S3), lo que activa el último párrafo de §8.5.2 |
| Lo que se decide aquí | la sección de la diagonal, y el momento con que se diseña el anclaje |

Los supuestos, en una línea cada uno. **S1**, la sección heredada es la que `case11_data.py`
declara *«parámetro ilustrativo, es del 13»*: el 12 la adoptó por copia de la diagonal de
techo del 11 para poder calcular una rigidez, y nunca fue dimensionada. **S2**, el acero es
A572 Gr. 50 del catálogo de la serie y **no se leyó de NCh427/1**, que no está en la
biblioteca: el `F_y` y el `R_y` entran como dato del caso y no como cita normativa. **S3**,
la sección adoptada es un **cajón soldado cuadrado**, así que la fila de Tabla 9 que le
aplica es la de *paredes de perfiles rectangulares soldados*; si fuera un HSS conformado en
frío la fila es otra y **el límite es el mismo**, de modo que la elección no cambia el
veredicto. **S4**, se toma `K = 1` y la longitud de pandeo la mitad de la diagonal, que es lo
que §8.6.4 permite y que C1 discute. **S5**, la demanda de la diagonal sale del reparto
elástico del corte del diafragma entre los cuatro paneles, sin considerar que la comprimida
pandee: si pandeara, la traccionada toma el doble y C3 mide cuánto margen hay.

## A · La sección heredada, contra los dos límites de §8.6.3

### A1 · Los dos límites de la misma frase no usan el mismo denominador

§8.6.3 pide dos cosas a la vez, y sus expresiones se parecen lo suficiente como para
confundirlas: la razón ancho/espesor contra el `λ_md` de la Tabla 9, y la esbeltez global.

$$\lambda_{md} = {{ vt('nch2369-galpon-grua/13', 'c_lam_md', 2) }}\sqrt{\frac{E}{R_y F_y}} = {{ vt('nch2369-galpon-grua/13', 'c_lam_md', 2) }}\sqrt{\frac{ {{ vt('nch2369-galpon-grua/13', 'E_ac', 0) }} }{ {{ vt('nch2369-galpon-grua/13', 'Ry', 2) }} \cdot {{ vt('nch2369-galpon-grua/13', 'Fy', 0) }} }} = {{ vt('nch2369-galpon-grua/13', 'lam_md', 5) }}$$

$$\lambda_{glob} = {{ vt('nch2369-galpon-grua/13', 'c_esbeltez', 2) }}\,\pi\sqrt{\frac{E}{F_y}} = {{ vt('nch2369-galpon-grua/13', 'esb_lim', 5) }}$$

→ **El primero lleva `R_y` en el denominador y el segundo no.** Es la fluencia *esperada*
contra la nominal, y la diferencia no es cosmética: omitir el `R_y` daría
{{ v('nch2369-galpon-grua/13', 'lam_md', 5) }} → 18,29, un límite **4,8 % más permisivo**, y
ninguna verificación posterior lo delataría. El segundo reproduce exactamente el
$\lambda_{glob}$ que el [11](../11-arriostramiento-continuo-de-techo/) publicó, por un camino
independiente: la diferencia es {{ v('nch2369-galpon-grua/13', 'dif_lam', 0) }}.

### A2 · La pared del tubo se pasa un 43 %

$$\frac{b}{t} = \frac{ {{ vt('nch2369-galpon-grua/13', 'B_ilus', 0) }} }{ {{ vt('nch2369-galpon-grua/13', 't_ilus', 0) }} } = {{ vt('nch2369-galpon-grua/13', 'bt_ilus', 1) }} \qquad \frac{b/t}{\lambda_{md}} = {{ vt('nch2369-galpon-grua/13', 'uso_bt_ilus', 5) }}$$

→ **{{ v('nch2369-galpon-grua/13', 'uso_bt_ilus', 4) }} veces el límite.** Medido con el ancho
plano en vez del exterior da 23,000, que tampoco pasa: el veredicto no depende de qué
convención se use para `b`. Lo que §8.6.3 compra con este límite lo dice su comentario — que
las diagonales *«no pueden presentar pandeo local previo a una incursión inelástica
moderada»*, porque los ciclos de pandeo generan fatiga de bajo ciclaje.

### A3 · Y la esbeltez se pasa aunque se le regale el punto de cruce

$$\frac{0{,}5\,L}{r} = \frac{0{,}5 \cdot {{ vt('nch2369-galpon-grua/13', 'L_diag', 2) }} }{ {{ vt('nch2369-galpon-grua/13', 'r_ilus', 5) }} } = {{ vt('nch2369-galpon-grua/13', 'esb_ilus', 5) }} \qquad \frac{ \lambda }{ \lambda_{glob} } = {{ vt('nch2369-galpon-grua/13', 'uso_esb_ilus', 5) }}$$

→ **{{ v('nch2369-galpon-grua/13', 'esb_ilus', 2) }} contra
{{ v('nch2369-galpon-grua/13', 'esb_lim', 2) }}**, y eso ya tomando la mitad de la longitud
que §8.6.4 permite cuando el cruce está conectado. Con la diagonal entera da
{{ v('nch2369-galpon-grua/13', 'esb_ilus_ent', 2) }}, un factor 2,3 sobre el límite.

**Y hay un problema anterior a la aritmética.** §8.6.4 sólo permite tomar el punto de cruce
como fijo *«cuando la otra esté traccionada y una de las diagonales sea continua en el
cruce»*. En el modelo del sitio las dos ramas se montan como bielas completas que **se cruzan
sin nudo**, así que hoy el modelo no materializa la condición que su propio cálculo invoca.
`## Límites` lo anota.

## B · La sección que sí pasa, y lo que cuesta

### B1 · El ancho/espesor manda sobre el espesor, no sobre el lado

$$\frac{b}{t} = \frac{ {{ vt('nch2369-galpon-grua/13', 'B_pan', 0) }} }{ {{ vt('nch2369-galpon-grua/13', 't_pan', 0) }} } = {{ vt('nch2369-galpon-grua/13', 'bt_pan', 5) }} \qquad \frac{b/t}{\lambda_{md}} = {{ vt('nch2369-galpon-grua/13', 'uso_bt', 5) }}$$

→ Se adopta un cajón soldado **{{ v('nch2369-galpon-grua/13', 'B_pan', 0) }} ×
{{ v('nch2369-galpon-grua/13', 'B_pan', 0) }} ×
{{ v('nch2369-galpon-grua/13', 't_pan', 0) }}**, con
`A` = {{ v('nch2369-galpon-grua/13', 'A_pan', 0) }} mm². Subir el lado sin subir el espesor
**empeora** el ancho/espesor mientras mejora la esbeltez: los dos límites tiran en sentidos
opuestos y por eso la solución es engrosar, no sólo agrandar.

### B2 · La esbeltez queda con margen, y el radio de giro dice cuánto

$$\lambda = \frac{0{,}5\,L}{r} = \frac{0{,}5 \cdot {{ vt('nch2369-galpon-grua/13', 'L_diag', 2) }} }{ {{ vt('nch2369-galpon-grua/13', 'r_pan', 5) }} } = {{ vt('nch2369-galpon-grua/13', 'esb_pan', 5) }} \qquad r_{req} = \frac{0{,}5\,L}{\lambda_{glob}} = {{ vt('nch2369-galpon-grua/13', 'r_req', 5) }}\ \text{mm}$$

→ Uso {{ v('nch2369-galpon-grua/13', 'uso_esb', 5) }}. El radio de giro requerido es
{{ v('nch2369-galpon-grua/13', 'r_req', 2) }} mm y la sección da
{{ v('nch2369-galpon-grua/13', 'r_pan', 2) }}.

### B3 · La capacidad, que ninguna demanda de este eslabón alcanza a usar

$$F_e = \frac{\pi^2 E}{\lambda^2} = {{ vt('nch2369-galpon-grua/13', 'Fe_pan', 5) }}\ \text{MPa} \qquad F_{cr} = 0{,}658^{F_y/F_e} F_y = {{ vt('nch2369-galpon-grua/13', 'Fcr_pan', 5) }}\ \text{MPa}$$

$$\phi P_n = {{ vt('nch2369-galpon-grua/13', 'phi_c', 2) }} \cdot F_{cr} \cdot A = {{ vt('nch2369-galpon-grua/13', 'phiPn_pan', 5) }}\ \text{kN} \qquad \phi T_n = {{ vt('nch2369-galpon-grua/13', 'phiTn_pan', 5) }}\ \text{kN}$$

→ **{{ v('nch2369-galpon-grua/13', 'phiPn_pan', 2) }} kN en compresión.**

### B4 · El precio: el área se multiplica por 3,26

$$\frac{A_{pan}}{A_{ilus}} = \frac{ {{ vt('nch2369-galpon-grua/13', 'A_pan', 0) }} }{ {{ vt('nch2369-galpon-grua/13', 'A_ilus', 0) }} } = {{ vt('nch2369-galpon-grua/13', 'crece_area', 5) }}$$

→ **{{ v('nch2369-galpon-grua/13', 'crece_area', 2) }} veces.** No es un ajuste de detalle: es
la diferencia entre una sección que se eligió para poder seguir calculando y una que cumple.

## C · §8.6.2 y el reparto del corte

### C1 · El corte de la línea, y un contraste que cierra en cero

El diafragma entrega {{ v('nch2369-galpon-grua/13', 'F_diaf_X', 5) }} kN en X, que se reparten
entre los dos muros y, dentro de cada muro, entre sus dos paneles.

$$V_{linea} = \frac{ {{ vt('nch2369-galpon-grua/13', 'F_diaf_X', 5) }} }{ {{ vt('nch2369-galpon-grua/13', 'n_lineas', 0) }} } = {{ vt('nch2369-galpon-grua/13', 'V_linea', 5) }}\ \text{kN} \qquad V_{panel} = {{ vt('nch2369-galpon-grua/13', 'V_panel', 5) }}\ \text{kN}$$

→ El corte por panel coincide con el `F_col_alero` que el 11 publicó por otro camino: la
diferencia es {{ v('nch2369-galpon-grua/13', 'dif_col', 0) }} kN. Es el mismo número visto
como colector allá y como corte de panel acá.

### C2 · La fuerza en la diagonal

$$N_{diag} = \frac{0{,}5\,V_{panel}}{\cos\theta} = \frac{0{,}5 \cdot {{ vt('nch2369-galpon-grua/13', 'V_panel', 5) }} }{ {{ vt('nch2369-galpon-grua/13', 'cos_diag', 5) }} } = {{ vt('nch2369-galpon-grua/13', 'N_diag', 5) }}\ \text{kN}$$

→ **{{ v('nch2369-galpon-grua/13', 'N_diag', 2) }} kN**, con uso
{{ v('nch2369-galpon-grua/13', 'uso_diag_comp', 5) }} en compresión y
{{ v('nch2369-galpon-grua/13', 'uso_diag_trac', 5) }} en tracción. La sección no la gobierna la
resistencia: la gobiernan los dos límites de §8.6.3.

### C3 · El 30 % de §8.6.2 lo cumple la geometría, no el dimensionamiento

§8.6.2 pide que las **diagonales traccionadas** aporten al menos el 30 % del corte de la
línea, para cada sentido. En una X simétrica con las dos ramas activas, la traccionada toma la
mitad.

$$\frac{ {{ vt('nch2369-galpon-grua/13', 'frac_traccion', 2) }} }{ {{ vt('nch2369-galpon-grua/13', 'frac_trac', 2) }} } = {{ vt('nch2369-galpon-grua/13', 'uso_862', 5) }} \qquad V_{trac,min} = {{ vt('nch2369-galpon-grua/13', 'V_trac_min', 5) }}\ \text{kN}$$

→ **Uso {{ v('nch2369-galpon-grua/13', 'uso_862', 2) }}**: la X cumple con holgura y lo hace
por ser X, no por la sección. El requisito muerde en otras configuraciones — una diagonal
única por panel deja el 100 % del corte en una sola rama y, si esa rama está comprimida, el
aporte traccionado es cero. Es la misma familia que §8.6.1, que **prohíbe** los sistemas de
sólo tracción: su comentario dice que el objetivo es *«generar redundancia en el sistema»*.

## D · La rigidez, que era el encargo del 12

### D1 · La cota inferior que el 12 dejó puesta

El 12 despejó una rigidez **mínima** de panel: por debajo de ella la irregularidad torsional
se pasa del umbral de 1,20.

$$k_{pan} = \frac{2EA\,b^2}{L^3} = {{ vt('nch2369-galpon-grua/13', 'k_pan', 5) }}\ \text{kN/m} \qquad \frac{k_{pan}}{k_{br,lim}} = {{ vt('nch2369-galpon-grua/13', 'uso_kbr_13', 5) }}$$

→ La sección adoptada da **{{ v('nch2369-galpon-grua/13', 'uso_kbr_13', 2) }} veces** la cota
inferior de {{ v('nch2369-galpon-grua/13', 'kbr_lim', 5) }} kN/m. Con la ilustrativa el 12
medía 2,40075, así que el encargo estaba cumplido antes y lo sigue estando: **la cota de
rigidez nunca fue la que gobernaba**. Lo que gobierna es el pandeo local.

### D2 · Y aquí la serie deja de ser una cadena

$$\frac{k_{pan}}{k_{pan,ilus}} = {{ vt('nch2369-galpon-grua/13', 'crece_k', 5) }}$$

→ La rigidez del panel se multiplica por {{ v('nch2369-galpon-grua/13', 'crece_k', 2) }}, y
**esa rigidez es una entrada del 12**: de ella cuelgan `rho_pan`, la razón torsional
{{ v('nch2369-galpon-grua/13', 'raz_tors_Y', 5) }}, el factor de diafragma y el colector
{{ v('nch2369-galpon-grua/13', 'F_col_12', 5) }} kN. El 13 realimenta al 12. Es la primera vez
en la serie que un eslabón le devuelve algo a otro anterior, y `## Límites` dice qué se hizo
con eso.

## E · Los dos encargos que quedaban

### E1 · El colector del 12 pasa por la diagonal nueva

$$\frac{F_{col,12}}{\phi T_n} = \frac{ {{ vt('nch2369-galpon-grua/13', 'F_col_12', 5) }} }{ {{ vt('nch2369-galpon-grua/13', 'phiTn_pan', 5) }} } = {{ vt('nch2369-galpon-grua/13', 'uso_col_pan', 5) }}$$

→ Uso {{ v('nch2369-galpon-grua/13', 'uso_col_pan', 5) }}. El colector con la torsión adentro
no dimensiona nada.

### E2 · La acumulación del Apéndice 6, que el 11 declaró inaplicable

$$N_{acum} = \frac{P_{br,acum}}{\cos\theta} = {{ vt('nch2369-galpon-grua/13', 'N_acum_diag', 5) }}\ \text{kN} \qquad \frac{N_{acum}}{\phi P_n} = {{ vt('nch2369-galpon-grua/13', 'uso_acum', 5) }}$$

→ **Uso {{ v('nch2369-galpon-grua/13', 'uso_acum', 2) }}, y es la demanda que más se acerca a
la capacidad** — {{ v('nch2369-galpon-grua/13', 'veces_sismo', 2) }} veces el corte sísmico del
panel. El 11 la declaró inaplicable porque §8.7.7 no dice qué pasa cuando un mismo sistema
arriostra cinco marcos, y la salida física que dejó anotada es el arriostramiento **torsional**
del par costanera-tirante. Este eslabón **no la resuelve**: la mide contra la sección adoptada
para mostrar que, incluso tomada al pie de la letra, no gobierna. La cláusula sigue sin
regla.

## F · El anclaje, del que cuelga todo lo demás

### F1 · La capacidad manda sobre la demanda, por un 20 %

La fila 5.5 de la Tabla 7 da `R = 5` sólo *«con arriostramiento continuo de techo, y con
anclajes dúctiles»*. Con bases empotradas, §8.5.2 fija el momento de diseño del anclaje.

$$M_{ancl} \ge {{ vt('nch2369-galpon-grua/13', 'frac_Mpe_base', 2) }}\,M_{pe} = {{ vt('nch2369-galpon-grua/13', 'frac_Mpe_base', 2) }} \cdot {{ vt('nch2369-galpon-grua/13', 'Mpe_col', 5) }} = {{ vt('nch2369-galpon-grua/13', 'M_ancl_min', 5) }}\ \text{kN·m}$$

$$\frac{M_{ancl,min}}{M_{base,u}} = \frac{ {{ vt('nch2369-galpon-grua/13', 'M_ancl_min', 5) }} }{ {{ vt('nch2369-galpon-grua/13', 'Mbase_u', 5) }} } = {{ vt('nch2369-galpon-grua/13', 'veces_Mbase', 5) }}$$

→ **{{ v('nch2369-galpon-grua/13', 'veces_Mbase', 5) }}.** El momento con que se diseña el
anclaje es {{ v('nch2369-galpon-grua/13', 'M_ancl', 5) }} kN·m, y **no sale del análisis**:
sale de la capacidad de la columna. La demanda que el 07 midió,
{{ v('nch2369-galpon-grua/13', 'Mbase_u', 2) }} kN·m, se queda un 20 % corta. Es un requisito
de capacidad, y el análisis no lo sustituye por más fino que sea.

### F2 · Qué hace dúctil a un anclaje, y por qué es geometría

§8.5.2 no pide un acero: pide un **detalle**. Silla y vástago inspeccionable y reparable, o
—sin silla— pernos reemplazables con una longitud libre equivalente. Y dos cotas duras:

$$\ell_{exp} \ge \max\left({{ vt('nch2369-galpon-grua/13', 'long_exp_min', 0) }};\ {{ vt('nch2369-galpon-grua/13', 'n_diam_exp', 0) }}\,d\right) \qquad d_{umbral} = \frac{ {{ vt('nch2369-galpon-grua/13', 'long_exp_min', 0) }} }{ {{ vt('nch2369-galpon-grua/13', 'n_diam_exp', 0) }} } = {{ vt('nch2369-galpon-grua/13', 'd_umbral', 2) }}\ \text{mm}$$

→ Son **dos cotas y manda la mayor**: bajo un diámetro de
{{ v('nch2369-galpon-grua/13', 'd_umbral', 2) }} mm gobiernan los
{{ v('nch2369-galpon-grua/13', 'long_exp_min', 0) }} mm fijos, y por encima gobierna el
$8d$. Más el hilo bajo la tuerca, no menor que
{{ v('nch2369-galpon-grua/13', 'hilo_min', 0) }} mm, *«para permitir reapriete»*.

**Y la parte que no es del perno.** El comentario C8.5.2 exige que los pernos *«se encuentren
sujetos en ambos extremos por elementos que no plastifiquen antes que ellos»*, lo que se
traduce en que **el hormigón del pedestal y las placas de silla se diseñan para la capacidad
de fluencia esperada de los pernos**. El anclaje dúctil no se compra eligiendo un perno: se
compra diseñando lo que lo rodea por encima de él.

### F3 · El corte no lo toman los pernos

§8.5.3 exige llave de corte para *«el total del esfuerzo de corte en el apoyo»*, con el sismo
amplificado, y exime los apoyos por debajo de 75 kN en LRFD.

$$V_{base} = \frac{k_{cap}\,V_{linea}}{n_{bases}/n_{lineas}} = {{ vt('nch2369-galpon-grua/13', 'V_base_amp', 5) }}\ \text{kN} \qquad \frac{V_{base}}{ {{ vt('nch2369-galpon-grua/13', 'corte_exento', 0) }} } = {{ vt('nch2369-galpon-grua/13', 'uso_exento', 5) }}$$

→ **{{ v('nch2369-galpon-grua/13', 'uso_exento', 2) }} veces el umbral: la excepción no
aplica y la llave de corte es obligatoria.** Y §8.5.4 agrega que en su diseño *no* se puede
contar ni el mortero de nivelación ni el roce entre placa base y hormigón, aunque en una base
a momento exista una compresión que físicamente lo produciría.

## Veredicto

La sección heredada **no cumple ninguno de los dos límites de §8.6.3**: el ancho/espesor por
un {{ v('nch2369-galpon-grua/13', 'uso_bt_ilus', 4) }} y la esbeltez por un
{{ v('nch2369-galpon-grua/13', 'uso_esb_ilus', 5) }}, esta última aun regalándole el punto de
cruce. Se adopta un cajón **{{ v('nch2369-galpon-grua/13', 'B_pan', 0) }} ×
{{ v('nch2369-galpon-grua/13', 'B_pan', 0) }} ×
{{ v('nch2369-galpon-grua/13', 't_pan', 0) }}**, con el área multiplicada por
{{ v('nch2369-galpon-grua/13', 'crece_area', 2) }}.

Lo que dimensiona esa sección **no es ninguna fuerza**. La demanda sísmica de la diagonal es
{{ v('nch2369-galpon-grua/13', 'N_diag', 2) }} kN contra
{{ v('nch2369-galpon-grua/13', 'phiPn_pan', 2) }} kN de capacidad, un uso de
{{ v('nch2369-galpon-grua/13', 'uso_diag_comp', 5) }}; la cota de rigidez del 12 estaba
cumplida desde antes. Lo que manda es el **pandeo local**, y su razón está en el comentario:
que los ciclos de pandeo no produzcan fatiga de bajo ciclaje.

Y el anclaje da la vuelta a la serie entera. `R = 5` se viene usando desde el
[04](../04-espectro-y-r-por-direccion/) y la fila 5.5 lo condiciona a que los anclajes sean
dúctiles; §8.5.2 dice qué significa eso, y con bases empotradas obliga a diseñar la base para
**{{ v('nch2369-galpon-grua/13', 'M_ancl', 5) }} kN·m**, que es
{{ v('nch2369-galpon-grua/13', 'veces_Mbase', 5) }} veces el momento que el análisis entrega.
Si esa condición no se cumpliera, el galpón cae en la fila 5.6 con `R = 3` y **hay que rehacer
la serie desde el 04**.

## Límites

- **Es el único eslabón sin memo previo, así que no tiene oráculo.** Los doce anteriores se
  validan contra la cifra que el memo original imprimió; acá `publicado` va vacío. Lo que
  sostiene estas cifras es la cadena —{{ v('nch2369-galpon-grua/13', 'n_paneles', 0) }} de sus
  entradas se contrastan contra lo que otros eslabones publicaron—, la hoja de valores del
  proyecto en Struct Harness, y tres contrastes cruzados que cierran en cero: el
  $\lambda_{glob}$ del 11, el `F_col_alero` del 11 y el `k_pan` del 12.
- **El 13 realimenta al 12, y eso todavía no se aplicó.** La sección adoptada multiplica
  `k_pan` por {{ v('nch2369-galpon-grua/13', 'crece_k', 2) }}, y el 12 usa esa rigidez para su
  razón torsional y su colector. Recorrer el 12 con el valor nuevo **mejoraría** la torsión
  —más rigidez longitudinal, menos giro—, pero cambia cifras que su oráculo ata al memo
  original. Se declara como hallazgo y se aplica junto con la cascada, no por separado.
- **El modelo no conecta el cruce de las X del panel.** Las dos ramas son bielas completas que
  se cruzan sin nudo, y §8.6.4 exige conectarlas para poder tomar `L/2`. El cálculo usa `L/2`
  porque es lo que la norma permite **al detalle construido**, no lo que el modelo tiene: son
  dos cosas distintas y hoy no coinciden.
- **Ninguna cifra de este eslabón sale de una corrida.** El modelo del sitio no publica la
  axial de las barras del panel (`PXAA1` y sus siete hermanas) ni reacciones en las bases; el
  reparto de C1 es elástico y a mano. Agregar esas sondas es trabajo pendiente, y hasta
  entonces la demanda de la diagonal es una repartición, no una medición.
- **`F_y` no está leído de NCh427/1.** Esa norma no está en la biblioteca del proyecto, así que
  el acero entra por el catálogo de la serie. Lo calculado con él es prediseño en lo que toca a
  propiedades del material.
- **La excepción de §8.6.3 no se toma, y su alcance es ambiguo.** La cláusula permite eximir
  las diagonales cuya resistencia se determine con el sismo amplificado por `0,7R₁ ≥ 1,0`,
  pero escribe *«esta exigencia»* en singular después de enunciar **dos** límites, así que no
  queda claro si exime del ancho/espesor, de la esbeltez, o de ambos. Se dimensionó para
  cumplir los dos, que es la lectura conservadora; si se quisiera usar la excepción, la
  ambigüedad hay que resolverla antes, no después.
- **El anclaje no se dimensiona aquí: se fija su momento de diseño.** El número de pernos, su
  diámetro, la placa, la silla y el pedestal quedan fuera. Y §8.5.5 remite el pedestal a la
  cláusula 9, que esta serie no recorre.
- **Las dos excepciones de §8.5.3 remiten a NCh427/1**, que es un hueco del proyecto. Aunque
  el corte no las alcanza —uso {{ v('nch2369-galpon-grua/13', 'uso_exento', 2) }}—, si alguna
  vez se quisiera invocar una, no hay con qué.

## Ficha

{{ ficha('nch2369-galpon-grua/13') }}

## Referencias

> **Las páginas de esta tabla son las impresas**, no las del visor de PDF. Es el criterio
> nuevo del proyecto: la paginación de un archivo es propiedad de nuestro ejemplar y caduca
> sola; la impresa es la que el lector puede abrir en el suyo. Los eslabones 00 a 12 todavía
> citan la del visor.

| Clave | Norma y edición | Cláusula | Leída en | Cita textual |
|---|---|---|---|---|
| NCh-13a | NCh2369:2025 (3.ª ed.) | §8.6.2, el mínimo traccionado que C3 verifica | `NCh 2369 - 3°Edición 2025.05.28.pdf`, p. 87 impresa | «la resistencia proporcionada por las diagonales traccionadas, para cada sentido de la acción sísmica, debe ser como mínimo un 30% del esfuerzo de corte total en esa línea» |
| NCh-13b | NCh2369:2025 (3.ª ed.) | §8.6.3, los **dos** límites que A1 separa, y su excepción | PDF ídem, p. 87 impresa | «deben tener razones ancho/espesor, menores que el valor λmd establecido en Tabla 9. La esbeltez global de estos elementos debe ser menor que» |
| NCh-13c | NCh2369:2025 (3.ª ed.) | C8.6.3, la razón del límite de pandeo local | PDF ídem, p. 87 impresa | «Con el fin de que los ciclos de pandeo de las diagonales no generen fatiga de bajo ciclaje, se establece que estas no pueden presentar pandeo local previo a una incursión inelástica moderada» |
| NCh-13d | NCh2369:2025 (3.ª ed.) | §8.6.4, la condición que A3 no puede dar por cumplida | PDF ídem, p. 87 impresa | «cuando la otra esté traccionada y una de las diagonales sea continua en el cruce» |
| NCh-13e | NCh2369:2025 (3.ª ed.) | §8.6.1 y C8.6.1, la prohibición del sólo-tracción que C3 discute | PDF ídem, p. 87 impresa | «Esta disposición tiene como objetivo generar redundancia en el sistema» |
| NCh-13f | NCh2369:2025 (3.ª ed.) | Tabla 9, la fila de paredes de perfiles rectangulares usados como arriostramientos | PDF ídem, p. 98 impresa | «Paredes de perfiles rectangulares soldados usados como arriostramientos» |
| NCh-13g | NCh2369:2025 (3.ª ed.) | §8.5.2, las dos cotas geométricas del perno que F2 aplica | PDF ídem, p. 85 impresa | «La longitud expuesta de los pernos no debe ser inferior a 250 mm ni a ocho veces su diámetro nominal» |
| NCh-13h | NCh2369:2025 (3.ª ed.) | §8.5.2, el requisito de capacidad para bases empotradas, que es F1 | PDF ídem, p. 85 impresa | «considerando que el momento de empotramiento no sea menor que 50% de la capacidad flexural esperada de la columna» |
| NCh-13i | NCh2369:2025 (3.ª ed.) | C8.5.2, la cadena de capacidad que F2 traslada al pedestal | PDF ídem, p. 85 impresa | «tanto el hormigón de pedestales como las placas de silla y atiesadores deban diseñarse para la capacidad de fluencia esperada de los pernos» |
| NCh-13j | NCh2369:2025 (3.ª ed.) | §8.5.3, la llave de corte y su excepción de 75 kN, que F3 mide | PDF ídem, p. 85 impresa | «diseñados para transmitir el total del esfuerzo de corte en el apoyo» |
| NCh-13k | NCh2369:2025 (3.ª ed.) | §8.5.4, lo que no se puede contar en la llave de corte | PDF ídem, p. 86 impresa | «no se debe considerar la resistencia del mortero de nivelación, ni el roce entre placa base y hormigón de la fundación» |
| NCh-13l | NCh2369:2025 (3.ª ed.) | §8.6, el título de la cláusula: es un MAC | PDF ídem, p. 86 impresa | «Marcos arriostrados concéntricamente» |
| NCh-13m | NCh2369:2025 (3.ª ed.) | Tabla 7, fila 5.5, las tres condiciones de las que cuelga `R = 5` | PDF ídem, p. 61 impresa | «Edificios industriales de un piso, con o sin puente grúa, con arriostramiento continuo de techo, y con anclajes dúctiles» |
| NCh-13n | NCh2369:2025 (3.ª ed.) | §4.5.1, las combinaciones a que §8.5.2, §8.5.3 y §8.6.3 remiten | PDF ídem, p. 15 impresa | «Cuando se considere la acción sísmica se deben utilizar a lo menos las siguientes combinaciones de cargas» |
| AISC-13 | ANSI/AISC 360-22 | Cap. E3, la resistencia a compresión que B3 usa | heredada del 11 · E1 | — |
