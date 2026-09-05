# Plan — lote D: los eslabones 07 a 12 de `nch2369-galpon-grua` en el sitio

## Contexto

Los lotes A y B migraron los eslabones 00 a 06 al sitio y `verificar_cadena` cierra. El lote C
cerró `escena@2`: el visor dibuja los esfuerzos a lo largo de la barra y existe la sonda
`esfuerzo` con `x`/`x_rel`. Falta el lote D: los seis eslabones que quedan escritos en el repo
de memos (07 marco de momento a dos aguas, 08 viga carrilera, 09 su fatiga, 10 columna
escalonada, 11 arriostramiento de techo, 12 los dos vanos libres).

El spec del lote C anunció el bloqueo: «el proyecto no tiene todavía ningún caso de grúa, de
nieve ni de sismo estático». **Al leer los seis memos, ese bloqueo resultó ser otro.** Ninguna
cifra publicada por 07–12 sale de una corrida:

| | De dónde nacen sus cifras |
|---|---|
| **07** | `k_Y`, `k_riel` y `Mbase_u` nacen en **S1**: son valores *declarados* de un modelo plano de rigidez directa con 42 segmentos prismáticos por miembro y bases empotradas, que «este memo describe y no ejecuta». Con ellos vienen declarados `M_nudo`, `M_cumbrera`, el punto de inflexión `y_infl = 7,74863 m`, la razón sway 2,81628, las dos flechas de cumbrera y la apertura de trocha. `Rcol_grua = 193,48696·(1+(7,5−3,4)/7,5)` y `Nbase_u = 251,63775 + 299,25983` son aritmética sobre el `Rv_max` del 03 |
| **08** | `M_ux = 246,70861·2,90 − 1,94714·2,90²/2` sobre un vano simple de 7,50 m; el resto, propiedades de sección |
| **09** | rangos de tensión `M/S` sobre la sección del 08 |
| **10** | sección compuesta y el ábaco `a_r`/`B` del Comentario AIST 5.9.1 |
| **11** | `k_pan = 2EA·b²/L³` y un reparto entre cinco marcos en forma cerrada |
| **12** | `δmáx/δprom = 1 + 75,00·2,88308/(562,50 + 625,00·ρ)`, cerrada. «Modelo tridimensional» ahí significa *que la rigidez torsional incluya los paneles longitudinales*, no una corrida |

Así que los casos nuevos no sirven a la **fidelidad**: sirven al **contraste**, que es la
identidad declarada del sitio («narra el modelo y lo que el motor hace con él»). Eso cambia qué
se agrega y por qué, y lo reduce a tres casos nodales que no tocan el esquema.

## Decisiones tomadas con el usuario (2026-09-06)

| Decisión | Elegido |
|---|---|
| Casos nuevos en el galpón | **Los tres de contraste**: `H_long`, `H_riel_uno`, `E_Y_tope`. **Sin nieve** — ningún eslabón 07–12 lee un resultado de nieve |
| El sismo | **Estático equivalente**, con las masas que el modelo ya tiene. `analisis.espectral` sigue siendo v2 |
| La viga carrilera del 08/09 | **Entrada nueva `sitio/docs/modelos/carrilera/`**: viga de 7,50 m con las dos ruedas. Estrena `combinaciones`, hoy vacío en todo el repo |
| La sonda `esfuerzo_extremo` | **No entra.** Ningún símbolo de las seis tablas `## Sale` es un máximo sobre un conjunto; rompe dos invariantes del runner (el máximo no es lineal, y devuelve tres cosas donde `salidas` devuelve un float). Queda encolada junto a `espectral` |
| Documentación | **Un solo spec**: `docs/superpowers/specs/2026-09-06-lote-d-eslabones-07-12-design.md` |

Decisiones menores tomadas por mí, para no bloquear:

- **Los tres casos nuevos son empujes unitarios de 1 000 kN**, como los tres que ya existen. Las
  magnitudes de diseño (`Q0_Y`, `F_diaf_X`) las pone la página como un `paso()` que escala, no el
  modelo. Así el modelo emite magnitudes primarias y ninguna decisión de nivel de diseño queda
  enterrada en el JSON. `δmáx/δprom` y las fracciones de reparto son invariantes de escala.
