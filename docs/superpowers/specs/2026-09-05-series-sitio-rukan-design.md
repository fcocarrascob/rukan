# Plan — Las series en el sitio de Rukan: la cadena `nch2369-galpon-grua` narrada con el modelo en pantalla

## Contexto

El sitio de Rukan (`sitio/`, 2026-09-05) ya narra un modelo con su visor 3D y con las cifras
inyectadas desde la corrida. La serie de memos `nch2369-galpon-grua` del repo
`Guias_Interactivas` (trece eslabones escritos, 00 a 12; el 13 pendiente) diseña ese mismo
galpón con un régimen de cinco arneses: contrato del memo, aritmética re-evaluada, modelo
independiente en `.check.js`, cadena entre eslabones y citas contra el PDF de la norma.

Decisión del usuario (2026-09-05): **el sitio de Rukan pasa a ser la casa de la serie**. Se
migra todo su contenido, se deja de depender del repo de guías, y cada vez que un eslabón
involucre el modelo, un esfuerzo, una rigidez o una deformada, la página lo muestra sobre el
modelo OpenSees, como hoy se hace con modos y deformadas. El repo de guías queda como
referencia histórica; nada nuevo se escribe allá.

Lo que hay que preservar del régimen de memos, porque es lo que hace confiable a la serie:
que **cada cifra nazca en un paso o en un modelo**, que **lo que un eslabón hereda sea
exactamente lo que el anterior publicó**, y que **toda cita a la norma lleve página y frase**.
Lo que se reemplaza: el parser de LaTeX que re-evalúa la aritmética (las cifras ya no se
teclean, salen de un script), el `.check.js` como segundo camino (el oráculo de migración son
los valores publicados por el memo), y el índice generado a mano (lo genera un macro).

## Decisiones tomadas con el usuario (2026-09-05)

| Decisión | Elegido |
|---|---|
| Molde de cada eslabón | **Narración con ficha de contrato**: prosa con visores y fórmulas en el orden de los pasos; al final, la ficha (qué entra y de dónde, qué sale y de qué paso, límites, referencias). La cadena se verifica con un test |
| De dónde salen las cifras de los pasos | **Un `_calculo.py` por eslabón**, Python puro, que escribe `<slug>.valores.json`; la prosa las inyecta con macros. Un assert compara cada valor con el que publicó el memo original |
| Orden respecto de `escena@2` | **Andamiaje y eslabones 00–06 primero**, con el visor actual; después `escena@2` (esfuerzos por barra) y con ella los eslabones 07–12 |
| Cascada 04→13 | **Fidelidad primero**: cada eslabón reproduce las cifras publicadas; la cascada con los períodos del 00 se aplica después, como cambio explícito que el test de cadena delata |

Decisiones menores tomadas por mí, para no bloquear:

- **La malla del modelo es la del memo 00** (`nsub=16`, 965 nudos): la serie publica
  `T*_Y = 0,24878 s` con esa malla y la fidelidad manda. La escena crece a ~1,3 MB; se acepta.
  `modelos/galpon-grua` se regenera con esa malla y queda como la **ficha del modelo**; la
  narración larga que hoy tiene se muda al eslabón 00.
- **Fórmulas con KaTeX vendoreado** (`pymdownx.arithmatex` genérico), coma decimal dentro del
  LaTeX con `{,}` como en los memos. El grafo de la cadena se emite como bloque `mermaid` desde
  un macro (Material lo dibuja; es la única pieza que carga desde CDN).
- **Las figuras se portan**: los `_figuras-NN.py` de los memos son Python puro que escribe SVG
  a mano; se copian a cada eslabón y sus cotas `D` pasan a leerse de `valores.json`, así
  «ningún número nace en la capa de dibujo» deja de ser una regla y pasa a ser una consecuencia.
  Donde una figura mostraba el modelo (planta, marco, modos, deformadas), la reemplaza un visor.
- **Español neutro con «tú»**, como el resto del sitio; los memos son impersonales y se
  re-narran, no se copian.
