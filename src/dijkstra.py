"""Algoritmo de Dijkstra: menor distância da origem até todos os nós do grafo.

Roda uma única vez a partir da loja e já devolve a distância mínima pra
qualquer nó do grafo (cruzamentos e clientes) — não precisa rodar de novo
pra cada cliente.
"""

import heapq

from grafo import Grafo


def dijkstra(grafo: Grafo, origem):
    """Calcula a distância mínima de `origem` até cada nó de `grafo`.

    Retorna um dicionário {no: distancia}. Nós inalcançáveis a partir da
    origem ficam com distância `float('inf')`.
    """
    dist = {no: float("inf") for no in grafo.nos()}
    dist[origem] = 0
    visitados = set()
    fila = [(0, origem)]

    while fila:
        d_atual, u = heapq.heappop(fila)
        if u in visitados:
            continue
        visitados.add(u)

        for v, peso in grafo.vizinhos(u):
            nova_dist = d_atual + peso
            if nova_dist < dist[v]:
                dist[v] = nova_dist
                heapq.heappush(fila, (nova_dist, v))

    return dist
