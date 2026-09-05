# 08 · La viga carrilera

El apoyo simple no es una simplificación: es lo que AIST prescribe, en tres frases distintas. Y
la clase de edificio que fija la flecha vertical **no es** la clase de servicio de la grúa,
aunque las dos se llamen C. Acá se dimensiona la viga carrilera de un vano, se cuantifica la
torsión que el riel le mete y se miden las tres flechas de servicio. Fuerzas en kN, longitudes
en mm salvo donde se indique.

## El caso

{{ figura('nch2369-galpon-grua/08', 'seccion', 'Sección transversal de la viga carrilera soldada con el riel encima: ala superior 350 por 20, alma 650 por 8, ala inferior 250 por 14, canto total 684, centro de gravedad a 269,64968 de la fibra superior, 667 entre centroides de ala, riel de 131,76 de alto y la excentricidad máxima de 6,00 que la tolerancia de montaje admite') }}

| Dato | Valor |
|---|---|
| Elemento | viga carrilera soldada de un vano, simplemente apoyada (A1) |
| Luz de la carrilera | {{ v('nch2369-galpon-grua/08', 's_marco', 2) }} m, igual a la separación de marcos (del 01) |
| Puente grúa | birriel, {{ v('nch2369-galpon-grua/08', 'Qn_grua', 2) }} kN, 4 ruedas a {{ v('nch2369-galpon-grua/08', 'wb_ruedas', 2) }} m por testero (del 03) |
| Sección adoptada | ala superior {{ v('nch2369-galpon-grua/08', 'bfs_carril', 0) }} × {{ v('nch2369-galpon-grua/08', 'tfs_carril', 0) }}, alma {{ v('nch2369-galpon-grua/08', 'hw_carril', 0) }} × {{ v('nch2369-galpon-grua/08', 'tw_carril', 0) }}, ala inferior {{ v('nch2369-galpon-grua/08', 'bfi_carril', 0) }} × {{ v('nch2369-galpon-grua/08', 'tfi_carril', 0) }} |
| Riel | ASCE 85 lb/yd, {{ v('nch2369-galpon-grua/08', 'h_riel_perfil', 2) }} mm de alto, {{ v('nch2369-galpon-grua/08', 'm_riel', 2) }} kg/m |
| Acero | ASTM A572 Gr. 50 en plancha: $F_y = {{ vt('nch2369-galpon-grua/08', 'Fy', 0) }}$ MPa, $E = {{ vt('nch2369-galpon-grua/08', 'E_ac', 0) }}$ MPa |
| Clase de edificio de AIST | **C**, de los ciclos del 03 y la vida útil declarada (B1) |
| Factores de resistencia | $\phi_b = \phi_v = \phi_c = {{ vt('nch2369-galpon-grua/08', 'phi_b', 2) }}$ |
| Lo que se decide aquí | el apoyo, la sección, la torsión del riel y las dos flechas |

Los supuestos, en una línea cada uno. **S1**, el acero es el mismo del 07, pero la carrilera
**no es un miembro sismorresistente**, así que no le aplican ni $R_y$ ni la Tabla 9. **S2**, la
sección es la adoptada acá, de simetría simple, con el ala superior más ancha y más gruesa
porque es la que resiste sola la flexión débil. **S3**, el riel es **declarado**: AIST deja su
tamaño al proveedor por un documento que no está en el corpus; su alto entra en el brazo de
torsión y su masa en el peso propio. **S4**, la flexión débil y la torsión las resiste el ala
superior sola, como una viga horizontal, y el par se descompone en un par de fuerzas entre las
dos alas — es la analogía que la propia cláusula remite a una guía que tampoco está en el
corpus. **S5**, el ala superior no pandea lateralmente en su propio plano porque el alma la
restringe de manera continua. **S6**, la tracción longitudinal la recoge la carrilera como
puntal, con la mitad del total en cada línea. **S7**, la clase de edificio se adopta **C**, que
es la que corresponde a los ciclos del 03 con la vida útil que ese eslabón declaró.

## A · El apoyo, que el 07 supuso y resulta ser una cláusula

### A1 · AIST no deja que la carrilera sea continua, y lo dice en tres frases

La cláusula pide que los vanos se dispongan **sin que se desarrolle continuidad apreciable**
entre vanos adyacentes, con conexiones independientes al final y al tope de cada viga, y
detalladas para minimizar la restricción al giro de extremo. Tres frases, tres formas de decir
lo mismo.

$$1 + \frac{ {{ vt('nch2369-galpon-grua/08', 's_marco', 2) }} - {{ vt('nch2369-galpon-grua/08', 'wb_ruedas', 2) }} }{ {{ vt('nch2369-galpon-grua/08', 's_marco', 2) }} } = {{ vt('nch2369-galpon-grua/08', 'coef_reac', 5) }} \qquad R_{\text{carril}} = {{ vt('nch2369-galpon-grua/08', 'R_carril_s', 5) }}\ \text{kN}$$

→ **{{ v('nch2369-galpon-grua/08', 'coef_reac', 5) }}** es el coeficiente de reacción con una
rueda sobre el apoyo y la otra a la distancia entre ruedas. Es el mismo que el 07 usó para
llevar el empuje lateral al marco.

### A2 · Y si fuera continua, la reacción del apoyo interior subiría 20,1 %

$$\frac{2L - w_b}{2L} = {{ vt('nch2369-galpon-grua/08', 'coef_077', 5) }} \qquad \frac{x\,(L^{2} - x^{2})}{2L^{3}} = {{ vt('nch2369-galpon-grua/08', 'eta2', 5) }} \qquad \eta = {{ vt('nch2369-galpon-grua/08', 'eta_cont', 5) }}$$

$$\frac{\eta}{ {{ vt('nch2369-galpon-grua/08', 'coef_reac', 5) }} } = {{ vt('nch2369-galpon-grua/08', 'sube_cont', 5) }} \qquad R_{\text{carril}}^{\text{cont}} = {{ vt('nch2369-galpon-grua/08', 'R_carril_cont', 5) }}\ \text{kN}$$

