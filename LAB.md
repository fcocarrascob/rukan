# LAB — backlog del laboratorio

Notas de análisis estructural verificable: una pregunta, dos caminos
independientes, un script permanente. La convención está en
[`lab/README.md`](lab/README.md); esta es la cola de temas y el índice de lo
publicado.

**Criterio de admisión:** una nota entra solo si tiene una **referencia
independiente** — fórmula cerrada citada o numpy puro. Sin patrón contra el cual
medir, no hay nota.

**Formato:** mayoría de notas cortas (~700–1000 palabras, una figura, una idea);
cada tanto un hito largo cuando el tema lo pide.

---

## Publicadas

| Nota | Script | Post | Fecha |
|---|---|---|---|
| 01 · El momento del vano no está en la salida del elemento | `lab/nota01_eleload_empotramiento.py` | [`lab-eleload-empotramiento`](https://fcocarrascob.github.io/blog/lab-eleload-empotramiento/) | 2026-08-03 |
| 02 · Mp = Z·Fy es una asíntota que nunca se toca | `lab/nota02_momento_curvatura_acero.py` | [`lab-momento-plastico-asintota`](https://fcocarrascob.github.io/blog/lab-momento-plastico-asintota/) | 2026-08-03 |
| 03 · El triángulo bajo la zapata no depende de la rigidez del suelo | `lab/nota03_zapata_sin_traccion.py` | [`lab-zapata-sin-traccion`](https://fcocarrascob.github.io/blog/lab-zapata-sin-traccion/) | 2026-08-05 |

---

## Cola

### A · Dinámica y amortiguamiento

| # | Nota | Referencia independiente | Estado |
|---|---|---|---|
| A1 | Rayleigh: qué amortiguamiento reciben los modos que **no** anclaste | ξᵢ = a₀/2ωᵢ + a₁ωᵢ/2 a mano, y ξ medido por decremento logarítmico en vibración libre | ⬜ |
| A2 | Masa consistente vs concentrada: cuántos elementos por barra | Solución exacta de viga continua (βL = 1.8751, 4.6941…) + numpy con masa consistente | ⬜ |
| A3 | CQC vs SRSS: cuánto importan los modos cercanos | ρᵢⱼ cerrado (Der Kiureghian) + barrido de separación de frecuencias | ⬜ |
| A4 | Masa modal faltante y el modo residual: ¿basta el 90 %? | Σ masas modales = masa total + corrección estática | ⬜ |
| A5 | Participación modal vs masa modal efectiva (la confusión clásica) | 2 GDL a mano | ⬜ |

### B · Trampas de modelación

| # | Nota | Referencia independiente | Estado |
|---|---|---|---|
| B1 | `eleLoad` y los momentos de empotramiento que hay que devolverle a la barra | wL²/8 y 9wL²/128 de la viga apuntalada, a mano | ✅ nota 01 |
| B2 | Área de corte: cuándo Timoshenko se separa de Euler-Bernoulli | δ = PL³/3EI + PL/GAs, barrido L/d | ⬜ |
| B3 | `vecxz` y la transformación geométrica en 3D: el error silencioso | matriz de rotación en numpy vs fuerzas locales de OpenSees | ⬜ |
| B4 | Diafragma rígido: `rigidDiaphragm` vs `equalDOF` vs vigas rígidas | centro de rigidez a mano, piso con 3 marcos | ⬜ |

### C · Estabilidad y no lineal

| # | Nota | Referencia independiente | Estado |
|---|---|---|---|
| C1 | Pandeo por autovalores: K − λK_g contra π²EI/(KL)² | fórmula de Euler + `K_g` ensamblada en numpy | ⬜ |
| C2 | El K del nomograma contra el pandeo real del marco | alignment chart AISC vs autovalor | ⬜ |
| C3 | P-Delta: cuándo 1/(1−θ) deja de servir | amplificador cerrado vs análisis geométrico no lineal | ⬜ |
| C4 | Análisis límite: mecanismo de colapso a mano vs pushover **(hito largo)** | método de los mecanismos (carga de colapso cerrada) | ⬜ |

### D · Del registro al espectro

| # | Nota | Referencia independiente | Estado |
|---|---|---|---|
| D1 | Newmark a mano vs el integrador de OpenSees | Duhamel cerrado para un pulso + Newmark β=¼ en numpy | ⬜ |
| D2 | Construir un espectro de respuesta desde un acelerograma y compararlo con NCh2369 | SDOF × N períodos en numpy | 🔒 falta el registro y su procedencia |
| D3 | La forma espectral con ξ = 2 %, 3 %, 5 %: qué dice NCh2369 y qué da el cálculo | espectro calculado vs curva de la norma (`src/rukan/spectra.py`) | ⬜ |
| D4 | Disipación numérica: HHT-α y el paso de tiempo | vibración libre cerrada, decaimiento espurio medido | ⬜ |

### E · Secciones

| # | Nota | Referencia independiente | Estado |
|---|---|---|---|
| E1 | `Mp = Z·Fy` es una asíntota que nunca se toca | M(φ) cerrada del perfil I elastoplástico, derivada + suma de fibras en numpy | ✅ nota 02 |
| E2 | Interacción P-M de un perfil I: la H1-1 del AISC contra la superficie plástica exacta | superficie plástica cerrada (eje neutro en el alma vs en el ala) | ⬜ |
| E3 | Momento-curvatura de hormigón armado: lo que compra el confinamiento | fibras en numpy con la σ-ε publicada (no confinado vs confinado) | 🔒 falta Mander (1988) / Kent-Park |
| E4 | Endurecimiento: qué cambia pasar de elastoplástico perfecto a bilineal con b = 1–3 % | suma de fibras en numpy, contra el caso b = 0 ya cerrado de la nota 02 | ⬜ |

### F · Suelo y fundaciones

Bloque abierto por la nota 03. Es el único donde la **falta de fuente en disco**
manda sobre el orden: el reparto bajo zapata rígida está cubierto por Das, pero
todo lo que necesite el módulo de balasto como propiedad del suelo está
bloqueado. Das no menciona balasto ni Winkler en sus 658 páginas, y Hetényi,
Bowles, Poulos & Davis y Terzaghi no están en disco en ningún formato.

| # | Nota | Referencia independiente | Estado |
|---|---|---|---|
| F1 | La zapata que se despega: el triángulo no depende de k_s, y la superposición muere | Das §16.7, Ecs. (16.20)–(16.22) + longitud de contacto derivada | ✅ nota 03 |
| F2 | Excentricidad bidireccional: reparto lineal vs área efectiva de Meyerhof | Das §16.9, Ecs. (16.23)–(16.25) — **está en disco** | ⬜ |
| F3 | Zapata rígida vs flexible: dónde deja de valer el reparto lineal | criterio de la Ec. (25) de NCh2369:2025 §10.1.5 (leerla rasterizada) + barrido de EI | ⬜ |
| F4 | Viga sobre fundación elástica: la longitud característica y cuándo λL manda | solución cerrada de Hetényi | 🔒 falta Hetényi o Bowles |
| F5 | k_s no es una propiedad del suelo: depende del ancho de la zapata | corrección de Terzaghi (1955) por ancho | 🔒 falta Terzaghi o Bowles |
| F6 | Winkler contra el semiespacio elástico: el punzón rígido tiene presión infinita en el borde | solución cerrada de Boussinesq para el punzón rígido | 🔒 falta Poulos & Davis |

**Orden sugerido:** B1 ✅ → E1 ✅ → F1 ✅ → A1 → C1 → A2, y C4 como primer hito
largo. F2 y F3 se pueden escribir hoy; F4, F5 y F6 no, hasta conseguir el libro.

---

## Fuentes a tener a mano antes de escribir

Regla no negociable del repo: la disposición o la fórmula se consulta en la
fuente, no se recuerda.

| Notas | Fuente |
|---|---|
| A1, A2, D1, D4 | Chopra, *Dynamics of Structures* — Rayleigh, masa consistente, Newmark, disipación numérica |
| A3 | Der Kiureghian (1981) — coeficiente de correlación de CQC |
| B1, B2 | Hibbeler, *Structural Analysis*; AISC *Manual* Tabla 3-22 (diagramas y fórmulas de vigas) |
| C1, C2 | AISC 360, Comentario Cap. C y Apéndice 7 — longitud efectiva y análisis de pandeo |
| D2 | **el acelerograma y su procedencia — pedirla, no asumirla** |
| D3 | NCh2369 (espectro de diseño) |
| E2 | AISC 360, Cap. H — ecuación de interacción H1-1 |
| E3 | **Mander, Priestley & Park (1988) y/o Kent & Park — pedirlos, no recordarlos** |
| F1, F2 | Das, *Fundamentos de Ingeniería Geotécnica*, 4.ª ed., §16.7 y §16.9 — `F:\OneDrive\Ingenieria\Libros\Braja_Das.pdf`, PDF pp. 511-522 (offset +21). Contraparte estructural del mismo teorema: AISC *Design Guide 1*, 3.ª ed., Ap. B §B.2.3 |
| F1, F3 | NCh2369:2025, cláusula 10 — área apoyada mínima (§10.1.4), deslizamiento sobre el área en compresión (§10.1.3), fundaciones flexibles (§10.1.5) y ancladas (§10.1.6) |
| F4, F5, F6 | **Hetényi, Bowles, Terzaghi, Poulos & Davis — ninguno está en disco; conseguirlos antes de escribir** |

E1 y E4 no necesitan fuente externa: la M(φ) elastoplástica es mecánica de
sección —equilibrio, Navier y la ley constitutiva—, así que se **deriva** en el
docstring y queda auditable, en vez de citarse. La regla vale para disposiciones
normativas y datos tabulados, no para lo que se puede demostrar en el archivo.