- **La regla de verificar contra la fuente sigue en pie**: `_calculo.py` transcribe fórmulas
  que los memos ya leyeron del PDF y cuya cita textual con página se migra tal cual. Cualquier
  disposición **nueva** (el eslabón 13, la cascada) exige abrir el PDF rasterizado antes de
  escribir un número.

## Diseño

### 1. Estructura

```
sitio/
  serie.py                        # la librería de series: Eslabon, valores@1, cadena, citas
  main.py                         # macros: los de hoy + v, ficha, tabla_serie, grafo_serie
  docs/
    js/katex.js                   # renderMathInElement bajo document$ (Material)
    visor/vendor/katex/           # katex.min.js, auto-render, katex.min.css, fonts/ (VERSION)
    modelos/galpon-grua/          # la ficha del modelo (nsub=16): proyecto, resultados, escena
    series/
      index.md                    # qué es una serie en este sitio
      nch2369-galpon-grua/
        index.md                  # el caso, la cadena (tabla_serie + grafo_serie), dónde quedó
        _serie.py                 # declaración: id, título, orden de eslabones, modelo asociado
        00-el-modelo/
          index.md
          _calculo.py             # la cadena del eslabón → 00-el-modelo.valores.json
          00-el-modelo.valores.json
          _figuras.py, figs/*.svg (solo si al eslabón le quedan figuras que no sean el modelo)
        01-el-umbral-de-las-20-t/
        02-nieve-balanceada-y-desbalanceada/
        …
        12-los-dos-vanos-libres/
```

Cada eslabón es una carpeta `NN-<slug>` (el `NN` es el `orden`; el slug es el del memo sin
el prefijo `nch2369-galpon-grua-`). El visor de un eslabón apunta a la escena del modelo:
`<rukan-visor src="../../../modelos/galpon-grua/galpon-grua.escena.json" caso="H_alero">`.

### 2. El esquema `rukan/valores@1` y `sitio/serie.py`

`_calculo.py` no escribe JSON a mano: declara y calcula con `serie.py`.

```python
from serie import Eslabon                      # sitio/serie.py, vía sys.path
E = Eslabon("nch2369-galpon-grua", orden=4, slug="espectro-y-r-por-direccion",
            titulo="Espectro y R* por dirección", normas=["NCh2369:2025"])
A_r = E.caso("A_r", 0.42, "g")                                 # dato de proyecto
T_star_Y = E.entra("T_star_Y", de="00", paso="M1")             # lee 00-*.valores.json
f_xi = E.paso("B1", "f_xi", (0.05 / xi) ** 0.4, "—")           # un paso con nombre
E.sale("R_star_Y", R_star_Y, "—", paso="C5", heredan=["05", "06", "07", "12"])
E.publicado({"R_star_Y": 5.00000, "Sa_ref_Y": 1.21275, …})    # el oráculo: lo que el memo imprimió
E.escribir()                                                   # valida y escribe el JSON
```

- `entra()` **lee el JSON del eslabón de origen** (`sale[simbolo]`) y falla si no existe, si el
  símbolo no está o si el origen tiene `orden` mayor. La cadena no se copia: se consume.
- `entra(..., de="modelo:galpon-grua")` lee `modelos/galpon-grua/galpon-grua.resultados.json`
  (el `Mn` de los memos). La regla primaria/derivada se mantiene: `k_Y = H/δ` es un `paso()`.
- `publicado()` guarda el dict y `escribir()` **falla** si algún `sale` difiere del publicado
  en más de media unidad del último decimal impreso (la tolerancia de `verify_serie.js`).
  Cuando la cascada cambie un número, ese dict se edita a mano y el diff lo muestra.
- `escribir()` escribe `<NN-slug>.valores.json`:

```json
{"esquema": "rukan/valores@1", "serie": "nch2369-galpon-grua", "orden": 4,
 "slug": "espectro-y-r-por-direccion", "titulo": "…", "normas": ["NCh2369:2025"],
 "hereda_de": ["00", "01"],
 "entra": {"T_star_Y": {"valor": 0.24878, "unidad": "s", "de": "00", "paso": "M1"}},
 "caso":  {"A_r": {"valor": 0.42, "unidad": "g"}},
 "pasos": {"B1": {"f_xi": {"valor": 1.4427, "unidad": "—"}}},
 "sale":  {"R_star_Y": {"valor": 5.0, "unidad": "—", "paso": "C5", "heredan": ["05", "06", "07", "12"]}},
 "publicado": {"R_star_Y": 5.0, "…": 0},
 "generado": "…", "rukan": "0.1.0", "commit": "…"}
```

