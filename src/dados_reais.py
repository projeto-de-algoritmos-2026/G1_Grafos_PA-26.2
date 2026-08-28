from __future__ import annotations

from dataclasses import dataclass
from math import asin, cos, radians, sin, sqrt

from grafo import Grafo

try:
    import osmnx as ox
except ModuleNotFoundError:  # pragma: no cover - validado pelos testes quando instalado
    ox = None


@dataclass(frozen=True)
class PontoEntrega:
    nome: str
    lat: float
    lon: float


# Area pequena em Brasilia, perto da CLN/SQN 204-205, Asa Norte.
# Formato do bbox no OSMnx 2.x: (lon_min, lat_min, lon_max, lat_max).
AREA_PADRAO = {
    "nome": "CLN/SQN 204-205, Asa Norte, Brasilia",
    "bbox": (-47.88770, -15.76685, -47.88295, -15.76305),
    "loja": PontoEntrega("Loja - CLN 204", -15.76598, -47.88518),
    "clientes": [
        PontoEntrega("Cliente 1 - SQN 204", -15.76495, -47.88653),
        PontoEntrega("Cliente 2 - SQN 205", -15.76522, -47.88376),
        PontoEntrega("Cliente 3 - CLN 205", -15.76632, -47.88418),
    ],
}


def _exigir_osmnx():
    if ox is None:
        raise ModuleNotFoundError(
            "O pacote 'osmnx' nao esta instalado. Rode: pip install -r requirements.txt"
        )
    return ox


def baixar_grafo_real(
    bbox: tuple[float, float, float, float] | None = None,
    network_type: str = "drive",
):
    """Baixa um grafo real pequeno do OpenStreetMap usando OSMnx."""
    osmnx = _exigir_osmnx()
    area = bbox or AREA_PADRAO["bbox"]
    return osmnx.graph_from_bbox(
        area,
        network_type=network_type,
        simplify=True,
        retain_all=False,
        truncate_by_edge=True,
    )


def converter_para_grafo(G_osmnx) -> Grafo:
    """Converte um grafo do OSMnx/NetworkX para a classe Grafo do projeto."""
    grafo = Grafo()

    for no in G_osmnx.nodes:
        grafo.adicionar_no(no)

    for u, v, dados in G_osmnx.edges(data=True):
        distancia = float(dados.get("length", 1))
        distancia_atual = grafo.adj.get(u, {}).get(v)

        if distancia_atual is None or distancia < distancia_atual:
            grafo.adicionar_aresta(u, v, distancia, mao_dupla=False)

    return grafo


def escolher_no_mais_proximo(G_osmnx, lat: float, lon: float):
    """Retorna o id do no do grafo mais proximo de uma coordenada lat/lon."""
    osmnx = _exigir_osmnx()

    try:
        return osmnx.distance.nearest_nodes(G_osmnx, X=lon, Y=lat)
    except ImportError:
        return _escolher_no_mais_proximo_sem_dependencia_extra(G_osmnx, lat, lon)


def _distancia_haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    raio_terra_m = 6_371_000
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)

    a = (
        sin(d_lat / 2) ** 2
        + cos(lat1_rad) * cos(lat2_rad) * sin(d_lon / 2) ** 2
    )
    return 2 * raio_terra_m * asin(sqrt(a))


def _escolher_no_mais_proximo_sem_dependencia_extra(G_osmnx, lat: float, lon: float):
    melhor_no = None
    melhor_distancia = float("inf")

    for no, dados in G_osmnx.nodes(data=True):
        if "x" not in dados or "y" not in dados:
            continue

        distancia = _distancia_haversine_m(lat, lon, dados["y"], dados["x"])
        if distancia < melhor_distancia:
            melhor_no = no
            melhor_distancia = distancia

    if melhor_no is None:
        raise ValueError("O grafo nao possui nos com coordenadas 'x' e 'y'.")

    return melhor_no


def pontos_padrao_com_nos(G_osmnx):
    """Associa loja e clientes padrao aos nos mais proximos do grafo real."""
    loja = AREA_PADRAO["loja"]
    clientes = AREA_PADRAO["clientes"]

    return {
        "area": AREA_PADRAO["nome"],
        "loja": {
            "nome": loja.nome,
            "lat": loja.lat,
            "lon": loja.lon,
            "no": escolher_no_mais_proximo(G_osmnx, loja.lat, loja.lon),
        },
        "clientes": [
            {
                "nome": cliente.nome,
                "lat": cliente.lat,
                "lon": cliente.lon,
                "no": escolher_no_mais_proximo(G_osmnx, cliente.lat, cliente.lon),
            }
            for cliente in clientes
        ],
    }


def executar_demo():
    """Executa um exemplo simples do download, conversao e pontos escolhidos."""
    print(f"Baixando mapa real: {AREA_PADRAO['nome']}...")
    G_osmnx = baixar_grafo_real()
    grafo = converter_para_grafo(G_osmnx)
    pontos = pontos_padrao_com_nos(G_osmnx)

    print("\nMapa baixado com sucesso.")
    print(f"Nos no OSMnx: {G_osmnx.number_of_nodes()}")
    print(f"Arestas no OSMnx: {G_osmnx.number_of_edges()}")
    print(f"Nos no Grafo do projeto: {len(list(grafo.nos()))}")
    print(f"Arestas no Grafo do projeto: {sum(len(v) for v in grafo.adj.values())}")

    loja = pontos["loja"]
    print("\nLoja:")
    print(f"- {loja['nome']}: no {loja['no']} ({loja['lat']}, {loja['lon']})")

    print("\nClientes:")
    for cliente in pontos["clientes"]:
        print(
            f"- {cliente['nome']}: no {cliente['no']} "
            f"({cliente['lat']}, {cliente['lon']})"
        )


if __name__ == "__main__":
    executar_demo()