→ la reacción sube **{{ v('nch2369-galpon-grua/08', 'sube_cont', 5) }}**. El primer término de
$\eta$ es el mismo {{ v('nch2369-galpon-grua/08', 'coef_077', 5) }} que aparece en D1 y que el
07 ya había usado: la línea de influencia de una viga simple está adentro de la de la continua.

### A3 · Lo que eso le habría hecho al 07: nada que cambie una decisión

$$SS_{\text{marco}}^{\text{cont}} = {{ vt('nch2369-galpon-grua/08', 'SS_marco_cont', 5) }}\ \text{kN} \qquad d_{\text{riel}}^{\text{cont}} = {{ vt('nch2369-galpon-grua/08', 'd_riel_cont', 5) }}\ \text{mm} \qquad {{ vt('nch2369-galpon-grua/08', 'uso_cont', 5) }}$$

→ el empuje que llega a un marco pasaría de {{ v('nch2369-galpon-grua/08', 'SS_marco', 5) }} a
{{ v('nch2369-galpon-grua/08', 'SS_marco_cont', 5) }} kN y la deriva de servicio del 07 de
{{ v('nch2369-galpon-grua/08', 'uso_grua_07', 5) }} a
{{ v('nch2369-galpon-grua/08', 'uso_cont', 5) }}, **sin dejar de pasar**: quedaría margen
{{ v('nch2369-galpon-grua/08', 'margen_cont', 5) }}. El supuesto del 07 queda confirmado por
una razón distinta de la que lo motivó.

## B · Las dos clases C, que no son la misma letra

### B1 · La clase de edificio de AIST la fijan los ciclos, y nada más

$$\frac{N}{100\,000} = {{ vt('nch2369-galpon-grua/08', 'frac_techoC', 5) }} \qquad \frac{N}{20\,000} = {{ vt('nch2369-galpon-grua/08', 'veces_pisoC', 5) }}$$

→ los {{ v('nch2369-galpon-grua/08', 'N_ciclos', 0) }} ciclos del 03 caen dentro de la clase
**C**, al {{ v('nch2369-galpon-grua/08', 'frac_techoC', 5, 100) }} % del techo. Las dos letras
C de esta serie —la de servicio de la grúa, que el 03 derivó de CMAA, y ésta, de edificio—
coinciden por el número y deciden cosas distintas.

### B2 · Y con la vida útil que la propia cláusula recomienda, sería clase B

$$N_{50} = {{ vt('nch2369-galpon-grua/08', 'N_ciclos', 0) }} \cdot \frac{ {{ vt('nch2369-galpon-grua/08', 'vida_aist', 0) }} }{ {{ vt('nch2369-galpon-grua/08', 'vida_grua', 0) }} } = {{ vt('nch2369-galpon-grua/08', 'N_50', 0) }} \qquad {{ vt('nch2369-galpon-grua/08', 'sobre_techoC', 5) }}$$

→ **{{ v('nch2369-galpon-grua/08', 'N_50', 0) }} ciclos**, un 50 % sobre el techo de la clase
C: con la vida útil que AIST recomienda, este edificio es **clase B**.

### B3 · Lo que la letra decide es un factor 1,67 en la flecha vertical

$$\frac{L}{600} = {{ vt('nch2369-galpon-grua/08', 'dlim_v_C', 2) }}\ \text{mm} \qquad \frac{L}{1\,000} = {{ vt('nch2369-galpon-grua/08', 'dlim_v_B', 2) }}\ \text{mm} \qquad {{ vt('nch2369-galpon-grua/08', 'razon_lim_v', 5) }} \qquad \frac{L}{400} = {{ vt('nch2369-galpon-grua/08', 'dlim_lat', 2) }}\ \text{mm}$$

→ **{{ v('nch2369-galpon-grua/08', 'dlim_v_C', 2) }} mm** con la clase C y
{{ v('nch2369-galpon-grua/08', 'dlim_v_B', 2) }} con la B, un factor
{{ v('nch2369-galpon-grua/08', 'razon_lim_v', 5) }}. Y el límite lateral coincide en número con
el de deriva del marco del 06, por dos caminos distintos.

## C · La sección, y el peso que el 05 no tenía

### C1 · El ala superior grande es lo que la tipología usa, y por la flexión débil

$$d = {{ vt('nch2369-galpon-grua/08', 'd_carril', 2) }}\ \text{mm} \qquad A = {{ vt('nch2369-galpon-grua/08', 'A_carril', 2) }}\ \text{mm}^2 \qquad \frac{A_{\text{sup}}}{A_{\text{inf}}} = {{ vt('nch2369-galpon-grua/08', 'razon_alas', 5) }}$$

→ **{{ v('nch2369-galpon-grua/08', 'd_carril', 2) }} mm de canto** y el ala superior con **el
doble** de área que la inferior. Ese doble no es estética: el ala superior resiste sola la
flexión débil y la torsión.

### C2 · Las propiedades, y que el eje neutro sube

$$\bar{y} = {{ vt('nch2369-galpon-grua/08', 'ybar_carril', 5) }}\ \text{mm} \qquad d - \bar{y} = {{ vt('nch2369-galpon-grua/08', 'y_inf', 5) }}\ \text{mm} \qquad I_x = {{ vt('nch2369-galpon-grua/08', 'Ix_carril', 0) }}\ \text{mm}^4$$

$$S_{xc} = {{ vt('nch2369-galpon-grua/08', 'Sxc_carril', 0) }}\ \text{mm}^3 \qquad S_{xt} = {{ vt('nch2369-galpon-grua/08', 'Sxt_carril', 0) }}\ \text{mm}^3 \qquad y_p = {{ vt('nch2369-galpon-grua/08', 'y_p', 2) }}\ \text{mm} \qquad Z_x = {{ vt('nch2369-galpon-grua/08', 'Zx_carril', 0) }}\ \text{mm}^3$$

$$h_o = {{ vt('nch2369-galpon-grua/08', 'h_o', 2) }}\ \text{mm} \qquad h_c = {{ vt('nch2369-galpon-grua/08', 'h_c', 5) }}\ \text{mm} \qquad h_p = {{ vt('nch2369-galpon-grua/08', 'h_p', 2) }}\ \text{mm} \qquad J = {{ vt('nch2369-galpon-grua/08', 'J_carril', 0) }}\ \text{mm}^4$$

