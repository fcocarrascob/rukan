# Roadmap — Rukan

App opensource de análisis estructural sobre OpenSeesPy, alternativa a SAP2000
para ingeniería chilena. Desarrollo dirigido por verificación: cada peldaño es
un test de regresión **y** un post de blog en struct_pad.

---

## ✅ Caso 5 CERRADO — modal espectral NCh2369 vs SAP2000 (error ~0%)

El peldaño decisivo pasó. Pórtico plano de momento (1 vano, 2 pisos) armado con
`engine.build` y contrastado contra SAP2000 v25 (vía MCP): períodos, masas
modales efectivas, corte basal combinado (CQC y SRSS) y desplazamiento de techo,
todos con error **< 0.01 %**. La combinación modal CQC/SRSS **propia** de Rukan
(`src/rukan/modal.py`) reproduce SAP2000 a 4+ cifras.

- Espectro NCh2369 portado a Python: `src/rukan/spectra.py` (misma tabla `(T,
  Sa/g)` que se alimenta a ambos motores → verificación limpia).
- Caso: `verification/case05_modal_spectral_nch2369.py`.
- Modelo SAP + extracción: scripts MCP `case5_portico2p_build_run`,
  `case5_extract_results` (`case5_portico2p.sdb`).

**Claves aprendidas (SAP OAPI):** secciones con `PropFrame.SetGeneral` y **área
de corte = 0** desactivan la deformación por corte → igualan exactamente el
`elasticBeamColumn` (Euler-Bernoulli) de OpenSees. `ResponseSpectrum.SetLoads`
devuelve una **lista** `[...,0]` (no int); `SetModalComb_1` exige **F1 = 1.0**
(F1 = 0 → error). Factor de escala del caso RS = **9.80665** (g en m/s², modelo
en metros).

## ✅ Caso 6 CERRADO — arriostramiento y liberación de momentos vs SAP2000 (error ~0%)

Se agregó la **liberación de momentos en extremos** (`FrameElement.release_z_i/j`,
`release_y_i/j`) — la técnica con que se modelan las diagonales de
arriostramiento (conexión a corte/axial, sin transmitir momento). Pórtico de un
vano arriostrado bajo carga lateral, contrastado contra SAP2000: diagonal rígida
vs liberada, desplazamiento, axial y momentos, todos con error **< 0.01 %**. La
diagonal liberada coincide además con un elemento `Truss` puro.

- Caso: `verification/case06_braced_releases.py`.
- Modelo SAP: script MCP `case6_braced_bay_build` (`case6_braced_bay.sdb`,
  `FrameObj.SetReleases` con M2 y M3 liberados).

**Claves aprendidas:** en 3D OpenSees usa `-releasez` / `-releasey` (¡`-release`
a secas **se ignora en 3D**!; sí funciona en 2D). En SAP2000 la práctica 3D es
liberar **M2 y M3** en ambos extremos (rótula completa a flexión). Convención de
momento de extremo j: OpenSees da el momento nodal, el diagrama interno (SAP)
invierte el signo → `M3_diag = (Mz_i, -Mz_j)`.

## ✅ Caso 7 CERRADO — galpón 3D completo vs SAP2000 (error ~0%)

Cierra la escalera de verificación del MVP. Galpón rectangular (10×6×5 m) con
arriostramiento en cruz (diagonales **partidas en el cruce**, liberadas solo en
el extremo de columna — práctica real; una X-brace sin nodo de intersección en
SAP queda "desconectada"), sismo espectral NCh2369 en X e Y, y combinación
direccional **100/30**. Todo contra SAP2000 con error **< 0.01 %**.

- Respuesta espectral **general** en `modal.py` (`run_directional_spectral`):
  fuerzas estáticas equivalentes modo a modo → cualquier reacción/fuerza de
  barra combinada por CQC. Más `directional_combination` (100/30).
- Caso: `verification/case07_galpon3d_nch2369.py`. Build SAP:
  `case7_galpon3d_build` + `case7_galpon3d_rs` (`case7_galpon3d.sdb`).

