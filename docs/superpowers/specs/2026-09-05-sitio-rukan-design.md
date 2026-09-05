# Plan — El sitio de Rukan: un repo de modelos OpenSees con su narración en 3D

## Contexto

Rukan ya tiene el documento que un visor consume: el archivo de proyecto `rukan/proyecto@1`
(`io.py`) y su `resultados.json` con hash. Lo que no tiene es ninguna forma de **ver** un modelo
más allá de los SVG de `vista.py` (proyecciones fijas, sin líneas ocultas, un modo por figura).
El ROADMAP pone «visor de resultados (webview three.js)» en la Fase 2 y lo dejó sin fecha.

La idea (2026-09-05): un sitio **dentro del repo Rukan**, independiente de struct_pad, que sea a
la vez el repositorio de modelos OpenSees y su narración visual, con incrustados 3D para mover
el modelo, animar modos y mirar deformadas. No es un desvío: el visor que narra el galpón hoy
es el visor de resultados de la GUI mañana, y el contrato de datos que lo alimenta es lo que
esa GUI leerá.

**Identidad del sitio, para no ser el tercer duplicado del galpón grúa**: narra **el modelo y lo
que el motor hace con él** (qué se idealizó, cómo se mueve, qué números salen y de dónde). El
cálculo normativo queda en el repo de memos y se **cita**, no se rehace; la verificación del
motor queda en struct_pad. La narración de NCh2369 / AISC 360 cae bajo la regla de verificar
contra la fuente igual que el código.

## Decisiones tomadas con el usuario (2026-09-05)

| Decisión | Elegido |
|---|---|
| Dónde vive | En el repo Rukan, sin relación con struct_pad |
| Generador | **MkDocs Material** (pip, cero npm; el repo sigue siendo solo Python) |
| Alcance del visor v1 | **Geometría + modos animados + deformadas por caso/combinación + reacciones.** Los esfuerzos (color y diagramas N/V/M) son una segunda entrega con su verificación |
| Trazabilidad de la prosa | **Cifras inyectadas desde la corrida** con `mkdocs-macros`; tablas como salida de script. Sin arnés aparte |
| Primera entrada | El galpón con puente grúa (caso 11), reciclando `case11_data.build_model` |

Decisiones menores tomadas por mí, para no bloquear: carpeta `sitio/` (no `site/`, que es el
nombre de salida por omisión de MkDocs); three.js **vendoreado y fijado a una versión**, no
desde CDN (la página funciona sin conexión, como las guías del repo de memos); los JSON
generados (`proyecto`, `resultados`, `escena`) **se versionan** y el build del sitio no
necesita OpenSees, igual que `_modelos/` en el repo de memos; despliegue en GitHub Pages del
repo (`https://fcocarrascob.github.io/rukan/`) con GitHub Actions.

## Diseño

### 1. El contrato de datos: esquema `rukan/escena@1` (motor, `src/rukan/escena.py` nuevo)

La versión numérica de `vista.escena()`: todo lo que un visor necesita para dibujar, en un JSON
con la misma procedencia que `resultados@1` (SHA-256 del proyecto, versión, commit,
`openseespy`, fecha). Sistema interno (m, kN, t), floats con 6 cifras significativas para
contener el tamaño (el galpón tiene 965 nudos × 15 modos).

```json
{
  "esquema": "rukan/escena@1",
  "proyecto": "galpon-grua.proyecto.json", "sha256_proyecto": "…",
  "rukan": "0.1.0", "commit": "…", "openseespy": "…", "generado": "…",
  "titulo": "…", "unidades": {"longitud": "m", "fuerza": "kN", "masa": "t"},
  "nudos":  [{"id": 1, "nombre": "K1A_0", "xyz": [0, 0, 0], "fijo": [1,1,1,1,1,1]}],
  "barras": [{"id": 1, "nombre": "COL1A_1", "i": 1, "j": 2, "seccion": "COL_0.52500"}],
  "masas":  [{"nudo": 7, "m": [2.1, 2.1, 2.1]}],
  "modos":  [{"n": 1, "T": 0.24878, "participacion": {"X": 0.0, "Y": 0.83, "Z": 0.0},
              "phi": [[dx, dy, dz], …]}],
  "casos":  {"D": {"u": [[ux,uy,uz,rx,ry,rz], …],
                   "reacciones": {"1": [Fx,Fy,Fz,Mx,My,Mz]},
                   "fuerzas": [[N_i,Vy_i,Vz_i,T_i,My_i,Mz_i, N_j,…], …]}},
  "combinaciones": {"1.2D+1.6Lr": {"u": …, "reacciones": …, "fuerzas": …}}
}
```