- **El orden es 07→12 y no hay alternativa**: `verificar_cadena` exige `orden` contiguo desde el
  mínimo, así que migrar el 08 sin el 07 rompe la serie entera.
- **El lote D no hereda del 00** (fidelidad primero): usa lo que el memo original usó
  (`T_star_Y = 0,40 s` del 04). La cascada es el lote F.

---

## 1 · Tres casos nuevos en `modelos/galpon-grua`

Todos son `nodales`; **ninguno toca `io.py`, `analysis.py` ni `loads.py`**. Se agregan en
`sitio/docs/modelos/galpon-grua/_generar.py`.

| Caso | Qué es | A quién sirve |
|---|---|---|
| `H_long` | 100 kN en **+X** en los diez nudos de alero (`R{1..5}_0`, `R{1..5}_6`) | **11**: los axiales de las diagonales de techo (`DTA*`, `DTB*`) y el arrastre del puntal de alero como colector, contra el `N_diag = 47,33782 kN` y el `F_col_alero = 164,74784 kN` de su D1 |
| `H_riel_uno` | 500 kN en **+Y** en los dos nudos de riel del marco 3 (`K3A_32`, `K3B_32`) | **11**: `f_marco_grua = 0,21408`, la fracción que el marco cargado retiene. Con `H_riel` (los diez nudos) forman las dos cotas de la banda que el 07 · C3 dejó abierta —el diafragma rígido de 51 522,74517 kN/m contra el marco solo— y que el 11 · D2 cierra en 0,93897 mm |
| `E_Y_tope` | 1 000 kN en **+Y** repartidos como la masa sísmica, con la cuota de la grúa (230/1 037,085 = 22,18 %) puesta en los nudos de riel de los marcos que un puente en `x_g_tope = 2,00 m` carga, y el resto proporcional a `model.masses` | **12**: `δmáx/δprom` medido sobre la línea de aleros, contra el `raz_tors_Y = 1,11962` de su forma cerrada |

Notas de implementación:

- `case11_data.X_G_TOPE = 2.0` ya existe (`verification/case11_data.py:79`) y hoy solo afecta a
  `masas()`. El símbolo que el 12 publica es **`x_g_tope`**, y nace en su **S3**: `3,40/2 + 0,30`,
  la mitad de la base de ruedas más el tope y la holgura. El reparto de `E_Y_tope` lo escribe
  `_generar.py` y **se declara en la página como supuesto**: con carrileras simplemente apoyadas
  por vano (07 · S4), un puente con ruedas a 0,30 y 3,70 m descarga sobre los marcos 1 y 2. Ese
  reparto es una decisión de Rukan que ningún memo tomó, y no se ajusta para acercarse a 1,11962.
- Sondas nuevas en `salidas` (todas con vocabulario existente): `d_alero_1..5` bajo `E_Y_tope`
  (`desplazamiento`, `Uy`, en `R{f}_0`), `d_riel_uno` bajo `H_riel_uno`, `N_dta` bajo `H_long`
  (`esfuerzo`, `N`, `x_rel: 0.5` sobre una diagonal de techo), `N_pun` sobre un puntal de alero,
  y `Mbase_u` bajo `H_alero_uno` (`esfuerzo`, `Mz`, `x_rel: 0.0` en `COL3A_1`) — que es lo que el
  07 declara en su S1 y hoy nadie mide.
- Los ganchos `Mz_raf3` y `N_col3` ya existen en `resultados.json` y nadie los consume: son del 07.
- **Costo**: `escena.armar` corre y emite *todos* los casos. Tres más → la escena pasa de 1,55 a
  ~2,3 MB. Se acepta; si molesta, la salida es bajar `CIFRAS` a 5 para `u` y `fuerzas`.

## 2 · Un modelo nuevo: `sitio/docs/modelos/carrilera`

Viga carrilera del 08, simplemente apoyada sobre un vano de `s_marco = 7,50 m`.

- **Geometría**: cuatro nudos (0 · 2,90 · 6,30 · 7,50) y tres barras. Las dos posiciones de rueda
  del 08 · D1 son nudos, así que las cargas son `nodales` y la fórmula de `esfuerzos.py` —que solo
  admite carga de vano **uniforme**— vale exacta en cada barra. No hace falta mallar: el diagrama
  es analítico, y decirlo es parte de lo que la página enseña.
