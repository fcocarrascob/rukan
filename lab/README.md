# Laboratorio — notas de análisis estructural verificable

`verification/` valida **el motor** contra SAP2000, peldaño a peldaño. Esta
carpeta es la otra línea: **notas cortas sobre un fenómeno de análisis**, cada
una con una pregunta concreta y una referencia independiente. No dependen de
SAP2000, así que se escriben desde cualquier máquina.

El backlog priorizado y el índice nota ↔ post están en [`../LAB.md`](../LAB.md).

## La regla de los dos caminos

Toda nota resuelve el mismo problema **dos veces**:

1. **Referencia independiente** — fórmula cerrada citada a su fuente, o numpy
   puro (rigidez directa, autovalores, Newmark) en [`_lib/ref.py`](_lib/ref.py).
2. **OpenSeesPy** — el mismo problema en el motor.

`_lib/ref.py` **no importa `rukan` ni `openseespy`**. Es la restricción que hace
que la verificación signifique algo: si la referencia compartiera código con lo
verificado, ambas se equivocarían igual y la tabla daría error 0 % sin decir
nada.

Si un fenómeno no tiene referencia independiente, no entra al laboratorio.

## Cómo correr

```bash
pip install -e ".[dev]"                      # una vez, desde la raíz
python -m lab.nota01_eleload_empotramiento   # desde la raíz del repo
pytest                                       # corre todas las notas como regresión
```

Se corre con `python -m` desde la raíz (no `python lab/notaXX.py`) para que
`lab._lib` resuelva. El `conftest.py` de la raíz hace lo propio en `pytest`.

## Anatomía de una nota

Cada `notaNN_<slug>.py` es autocontenido y expone dos funciones:

- `main()` — el cálculo, la tabla y los `assert`. Es lo que corre `pytest`.
- `figuras()` — genera los SVG en `figs/`. Solo corre al ejecutar el script.

El docstring del archivo lleva la teoría y **la fuente citada**: regla no
negociable del repo (ver [`../CLAUDE.md`](../CLAUDE.md)). Si la fuente no está
a mano, se pide antes de escribir; no se calcula de memoria.

La comparación se arma con `_lib/report.py`, que imprime una **tabla markdown
pegable directo en el MDX** y verifica las tolerancias:

```python
from lab._lib.report import Fila, reportar

reportar("Momentos", [
    Fila("Momento de empotramiento", "kN·m", ref=M_ref, ops=M_ops),
    Fila("Rotación del empotramiento", "mrad", ref=0.0, ops=θ, tol_abs=1e-9),
])
```

La tabla del post es **copia literal de esa salida**, no transcrita a mano.

## Figuras

Se generan con `_lib/svg.py`, que reproduce la paleta y las proporciones de los
SVG ya publicados (560 px de ancho, fondo blanco —el sitio no tiene modo
oscuro—). La figura sale de la misma corrida que el número, así que no pueden
desincronizarse.

```bash
python -m lab.nota01_eleload_empotramiento                       # escribe figs/nota01-*.svg
python -m lab._lib.publish nota01 --slug lab-eleload-empotramiento
```

`publish` las copia a `../struct_pad/public/<slug>/` renombrando
`nota01-momentos.svg` → `fig-momentos.svg`.

## El molde del post

1. **La pregunta**, en una frase.
2. **Lo que dice la teoría** — fórmula cerrada, con la fuente.
3. **El camino independiente** (numpy / a mano).
4. **OpenSees**.
5. **La tabla** — salida literal del script.
6. **El veredicto**: qué hacer en la práctica y cuándo la trampa muerde.
7. **«Reproducir»** — `python -m lab.notaNN_slug` y el enlace al archivo exacto
   en GitHub.

En el blog: `section: "Laboratorio"`, sin `series` (las notas son
independientes), slug `lab-<tema>`.
