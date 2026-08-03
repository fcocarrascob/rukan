"""Copia las figuras de una nota al repositorio del blog.

Los scripts viven en rukan; el MDX y los SVG, en struct_pad. Esto mueve lo
segundo sin que haya que acordarse de la ruta::

    python -m lab._lib.publish nota01 --slug lab-eleload-empotramiento

Renombra según la convención ya usada en el blog: ``lab/figs/nota01-momentos.svg``
termina como ``public/lab-eleload-empotramiento/fig-momentos.svg``.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
FIGS = RAIZ / "lab" / "figs"
BLOG_POR_DEFECTO = RAIZ.parent / "struct_pad"


def publicar(nota: str, slug: str, blog: Path, *, dry_run: bool = False) -> list[Path]:
    origenes = sorted(FIGS.glob(f"{nota}-*.svg"))
    if not origenes:
        raise SystemExit(
            f"No hay figuras {nota}-*.svg en {FIGS}. "
            f"¿Corriste `python -m lab.{nota}_...` antes?"
        )

    destino_dir = blog / "public" / slug
    if not (blog / "public").is_dir():
        raise SystemExit(f"No parece el repo del blog: no existe {blog / 'public'}")

    copiados = []
    for origen in origenes:
        nombre = "fig-" + origen.name[len(nota) + 1 :]
        destino = destino_dir / nombre
        print(f"  {origen.relative_to(RAIZ)} -> {destino}")
        if not dry_run:
            destino_dir.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(origen, destino)
        copiados.append(destino)

    print(f"\n{len(copiados)} figura(s) {'a copiar' if dry_run else 'copiadas'}.")
    print(f"En el MDX: src=\"/{slug}/fig-....svg\"")
    return copiados


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("nota", help="prefijo de la nota, p.ej. nota01")
    p.add_argument("--slug", required=True, help="slug del post en el blog")
    p.add_argument("--blog", type=Path, default=BLOG_POR_DEFECTO,
                   help=f"ruta al repo struct_pad (por defecto {BLOG_POR_DEFECTO})")
    p.add_argument("--dry-run", action="store_true", help="solo mostrar qué haría")
    args = p.parse_args(argv)

    publicar(args.nota, args.slug, args.blog.resolve(), dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
