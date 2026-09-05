# Plan — El puente Rukan ↔ memos: un archivo de proyecto que se corre, se cita y se audita

## Contexto

Los memos de `F:\Proyectos_Python\Guias_Interactivas` hoy pueden citar un resultado de
análisis de dos formas: **declarado** (`Sn`) o **corrido** (`Mn`, respaldado por
`## Modelo` y por `_kit/verify_modelo.py`, que cruza cada fila de `## Sale` contra un JSON
que Rukan emite). La maquinaria del lado de los memos existe desde el 2026-09-04, pero:

- **Ningún memo la usa todavía.** El `00-el-modelo` de la serie `nch2369-galpon-grua` está
  pendiente (`memos/_serie-nch2369-galpon-grua.md:104-115`).
- **El puente es artesanal.** El caso 11 de Rukan emite su JSON con un `emitir_json` escrito
  a mano; cada serie nueva exigiría otro `caseNN` con su propio `emitir_json`.
- **`Model` no se serializa.** El principio "config → script" de `CLAUDE.md` es aspiracional:
  no hay `to_dict`/`from_dict`, ni nombres en nudos y barras (el caso 11 los guarda en una
  clase `Meta` aparte).
- **Las figuras del caso 11 no las regenera nadie** (`verification/figs/case11-*.svg` están
  committeadas sin script), lo que rompe la regla de procedencia que el propio JSON cita.

Lo que se quiere a futuro es una app tipo SAP2000 sobre Rukan. **Un modelo serializable
con casos, análisis y salidas es exactamente el documento que esa GUI editaría**, así que
este puente es la base de la Fase 2 y no un desvío.

## Decisiones tomadas con el usuario (2026-09-05)

| Decisión | Elegido |
|---|---|
| Qué se diseña primero | El puente Rukan ↔ memos (antes que GUI o Fase 1) |
| Dueño de la definición del modelo | **Archivo junto al memo**, en el repo de memos |
| Formato | **JSON**, sin dependencias nuevas |
| Contenido del archivo | **Proyecto completo**: modelo + casos + análisis + salidas. `python -m rukan run` no toma opciones |
| Geometría paramétrica del galpón | **Sigue en Rukan** (`verification/case11_data.py`); un generador en el repo de memos la importa vía `RUKAN_ROOT` y escribe el JSON |
| Alcance de este plan | Rukan + memo 00. La cascada 04→13 queda para después |

## Diseño

### 1. El archivo de proyecto — esquema `rukan/proyecto@1`

Un JSON, todo en el sistema interno (m, kN, t) salvo que `unidades` diga otra cosa, en
cuyo caso `io.load` convierte en la frontera con los factores de `src/rukan/units.py`.

```json
{
  "esquema": "rukan/proyecto@1",
  "titulo": "Galpón con puente grúa — nch2369-galpon-grua-00",
  "unidades": {"longitud": "m", "fuerza": "kN", "masa": "t"},
  "materiales": [{"id": 1, "E": 2.0e8, "nu": 0.3, "rho": 7.85}],
  "secciones":  [{"id": 1, "nombre": "COL_0.52500", "A": 0.0273, "Iy": 4.7e-3, "Iz": 3.1e-5, "J": 1.2e-6}],
  "nudos":  [{"id": 1, "nombre": "K1A_0", "x": 0, "y": 0, "z": 0, "fijo": [1,1,1,1,1,1]}],
  "barras": [{"id": 1, "nombre": "COL1A_1", "i": 1, "j": 2, "material": 1, "seccion": 1,
              "vecxz": [1,0,0], "libera": {"z_i": false, "z_j": false, "y_i": false, "y_j": false}}],
  "masas":  [{"nudo": "R1_0", "valores": [2.1, 2.1, 2.1, 0, 0, 0]}],
  "casos": {
    "D":       {"peso_propio": "distribuido"},
    "H_alero": {"nodales": [{"nudo": "R1_0", "F": [0, 0.5, 0, 0, 0, 0]},
                            {"nudo": "R1_6", "F": [0, 0.5, 0, 0, 0, 0]}]}
  },
  "combinaciones": {"1.2D+1.6Lr": {"D": 1.2, "Lr": 1.6}},
  "analisis": {"modal": {"n_modos": 15}},
  "salidas": {
    "T_star_X": {"que": "periodo_dominante", "direccion": "X"},
    "Ux":       {"que": "participacion_dominante", "direccion": "X"},
    "macum_X":  {"que": "masa_acumulada", "direccion": "X"},
    "d_alero":  {"que": "desplazamiento", "nudo": "R1_0", "gdl": "Uy", "caso": "H_alero"},
    "Rz_1A":    {"que": "reaccion", "nudo": "K1A_0", "gdl": "Uz", "caso": "D"},
    "N_diag":   {"que": "fuerza", "barra": "DTA1_0", "extremo": "i", "componente": "N", "caso": "1.2D+1.6Lr"}
  }
}
```

