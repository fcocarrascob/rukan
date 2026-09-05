# Plan — `escena@2`: los esfuerzos a lo largo de la barra, sobre el modelo

## Contexto

El lote B de la serie `nch2369-galpon-grua` quedó cerrado: los eslabones 00 a 06 están
migrados en `sitio/docs/series/nch2369-galpon-grua/` y `verificar_cadena` devuelve vacío. Lo
que el plan de series (§ 7) llama **lote C** es lo que sigue, y su enunciado era: «esfuerzos a
lo largo de la barra (superposición de la carga distribuida sobre las fuerzas de extremo, la
maquinaria de `lab/nota01`), verificados contra numpy y SAP2000; color y diagramas N/V/M en el
visor. **Spec aparte.**» Este es ese spec.

Hoy la escena `rukan/escena@1` emite, por caso y por barra, las **doce fuerzas de extremo** con
el signo del diagrama (`analysis.signo_diagrama`). Entre esos dos números no hay nada: el visor
no puede dibujar el momento del vano, y la `nota01` del laboratorio ya demostró que interpolar
linealmente entre los extremos no se queda corto sino que **cambia de signo** (−16,9 kN·m donde
el real es +25,3).

### Cuatro hallazgos que fijaron el diseño

**1 · OpenSees no entrega esfuerzos dentro de la barra, y se comprobó en vez de suponerlo.**
Sobre un `elasticBeamColumn` 3D con `eleLoad -beamUniform`, `eleResponse(tag, "sectionX", perc)`,
`"section"` e `"integrationPoints"` devuelven `[]`; solo hay `localForces` / `localForce` /
`forces` / `globalForce` (los dos extremos) y `basicForce` (las seis fuerzas básicas). Las
respuestas `sectionI` / `sectionC` / `sectionJ` / `sectionX` que documenta OpenSeesPy pertenecen
a `pipe` y `curvedPipe`, no a `elasticBeamColumn`. La superposición la tiene que hacer Rukan.

**2 · El tamaño no es cuestión de gusto: son ~25 KB contra ~880 KB.** La escena del galpón pesa
1,50 MB (casos 839 KB, modos 532 KB, geometría 128 KB). Muestrear seis componentes en cinco
estaciones sobre 1 044 barras cuesta ~220 KB **por caso** — +880 KB con los cuatro casos de hoy,
y crece con cada caso que agregue el lote D. Emitir la carga de vano local son tres números por
barra, y **solo en los casos que tienen carga distribuida** (hoy uno, `D`).

**3 · El signo del corte se puede fijar acá, y no por analogía.** Ver § 2.

**4 · El lote D depende de `escena@2` menos de lo que el plan de series suponía.** De las
salidas de los memos 07 a 12, la mayoría son desplazamientos, propiedades de sección y pasos a
mano. Los que sí piden esfuerzos son el 07 (`Rcol_grua`, `Nbase_u`, `Mbase_u`), el 08 (`M_ux` =
707,27 kN·m, que es literalmente el caso de la `nota01`: `R·x − w·x²/2`) y el 11 (los axiales de
las diagonales). El bloqueo real del lote D es otro y no lo levanta este plan: **el proyecto no
tiene todavía ningún caso de grúa, de nieve ni de sismo estático**, solo tres empujes unitarios
y el peso propio.

## Decisiones tomadas con el usuario (2026-09-06)