$$I_y = {{ vt('nch2369-galpon-grua/08', 'Iy_carril', 0) }}\ \text{mm}^4 \qquad r_y = {{ vt('nch2369-galpon-grua/08', 'ry_carril', 5) }}\ \text{mm}$$

→ el eje neutro elástico queda a {{ v('nch2369-galpon-grua/08', 'ybar_carril', 5) }} mm del ala
superior, o sea **arriba del medio canto**, y por eso el módulo al ala traccionada es el menor
de los dos: es esa ala la que fluye primero.

### C3 · La compacidad no es opcional, y es el ala superior la que la fija

$$\lambda_{\text{ala}} = {{ vt('nch2369-galpon-grua/08', 'lam_ala_sup', 2) }} \qquad \lambda_p = {{ vt('nch2369-galpon-grua/08', 'lam_p_ala', 5) }} \qquad {{ vt('nch2369-galpon-grua/08', 'uso_compac', 5) }} \qquad b_{f}^{\text{máx}} = {{ vt('nch2369-galpon-grua/08', 'bf_max', 5) }}\ \text{mm}$$

$$\lambda_{\text{alma}} = {{ vt('nch2369-galpon-grua/08', 'lam_alma', 5) }} \qquad \lambda_{rw} = {{ vt('nch2369-galpon-grua/08', 'lam_rw', 5) }}$$

→ el ala superior usa **{{ v('nch2369-galpon-grua/08', 'uso_compac', 5) }}** de su límite de
compacidad: **el ancho de {{ v('nch2369-galpon-grua/08', 'bfs_carril', 0) }} mm no lo elige el
diseñador**, lo fija la cláusula, y el máximo compacto está en
{{ v('nch2369-galpon-grua/08', 'bf_max', 5) }} mm.

### C4 · El peso propio real, que es 1,35 veces el que el 05 declaró

$$w_{\text{viga}} = {{ vt('nch2369-galpon-grua/08', 'w_viga', 5) }}\ \text{kN}/\text{m} \qquad w_{\text{riel}} = {{ vt('nch2369-galpon-grua/08', 'w_riel', 5) }}\ \text{kN}/\text{m} \qquad w = {{ vt('nch2369-galpon-grua/08', 'w_carril', 5) }}\ \text{kN}/\text{m}$$

$$\frac{w}{w^{05}} = {{ vt('nch2369-galpon-grua/08', 'sobre_05', 5) }} \qquad E_{z}^{\text{real}} = {{ vt('nch2369-galpon-grua/08', 'Ez_real', 5) }}\ \text{kN} \qquad {{ vt('nch2369-galpon-grua/08', 'sube_Ez', 5) }} \qquad {{ vt('nch2369-galpon-grua/08', 'sube_P', 5) }}$$

→ la viga sola pesa {{ v('nch2369-galpon-grua/08', 'w_viga', 5) }} kN/m, o sea **el presupuesto
entero** que el 05 le había dado para viga, riel y ménsula juntos; con el riel encima suma
{{ v('nch2369-galpon-grua/08', 'w_carril', 5) }}. La componente vertical de esa línea subiría
{{ v('nch2369-galpon-grua/08', 'sube_Ez', 5) }} y el peso sísmico del edificio
{{ v('nch2369-galpon-grua/08', 'sube_P', 5) }}. Son correcciones que este eslabón **devuelve
hacia atrás sin rehacer nada**, porque las razones de la serie son invariantes en el peso.

## D · Las solicitaciones, y una excentricidad que no elige el diseñador

{{ figura('nch2369-galpon-grua/08', 'posiciones', 'Tres elevaciones del mismo vano de 7,50 metros con las dos ruedas a 3,40 de separación en las tres posiciones que gobiernan: momento máximo con la primera rueda a 2,90 y reacción 0,77333 por rueda, reacción máxima con una rueda sobre el apoyo y coeficiente 1,54667, y flecha máxima con las dos ruedas simétricas respecto del centro a 2 050 mm de cada apoyo') }}

### D1 · La posición de momento máximo, y el 0,77333 por tercera vez

Con dos cargas iguales separadas $w_b$ sobre un vano simple, el momento máximo cae bajo una
rueda cuando el centro del vano bisecta la distancia entre esa rueda y la resultante.

$$x_1 = \frac{L}{2} - \frac{w_b}{4} = {{ vt('nch2369-galpon-grua/08', 'x1_rueda', 2) }}\ \text{m} \qquad \frac{2L - w_b}{2L} = {{ vt('nch2369-galpon-grua/08', 'coef_077', 5) }} \qquad {{ vt('nch2369-galpon-grua/08', 'coef_M', 5) }}\ \text{m}$$

$$M_{\text{serv}} = R_w^{\text{máx}} \cdot {{ vt('nch2369-galpon-grua/08', 'coef_M', 5) }} = {{ vt('nch2369-galpon-grua/08', 'M_serv', 5) }}\ \text{kN}\cdot\text{m}$$

→ la primera rueda a {{ v('nch2369-galpon-grua/08', 'x1_rueda', 2) }} m del apoyo y la segunda a
{{ v('nch2369-galpon-grua/08', 'x2_rueda', 2) }}, con la reacción izquierda en
{{ v('nch2369-galpon-grua/08', 'coef_077', 5) }} de una rueda. El coeficiente de momento es
{{ v('nch2369-galpon-grua/08', 'coef_M', 5) }} m, un 19,6 % más que el $L/4$ de una sola rueda
al centro; y es una reacción **adimensional**: dos ruedas reparten y el número no depende de
cuánto pesan.

### D2 · El momento de diseño, con la combinación chilena y no la de AIST

NCh3171 trata la carga de grúa como sobrecarga entera; AIST la **separa** en peso propio de la
grúa, carga izada, impacto y empuje, y amplifica el primero por 1,2 y el resto por 1,6.