- **Sección**: `case11_data.carrilera_props()` (`verification/case11_data.py:198`), que hoy está
  escrita y sin usar. `Iz` es la inercia fuerte y `vecxz` se elige para que el eje local **y** sea
  vertical, de modo que el momento de la carga vertical sea `Mz` — como lo llama el memo (`M_ux`).
  Un test lo fija.
- **Densidad**: el `w_carril = 1,62262 kN/m` del memo es la viga **más el riel** ASCE 85 lb/yd; el
  peso propio de la sección sola da 1,2087. Se usa un material con `rho` equivalente tal que
  `rho·A·g = w_carril`, declarado en `_generar.py` y en la página como supuesto. No es la densidad
  del acero y no se disimula.
- **Casos y combinación**: `Rueda` (dos nodales de `RV_MAX = 193,48696 kN` hacia −Z) y `D`
  (peso propio distribuido); combinación `U = {D: 1.2, Rueda: 1.6}`, la de NCh3171 §9.1.1 que el
  memo usa. **Es la primera combinación del repo**: el esquema, el runner y la escena ya la
  soportan enteros y nadie la había ejercido.
- **Salidas**: `M_ux` (`esfuerzo`, `Mz`, `x: 2.90`, caso `U`), `M_serv` (lo mismo bajo una
  combinación de servicio), `d_centro` (`desplazamiento`, `Uz`), reacciones.
- **Hallazgo esperado y previsto**: el modelo dará `M_ux ≈ 707,270` contra los 707,26725 que el
  memo imprime, porque el memo sustituye el coeficiente **impreso** `0,77333` y no `5,8/7,5`.
  `M_ux` no está en el `## Sale` del 08 —es una entrada de su `## La cadena`, un `paso()`—, así que
  el oráculo no lo ata: el `_calculo.py` reproduce la aritmética del memo con la cifra impresa y el
  modelo aparece al lado como **segundo camino independiente**, con la diferencia dicha.
- Pesa ~30 KB de escena, no ~250.

Archivos: `sitio/docs/modelos/carrilera/_generar.py`, `carrilera.proyecto.json`,
`carrilera.resultados.json`, `carrilera.escena.json`, `index.md`; entrada en `sitio/mkdocs.yml`.
`tests/test_sitio.py` la descubre sola (`_modelos()` recorre `docs/modelos/*`).

## 3 · Qué entra en cada eslabón

La columna «`entra`» separa los que **la reciprocidad ya obliga** (prometidos por los eslabones
00–06, ya migrados) del total de la tabla `## Entra` del memo, que incluye los que vienen de
eslabones del propio lote.

| NN | `entra` obligados / totales | Visor | Contraste del motor |
|---|---:|---|---|
| **07** marco de momento a dos aguas | **43** / 43 | sí, dos | `Mbase_u` y el momento de la columna bajo `H_alero_uno`, con el **punto de inflexión** en 7,74863 m visible en el diagrama — la carta de `escena@2`. Y `k_Y`/`k_riel` declarados en S1 contra `d_alero_uno`/`d_riel`, que es el hallazgo del caso 11 puesto en su eslabón: el 00 ya midió 6 152,89 kN/m con el empuje en un alero contra los 5 612,12 del memo |
| **08** viga carrilera | **16** / 19 (+07) | sí, `modelos/carrilera` | `M_ux` por el modelo contra la aritmética del memo |
| **09** fatiga de la carrilera | **10** / 27 (+08) | reutiliza el de la carrilera | ninguno nuevo: son rangos `M/S` sobre la misma sección. Figuras portadas |
| **10** columna escalonada | **15** / ~30 (+07, 08, 09) | sí, `filtro="COL3A_*"` | el escalón está en el modelo (`escalonada=True`): se ve el cambio de sección y el axial/momento a lo largo. `k_esc` se cita publicado; medirlo pediría un segundo modelo sin escalón y queda fuera |
| **11** arriostramiento de techo | **12** / 26 (+07, 10) | sí, `H_long` con `esfuerzo="N"` sobre todo el techo | los axiales de `DTA*`/`DTB*` y el arrastre del puntal contra el reparto cerrado de D1; y `f_marco_grua` con el par `H_riel` / `H_riel_uno` |
| **12** los dos vanos libres | **34** / 51 (+07, 10, 11) | sí, `E_Y_tope` | `δmáx/δprom` medido contra el 1,11962 cerrado. **El modelo tiene diafragma flexible y la fórmula lo supone rígido: una diferencia es el hallazgo, no un error**, y así se narra |