| Decisión | Elegido |
|---|---|
| Qué emite `escena@2` | **Magnitudes primarias**: las fuerzas de extremo que ya tiene, más la carga de vano local `w` por barra y caso. La fórmula vive una sola vez, en un módulo sin dependencias, con gemelo en JS cruzado por un test con `node` |
| Qué se verifica y contra qué | **Nota de laboratorio + identidad de malla**; el signo de `Vy` queda fijado por equilibrio contra la convención de momento ya verificada. Solo la **torsión** y el signo de `Vz` quedan sin contraste externo, esperando SAP2000, y se declara explícito |
| Qué dibuja el visor | **Color por magnitud en todas las barras + diagrama normal al eje solo en la selección** (`filtro`), con selector de componente, escala declarada en el rótulo y valor en el tooltip |
| Compatibilidad | **`escena@2` reemplaza a `@1`**: se regenera el JSON versionado y el visor pasa a comprobar `esquema` (hoy no lo mira) |
| La sonda nueva | **Sí, en este lote**: `esfuerzo` con `x` o `x_rel`, para que la prosa del lote D pueda **citar** un esfuerzo del vano y no solo mirarlo |
| `x_grua = X_G_TOPE` | **Lote D**, con los demás casos de grúa |
| Dónde se publica | **Nota de `lab/` + la ficha del modelo en el sitio**; sin página nueva de serie |
| Segundo camino de la nota | **Equilibrio integrado en numpy + identidad de malla**; `Portico3D` en `ref.py` queda para cuando lo pida la nota B3 de la cola |

## 1 · La fórmula, y que exista una sola vez

Con `S = eleResponse(tag, "localForces")` —las fuerzas que los **nudos aplican a la barra**, en
ejes locales— y `w = (wx, wy, wz)` la carga uniforme en esos mismos ejes locales, los seis
esfuerzos a distancia `x` del extremo i son:

```
N(x)  = −S₀ − wx·x                    Mz(x) = S₅ − S₁·x − wy·x²/2
Vy(x) = −S₁ − wy·x                    My(x) = S₄ + S₂·x + wz·x²/2
Vz(x) = −S₂ − wz·x
T(x)  = −S₃
```

**No son una elección.** Salen del equilibrio del cuerpo libre `[0, x]` y son las **únicas**
funciones que valen, en `x = 0` y `x = L`, los valores de extremo que `analysis.signo_diagrama`
ya define y que los casos 6, 9 y 10 verificaron contra SAP2000:

    N  (tracción +)   i: −S₀   j: +S₆          My, Mz            i: +S₄₋₅   j: −S₁₀₋₁₁
    Vy, Vz, T                                  i: −S₁₋₃   j: +S₇₋₉

La asimetría entre `Mz` y `My` —el `−S₁·x` contra el `+S₂·x`— es real y viene de que los ejes
son dextrógiros: `ex × ey = ez` pero `ex × ez = −ey`. De ahí caen dos identidades que en este
plan son **tests, no comentarios**:

    dMz/dx = +Vy(x)          dMy/dx = −Vz(x)

Y con ellas, el argumento que cierra la verificación del corte sin SAP2000: si `Mz(x)` está
anclado en sus dos extremos a una convención de momento **ya verificada contra SAP2000**, el
signo de `Vy(x)` no se elige por analogía con la axial, queda **determinado** por la derivada
del momento. Lo mismo vale para `Vz` respecto de `My`, con el signo opuesto. Lo que no tiene
diagrama del cual derivarse es la **torsión**.

### Comprobación empírica hecha al diseñar

Sobre una barra vertical de 6 m con las tres componentes de `w` simultáneas, dos `vecxz`
distintos —`(1,0,0)` con el extremo j libre y `(0,1,0)` con j apoyado— y `Iy ≠ Iz`, las seis
funciones reproducen los doce valores de extremo a precisión de máquina, y las dos identidades
cierran a 1·10⁻⁹ (ruido de la diferencia finita). En la viga apuntalada de la `nota01`:
`Mz(x) = 45 − 37,5x + 5x²`, que da 0 en `x = L` y −25,3125 en `x = 3L/8`, o sea `9qL²/128` con
el signo del diagrama de Rukan —el opuesto al de tracción-abajo de `ref.py`, como la propia
`nota01` ya reconciliaba en su paso 6—.

### Dónde vive

- **`src/rukan/esfuerzos.py`** — módulo puro: no importa `openseespy` ni monta nada. Expone
  `esfuerzo(S, w, L, componente, x) -> float` y `diagrama(S, w, L, n) -> list[list[float]]`
  (los seis componentes en `n` estaciones equiespaciadas). Es la definición canónica.