$$\kappa = {{ vt('nch2369-galpon-grua/08', 'kappa', 5) }} \qquad R_{Cds} = {{ vt('nch2369-galpon-grua/08', 'R_Cds', 5) }}\ \text{kN} \qquad R_{Cvs} = {{ vt('nch2369-galpon-grua/08', 'R_Cvs', 5) }}\ \text{kN} \qquad {{ vt('nch2369-galpon-grua/08', 'R_suma', 5) }}\ \text{kN}$$

$$P^{\text{AIST}} = {{ vt('nch2369-galpon-grua/08', 'P_aist', 5) }}\ \text{kN} \qquad P^{\text{NCh}} = {{ vt('nch2369-galpon-grua/08', 'P_nch', 5) }}\ \text{kN} \qquad {{ vt('nch2369-galpon-grua/08', 'mas_nch', 5) }}$$

$$w_u = {{ vt('nch2369-galpon-grua/08', 'w_u', 5) }}\ \text{kN}/\text{m} \qquad R_{izq} = {{ vt('nch2369-galpon-grua/08', 'R_izq', 5) }}\ \text{kN} \qquad M_{ux} = {{ vt('nch2369-galpon-grua/08', 'M_ux', 5) }}\ \text{kN}\cdot\text{m}$$

→ **{{ v('nch2369-galpon-grua/08', 'M_ux', 5) }} kN·m**. La rueda mayorada por la combinación
chilena es {{ v('nch2369-galpon-grua/08', 'mas_nch', 5) }} veces la de AIST, y la diferencia es
exactamente el peso propio del puente y del carro: **carga muerta que se mueve**, y NCh3171 no
tiene dónde ponerla.

Ese momento es el que el modelo dibuja. La viga de un vano con sus dos ruedas es una entrada
propia de este sitio, y el visor la resuelve entera:

<rukan-visor src="../../../modelos/carrilera/carrilera.escena.json" caso="U" esfuerzo="Mz" filtro="CAR_*" vista="longitudinal"></rukan-visor>

El máximo cae bajo la primera rueda, en {{ r('carrilera', 'M_ux', 5, factor=-1) }} kN·m contra
los {{ v('nch2369-galpon-grua/08', 'M_ux', 5) }} de arriba: la diferencia es de 4·10⁻⁶
relativos y sale de que este eslabón sustituye el coeficiente
{{ v('nch2369-galpon-grua/08', 'coef_077', 5) }} **impreso** y el modelo divide sin redondear.
Los cuartos de vano cierran igual, y son los que el $C_b$ de E2 consume.

### D3 · La torsión, y que su excentricidad la fija una tolerancia de montaje

$$e_v = {{ vt('nch2369-galpon-grua/08', 'ev_carril', 5) }}\ \text{mm} \qquad e_h = {{ vt('nch2369-galpon-grua/08', 'c_e_riel', 2) }}\,t_w = {{ vt('nch2369-galpon-grua/08', 'e_riel', 5) }}\ \text{mm}$$

$$T = {{ vt('nch2369-galpon-grua/08', 'T_empuje', 5) }} + {{ vt('nch2369-galpon-grua/08', 'T_exc', 5) }} = {{ vt('nch2369-galpon-grua/08', 'T_par', 5) }}\ \text{kN}\cdot\text{mm} \qquad {{ vt('nch2369-galpon-grua/08', 'frac_exc', 5) }}$$

→ el par por rueda tiene dos fuentes, y la segunda no es una carga: es la **excentricidad
máxima que la tolerancia de montaje admite**, tres cuartos del espesor del alma. Pone el
{{ v('nch2369-galpon-grua/08', 'frac_exc', 5, 100) }} % del par. Eso vuelve al alma un elemento
con el signo cambiado: engrosarla aumenta la excentricidad admitida en la misma proporción, sin
aumentar la resistencia del ala, que es quien resiste el par.

### D4 · El momento débil, con el par convertido en fuerza de ala

$$F_{\text{par}} = \frac{T}{h_o} = {{ vt('nch2369-galpon-grua/08', 'F_par', 5) }}\ \text{kN} \qquad H_{\text{ala}} = {{ vt('nch2369-galpon-grua/08', 'H_ala', 5) }}\ \text{kN} \qquad {{ vt('nch2369-galpon-grua/08', 'amplif_tors', 5) }} \qquad M_{uy} = {{ vt('nch2369-galpon-grua/08', 'M_uy', 5) }}\ \text{kN}\cdot\text{m}$$

→ la torsión amplifica la fuerza lateral sobre el ala superior en
{{ v('nch2369-galpon-grua/08', 'amplif_tors', 5) }}.

### D5 · El corte y la reacción, que es la que el 07 ya había publicado

$$R = {{ vt('nch2369-galpon-grua/08', 'R_serv', 5) }}\ \text{kN} \qquad V_u = {{ vt('nch2369-galpon-grua/08', 'V_u', 5) }}\ \text{kN} \qquad P_u = {{ vt('nch2369-galpon-grua/08', 'P_u', 5) }}\ \text{kN}$$

→ la reacción de servicio coincide con la que el 07 metió en la columna, y el axial
longitudinal es la mitad de la tracción total del 03, mayorada.

## E · Resistencias e interacción biaxial

### E1 · El ala grande sube $S_{xc}$ y baja $F_L$, que es el precio de C1

$$M_p = {{ vt('nch2369-galpon-grua/08', 'M_p', 5) }}\ \text{kN}\cdot\text{m} \qquad M_{yt} = {{ vt('nch2369-galpon-grua/08', 'M_yt', 5) }}\ \text{kN}\cdot\text{m} \qquad R_{pc} = {{ vt('nch2369-galpon-grua/08', 'R_pc', 5) }} \qquad R_{pt} = {{ vt('nch2369-galpon-grua/08', 'R_pt', 5) }}$$

$$\frac{S_{xt}}{S_{xc}} = {{ vt('nch2369-galpon-grua/08', 'razon_S', 5) }} \qquad F_L = {{ vt('nch2369-galpon-grua/08', 'F_L', 5) }}\ \text{MPa} \qquad {{ vt('nch2369-galpon-grua/08', 'queda_07Fy', 5) }}$$