## 4 · Las restricciones del andamiaje que gobiernan cada commit

Son duras y ya están codificadas en `sitio/serie.py` y `tests/test_series.py`:

1. **Reciprocidad.** En cuanto exista `sitio/docs/series/nch2369-galpon-grua/07-…/07-….valores.json`,
   los 43 símbolos que los eslabones 00–06 le prometen con `heredan` pasan a ser **obligación**:
   cada uno tiene que aparecer como `E.entra(simbolo, de="NN")` con ese origen exacto, o
   `test_la_serie_publicada_cierra` falla nombrándolo (`serie.py:322-328`). Igual para 08 (16),
   09 (10), 10 (15), 11 (12) y 12 (34). Si un símbolo prometido no se usa, se declara el `entra`
   igual; el escape opuesto —un valor que el productor **no** prometió— es `E.caso(...)` con el
   comentario `# del 0X, SN`, como hacen el 05 y el 06.
2. **Contigüidad**: `orden` entero, sin repetir, contiguo desde el mínimo. 07→12 secuencial.
   Y la **unidad se compara como string**: el 03 publica `vida_grua` en `"años"` y `N_ciclos` en
   `"ciclos"`; se copian exactas o `verificar_cadena` las delata.
3. **La cifra impresa es la regla, no la excepción.** Cuando un paso no reproduce el `publicado`,
   se prueba primero con el valor redondeado a los decimales que el eslabón origen imprimió
   (patrón `_pub` / `_p` / `r5` del 05 y el 06; el `r5` del 06 redondea **medio hacia arriba**,
   `math.floor(x*1e5+0.5)/1e5`). Si aun así no reproduce, es un **hallazgo** y va a los
   `## Límites` de su página. No se afloja la tolerancia.
4. **Publicación efectiva**: todo `sale` citado en `index.md` con `v('serie/NN','simbolo'` o `vt(`,
   comillas **simples**. Ningún `\d\.\d` dentro de `$$…$$` fuera de `\text{}`. Toda cifra ≥ 10 en un
   `<text>` de un SVG existe entre los valores del eslabón.
5. **Referencias literales**: la tabla de cinco columnas del memo, celda por celda, con PDF entre
   backticks, `p. N` y cita entre `«»` de ≥ 12 caracteres canónicos en las filas de nivel `fuente`.
6. **Regenerar el modelo** obliga a los tres comandos (`_generar.py`, `python -m rukan run`,
   `python -m rukan escena`) porque el SHA-256 del proyecto viaja dentro de resultados y escena, y
   `procedencia()` rompe el build si no cuadra.

## 5 · Orden de implementación (un commit por paso)

1. **Spec** — copiar este plan a `docs/superpowers/specs/2026-09-06-lote-d-eslabones-07-12-design.md`.
2. **Los tres casos del galpón** — `sitio/docs/modelos/galpon-grua/_generar.py` con `H_long`,
   `H_riel_uno`, `E_Y_tope` y las sondas nuevas; regenerar proyecto + resultados + escena;
   actualizar `modelos/galpon-grua/index.md` (la sección «Los casos de carga» y la frase de
   `## Límites` que hoy dice que el modelo no tiene casos de grúa ni de sismo). `pytest` +
   `mkdocs build --strict` + captura mirada.
3. **`modelos/carrilera`** — `_generar.py`, los tres JSON, `index.md`, entrada en `mkdocs.yml`.
   Test propio: `M_ux` del modelo contra `R·x − w·x²/2` evaluado a mano, y el `vecxz` que pone la
   flexión fuerte en `Mz`.
4. **Eslabón 07** — el más grande (43 `entra`, 24 `sale`, 953 líneas de memo). `_calculo.py`,
   `_figuras.py`, `index.md` con los dos visores, ficha, referencias literales.
