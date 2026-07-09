# Rukan

**Análisis estructural opensource para ingeniería chilena**, con
[OpenSeesPy](https://openseespydoc.readthedocs.io/) como motor — una
alternativa económica a SAP2000 para ingenieros independientes que trabajan
estructuras simples y cotidianas (análisis modal, espectral, pushover).

*Rukan* viene de *ruka* (casa / estructura, en mapudungun).

## Estado

En desarrollo temprano. Wedge inicial: **estructuras de acero industriales
NCh2369** (galpones). Ver [`ROADMAP.md`](ROADMAP.md).

## Filosofía: transparencia y verificación

Ningún ingeniero firma cálculos de una caja negra. Por eso Rukan:

- Genera análisis **legibles y auditables** (no oculta el modelo OpenSees).
- Se construye por **Desarrollo Dirigido por Verificación**: cada capacidad
  nace de un caso que se contrasta contra cálculo a mano y/o SAP2000, y se
  publica como post en [struct_pad](https://fcocarrascob.github.io).

## Instalación

Requiere Python ≥ 3.10.

```bash
pip install -e ".[dev]"
```

## Uso

```bash
pytest                                            # tests del núcleo
python verification/case01_cantilever_column.py   # caso de verificación
```

## Estructura

```
src/rukan/
  units.py    # capa de unidades (Pint en la frontera) + sistema interno
  model.py    # modelo de datos estructural (3D desde el día 1)
verification/ # escalera de casos de verificación (test + artefacto de blog)
tests/        # tests unitarios
```

## Licencia

MIT.