## ✅ Caso 8 CERRADO — peso propio, casos de carga y combinaciones (galpón a dos aguas, error ~0%)

Análisis **indispensable**: todo modelo real es gravedad + otros casos, y sin
peso propio no hay memoria de cálculo. Introduce dos capacidades que Rukan aún
no tiene y que son la base de todo: **casos de carga** y **combinaciones**.
(Diseño acordado con el usuario; **aún no implementado** — este es el plan.)

**Modelo elegido — galpón a dos aguas (gable):** el caso típico y didáctico.
- **Transversal (Y):** marco a momento — columnas + dos dinteles inclinados que
  se juntan en la cumbrera. Bases articuladas (translaciones + torsión fijas,
  giros de flexión libres). Sin diagonales: resiste por acción de pórtico.
- **Longitudinal (X):** arriostrado — X-braces partidas en el cruce y liberadas
  solo en el extremo de columna (igual que el caso 7), en un vano longitudinal.
- **Techo arriostrado (diafragma):** diagonales horizontales en el plano del techo
  que conectan los marcos y forman un diafragma — reparte las cargas horizontales
  entre marcos y estabiliza la cumbrera/aleros longitudinalmente.
- **3 marcos transversales** (no 2) → 2 vanos longitudinales; da un modelo más
  interesante (marco central vs extremos, reparto por el diafragma de techo).
- **Fenómeno estrella:** bajo carga de techo/peso propio el pórtico **"se abre"**
  — los dinteles inclinados empujan las columnas hacia afuera (empuje horizontal
  en las bases + desplazamiento del alero). Ese empuje **nace de la carga
  gravitacional sobre el dintel inclinado**, así que es la demostración perfecta
  de por qué el peso propio hay que distribuirlo bien.
- **Geometría validada** (bosquejo del usuario en SAP, 38 barras / 21 nodos):
  luz transversal 6 m (X), alero 3 m, cumbrera 4 m (x=3, pendiente ~18°);
  **3 marcos** a y=0,6,12 (2 vanos de 6 m). Miembros: 6 columnas, 6 dinteles,
  cumbrera (5-10-15) y aleros longitudinales, X-braces de muro en el 1er vano
  (ambos muros) y 16 diagonales de techo (diafragma en ambas aguas, vía nodos
  intermedios 16–21). Secciones tubulares (I22=I33) para ejes 3D limpios.
- **Correcciones pendientes en el modelo antes de analizar** (validado 2026-07-09):
  1. **Apoyos: no hay** — falta restringir los 6 nudos base.
  2. **X-braces de muro sin partir**: 3-9 y 8-4 se cruzan en (6,3,1.5) sin nodo →
     partir en el cruce + liberar M2/M3 en el extremo de columna.
  3. **Cumbrera/aleros sin partir en los nodos 16–21**: esos nodos caen sobre las
     vigas (p.ej. 16 en el medio de la cumbrera 5-10) pero las vigas pasan de
     largo sin conectarse → el diafragma "flota". Partir cumbrera y aleros ahí.
  4. Diagonales de techo también se cruzan sin nodo (mismo tratamiento).
  (SAP: peso propio con `SetWeightAndMass` opción 1 y masa 0; el patrón DEAD debe
  tener multiplicador de peso propio = 1 — el probe dio 0, revisar.)

**Estado: verificado contra SAP2000 (~0%); falta solo el post.**
- `src/rukan/loads.py`: peso propio distribuido (proyección a ejes locales) /
  concentrado, `self_mass_lumped` (masa sísmica del peso propio), `run_static_case`,
  `spectral_case`, `combine`, `envelope`.
- `verification/case08_gable_loads.py`: galpón a dos aguas de 3 marcos armado en
  SAP + Rukan. Verificado: **chequeo modal** (períodos <0.01%), **4 casos** (D peso
  propio, Lr techo, E_X transversal, E_Y longitudinal) <0.02%, **apertura del
  pórtico** bajo peso propio, contraste distribuido vs concentrado (el momento del
  dintel se pierde al concentrar) y **combinaciones** 1.2D+1.6Lr, 1.2D±E_X.
