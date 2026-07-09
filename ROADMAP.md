# Roadmap — Rukan

App opensource de análisis estructural sobre OpenSeesPy, alternativa a SAP2000
para ingeniería chilena. Desarrollo dirigido por verificación: cada peldaño es
un test de regresión **y** un post de blog en struct_pad.

## Wedge 1 — Acero industrial NCh2369 (MVP)

### Fase 0 — Núcleo headless (sin GUI)
- [x] Capa de unidades (Pint en la frontera + sistema interno consistente)
- [x] Modelo de datos 3D (dataclasses)
- [ ] Constructor OpenSees desde el modelo (`engine.py`) — cuando el caso 2 lo justifique
- [ ] Base de perfiles chilenos (catálogo ICHA: IN, HN, cajón, tubos, ángulos, XL)
- [ ] Análisis estático y modal
- [ ] Espectro NCh2369 + análisis espectral (combinación CQC/SRSS propia)
- [ ] Combinaciones de carga (NCh3171 / NCh2369)

### Escalera de verificación
1. [x] Columna en voladizo (1 GDL) — vs fórmula a mano
2. [ ] Pórtico de corte 2 GDL — vs fórmula a mano
3. [ ] Reticulado simple — vs mano / SAP2000
4. [ ] Pórtico plano gravitacional — vs SAP2000
5. [ ] **Modal espectral 2D (NCh2369)** — vs SAP2000 · *riesgo: RSA + CQC manual*
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
