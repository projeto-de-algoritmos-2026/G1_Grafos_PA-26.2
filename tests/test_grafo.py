import sys
from pathlib import Path

# garante que src/ esteja no path, não importa de onde o arquivo é executado
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from grafo import Grafo

def test_adicionar_aresta_mao_dupla():
    g = Grafo()
    g.adicionar_aresta("A", "B", 5)
    assert g.adj == {"A": {"B": 5}, "B": {"A": 5}}

def test_aresta_mao_unica():
    g = Grafo()
    g.adicionar_aresta("A", "B", 5, mao_dupla=False)
    assert g.adj == {"A": {"B": 5}, "B": {}}