5. **Eslabón 08** — con el visor de la carrilera y el contraste de `M_ux`.
6. **Eslabón 09** — sin modelo nuevo; figuras portadas.
7. **Eslabón 10** — visor con `filtro="COL3A_*"`.
8. **Eslabón 11** — visor de `H_long` con `esfuerzo="N"`.
9. **Eslabón 12** — visor de `E_Y_tope` y el contraste de `δmáx/δprom`.
10. **Docs** — `CLAUDE.md` (estado, la serie completa migrada), `ROADMAP.md` (lote D cerrado,
    lotes E y F pendientes), `sitio/docs/series/nch2369-galpon-grua/index.md` (el párrafo «Los que
    faltan» y «Dónde quedó»), `sitio/mkdocs.yml` (`nav` hasta el 12).

Cada eslabón (4–9) sigue el pipeline del § 6 del spec de series: leer el memo y su `.check.js` →
`_calculo.py` con `publicado` → `_figuras.py` con `cotas()` → `index.md` con el molde → build
estricto y captura → commit «Serie galpón grúa: eslabón NN».

## 6 · Verificación

- `pytest` en verde antes de **cada** commit, con `test_series.py`, `test_sitio.py`, `test_io.py`,
  `test_analysis.py` y `test_escena.py`.
- `mkdocs build --strict -f sitio/mkdocs.yml` en 0.
- Cada `_calculo.py` corrido a mano imprime cada `sale` con el valor del memo al lado y termina en
  0; cambiar un dígito de `publicado` lo hace fallar nombrando el símbolo.
- `serie.verificar_cadena(SITIO, "nch2369-galpon-grua") == []` tras cada eslabón — es lo que
  atrapa un `heredan` prometido y no declarado.
- `python -m rukan run` y `python -m rukan escena` sobre los dos proyectos; el `sha256_proyecto`
  cuadra en los seis JSON.
- **La página mirada de verdad en el navegador**, no solo generada: servir `sitio/_build` con
  `python -m http.server 8765` y capturar con `puppeteer-core` sobre el Chrome instalado, sin el
  prefijo `/rukan/` y pasando la URL completa (memoria `sitio-rukan-verificacion-visual`).
- Prueba negativa al cerrar: borrar un `E.entra` del 12 y comprobar que `test_series` falla
  nombrando el símbolo, su origen y el consumidor.

## 7 · Fuera de alcance

- **`analisis.espectral`** (T*/R* por dirección, CQC, 100/30): sigue siendo el esquema v2. El caso
  sísmico del lote D es estático equivalente, que es el método que los memos usan.
- **La sonda `esfuerzo_extremo`**: encolada, con el porqué escrito arriba.
- **Cargas distribuidas declarables** (nieve, viento): el esquema cierra las claves de un caso a
  `peso_propio` y `nodales`, y ningún eslabón 07–12 lee un resultado de nieve. Cuando haga falta,
  el camino está identificado —`distribuidas[]` como vocabulario aditivo, tocando `_validar_casos`,
  la conversión de unidades de `from_dict` y **obligatoriamente `analysis.cargas_de_vano`**, que si
  se olvida hace desaparecer la parábola de las sondas y del visor sin ningún error.
- **El eslabón 13** (lote E, con el PDF abierto) y **la cascada 04→13** (lote F).
- **Meter la carrilera al modelo del galpón**: cambiaría los períodos que los eslabones 00 a 06 ya
  publicaron.

## 8 · Riesgos

- **El 07 es un memo de 953 líneas con 43 entradas y 24 salidas.** Es el eslabón más grande de la
  serie y el primero del lote; si algo va a costar, es ese. Se migra solo, sin empezar el 08.
- **La reciprocidad muerde al primer commit.** El 07 tiene que declarar los 43 `entra` aunque no
  use todos, y algunos vendrán del 02 y del 04 con símbolos que su prosa no menciona.
- **`E_Y_tope` mete una decisión de reparto que ningún memo tomó.** Va declarada como supuesto en
  la página, y su resultado se narra como contraste, no como verificación. El riesgo real es
  ajustar el reparto hasta que dé 1,11962: no se hace.
- **La escena a ~2,3 MB.** Se acepta; la mitigación es bajar `CIFRAS`, no quitar casos.
- **La torsión sigue sin contraste contra SAP2000.** Ninguna página del lote D debe citar un `T`
  del visor sin repetir ese límite; `verification/case12` sigue encolado.