`serie.py` expone además lo que macros y tests necesitan: `cargar(raiz, serie, nn)`,
`eslabones(raiz, serie)` (ordenados), `verificar_cadena(raiz, serie) -> list[str]` (los diez
chequeos de `verify_serie.js` que siguen teniendo sentido: orden entero, sin repetidos y
contiguo desde el mínimo; `hereda_de` cubre `entra` y no declara de más; todo origen es
anterior; valor y unidad coinciden a media unidad del mínimo de decimales; reciprocidad de
`heredan`), `citas(raiz, serie, nn)` (parsea la tabla `## Referencias` de `index.md`).

### 3. Los macros nuevos (`sitio/main.py`)

- `v(eslabon, simbolo, cifras=None, factor=1, unidad=False)` — como `r()`, pero sobre
  `valores.json`; `eslabon` es `"nch2369-galpon-grua/04"`. Busca en `sale`, `pasos`, `entra` y
  `caso`, en ese orden; símbolo inexistente rompe el build nombrándolo.
- `ficha(eslabon)` — la ficha de contrato al final de la página: tabla **Entra** (símbolo,
  valor, unidad, de qué eslabón y paso, con enlace), tabla **Sale** (símbolo, valor, unidad,
  paso, quién lo hereda, con enlace) y la línea de procedencia del JSON.
- `tabla_serie(serie)` — la tabla de eslabones del índice de la serie (orden, título con
  enlace, normas, cuántas salidas), desde los JSON.
- `grafo_serie(serie)` — el bloque `mermaid` del grafo de herencias con hasta tres símbolos por
  arista, como `verify_serie.js --mermaid`.
- `figura(eslabon, nombre, alt)` — inserta `figs/<nombre>.svg` y comprueba que exista.

### 4. La página de un eslabón (`index.md`)

Molde, en este orden:

1. **Título** (la tesis del memo, en una frase) y el párrafo de qué decide.
2. **El caso**: tabla `Dato | Valor` con lo que el eslabón fija, más un visor o figura si hay
   geometría. Los supuestos, como lista `S1…Sn` en prosa breve.
3. **La narración por bloques** (A, B, C… del memo), cada paso con su titular, la fórmula con
   símbolos = sustitución = resultado (los números por `v()`), la conclusión con `→`, y **el
   visor en el punto donde entra el modelo**: la deformada del caso, el modo, o el tooltip de
   la barra cuyo esfuerzo se está leyendo. Donde hoy no hay esfuerzos dibujables, se remite a
   `escena@2` sin inventar.
4. **Veredicto** y **Límites**.
5. **Ficha**: `{{ ficha('nch2369-galpon-grua/04') }}`.
6. **Referencias**: la tabla de cinco columnas del memo (`Clave | Norma | Cláusula | Leída en |
   Cita textual`) migrada **tal cual**, con página y frase.

### 5. Tests (`tests/test_series.py`)

Por cada eslabón de cada serie en `sitio/docs/series/`:

- (a) `_calculo.py` corrido a un directorio temporal produce un dict **igual** al
  `valores.json` versionado (la atadura, como con `_generar.py`).
- (b) `publicado` coincide con `sale` a media unidad del último decimal (redundante con el
  assert del script, pero lo corre pytest).
- (c) `verificar_cadena()` devuelve lista vacía para la serie.
- (d) **Publicación efectiva**: todo símbolo de `sale` aparece en `index.md` dentro de un
  `v(`; y toda cifra ≥ 10 en un `<text>` de `figs/*.svg` existe entre los valores del eslabón
  (la capa 2b, en Python).
- (e) La tabla `## Referencias` parsea y toda fila de nivel «fuente» trae PDF, página y cita
  de al menos 12 caracteres útiles.
