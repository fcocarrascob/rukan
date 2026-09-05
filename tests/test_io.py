"""`io.py` — el archivo de proyecto: lo que entra tiene que salir igual, y lo que
está mal tiene que fallar nombrando el campo.

No se corre ningún análisis acá: se prueba la serialización, la validación del
esquema, la resolución nombre → id y la conversión de unidades en la frontera.
"""

from __future__ import annotations

import copy
import json

import pytest

from rukan import io
from rukan.model import FrameElement, Material, Model, NodalMass, Node, Section


@pytest.fixture
def portico() -> Model:
    """Pórtico plano de un vano con nombres en nudos, secciones y barras."""
    fijo, libre = (True,) * 6, (False,) * 6
    nodos = [Node(1, 0.0, 0.0, 0.0, fijo, nombre="A0"),
             Node(2, 0.0, 6.0, 0.0, fijo, nombre="B0"),
             Node(3, 0.0, 0.0, 4.0, libre, nombre="A1"),
             Node(4, 0.0, 6.0, 4.0, libre, nombre="B1")]
    sec = Section(1, A=1e-2, Iy=1e-4, Iz=1e-4, J=1e-5, nombre="TUBO")
    els = [FrameElement(1, 1, 3, 1, 1, (1.0, 0.0, 0.0), nombre="COL_A"),
           FrameElement(2, 2, 4, 1, 1, (1.0, 0.0, 0.0), nombre="COL_B"),
           FrameElement(3, 3, 4, 1, 1, (1.0, 0.0, 0.0), nombre="VIGA",
                        release_z_i=True)]
    return Model(nodes=nodos, materials=[Material(1, E=2.0e8, nu=0.3, rho=7.85)],
                 sections=[sec], elements=els,
                 masses=[NodalMass(3, (1.0,) * 3 + (0.0,) * 3),
                         NodalMass(4, (1.0,) * 3 + (0.0,) * 3)])


@pytest.fixture
def proyecto(portico) -> io.Proyecto:
    return io.Proyecto(
        model=portico, titulo="pórtico de prueba",
        casos={"D": {"peso_propio": "distribuido"},
               "H": {"nodales": [{"nudo": "A1", "F": [0, 1.0, 0, 0, 0, 0]}]}},
        combinaciones={"1.2D+H": {"D": 1.2, "H": 1.0}},
        analisis={"modal": {"n_modos": 2}},
        salidas={"T1": {"que": "periodo", "modo": 1},
                 "T_star_Y": {"que": "periodo_dominante", "direccion": "Y"},
                 "Uy": {"que": "participacion_dominante", "direccion": "Y"},
                 "macum_Y": {"que": "masa_acumulada", "direccion": "Y"},
                 "d": {"que": "desplazamiento", "nudo": "A1", "gdl": "Uy", "caso": "H"},
                 "R": {"que": "reaccion", "nudo": "A0", "gdl": "Uz", "caso": "1.2D+H"},
                 "M": {"que": "fuerza", "barra": "COL_A", "extremo": "i",
                       "componente": "Mz", "caso": "H"},
                 "W": {"que": "peso_total"}})


# ------------------------------------------------------------ round-trip
def test_round_trip_por_dict(proyecto):
    d = io.to_dict(proyecto)
    assert d["esquema"] == io.ESQUEMA_PROYECTO
    p2 = io.from_dict(d)
    assert p2.model == proyecto.model
    assert p2.casos == proyecto.casos
    assert p2.combinaciones == proyecto.combinaciones
    assert p2.analisis == proyecto.analisis
    assert p2.salidas == proyecto.salidas
    assert p2.titulo == proyecto.titulo
    # y el dict que sale del segundo es el mismo: la serialización es estable
    assert io.to_dict(p2) == d


def test_round_trip_por_archivo(proyecto, tmp_path):
    ruta = tmp_path / "p.proyecto.json"
    io.save(proyecto, ruta)
    texto = ruta.read_text(encoding="utf-8")
    assert "rukan/proyecto@1" in texto
    assert json.loads(texto)["nudos"][0]["nombre"] == "A0"
    p2 = io.load(ruta)
    assert p2.model == proyecto.model
    assert p2.salidas == proyecto.salidas


def test_el_dict_es_json_plano(proyecto):
    """Sin tuplas ni objetos: lo que escribe `save` lo lee cualquier cosa."""
    d = io.to_dict(proyecto)
    json.dumps(d)  # no debe fallar
    assert isinstance(d["nudos"][0]["fijo"], list)
    assert isinstance(d["barras"][0]["vecxz"], list)


