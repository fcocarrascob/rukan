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
| 9 | Torre CBF/MRF, espectro por dirección (NCh2369:2025) | R* con T* por dirección (Ec. 1b), 5 casos RS, banda §5.12–§5.13, R₁ | SAP | ✅ |
| 10 | **Galpón del altiplano** — 105 nodos, 188 barras, peralte variable, 11 estados, 79 combinaciones | peso de acero, equilibrio de los 11 estados, momentos de un marco hiperestático, modal de 60 modos, T\* de las dos direcciones, R\*, Q₀ y las tres envolventes miembro a miembro | SAP | ✅ |

Los casos contra SAP2000 se armaron en el **notebook del trabajo** (vía MCP de
SAP2000); acá quedan con los valores de referencia ya extraídos, así que corren
en cualquier máquina.

El **caso 10 se construyó sin SAP2000 delante**, y es el que prueba que eso se
puede: el modelo de referencia vive congelado en las cabeceras `# Result:` de
`Skills_SAP/scripts/galpon_altiplano_*.py` y en la memoria de cálculo
`struct_pad/SERIE-GALPON.md`. Sus datos están separados en
[`case10_data.py`](case10_data.py), que no importa OpenSees y por eso sirve igual
como entrada de una referencia independiente.

Encontró además una diferencia real, de las que no aparecen mirando resultados:
el período fundamental salía **3,66 % largo** con la rigidez verificada exacta
(los momentos de un marco hiperestático coinciden a la sexta cifra). La causa es
que SAP deja los **pilares de hastial fuera de la matriz de masa** —arrastra al
armado de la masa la liberación axial de su extremo superior—, así que la
estructura sacude 582 kN y no los 674,9 kN que la memoria declara como masa
sísmica. Ver `SERIE-GALPON.md` §5.46.

Ver el detalle y las fases en [`../ROADMAP.md`](../ROADMAP.md).

## La otra línea: `lab/`

`verification/` valida **el motor**. Las notas de [`../lab/`](../lab/) exploran
**fenómenos de análisis** —cada una con una referencia independiente en numpy o
a mano— y no dependen de SAP2000. Ver [`../LAB.md`](../LAB.md).
