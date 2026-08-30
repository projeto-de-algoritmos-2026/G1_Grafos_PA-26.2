# Mapa fictício do bairro (loja + clientes + cruzamentos).
#
# Plano B: serve de garantia caso o mapa real via OSMnx (dados_reais.py) não funcione.
#
# O mapa não é só um caminho único loja -> cliente: tem ruas de sobra, do jeito
# que um bairro de verdade teria, pra dar trabalho de verdade pro Dijkstra:
#   - atalho:            cruz_1 -> cruz_3, mais curto que ir por cruz_2.
#   - caminho alternativo: dá pra chegar em cliente_E tanto por cruz_2 quanto
#     por cruz_3 -> cruz_2; o Dijkstra tem que escolher o mais curto.
#   - caminhos mais longos: cliente_D e cliente_E ficam numa ponta mais
#     distante do bairro, sem atalho, só rua mesmo.
#   - caminhos não usados: ruas que existem mas nunca entram na rota mais
#     curta de ninguém (ex: cruz_4 -> cliente_A é mais longo que ir direto
#     por cruz_1) e becos sem saída (beco_1, beco_2) que não levam a nenhum
#     cliente — só ocupam espaço no mapa, como uma rua real qualquer.
#   - quadra fechada: cruz_5 <-> cruz_7 fecha um anel externo (leste-norte),
#     como uma rua que contorna o quarteirão em vez de só um beco pendurado.
#     cliente_F fica nesse anel nem sempre é a via mais curta pra chegar nele.

from grafo import Grafo

coordenadas = {
    "loja": (3, 0),
    "cruz_1": (3, 2),
    "cliente_A": (5.2, 1.6),
    "cruz_2": (3, 5),
    "cliente_B": (5.3, 6.2),
    "cruz_3": (0, 5),
    "cliente_C": (-1, 7.3),
    "cruz_4": (7, 0.8),
    "beco_2": (9.3, 0.2),
    "cruz_5": (8, 4),
    "cliente_D": (10.3, 5),
    "cruz_6": (-3.2, 6),
    "beco_1": (-5.6, 6.6),
    "cruz_7": (2.6, 8.2),
    "cliente_E": (2.3, 11),
    "cruz_8": (5.6, 7.2),
    "cliente_F": (7.4, 8.6),
}

ruas = [
    # núcleo original
    ("loja", "cruz_1", 2),
    ("cruz_1", "cliente_A", 1),
    ("cruz_1", "cruz_2", 3),
    ("cruz_2", "cliente_B", 1),
    ("cruz_2", "cruz_3", 3),
    ("cruz_3", "cliente_C", 1),
    ("cruz_1", "cruz_3", 2),  # atalho: usado na rota até cliente_C

    # ramo leste — caminho mais longo até cliente_D + ruas não usadas
    ("cruz_1", "cruz_4", 4),
    ("cruz_4", "cliente_A", 5),   # rota alternativa até cliente_A, mais longa (não usada)
    ("cruz_4", "cruz_5", 2),
    ("cruz_5", "cliente_B", 3),   # rota alternativa até cliente_B, mais longa (não usada)
    ("cruz_5", "cliente_D", 2),
    ("cruz_4", "beco_2", 1),      # beco sem saída, não leva a nenhum cliente

    # ramo norte — caminho alternativo/mais longo até cliente_E
    ("cruz_2", "cruz_7", 4),
    ("cruz_3", "cruz_7", 6),      # segunda via até cruz_7, mais longa (não usada)
    ("cruz_7", "cliente_E", 3),

    # ramo oeste — rota alternativa até cliente_C + beco sem saída
    ("cruz_3", "cruz_6", 2),
    ("cruz_6", "cliente_C", 5),   # rota alternativa até cliente_C, mais longa (não usada)
    ("cruz_6", "beco_1", 1),      # beco sem saída, não leva a nenhum cliente

    # anel externo — fecha a quadra leste/norte, 6º cliente (cliente_F)
    ("cruz_5", "cruz_8", 3),
    ("cruz_8", "cruz_7", 3),      # segunda via do anel, mais longa (não usada pra chegar em cruz_8)
    ("cruz_8", "cliente_F", 2),
]


def montar_grafo_bairro() -> Grafo:
    """Monta o Grafo do bairro fictício a partir das ruas definidas acima."""
    g = Grafo()
    for u, v, peso in ruas:
        g.adicionar_aresta(u, v, peso)
    return g