- `phi` en el orden de `nudos`, normalizado a `max|phi| = 1` (el visor escala a una fracción
  del tamaño del modelo). Sale de `ops.nodeEigenvector`, como en `analysis.modal`.
- `casos`: **todos** los de `p.casos` (no solo los que alguna sonda cita), con `ops.nodeDisp`
  en todos los nudos, `ops.nodeReaction` en los nudos con algún GDL fijo y
  `ops.eleResponse(tag, "localForces")` en todas las barras, con la **misma conversión de
  signo** de `analysis._extractor` (se extrae a una función compartida `signo_diagrama` para
  que las dos rutas no diverjan). `combinaciones`: combinación lineal en numpy de los arrays
  de casos, con los factores del proyecto.
- `fuerzas` va en el JSON porque cuesta cero y sale por el camino ya verificado (axial y
  momentos; corte y torsión siguen sin verificar contra SAP2000, el docstring lo dice). En v1
  el visor solo las muestra al pasar el cursor por los extremos; **ningún color ni diagrama**.
  Los valores intermedios de barra son la v2 (ver «Fuera de alcance»).
- API: `escena.armar(p: Proyecto, ruta_proyecto) -> dict` (corre modal si `analisis.modal`
  existe, y cada caso con `loads.run_static_case`) y `escena.escribir(doc, ruta)`.
  Reutiliza `engine.build`, `analysis.modal`, `analysis._aplicar`, `io.sha256`,
  `io.resultados` (para la cabecera de procedencia; refactor mínimo: sacar la cabecera a
  `io._cabecera(ruta_proyecto)` y que `resultados` y `escena` la compartan).
- CLI: `python -m rukan escena <p>.proyecto.json [--salida RUTA]` escribe
  `<p>.escena.json` junto al proyecto, sin más opciones (misma regla que `run`). Se agrega
  `io.ruta_escena` al lado de `io.ruta_resultados`.
- Tests `tests/test_escena.py`: sobre el pórtico fixture de `tests/test_vista.py`: (a) `u` bajo
  carga nodal coincide con la sonda `desplazamiento` de `analysis.run` a 1e-12; (b) `T` de
  `modos` coincide con `analysis.modal`; (c) `max|phi| = 1`; (d) suma de reacciones
  verticales bajo `D` = `loads.total_weight`; (e) una combinación = suma ponderada de los
  casos; (f) el esquema round-trip por JSON no pierde nada; (g) `python -m rukan escena`
  (en `tests/test_cli.py`) escribe el archivo con el hash correcto.

### 2. El visor: `sitio/docs/visor/rukan-visor.js` (JS suelto, sin build)

Un *web component* `<rukan-visor src="galpon-grua.escena.json" modo="1" caso="H_alero">`
en JavaScript moderno sin framework; three.js es la única librería.

- **Vendoreado** en `sitio/docs/visor/vendor/`: `three.module.min.js` y
  `addons/controls/OrbitControls.js` de una versión fijada, descargados de la distribución
  oficial al implementar; `sitio/docs/visor/vendor/VERSION` registra cuál. `OrbitControls`
  importa el especificador desnudo `'three'`, así que hace falta un **importmap** en el
  `<head>`: va en `sitio/overrides/main.html` (bloque `extrahead` de Material) apuntando a
  `{{ base_url }}/visor/vendor/…`. El visor se carga con
  `extra_javascript: [{path: visor/rukan-visor.js, type: module}]`.
- **Qué dibuja**: barras sin deformar en trazo tenue (`LineSegments`), deformadas en acento
  (`BufferGeometry` con `DynamicDrawUsage`, posiciones actualizadas por cuadro), apoyos como
  marcadores, nudos con masa como puntos. Paleta = la de `vista.PALETA` (tinta, suave, acento,
  fondo claro propio), para que el visor y los SVG se lean como una misma cosa.
- **Controles**, en una barra sobre el lienzo: vista (`iso`, `planta`, `transversal`,
  `longitudinal`, libre con órbita), selector de **modo** (rótulo `n · T = 0,249 s · Y 83 %`),
  selector de **caso/combinación**, deslizador de **escala** (por omisión, la que hace que el
  máximo desplazamiento sea un 5 % de la diagonal del modelo), botón **animar** (modo: seno en
  el tiempo; caso: ida y vuelta), y un **tooltip** al pasar el cursor: nudo (nombre, xyz, `u`
  del caso activo) o barra (nombre, sección, fuerzas de extremo del caso activo).
- `ResizeObserver` para el ancho del contenedor; `aria-label` con el título del modelo.
- Sin eliminación de líneas ocultas ni sombreado: es un reticulado de líneas, como `vista.py`.
  Consciente de ello y dicho en el docstring.

