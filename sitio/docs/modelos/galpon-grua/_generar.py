"""Escribe `galpon-grua.proyecto.json`: el galpón con puente grúa del caso 11.

    python sitio/docs/modelos/galpon-grua/_generar.py [salida]

El modelo es el de `verification/case11_data.build_model(escalonada=True)`
con la **malla del memo 00 de la serie**: `nsub=16` tramos prismáticos por corte,
965 nudos y 1 044 barras, con la que la serie publica `T*_Y = 0,24878 s` (la capa
D del caso 11 usa `nsub=4` y da 0,24895; la diferencia es el error de
discretización que el memo 00 · A3 mide). `tests/test_sitio.py` comprueba que
este generador reproduce el JSON versionado.

Los casos son **seis empujes unitarios y el peso propio**. Los tres primeros son
del lote A; los tres que siguen los pide el lote D, y **ninguno reproduce una
cifra de los memos 07 a 12**: esos seis eslabones resuelven en forma cerrada o
declaran los resultados de un modelo plano que no ejecutan. Están para
contrastar, que es lo que este sitio hace.

* `H_alero` — el sway: los diez aleros empujados a la vez.
* `H_alero_uno` — el empuje en **un solo alero**, el caso con el que el memo 07
  obtuvo la `k_Y` que publica sin decirlo; junto a `H_alero` es el hallazgo del
  caso 11 puesto en pantalla.
* `H_riel` — los diez nudos de riel, que es el límite de diafragma rígido de la
  banda que el 07 · C3 dejó abierta.
* `H_riel_uno` — los **dos rieles de un marco**, la otra cota de esa banda: el
  empuje de grúa entrando por un marco solo. El 11 · D2 la cierra.
* `E_X` — sismo longitudinal estático equivalente, repartido como la masa
  sísmica: el techo recoge la inercia y la lleva a los aleros por las diagonales,
  que es la frase de §12.1.2 que el 11 dimensiona.
* `E_Y_tope` — el mismo reparto en la dirección de los marcos, pero con la grúa
  en `X_G_TOPE`: la resultante se corre a los 12,11692 m que el 12 · C3 publica
  y el galpón gira en planta.
* `D` — el peso propio de los perfiles, distribuido, para ver la deformada de
  gravedad. **No es la masa sísmica**: la serie fijó su masa por áreas
  tributarias (05 · A3) y el modal la consume tal cual.

Los seis empujes son **unitarios**, en la convención que el memo 00 · S5 fijó y
que los eslabones 00 a 06 ya publicaron: `H_MARCO = 1 000 kN` **por marco**. Los
cuatro que cargan el edificio entero (`H_alero`, `H_riel`, `E_X`, `E_Y_tope`)
suman 5 000 kN; los dos que cargan un marco solo (`H_alero_uno`, `H_riel_uno`),
1 000 kN.

Que sean unitarios no es una comodidad: deja fuera del modelo toda magnitud de
nivel de diseño (`Q0_Y`, `F_diaf_X`), que la página escala en un paso a la vista.
Y las razones que los memos publican —`δmáx/δprom`, el reparto entre marcos, la
razón sway— son invariantes de escala.

Después: `python -m rukan run` y `python -m rukan escena` sobre el JSON.
"""

from __future__ import annotations

import os
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 4))
sys.path.insert(0, os.path.join(RAIZ, "verification"))

import case11_data as D  # noqa: E402
from rukan import io  # noqa: E402

NSUB, ESCALONADA = 16, True
H_MARCO = 1000.0   # kN por marco — la unidad de empuje del memo 00 · S5


