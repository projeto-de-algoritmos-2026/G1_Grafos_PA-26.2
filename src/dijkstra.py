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


def dijkstra_com_caminho(grafo: Grafo, origem):
    """Calcula distancias minimas e predecessores a partir de `origem`.

    Retorna `(dist, predecessor)`, onde `predecessor[no]` guarda o no anterior
    no menor caminho encontrado ate `no`. Nos inalcançaveis ficam com
    predecessor `None`.
    """
    dist = {no: float("inf") for no in grafo.nos()}
    dist[origem] = 0
    predecessor = {no: None for no in grafo.nos()}
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
                predecessor[v] = u
                heapq.heappush(fila, (nova_dist, v))

    return dist, predecessor


def reconstruir_caminho(predecessor, origem, destino):
    """Reconstrói o caminho de `origem` ate `destino`.

    Devolve uma lista com os nos do caminho, ou `None` quando o destino nao
    foi alcançado a partir da origem.
    """
    caminho = []
    atual = destino

    while atual is not None:
        caminho.append(atual)
        atual = predecessor.get(atual)

    caminho.reverse()
    if not caminho or caminho[0] != origem:
        return None

    return caminho
