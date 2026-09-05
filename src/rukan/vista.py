"""Dibujo del modelo a SVG — proyecciones, y la deformada de un modo.

Rukan no tenía ninguna visualización: el ROADMAP la pone en la Fase 2 y no hay
matplotlib, ni `opsvis`, ni `vfo`, ni VTK en el entorno. Este módulo es el
adelanto mínimo de esa fase, y **no agrega ninguna dependencia**: escribe el SVG
a mano, con la misma técnica de `lab/_lib/svg.py`, que ya genera las figuras de
las notas del laboratorio.

Qué dibuja, y qué no
--------------------
Dibuja el modelo que existe en memoria —los nudos, las barras, los apoyos, los
nudos con masa— proyectado ortográficamente, y la deformada de un modo. **No hace
eliminación de líneas ocultas**: en una isométrica todo se ve, y en una estructura
reticulada eso es más legible que lo contrario, pero hay que saberlo.

La regla que gobierna los rótulos
---------------------------------
`cotas` es explícito y por omisión está vacío. No es un descuido de la API: el
arnés que audita las figuras de un memo (`verify_memo.js`, capa 2b) lee los
`<text>` del SVG y **exige que todo número de valor absoluto ≥ 10 exista en el
memo**. Un dibujo que rotulara solas las coordenadas de 245 nudos rompería ese
chequeo en la primera corrida. Quien llama decide qué se rotula, y responde por
que esa cifra esté escrita en el texto.

Otras cuatro decisiones que vienen del consumidor y no del gusto:

* **`viewBox` siempre**, porque `render_figura.py` omite el SVG que no lo trae;
* **fondo claro propio**, para que la figura se lea también en tema oscuro;
* **flechas como triángulos**, nunca `<marker>`: hay visores que lo ignoran y
  dejan la flecha sin punta;
* **ningún `<text>` rotado**, porque `verify_figura.py` no revisa los rótulos con
  `transform` y un rótulo girado queda fuera de todo control.

Uso
---
    from rukan.vista import planta, elevacion, isometrica, modo

    open("planta.svg", "w", encoding="utf-8").write(
        planta(model, titulo="Planta del galpón",
               alt="Planta de 30,00 por 25,00 m con los cinco marcos",
               cotas=[((15.0, -1.2), "30,00"), ((-1.8, 12.5), "25,00")]))
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from .model import Model

__all__ = ["Paleta", "PALETA", "planta", "elevacion", "isometrica", "modo",
           "escena", "svg"]


# ------------------------------------------------------------------ paleta
@dataclass(frozen=True)
class Paleta:
    """Colores y tipografía. Los valores por omisión son los de las figuras de
    `Guias_Interactivas`, que es quien consume estos SVG.

    **Ningún color porta información**: la figura se imprime en blanco y negro y
    tiene que seguir diciendo lo mismo. Lo que distingue una barra de otra es su
    grosor y su trazo, no su tono.
    """

    tinta: str = "#2b2a26"
    suave: str = "#8a8578"
    linea: str = "#c9c4b5"
    fondo: str = "#fcfcfa"
    acento: str = "#a4442c"
    frio: str = "#2f5d7c"
    mono: str = "ui-monospace,'IBM Plex Mono',Menlo,Consolas,monospace"


PALETA = Paleta()


# ------------------------------------------------------------- proyecciones
def _proy_planta(p):
    return (p[0], p[1])


def _proy_xz(p):
    return (p[0], p[2])


def _proy_yz(p):
    return (p[1], p[2])


def _proy_iso(az_deg: float, el_deg: float):
    """Axonometría: gira `az` en torno a Z y después inclina `el`."""
    a, e = math.radians(az_deg), math.radians(el_deg)
    ca, sa, se = math.cos(a), math.sin(a), math.sin(e)
    ce = math.cos(e)

    def f(p):
        x, y, z = p
        return (x * ca - y * sa, (x * sa + y * ca) * se + z * ce)

    return f


PROYECCIONES = {"planta": _proy_planta, "XZ": _proy_xz, "YZ": _proy_yz}


# ------------------------------------------------------------------ escena
@dataclass
class Escena:
    """Lo que se va a dibujar, ya en coordenadas del plano de proyección."""

    puntos: dict[int, tuple[float, float]] = field(default_factory=dict)
    barras: list[tuple[int, int, str]] = field(default_factory=list)
    apoyos: list[int] = field(default_factory=list)
    masas: list[int] = field(default_factory=list)


def escena(model: Model, proy, desplaz: dict[int, tuple[float, float, float]] | None = None,
           factor: float = 1.0, clases=None, filtro=None) -> Escena:
    """Proyecta el modelo. `desplaz` suma `factor · d` a cada nudo antes de proyectar.

    `clases` es `{id de barra: nombre}` para que quien llama pueda pedir trazos
    distintos —una diagonal más fina que una columna—; lo que no haya nombrado
    cae en `"barra"`.

    `filtro` es un conjunto de ids de barra, y **hace falta más de lo que
    parece**: en una elevación se superponen todas las barras que comparten
    proyección, y las que quedan encima ganan. En este galpón las X de muro
    proyectan exactamente sobre las columnas del marco, así que sin filtro la
    elevación transversal dibuja columnas de color de diagonal — geométricamente
    correcto y una mentira para el que la lee. Una elevación de un marco se pide
    con el filtro puesto, no recortando el modelo.
    """
    clases = clases or {}
    e = Escena()
    usados: set[int] = set()
    for el in model.elements:
        if filtro is not None and el.id not in filtro:
            continue
        e.barras.append((el.node_i, el.node_j, clases.get(el.id, "barra")))
        usados.update((el.node_i, el.node_j))
    for n in model.nodes:
        if filtro is not None and n.id not in usados:
            continue
        p = (n.x, n.y, n.z)
        if desplaz and n.id in desplaz:
            d = desplaz[n.id]
            p = (p[0] + factor * d[0], p[1] + factor * d[1], p[2] + factor * d[2])
        e.puntos[n.id] = proy(p)
        if any(n.restraints):
            e.apoyos.append(n.id)
    e.masas = [m.node for m in model.masses if m.node in e.puntos]
    return e


# -------------------------------------------------------------------- SVG
TRAZO = {          # (color, ancho, dasharray)
    "barra": ("tinta", 1.6, ""),
    "fina": ("suave", 0.9, ""),
    "tenue": ("linea", 0.8, ""),
    "acento": ("acento", 2.0, ""),
    "guia": ("linea", 0.8, "3 3"),
}


def _esc(s) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def svg(esc: Escena, *, titulo: str = "", alt: str = "", pie: str = "",
        cotas=None, ancho: int = 860, margen: int = 34,
        alto_max: int | None = None, escala: float | None = None,
        paleta: Paleta = PALETA, nudos: bool = True) -> str:
    """Rinde una `Escena` a SVG.

    `escala` en px por unidad del modelo (metros). Si no se da, se elige la que
    hace entrar el dibujo en `ancho`; se **informa** en el pie, porque una figura
    a escala real es un chequeo del cálculo y hay que poder medirla.

    `cotas` es una lista `((u, v), texto)` en coordenadas **del modelo**, ya
    proyectadas por quien llama. Cada texto se escribe tal cual: es la cifra que
    el memo tiene que contener.
    """
    cotas = cotas or []
    xs = [p[0] for p in esc.puntos.values()]
    ys = [p[1] for p in esc.puntos.values()]
    for (u, v), _ in cotas:
        xs.append(u)
        ys.append(v)
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    du, dv = max(x1 - x0, 1e-9), max(y1 - y0, 1e-9)

    cab = 26 if titulo else 6
    pie_h = 22 if pie else 8
    k = escala if escala else (ancho - 2 * margen) / du
    alto = int(round(dv * k + 2 * margen + cab + pie_h))
    if alto_max and alto > alto_max:
        k *= (alto_max - 2 * margen - cab - pie_h) / (dv * k)
        alto = alto_max

    def X(u):
        return margen + (u - x0) * k

    def Y(v):
        return alto - margen - pie_h - (v - y0) * k     # +v hacia arriba

    C = paleta
    col = {"tinta": C.tinta, "suave": C.suave, "linea": C.linea, "acento": C.acento,
           "frio": C.frio}
    out: list[str] = []
    if titulo:
        out.append(f'<text x="{margen}" y="18" fill="{C.tinta}" font-size="13" '
                   f'font-weight="700">{_esc(titulo)}</text>')
    for (i, j, cl) in esc.barras:
        if i not in esc.puntos or j not in esc.puntos:
            continue
        c, w, dash = TRAZO.get(cl, TRAZO["barra"])
        d = f' stroke-dasharray="{dash}"' if dash else ""
        a, b = esc.puntos[i], esc.puntos[j]
        out.append(f'<line x1="{X(a[0]):.2f}" y1="{Y(a[1]):.2f}" '
                   f'x2="{X(b[0]):.2f}" y2="{Y(b[1]):.2f}" '
                   f'stroke="{col[c]}" stroke-width="{w}" stroke-linecap="round"{d}/>')
    if nudos:
        for n, p in esc.puntos.items():
            out.append(f'<circle cx="{X(p[0]):.2f}" cy="{Y(p[1]):.2f}" r="1.5" '
                       f'fill="{C.suave}"/>')
    for n in esc.masas:                       # nudo con masa: cuadrado abierto
        p = esc.puntos[n]
        x, y = X(p[0]), Y(p[1])
        out.append(f'<rect x="{x-2.6:.2f}" y="{y-2.6:.2f}" width="5.2" height="5.2" '
                   f'fill="none" stroke="{C.tinta}" stroke-width="0.9"/>')
    for n in esc.apoyos:                      # triángulo de apoyo, sin <marker>
        p = esc.puntos[n]
        x, y = X(p[0]), Y(p[1])
        out.append(f'<polygon points="{x:.2f},{y:.2f} {x-5:.2f},{y+9:.2f} '
                   f'{x+5:.2f},{y+9:.2f}" fill="{C.tinta}"/>')
    for (u, v), texto in cotas:
        out.append(f'<text x="{X(u):.2f}" y="{Y(v):.2f}" fill="{C.tinta}" '
                   f'font-size="11" text-anchor="middle">{_esc(texto)}</text>')
    if pie:
        out.append(f'<text x="{margen}" y="{alto - 7}" fill="{C.suave}" '
                   f'font-size="10">{_esc(pie)}</text>')

    cuerpo = "\n".join(out)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" '
            f'width="{ancho}" height="{alto}" role="img" aria-label="{_esc(alt)}" '
            f'font-family="{C.mono}" font-size="11">\n'
            f'<title>{_esc(titulo or alt)}</title>\n'
            f'<rect width="{ancho}" height="{alto}" fill="{C.fondo}"/>\n'
            f'{cuerpo}\n</svg>\n')


# -------------------------------------------------------- las cuatro vistas
def _pie(k: float, extra: str = "") -> str:
    return f"escala {k:.2f} px/m" + (f" · {extra}" if extra else "")


def planta(model: Model, **kw) -> str:
    """Vista en planta: el plano X-Y, con +Y hacia arriba."""
    return _vista(model, PROYECCIONES["planta"], **kw)


def elevacion(model: Model, plano: str = "XZ", **kw) -> str:
    """Elevación: `"XZ"` es la longitudinal y `"YZ"` la transversal."""
    if plano not in ("XZ", "YZ"):
        raise ValueError("plano tiene que ser 'XZ' o 'YZ'")
    return _vista(model, PROYECCIONES[plano], **kw)


def isometrica(model: Model, az: float = 35.0, el: float = 25.0, **kw) -> str:
    """Axonometría. **Sin eliminación de líneas ocultas**: se ve todo."""
    return _vista(model, _proy_iso(az, el), **kw)


def modo(model: Model, vectores: dict[int, tuple[float, float, float]],
         proy="planta", *, amplitud: float = 0.06, **kw) -> str:
    """La deformada de un modo, superpuesta a la geometría sin deformar.

    `vectores` es `{id de nudo: (dx, dy, dz)}` —lo que devuelve
    `ops.nodeEigenvector` nudo a nudo—. `amplitud` es la flecha máxima que se
    dibuja, como fracción de la dimensión mayor del modelo: la deformada de un
    modo no tiene escala propia, así que el factor **se elige para ver** y por
    eso se informa en el pie en vez de fingir que es una medida.
    """
    filtro = kw.pop("filtro", None)
    f = PROYECCIONES.get(proy, proy) if isinstance(proy, str) else proy
    dim = max(max(abs(n.x) for n in model.nodes),
              max(abs(n.y) for n in model.nodes),
              max(abs(n.z) for n in model.nodes))
    vmax = max((math.dist((0, 0, 0), v) for v in vectores.values()), default=0.0)
    fac = (amplitud * dim / vmax) if vmax > 0 else 0.0
    base = escena(model, f, filtro=filtro)
    defo = escena(model, f, vectores, fac, filtro=filtro)
    base.barras = [(i, j, "guia") for (i, j, _) in base.barras]
    fusion = Escena(puntos={**{-k: v for k, v in base.puntos.items()}, **defo.puntos},
                    barras=[(-i, -j, "guia") for (i, j, _) in base.barras] + defo.barras,
                    apoyos=defo.apoyos, masas=defo.masas)
    kw.setdefault("pie", f"deformada amplificada · el trazo punteado es la"
                         f" geometría sin deformar")
    return svg(fusion, nudos=False, **kw)


def _vista(model: Model, proy, *, clases=None, filtro=None, **kw) -> str:
    e = escena(model, proy, clases=clases, filtro=filtro)
    return svg(e, **kw)
