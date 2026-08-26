# Plano de Commits 

Entrega: 07/09


## Commit 1 — `chore: setup + estrutura do grafo` (26/08, qua)
- Criar repositório no GitHub
- Criar `.gitignore`
- Criar estrutura de pastas do projeto
- Criar `requirements.txt`
- Escrever primeira versão do README
- Implementar a classe `Grafo` (estrutura de dados básica)

**Saída esperada:** repositório criado, `pip install -r requirements.txt` roda sem erro, teste manual confirma que adicionar nó/aresta funciona.


## Commit 2 — `feat: baixar e converter mapa real (osmnx)` (27/08, qui)
- Implementar função pra baixar o grafo de um bairro real via `osmnx`
- Implementar função pra converter esse grafo pra classe `Grafo` de vocês
- Implementar função pra achar o nó mais próximo de uma coordenada (lat/lon)
- Escolher a área real (2-3 quarteirões) e as coordenadas de loja/clientes

**Saída esperada:** download do grafo real funciona sem travar; conversão devolve um `Grafo` válido. (Se der problema, sobram 10 dias pra resolver ou seguir só com o fictício.)


## Commit 3 — `feat: dados do bairro fictício` (28/08, sex)
- Desenhar o mapa fictício no papel (loja, clientes, cruzamentos, distâncias)
- Criar as coordenadas de cada ponto (pra desenhar depois)
- Criar a lista de ruas com pesos
- Implementar função que monta o `Grafo` a partir desses dados

**Saída esperada:** função devolve um `Grafo` com todos os nós e ruas carregados; distâncias mínimas calculadas manualmente no papel, pra comparar depois.


## Commit 4 — `feat: implementação do Dijkstra` (29/08, sáb)
- Implementar o algoritmo de Dijkstra usando fila de prioridade

**Saída esperada:** rodar o algoritmo no grafo fictício bate com o cálculo manual feito no commit 3.


## Commit 5 — `feat: reconstrução do caminho` (30/08, dom)
- Adicionar rastreamento de predecessores dentro do Dijkstra
- Implementar função que reconstrói o caminho completo da origem até um destino

**Saída esperada:** função devolve o caminho correto passo a passo; caso sem caminho possível devolve resultado nulo.


## Commit 6 — `test: casos de teste do Dijkstra` (31/08, seg)
- Escrever testes automatizados com casos conhecidos (caminho direto, caminho com atalho, nó desconectado)

**Saída esperada:** todos os testes passam ao rodar o framework de testes.


## Commit 7 — `feat: visualização do mapa fictício` (01/09, ter)
- Implementar função de desenho do grafo fictício
- Destacar visualmente a loja e a rota até cada cliente
- Gerar uma imagem por cliente

**Saída esperada:** rodar o programa gera as imagens das rotas corretamente. Nesse ponto o projeto já está completo e entregável, mesmo se o mapa real falhar depois.


## Commit 8 — `feat: visualização do mapa real` (02/09, qua)
- Integrar as funções do commit 2 com o Dijkstra
- Calcular e desenhar a rota real da loja até um cliente no bairro real

**Saída esperada:** imagem da rota real gerada, com a distância real (em metros) impressa.


## Commit 9 — `docs: relatório - modelagem e complexidade` (03/09, qui)
- Escrever a modelagem do grafo (fictício e real)
- Justificar a escolha do Dijkstra
- Explicar a complexidade do algoritmo
- Comparar os dois mapas e incluir as imagens geradas

**Saída esperada:** relatório completo, pronto pra entrega.


## Commit 10 — `docs: vídeo de apresentação` (04/09, sex)
- Roteirizar o vídeo (problema, modelagem, demonstração ao vivo, complexidade)
- Gravar a tela mostrando o programa rodando de verdade
- Subir o vídeo e linkar no README

**Saída esperada:** vídeo gravado, link funcional, referenciado no README/relatório.


## Commit 11 — `fix: ajustes finais e polimento` (05/09, sáb)
- Rodar tudo do zero num ambiente limpo
- Corrigir erros encontrados
- Revisar README e remover código morto

**Saída esperada:** projeto roda do zero, sem passo manual escondido.


## Commit 12 — `docs: entrega final` (06/09, dom)
- Conferir link do repositório público
- Conferir link do vídeo
- Submeter tudo na planilha compartilhada

**Saída esperada:** repositório, vídeo e histórico de commits todos acessíveis e funcionando.