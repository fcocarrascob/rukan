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

## ▶ PRÓXIMA SESIÓN — candidatos

1. **Caso 6 — Galpón 3D completo vs SAP2000**: subir de 2D a 3D real (dos
   direcciones, combinación direccional **100/30**, espectro vertical). Cierra
   la escalera de verificación del MVP.
2. **Caso 4 — Pórtico plano gravitacional vs SAP2000** (quedó pendiente; estática
   de marcos con vigas cargadas, momentos y cortes).
3. **Fase 1 — Chequeo de código** (AISC 360 / NCh427 por elemento): el valor que
   se paga. Empezar por tracción/compresión+pandeo.

**Riesgo técnico próximo:** la combinación **direccional (100/30)** aún no se
implementa; el espectro **vertical** NCh2369 ya está portado en `spectra.py`
(struct_pad lo tiene como `computeVerticalSpectrum`, factor 0.7 y período 1.7·T).

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
6. [ ] Galpón 3D completo — vs SAP2000

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
