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
2 direcciones + CQC + 100/30) y **8** (peso propio, casos de carga y combinaciones,
galpón a dos aguas), todos con error ~0% vs SAP2000. El ensamblador `engine.py`
(Model 3D → OpenSees, con liberación de momentos), el análisis espectral propio
(`modal.py`: CQC/SRSS + `run_directional_spectral` + `directional_combination`
100/30) y las cargas (`loads.py`: peso propio distribuido/concentrado, masa
propia, casos y combinaciones) están verificados contra SAP2000. **Próximo paso:
Fase 1 (chequeo de código AISC/NCh427) o el espectro vertical NCh2369** — ver
`ROADMAP.md`. Los casos contra SAP2000 requieren el notebook del trabajo (MCP SAP2000).

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
```

## Estructura

```
src/rukan/
  units.py    # capa de unidades Pint + sistema interno
  model.py    # dataclasses del modelo (3D desde día 1)
  engine.py   # ensamblador Model 3D → dominio OpenSees
  loads.py    # peso propio, casos de carga y combinaciones
  modal.py    # análisis espectral propio: CQC/SRSS + direccional 100/30
  spectra.py  # espectro NCh2369
verification/ # escalera de casos: test + artefacto de blog (vs SAP2000)
lab/          # notas de análisis verificable (vs fórmula cerrada / numpy)
  _lib/       # report (tabla + assert), ref (numpy puro), svg, publish
  figs/       # SVG generados, se copian al blog
tests/        # tests unitarios del núcleo + corrida de cada nota
```