- **`sitio/docs/visor/esfuerzos.js`** — su gemelo, **sin ningún import** (tampoco three.js),
  para que `node` lo cargue como módulo ES en un test. Lleva además `ejesLocales(pi, pj, vecxz)`,
  portado de `loads.local_axes`, que el visor necesita para dibujar el diagrama normal al eje.

Las barras con liberación de momento no son un caso especial: la fórmula es estática de cuerpo
libre, y una diagonal liberada en ambos extremos sale con `Mz(x) ≡ 0` por sus propias fuerzas
de extremo, sin que nadie se lo diga.

## 2 · El esquema `rukan/escena@2`

Cambia lo mínimo, y nada más:

```
barras[]    {id, nombre, i, j, seccion, vecxz[3]}          ← + vecxz
casos.<c>   {u, reacciones, fuerzas, w?}                   ← + w, opcional
combinaciones.<k>  lo mismo
```

- `w[k] = [wx, wy, wz]` en **ejes locales**, alineado con `barras[]`. El docstring declara que
  el orden es el de los ejes locales `(x, y, z)` y **no** el de `eleLoad -beamUniform`, que es
  `(Wy, Wz, Wx)`.
- La clave `w` **se omite entera** si el caso no tiene ninguna barra con carga de vano. Hoy solo
  la tiene `D` (peso propio distribuido); `H_alero`, `H_alero_uno` y `H_riel` son cargas nodales.
- En una combinación, `w` sale de la misma suma lineal que `u`, `reacciones` y `fuerzas`. Un caso
  sin `w` aporta ceros.
- `vecxz` es dato del modelo (primario), no derivado: el visor calcula `ey`, `ez` con
  `ejesLocales`, que el test con `node` cruza contra `loads.local_axes`. Emitir `ey` y `ez`
  costaría el doble de bytes y dejaría la convención de ejes sin test.

`ESQUEMA_ESCENA` sube a `"rukan/escena@2"`. **No hay convivencia**: la escena es un artefacto
generado cuyo único consumidor es el visor de este repo, y `tests/test_sitio.py` ata byte a byte
el **proyecto**, no la escena. El visor pasa a comprobar `esc.esquema` —hoy no lo mira— y a
fallar con un mensaje legible en el pie si no es `rukan/escena@2`. Se regenera
`sitio/docs/modelos/galpon-grua/galpon-grua.escena.json`: 1,50 → ~1,56 MB (+25 KB de `vecxz`, +37 KB de la `w` de `D`).

### De dónde sale `w`

Dos funciones nuevas, ninguna de las cuales toca OpenSees:

- **`loads.uniform_local_loads(model, gravity=(0,0,-1)) -> dict[int, tuple[float,float,float]]`** —
  el peso propio distribuido proyectado a los ejes locales de cada barra, que es exactamente lo
  que `self_weight_distributed` le pasa a `eleLoad`, pero devuelto en vez de aplicado. La
  proyección deja de estar escrita dos veces: `self_weight_distributed` pasa a consumirla.
- **`analysis.cargas_de_vano(p, caso) -> dict[int, tuple[float,float,float]]`** — `{}` salvo que
  el caso declare `peso_propio: "distribuido"`. El peso propio **nodal** no produce carga de vano,
  y las cargas nodales tampoco.

## 3 · La sonda `esfuerzo`

```json
"M_vano": {"que": "esfuerzo", "barra": "RAF3_2", "componente": "Mz",
           "x_rel": 0.39, "caso": "D"}
```

- `x` (metros desde el extremo i) o `x_rel` (0 a 1), **exactamente uno**; `io._validar_salidas`
  falla nombrando la salida si faltan los dos o vienen los dos, si `x_rel` cae fuera de `[0, 1]`
  o si `x` cae fuera de `[0, L]`.
