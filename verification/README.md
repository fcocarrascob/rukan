# Casos de verificación

Cada archivo `caseNN_*.py` es autocontenido y verificable: imprime la
comparación entre el resultado de OpenSees y la referencia (cálculo a mano y/o
SAP2000), y falla con `assert` si la discrepancia excede la tolerancia. Cada
caso es, a la vez, un **test de regresión** y el borrador de un **post de blog**
en struct_pad.

## Cómo correr

```bash
pip install -e ".[dev]"                            # desde la raíz del repo
python verification/case01_cantilever_column.py
```

## La escalera

| # | Caso | Verifica | Contra | Estado |
|---|------|----------|--------|--------|
| 1 | Columna en voladizo (1 GDL) | período, rigidez lateral | mano | ✅ |
| 2 | Pórtico de corte 2 GDL | períodos, modos, participación | mano | ⬜ |
| 3 | Reticulado simple | fuerzas axiales | mano / SAP | ⬜ |
| 4 | Pórtico plano gravitacional | deflexiones, momentos | SAP | ⬜ |
| 5 | Modal espectral 2D (NCh2369) | Sa, CQC/SRSS, corte basal | SAP | ⬜ |
| 6 | Galpón 3D completo | derivas, esfuerzos, límites | SAP | ⬜ |

Ver el detalle y las fases en [`../ROADMAP.md`](../ROADMAP.md).
