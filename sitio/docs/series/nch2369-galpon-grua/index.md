# El galpón con puente grúa

Un galpón industrial de acero a dos aguas, una nave de 25,00 m de luz y 30,00 m de largo en
cinco marcos, con un puente grúa birriel de 200 kN sin cabina que corre sobre un riel a
7,50 m. Marcos de momento de alma variable en la dirección transversal, arriostramiento
concéntrico en dos de los cuatro vanos en la longitudinal, techo arriostrado. Zona sísmica 2,
suelo C, Categoría II. Diseñado por NCh2369:2025 con AISC 360-22, AISC 341-22, NCh431,
NCh3171, AIST TR-13 y CMAA 70 donde cada una manda.

La serie lo recorre en trece eslabones, desde la clasificación de la norma hasta el
arriostramiento de techo, y uno más al frente: **el modelo**, que corre el galpón entero y
publica los períodos con que todo lo demás debería haber empezado. Nació como una serie de
memos en el repositorio de guías y se muda aquí, eslabón por eslabón, con el modelo
tridimensional en pantalla en el punto donde cada uno lo necesita. El modelo vive en
[su ficha](../../modelos/galpon-grua/).

## Los eslabones

{{ tabla_serie('nch2369-galpon-grua') }}

Los que faltan, en el orden en que se migran: 07 el marco de momento a dos aguas, 08 la viga
carrilera, 09 su fatiga, 10 la columna escalonada y el apoyo de la carrilera, 11 el
arriostramiento continuo de techo, 12 los dos vanos libres, y 13 diagonales longitudinales y
anclaje, que todavía no se ha escrito.

## La cadena

Cada arista es un símbolo que un eslabón publica y otro consume. El test del repositorio
verifica que lo que entra sea exactamente lo que salió: mismo valor, misma unidad, y que
cada origen sea anterior a su consumidor.

{{ grafo_serie('nch2369-galpon-grua') }}

## Dónde quedó

- **Migrados**: 00 a 06, el lote completo del andamiaje. Cada uno reproduce, a la precisión que el memo original publicó,
  las cifras de ese memo; un assert en su script lo garantiza.
- **La cascada pendiente.** El 00 publica períodos que el 04 todavía no hereda: el 04 usa
  los declarados (0,20 y 0,40 s). Cuando los tome, cambiará de rama en Y y de ahí bajan R₁,
  el amplificador de capacidad, la componente vertical del 06, los M_pe del 07 y el anclaje
  del 13. Se aplica después de migrar la serie completa, como un cambio explícito.
- **Esfuerzos en pantalla.** Los eslabones 07 en adelante leen momentos y axiales en barras;
  el visor los mostrará sobre el modelo cuando exista la segunda versión de la escena, con
  los esfuerzos a lo largo de cada barra verificados.
