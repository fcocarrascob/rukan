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
- Publica sus modelos con su narración en 3D en
  [el sitio de Rukan](https://fcocarrascob.github.io/rukan/): cada entrada es un
  archivo de proyecto que se corre, y lo que se dibuja y se escribe sale de esa corrida.
  Las **series** encadenan eslabones de diseño sobre un mismo modelo; la primera es el
  galpón con puente grúa por NCh2369.

## Instalación

Requiere Python ≥ 3.10.

```bash
pip install -e ".[dev]"
```

## Uso

```bash
pytest                                            # tests del núcleo
python verification/case01_cantilever_column.py   # caso de verificación
python -m rukan run    <p>.proyecto.json          # corre un archivo de proyecto
python -m rukan escena <p>.proyecto.json          # y escribe la escena que dibuja el visor
pip install -e ".[sitio]" && mkdocs serve -f sitio/mkdocs.yml   # el sitio en local
```

## Estructura

```
src/rukan/
  units.py    # capa de unidades (Pint en la frontera) + sistema interno
  model.py    # modelo de datos estructural (3D desde el día 1)
verification/ # escalera de casos de verificación (test + artefacto de blog)
sitio/        # el sitio: modelos con su narración y visor 3D (MkDocs + three.js)
tests/        # tests unitarios
```

## Licencia

MIT.
