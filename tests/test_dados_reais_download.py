import os
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_OSMNX_REAL") != "1",
    reason="usa internet/OpenStreetMap; rode com RUN_OSMNX_REAL=1 para validar",
)


def test_download_conversao_e_nos_proximos_reais():
    import dados_reais

    inicio = time.perf_counter()
    G_osmnx = dados_reais.baixar_grafo_real()
    duracao = time.perf_counter() - inicio

    grafo = dados_reais.converter_para_grafo(G_osmnx)
    pontos = dados_reais.pontos_padrao_com_nos(G_osmnx)

    assert G_osmnx.number_of_nodes() > 0
    assert G_osmnx.number_of_edges() > 0
    assert len(list(grafo.nos())) == G_osmnx.number_of_nodes()
    assert any(grafo.adj[no] for no in grafo.nos())
    assert pontos["loja"]["no"] in G_osmnx.nodes
    assert all(cliente["no"] in G_osmnx.nodes for cliente in pontos["clientes"])
    assert duracao < 120