def _sismico(model, meta, x_grua: float, gdl: int, total: float) -> dict:
    """Un caso sísmico estático equivalente **unitario**, repartido como la masa.

    Reusa `case11_data.masas`, que es la misma función con que se arma la masa
    del modal, así que la resultante cae exactamente en el centro de masa que el
    05 declaró; con `x_grua = X_G_TOPE` cae en los 12,11692 m del 12 · C3, sin
    que este script decida ningún reparto por su cuenta.

    Las masas **del modelo** no se tocan: siguen siendo las del reparto por
    omisión (la grúa al centro), que es lo que los eslabones 00 a 06 publicaron y
    lo que el modal consume. Acá solo se les copia el reparto para escribir
    fuerzas.
    """
    nombre = {n.id: n.nombre for n in model.nodes}
    masas = D.masas(meta, x_grua=x_grua)
    suma = sum(m.values[0] for m in masas)
    nodales = []
    for m in sorted(masas, key=lambda m: m.node):
        F = [0.0] * 6
        F[gdl] = total * m.values[0] / suma
        nodales.append({"nudo": nombre[m.node], "F": F})
    return {"nodales": nodales}


def proyecto() -> io.Proyecto:
    model, meta = D.build_model(nsub=NSUB, escalonada=ESCALONADA)
    aleros = ["R%d_0" % f for f in range(1, D.NMARCOS + 1)] + \
             ["R%d_%d" % (f, D.NJ) for f in range(1, D.NMARCOS + 1)]
    rieles = []
    for f in range(1, D.NMARCOS + 1):
        for l in D.WALLS:
            cand = [(abs(xyz[2] - D.Z_RIEL), nm) for nm, xyz in meta.node_xyz.items()
                    if nm.startswith("K%d%s_" % (f, l))]
            d_, nm = min(cand)
            assert d_ < 1e-9, "no hay nudo de riel en el marco %d" % f
            rieles.append(nm)
    h = H_MARCO / 2.0         # medio a cada lado: diez nudos (memo 00 · S5)
    total = H_MARCO * D.NMARCOS                # el edificio entero: 5 000 kN
    empuje = lambda nudos: {"nodales": [{"nudo": n, "F": [0, h, 0, 0, 0, 0]} for n in nudos]}
    col_top = "COL3A_%d" % (3 * NSUB)     # el tramo de columna que llega al alero
    return io.Proyecto(
        model=model,
        titulo="Galpón con puente grúa — nch2369-galpon-grua",
        origen={"script": "sitio/docs/modelos/galpon-grua/_generar.py",
                "generador": "case11_data.build_model(nsub=%d, escalonada=%s)"
                             % (NSUB, ESCALONADA)},
        casos={"H_alero": empuje(aleros),
               "H_alero_uno": {"nodales": [{"nudo": "R3_0", "F": [0, 2 * h, 0, 0, 0, 0]}]},
               "H_riel": empuje(rieles),
               "H_riel_uno": {"nodales": [{"nudo": n, "F": [0, h, 0, 0, 0, 0]}
                                          for n in rieles[4:6]]},
               "E_X": _sismico(model, meta, D.LARGO / 2.0, 0, total),
               "E_Y_tope": _sismico(model, meta, D.X_G_TOPE, 1, total),
               "D": {"peso_propio": "distribuido"}},
        analisis={"modal": {"n_modos": 15}},
        salidas={
            "T_star_X": {"que": "periodo_dominante", "direccion": "X"},
            "T_star_Y": {"que": "periodo_dominante", "direccion": "Y"},
            "Ux": {"que": "participacion_dominante", "direccion": "X"},
            "Uy": {"que": "participacion_dominante", "direccion": "Y"},
            "macum_X": {"que": "masa_acumulada", "direccion": "X"},
            "macum_Y": {"que": "masa_acumulada", "direccion": "Y"},
            "macum_Z": {"que": "masa_acumulada", "direccion": "Z"},
            "d_alero": {"que": "desplazamiento", "nudo": "R3_0", "gdl": "Uy",
                        "caso": "H_alero"},
            "d_alero_uno": {"que": "desplazamiento", "nudo": "R3_0", "gdl": "Uy",
                            "caso": "H_alero_uno"},
            "d_riel": {"que": "desplazamiento", "nudo": rieles[4], "gdl": "Uy",
                       "caso": "H_riel"},
            "d_cumbrera_D": {"que": "desplazamiento", "nudo": "R3_%d" % (D.NJ // 2),
                             "gdl": "Uz", "caso": "D"},
            # Dos esfuerzos **dentro** de la barra, no en sus extremos: es lo que
            # la escena@2 agrega y lo que el visor dibuja.
            "Mz_raf3": {"que": "esfuerzo", "barra": "RAF3_1", "componente": "Mz",
                        "x_rel": 0.5, "caso": "D"},
            "N_col3": {"que": "esfuerzo", "barra": "COL3A_1", "componente": "N",
                       "x_rel": 0.5, "caso": "D"},
            # --- lo que el lote D contrasta ---------------------------------
            # 07 · la columna bajo el sway no lleva carga de vano, así que su Mz
            #      es lineal: sus dos extremos fijan la razón M_base/M_nudo y el
            #      punto de inflexión que el memo declara sin ejecutar.
            "Mz_base_sway": {"que": "esfuerzo", "barra": "COL3A_1", "componente": "Mz",
                             "x_rel": 0.0, "caso": "H_alero"},
            "Mz_nudo_sway": {"que": "esfuerzo", "barra": col_top, "componente": "Mz",
                             "x_rel": 1.0, "caso": "H_alero"},
            # 11 · el empuje de grúa entrando por un marco solo, y el diafragma
            #      de techo bajo el sismo longitudinal.
            "d_riel_uno": {"que": "desplazamiento", "nudo": rieles[4], "gdl": "Uy",
                           "caso": "H_riel_uno"},
            "N_dta1": {"que": "esfuerzo", "barra": "DTA1_0", "componente": "N",
                       "x_rel": 0.5, "caso": "E_X"},
            "N_dta2": {"que": "esfuerzo", "barra": "DTA2_0", "componente": "N",
                       "x_rel": 0.5, "caso": "E_X"},
            # El puntal de alero es un **colector**: no resiste, arrastra. Los
            # cuatro vanos de una misma línea muestran la acumulación hacia el
            # vano arriostrado, que es la tesis del 11 · D1.
            "N_pun1": {"que": "esfuerzo", "barra": "PUN1_0", "componente": "N",
                       "x_rel": 0.5, "caso": "E_X"},
            "N_pun2": {"que": "esfuerzo", "barra": "PUN2_0", "componente": "N",
                       "x_rel": 0.5, "caso": "E_X"},
            "N_pun3": {"que": "esfuerzo", "barra": "PUN3_0", "componente": "N",
                       "x_rel": 0.5, "caso": "E_X"},
            "N_pun4": {"que": "esfuerzo", "barra": "PUN4_0", "componente": "N",
                       "x_rel": 0.5, "caso": "E_X"},
            # 12 · la deriva de cada marco con la grúa en el tope; `dY_m1_B` es
            #      el control de que los dos aleros de un marco van juntos.
            "dY_m1": {"que": "desplazamiento", "nudo": "R1_0", "gdl": "Uy",
                      "caso": "E_Y_tope"},
            "dY_m2": {"que": "desplazamiento", "nudo": "R2_0", "gdl": "Uy",
                      "caso": "E_Y_tope"},
            "dY_m3": {"que": "desplazamiento", "nudo": "R3_0", "gdl": "Uy",
                      "caso": "E_Y_tope"},
            "dY_m4": {"que": "desplazamiento", "nudo": "R4_0", "gdl": "Uy",
                      "caso": "E_Y_tope"},
            "dY_m5": {"que": "desplazamiento", "nudo": "R5_0", "gdl": "Uy",
                      "caso": "E_Y_tope"},
            "dY_m1_B": {"que": "desplazamiento", "nudo": "R1_%d" % D.NJ, "gdl": "Uy",
                        "caso": "E_Y_tope"},
            "peso_total": {"que": "peso_total"},
        })


def main(argv: list[str]) -> int:
    salida = argv[1] if len(argv) > 1 else \
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "galpon-grua.proyecto.json")
    p = proyecto()
    io.save(p, salida)
    print(f"escrito {salida}: {len(p.model.nodes)} nudos, {len(p.model.elements)} barras, "
          f"{len(p.casos)} casos, {len(p.salidas)} salidas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
