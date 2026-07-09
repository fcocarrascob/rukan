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
5. Modal espectral 2D (NCh2369) — vs SAP  ← riesgo técnico: RSA + CQC es manual
6. Galpón 3D completo — vs SAP

Regla de contenido: teoría + cálculo a mano donde ilumina (casos 1-3); a partir
del caso 4-5 el cálculo a mano deja de ser tractable y SAP2000 pasa a ser el
patrón de referencia. No forzar cálculo manual donde no aporta.

## Comandos

```bash
pip install -e ".[dev]"                       # instala Rukan editable + pytest
pytest                                        # tests unitarios (units, modelo)
python verification/case01_cantilever_column.py   # corre un caso de verificación
```

## Estructura

```
src/rukan/
  units.py    # capa de unidades Pint + sistema interno
  model.py    # dataclasses del modelo (3D desde día 1)
verification/ # escalera de casos: test + artefacto de blog
tests/        # tests unitarios del núcleo
```