Reglas del esquema:
- `nudo`/`barra` en `masas`, `casos` y `salidas` aceptan **nombre o id**. Nombres únicos si
  se usan.
- **Las salidas son magnitudes primarias del análisis.** Nada derivado (`k = H/δ`, `R*`,
  `T` de 1 GDL): eso es un paso escrito en el memo, coherente con `SERIES.md` § 4 (el arnés
  no convierte, el memo escribe la sustitución). Es lo que hace que `k_Y` del caso 11 se
  publique como `d_alero` bajo un caso con nombre, y el memo diga de qué caso sale.
- Sondas v1: `periodo{modo}`, `periodo_dominante{direccion}`,
  `participacion_dominante{direccion}`, `masa_acumulada{direccion}`, `desplazamiento{nudo,gdl,caso}`,
  `reaccion{nudo,gdl,caso}`, `fuerza{barra,extremo,componente∈N,Vy,Vz,T,My,Mz,caso}`,
  `peso_total{}`. `caso` puede ser un caso o una combinación.
- Análisis v1: `modal` y casos estáticos + combinaciones. **`espectral` (NCh2369, T*/R* en
  dos pasadas) es v2** y se declara fuera de alcance: el memo 00 solo necesita modal y
  estático, y la cascada 04→13 decide cómo entra R*.

### 2. El archivo de resultados — esquema `rukan/resultados@1`

Lo escribe `python -m rukan run <proyecto>.json` junto al proyecto, como
`<stem>.resultados.json`. Sustituye al JSON del caso 11 para el consumo del memo.

```json
{
  "esquema": "rukan/resultados@1",
  "proyecto": "nch2369-galpon-grua-00.proyecto.json",
  "sha256_proyecto": "…",
  "rukan": "0.1.0", "commit": "a03853a", "openseespy": "3.7.1",
  "generado": "2026-09-05T…",
  "unidades": {"T": "s", "d": "m", "F": "kN", "M": "kN·m"},
  "valores": {"T_star_X": 0.20603, "…": 0}
}
```

**La frescura se verifica por hash, no por mtime**: el arnés recalcula el SHA-256 del
proyecto y lo compara. Es más fuerte (un `git checkout` no lo engaña) y elimina la
dependencia de `RUKAN_ROOT` en el arnés.

### 3. Cambios en Rukan (`F:\Proyectos_Python\rukan`)