# ------------------------------------------------------------ nombres e ids
def test_nombre_o_id_resuelven_igual(proyecto):
    assert proyecto.nudo_id("A1") == 3
    assert proyecto.nudo_id(3) == 3
    assert proyecto.barra_id("VIGA") == 3
    assert proyecto.barra_id(2) == 2


def test_barras_por_nombre_en_el_archivo(proyecto):
    """`i`/`j`, `material` y `seccion` de una barra aceptan nombre o id."""
    d = io.to_dict(proyecto)
    d["barras"][2]["i"], d["barras"][2]["j"] = "A1", "B1"
    d["barras"][2]["seccion"] = "TUBO"
    p2 = io.from_dict(d)
    assert p2.model.elements[2].node_i == 3
    assert p2.model.elements[2].node_j == 4
    assert p2.model.elements[2].section == 1


# ------------------------------------------------------------ validación
def _roto(proyecto, mutar):
    d = copy.deepcopy(io.to_dict(proyecto))
    mutar(d)
    return d


@pytest.mark.parametrize("mutar, texto", [
    (lambda d: d.update(esquema="rukan/proyecto@9"), "esquema"),
    (lambda d: d["nudos"].append(dict(d["nudos"][0])), "nudos"),
    (lambda d: d["nudos"][1].update(nombre="A0"), "A0"),
    (lambda d: d["barras"][0].update(i=99), "99"),
    (lambda d: d["barras"][0].update(seccion="NADA"), "NADA"),
    (lambda d: d["masas"][0].update(nudo="Z9"), "Z9"),
    (lambda d: d["masas"][0].update(valores=[1, 1, 1]), "valores"),
    (lambda d: d["casos"]["D"].update(peso_propio="magico"), "peso_propio"),
    (lambda d: d["casos"]["D"].update(sorpresa=1), "sorpresa"),
    (lambda d: d["casos"]["H"]["nodales"][0].update(nudo="Z9"), "Z9"),
    (lambda d: d["combinaciones"]["1.2D+H"].update(Lr=1.6), "Lr"),
    (lambda d: d["analisis"].update(espectral={}), "espectral"),
    (lambda d: d["analisis"]["modal"].update(n_modos=0), "n_modos"),
    (lambda d: d["salidas"]["T1"].update(que="periodo_magico"), "periodo_magico"),
    (lambda d: d["salidas"]["T1"].update(modo=7), "modo"),
    (lambda d: d["salidas"]["d"].update(caso="NADA"), "NADA"),
    (lambda d: d["salidas"]["d"].update(gdl="Uq"), "Uq"),
    (lambda d: d["salidas"]["d"].update(nudo="Z9"), "Z9"),
    (lambda d: d["salidas"]["M"].update(componente="Mq"), "Mq"),
    (lambda d: d["salidas"]["M"].update(extremo="k"), "extremo"),
    (lambda d: d["salidas"]["T_star_Y"].update(direccion="W"), "direccion"),
    (lambda d: d["salidas"]["d"].pop("caso"), "caso"),
    (lambda d: d.update(unidades={"longitud": "codos", "fuerza": "kN", "masa": "t"}), "codos"),
])
def test_el_esquema_falla_nombrando_el_campo(proyecto, mutar, texto):
    with pytest.raises(io.ErrorDeEsquema) as exc:
        io.from_dict(_roto(proyecto, mutar))
    assert texto in str(exc.value)


def test_una_sonda_modal_exige_analisis_modal(proyecto):
    d = io.to_dict(proyecto)
    d["analisis"] = {}
    with pytest.raises(io.ErrorDeEsquema, match="modal"):
        io.from_dict(d)


def test_un_proyecto_minimo_carga(portico):
    """Modelo solo, sin casos ni salidas: también es un proyecto válido."""
    d = io.to_dict(io.Proyecto(model=portico))
    p = io.from_dict(d)
    assert p.casos == {} and p.salidas == {} and p.analisis == {}


