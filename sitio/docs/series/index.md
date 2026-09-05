# Las series

Una serie es una cadena de eslabones que diseñan la misma estructura, cada uno con una
pregunta y una decisión. El primero fija el caso; cada uno de los siguientes toma lo que los
anteriores publicaron, hace su cálculo y publica lo suyo. Cuando un eslabón involucra el
modelo, un esfuerzo, una rigidez o una deformada, la página lo muestra sobre el modelo
OpenSees, en el punto exacto de la narración donde entra.

## El contrato

Tres cosas hacen confiable a una serie, y las tres se verifican con un test, no a ojo.

**Cada cifra nace en un paso o en un modelo.** Ningún número de la prosa se teclea: sale del
script de cálculo del eslabón, que declara qué es dato del caso, qué entra de otro eslabón,
qué se calcula en cada paso y qué se publica. Un paso se escribe como símbolos, sustitución
y resultado, y el resultado es el que el script produjo:

$$k_{Y} = \frac{H_{marco}}{\delta_{alero}} = \frac{1\,000}{0{,}0664559} = 15\,047{,}57290\ \text{kN/m}$$

**Lo que un eslabón hereda es exactamente lo que el anterior publicó.** El script del eslabón
que consume lee el archivo de valores del que produce; no lo copia. Si el origen cambia y el
consumidor no se vuelve a correr, la cadena no cierra y el sitio no se construye.

**Toda cita a la norma lleva página y frase.** La tabla de referencias de cada eslabón dice
en qué PDF y en qué página se leyó cada cláusula, y cita la frase textual.

Al final de cada eslabón va su ficha de contrato: qué entró y de dónde, qué sale y en qué
paso nace, y quién lo hereda.

## Las series publicadas

- [El galpón con puente grúa (NCh2369)](nch2369-galpon-grua/) — trece eslabones que diseñan
  un galpón industrial de acero con puente grúa, desde la clasificación de la norma hasta el
  arriostramiento de techo, con el modelo tridimensional corriendo al frente.
