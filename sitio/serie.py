"""El andamiaje de una serie: el esquema `rukan/valores@1`, la cadena y el oráculo.

Una **serie** es una cadena de eslabones que diseñan la misma estructura; cada
eslabón es una carpeta `sitio/docs/series/<serie>/<NN-slug>/` con un
`_calculo.py` que declara y calcula con esta librería, y escribe
`<NN-slug>.valores.json`. La prosa de `index.md` inyecta cada cifra con el
macro `v()`; la ficha de contrato, con `ficha()` (`sitio/main.py`).

Lo que hereda del régimen de memos de `Guias_Interactivas`, y lo que cambia:

* **Cada cifra nace en un paso o en un modelo.** `caso()` es un dato de proyecto,
  `entra()` lo que otro eslabón publicó, `paso()` lo que este eslabón calcula,
  `sale()` lo que publica. Un `sale` cita el paso que lo produjo.
* **La cadena no se copia: se consume.** `entra(simbolo, de="04")` lee el JSON del
  eslabón 04 y devuelve su valor; si el 04 cambia y no se recorre este, el test
  de cadena lo dice. `de="modelo:<slug>"` lee `modelos/<slug>/<slug>.resultados.json`,
  que es el `Mn` de los memos.
* **El oráculo de migración.** `publicado()` recibe lo que el memo original
  imprimió, como texto y con coma decimal (`"15047,57290"`), y `escribir()` falla si
  algún `sale` se aparta más de media unidad del último decimal impreso: la
  misma tolerancia con que `verify_serie.js` cruzaba dos memos. Un decimal de más
  es una promesa de más.
* **Primario y derivado.** El modelo emite desplazamientos; `k = H/δ` es un
  `paso()` de este eslabón, con su símbolo propio. El arnés nunca convierte.

Tolerancias, como en el repo de memos: **absolutas**, media unidad del último
dígito impreso, porque una magnitud que viaja puede valer cero.
"""

from __future__ import annotations

import datetime
import json
import re
import subprocess
import unicodedata
from pathlib import Path
from typing import Any

ESQUEMA_VALORES = "rukan/valores@1"
RX_NN = re.compile(r"^(\d\d)-")


# ============================ números ================================
def num(s: str | float) -> float:
    """`"15 047,57290"` → 15047.5729. Guion ASCII para el signo, coma decimal."""
    if isinstance(s, (int, float)):
        return float(s)
    t = str(s).strip().replace(" ", "").replace("\xa0", "").replace(" ", "")
    t = t.replace(".", "").replace(",", ".") if "," in t else t
    return float(t)


def decimales(s: str | float) -> int:
    """Cuántos decimales muestra la cifra **tal como está escrita**."""
    if isinstance(s, (int, float)):
        s = repr(float(s))
        return 0 if s.endswith(".0") else len(s.split(".")[1])
    t = str(s).strip().replace(" ", "")
    m = re.search(r"[,.](\d+)$", t)
    return len(m.group(1)) if m else 0


def tolerancia(publicado: str | float) -> float:
    return 0.5 * 10.0 ** (-decimales(publicado))


def fmt(v: float, cifras: int | None = None) -> str:
    """`15047.5712, 2` → `15 047,57`; sin cifras, seis significativas tal cual."""
    s = f"{v:,.{cifras}f}" if cifras is not None else f"{v:.6g}"
    return s.replace(",", "\0").replace(".", ",").replace("\0", " ")


def canon(s: str) -> str:
    """Sin ligaduras, sin acentos, sin mayúsculas y sin nada que no sea letra o
    dígito: lo que sobrevive a un PDF que parte palabras entre columnas."""
    s = unicodedata.normalize("NFKC", s)
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "", s.casefold())


# ============================ rutas ==================================
def carpeta_series(raiz: Path) -> Path:
    return Path(raiz) / "docs" / "series"


def carpeta_eslabon(raiz: Path, serie: str, nn: str) -> Path:
    base = carpeta_series(raiz) / serie
    cands = sorted(base.glob(f"{nn}-*")) if base.exists() else []
    cands = [c for c in cands if c.is_dir()]
    if not cands:
        raise FileNotFoundError(f"no existe el eslabón {nn} de la serie {serie!r} "
                                f"en {base}")
    return cands[0]


def cargar(raiz: Path, serie: str, nn: str) -> dict:
    c = carpeta_eslabon(raiz, serie, nn)
    ruta = c / f"{c.name}.valores.json"
    if not ruta.exists():
        raise FileNotFoundError(f"falta {ruta.name}: corre {c.name}/_calculo.py")
    return json.loads(ruta.read_text(encoding="utf-8"))