- `componente` usa el vocabulario que ya existe (`io.COMPONENTES`), y `analysis.unidades` le da
  `kN` o `kN·m` con la misma regla que `fuerza`.
- La sonda `fuerza` **no se toca**: queda como el caso `x = 0` / `x = L`.
- `proyecto@1` **no cambia de versión**. Es vocabulario nuevo y aditivo: los proyectos existentes
  siguen cargando sin tocarlos.

El único cambio de fondo en `analysis.run`: los extractores pasan a construirse **dentro** del
bucle de casos, porque el extractor de un `esfuerzo` necesita la `w` de *ese* caso. Las
combinaciones siguen siendo `loads.combine` sobre floats, y eso es exacto porque el esfuerzo a
`x` fijo es **lineal** en el caso — la misma razón por la que `_lineal` de la escena puede
combinar `fuerzas`.

## 4 · El visor

Barra de herramientas: un selector **Esfuerzo** con `—`, `N`, `Vy`, `Vz`, `T`, `My`, `Mz`,
excluyente con `Modo` (un modo no tiene esfuerzos: se deshabilita).

- **Color**, sobre las 1 044 barras: rampa divergente con la paleta que ya existe —`frio`
  (`#2f5d7c`) negativo, `acento` (`#a4442c`) positivo, `linea` en cero—, cada barra subdividida
  en 8 tramos para que la parábola se vea y no se lea como una recta. Leyenda con los dos
  extremos rotulados.
- **Diagrama normal al eje**, solo para las barras que `filtro` selecciona. `filtro` son globs
  sobre el nombre de barra separados por coma (`filtro="RAF3_*,COL3A_*"`), por la misma razón por
  la que `vista.escena()` tiene `filtro`: 1 044 diagramas en una axonometría son una maraña
  ilegible. La ordenada va sobre el eje local **y** para `Mz`, `Vy`, `N` y `T`, y sobre el eje
  local **z** para `My` y `Vz`; se dibuja **con su signo tal cual**, no sobre la cara traccionada,
  que sería una segunda convención sin justificar.
- **Rótulo obligatorio** en el pie, como la deformada. Su forma —las cifras las pone la corrida,
  no este spec— es
  `<componente> · <caso> · máx |·| = <valor> <unidad> en <barra> (x/L = <fracción>) · ordenada máx = 5 % de la diagonal ×<factor>`.
  Un diagrama sin escala declarada es una figura que miente.
- **Tooltip**: al pasar sobre una barra, además de las doce fuerzas de extremo que ya muestra,
  el valor del componente seleccionado en la estación bajo el cursor, con su `x` en metros y su
  `x/L`.

Atributos nuevos del elemento: `esfuerzo` (componente inicial) y `filtro` (los globs). Una sola
regla, sin un tercer atributo que la duplique: **el diagrama normal se dibuja si y solo si hay
`filtro` y hay componente seleccionado**; sin `filtro`, el visor pinta color y nada más.

## 5 · Verificación

### La nota de laboratorio

`lab/nota07_esfuerzos_en_el_vano.py` — el 07 es el siguiente número libre (01, 02, 03 y 06 están
publicadas; 04 y 05 son huecos sin asignar y se dejan como están). Tres caminos, y la tabla del
post es la salida literal del script:

| Camino | Qué es | Independencia |
|---|---|---|
| `rukan/esfuerzos.py` | la fórmula cerrada que se verifica | — |
| `lab/_lib/ref.py` · `diagrama_por_integracion(S, w, L, n)` | numpy puro: integra `dV/dx = −w` y `dM/dx = V` desde el extremo i por sumas acumuladas, **sin** la fórmula cerrada | no importa `rukan` ni `openseespy` |
| OpenSees, malla ×16 | otro solve del mismo tramo: sus nudos interiores muestrean el mismo campo continuo | modelo distinto, sistema distinto |