→ la razón entre los dos módulos elásticos cae **bajo 0,70**, así que el esfuerzo que arranca
el pandeo no es el $0{,}7F_y$ del caso simétrico sino
{{ v('nch2369-galpon-grua/08', 'F_L', 5) }} MPa: queda el
{{ v('nch2369-galpon-grua/08', 'queda_07Fy', 5) }} de aquél. Es el precio de haber hecho el ala
superior grande, y lo paga el pandeo lateral-torsional.

### E2 · El pandeo lateral-torsional no gobierna, y lo salva el $C_b$ por 2,6 %

$$a_w = {{ vt('nch2369-galpon-grua/08', 'a_w', 5) }} \qquad r_t = {{ vt('nch2369-galpon-grua/08', 'r_t', 5) }}\ \text{mm} \qquad L_p = {{ vt('nch2369-galpon-grua/08', 'L_p', 5) }}\ \text{mm} \qquad L_r = {{ vt('nch2369-galpon-grua/08', 'L_r_ltb', 5) }}\ \text{mm}$$

$$M_A = {{ vt('nch2369-galpon-grua/08', 'M_A', 5) }} \qquad M_B = {{ vt('nch2369-galpon-grua/08', 'M_B', 5) }} \qquad M_C = {{ vt('nch2369-galpon-grua/08', 'M_C', 5) }} \qquad C_b = {{ vt('nch2369-galpon-grua/08', 'C_b', 5) }}$$

$$M_n^{LTB} = {{ vt('nch2369-galpon-grua/08', 'Mn_LTB', 5) }}\ \text{kN}\cdot\text{m} \qquad C_b^{\text{mín}} = {{ vt('nch2369-galpon-grua/08', 'Cb_min', 5) }} \qquad {{ vt('nch2369-galpon-grua/08', 'margen_Cb', 5) }} \qquad M_{cx} = {{ vt('nch2369-galpon-grua/08', 'M_cx', 5) }}\ \text{kN}\cdot\text{m}$$

→ el pandeo **no gobierna**, y lo salva el factor de forma del diagrama por
{{ v('nch2369-galpon-grua/08', 'margen_Cb', 5) }}: con $C_b = 1$ el momento nominal caería bajo
$M_p$. Los tres momentos que ese factor consume son los cuartos del vano, y el visor de arriba
los dibuja. El uso en flexión fuerte queda en
{{ v('nch2369-galpon-grua/08', 'uso_fuerte', 5) }}.

### E3 · El ala superior en flexión débil, y el axial

$$Z_y = {{ vt('nch2369-galpon-grua/08', 'Z_y', 0) }}\ \text{mm}^3 \qquad M_{cy} = {{ vt('nch2369-galpon-grua/08', 'M_cy', 5) }}\ \text{kN}\cdot\text{m} \qquad {{ vt('nch2369-galpon-grua/08', 'uso_debil', 5) }}$$

$$\frac{L}{r_y} = {{ vt('nch2369-galpon-grua/08', 'esbeltez_punt', 5) }} \qquad F_e = {{ vt('nch2369-galpon-grua/08', 'F_e', 5) }}\ \text{MPa} \qquad F_{cr} = {{ vt('nch2369-galpon-grua/08', 'F_cr', 5) }}\ \text{MPa} \qquad P_c = {{ vt('nch2369-galpon-grua/08', 'P_c', 5) }}\ \text{kN}$$

### E4 · La interacción de H1-1b, que es lo que dimensiona la viga

$$\frac{P_r}{P_c} = {{ vt('nch2369-galpon-grua/08', 'razon_axial', 5) }} \qquad {{ vt('nch2369-galpon-grua/08', 'term_axial', 5) }} + {{ vt('nch2369-galpon-grua/08', 'uso_fuerte', 5) }} + {{ vt('nch2369-galpon-grua/08', 'uso_debil', 5) }} = {{ vt('nch2369-galpon-grua/08', 'interaccion', 5) }}$$

$$\text{sin torsión: } {{ vt('nch2369-galpon-grua/08', 'interaccion_sin', 5) }} \qquad {{ vt('nch2369-galpon-grua/08', 'pesa_tors', 5) }}$$

→ **{{ v('nch2369-galpon-grua/08', 'interaccion', 5) }}**, y eso es lo que dimensiona la viga.
Ignorar la torsión dejaría la interacción en
{{ v('nch2369-galpon-grua/08', 'interaccion_sin', 5) }} y **el margen aparente en el doble del
real**.

### E5 y E6 · El corte, y el alma bajo la rueda

$$C_{v1} = {{ vt('nch2369-galpon-grua/08', 'C_v1', 5) }} \qquad V_c = {{ vt('nch2369-galpon-grua/08', 'V_c', 5) }}\ \text{kN} \qquad {{ vt('nch2369-galpon-grua/08', 'uso_corte', 5) }}$$

$$l_{ef} = {{ vt('nch2369-galpon-grua/08', 'lef_carril', 5) }}\ \text{mm} \qquad R_n = {{ vt('nch2369-galpon-grua/08', 'R_n', 5) }}\ \text{kN} \qquad {{ vt('nch2369-galpon-grua/08', 'uso_alma_rueda', 5) }}$$

→ el campo de tracción está **prohibido** en carrileras, así que el corte se toma sin él. Y el
largo efectivo de alma bajo la rueda **lo define AIST él mismo**, en vez de remitir a AISC: dos
veces el canto combinado del riel y el ala.

## F · Las tres flechas de servicio, y la que nadie mide

{{ figura('nch2369-galpon-grua/08', 'flechas', 'Cuatro flechas de servicio de la viga carrilera contra sus límites en la misma escala de milímetros: la vertical de 8,26725 contra los 12,50 de la clase C y los 7,50 de la clase B, la lateral de 14,64206 con la fuerza de CMAA y 13,62144 con la de AIST contra 18,75, y la suma de la deriva del marco con la flecha de la viga, 17,72361, contra el mismo 18,75 que ninguna cláusula aplica a la suma') }}

### F1 y F3 · La flecha vertical, y lo que la clase B habría exigido