def eslabones(raiz: Path, serie: str) -> list[dict]:
    base = carpeta_series(raiz) / serie
    out = []
    for c in sorted(d for d in base.iterdir() if d.is_dir() and RX_NN.match(d.name)):
        ruta = c / f"{c.name}.valores.json"
        if ruta.exists():
            d = json.loads(ruta.read_text(encoding="utf-8"))
            d["_nn"] = RX_NN.match(c.name).group(1)      # la identidad es la carpeta
            out.append(d)
    return sorted(out, key=lambda d: d["orden"])


def resultados_modelo(raiz: Path, slug: str) -> dict:
    ruta = Path(raiz) / "docs" / "modelos" / slug / f"{slug}.resultados.json"
    if not ruta.exists():
        raise FileNotFoundError(f"no existe el modelo {slug!r}: falta {ruta}")
    return json.loads(ruta.read_text(encoding="utf-8"))


def _nn(orden: int) -> str:
    return f"{orden:02d}"


# ============================ el eslabón =============================
class Eslabon:
    """Lo que un `_calculo.py` declara. `carpeta` es la del eslabón
    (`Path(__file__).parent`); la raíz del sitio se deduce de ella."""

    def __init__(self, serie: str, orden: int, slug: str, titulo: str,
                 normas: list[str] | tuple[str, ...] = (), carpeta: str | Path | None = None,
                 raiz: str | Path | None = None):
        self.serie, self.orden, self.slug, self.titulo = serie, int(orden), slug, titulo
        self.normas = list(normas)
        self.carpeta = Path(carpeta).resolve() if carpeta else None
        if raiz is not None:
            self.raiz = Path(raiz).resolve()
        elif self.carpeta is not None:
            self.raiz = self.carpeta.parents[3]        # <raiz>/docs/series/<serie>/<NN-slug>
        else:
            raise ValueError("Eslabon necesita `carpeta` o `raiz`")
        self._caso: dict[str, dict] = {}
        self._entra: dict[str, dict] = {}
        self._pasos: dict[str, dict[str, dict]] = {}
        self._sale: dict[str, dict] = {}
        self._publicado: dict[str, str] = {}

    @property
    def nn(self) -> str:
        return _nn(self.orden)

    @property
    def nombre(self) -> str:
        return f"{self.nn}-{self.slug}"

    # --- declaraciones -------------------------------------------------
    def caso(self, simbolo: str, valor: float, unidad: str) -> float:
        self._caso[simbolo] = {"valor": float(valor), "unidad": unidad}
        return float(valor)

    def entra(self, simbolo: str, de: str, paso: str | None = None) -> float:
        if de.startswith("modelo:"):
            slug = de[len("modelo:"):]
            doc = resultados_modelo(self.raiz, slug)
            if simbolo not in doc["valores"]:
                raise KeyError(f"{simbolo!r} no es una salida del modelo {slug!r} "
                               f"(hay: {', '.join(doc['valores'])})")
            valor = float(doc["valores"][simbolo])
            unidad = doc.get("unidades", {}).get(simbolo, "")
        else:
            origen = cargar(self.raiz, self.serie, de)
            if simbolo not in origen["sale"]:
                raise KeyError(f"{simbolo!r} no está en el `sale` del eslabón {de} "
                               f"(hay: {', '.join(origen['sale'])})")
            if origen["orden"] >= self.orden:
                raise ValueError(f"el eslabón {de} no es anterior al {self.nn}")
            s = origen["sale"][simbolo]
            valor, unidad = float(s["valor"]), s["unidad"]
        self._entra[simbolo] = {"valor": valor, "unidad": unidad, "de": de, "paso": paso}
        return valor

    def paso(self, id: str, simbolo: str, valor: float, unidad: str) -> float:
        self._pasos.setdefault(id, {})[simbolo] = {"valor": float(valor), "unidad": unidad}
        return float(valor)

    def sale(self, simbolo: str, valor: float, unidad: str, paso: str,
             heredan: list[str] | tuple[str, ...] = ()) -> float:
        self._sale[simbolo] = {"valor": float(valor), "unidad": unidad, "paso": paso,
                               "heredan": [str(h) for h in heredan]}
        return float(valor)

    def publicado(self, valores: dict[str, str | float]) -> None:
        self._publicado = {k: (v if isinstance(v, str) else repr(float(v)).replace(".", ","))
                           for k, v in valores.items()}

    # --- salida ----------------------------------------------------------
    @property
    def hereda_de(self) -> list[str]:
        return sorted({e["de"] for e in self._entra.values() if not e["de"].startswith("modelo:")})

    def doc(self) -> dict[str, Any]:
        return {
            "esquema": ESQUEMA_VALORES,
            "serie": self.serie, "orden": self.orden, "slug": self.slug,
            "titulo": self.titulo, "normas": self.normas,
            "hereda_de": self.hereda_de,
            "entra": self._entra, "caso": self._caso, "pasos": self._pasos,
            "sale": self._sale, "publicado": self._publicado,
            **_cabecera(),
        }

    def _validar_oraculo(self) -> None:
        for simbolo, texto in self._publicado.items():
            if simbolo not in self._sale:
                raise ValueError(f"publicado {simbolo!r} no es una salida de este eslabón")
            v, p = self._sale[simbolo]["valor"], num(texto)
            if abs(v - p) > tolerancia(texto):
                raise ValueError(f"{simbolo}: el cálculo da {v!r} y el memo publicó {texto} "
                                 f"(tolerancia {tolerancia(texto):g}); no se ajusta el oráculo, "
                                 "se investiga")

    def escribir(self, ruta: str | Path | None = None) -> Path:
        self._validar_oraculo()
        ruta = Path(ruta) if ruta else self.carpeta / f"{self.nombre}.valores.json"
        with open(ruta, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(self.doc(), fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        return ruta

    def imprimir(self) -> None:
        ancho = max((len(s) for s in self._sale), default=8)
        for s, x in self._sale.items():
            pub = self._publicado.get(s, "")
            print(f"  {s:{ancho}s}  {x['valor']:16.8g}  {x['unidad']:6s}  {x['paso']:4s}"
                  f"  {('memo ' + pub) if pub else ''}")


def _cabecera() -> dict:
    try:
        from rukan import __version__
    except Exception:            # el sitio se construye sin rukan instalado
        __version__ = None
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                                cwd=Path(__file__).resolve().parent,
                                capture_output=True, text=True, timeout=10).stdout.strip() or None
    except Exception:
        commit = None
    return {"rukan": __version__, "commit": commit,
            "generado": datetime.datetime.now().isoformat(timespec="seconds")}


def main(argv: list[str], eslabon: Eslabon) -> int:
    """El `main` de un `_calculo.py`: escribe junto al script, o en `argv[1]`."""
    ruta = eslabon.escribir(argv[1] if len(argv) > 1 else None)
    eslabon.imprimir()
    print(f"escrito {ruta}")
    return 0


# ============================ la cadena ==============================
def verificar_cadena(raiz: Path, serie: str) -> list[str]:
    """Los chequeos de `verify_serie.js` que siguen teniendo sentido cuando la
    cadena se consume en vez de copiarse. Devuelve la lista de hallazgos; vacía
    si la serie cierra."""
    es = eslabones(raiz, serie)
    h: list[str] = []
    if not es:
        return [f"la serie {serie!r} no tiene eslabones con valores.json"]
    ordenes = [e["orden"] for e in es]
    if len(set(ordenes)) != len(ordenes):
        h.append(f"orden repetido: {sorted(ordenes)}")
    else:
        base = min(ordenes)
        if ordenes != list(range(base, base + len(ordenes))):
            h.append(f"orden no contiguo desde {base}: {ordenes}")
    por_nn = {e["_nn"]: e for e in es}
    for e in es:
        nn = e["_nn"]
        if nn != _nn(e["orden"]):
            h.append(f"{nn}: la carpeta dice {nn} y el orden del JSON es {e['orden']}")
        usados = sorted({x["de"] for x in e["entra"].values() if not x["de"].startswith("modelo:")})
        if usados != sorted(e["hereda_de"]):
            h.append(f"{nn}: hereda_de {e['hereda_de']} no coincide con lo que entra {usados}")
        for simbolo, x in e["entra"].items():
            de = x["de"]
            if de.startswith("modelo:"):
                slug = de[len("modelo:"):]
                try:
                    doc = resultados_modelo(raiz, slug)
                except FileNotFoundError as exc:
                    h.append(f"{nn}: {simbolo}: {exc}")
                    continue
                if simbolo not in doc["valores"]:
                    h.append(f"{nn}: {simbolo} no es una salida del modelo {slug}")
                elif float(doc["valores"][simbolo]) != x["valor"]:
                    h.append(f"{nn}: {simbolo} vale {x['valor']!r} y el modelo {slug} emite "
                             f"{doc['valores'][simbolo]!r}: recorrer el {nn}")
                continue
            o = por_nn.get(de)
            if o is None:
                h.append(f"{nn}: {simbolo} entra del eslabón {de}, que no existe")
                continue
            if o["orden"] >= e["orden"]:
                h.append(f"{nn}: el origen {de} de {simbolo} no es anterior (orden {o['orden']})")
            s = o["sale"].get(simbolo)
            if s is None:
                h.append(f"{nn}: {simbolo} no está en el sale del {de}")
                continue
            if float(s["valor"]) != x["valor"]:
                h.append(f"{nn}: {simbolo} entra como {x['valor']!r} y el {de} publica "
                         f"{s['valor']!r}: el {de} cambió y el {nn} no se recorrió")
            if s["unidad"] != x["unidad"]:
                h.append(f"{nn}: {simbolo} entra en {x['unidad']!r} y el {de} publica en "
                         f"{s['unidad']!r}: unidad distinta, el arnés no convierte")
            if nn not in s.get("heredan", []):
                h.append(f"{de}: {simbolo} no declara que lo hereda el {nn}")
        for simbolo, s in e["sale"].items():
            for hn in s.get("heredan", []):
                c = por_nn.get(hn)
                if c is None:
                    continue        # un consumidor que todavía no se migró: promesa, no hallazgo
                if simbolo not in c["entra"] or c["entra"][simbolo]["de"] != nn:
                    h.append(f"{nn}: {simbolo} dice que lo hereda el {hn}, y el {hn} no lo declara")
    return h


# ============================ las citas ==============================
RX_PDF = re.compile(r"`([^`]*\.pdf)`", re.I)
RX_IDEM = re.compile(r"\bPDF\s+[ií]dem\b", re.I)
RX_PAG = re.compile(r"\bpp?\.\s*(\d{1,4})(?:\s*[-–—]\s*(\d{1,4}))?")


def citas(md: str) -> list[dict]:
    """Las filas de la tabla `## Referencias`: clave, norma, cláusula, leída en,
    cita, nivel (`fuente` | `wiki` | `memo` | `pendiente` | `referencial` | `?`),
    pdf (heredado con «PDF ídem») y páginas."""
    m = re.search(r"^## Referencias\s*$(.*?)(?=^## |\Z)", md, flags=re.M | re.S)
    if not m:
        return []
    out: list[dict] = []
    ultimo_pdf = ""
    for linea in m.group(1).splitlines():
        if not linea.startswith("|"):
            continue
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
        if len(celdas) < 5 or celdas[0] in ("Clave", "") or set(celdas[0]) <= set("-: "):
            continue
        clave, norma, clausula, leida, cita = celdas[:5]
        nivel, pdf, paginas = "?", "", []
        if re.search(r"pendiente", leida, re.I):
            nivel = "pendiente"
        elif re.search(r"referencial", leida, re.I):
            nivel = "referencial"
        elif RX_PDF.search(leida) or RX_IDEM.search(leida):
            nivel = "fuente"
            mp = RX_PDF.search(leida)
            pdf = mp.group(1) if mp else ultimo_pdf
            ultimo_pdf = pdf
            for mg in RX_PAG.finditer(leida):
                a, b = int(mg.group(1)), mg.group(2)
                paginas += list(range(a, int(b) + 1)) if b and int(b) - a <= 40 else [a]
        elif "referencias/" in leida or "taller/" in leida:
            nivel = "wiki"
        elif re.search(r"heredad", leida, re.I) or "memos/" in leida:
            nivel = "memo"
        texto = cita.strip()
        texto = texto[1:-1].strip() if texto.startswith("«") and texto.endswith("»") else \
            ("" if texto in ("—", "-", "") else texto)
        out.append({"clave": clave, "norma": norma, "clausula": clausula, "leida_en": leida,
                    "cita": texto, "nivel": nivel, "pdf": pdf, "paginas": paginas})
    return out


# ============================ las figuras ============================
def cotas_sin_respaldo(svg: str, valores: dict, minimo: float = 10.0) -> list[str]:
    """Las cifras ≥ `minimo` que un `<text>` del SVG muestra y que no aparecen
    entre los valores del eslabón (la capa 2b de `verify_memo.js`)."""
    numeros: set[float] = set()
    for grupo in ("caso", "entra", "sale"):
        for x in valores.get(grupo, {}).values():
            numeros.add(abs(float(x["valor"])))
    for paso in valores.get("pasos", {}).values():
        for x in paso.values():
            numeros.add(abs(float(x["valor"])))
    faltan: list[str] = []
    for t in re.findall(r"<text[^>]*>([\s\S]*?)</text>", svg):
        t = re.sub(r"<[^>]+>", "", t)
        for c in re.findall(r"\d[\d\s.,]*\d|\d\d+", t):
            try:
                v = abs(num(c))
            except ValueError:
                continue
            if v < minimo:
                continue
            tol = 0.5 * 10.0 ** (-decimales(c))
            if not any(abs(v - n) <= tol for n in numeros):
                faltan.append(c.strip())
    return faltan
