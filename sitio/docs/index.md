# Rukan, los modelos

Este sitio es el repositorio de modelos de [Rukan](https://github.com/fcocarrascob/rukan),
un motor de análisis estructural opensource sobre OpenSeesPy. Cada entrada es **un modelo
que se puede correr**: su archivo de proyecto, la corrida que lo acompaña y la escena en
3D que sale de esa corrida. Lo que se dibuja y lo que se escribe salen del mismo archivo.

## Modelos y series

Hay dos clases de entrada. Un **modelo** es una estructura que se corre: su archivo de
proyecto, su corrida y su escena, con el visor al frente. Una **serie** es una cadena de
eslabones que diseñan la misma estructura, cada uno con una pregunta y una decisión, con el
modelo en pantalla en el punto donde cada eslabón lo necesita. [Qué es una serie](series/).

## Qué narra y qué no

Narra **el modelo y lo que el motor hace con él**: qué se idealizó, cuántos nudos y barras
tiene y por qué, cómo se mueve en cada modo, qué deformada deja cada caso de carga, y de
dónde sale cada número. Y en las series, **el diseño que se apoya en ese modelo**, paso a
paso, con cada cláusula citada por página y frase.

Una cosa queda fuera a propósito: la **verificación del motor** contra SAP2000 vive en
[struct_pad](https://fcocarrascob.github.io), como serie numerada.

## Cómo se lee una entrada

Cada modelo trae un visor incrustado. Se orbita con el ratón, se elige una vista fija
(planta, elevaciones, isométrica), un modo o un caso de carga, y una escala para la
deformada. Al pasar el cursor por un nudo o una barra aparecen su nombre y sus valores en
el caso activo. Es un reticulado de líneas, sin sombreado ni eliminación de líneas
ocultas: en una estructura de barras eso se lee mejor que lo contrario.

Las cifras del texto no se escriben a mano. Salen del archivo de resultados de la corrida
al construir el sitio, y cada entrada cierra con su procedencia: versión de Rukan, commit,
versión de OpenSeesPy y el hash del proyecto. Si el modelo cambia y no se vuelve a correr,
el sitio no se construye.

## Regenerar una entrada

```bash
python sitio/docs/modelos/<modelo>/_generar.py     # escribe <modelo>.proyecto.json
python -m rukan run    sitio/docs/modelos/<modelo>/<modelo>.proyecto.json
python -m rukan escena sitio/docs/modelos/<modelo>/<modelo>.proyecto.json
mkdocs serve -f sitio/mkdocs.yml
```