$$b = {{ vt('nch2369-galpon-grua/08', 'b_flecha', 2) }}\ \text{mm} \qquad \delta_v = {{ vt('nch2369-galpon-grua/08', 'delta_v', 5) }}\ \text{mm} \qquad {{ vt('nch2369-galpon-grua/08', 'uso_v_C', 5) }} \qquad \text{clase B: } {{ vt('nch2369-galpon-grua/08', 'uso_v_B', 5) }}$$

→ con la clase C pasa en {{ v('nch2369-galpon-grua/08', 'uso_v_C', 5) }}; con la B **no pasa**,
y pediría {{ v('nch2369-galpon-grua/08', 'I_clase_B', 0) }} mm⁴ de inercia, un 10,2 % más. Es
la decisión más frágil del eslabón y **no la toma el calculista**.

### F2 · La flecha lateral, y las dos fuerzas que se disputan el mismo límite

$$I_{\text{ala}} = {{ vt('nch2369-galpon-grua/08', 'I_ala', 0) }}\ \text{mm}^4 \qquad H_{CMAA} = {{ vt('nch2369-galpon-grua/08', 'H_CMAA', 5) }}\ \text{kN} \qquad \delta_l^{CMAA} = {{ vt('nch2369-galpon-grua/08', 'delta_l_CMAA', 5) }}\ \text{mm} \qquad {{ vt('nch2369-galpon-grua/08', 'uso_l_CMAA', 5) }}$$

$$\delta_l^{AIST} = {{ vt('nch2369-galpon-grua/08', 'delta_l_AIST', 5) }}\ \text{mm} \qquad {{ vt('nch2369-galpon-grua/08', 'uso_l_AIST', 5) }} \qquad {{ vt('nch2369-galpon-grua/08', 'mayor_CMAA', 5) }} \qquad {{ vt('nch2369-galpon-grua/08', 'frac_desc', 5) }}$$

→ **gobierna la de CMAA**. Y acá se corrige un hallazgo del 03, que llamó al 10 % de CMAA «un
tercio del 30 % de AIST»: **el factor 3 compara porcentajes de bases distintas**. En fuerza por
rueda, la de servicio de CMAA es {{ v('nch2369-galpon-grua/08', 'mayor_CMAA', 5) }} veces la de
AIST en la carrilera cargada, y {{ v('nch2369-galpon-grua/08', 'frac_desc', 5) }} de ella en la
descargada: **se invierte**.

### F4 · Y el desplazamiento que la cabeza del riel sí ve

$$d_{\text{riel}}^{\text{marco}} + \delta_l^{CMAA} = {{ vt('nch2369-galpon-grua/08', 'd_riel_grua', 5) }} + {{ vt('nch2369-galpon-grua/08', 'delta_l_CMAA', 5) }} = {{ vt('nch2369-galpon-grua/08', 'd_total_riel', 5) }}\ \text{mm} \qquad {{ vt('nch2369-galpon-grua/08', 'uso_suma', 5) }}$$

→ la cabeza del riel se mueve {{ v('nch2369-galpon-grua/08', 'd_total_riel', 5) }} mm, el
{{ v('nch2369-galpon-grua/08', 'uso_suma', 5, 100) }} % de un límite que la deriva y la flecha
miran **cada una por separado**. El 07 mostró que el criterio de la grúa toleraría un marco
mucho más flexible; lo que falta decir es que **esa holgura no era del sistema**.

## Veredicto

**La carrilera cierra, y lo que la dimensiona es la interacción biaxial**, en
{{ v('nch2369-galpon-grua/08', 'interaccion', 5) }} de H1-1b contra
{{ v('nch2369-galpon-grua/08', 'uso_v_C', 5) }} de la flecha vertical,
{{ v('nch2369-galpon-grua/08', 'uso_l_CMAA', 5) }} de la lateral y
{{ v('nch2369-galpon-grua/08', 'uso_corte', 5) }} de corte. **No gobierna un estado de
servicio**, que es lo que la tipología hace esperar: la luz es demasiado corta para que $L/600$
muerda.

**El apoyo simple no era una simplificación conservadora: era la cláusula.** Si hubiera
continuidad, la reacción de un apoyo interior subiría
{{ v('nch2369-galpon-grua/08', 'sube_cont', 5) }} y la deriva del 07 iría a
{{ v('nch2369-galpon-grua/08', 'uso_cont', 5) }}, sin dejar de pasar.

**Hay dos clases C en esta serie y no son la misma letra.** Con los
{{ v('nch2369-galpon-grua/08', 'vida_aist', 0) }} años que la cláusula recomienda —contra los
{{ v('nch2369-galpon-grua/08', 'vida_grua', 0) }} que el 03 declaró— el mismo régimen da
{{ v('nch2369-galpon-grua/08', 'N_50', 0) }} ciclos, clase **B**, y la flecha vertical fallaría
en {{ v('nch2369-galpon-grua/08', 'uso_v_B', 5) }}.

**La torsión vale casi diez puntos de la interacción, y un tercio de eso no es de diseño**:
sale de la excentricidad máxima que la tolerancia de montaje admite,
{{ v('nch2369-galpon-grua/08', 'e_riel', 2) }} mm.

Y dos correcciones que este eslabón devuelve hacia atrás **sin rehacer nada**: el peso propio
real de la carrilera con su riel es {{ v('nch2369-galpon-grua/08', 'sobre_05', 5) }} veces el
que el 05 declaró, y la fuerza lateral de servicio de CMAA no es un tercio de la de AIST sino
{{ v('nch2369-galpon-grua/08', 'mayor_CMAA', 5) }} veces.

## Límites

- **Dos filas del `## Resumen` del memo no reproducen, y son la misma especie que las tres del
  07.** El momento de fluencia del ala comprimida cae en un **empate exacto** en el sexto
  decimal, y el memo imprimió el dígito que su propia regla de redondeo —medio hacia arriba— no
  da. Y la razón entre la flecha de la viga y la deriva del marco sale
  {{ v('nch2369-galpon-grua/08', 'veces_viga', 5) }} con las cifras impresas, que es lo que la
  regla de la serie manda sustituir, contra el 4,75151 que el memo publica dividiendo sin
  redondear. Ninguna de las dos se propaga. Su arnés las dejaba pasar porque comparaba con
  tolerancia relativa.
