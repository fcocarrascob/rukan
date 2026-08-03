"""Figuras SVG en el estilo del blog, generadas por el mismo script que calcula.

Las figuras de struct_pad hasta ahora se escribían a mano. Acá se emiten desde
Python con la misma paleta y proporciones, de modo que **la figura y el número
salgan de la misma corrida**: si el resultado cambia, la figura cambia con él.

El sitio no tiene modo oscuro, así que el fondo es blanco fijo (igual que los
SVG existentes en ``struct_pad/public/rukan-*/``).

Uso típico::

    lienzo = Lienzo(alto=300, titulo="…", subtitulo="…")
    ejes = lienzo.ejes(x=(0, 6), y=(-60, 30), etiqueta_x="x [m]", etiqueta_y="M [kN·m]")
    ejes.curva(xs, ys, color=AZUL, ancho=2.0)
    lienzo.guardar("lab/figs/nota01-momentos.svg")
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from xml.sax.saxutils import escape

__all__ = [
    "Lienzo",
    "Ejes",
    "AZUL",
    "GRIS",
    "ROJO",
    "VERDE",
    "TINTA",
    "TEXTO",
    "TENUE",
    "TICK",
    "GRILLA",
]

# Paleta tomada de los SVG ya publicados en struct_pad/public/rukan-*/.
AZUL = "#1a63a8"
GRIS = "#888"
ROJO = "#b02a1a"
VERDE = "#2f7d32"
TINTA = "#222"
TEXTO = "#333"
TENUE = "#666"
TICK = "#777"
GRILLA = "#eee"
EJE = "#333"

ANCHO = 560
FUENTE = "Segoe UI, Arial, sans-serif"


def _num(v: float) -> str:
    """Formatea una coordenada sin ceros de más."""
    return f"{v:.1f}".rstrip("0").rstrip(".") if v % 1 else str(int(v))


@dataclass
class Lienzo:
    """Un SVG del ancho del contenido del blog (560 px), con título opcional."""

    alto: int = 320
    titulo: str = ""
    subtitulo: str = ""
    ancho: int = ANCHO
    _elementos: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.titulo:
            self.texto(
                self.ancho / 2, 24, self.titulo, tam=14.5, color=TINTA,
                anclaje="middle", negrita=True,
            )
        if self.subtitulo:
            self.texto(
                self.ancho / 2, 42, self.subtitulo, tam=11, color=TENUE,
                anclaje="middle",
            )

    # --- primitivas ---------------------------------------------------------

    def linea(self, x1, y1, x2, y2, *, color=EJE, ancho=1.0, guion="") -> None:
        dash = f' stroke-dasharray="{guion}"' if guion else ""
        grosor = f' stroke-width="{ancho}"' if ancho != 1.0 else ""
        self._elementos.append(
            f'<line x1="{_num(x1)}" y1="{_num(y1)}" x2="{_num(x2)}" '
            f'y2="{_num(y2)}" stroke="{color}"{grosor}{dash}/>'
        )

    def texto(self, x, y, contenido, *, tam=11, color=TEXTO, anclaje="start",
              negrita=False) -> None:
        peso = ' font-weight="bold"' if negrita else ""
        self._elementos.append(
            f'<text x="{_num(x)}" y="{_num(y)}" font-size="{tam}" '
            f'text-anchor="{anclaje}" fill="{color}"{peso}>'
            f"{escape(str(contenido))}</text>"
        )

    def rect(self, x, y, ancho, alto, *, color=AZUL, radio=2, opacidad=1.0) -> None:
        op = f' opacity="{opacidad}"' if opacidad != 1.0 else ""
        self._elementos.append(
            f'<rect x="{_num(x)}" y="{_num(y)}" width="{_num(ancho)}" '
            f'height="{_num(alto)}" rx="{radio}" fill="{color}"{op}/>'
        )

    def poligono(self, puntos, *, relleno="none", borde=AZUL, ancho=1.5,
                 opacidad=1.0) -> None:
        d = " ".join(f"{_num(x)},{_num(y)}" for x, y in puntos)
        op = f' opacity="{opacidad}"' if opacidad != 1.0 else ""
        self._elementos.append(
            f'<polygon points="{d}" fill="{relleno}" stroke="{borde}" '
            f'stroke-width="{ancho}"{op}/>'
        )

    def polilinea(self, puntos, *, color=AZUL, ancho=2.0, guion="") -> None:
        d = " ".join(f"{_num(x)},{_num(y)}" for x, y in puntos)
        dash = f' stroke-dasharray="{guion}"' if guion else ""
        self._elementos.append(
            f'<polyline points="{d}" fill="none" stroke="{color}" '
            f'stroke-width="{ancho}"{dash} stroke-linejoin="round"/>'
        )

    def circulo(self, x, y, r, *, color=AZUL) -> None:
        self._elementos.append(
            f'<circle cx="{_num(x)}" cy="{_num(y)}" r="{r}" fill="{color}"/>'
        )

    # --- compuestos ---------------------------------------------------------

    def ejes(self, *, x: tuple[float, float], y: tuple[float, float],
             caja: tuple[float, float, float, float] = (60, 62, 500, 260),
             etiqueta_x: str = "", etiqueta_y: str = "",
             ticks_x: int = 5, ticks_y: int = 5) -> "Ejes":
        """Dibuja el marco y devuelve el mapeador de coordenadas."""
        ejes = Ejes(self, x, y, caja)
        ejes._dibujar_marco(etiqueta_x, etiqueta_y, ticks_x, ticks_y)
        return ejes

    def leyenda(self, x: float, y: float, entradas: list[tuple[str, str]],
                *, tam: float = 10.5) -> None:
        """Entradas ``(color, texto)`` apiladas verticalmente."""
        for k, (color, etiqueta) in enumerate(entradas):
            yy = y + k * 16
            self.linea(x, yy - 4, x + 18, yy - 4, color=color, ancho=2.5)
            self.texto(x + 24, yy, etiqueta, tam=tam, color=TEXTO)

    # --- salida -------------------------------------------------------------

    def render(self) -> str:
        cuerpo = "\n".join(self._elementos)
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {self.ancho} {self.alto}" font-family="{FUENTE}">\n'
            f'<rect width="{self.ancho}" height="{self.alto}" fill="#ffffff"/>\n'
            f"{cuerpo}\n</svg>\n"
        )

    def guardar(self, ruta: str | Path) -> Path:
        destino = Path(ruta)
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(self.render(), encoding="utf-8")
        return destino


@dataclass
class Ejes:
    """Mapea coordenadas de datos a píxeles dentro de una caja del lienzo."""

    lienzo: Lienzo
    rango_x: tuple[float, float]
    rango_y: tuple[float, float]
    caja: tuple[float, float, float, float]  # (izq, sup, der, inf) en píxeles

    def x(self, v: float) -> float:
        x0, x1 = self.rango_x
        izq, _, der, _ = self.caja
        return izq + (v - x0) / (x1 - x0) * (der - izq)

    def y(self, v: float) -> float:
        y0, y1 = self.rango_y
        _, sup, _, inf = self.caja
        return inf - (v - y0) / (y1 - y0) * (inf - sup)

    def _dibujar_marco(self, etiqueta_x, etiqueta_y, ticks_x, ticks_y) -> None:
        izq, sup, der, inf = self.caja
        for k in range(ticks_y + 1):
            v = self.rango_y[0] + k * (self.rango_y[1] - self.rango_y[0]) / ticks_y
            yy = self.y(v)
            self.lienzo.linea(izq, yy, der, yy, color=GRILLA)
            self.lienzo.texto(izq - 6, yy + 3.5, _etiqueta(v), tam=10,
                              color=TICK, anclaje="end")
        for k in range(ticks_x + 1):
            v = self.rango_x[0] + k * (self.rango_x[1] - self.rango_x[0]) / ticks_x
            xx = self.x(v)
            self.lienzo.linea(xx, sup, xx, inf, color=GRILLA)
            self.lienzo.texto(xx, inf + 16, _etiqueta(v), tam=10, color=TICK,
                              anclaje="middle")
        # Eje horizontal en y = 0 si el rango lo cruza; si no, el borde inferior.
        y_cero = self.y(0.0) if self.rango_y[0] < 0 < self.rango_y[1] else inf
        self.lienzo.linea(izq, y_cero, der, y_cero, color=EJE)
        self.lienzo.linea(izq, sup, izq, inf, color=EJE)
        if etiqueta_x:
            self.lienzo.texto((izq + der) / 2, inf + 34, etiqueta_x, tam=11,
                              color=TENUE, anclaje="middle")
        if etiqueta_y:
            # Anclada al margen izquierdo: centrarla sobre el eje la sacaría
            # del lienzo apenas la etiqueta pasa de unos pocos caracteres.
            self.lienzo.texto(6, sup - 8, etiqueta_y, tam=11, color=TENUE,
                              anclaje="start")

    def curva(self, xs, ys, *, color=AZUL, ancho=2.0, guion="") -> None:
        self.lienzo.polilinea(
            [(self.x(a), self.y(b)) for a, b in zip(xs, ys)],
            color=color, ancho=ancho, guion=guion,
        )

    def area(self, xs, ys, *, color=AZUL, opacidad=0.15, base=0.0) -> None:
        puntos = [(self.x(a), self.y(b)) for a, b in zip(xs, ys)]
        puntos += [(self.x(xs[-1]), self.y(base)), (self.x(xs[0]), self.y(base))]
        self.lienzo.poligono(puntos, relleno=color, borde="none", ancho=0,
                             opacidad=opacidad)

    def marcar(self, xv: float, yv: float, etiqueta: str, *, color=ROJO,
               dx: float = 8, dy: float = -8) -> None:
        px, py = self.x(xv), self.y(yv)
        self.lienzo.circulo(px, py, 3.5, color=color)
        self.lienzo.texto(px + dx, py + dy, etiqueta, tam=10.5, color=color,
                          negrita=True)


def _etiqueta(v: float) -> str:
    if abs(v) < 1e-12:
        return "0"
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f"{v:.2f}".rstrip("0").rstrip(".")