Más la viga apuntalada cerrada de la `nota01` (`qL²/8`, `9qL²/128` en `3L/8`) extendida a los
seis componentes en 3D. La identidad de malla es exacta, no asintótica, y la `nota01` ya
estableció por qué: la solución de elementos finitos de una viga Euler-Bernoulli prismática con
carga uniforme es **exacta en los nudos**, así que refinar no converge — muestrea.

Figuras: el diagrama continuo contra la recta entre extremos, en 3D, con `lab/_lib/svg.py`.
`tests/test_lab.py` la descubre y la corre sola; `LAB.md` se actualiza con la fila de publicadas
y con la marca de la cola.

### Lo que queda esperando SAP2000, dicho explícito en tres lugares

`CLAUDE.md` ya dice que «corte y torsión de barra siguen la regla análoga a la axial y **no están
verificados contra SAP2000**; axial y momentos sí». Este plan **mejora** ese estado pero no lo
cierra, y la diferencia hay que decirla donde alguien la vaya a leer:

- **`## Límites` de la nota 07** y **docstring de `analysis.py`**: el signo de `Vy` queda
  determinado por `dMz/dx` contra una convención de momento verificada contra SAP2000; el de `Vz`
  por `dMy/dx` con el signo opuesto, que es consistencia interna y no contraste externo; la
  **torsión** no tiene diagrama del cual derivarse y sigue por analogía con la axial.
- **`## Límites` de `sitio/docs/modelos/galpon-grua/index.md`**: lo mismo, en una frase, junto al
  visor que dibuja esos esfuerzos.
- **`ROADMAP.md`**: `verification/case12` encolado, con lo que tiene que comparar cuando haya
  notebook del trabajo — los seis componentes en `x/L = 0; 0,25; 0,5; 0,75; 1` sobre una barra
  con carga de vano, en los dos planos locales, más torsión pura.

### Los tests

- **`tests/test_esfuerzos.py`** — los extremos reproducen los doce valores de `signo_diagrama`;
  las identidades `dMz/dx = +Vy` y `dMy/dx = −Vz`; la viga apuntalada contra la fórmula cerrada;
  la identidad de malla (1 elemento contra 16, con `vecxz` no trivial y las tres componentes de
  `w`); una barra con `w = 0` da `N`, `V`, `T` constantes y `M` lineal; una barra con los dos
  extremos liberados da `Mz(x) ≡ 0`.
- **`tests/test_esfuerzos_js.py`** — `node --input-type=module` carga `esfuerzos.js` y compara,
  sobre entradas aleatorias con semilla fija, `esfuerzo`, `diagrama` y `ejesLocales` contra
  `rukan.esfuerzos` y `loads.local_axes`. `pytest.skip` si no hay `node` en el `PATH`, como el
  test de `mkdocs` hace con `mkdocs`.
- **`tests/test_io.py` / `tests/test_analysis.py`** — la sonda `esfuerzo`: validación de `x` /
  `x_rel`, unidades, el valor contra `esfuerzos.esfuerzo` evaluado a mano, y que una combinación
  que la cite sea lineal en los casos.
- **`tests/test_escena.py`** — `vecxz` en cada barra; `w` presente solo en los casos con carga de
  vano; `w` de una combinación igual a la suma lineal; el esquema es `rukan/escena@2`.
- **`tests/test_sitio.py`** — sin cambios estructurales: el `sha256_proyecto` de la escena
  regenerada tiene que seguir cuadrando.
- **`mkdocs build --strict`** y captura del visor con `puppeteer-core` sobre
  `python -m http.server 8765` en `sitio/_build`, sin el prefijo `/rukan/`.

## 6 · Orden de implementación (TDD, un commit por paso)

1. **Spec** — este documento.
2. **`src/rukan/esfuerzos.py`** + `tests/test_esfuerzos.py`.
3. **`lab/nota07_esfuerzos_en_el_vano.py`** + `ref.diagrama_por_integracion` + figuras + `LAB.md`.
4. **`loads.uniform_local_loads`**, **`analysis.cargas_de_vano`** y la sonda **`esfuerzo`** en
   `io.py` / `analysis.py`, con sus tests.