- **La carrilera no se verifica a fatiga acá.** Todo esto es resistencia y servicio bajo la
  carga máxima; el rango de tensiones bajo el paso de cada rueda y la categoría de la soldadura
  alma-ala son del eslabón 09, que hereda la sección, los dos módulos, el momento de servicio y
  la excentricidad del riel.
- **La clase de edificio se adopta y no se deriva.** Es el único resultado que cambia de signo
  con un dato que nadie ha fijado, y la sección publicada depende de él.
- **El peso propio real supera lo que el 05 declaró y no se propaga hacia atrás.** La ménsula
  del 10 todavía no está adentro y **va a agrandar la diferencia**, no a cerrarla.
- **La continuidad se cuantifica sobre dos vanos y la carrilera real tiene cuatro.** El arnés
  del memo resuelve la de cuatro por rigidez directa y da 1,84482 contra los
  {{ v('nch2369-galpon-grua/08', 'eta_cont', 5) }} de dos: el caso de dos vanos es 0,7 % más
  desfavorable. Como la conclusión es que la continuidad no se puede usar, no decide nada.
- **La analogía de flexión para la torsión es un modelo, no una cláusula.** La propia cláusula
  declara que la solución exacta queda fuera de su alcance y remite a una guía que no está en
  el corpus. El tratamiento riguroso —alabeo, bimomento, la rigidez torsional de la sección
  abierta— daría menos demanda en el ala; el modelo adoptado es el conservador.
- **El pandeo lateral del ala superior en su propio plano se descarta por argumento.** El alma
  la restringe de manera continua, pero la cláusula no tiene una excepción escrita para esto.
- **El riel es declarado.** Un riel más alto sube el brazo de torsión proporcionalmente; uno de
  152 mm llevaría la interacción a rozar 1,0.
- **La sujeción del riel al ala no se diseña**, ni los atiesadores de apoyo, ni la conexión de
  tirante, ni el asiento sobre la ménsula: los cuatro son del eslabón 10.
- **El modelo de esta página no lleva el empuje lateral ni la torsión.** El visor resuelve la
  flexión vertical del vano con sus dos ruedas, que es lo que D2 calcula; la flexión débil y el
  par son del ala superior sola y se resuelven a mano acá. Además, la torsión de barra de Rukan
  sigue sin contraste contra SAP2000.
- **No se verifica el pandeo del alma por desplazamiento lateral**, que la cláusula lista como
  estado límite. Con la esbeltez de esta alma el parámetro queda del lado holgado, pero no se
  calculó.

## Ficha

{{ ficha('nch2369-galpon-grua/08') }}

## Referencias

