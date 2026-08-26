class Grafo:
    def __init__(self):
        self.adj = {}  # {no: {vizinho: peso}}

    def adicionar_no(self, no):
        self.adj.setdefault(no, {})

    def adicionar_aresta(self, u, v, peso, mao_dupla=True):
        self.adicionar_no(u)
        self.adicionar_no(v)
        self.adj[u][v] = peso
        if mao_dupla:
            self.adj[v][u] = peso

    def vizinhos(self, no):
        return self.adj[no].items()

    def nos(self):
        return self.adj.keys()