### 3. El sitio: `sitio/` (MkDocs Material + mkdocs-macros)

```
sitio/
  mkdocs.yml            # site_name Rukan, language es, theme material, plugins [search, macros]
  main.py               # define_env: macros r(), tabla_modos(), procedencia()
  overrides/main.html   # importmap de three
  docs/
    index.md            # qué es este sitio y qué no (la identidad de arriba)
    visor/rukan-visor.js, vendor/…
    modelos/
      galpon-grua/
        index.md                       # la entrada
        _generar.py                    # escribe galpon-grua.proyecto.json desde case11_data
        galpon-grua.proyecto.json      # versionado
        galpon-grua.resultados.json    # `python -m rukan run`, versionado
        galpon-grua.escena.json        # `python -m rukan escena`, versionado
```

- `pyproject.toml`: grupo opcional `sitio = ["mkdocs-material", "mkdocs-macros-plugin"]`.
  `.gitignore`: `sitio/_build/` (`site_dir: _build`).
- **Macros** (`sitio/main.py`, `define_env`): `r(modelo, simbolo, cifras=None)` lee
  `docs/modelos/<modelo>/<modelo>.resultados.json` y devuelve el valor formateado con **coma
  decimal** y la unidad opcional (`r('galpon-grua', 'T_star_Y', 5)` → `0,24878`);
  `tabla_modos(modelo, n)` arma la tabla markdown de períodos y participación desde la escena;
  `procedencia(modelo)` imprime la línea «corrido con rukan 0.1.0 @ abc1234 · openseespy 3.7.1
  · sha256 …» desde los dos JSON y **falla el build** si sus hashes no coinciden con el proyecto
  (la frescura, por hash, como el arnés del repo de memos). Un símbolo inexistente falla el build
  con el nombre del símbolo.
- El markdown incrusta el visor como HTML crudo en su propia línea:
  `<rukan-visor src="galpon-grua.escena.json" modo="2"></rukan-visor>`.
- **Tests `tests/test_sitio.py`**: por cada carpeta en `sitio/docs/modelos/`, (a) el proyecto
  valida (`io.load`), (b) `sha256(proyecto)` == `sha256_proyecto` de resultados y de escena,
  (c) `_generar.py` corrido a un directorio temporal produce un dict **igual** al proyecto
  versionado (el modelo del sitio es el del caso 11, no una copia que se aleja), (d) si
  `mkdocs` está instalado, `mkdocs build --strict` termina en 0 (se salta con `pytest.skip` si
  no lo está).

### 4. La primera entrada: el galpón con puente grúa

`_generar.py` importa `build_model(nsub=4, escalonada=True)` y `masas` de
`verification/case11_data.py` (con `sys.path`, como hace `case11_galpon_grua_nch2369.py`) y
arma el proyecto con: `analisis.modal` 15 modos; casos `D` (peso propio distribuido, para ver
la deformada de gravedad), `H_alero` (sway: los diez aleros con la misma H), `H_alero_uno` (un
solo alero, el caso que el memo 07 usó sin decirlo) y `H_riel`; salidas `T_star_X`, `T_star_Y`,
`Ux`, `Uy`, `macum_X/Y`, `d_alero`, `d_alero_uno`, `d_riel`, `peso_total`. Es el mismo modelo
que `case11.proyecto_3d`, con dos casos más; el test (c) lo mantiene atado.

Guion de `index.md` (prosa en español neutro, tú, sin regionalismos; cifras solo por macro):

1. **Qué es este galpón** y de dónde sale: enlace a la serie de memos y al memo 00; qué se
   idealizó (masa por áreas tributarias, bielas, alma variable prismatizada por tramos).
2. **El modelo en 3D**: el visor en geometría; planta, elevaciones e isométrica como vistas.
   Cuántos nudos y barras, y por qué (malla del tapered, `nsub`).
3. **Cómo se mueve**: el visor en el modo dominante en Y y luego en X; `tabla_modos`; qué lee
   NCh2369 de aquí (T* → R* de la Ec. 1b) **citando el memo 04**, sin rederivar.
4. **Los empujes**: deformada de `H_alero` contra `H_alero_uno`; el hallazgo del caso 11
   (9,6 % en `k_Y` por el caso de carga, no por la malla) narrado con `d_alero` y
   `d_alero_uno`; `k = H/δ` escrito como paso, como en el memo.
5. **La gravedad**: deformada bajo `D` y `peso_total`; nota de que la masa sísmica del memo no
   es este peso.
