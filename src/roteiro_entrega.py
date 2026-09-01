"""Roteiro de entrega: loja -> todos os clientes -> volta pra loja (bônus/extra).

Importante: isso NÃO é o Dijkstra do projeto, é um algoritmo diferente por
cima dele. Dijkstra só responde "qual o caminho mais curto até UM destino
fixo?" — decidir a MELHOR ORDEM de visitar vários destinos numa única
viagem é o problema do caixeiro-viajante (TSP), que é NP-difícil (não tem
algoritmo exato conhecido que resolva em tempo polinomial pra qualquer n).

Aqui usamos a heurística gulosa do "vizinho mais próximo": a cada passo,
roda `dijkstra_com_caminho` a partir de onde está agora e vai pro destino
não visitado mais próximo. Complexidade O(k * (n + m) log n), pra k
clientes — continua polinomial, mas NÃO garante a rota mais curta possível
entre todos os clientes, só uma aproximação razoável.
"""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D

from dados_ficticios import coordenadas, montar_grafo_bairro
from dijkstra import dijkstra_com_caminho, reconstruir_caminho
from main import _arestas_mao_unica, _cor_do_no

CLIENTES = [
    "cliente_A",
    "cliente_B",
    "cliente_C",
    "cliente_D",
    "cliente_E",
    "cliente_F",
]

# uma cor por perna do roteiro (loja->1º cliente, cliente->cliente, ..., volta pra loja)
CORES_PERNA = [
    "#9b59b6",  # roxo
    "#2980b9",  # azul
    "#16a085",  # verde-água
    "#e91e63",  # rosa
    "#8d5524",  # marrom
    "#607d8b",  # cinza-azulado
    "#f1c40f",  # amarelo
]


def vizinho_mais_proximo(grafo, origem: str, destinos: list[str]):
    """Monta um roteiro guloso: origem -> destino não visitado mais próximo -> ... -> origem.

    Retorna `(ordem_de_visita, pernas, distancia_total)`, onde `pernas` é a
    lista dos caminhos de cada trecho (na ordem percorrida). Levanta
    `ValueError` se algum destino (ou a volta pra origem) for inalcançável.
    """
    restantes = set(destinos)
    atual = origem
    ordem = [origem]
    pernas: list[list[str]] = []
    distancia_total = 0.0

    while restantes:
        dist, pred = dijkstra_com_caminho(grafo, atual)
        alcancaveis = {c: dist[c] for c in restantes if dist[c] != float("inf")}
        if not alcancaveis:
            raise ValueError(
                f"Nenhum destino em {sorted(restantes)} é alcançável a partir de {atual}"
            )

        proximo = min(alcancaveis, key=alcancaveis.get)
        pernas.append(reconstruir_caminho(pred, atual, proximo))
        distancia_total += dist[proximo]
        ordem.append(proximo)
        restantes.remove(proximo)
        atual = proximo

    dist, pred = dijkstra_com_caminho(grafo, atual)
    if dist[origem] == float("inf"):
        raise ValueError(f"Não há caminho de volta de {atual} até {origem}")
    pernas.append(reconstruir_caminho(pred, atual, origem))
    distancia_total += dist[origem]
    ordem.append(origem)

    return ordem, pernas, distancia_total


def desenhar_roteiro(grafo, coordenadas, pernas, ordem, pasta="relatorio"):
    """Desenha o mapa inteiro com o roteiro de entrega completo, uma cor por trecho.

    Toda aresta que faz parte do roteiro ganha seta (mostrando o sentido
    percorrido), mesmo nas ruas de mão dupla — só as ruas de fundo (fora da
    rota) continuam sem seta quando são de mão dupla.
    """
    G = nx.Graph()
    for u in grafo.nos():
        G.add_node(u)
    for u in grafo.nos():
        for v, peso in grafo.vizinhos(u):
            G.add_edge(u, v, weight=peso)

    mao_unica = _arestas_mao_unica(grafo)
    mao_dupla_fundo = [
        (u, v) for u, v in G.edges() if (u, v) not in mao_unica and (v, u) not in mao_unica
    ]

    caminho_completo = pernas[0][:]
    for perna in pernas[1:]:
        caminho_completo.extend(perna[1:])

    cores_no = [_cor_do_no(no, caminho_completo) for no in G.nodes()]

    plt.figure(figsize=(12, 11))
    nx.draw_networkx_nodes(G, pos=coordenadas, node_color=cores_no, node_size=1200)
    nx.draw_networkx_labels(G, pos=coordenadas, font_size=8, font_weight="bold")

    # ruas de fundo, fora do roteiro
    nx.draw_networkx_edges(G, pos=coordenadas, edgelist=mao_dupla_fundo, edge_color="#dddddd", width=1.0)
    nx.draw_networkx_edges(
        G, pos=coordenadas, edgelist=mao_unica, edge_color="#cccccc", width=1.0,
        arrows=True, arrowstyle="-|>", arrowsize=12, node_size=1200,
    )
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos=coordenadas, edge_labels=labels, font_size=7)

    # cada perna do roteiro com cor própria + seta em toda aresta, levemente
    # curvada pra não sobrepor quando duas pernas usam a mesma rua em sentidos opostos
    legenda = []
    for i, perna in enumerate(pernas):
        cor = CORES_PERNA[i % len(CORES_PERNA)]
        arestas_perna = list(zip(perna, perna[1:]))
        nx.draw_networkx_edges(
            G, pos=coordenadas, edgelist=arestas_perna, edge_color=cor, width=3,
            arrows=True, arrowstyle="-|>", arrowsize=20, node_size=1200,
            connectionstyle="arc3,rad=0.08",
        )
        legenda.append(Line2D([0], [0], color=cor, lw=3, label=f"{ordem[i]} → {ordem[i + 1]}"))

    plt.legend(handles=legenda, loc="upper left", fontsize=7, framealpha=0.9, title="Trechos do roteiro")

    ordem_str = " -> ".join(ordem)
    plt.title(f"Roteiro de entrega (vizinho mais próximo): {ordem_str}", fontsize=10)

    os.makedirs(pasta, exist_ok=True)
    plt.savefig(f"{pasta}/roteiro_entrega_completo.png", dpi=130)
    plt.close()


def rodar_roteiro_entrega():
    grafo = montar_grafo_bairro()
    ordem, pernas, distancia_total = vizinho_mais_proximo(grafo, "loja", CLIENTES)

    print("Ordem de visita:", " -> ".join(ordem))
    for i, perna in enumerate(pernas):
        print(f"  {ordem[i]} -> {ordem[i + 1]}: {perna}")
    print(f"Distância total do roteiro: {distancia_total}")

    desenhar_roteiro(grafo, coordenadas, pernas, ordem)


if __name__ == "__main__":
    rodar_roteiro_entrega()
