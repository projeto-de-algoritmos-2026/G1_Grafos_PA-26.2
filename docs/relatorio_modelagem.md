# Relatório: modelagem e complexidade

## 1. Descrição do problema

O projeto simula um sistema de roteamento de entregas. A loja é a origem das
rotas e os clientes são os destinos. O objetivo é calcular o menor caminho da
loja até cada cliente, considerando que cada rua tem um custo associado.

Esse custo representa distância. Por isso, o bairro é modelado como um grafo
ponderado: os pontos importantes do bairro são nós, e as ruas são arestas com
pesos não-negativos.

## 2. Modelagem do grafo fictício

No mapa fictício, os nós representam:

- a loja;
- clientes;
- cruzamentos;
- becos e ruas alternativas.

As arestas representam ruas entre esses pontos. Cada aresta possui um peso
numérico que indica a distância entre os dois nós. O arquivo
`src/dados_ficticios.py` define manualmente:

- as coordenadas usadas para desenhar o mapa;
- a lista de ruas;
- a função `montar_grafo_bairro()`, que carrega esses dados na classe `Grafo`.

As ruas são cadastradas como direcionadas. Quando uma rua é de mão dupla, ela
aparece como duas arestas: uma de `u` para `v` e outra de `v` para `u`. Isso
mantém a representação simples e compatível com ruas de mão única.

O mapa fictício foi construído com mais caminhos do que o mínimo necessário:
existem atalhos, rotas alternativas, becos sem saída e ruas que não entram no
menor caminho. Isso ajuda a demonstrar que o algoritmo realmente compara os
custos das rotas em vez de apenas seguir um caminho óbvio.

## 3. Modelagem do grafo real

No mapa real, os dados vêm do OpenStreetMap usando a biblioteca OSMnx. O arquivo
`src/dados_reais.py` baixa uma área da Asa Norte, em Brasília:

- CLN/SQN 203-206, Asa Norte, Brasília.

O grafo baixado pelo OSMnx é convertido para a classe `Grafo` do projeto pela
função `converter_para_grafo()`. Nessa conversão:

- cada nó real do OpenStreetMap vira um nó do `Grafo`;
- cada rua vira uma aresta direcionada;
- o peso da aresta é a distância real em metros, obtida do atributo `length`;
- quando existem arestas paralelas entre os mesmos nós, fica a menor distância.

A loja e os clientes reais são definidos por latitude e longitude. A função
`escolher_no_mais_proximo()` associa cada coordenada ao nó mais próximo do grafo
real, permitindo usar o mesmo Dijkstra implementado para o mapa fictício.

## 4. Por que Dijkstra

O algoritmo de Dijkstra foi escolhido porque o problema tem duas propriedades
centrais:

- todos os pesos são não-negativos;
- a origem é única: a loja.

Esse é exatamente o caso de uso de Dijkstra para o problema de caminhos mínimos
de fonte única, ou *single-source shortest path*. Rodando o algoritmo uma vez a
partir da loja, obtemos a menor distância até todos os outros nós do grafo. Em
seguida, usando o vetor de predecessores, é possível reconstruir o caminho da
loja até qualquer cliente.

## 5. Complexidade

A implementação em `src/dijkstra.py` usa uma fila de prioridade com `heapq`.
Para um grafo com:

- `n` nós;
- `m` arestas;

a complexidade é:

```text
O((n + m) log n)
```

O termo `log n` vem das operações de inserção e remoção na heap binária. Cada nó
e cada aresta pode influenciar a fila durante o relaxamento das distâncias.

No mapa fictício, `n` e `m` são pequenos e definidos manualmente. No mapa real,
`n` e `m` dependem da quantidade de ruas e cruzamentos baixados do
OpenStreetMap. Apesar disso, o algoritmo usado é o mesmo nos dois casos.

## 6. Comparação entre os mapas

Os dois mapas usam a mesma estrutura de grafo e o mesmo algoritmo. A diferença
está na origem dos dados:

| Aspecto | Mapa fictício | Mapa real |
|---|---|---|
| Fonte dos dados | Definida manualmente no projeto | OpenStreetMap via OSMnx |
| Nós | Loja, clientes, cruzamentos e becos criados pela dupla | Interseções e pontos reais do mapa |
| Arestas | Ruas criadas manualmente | Ruas reais baixadas do OSM |
| Pesos | Distâncias simuladas | Distâncias reais em metros |
| Visualização | NetworkX + Matplotlib | OSMnx + Matplotlib |

No mapa fictício, a vantagem é o controle total: é possível criar casos com
atalhos, becos e ruas de mão única para validar o comportamento esperado. No
mapa real, a vantagem é aproximar o problema de uma situação prática, usando
distâncias e ruas reais.

## 7. Visualizações

O commit 7 gera uma imagem para cada cliente no mapa fictício. As imagens já
geradas ficam na pasta `imagens/`, por exemplo:

- `imagens/rota_ficticia_cliente_A.png`;
- `imagens/rota_ficticia_cliente_B.png`;
- `imagens/rota_ficticia_cliente_C.png`;
- `imagens/rota_ficticia_cliente_D.png`;
- `imagens/rota_ficticia_cliente_E.png`;
- `imagens/rota_ficticia_cliente_F.png`.

O commit 8 adiciona a visualização real. Ao executar:

```bash
python src/main.py real
```

o programa baixa o mapa real, calcula a rota da loja até cada cliente real
e salva uma imagem por cliente:

```text
relatorio/rota_real.png
relatorio/rota_real_1_cliente_1_sqn_204.png
relatorio/rota_real_2_cliente_2_sqn_205.png
...
```

Além das imagens, as distâncias reais são impressas no terminal em metros.

## 8. Testes

Os testes do commit 6 validam os principais comportamentos do Dijkstra:

- caminho direto;
- escolha de um atalho mais curto;
- nó desconectado;
- distâncias esperadas para os clientes do mapa fictício.

Também existem testes para a integração com dados reais sem depender de
internet, usando um grafo OSMnx falso. Esses testes verificam:

- preservação da direção das ruas;
- escolha da menor aresta quando há arestas paralelas;
- chamada correta da função de nó mais próximo usando longitude e latitude;
- fallback para cálculo local do nó mais próximo quando dependências opcionais
do OSMnx não estão disponíveis.

O teste real de download do OpenStreetMap fica separado porque depende de
internet. Ele pode ser executado com:

```powershell
$env:RUN_OSMNX_REAL = "1"
pytest tests/test_dados_reais_download.py -v
```

## 9. Conclusão

O projeto usa uma única solução algorítmica para dois cenários diferentes. No
mapa fictício, os dados são controlados pela dupla e ajudam a testar o algoritmo
em casos conhecidos. No mapa real, os dados vêm do OpenStreetMap e demonstram
que a mesma modelagem também funciona com ruas e distâncias reais.

Como as distâncias são não-negativas e a origem é única, Dijkstra com heap
binário resolve o problema de forma adequada, com complexidade
`O((n + m) log n)`.