5. **`escena@2`**: `vecxz` y `w` en `escena.py`, esquema arriba, `tests/test_escena.py`.
6. **`sitio/docs/visor/esfuerzos.js`** + `tests/test_esfuerzos_js.py`.
7. **El visor**: selector, color, diagrama con `filtro`, tooltip, chequeo de esquema; escena
   regenerada; `sitio/docs/modelos/galpon-grua/index.md` con el visor nuevo y su `## Límites`;
   `mkdocs build --strict` y captura mirada.
8. **Docs**: `CLAUDE.md` (estado, estructura, la frase de la torsión), `ROADMAP.md`
   (`verification/case12` encolado, lote C cerrado).

## 7 · Verificación del plan

- `pytest` en verde, con los tests nuevos y los existentes.
- `python -m lab.nota07_esfuerzos_en_el_vano` imprime sus tablas con error 0 % y termina en 0;
  cambiar un signo de `esfuerzos.py` la hace fallar nombrando la fila.
- `python -m rukan run` y `python -m rukan escena` sobre `galpon-grua.proyecto.json` corren y el
  `sha256_proyecto` cuadra.
- `mkdocs build --strict -f sitio/mkdocs.yml` en 0.
- En el navegador: el selector de esfuerzo pinta el galpón, el diagrama sale normal al eje sobre
  el marco filtrado, el pie declara la escala y el máximo con su barra y su `x/L`, y el tooltip
  da el valor bajo el cursor. Captura mirada, no solo generada.
- Prueba negativa: dejar la escena vieja (`@1`) en su sitio y comprobar que el visor lo dice en
  el pie en vez de dibujar cualquier cosa.

## 8 · Fuera de alcance

- **Los casos de carga que el lote D va a necesitar**: ruedas de grúa del 08, empujes del 07,
  nieve del 02, sismo estático, y `x_grua = X_G_TOPE` del 12. Los define el memo que los consume.
- **`Portico3D` en `lab/_lib/ref.py`** (rigidez 12×12 y rotación 3D en numpy): cuando lo pida la
  nota B3 de la cola —`vecxz` y el error silencioso de la transformación—, con la fuente en mano
  (Cook, Malkus & Plesha o Przemieniecki). Entonces se vuelve sobre la nota 07 a agregarle una
  cuarta columna.
- **`verification/case12`** contra SAP2000: encolado, necesita el notebook del trabajo.
- **Cargas de vano que no sean uniformes** (`-beamPoint`, trapezoidales): el modelo no las usa y
  ninguna las pide. La fórmula del § 1 vale solo para carga uniforme, y `esfuerzos.py` lo dice en
  su docstring.
- **Esfuerzos de un caso espectral**: la respuesta modal espectral es ±, y un diagrama con signo
  ambiguo es otra discusión. Fuera.

## 9 · Riesgos

- **Dos implementaciones de la misma fórmula.** Es el riesgo central del diseño elegido, y su
  mitigación es el paso 6: si el test con `node` no existe o queda saltado en CI, las dos se
  separan sin que nadie lo note. El test compara también `ejesLocales`, que es donde la
  divergencia sería más difícil de ver a ojo.
- **El signo de la torsión.** Queda por analogía, dicho en tres lugares. El riesgo de que alguien
  lea un `T` del visor y lo firme es real; por eso el límite va **junto al visor**, no solo en el
  spec.
- **Legibilidad del diagrama en 3D.** Sin eliminación de líneas ocultas, un diagrama normal al eje
  sobre un filtro amplio puede seguir siendo ilegible. Si pasa, se acota el filtro en la página;
  no se cambia el visor para taparlo.
- **El peso de la escena.** +62 KB es despreciable ahora, pero cada caso del lote D con carga
  distribuida suma otros ~37 KB. Si el lote D agrega muchos, la salida es bajar `CIFRAS` a 5 para
  `w`, que es una carga y no un resultado que se cite.
