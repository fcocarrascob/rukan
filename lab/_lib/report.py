"""Tabla comparativa de una nota: se imprime en markdown y se verifica sola.

La salida de `reportar()` es **markdown pegable directo en el MDX del post**.
Esa es la regla del laboratorio: la tabla que se publica es la que imprimió el
script, no una transcrita a mano. Si el motor cambia y el número se mueve, el
`assert` falla en `pytest` antes de que el post quede mintiendo.

Uso típico::

    from lab._lib.report import Fila, reportar

    reportar(
        "Momentos de la viga apuntalada",
        [
            Fila("Momento de empotramiento", "kN·m", ref=41.6667, ops=41.6667),
            Fila("Momento máximo del vano", "kN·m", ref=23.4375, ops=23.4375),
            Fila("Rotación del apoyo móvil", "mrad", ref=0.0, ops=1e-14, tol_abs=1e-9),
        ],
    )
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

__all__ = ["Fila", "tabla_markdown", "verificar", "reportar"]

# La tabla se pega en un MDX: la consola de Windows (cp1252) se comería los
# acentos y el "·" de kN·m. Se fuerza UTF-8 en la salida.
for _flujo in (sys.stdout, sys.stderr):
    if hasattr(_flujo, "reconfigure"):
        try:
            _flujo.reconfigure(encoding="utf-8")
        except (ValueError, OSError):  # flujo ya cerrado o redirigido raro
            pass


@dataclass
class Fila:
    """Una magnitud comparada entre la referencia independiente y OpenSees.

    El criterio de tolerancia se elige solo: si se declara ``tol_abs``, la
    comparación es **absoluta** (el caso de las magnitudes que deben dar cero,
    donde el error relativo no significa nada); si no, es **relativa en %**
    contra ``tol_pct``.
    """

    magnitud: str
    unidad: str
    ref: float
    ops: float
    tol_pct: float = 0.1
    tol_abs: float | None = None
    decimales: int = 4

    @property
    def absoluta(self) -> bool:
        return self.tol_abs is not None

    @property
    def error(self) -> float:
        """Error absoluto, o relativo en % según el criterio de la fila."""
        if self.absoluta:
            return abs(self.ops - self.ref)
        if self.ref == 0.0:
            raise ValueError(
                f"'{self.magnitud}': referencia = 0 exige tol_abs "
                "(el error relativo no está definido)"
            )
        return abs(self.ops - self.ref) / abs(self.ref) * 100.0

    @property
    def tolerancia(self) -> float:
        return self.tol_abs if self.absoluta else self.tol_pct

    @property
    def pasa(self) -> bool:
        return self.error < self.tolerancia

    def _fmt(self, valor: float) -> str:
        return f"{valor:.{self.decimales}f}"

    def _fmt_error(self) -> str:
        if self.absoluta:
            return f"{self.error:.2e}"
        return f"{self.error:.4f} %"


def tabla_markdown(
    filas: list[Fila],
    *,
    ref_label: str = "Referencia",
    ops_label: str = "OpenSees",
) -> str:
    """Devuelve la tabla en markdown, lista para pegar en el MDX."""
    lineas = [
        f"| Magnitud | {ref_label} | {ops_label} | Error |",
        "|---|---|---|---|",
    ]
    for f in filas:
        nombre = f"{f.magnitud} [{f.unidad}]" if f.unidad else f.magnitud
        lineas.append(
            f"| {nombre} | {f._fmt(f.ref)} | {f._fmt(f.ops)} | {f._fmt_error()} |"
        )
    return "\n".join(lineas)


def verificar(filas: list[Fila]) -> None:
    """Falla con `assert` en la primera fila fuera de tolerancia."""
    for f in filas:
        criterio = "absoluta" if f.absoluta else "%"
        assert f.pasa, (
            f"'{f.magnitud}': error {f.error:.6g} excede la tolerancia "
            f"{f.tolerancia:.6g} ({criterio}) — "
            f"referencia {f.ref:.6g}, OpenSees {f.ops:.6g}"
        )


def reportar(
    titulo: str,
    filas: list[Fila],
    *,
    ref_label: str = "Referencia",
    ops_label: str = "OpenSees",
    nota: str = "",
) -> None:
    """Imprime la tabla markdown y verifica las tolerancias."""
    print(f"\n### {titulo}\n")
    print(tabla_markdown(filas, ref_label=ref_label, ops_label=ops_label))
    if nota:
        print(f"\n{nota}")
    verificar(filas)
    n = len(filas)
    plural = "magnitudes verificadas" if n != 1 else "magnitud verificada"
    print(f"\n> {n} {plural} — dentro de tolerancia.")
