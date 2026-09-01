# Mapa fictício do bairro (loja + clientes + cruzamentos).
#
# Plano B: serve de garantia caso o mapa real via OSMnx (dados_reais.py) não funcione.
#
# Todas as ruas aqui são de mão única. Isso não é uma limitação: pro
# Dijkstra, "mão dupla" nunca foi um conceito à parte — é só duas ruas de
# mão única em sentidos opostos com o mesmo peso. Então, em vez de ter uma
# entrada `(u, v, peso)` marcada como "mão dupla" por baixo dos panos, cada
# rua de duas mãos daqui vira duas entradas explícitas: `(u, v, peso)` e
# `(v, u, peso)`. O grafo final é idêntico, só a representação é mais direta.
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
#   - ruas só de ida: cruz_8 -> cruz_7 (sentido único no anel externo),
#     cruz_3 -> cruz_5 (diagonal longa ligando oeste e leste) e
#     cruz_5 -> beco_3 (só dá pra entrar no beco) não têm o par de volta —
#     nenhuma delas muda a distância mínima de ninguém (já não eram usadas
#     mesmo quando existia a possibilidade de ida e volta).
#   - entrada da loja: cruz_1 -> loja é uma rua separada da saída
#     (loja -> cruz_1), tipo portão de entrada/saída diferentes de um
#     depósito. Sem ela não existiria NENHUM jeito de voltar pra loja
#     (necessário pro roteiro de entrega em src/roteiro_entrega.py).

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
    "beco_3": (9.2, 2.3),
}

ruas = [
    # núcleo original
    ("loja", "cruz_1", 2),      # saída da loja
    ("cruz_1", "loja", 2),      # entrada da loja (portão separado)

    ("cruz_1", "cliente_A", 1),
    ("cliente_A", "cruz_1", 1),

    ("cruz_1", "cruz_2", 3),
    ("cruz_2", "cruz_1", 3),

    ("cruz_2", "cliente_B", 1),
    ("cliente_B", "cruz_2", 1),

    ("cruz_2", "cruz_3", 3),
    ("cruz_3", "cruz_2", 3),

    ("cruz_3", "cliente_C", 1),
    ("cliente_C", "cruz_3", 1),

    ("cruz_1", "cruz_3", 2),    # atalho: usado na rota até cliente_C
    ("cruz_3", "cruz_1", 2),

    # ramo leste — caminho mais longo até cliente_D + ruas não usadas
    ("cruz_1", "cruz_4", 4),
    ("cruz_4", "cruz_1", 4),

    ("cruz_4", "cliente_A", 5),  # rota alternativa até cliente_A, mais longa (não usada)
    ("cliente_A", "cruz_4", 5),

    ("cruz_4", "cruz_5", 2),
    ("cruz_5", "cruz_4", 2),

    ("cruz_5", "cliente_B", 3),  # rota alternativa até cliente_B, mais longa (não usada)
    ("cliente_B", "cruz_5", 3),

    ("cruz_5", "cliente_D", 2),
    ("cliente_D", "cruz_5", 2),

    ("cruz_4", "beco_2", 1),     # beco sem saída, não leva a nenhum cliente
    ("beco_2", "cruz_4", 1),

    # ramo norte — caminho alternativo/mais longo até cliente_E
    ("cruz_2", "cruz_7", 4),
    ("cruz_7", "cruz_2", 4),

    ("cruz_3", "cruz_7", 6),     # segunda via até cruz_7, mais longa (não usada)
    ("cruz_7", "cruz_3", 6),

    ("cruz_7", "cliente_E", 3),
    ("cliente_E", "cruz_7", 3),

    # ramo oeste — rota alternativa até cliente_C + beco sem saída
    ("cruz_3", "cruz_6", 2),
    ("cruz_6", "cruz_3", 2),

    ("cruz_6", "cliente_C", 5),  # rota alternativa até cliente_C, mais longa (não usada)
    ("cliente_C", "cruz_6", 5),

    ("cruz_6", "beco_1", 1),     # beco sem saída, não leva a nenhum cliente
    ("beco_1", "cruz_6", 1),

    # anel externo — fecha a quadra leste/norte, 6º cliente (cliente_F)
    ("cruz_5", "cruz_8", 3),
    ("cruz_8", "cruz_5", 3),

    ("cruz_8", "cruz_7", 3),     # só de ida: sentido único no anel externo (já não era usada)

    ("cruz_8", "cliente_F", 2),
    ("cliente_F", "cruz_8", 2),

    # conectores novos — mais ruas de sobra
    ("cruz_2", "cruz_5", 5),     # atravessa o meio do bairro, mais longa (não usada)
    ("cruz_5", "cruz_2", 5),

    ("cruz_1", "cruz_6", 5),     # liga direto ao ramo oeste, mais longa que ir por cruz_3
    ("cruz_6", "cruz_1", 5),

    ("cruz_3", "cruz_5", 6),     # só de ida: diagonal longa oeste-leste
    ("cruz_5", "beco_3", 2),     # só de ida: beco novo, só dá pra entrar
]


def montar_grafo_bairro() -> Grafo:
    """Monta o Grafo do bairro fictício a partir das ruas definidas acima.

    Toda rua em `ruas` é `(u, v, peso)` e representa mão única no sentido
    `u -> v`. Uma rua de duas mãos é sempre duas entradas separadas
    (`(u, v, peso)` e `(v, u, peso)`), nunca uma flag à parte.
    """
    g = Grafo()
    for u, v, peso in ruas:
        g.adicionar_aresta(u, v, peso, mao_dupla=False)
    return g