- Modelos/scripts SAP MCP: `case8_gable_build`, `case8_gable_selfweight`,
  `case8_gable_modal`, `case8_gable_cases` (`case8_gable.sdb`).
- Clave: en SAP peso y masa están **acoplados** (peso=masa·g) → no se puede masa 0
  con peso ≠ 0; la masa sísmica sale del peso propio, concentrada en nudos (SAP lo
  hace igual → períodos coinciden). Suma de reacciones bajo RS es ambigua por
  signo/CQC (SAP suma magnitudes por columna); usar cantidades por nudo/elemento.
- **Post publicado** (parte 6 de la serie en struct_pad): peso propio y sus dos
  alcances, la apertura del pórtico, el chequeo modal, y combinar casos como en
  SAP2000. `src/content/blog/rukan-verificacion-peso-propio-combinaciones.mdx`.

**Para el post (indicaciones del usuario):**
- Explicar los **dos alcances** de distribución de peso propio: **distribuido**
  (esfuerzos correctos, momento del dintel) vs **en los extremos/nudos**
  (correcto para masa, pierde la flexión de la barra) — mostrar cuándo sirve cada uno.
- Incluir un **caso modal espectral** combinado con la gravedad, para mostrar que
  se combinan distintos casos como en SAP2000 (D + Lr + E). Si da para mucho,
  **partir en dos posts**.
- Mostrar el **chequeo de sanidad modal**: siempre conviene revisar el análisis
  modal (períodos, participación) para detectar errores/inconsistencias de los modos.

**Capacidades a construir en Rukan (`src/rukan/loads.py` nuevo):**
1. **Peso propio, DOS enfoques contrastados** (decisión del usuario):
   - **Distribuido** (correcto para esfuerzos): carga uniforme `w = ρ·A·g` sobre
     la barra vía `ops.eleLoad('-ele',tag,'-type','-beamUniform',Wy,Wz,Wx)`. OJO:
     el `beamUniform` de `elasticBeamColumn` es en **ejes locales** → hay que
     **proyectar la gravedad global (0,0,−w) a los ejes locales** de cada barra
     (replicar la convención de `geomTransf`: localX=(J−I)/L, localY=û(vecxz×localX),
     localZ=localX×localY). Para columnas la gravedad es axial (Wx); para vigas,
     transversal; para dinteles inclinados/diagonales, mixta.
   - **Concentrado en nudos** (lo que el usuario llamó "a las esquinas"): mitad
     del peso de cada barra a cada nudo extremo como fuerza −Z.
   - **La enseñanza central:** concentrar en nudos es lo correcto para la **MASA**
     sísmica (modal, casos 5 y 7) pero **pierde la flexión de la barra bajo su
     peso**; para los **esfuerzos estáticos** de gravedad hay que distribuir.
2. **Casos de carga** nombrados (D = peso propio, Lr = carga de techo, E = sismo)
   — correr varios patrones y guardar resultados por caso.
3. **Combinaciones** lineales: `combine({'D':1.2,'Lr':1.6})`, etc. Verificar
   esfuerzos combinados. Combos objetivo: 1.4D; 1.2D+1.6Lr; y gravedad+sismo
   (1.2D ± 1.0E, con E = caso RS ya verificado).
4. **Futuro (shells):** el mismo mecanismo — peso del shell (ρ·espesor·área)
   repartido a sus nudos de esquina.

**Verificación vs SAP2000 (qué comparar):**
- Reacciones bajo D: total vertical (= peso propio) y **empuje horizontal** en la
  base (Fy) — ambos enfoques dan el total, el distribuido da el empuje correcto.
- **Momento del dintel** bajo D: el distribuido reproduce SAP (parábola por peso
  propio); el concentrado da ~0 → el contraste didáctico.
- **Apertura del pórtico**: desplazamiento horizontal del alero bajo D+Lr.
- Esfuerzos bajo combinaciones (1.2D+1.6Lr; 1.2D±E) vs combos de SAP (`RespCombo`).