- (f) `mkdocs build --strict` (ya existe).

`tests/test_citas.py` (paso posterior): la frase de cada cita está en la página declarada del
PDF, con `canon()` como en `verify_cita.py`; `pytest.skip` si no hay `fitz` o no está
`F:/OneDrive/Ingenieria/Normas`. Grupo opcional `citas = ["pymupdf"]` en `pyproject`.

### 6. El pipeline de un eslabón (se repite trece veces)

1. Leer el memo y su `.check.js`; anotar las salidas publicadas (`## Sale`) y las del
   `## Resumen` que la prosa cita.
2. Escribir `_calculo.py` con `Eslabon`: `caso()`, `entra()`, los pasos en el orden del memo,
   `sale()`, `publicado()`. Correr; si algún valor no reproduce el publicado, la diferencia es
   un hallazgo y se resuelve leyendo el memo (o el PDF), nunca ajustando el oráculo.
3. Portar `_figuras-NN.py` → `_figuras.py` con `D = cotas(valores)`; descartar las figuras que
   un visor reemplaza. Correr; mirar los SVG (Chrome vía puppeteer, como el visor).
4. Escribir `index.md` con el molde del § 4; los visores donde entra el modelo.
5. `mkdocs build --strict`, `pytest tests/test_series.py`, captura de la página.
6. Actualizar `_serie.py` y el `index.md` de la serie; commit «Serie galpón grúa: eslabón NN».

### 7. Lotes

- **Lote A — andamiaje + 00 + 01** (este plan, primera parte). `serie.py` + tests con un
  fixture de dos eslabones sintéticos; KaTeX; macros; `modelos/galpon-grua` a `nsub=16`;
  `series/index.md`; `series/nch2369-galpon-grua/index.md`; eslabón **00** (el modelo: modos,
  los dos empujes, `k_Y` y `k_riel` como pasos, oráculo = memo 00) y eslabón **01** (el umbral
  de las 20 t: las ocho letras de §12.2.1, la fila de la Tabla 7, R, ξ; sin modelo, es la raíz
  de la cadena). Con estos dos queda probado el molde en sus dos extremos.
- **Lote B — 02 a 06** (este plan, segunda parte), uno por commit, con el pipeline del § 6.
  Visores que entran: 05 (masa sísmica: los nudos con masa y el modo dominante), 06 (derivas:
  deformada de `H_alero` con la escala del sismo escrita como paso).
- **Lote C — `escena@2`**: esfuerzos a lo largo de la barra (superposición de la carga
  distribuida sobre las fuerzas de extremo, la maquinaria de `lab/nota01`), verificados contra
  numpy y SAP2000; color y diagramas N/V/M en el visor. **Spec aparte.**
- **Lote D — 07 a 12**: marco (07: momento en la base, punto de inflexión, rigidez), carrilera
  (08, 09: esfuerzos de la viga bajo las tres posiciones de rueda), columna escalonada (10),
  techo arriostrado (11: axiales de las diagonales), torsión en planta (12: el caso con la grúa
  en el tope, que pide un caso nuevo en el proyecto: `x_grua = X_G_TOPE`).
- **Lote E — el eslabón 13** (nuevo: diagonales longitudinales y anclaje, §8.6 y §8.5.2), con
  el PDF abierto. **Lote F — la cascada** 04→13 con los períodos del 00.

## Orden de implementación del lote A (TDD, un commit por paso)

1. **Spec**: copiar este plan a `docs/superpowers/specs/2026-09-05-series-sitio-rukan-design.md`.
2. **`sitio/serie.py`** + `tests/test_series.py` sobre un fixture sintético (dos eslabones en
   `tmp_path`): `Eslabon` escribe el esquema; `entra` lee del origen y falla con el símbolo;
   `publicado` atrapa una desviación de una unidad del último decimal; `verificar_cadena`
   detecta orden repetido, origen posterior, unidad distinta, herencia no recíproca.
