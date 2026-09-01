"""Gera as imagens do mapa fictício com a rota da loja até cada cliente."""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import networkx as nx

from dados_ficticios import coordenadas, montar_grafo_bairro
from dijkstra import dijkstra_com_caminho, reconstruir_caminho

CLIENTES = [
    "cliente_A",
    "cliente_B",
    "cliente_C",
    "cliente_D",
    "cliente_E",
    "cliente_F",
]


def _cor_do_no(no: str, caminho: list[str] | None) -> str:
    if no == "loja":
        return "#e74c3c"
    if caminho and no in caminho:
        return "#f39c12"  # nó faz parte da rota escolhida
    if no.startswith("cliente"):
        return "#2ecc71"
    if no.startswith("beco"):
        return "#bdc3c7"  # beco sem saída, fora de qualquer rota
    return "#87ceeb"  # cruzamento comum


def _arestas_mao_unica(grafo) -> list[tuple[str, str]]:
    """Lista as arestas (u, v) que só existem nesse sentido (ruas de mão única)."""
    return [
        (u, v)
        for u in grafo.nos()
        for v in grafo.adj[u]
        if u not in grafo.adj.get(v, {})
    ]


def desenhar_ficticio(grafo, coordenadas, caminho=None, destino_nome="", pasta="relatorio"):
    """Desenha o mapa fictício e destaca a rota da loja até `destino_nome`.

    As ruas de fundo (fora da rota) só ganham seta quando são de mão única.
    A rota destacada ganha seta em toda aresta, mostrando o sentido
    percorrido mesmo nas ruas de mão dupla.
    """
    G = nx.Graph()
    for u in grafo.nos():
        G.add_node(u)
    for u in grafo.nos():
        for v, peso in grafo.vizinhos(u):
            G.add_edge(u, v, weight=peso)

    mao_unica = _arestas_mao_unica(grafo)
    mao_dupla = [(u, v) for u, v in G.edges() if (u, v) not in mao_unica and (v, u) not in mao_unica]

    cores = [_cor_do_no(no, caminho) for no in G.nodes()]

    plt.figure(figsize=(11, 10))
    nx.draw_networkx_nodes(G, pos=coordenadas, node_color=cores, node_size=1200)
    nx.draw_networkx_labels(G, pos=coordenadas, font_size=8, font_weight="bold")

    nx.draw_networkx_edges(
        G, pos=coordenadas, edgelist=mao_dupla, edge_color="#999999", width=1.3
    )
    nx.draw_networkx_edges(
        G, pos=coordenadas, edgelist=mao_unica, edge_color="#666666", width=1.3,
        arrows=True, arrowstyle="-|>", arrowsize=16, node_size=1200,
    )

    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos=coordenadas, edge_labels=labels, font_size=7)

    if caminho:
        arestas_caminho = list(zip(caminho, caminho[1:]))
        nx.draw_networkx_edges(
            G, pos=coordenadas, edgelist=arestas_caminho, edge_color="#e74c3c", width=3,
            arrows=True, arrowstyle="-|>", arrowsize=22, node_size=1200,
        )

    plt.title(f"Rota da loja até {destino_nome}")
    plt.tight_layout()

    os.makedirs(pasta, exist_ok=True)
    plt.savefig(f"{pasta}/rota_ficticia_{destino_nome}.png", dpi=130)
    plt.close()


def rodar_mapa_ficticio():
    """Roda o Dijkstra uma vez a partir da loja e desenha a rota até cada cliente."""
    grafo = montar_grafo_bairro()
    dist, pred = dijkstra_com_caminho(grafo, "loja")

    for cliente in CLIENTES:
        caminho = reconstruir_caminho(pred, "loja", cliente)
        print(f"{cliente}: distância = {dist[cliente]}, caminho = {caminho}")
        desenhar_ficticio(grafo, coordenadas, caminho, cliente)


if __name__ == "__main__":
    rodar_mapa_ficticio()