| Archivo | Cambio |
|---|---|
| `src/rukan/model.py` | `nombre: str = ""` en `Node`, `Section`, `FrameElement` (kwarg al final; nada existente se rompe) |
| `src/rukan/io.py` **nuevo** | `Proyecto` dataclass (`model, casos, combinaciones, analisis, salidas, titulo`), `to_dict/from_dict`, `load(path)/save(proyecto, path)`, validación del esquema con errores que nombran el campo, resolución nombre→id, conversión de unidades en la frontera con `units.py` |
| `src/rukan/analysis.py` **nuevo** | `modal(model, n_modos) -> ModalResult` (períodos, participación por dirección con la masa generalizada 3D de `case11:modal_3d` / caso 9 — **no** la de `run_spectral`, que es por dirección); `run(proyecto) -> dict[str, float]`: `engine.build`, modal, casos estáticos vía `loads.run_static_case` + `self_weight_distributed`/`self_weight_nodal` + cargas nodales, `loads.combine`, y evaluación de cada sonda |
| `src/rukan/__main__.py` **nuevo** | CLI con dos subcomandos: `run <proyecto.json> [--salida RUTA]` y `validar <proyecto.json>`. Sin más opciones, por diseño |
| `src/rukan/__init__.py` | `__version__ = "0.1.0"` (el resultados lo reporta) |
| `pyproject.toml` | versión 0.1.0; `[project.scripts] rukan = "rukan.__main__:main"` |
| `verification/case11_galpon_grua_nch2369.py` | **Capa E**: `build_model()` → `io.save` → `io.load` → `analysis.run` y assert de que `T_star_*` coinciden con la capa D a 1e-12 (regresión del round-trip). `case11_data._Armador` pasa los nombres de `Meta` a los dataclasses. Regenerar `verification/figs/case11-*.svg` desde el script con `rukan.vista` para que tengan procedencia. `emitir_json` se mantiene (es el post del caso 11), pero deja de ser lo que el memo consume |
| `tests/test_io.py` **nuevo** | round-trip `Model` ↔ dict ↔ JSON; errores de esquema (nudo inexistente, nombre duplicado, unidad no reconocida); conversión de unidades |
| `tests/test_analysis.py` **nuevo** | pórtico de `tests/test_vista.py` como fixture: modal por el runner = `ops.eigen` directo; desplazamiento bajo carga nodal = rigidez directa a mano; sonda contra caso inexistente falla con mensaje |
| `CLAUDE.md`, `ROADMAP.md` | Sección nueva "El archivo de proyecto" y el estado; en ROADMAP marcar Fase 0 "modelo serializable" y anotar `espectral` como v2 |

### 4. Cambios en el repo de memos (`F:\Proyectos_Python\Guias_Interactivas`)

Convención nueva, espejo de `_img/`:

```
memos/estructural/_modelos/
  _proyecto-nch2369-galpon-grua-00.py       # generador: escribe el proyecto y las figuras
  nch2369-galpon-grua-00.proyecto.json      # versionado
  nch2369-galpon-grua-00.resultados.json    # versionado; lo escribe `python -m rukan run`
```

| Archivo | Cambio |
|---|---|
| `_modelos/_proyecto-nch2369-galpon-grua-00.py` | Importa `build_model` desde `$RUKAN_ROOT/verification/case11_data.py`, arma el `Proyecto` (modelo escalonado `nsub=4`, casos `H_alero` sway y `H_riel` sway con H = 1 kN, `modal` 15 modos, las salidas de arriba), `io.save`. Además dibuja `_img/nch2369-galpon-grua-00-{planta,transversal,longitudinal,iso,modo-x,modo-y}.svg` con `rukan.vista` y un dict `D` de cotas, como `_figuras-*-12.py` |
| `_kit/verify_modelo.py` | `modelo:` se resuelve **relativo al memo**; el resultados es `<stem>.resultados.json` junto al proyecto; chequeo 3 pasa a ser `sha256(proyecto) == doc["sha256_proyecto"]`; desaparecen `--rukan`/`RUKAN_ROOT`; aviso `··` si falta cualquiera de los dos archivos |
| `SERIES.md` § 5, `MEMOS.md` (checklist y § modelo) | Reemplazar "más viejo que el script" por el hash, y `modelo: <ruta relativa a $RUKAN_ROOT>` por `modelo: _modelos/<memo>.proyecto.json` |
| `memos/estructural/nch2369-galpon-grua-00-el-modelo.md` + `.check.js` | `orden: 0`, `hereda_de: []`, `modelo: _modelos/nch2369-galpon-grua-00.proyecto.json`. `## Entra` con origen `caso`. `## Modelo` con `M1` (el galpón 3D: nudos, barras, qué se lumpeó) y `M2` (los dos empujes unitarios). `## Sale`: `T_star_X`, `T_star_Y`, `Ux`, `Uy`, `macum_X`, `macum_Y` nacidos en `M1`; `d_alero`, `d_riel` en `M2`; `k_Y` y `k_riel` como **pasos** del memo (`k = H/δ`). `## Límites`: es la **segunda pasada** del ciclo dimensionar → analizar y va primero aunque se escribió último; idealizaciones (masa por áreas del 05, no peso propio; bielas; prismatización del alma variable). `.check.js`: banda de sensatez para `T_star_Y` desde `k_Y` y `m_marco` a 1 GDL (regla 5b: mismo caso de carga, otra formulación) |
| `memos/_serie-nch2369-galpon-grua.md` | "Dónde quedó" y `## Lo que el modelo 3D encontró` apuntan al proyecto; registrar que `k_Y` publicado por el 00 es el de *sway* |
| `_kit/build.py` | Correr para regenerar `memos/INDICE.md` y el hub |