3. **Macros** `v`, `ficha`, `tabla_serie`, `grafo_serie`, `figura` en `main.py`, con tests
   sobre el mismo fixture. KaTeX vendoreado (`vendor/katex/VERSION`), `js/katex.js`,
   `pymdownx.arithmatex` y `pymdownx.superfences` (mermaid) en `mkdocs.yml`; una fórmula de
   prueba en una página y captura para verla renderizada.
4. **El modelo a `nsub=16`**: `_generar.py` con `NSUB = 16`, regenerar proyecto, resultados y
   escena; `modelos/galpon-grua/index.md` se reduce a la ficha del modelo (qué es, visor,
   procedencia, cómo regenerar) y el resto de su narración pasa al 00. Comprobar
   `T_star_Y = 0,24878` y `T_star_X = 0,20602` como publica el memo.
5. **Eslabón 00**: `_calculo.py` (entra de `modelo:galpon-grua`; pasos B1 `k_Y = H/δ`, B2
   `k_riel`; D1/D2 los osciladores de 1 GDL como bandas; `sale` las diez filas del memo;
   `publicado` con sus valores), `index.md` con los visores de modos y empujes, ficha,
   referencias. `_serie.py` y el `index.md` de la serie con `tabla_serie` y `grafo_serie`.
6. **Eslabón 01**: `_calculo.py` (las ocho letras de §12.2.1 como predicados con su valor,
   Tabla 7, R = 5, ξ = 0,02, el amplificador; once salidas), figuras portadas (planta con
   portones, sección), `index.md`.
7. **Docs**: `CLAUDE.md` (sección «Las series»), `ROADMAP.md`, `sitio/docs/index.md` (qué es
   una serie), `README.md`. Lote B sigue con el pipeline del § 6, un eslabón por commit.

## Verificación

- `pytest` en verde, incluidos `test_series` y `test_sitio`.
- `python sitio/docs/series/nch2369-galpon-grua/04-*/_calculo.py` imprime cada `sale` con
  su valor publicado al lado y termina en 0; cambiar un dígito de `publicado` lo hace fallar.
- Prueba de cadena: editar el valor de una salida del 01 sin recorrer el 02 → `test_series`
  falla nombrando el símbolo, el origen y el consumidor.
- `mkdocs build --strict -f sitio/mkdocs.yml` en 0; en el navegador: las fórmulas se ven con
  KaTeX y coma decimal, el grafo de la serie se dibuja, la ficha del 00 enlaza al 04 y el
  visor del 00 muestra `T = 0,2488 s` en el modo 1 (la malla del memo).
- Captura de cada página nueva con `captura.mjs` (puppeteer-core) y mirarla.
- Al cerrar el lote B: `verificar_cadena` en vacío para 00–06 y cada `publicado` igual al memo.

## Fuera de alcance de este plan

- `escena@2` (lote C), los eslabones 07–13 (lotes D y E) y la cascada (lote F): cada uno con
  su spec o su sesión, sobre este andamiaje.
- Un segundo camino independiente por eslabón (el `.check.js`): el oráculo de migración lo
  reemplaza mientras las cifras sean las publicadas; para la cascada se decidirá si un paso
  crítico (el R* de la Ec. 1b) merece una banda de sensatez en el test.
- Tocar el repo de guías: no se edita; su serie queda congelada como referencia.

## Riesgos

- **Fidelidad numérica**: un memo puede haber redondeado en un paso intermedio; el oráculo
  compara a media unidad del último decimal impreso, que es lo que el memo prometió. Si un
  valor no reproduce, se investiga antes de seguir; no se afloja la tolerancia.
- **Tamaño de la escena** con 965 nudos (~1,3 MB): si pesa en la carga, bajar `CIFRAS` a 5
  para `phi` y `u`.
- **KaTeX y `{,}`**: la coma decimal dentro de LaTeX se escribe `0{,}24878`; un test busca
  `\d\.\d` dentro de `$$…$$` en cada `index.md` y falla (la regla 6 del repo de memos).
- **Volumen**: trece eslabones de 400 a 1 000 líneas. El pipeline del § 6 está pensado para
  avanzar de a uno y dejar cada uno publicable; no se migran dos a medias.
