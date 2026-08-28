import sys
from pathlib import Path
from types import SimpleNamespace

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import dados_reais
from grafo import Grafo


def criar_grafo_osmnx_fake():
    G = nx.MultiDiGraph()
    G.graph["crs"] = "epsg:4326"
    G.add_node(1, x=-47.88518, y=-15.76598)
    G.add_node(2, x=-47.88418, y=-15.76632)
    G.add_node(3, x=-47.88376, y=-15.76522)
    G.add_edge(1, 2, length=120.5)
    G.add_edge(2, 1, length=121.0)
    G.add_edge(1, 2, length=118.0)
    G.add_edge(2, 3, length=95.0)
    return G


def test_converter_para_grafo_preserva_direcao_e_menor_aresta():
    G_osmnx = criar_grafo_osmnx_fake()

    grafo = dados_reais.converter_para_grafo(G_osmnx)

    assert isinstance(grafo, Grafo)
    assert set(grafo.nos()) == {1, 2, 3}
    assert grafo.adj[1][2] == 118.0
    assert grafo.adj[2][1] == 121.0
    assert grafo.adj[2][3] == 95.0
    assert 1 not in grafo.adj[3]


def test_escolher_no_mais_proximo_chama_osmnx_com_lon_lat(monkeypatch):
    chamadas = []

    def nearest_nodes(G, X, Y):
        chamadas.append((G, X, Y))
        return 123

    monkeypatch.setattr(
        dados_reais,
        "ox",
        SimpleNamespace(distance=SimpleNamespace(nearest_nodes=nearest_nodes)),
    )

    no = dados_reais.escolher_no_mais_proximo("grafo", lat=-15.76598, lon=-47.88518)

    assert no == 123
    assert chamadas == [("grafo", -47.88518, -15.76598)]


def test_escolher_no_mais_proximo_tem_fallback_sem_scikit_learn(monkeypatch):
    G_osmnx = criar_grafo_osmnx_fake()

    def nearest_nodes(G, X, Y):
        raise ImportError("scikit-learn must be installed")

    monkeypatch.setattr(
        dados_reais,
        "ox",
        SimpleNamespace(distance=SimpleNamespace(nearest_nodes=nearest_nodes)),
    )

    no = dados_reais.escolher_no_mais_proximo(
        G_osmnx,
        lat=-15.76630,
        lon=-47.88420,
    )

    assert no == 2


def test_area_padrao_tem_loja_e_clientes():
    assert dados_reais.AREA_PADRAO["bbox"] == (
        -47.88770,
        -15.76685,
        -47.88295,
        -15.76305,
    )
    assert dados_reais.AREA_PADRAO["loja"].nome.startswith("Loja")
    assert len(dados_reais.AREA_PADRAO["clientes"]) >= 3