# ------------------------------------------------------------ unidades
def test_convierte_en_la_frontera(proyecto):
    """Un archivo en mm y N entra al núcleo en m y kN, sin tocar nada más."""
    d = io.to_dict(proyecto)
    d["unidades"] = {"longitud": "mm", "fuerza": "N", "masa": "kg"}
    for n in d["nudos"]:
        n["x"], n["y"], n["z"] = n["x"] * 1e3, n["y"] * 1e3, n["z"] * 1e3
    for s in d["secciones"]:
        s["A"] *= 1e6
        s["Iy"] *= 1e12
        s["Iz"] *= 1e12
        s["J"] *= 1e12
    for m in d["materiales"]:
        m["E"] *= 1e3 / 1e6        # kN/m² -> N/mm²
        m["rho"] *= 1e3 / 1e9      # t/m³ -> kg/mm³
    for ms in d["masas"]:
        ms["valores"] = [v * 1e3 for v in ms["valores"][:3]] + \
                        [v * 1e3 * 1e6 for v in ms["valores"][3:]]
    d["casos"]["H"]["nodales"][0]["F"] = [0, 1000.0, 0, 0, 0, 0]
    p2 = io.from_dict(d)
    assert p2.model.nodes[1].y == pytest.approx(6.0)
    assert p2.model.sections[0].Iz == pytest.approx(1e-4)
    assert p2.model.materials[0].E == pytest.approx(2.0e8)
    assert p2.model.materials[0].rho == pytest.approx(7.85)
    assert p2.model.masses[0].values[0] == pytest.approx(1.0)
    assert p2.casos["H"]["nodales"][0]["F"][1] == pytest.approx(1.0)
    # y `to_dict` escribe siempre el sistema interno
    assert io.to_dict(p2)["unidades"] == io.UNIDADES_INTERNAS


def test_sha256_de_un_archivo(tmp_path):
    ruta = tmp_path / "x.json"
    ruta.write_bytes(b"hola")
    assert io.sha256(ruta) == \
        "b221d9dbb083a7f33428d7c2a3c3198ae925614d70210e28716ccaa7cd4ddb79"


# ------------------------------------------------------------ la sonda esfuerzo
def _con_esfuerzo(proyecto, **campos):
    d = io.to_dict(proyecto)
    d["salidas"] = {"M": {"que": "esfuerzo", "barra": "VIGA",
                          "componente": "Mz", "caso": "D", **campos}}
    return d


def test_la_sonda_esfuerzo_acepta_x_o_x_rel(proyecto):
    p = io.from_dict(_con_esfuerzo(proyecto, x_rel=0.35))
    assert p.salidas["M"]["x_rel"] == 0.35
    p = io.from_dict(_con_esfuerzo(proyecto, x=2.0))
    assert p.salidas["M"]["x"] == pytest.approx(2.0)


@pytest.mark.parametrize("campos,trozo", [
    ({}, "x"),                              # ni x ni x_rel
    ({"x": 1.0, "x_rel": 0.5}, "uno"),      # los dos
    ({"x_rel": 1.4}, "x_rel"),              # fuera de 0..1
    ({"x_rel": -0.1}, "x_rel"),
    ({"x": 99.0}, "largo"),                 # fuera de la barra
    ({"x": -1.0}, "largo"),
])
def test_la_sonda_esfuerzo_valida_la_estacion(proyecto, campos, trozo):
    with pytest.raises(io.ErrorDeEsquema, match=trozo):
        io.from_dict(_con_esfuerzo(proyecto, **campos))


def test_la_estacion_x_se_convierte_en_la_frontera(proyecto):
    """`x` es una longitud: en un archivo en mm entra al núcleo en metros."""
    d = _con_esfuerzo(proyecto, x=2000.0)
    d["unidades"] = {"longitud": "mm", "fuerza": "N", "masa": "kg"}
    for n in d["nudos"]:
        n["x"], n["y"], n["z"] = n["x"] * 1e3, n["y"] * 1e3, n["z"] * 1e3
    for s in d["secciones"]:
        s["A"] *= 1e6
        s["Iy"] *= 1e12
        s["Iz"] *= 1e12
        s["J"] *= 1e12
    for m in d["materiales"]:
        m["E"] *= 1e3 / 1e6
        m["rho"] *= 1e3 / 1e9
    for ms in d["masas"]:
        ms["valores"] = [v * 1e3 for v in ms["valores"][:3]] + \
                        [v * 1e3 * 1e6 for v in ms["valores"][3:]]
    d["casos"]["H"]["nodales"][0]["F"] = [0, 1000.0, 0, 0, 0, 0]
    p = io.from_dict(d)
    assert p.salidas["M"]["x"] == pytest.approx(2.0)
    assert io.to_dict(p)["salidas"]["M"]["x"] == pytest.approx(2.0)


def test_largo_barra_resuelve_por_nombre_y_por_id(proyecto):
    assert proyecto.largo_barra("VIGA") == pytest.approx(6.0)
    assert proyecto.largo_barra(1) == pytest.approx(4.0)
