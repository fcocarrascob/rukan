# CLAUDE.md — Rukan

Guía para Claude Code al trabajar en este repositorio.

## ⚠️ Regla no negociable: verificar contra la fuente

Este es software de análisis estructural con implicancias de seguridad: los
cálculos que produce un ingeniero los **firma**. Por lo tanto, ante cualquier
duda técnica —fórmulas, disposiciones de normas (NCh433, NCh2369, NCh427,
ACI 318, AISC 360…), propiedades de perfiles, API de librerías— **se consulta
la fuente autoritativa antes de afirmar nada**. Nunca se responde de memoria.

- Librerías → `ctx7` / find-docs (ver reglas globales context7).
- Normas y libros → pedir/consultar el texto antes de implementar una
  disposición de código. Si la fuente no está disponible, **pedírsela al
  usuario en vez de asumir**.
- Un dato inventado o desactualizado invalida la verificación y destruye la
  confianza del producto. No hay excepciones a esta regla.

## Qué es Rukan

App opensource de análisis estructural que usa **OpenSeesPy** como motor —
alternativa económica a SAP2000 para ingenieros independientes en Chile, para
estructuras simples/cotidianas (análisis modal, espectral, pushover).

- **Wedge MVP**: acero industrial NCh2369 (galpones). Wedge 2 futuro:
  edificios de hormigón NCh433.