**Circularidad**, explícita en el memo 00: el modelo consume las secciones que el 07 y el
10 dimensionan. Se resuelve como el estado de la serie ya decidió: las entradas del 00 son
`caso` (dato de proyecto al momento de correr), y `## Límites` lo declara. No se cambia
`verify_serie.js`: ya acepta `orden: 0` y `Mn`.

## Orden de implementación

1. **Spec.** Copiar este diseño a `rukan/docs/superpowers/specs/2026-09-05-puente-rukan-memos-design.md` y commitear (regla del flujo de brainstorming).
2. **Rukan, núcleo** (TDD, un commit por paso): `model.py` nombres → `io.py` + `test_io.py` → `analysis.py` + `test_analysis.py` → `__main__.py` + versión.
3. **Rukan, caso 11**: nombres en `_Armador`, capa E round-trip, regeneración de figuras. `python verification/case11_galpon_grua_nch2369.py` en verde.
4. **Memos, arnés**: `verify_modelo.py` por hash y ruta relativa; `SERIES.md`/`MEMOS.md`.
5. **Memos, generador**: `_proyecto-…-00.py` → `python -m rukan run …` → resultados y figuras versionados.
6. **Memos, memo 00** + `.check.js`, estado de la serie, `build.py`.
7. **Docs de Rukan**: `CLAUDE.md`, `ROADMAP.md`.

## Verificación

- Rukan: `pytest` (incluye `test_io`, `test_analysis`, `test_lab`, `test_vista`) y
  `python verification/case11_galpon_grua_nch2369.py` (capas A–E).
- Round-trip: `python -m rukan run memos/estructural/_modelos/nch2369-galpon-grua-00.proyecto.json`
  debe dar `T_star_X = 0,20603` y `T_star_Y = 0,24895` (los del caso 11, capa D, escalonado).
- Memos, los cinco arneses en verde sobre el memo 00:
  `node _kit/verify_memo.js memos/estructural/nch2369-galpon-grua-00-el-modelo.md`,
  `node _kit/verify_serie.js --serie nch2369-galpon-grua`,
  `python _kit/verify_modelo.py memos/estructural/nch2369-galpon-grua-00-el-modelo.md`,
  `python _kit/verify_figura.py`, `python _kit/render_figura.py --memo nch2369-galpon-grua-00-el-modelo`
  y mirar los PNG.
- Prueba de frescura: editar un dígito del proyecto sin recorrer → `verify_modelo.py` debe
  dar `XX`.
- `verify_serie.js` sigue en verde para los eslabones 01–12 (no se tocan).

## Fuera de alcance (siguiente)

- Cascada 04→13 con los períodos nuevos (`R_star`, `R1_Y`, `kcap_Y`, vertical del 06, `Mpe` del 07, anclaje del 13).
- `analisis.espectral` (NCh2369 con T*/R* por dirección) → esquema v2; ya existe `modal.run_directional_spectral`.
- Constructor paramétrico de galpón dentro de Rukan (`galpon.py`) y la GUI: el proyecto JSON es el documento que editarán.
- Geotecnia: sigue en memos con referencia cerrada; si entra al motor será como resortes en nudos (`zeroLength`), otro esquema.

## Riesgos

- **Participación modal**: `modal.run_spectral` usa masa por dirección; el caso 11 y el 9 usan la generalizada 3D. `analysis.modal` debe usar la segunda o `T_star` cambia de modo dominante. La capa E lo atrapa.
- **`RUKAN_ROOT` en el generador**: dependencia entre repos declarada en el docstring y en la cabecera del proyecto (`generado_por`). Se acepta hasta que exista `galpon.py`.
- **Nombres vs ids en `salidas`**: resolver en `io.load`, con error que nombre el símbolo y el nudo que no existe.
