# Rota de Entregas

Projeto da disciplina de Projeto e Análise de Açgoritmos (UnB). Simulação de um sistema de roteamento de entregas usando o algoritmo de Dijkstra.

## Dupla

| Nome | Matrícula |
|---|---|
| Maria Clara Oleari de Araujo | 221008338 |
| Ana Júlia Mendes Santos | 221007798 |


## Descrição do problema

O projeto simula um sistema de roteamento de entregas: existe uma **loja** (centro de distribuição) e vários **clientes** espalhados por um bairro. O bairro é modelado como um grafo, cruzamentos e pontos de entrega são nós, e as ruas são arestas com peso (distância). O algoritmo de **Dijkstra** calcula o caminho mais curto da loja até cada cliente.

São usados dois cenários:
- Um **mapa fictício**, desenhado à mão, com coordenadas e distâncias definidas pela dupla.
- Um **mapa real** (bônus), extraído do OpenStreetMap via `osmnx`, com ruas e distâncias reais de um bairro de Brasília.

### Por que Dijkstra é o algoritmo certo aqui

- Todos os pesos (distâncias) são não-negativos.
- É um problema de **single-source shortest path**: uma origem (a loja) e múltiplos destinos (os clientes).

### Complexidade



## Estrutura do repositório

```

```

## Como instalar

```bash
cd G1_Grafos_PA-26.2
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Como rodar

```bash

```

## Como rodar os testes

```bash
pytest tests/ -v
```

## Mapa real com OSMnx

O modulo `src/dados_reais.py` baixa uma area pequena real da Asa Norte, em
Brasilia, converte o grafo do OpenStreetMap para a classe `Grafo` do projeto e
encontra os nos mais proximos da loja/clientes escolhidos.

Area escolhida: CLN/SQN 204-205, Asa Norte, Brasilia.

- Loja - CLN 204: `lat=-15.76598`, `lon=-47.88518`
- Cliente 1 - SQN 204: `lat=-15.76495`, `lon=-47.88653`
- Cliente 2 - SQN 205: `lat=-15.76522`, `lon=-47.88376`
- Cliente 3 - CLN 205: `lat=-15.76632`, `lon=-47.88418`

Testes rapidos, sem internet:

```bash
pytest tests/test_dados_reais.py -v
```

Teste real, usando internet/OpenStreetMap:

```bash
$env:RUN_OSMNX_REAL = "1"
pytest tests/test_dados_reais_download.py -v
```

## Cronograma

O plano de commits detalhado está em [docs/cronograma_v1.md](docs/cronograma_v1.md).

## Relatório e vídeo de apresentação

- Relatório: *(link a adicionar)*
- Vídeo de apresentação: *(link a adicionar)*