- El sitio [struct_pad](https://github.com/fcocarrascob/fcocarrascob.github.io)
  es el canal de publicación de los casos de verificación (blog).

## Estado actual y próximo paso

Verificados los casos 1–3 (voladizo, edificio de corte, reticulado), 5 (modal
espectral NCh2369), 6 (arriostramiento con liberación de momentos), 7 (galpón 3D:
2 direcciones + CQC + 100/30), 8 (peso propio, casos de carga y combinaciones,
galpón a dos aguas), 9 (torre CBF/MRF con T*/R* por dirección) y 10 (galpón del
altiplano: 188 barras, 79 combinaciones), todos con error ~0 % vs SAP2000.

El ensamblador `engine.py` (Model 3D → OpenSees, con liberación de momentos), el
análisis espectral propio (`modal.py`: CQC/SRSS + `run_directional_spectral` +
`directional_combination` 100/30) y las cargas (`loads.py`: peso propio
distribuido/concentrado, masa propia, casos y combinaciones) están verificados
contra SAP2000. Los casos contra SAP2000 requieren el notebook del trabajo (MCP
SAP2000).

**Caso 11 (2026-09-04): el primero cuyo patrón de referencia no es SAP2000.** Es
el galpón con puente grúa de la serie de memos `nch2369-galpon-grua` de
`F:\Proyectos_Python\Guias_Interactivas`, que publica sus resultados de análisis
**declarados**; el caso los corre y los contrasta. Tres archivos: `case11_data.py`
(geometría y secciones, cada constante con el eslabón que la publica),
`case11_ref.py` (rigidez directa 2D en numpy puro, sin `rukan` ni `openseespy` —
la regla del laboratorio aplicada a `verification/`) y
`case11_galpon_grua_nch2369.py`. Capas A–C —geometría, rigidez del marco y
arrastre—, **D** (el galpón completo en 3D: períodos por dirección y masas
participantes) y **E** (el galpón como archivo de proyecto, round-trip a 1e-15).
Encontró que la `k_Y` declarada en el memo 07 sale de un empuje en un solo alero y
no de un *sway*: 9,6 % de diferencia, con `k_riel` calzando a 2·10⁻⁵ por venir del
caso correcto. Y en la capa E, que empujar los diez aleros con la misma H es el sway
del marco **más el techo arriostrado**, que lo endurece 2,6·10⁻⁴ porque las
diagonales unen líneas distintas del rafter. `figuras()` regenera sus seis SVG.

**El archivo de proyecto (2026-09-05) es el puente con el repo de memos.** Esquema
`rukan/proyecto@1` (`io.py`): un JSON con modelo + casos + combinaciones + análisis +
**salidas** (símbolo del memo → sonda: `periodo_dominante`, `desplazamiento{nudo,gdl,caso}`,
`reaccion`, `fuerza`, …). `python -m rukan run <p>.proyecto.json` (`__main__.py`,
`analysis.py`) no toma opciones y escribe `<p>.resultados.json` con el SHA-256 del
proyecto, la versión, el commit y el `openseespy`. El repo de memos versiona el
proyecto junto al memo (`_modelos/`), un generador lo escribe importando la geometría
de `case11_data.py` vía `RUKAN_ROOT`, y `_kit/verify_modelo.py` compara hashes. **El
memo 00 de la serie es el primer consumidor**, con los cinco arneses en verde. Reglas:
las salidas son magnitudes primarias (`k = H/δ` es un paso del memo); nombres o ids en
`nudo`/`barra`; Pint en `io.load`, el núcleo nunca ve otra unidad. `espectral` (T*/R*
por dirección) queda para el esquema v2. Corte y torsión de barra siguen la regla
análoga a la axial y **no están verificados contra SAP2000**; axial y momentos sí.

**`vista.py` (2026-09-05) es la primera visualización que tiene el repo**, y un
adelanto parcial de la Fase 2: planta, elevaciones, axonometría y deformada de un
modo, a SVG y sin dependencias nuevas. **Sin eliminación de líneas ocultas**, y con
`cotas` explícito porque el arnés del repo de memos exige que toda cifra dibujada
exista en el texto. `escena()` toma `filtro` — sin él, en una elevación las barras
que comparten proyección se tapan y la que queda encima miente.

**El sitio (2026-09-05) es el repo de modelos con su narración en 3D**, en `sitio/`,
sin relación con struct_pad. Tres capas: el esquema `rukan/escena@2` (`escena.py`,
`python -m rukan escena`: geometría, modos normalizados, deformadas de **todos** los casos y
combinaciones, reacciones y fuerzas de extremo con el signo del diagrama, misma cabecera de
procedencia que los resultados); el visor `sitio/docs/visor/rukan-visor.js` (web component
sobre three.js **vendoreado** en `vendor/`, cámara ortográfica con órbita, vistas fijas,
modos animados, deformada con escala declarada en el rótulo, tooltip); y MkDocs Material
con `mkdocs-macros`, donde **ninguna cifra de la prosa se teclea**: `r()`, `cociente()` y
`tabla_modos()` la leen de la corrida, y `procedencia()` rompe el build si el hash del
proyecto no es el de los JSON. Cada entrada es `sitio/docs/modelos/<slug>/` con
`_generar.py`, el proyecto, los resultados y la escena **versionados** (el build no
necesita OpenSees). `tests/test_sitio.py` exige que el generador reproduzca byte a byte el
proyecto versionado. Identidad del sitio: narra **el modelo y lo que el motor hace con él**;
el cálculo normativo se cita al memo, la verificación del motor queda en struct_pad. Primera
entrada: el galpón con puente grúa (caso 11, cuatro casos estáticos). **Esfuerzos a lo largo
de la barra (color, diagramas N/V/M) quedan para `escena@2`**, que cerró el lote C (más abajo). Se
despliega a GitHub Pages con `.github/workflows/sitio.yml` (hay que activar Pages con origen
«GitHub Actions» una vez). Diseño: `docs/superpowers/specs/2026-09-05-sitio-rukan-design.md`.

**Las series (2026-09-05): el sitio es la casa de la serie `nch2369-galpon-grua`.** Se
migra desde el repo de guías eslabón por eslabón, y **nada nuevo se escribe allá**. Andamiaje
en `sitio/serie.py`: cada eslabón es `sitio/docs/series/<serie>/<NN-slug>/` con un
`_calculo.py` que declara con `Eslabon` (`caso`, `entra`, `paso`, `sale`, `publicado`) y
escribe `<NN-slug>.valores.json` (esquema `rukan/valores@1`). Reglas: **la cadena se consume,
no se copia** (`entra()` lee el JSON del origen o los `resultados.json` del modelo);
`publicado()` es el **oráculo de migración** (lo que el memo original imprimió, como texto con
coma decimal) y `escribir()` falla si un `sale` se aparta media unidad del último decimal;
primario vs derivado (el modelo emite δ, `k = H/δ` es un `paso`); el memo sustituye en sus
fórmulas la cifra **impresa**, así que cuando un paso no reproduce, primero se prueba con el
valor redondeado a los decimales publicados (el 00 lo hizo con δ a 7 decimales). Macros en
`main.py`: `v()` / `vt()` (LaTeX: `{,}` y `\,`), `ficha()`, `tabla_serie()`, `grafo_serie()`
(mermaid), `figura()`, `razon()`. Figuras: `sitio/figuras.py` (helper SVG portado) y
`_figuras.py` por eslabón con `cotas()` leídas del JSON. KaTeX vendoreado.
`tests/test_series.py`: cadena (`verificar_cadena`), `_calculo.py` reproduce el JSON, cada
`sale` aparece en `index.md` con `v(`/`vt(`, sin `\d.\d` dentro de `$$`, citas con página,
cotas de SVG con respaldo. Un `heredan` hacia un eslabón no migrado es promesa, no hallazgo.
**Migrados: 00 a 12, la serie escrita entera** (lotes A, B y D); falta el **13**, que no existe
en el repo de memos y hay que escribirlo. El pipeline por eslabón
(`docs/superpowers/specs/2026-09-05-series-sitio-rukan-design.md` § 6): leer memo y
`.check.js` → `_calculo.py` con `publicado` y `resumen` → `_figuras.py` → `index.md` con el
molde (narración por pasos, visores donde entra el modelo, ficha, referencias) → build estricto
y captura → commit. **La tabla de Referencias se migra literal**, celda por celda. **Fidelidad
primero**: la cascada 04→13 con los períodos del 00 se aplica después de migrar todo. El
modelo del sitio tiene la malla del memo (`nsub=16`, 1 000 kN por marco).

**El lote B (2026-09-05) confirmó que la sustitución de la cifra impresa es la regla y no la
excepción**: el 04 divide ordenadas impresas (con las exactas su razón daría 1,04686 y no
1,04687), el 05 multiplica el peso por las ordenadas del 04 a cinco decimales, y el 06
redondea **todos** sus pasos a cinco —con redondeo medio hacia **arriba**, el `Math.round` del
arnés del memo y no el medio-al-par de `round()` de Python, que en el pico del espectro
vertical dan dígitos distintos—. Dos dígitos del repo de memos no reproducen y quedan anotados
en los `## Límites` de su página: el `k_req_Y` del 05 (5 216,93102 impreso contra 5 216,931030)
y el corte con nieve en la masa del 06 (357,53340 contra 357,53342); los dos pasaban porque el
arnés de allá comparaba con tolerancia **relativa** y el oráculo de acá es absoluto.

**El lote C (2026-09-06) cerró `escena@2`: los esfuerzos a lo largo de la barra.** OpenSees no los
entrega —se comprobó que `sectionX`, `section` e `integrationPoints` devuelven `[]` en un
`elasticBeamColumn`—, así que la superposición de la carga de vano sobre las fuerzas de extremo la
hace Rukan, y la hace en **un** lugar: `esfuerzos.py`, sobre los seis valores del **diagrama en el
extremo i** (no las `localForces` crudas, para que el visor pueda alimentarla con lo que la escena
publica), con `Mz(x) = Mz_i + Vy_i·x − wy·x²/2` y `My(x) = My_i − Vz_i·x + wz·x²/2`. La escena gana
`barras[].vecxz` y `casos.<c>.w` —magnitudes primarias, +47 KB, contra los ~880 KB que costaría
muestrear el diagrama— y **reemplaza** a `@1`; el visor comprueba el esquema. El gemelo en JS
(`sitio/docs/visor/esfuerzos.js`) no importa nada y `tests/test_esfuerzos_js.py` lo cruza con
`node`: es la mitigación del único riesgo real del diseño, que la fórmula viva en dos lenguajes.
El visor pinta las 1 044 barras con una rampa divergente y dibuja el diagrama normal al eje solo
sobre las que `filtro` selecciona. Verificado en `lab/nota07` con tres caminos (la cerrada, el
equilibrio integrado en numpy, una malla ×16 en OpenSees), 34 magnitudes con error 0 %. Diseño:
`docs/superpowers/specs/2026-09-06-escena2-esfuerzos-por-barra-design.md`.

**El lote D (2026-09-06) migró los eslabones 07 a 12 y dejó la serie escrita entera en el
sitio.** Su hallazgo de partida fue que **ninguna cifra publicada por esos seis memos sale de una
corrida** —el 07 declara los resultados de un modelo plano que «describe y no ejecuta», el 08 es
un vano simple, el 09 rangos M/S, el 10 un ábaco de AIST, el 11 y el 12 formas cerradas—, así que
los casos nuevos del proyecto no sirven a la fidelidad sino al **contraste**. El galpón gana tres
casos nodales (`H_riel_uno`, `E_X`, `E_Y_tope` con la grúa en `X_G_TOPE`) y el sitio un modelo
nuevo, **`modelos/carrilera`**, que estrena `combinaciones`. `serie.py` gana el oráculo del
`## Resumen` (`E.resumen()`, todas las filas del memo y no sólo las salidas) y `main.py` el macro
`razon(modelo, a, b)`. El sismo es **estático equivalente**: `analisis.espectral` sigue siendo del
esquema v2, y la sonda `esfuerzo_extremo` queda encolada con él porque el máximo sobre un conjunto
no es lineal y devolvería tres cosas donde `salidas` devuelve un float.

**Lo que el lote D agregó a la regla del oráculo:** la sustitución de la cifra impresa ya era la
norma; acá apareció su causa. **El memo 11 aporta dieciséis de sus 118 filas** que su propia
aritmética sobre las cifras impresas no da, porque su `.check.js` compara los bloques D y E con
**1e-4 absoluto** y su quinto decimal nunca se verificó. Con el 07, el 08, el 10 y el 12 el lote
deja veinte y tantos dígitos anotados en los `## Límites` de sus páginas; ninguno cambia una
sección ni una conclusión. Y **un `J` mal calculado en `comp_props()`** (lado largo como espesor)
se dejó **sin corregir a propósito**: mueve todos los resultados del modelo entre 1e-9 y 1e-5
relativo y saca el `Ux_star` del 00 de su tolerancia, así que es de la clase de la cascada y va
con el lote F. Diseño: `docs/superpowers/specs/2026-09-06-lote-d-eslabones-07-12-design.md`.

**Próximo paso:** el **lote E** —el eslabón 13, diagonales longitudinales y anclaje, que **no
existe en el repo de memos** y hay que escribirlo con el PDF abierto; llega con tres encargos ya
cuantificados del 11 y del 12— o el **lote F**, la cascada 04→13 con los períodos del 00, que
arrastra el `J` de `comp_props()`; o **Fase 1** (chequeo de código AISC/NCh427). Ver
`ROADMAP.md`.

## Principios de arquitectura

1. **Motor separado de la GUI.** El núcleo (`src/rukan/`) es puro Python, sin
   dependencias de UI, testeable y portable. La GUI (PySide6) vendrá después y
   se apoyará en el núcleo.
2. **config → script.** El modelo se define como dataclasses serializables que
   generan/ejecutan un análisis OpenSees **legible y auditable** (mismo patrón
   que Skills_SAP). Transparencia total: el análisis no es una caja negra.
3. **Modelo de datos 3D desde el día 1.** Los nodos son `(x, y, z)` con 6 GDL.
   El caso 2D es `z = 0` con los GDL fuera de plano restringidos. Nunca se
   modela 2D-only para "subir" a 3D después.
4. **Pint solo en la frontera.** Validación dimensional y unidades en IO; el
   núcleo numérico y OpenSees reciben **floats** en el sistema interno
   consistente. Ver `src/rukan/units.py`.

## Sistema de unidades interno (consistente)

OpenSees no gestiona unidades: la consistencia es responsabilidad nuestra.
Sistema interno fijo:

    longitud = m,  fuerza = kN,  tiempo = s

Derivadas por consistencia (F = m·a):

    masa    = tonne (Mg = 1000 kg)   [kN·s²/m]
    tensión = kN/m² (= kPa)
    inercia = m⁴

Todo lo que entra al núcleo se normaliza a este sistema en la frontera.

## Desarrollo Dirigido por Verificación

Cada feature nace de un caso de verificación. Cada caso es **a la vez** un test
de regresión y un post de blog. La escalera (ver `ROADMAP.md`):

1. Columna en voladizo (1 GDL) — vs fórmula a mano ✅ implementado
2. Pórtico de corte 2 GDL — vs fórmula a mano
3. Reticulado simple — vs mano / SAP
4. Pórtico plano gravitacional — vs SAP
5. Modal espectral 2D (NCh2369) — vs SAP ✅ error ~0% (RSA + CQC/SRSS propio)
6. Arriostramiento / liberación de momentos — vs SAP ✅ error ~0% (biela = Truss)
7. Galpón 3D completo — vs SAP ✅ error ~0% (2 direcciones + CQC + 100/30)
8. Peso propio, casos de carga y combinaciones — vs SAP ✅ error ~0% (galpón dos aguas)
9. Torre CBF/MRF, T*/R* por dirección — vs SAP ✅
10. Galpón del altiplano, 188 barras, 79 combinaciones — vs SAP ✅
11. Galpón con puente grúa — **vs una serie de memos verificados y numpy puro**, no vs SAP

Regla de contenido: teoría + cálculo a mano donde ilumina (casos 1-3); a partir
del caso 4-5 el cálculo a mano deja de ser tractable y SAP2000 pasa a ser el
patrón de referencia. No forzar cálculo manual donde no aporta.

## Las dos líneas de contenido

El repo alimenta **dos** líneas de posts en struct_pad, con reglas distintas:

| | `verification/` | `lab/` |
|---|---|---|
| Qué valida | **el motor** de Rukan | **un fenómeno** de análisis |
| Patrón de referencia | SAP2000 (y mano en los primeros) | fórmula cerrada o numpy puro |
| Necesita SAP2000 | sí (notebook del trabajo) | **no** — se escribe en cualquier máquina |
| En el blog | `section: "Rukan"`, serie numerada | `section: "Laboratorio"`, notas sueltas |

El backlog de notas está en [`LAB.md`](LAB.md) y la convención en
[`lab/README.md`](lab/README.md). Tres reglas que no se negocian:

1. **Dos caminos independientes por nota.** Una referencia (cerrada o numpy) y
   OpenSeesPy. Sin patrón contra el cual medir, la nota no entra.
2. **`lab/_lib/ref.py` no importa `rukan` ni `openseespy`.** Si la referencia
   compartiera código con lo verificado, ambas se equivocarían igual y la tabla
   daría error 0 % sin decir nada.
3. **La tabla del post es la salida literal del script.** `lab/_lib/report.py`
   la imprime en markdown y hace `assert`; `tests/test_lab.py` corre cada nota
   como test de regresión, así un post publicado no puede quedar mintiendo.

Los scripts viven acá; el MDX y los SVG, en struct_pad. Las figuras las genera
el mismo script que calcula (`lab/_lib/svg.py`) y se copian con
`python -m lab._lib.publish notaNN --slug lab-<tema>`.

## Comandos

```bash
pip install -e ".[dev]"                       # instala Rukan editable + pytest
pytest                                        # tests unitarios + notas del laboratorio
python verification/case01_cantilever_column.py   # corre un caso de verificación
python -m lab.nota01_eleload_empotramiento        # corre una nota del laboratorio
python -m rukan validar <p>.proyecto.json         # valida el esquema sin correr nada
python -m rukan run <p>.proyecto.json             # corre y escribe <p>.resultados.json
python -m rukan escena <p>.proyecto.json          # corre todo y escribe <p>.escena.json (el visor)
pip install -e ".[sitio]"                         # MkDocs Material + macros
mkdocs serve -f sitio/mkdocs.yml                  # el sitio en local; `mkdocs build --strict` en CI
```

## Estructura

```
src/rukan/
  units.py    # capa de unidades Pint + sistema interno
  model.py    # dataclasses del modelo (3D desde día 1)
  engine.py   # ensamblador Model 3D → dominio OpenSees
  loads.py    # peso propio, casos de carga y combinaciones
  modal.py    # análisis espectral propio: CQC/SRSS + direccional 100/30
  esfuerzos.py # los seis esfuerzos a lo largo de la barra: extremo i + carga de vano
  spectra.py  # espectro NCh2369
  vista.py    # dibujo del modelo a SVG: planta, elevaciones, isométrica, deformada
  io.py       # el archivo de proyecto rukan/proyecto@1: (de)serialización, validación, unidades
  analysis.py # el runner: modal + casos + combinaciones + sondas -> {simbolo: valor}
  escena.py   # el esquema rukan/escena@2: lo que el visor dibuja, con procedencia
  __main__.py # CLI: `python -m rukan run|validar|escena`
verification/ # escalera de casos: test + artefacto de blog (vs SAP2000)
lab/          # notas de análisis verificable (vs fórmula cerrada / numpy)
  _lib/       # report (tabla + assert), ref (numpy puro), svg, publish
  figs/       # SVG generados, se copian al blog
sitio/        # el sitio: MkDocs Material + macros (main.py) + visor three.js
  serie.py    # el andamiaje de una serie: Eslabon, valores@1, cadena, oráculo, citas
  figuras.py  # helper SVG de las figuras de un eslabón (cotas desde el JSON)
  docs/visor/ # rukan-visor.js, esfuerzos.js (gemelo de rukan/esfuerzos.py, sin imports),
              # three.js y KaTeX vendoreados (vendor/*/VERSION)
  docs/modelos/<slug>/  # _generar.py + proyecto + resultados + escena + index.md
                        # galpon-grua (7 casos) y carrilera (la viga del 08, con combinacion)
  docs/series/<serie>/<NN-slug>/  # _calculo.py + valores.json + _figuras.py + figs/ + index.md
tests/        # tests unitarios del núcleo + corrida de cada nota + el sitio
```
