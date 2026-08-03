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
| 2 | Pórtico de corte 2 GDL | períodos, modos, participación | mano | ✅ |
| 3 | Reticulado triangular | fuerzas axiales | mano | ✅ |
| 4 | Pórtico plano gravitacional | deflexiones, momentos | SAP | ⬜ (absorbido por el 8) |
| 5 | Modal espectral 2D (NCh2369) | Sa, CQC/SRSS, corte basal | SAP | ✅ |
| 6 | Arriostramiento / liberación de momentos | axial, momentos, biela = Truss | SAP | ✅ |
| 7 | Galpón 3D completo | 2 direcciones, CQC, 100/30 | SAP | ✅ |
| 8 | Peso propio, casos y combinaciones | peso distribuido/concentrado, combinaciones | SAP | ✅ |

Los casos contra SAP2000 se armaron en el **notebook del trabajo** (vía MCP de
SAP2000); acá quedan con los valores de referencia ya extraídos, así que corren
en cualquier máquina.

Ver el detalle y las fases en [`../ROADMAP.md`](../ROADMAP.md).

## La otra línea: `lab/`

`verification/` valida **el motor**. Las notas de [`../lab/`](../lab/) exploran
**fenómenos de análisis** —cada una con una referencia independiente en numpy o
a mano— y no dependen de SAP2000. Ver [`../LAB.md`](../LAB.md).
