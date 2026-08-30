import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from grafo import Grafo
from dijkstra import dijkstra


def test_caminho_direto():
    g = Grafo()
    g.adicionar_aresta("A", "B", 5)
    dist = dijkstra(g, "A")
    assert dist["B"] == 5


def test_caminho_com_atalho():
    g = Grafo()
    g.adicionar_aresta("A", "B", 10)
    g.adicionar_aresta("A", "C", 2)
    g.adicionar_aresta("C", "B", 2)
    dist = dijkstra(g, "A")
    assert dist["B"] == 4


def test_no_desconectado():
    g = Grafo()
    g.adicionar_no("A")
    g.adicionar_no("Ilha")
    dist = dijkstra(g, "A")
    assert dist["Ilha"] == float("inf")


def test_mapa_ficticio_distancias_dos_clientes():
    from dados_ficticios import montar_grafo_bairro

    grafo = montar_grafo_bairro()
    dist = dijkstra(grafo, "loja")

    esperado = {
        "cliente_A": 3,
        "cliente_B": 6,
        "cliente_C": 5,
        "cliente_D": 10,
        "cliente_E": 12,
        "cliente_F": 13,
    }
    for cliente, distancia in esperado.items():
        assert dist[cliente] == distancia