| Clave | Norma y edición | Cláusula | Leída en | Cita textual |
|---|---|---|---|---|
| AIST-1 | AIST TR-13:2021 | §1.4, que la clasificación se basa en los ciclos y que la vida de servicio recomendada es de 50 años | `Normas/aist-tr-no13-2021-3.pdf`, p. 10 | «A service life of 50 years is generally recommended» |
| AIST-1b | AIST TR-13:2021 | §1.4, que la clasificación la especifica el propietario | PDF ídem, p. 10 | «the owner shall specify the classification for all or any portion of a building» |
| AIST-1c | AIST TR-13:2021 | §1.4.3, la clase C de edificio entre 20 000 y 100 000 repeticiones | PDF ídem, p. 10 | «Buildings in this category are those buildings in which members experience 20,000 to 100,000 repetitions of a specific loading» |
| AIST-1d | AIST TR-13:2021 | §1.4.2, la clase B, que es donde cae con 50 años de vida | PDF ídem, p. 10 | «100,000 to 500,000 repetitions of a specific loading during the expected service life» |
| AIST-1e | AIST TR-13:2021 | Tabla 1.1, los cuatro rangos de ciclos y su base de 50 años — **mirada en PNG**, no extraída | PDF ídem, p. 11 | «About 5 applications per day for 50 years» |
| AIST-2 | AIST TR-13:2021 | §5.8.1, que no se desarrolle continuidad apreciable entre vanos adyacentes | PDF ídem, p. 30 | «without the development of appreciable continuity between adjacent spans» |
| AIST-2b | AIST TR-13:2021 | §5.8.1, las conexiones independientes al final y al tope de cada viga | PDF ídem, p. 30 | «Independent connections to the column at the end and top of each girder shall be provided» |
| AIST-2c | AIST TR-13:2021 | §5.8.1, el detalle que minimiza la restricción al giro de extremo | PDF ídem, p. 30 | «designed and detailed to minimize restraint of girder end rotations» |
| AIST-3 | AIST TR-13:2021 | §5.8.2, la flexión biaxial y la sección de simetría simple con ala superior mayor | PDF ídem, p. 31 | «Crane runway girders are often singly symmetric shapes with a larger top flange» |
| AIST-3b | AIST TR-13:2021 | §5.8.2, que el ala superior y el alma deben ser compactas | PDF ídem, p. 31 | «The top flange and web of the crane runway girder shall be compact as defined» |
| AIST-3c | AIST TR-13:2021 | §5.8.2, la torsión de la carga vertical cuando el riel no se alinea con el alma | PDF ídem, p. 31 | «Torsional moments are also generated by crane vertical wheel loads if the centerline of rail does not align with the centerline of the crane girder web» |
| AIST-3d | AIST TR-13:2021 | §5.8.2, que la solución exacta de la torsión queda fuera del alcance del documento | PDF ídem, p. 31 | «is complex and beyond the scope of this document» |
| AIST-3e | AIST TR-13:2021 | §5.8.2, la lista de estados límite pertinentes, incluida la interacción biaxial con axial | PDF ídem, p. 31 | «Design for Interaction of Strong Axis Bending, Weak Axis Bending and Axial Forces» |
| AIST-3f | AIST TR-13:2021 | §5.8.2.1, el arriostramiento de respaldo recomendado sobre 50 ft, que este vano no alcanza | PDF ídem, p. 32 | «be provided for girders with spans greater than 50 ft» |
| AIST-4 | AIST TR-13:2021 | §5.8.3, que la acción de campo de tracción no se permite en carrileras | PDF ídem, p. 33 | «The use of tension field action per Section G3 of Ref. 1 is not permitted for crane girders» |
| AIST-4b | AIST TR-13:2021 | §5.8.3, los atiesadores de apoyo, que este memo no diseña | PDF ídem, p. 33 | «Bearing stiffeners shall be used where required to transmit end reactions» |
| AIST-5 | AIST TR-13:2021 | §5.8.4, el largo efectivo de alma bajo la rueda, que AIST define en vez de remitir | PDF ídem, p. 33 | «the effective length of web beneath the wheel load shall be equal to two times the combined depth of the crane rail and girder flange thickness» |
| AIST-6 | AIST TR-13:2021 | §5.8.7, la flecha vertical por clase de edificio, con una grúa y sin impacto | PDF ídem, p. 34 | «Maximum vertical deflection of the girders due to a single crane load without impact shall not exceed the following ratios of the span length» |
| AIST-6b | AIST TR-13:2021 | §5.8.7, la flecha lateral bajo el empuje de una sola grúa | PDF ídem, p. 34 | «Maximum lateral deflection of a girder caused by a side thrust load from one crane shall not exceed 1/400 of the span length» |
| AIST-6c | AIST TR-13:2021 | §5.8.8, la contraflecha sobre 75 ft, umbral que este vano no alcanza | PDF ídem, p. 34 | «Girders of spans greater than 75 ft. shall be cambered» |
| AIST-7 | AIST TR-13:2021 | §5.17.6, la excentricidad máxima del riel sobre el alma, que fija el par torsor de D3 | PDF ídem, p. 40 | «In no case shall the rail eccentricity be greater than three-fourths of the girder web thickness» |
| AIST-8 | AIST TR-13:2021 | §3.11.2.1, las combinaciones LRFD y la 2c, que separa la carga muerta de la grúa de la izada | PDF ídem, p. 23 | «Load and Resistance Factor Design (LRFD) Load Combinations» |
| AIST-9 | AIST TR-13:2021 | §3.11.2.3, que los ciclos de fatiga siguen la clasificación de edificio del §1.4 | PDF ídem, p. 23 | «The number of cycles used as the basis for fatigue design shall be consistent with the building classification» |
| AIST-10 | AIST TR-13:2021 | Comm 5.8, por qué la tipología prefiere el vano simple | PDF ídem, p. 53 | «Simple beam girders are preferred by most mill building engineers because they are readily replaced if damaged» |
| AIST-11 | AIST TR-13:2021 | §5.3, la deriva del marco al nivel de las carrileras, que F4 suma con la de la viga | PDF ídem, p. 29 | «shall be no greater than 1/400 of the height from column base or 2 in., whichever is less» |
| CMAA-1 | CMAA 70:2010 | §1.4.6, que la carrilera se diseña con rigidez suficiente para evitar flechas perjudiciales — **PDF escaneado, leído a ojo** | `Normas/cmaa-70.pdf`, p. 8 | «The crane runway shall be designed with sufficient strength and rigidity to prevent detrimental lateral or vertical deflection» |
| CMAA-2 | CMAA 70:2010 | §1.4.6, la flecha lateral con el 10 % de la carga máxima de rueda — **leído a ojo** | PDF ídem, p. 8 | «The lateral deflection should not exceed» |
| CMAA-3 | CMAA 70:2010 | §1.4.6, la flecha vertical con la carga máxima de rueda sin factor de impacto — **leído a ojo** | PDF ídem, p. 8 | «The vertical deflection should not exceed» |
| CMAA-4 | CMAA 70:2010 | §1.4.6, que la luz de referencia es la del vano evaluado — **leído a ojo** | PDF ídem, p. 8 | «Runway girder span being evaluated» |
| NCh-p1 | NCh2369:2025 (3.ª ed.) | C6.1, la obligación de informar cuando el desplazamiento afecta la operación del equipo | `Normas/NCh 2369 - 3°Edición 2025.05.28.pdf`, p. 75 | «las condiciones se deben informar, indicando las consecuencias directas causadas por el desplazamiento relativo» |
| NCh-5 | NCh2369:2025 (3.ª ed.) | §5.1.2 y §5.7.1, las cargas permanentes y la componente vertical que C4 recalcula | `referencias/NCh2369-2025/cap05-analisis-sismico.md` | — |
| NCh-12 | NCh2369:2025 (3.ª ed.) | §12.1.3, que la carga suspendida no entra a la masa sísmica | `referencias/NCh2369-2025/cap12-estructuras-especificas.md` | — |
| N3171-w | NCh3171:2017 | §9.1.1 (2), la combinación $1{,}2D + 1{,}6L$ con la que se mayora la carga de grúa | `referencias/NCh3171-2017/cap09-combinaciones-de-carga.md` | — |
| AISC360-1 | ANSI/AISC 360-22 | §B4 y Tabla B4.1b casos 11 y 15, las propiedades y la compacidad de una sección armada | `referencias/AISC360-22/capB-requisitos-de-diseno.md` | — |
| AISC360-2 | ANSI/AISC 360-22 | §F1 y el $C_b$ de la Ec. F1-1; §F4 y Ecs. F4-1 a F4-15 para simetría simple; §F11 para el ala en su plano | `referencias/AISC360-22/capF-flexion.md` | — |
| AISC360-3 | ANSI/AISC 360-22 | §G2.1 con $C_{v1}$ y $k_v = 5{,}34$, y §G2.3 sobre cuándo se exigen atiesadores | `referencias/AISC360-22/capG-corte.md` | — |
| AISC360-4 | ANSI/AISC 360-22 | §H1.1 y la Ec. H1-1b, la interacción con $P_r/P_c < 0{,}20$ | `referencias/AISC360-22/capH-fuerzas-combinadas.md` | — |
| AISC360-5 | ANSI/AISC 360-22 | §E3, la resistencia de compresión por pandeo por flexión | `referencias/AISC360-22/capE-compresion.md` | — |
| AISC360-6 | ANSI/AISC 360-22 | §J10.2 y §J10.4, la fluencia local del alma y el pandeo por desplazamiento lateral que no se verifica | `referencias/AISC360-22/capJ-conexiones.md` | — |