6. **Procedencia**: `procedencia('galpon-grua')` y cómo regenerar todo con tres comandos.

### 5. Despliegue y docs

- `.github/workflows/sitio.yml`: en push a `main`, `pip install mkdocs-material
  mkdocs-macros-plugin` (sin Rukan ni OpenSees: los JSON están versionados),
  `mkdocs build --strict -f sitio/mkdocs.yml`, `actions/upload-pages-artifact` +
  `actions/deploy-pages`. **Requiere activar Pages con origen «GitHub Actions» en los
  ajustes del repo** (lo hace el usuario; el plan lo deja dicho en el README del sitio).
- `CLAUDE.md`: sección «El sitio» (identidad, esquema `escena@1`, comandos, regla de las
  cifras por macro). `ROADMAP.md`: Fase 2 marca «visor de resultados: v1 web, three.js» y
  anota la v2 de esfuerzos. `README.md`: enlace al sitio.

## Orden de implementación (TDD, un commit por paso)

1. **Spec**: copiar este diseño a `docs/superpowers/specs/2026-09-05-sitio-rukan-design.md`
   y commitear.
2. **Motor**: `io._cabecera` + `io.ruta_escena` → `escena.py` + `tests/test_escena.py` →
   subcomando `escena` en `__main__.py` + test en `test_cli.py`.
3. **Sitio, esqueleto**: `pyproject` (grupo `sitio`), `.gitignore`, `sitio/mkdocs.yml`,
   `main.py` con los tres macros y sus tests (en `test_sitio.py`, sobre un `resultados.json`
   de fixture), `overrides/main.html`, `index.md`.
4. **Visor**: vendorear three.js (versión fijada en `VERSION`), `rukan-visor.js`. Se prueba
   con la escena del galpón servida por `mkdocs serve`; captura con Chrome headless
   (`--headless --screenshot`, WebGL por software) para dejar evidencia.
5. **Entrada del galpón**: `_generar.py` → `python -m rukan run` → `python -m rukan escena`
   → `index.md`; `tests/test_sitio.py` completo.
6. **Workflow de Pages**, `CLAUDE.md`, `ROADMAP.md`, `README.md`.

## Verificación

- `pytest` en verde (incluye `test_escena`, `test_sitio`, y todo lo anterior).
- `python -m rukan escena sitio/docs/modelos/galpon-grua/galpon-grua.proyecto.json` escribe
  la escena; `T` del modo dominante en Y en la escena = `T_star_Y` de resultados =
  `0,24895` (capa D del caso 11, escalonado, `nsub=4`).
- `mkdocs build --strict -f sitio/mkdocs.yml` termina en 0; `mkdocs serve` y en el navegador:
  el galpón orbita, los modos animan con el rótulo correcto, la deformada de `H_alero` es un
  sway y la de `H_alero_uno` no, el tooltip da el `u` de un alero igual a `d_alero` de
  resultados, las vistas preset coinciden con los SVG de `verification/figs/case11-*.svg`.
- Prueba de frescura: cambiar un dígito del proyecto sin recorrer → `test_sitio` y el build
  (`procedencia`) fallan.
- Prueba de atadura: cambiar `nsub` en `_generar.py` sin regenerar → test (c) falla.

## Fuera de alcance (siguiente)

- **Esfuerzos, `escena@2`**: valores intermedios por barra (superposición de la carga
  distribuida sobre las fuerzas de extremo, la maquinaria de `lab/nota01`), verificados
  contra numpy y SAP2000; luego color por esfuerzo y diagramas N/V/M en el visor.
- Espectral (`T*/R*` por dirección) como caso del proyecto: es el esquema v2 de `proyecto`.
- Segundas entradas: el galpón a dos aguas del caso 8 (la apertura del pórtico) y la torre del
  caso 9; el laboratorio no entra (su patrón es struct_pad).
- Modo oscuro del visor: dibuja su fondo claro propio, como `vista.py`.

## Riesgos

- **WebGL en la captura headless**: Chrome headless usa SwiftShader; si la captura sale en
  blanco, se verifica a ojo en el navegador y se anota.
- **Tamaño de la escena** del galpón (965 nudos, 15 modos, 4 casos): estimado bajo 1 MB con 6
  cifras; si crece, se baja a 5 cifras o se comprime `phi` a `Float32`.
- **`base_url` en el importmap**: en GitHub Pages el sitio cuelga de `/rukan/`; la ruta se
  prueba con `mkdocs build` y una página anidada, no solo en `serve`.
- **Divergencia de signos** entre `analysis._extractor` y `escena`: se evita compartiendo la
  función; el test (a) de `test_escena` compara contra `analysis.run`.
