"""`python -m rukan` — correr o validar un archivo de proyecto.

    python -m rukan run     <proyecto.json> [--salida RUTA]
    python -m rukan validar <proyecto.json>

`run` no toma ninguna opción de análisis, por diseño: qué se corre y qué se
reporta lo dice el archivo, y así el arnés del repo de memos puede leerlo. El
resultado va junto al proyecto como `<nombre>.resultados.json`, con el hash del
proyecto adentro para que nadie lo cite después de cambiar el modelo.
"""

from __future__ import annotations

import argparse
import json
import sys

from . import analysis, io


def _cargar(ruta: str) -> io.Proyecto | None:
    try:
        return io.load(ruta)
    except FileNotFoundError:
        print(f"no existe {ruta}", file=sys.stderr)
    except json.JSONDecodeError as exc:
        print(f"{ruta}: no es JSON válido ({exc})", file=sys.stderr)
    except io.ErrorDeEsquema as exc:
        print(f"{ruta}: {exc}", file=sys.stderr)
    return None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="rukan", description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="corre el proyecto y escribe los resultados")
    r.add_argument("proyecto")
    r.add_argument("--salida", help="ruta del JSON de resultados "
                                    "(por omisión, junto al proyecto)")
    v = sub.add_parser("validar", help="valida el esquema sin correr nada")
    v.add_argument("proyecto")
    a = ap.parse_args(argv)

    p = _cargar(a.proyecto)
    if p is None:
        return 1
    m = p.model
    print(f"{a.proyecto}: {len(m.nodes)} nudos · {len(m.elements)} barras · "
          f"{len(p.casos)} casos · {len(p.combinaciones)} combinaciones · "
          f"{len(p.salidas)} salidas")
    if a.cmd == "validar":
        print("esquema OK")
        return 0

    valores = analysis.run(p)
    unidades = analysis.unidades(p)
    doc = io.resultados(a.proyecto, valores, unidades)
    salida = a.salida or io.ruta_resultados(a.proyecto)
    with open(salida, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    ancho = max((len(s) for s in valores), default=8)
    for s, v in valores.items():
        print(f"  {s:{ancho}s}  {v:16.8g}  {unidades[s]}")
    print(f"escrito  {salida}  ({len(valores)} magnitudes, "
          f"rukan {doc['rukan']} @ {doc['commit']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
