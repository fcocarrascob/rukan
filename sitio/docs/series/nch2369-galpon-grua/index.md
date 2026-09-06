# El galpón con puente grúa

Un galpón industrial de acero a dos aguas, una nave de 25,00 m de luz y 30,00 m de largo en
cinco marcos, con un puente grúa birriel de 200 kN sin cabina que corre sobre un riel a
7,50 m. Marcos de momento de alma variable en la dirección transversal, arriostramiento
concéntrico en dos de los cuatro vanos en la longitudinal, techo arriostrado. Zona sísmica 2,
suelo C, Categoría II. Diseñado por NCh2369:2025 con AISC 360-22, AISC 341-22, NCh431,
NCh3171, AIST TR-13 y CMAA 70 donde cada una manda.

La serie lo recorre en catorce eslabones, desde la clasificación de la norma hasta el anclaje,
y uno de ellos va al frente: **el modelo**, que corre el galpón entero y publica los períodos
con que todo lo demás debería haber empezado. Nació como una serie de memos en el repositorio
de guías y se mudó aquí, eslabón por eslabón, con el modelo tridimensional en pantalla en el
punto donde cada uno lo necesita. El modelo vive en [su ficha](../../modelos/galpon-grua/).

## Los eslabones

{{ tabla_serie('nch2369-galpon-grua') }}

El **13** es distinto de los otros trece: **no existía en el repositorio de memos** y se
escribió aquí, con el PDF de la norma abierto. Por eso es el único sin oráculo —no hay cifra
previa que reproducir— y lo que sostiene sus números es la cadena, la hoja de valores del
proyecto en Struct Harness y tres contrastes cruzados contra lo que el 11 y el 12 ya habían
publicado. Cierra los tres encargos que aquéllos le dejaron: la cota inferior de rigidez del
panel, el colector con la torsión adentro y la acumulación del Apéndice 6.

## La cadena

Cada arista es un símbolo que un eslabón publica y otro consume. El test del repositorio
verifica que lo que entra sea exactamente lo que salió: mismo valor, misma unidad, y que
cada origen sea anterior a su consumidor.

{{ grafo_serie('nch2369-galpon-grua') }}

## Dónde quedó

- **Migrados**: 00 a 12. Cada uno reproduce, a la precisión que el memo original publicó, las
  cifras de ese memo; un assert en su script lo garantiza, y desde el 07 el oráculo cubre además
  las filas del `## Resumen` y no solo las salidas. **Escrito aquí**: el 13.
- **El 13 le devuelve algo al 12, y todavía no se aplicó.** Al dimensionar la diagonal del
  panel, la rigidez `k_pan` se multiplica por 3,26 — y esa rigidez es una entrada del 12, de la
  que cuelgan su razón torsional y su colector. Es la primera vez que la serie deja de ser una
  cadena y se cierra sobre sí misma. Recorrer el 12 con el valor nuevo **mejoraría** la
  torsión, pero cambia cifras que su oráculo ata al memo original, así que va junto con la
  cascada y no por separado.
- **La cascada pendiente.** El 00 publica períodos que el 04 todavía no hereda: el 04 usa
  los declarados (0,20 y 0,40 s). Cuando los tome, cambiará de rama en Y y de ahí bajan R₁,
  el amplificador de capacidad, la componente vertical del 06, los M_pe del 07 y el anclaje
  del 13. Se aplica después de migrar la serie completa, como un cambio explícito.
- **Esfuerzos en pantalla.** Los eslabones 07 en adelante leen momentos y axiales en barras, y
  el visor ya los dibuja a lo largo de cada una. El 07 lo usa para mostrar que los tres números
  que declara —la rigidez del alero, la razón entre los dos momentos y el punto de inflexión—
  salen de un empuje en **un solo alero**, mientras la rigidez del riel del mismo memo sale del
  *sway*: dos convenciones distintas en la misma página.
