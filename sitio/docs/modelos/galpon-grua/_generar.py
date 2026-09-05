"""Escribe `galpon-grua.proyecto.json`: el galpón con puente grúa del caso 11.

    python sitio/docs/modelos/galpon-grua/_generar.py [salida]

El modelo es **el mismo** que `verification/case11_galpon_grua_nch2369.py`
arma en su capa E (`case11_data.build_model(nsub=4, escalonada=True)`), y
`tests/test_sitio.py` lo comprueba corriendo este generador contra el JSON
versionado. Lo que agrega esta entrada son dos casos para mirar:

* `H_alero_uno` — el empuje en **un solo alero**, el caso con el que el memo 07
  obtuvo la `k_Y` que publica sin decirlo; junto a `H_alero` (sway, los diez
  aleros) es el hallazgo del caso 11 puesto en pantalla.
* `D` — el peso propio de los perfiles, distribuido, para ver la deformada de
  gravedad. **No es la masa sísmica**: la serie fijó su masa por áreas
  tributarias (05 · A3) y el modal la consume tal cual.

Después: `python -m rukan run` y `python -m rukan escena` sobre el JSON.
"""

from __future__ import annotations

import os
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 4))
sys.path.insert(0, os.path.join(RAIZ, "verification"))

import case11_data as D  # noqa: E402
from rukan import io  # noqa: E402

NSUB, ESCALONADA = 4, True


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
    h = 0.5                   # 1 kN por marco, medio a cada lado: diez nudos
    empuje = lambda nudos: {"nodales": [{"nudo": n, "F": [0, h, 0, 0, 0, 0]} for n in nudos]}
    return io.Proyecto(
        model=model,
        titulo="Galpón con puente grúa — nch2369-galpon-grua",
        origen={"script": "sitio/docs/modelos/galpon-grua/_generar.py",
                "generador": "case11_data.build_model(nsub=%d, escalonada=%s)"
                             % (NSUB, ESCALONADA)},
        casos={"H_alero": empuje(aleros),
               "H_alero_uno": {"nodales": [{"nudo": "R3_0", "F": [0, 1.0, 0, 0, 0, 0]}]},
               "H_riel": empuje(rieles),
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