**Nota SAP:** material con densidad de **peso** (`SetWeightAndMass` opción 1 =
76.98 kN/m³ para acero) pero **masa = 0** (opción 2), para que el peso propio
cargue pero el modal siga usando solo las masas explícitas de nudo (como caso 7).

## ▶ PRÓXIMA SESIÓN — candidatos

1. **Fase 1 — Chequeo de código** (AISC 360 / NCh427 por elemento): el valor que
   se paga. Con el análisis ya verificado (casos 1–8), viene "la otra mitad":
   tracción/compresión+pandeo (esbeltez KL/r de la diagonal, ya con la longitud
   de pandeo partida en el cruce), flexión, interacción H1, + memoria de cálculo.
2. **Espectro vertical NCh2369**: falta para el galpón "completo"; necesita
   flexibilidad vertical real. `computeVerticalSpectrum` (factor 0.7, período
   1.7·T) ya está en struct_pad; portar a `spectra.py`.
3. **Base de perfiles chilenos** (catálogo ICHA) para dejar de teclear A/I/J.

---

## Wedge 1 — Acero industrial NCh2369 (MVP)

### Fase 0 — Núcleo headless (sin GUI)
- [x] Capa de unidades (Pint en la frontera + sistema interno consistente)
- [x] Modelo de datos 3D (dataclasses)
- [x] Constructor OpenSees desde el modelo (`engine.py`) — 3D, verificado vs voladizo analítico
- [ ] Base de perfiles chilenos (catálogo ICHA: IN, HN, cajón, tubos, ángulos, XL)
- [x] Análisis estático y modal
- [x] Espectro NCh2369 + análisis espectral (combinación CQC/SRSS propia) — vs SAP2000, error ~0%
- [x] **Peso propio + casos de carga + combinaciones** (Caso 8, galpón a dos aguas) — vs SAP2000, error ~0%
- [x] Combinaciones de carga (NCh3171 / NCh2369) — cubierto por el Caso 8

### Escalera de verificación
1. [x] Columna en voladizo (1 GDL) — vs fórmula a mano
2. [x] Pórtico de corte 2 GDL — vs fórmula a mano (razón áurea, masas 94.7/5.3%)
3. [x] Reticulado triangular isostático — vs mano (método de los nudos)
4. [ ] Pórtico plano gravitacional — vs SAP2000
5. [x] **Modal espectral 2D (NCh2369)** — vs SAP2000, error ~0% (RSA + CQC/SRSS propio)
6. [x] **Arriostramiento / liberación de momentos** — vs SAP2000, error ~0% (biela axial = Truss)
7. [x] **Galpón 3D completo** — vs SAP2000, error ~0% (2 direcciones + CQC + 100/30; falta vertical)
8. [x] **Peso propio, casos de carga y combinaciones** (galpón a dos aguas, 3 marcos + techo arriostrado) — vs SAP2000, error ~0%

### Fase 1 — Chequeo de código (el valor que se paga)
- [ ] Verificación AISC 360 / NCh427 por elemento (tracción, compresión+pandeo, flexión, interacción H1)
- [ ] Límites NCh2369 (esbeltez de diagonales KL/r, deformaciones sísmicas)
- [ ] Reporte / memoria de cálculo automática

### Fase 2 — GUI
- [ ] Constructor de modelo (empezar en 2D → galpón por marcos)
- [ ] Visor de resultados (pyvista/VTK o webview three.js)
- [ ] PySide6

## Wedge 2 — Edificios de hormigón NCh433 (expansión, no MVP)
- [ ] Muros de corte por **columna ancha** (equivalent frame) — camino pragmático primero
- [ ] Diafragmas rígidos, losas
- [ ] Muros shell / MVLEM + pushover no lineal (madurez, diferenciador de largo plazo)

## Riesgos técnicos a clavar temprano
- **RSA + combinación modal**: OpenSees no hace análisis espectral "de un
  botón"; la combinación CQC/direccional (100/30) se implementa y valida a mano
  (peldaño 5).
- **Unidades**: fuente #1 de error en OpenSees — mitigado con la capa Pint.
- **Base de perfiles**: digitalizar el catálogo ICHA una vez.
