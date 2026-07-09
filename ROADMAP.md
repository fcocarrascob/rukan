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

## ▶ PRÓXIMA SESIÓN — candidatos

1. **Espectro vertical NCh2369**: falta para el galpón "completo"; necesita
   flexibilidad vertical real (nudos a media luz de vigas largas con masa, o
   arriostramiento de techo). `computeVerticalSpectrum` (factor 0.7, período
   1.7·T) ya está en struct_pad; portar a `spectra.py`.
2. **Fase 1 — Chequeo de código** (AISC 360 / NCh427 por elemento): el valor que
   se paga. Empezar por tracción/compresión+pandeo (esbeltez KL/r de la diagonal,
   que ya se modela bien, ahora con la longitud de pandeo partida en el cruce).
3. **Pórtico plano gravitacional vs SAP2000** (pendiente; estática de marcos con
   vigas cargadas).
4. **Base de perfiles chilenos** (catálogo ICHA) para dejar de teclear A/I/J.

---

## Wedge 1 — Acero industrial NCh2369 (MVP)

### Fase 0 — Núcleo headless (sin GUI)
- [x] Capa de unidades (Pint en la frontera + sistema interno consistente)
- [x] Modelo de datos 3D (dataclasses)
- [x] Constructor OpenSees desde el modelo (`engine.py`) — 3D, verificado vs voladizo analítico
- [ ] Base de perfiles chilenos (catálogo ICHA: IN, HN, cajón, tubos, ángulos, XL)
- [x] Análisis estático y modal
- [x] Espectro NCh2369 + análisis espectral (combinación CQC/SRSS propia) — vs SAP2000, error ~0%
- [ ] Combinaciones de carga (NCh3171 / NCh2369)

### Escalera de verificación
1. [x] Columna en voladizo (1 GDL) — vs fórmula a mano
2. [x] Pórtico de corte 2 GDL — vs fórmula a mano (razón áurea, masas 94.7/5.3%)
3. [x] Reticulado triangular isostático — vs mano (método de los nudos)
4. [ ] Pórtico plano gravitacional — vs SAP2000
5. [x] **Modal espectral 2D (NCh2369)** — vs SAP2000, error ~0% (RSA + CQC/SRSS propio)
6. [x] **Arriostramiento / liberación de momentos** — vs SAP2000, error ~0% (biela axial = Truss)
7. [x] **Galpón 3D completo** — vs SAP2000, error ~0% (2 direcciones + CQC + 100/30; falta vertical)

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
