# Projeto_Grafos
Repositório destinado para as entregas das etapas do trabalho prático da disciplina de Grafos. 
 
  A primeira etapa tem como objetivo ler, representar e analisar grafos com arestas e arcos que podem ser requeridos ou não, cada um com seus atributos de transporte, demanda e custo de serviço. O grafo é lido a partir de um arquivo `.dat` estruturado, e várias estatísticas são calculadas automaticamente.
  
  A segunda tem como objetivo encontrar uma aprximação incial de um conjunto de rotas factíveis que solucionam o problema do caixeiro viajante no grafo misto dado em tempo mínimo. Nesta etapa, a qualidade da resposta é desfavorefida em função á um melor gasto temporal.

  A terceira etapa tem como objetivo aplicar melhorias na solução adquirida na etapa anterior,bem como corrigir os erros cometidos. A melhora aplicada foi uma Busca Local baseada em trocas de serviçoes entre rotas de um mesmo grafo.

## 📂 Estrutura do Projeto
### Etapa 1
- `main.py` (arquivo principal): contém a implementação da classe `Grafo`, as funções de leitura de arquivo e geração de estatísticas.
- `visualização.ipynb`: contém a implementação relacionada à visualização dos dados.
- Arquivos `.dat`: contém os dados do grafo a ser lido.
- Saída no terminal e exportação das estatísticas para CSV.


### Etapa 2
- Nesta etpa, todo o projeto foi unificado em único [notebook](https://colab.research.google.com/drive/1fmRf6RJuSCepaBqJSvrDy9Gjikoc1NRb?usp=drive_link) do Google Colab (também salvo como Grafos_projeto.ipynb do diretório) que é dividido da seguinte forma.:
- grafo.py: contem a implementação da classe `grafo`, os cálculos estatísticos relacionados ao grafo, bem como o cálculo das rotas
- lerarquivo.py: contém todo o trecho de código responsável pela leitura dos arquivos `.dat` de entrada
- visualização.ipynb: coném a implementação relacionada á vizualização das estatísticas do grafo (comentadas) e a geração do arquivo `sol-` de cada instância (saída única)


### Etapa 3
- Nesta etapa, o projeto ainda se mantém unificado no [notebook](https://) do Google Colab (Ainda salvo no diretório principal do Projeto), e segue divido da seguinte forma:
- grafo.py : contem a implementação da classe `grafo`, os cálculos estatísticos relacionados ao grafo;
- lerarquivo.py: contém todo o trecho de código responsável pela leitura dos arquivos `.dat` de entrada;
- gerarRotas.py: contém a heurística de cálculo inicial das rotas da etapa anterior;
- buscaLocal.py: contém a função relacionada a búsca local `busca_local` bem como sua auxiliar `calcular_custo_rota`;
- - visualização.ipynb: coném toda a integração das demais partes do programa, bem como toda a perte responsável pela gravação dos arquivos das soluções;
**OBS:** Caso não seja possível abrir o notebook pelo colab, o projeto também está disposto como arquivos separados no diretório
## 📥 Entrada Esperada
Com as modificações aplicadas na Etapa 3, o programa espera um conjunto de arquivos `.dat` alocados em um mesmo diretório, com seções identificadas pelas palavras-chave:

- `ReN.` – Início da seção de nós requeridos.
- `ReE.` – Início da seção de arestas requeridas.
- `ReA.` – Início da seção de arcos requeridos.
- `EDGE` – Início da seção de arestas **não** requeridas.
- `ARC` – Início da seção de arcos **não** requeridos.

Cada seção deve conter linhas com os dados de acordo com o seguinte formato:

- Nó requerido: `N{id} {demanda} {custo_servico}`
- Aresta requerida: `E {de} {para} {custo_transporte} {demanda} {custo_servico}`
- Arco requerido: `A {de} {para} {custo_transporte} {demanda} {custo_servico}`
- Aresta não requerida: `NrE {de} {para} {custo_transporte}`
- Arco não requerido: `NrA {de} {para} {custo_transporte}`

## ⚙️ Funcionalidades
### 📊 Estatísticas calculadas(comentadas na parte 2):

- Total de vértices
- Total de arestas (requeridas e não requeridas)
- Total de arcos (requeridos e não requeridos)
- Total de nós requeridos
- Densidade do grafo
- Número de componentes conectados
- Grau mínimo e máximo
- Caminho médio (usando Floyd-Warshall)
- Diâmetro do grafo
- Intermediação de vértices

### 🚚 Rotas (Melhoras pela Etapa 3)
- Custo total das rotas para atender todos os serviços requeridos
- Número de rotas necessárias
- Clock total do programa (tempoTotal *3.0 * 1e9)
- Clock de melhor solução (tempoDeSolucao *3.0 * 1e9)
- Descrição dos servições requeridos percorridos em cada rota
  
### 💾 Exportação
**Etapa 1:**
Ao final do programa, é gerado um arquivo csv contendo uma tabela com as principais estatísticas calculadas (com excesão de intermediação) usando a função `exportar_estatisticas_para_csv(grafo, nome_arquivo)`.

**Etapa 2**
Ao final do programa, é gerado um arquivo de formatação `sol-`+nome_instancia+`.dat`

**Etapa 3**
Ao final do programa, são gerados duas pastas no diretório drive/MyDrive/ProjetoGrafos no Drive, no qual uma das pastas possui os arquivos relacionados as estatísticas e na outra, os arquivos relacionados às soluções encontradas; 
## ▶️ Como Usar
1. Acesse o google colab pelo link do [notebook](https://)  (ou então abra manualmente o arquivo unificado do projeto no colab) e execute todas as partes do programa ou então execute o script:
```bash
python visualização.ipynb
```
2. Pelo terminal gerado pela cédula `visualização`, digite todo o caminho do diretório em que os arquivos `.dat` estão quando solicitado

3. O programa irá:

**Etapa 1**
  - Imprimir no terminal os dados dos nós, vértices e arestas (para fins de depuração)
  - Imprimir as estatísticas calculadas
  - Gerar um arquivo '.csv' contendo as estatísticas (exceto a intermediação)

**Etapa 2**
  - Gerar um arquivo `sol-`+nome_instancia+`.dat` contendo a seguinte formatção:
    `custo total da solução`
    `total de rotas`
    `total de clocks para a execução do algoritmo`
    `total de clocks para encontrar a solução`
        `indice_do_deposito(sempre zero)` `dia_Daroteirização(sempre 1)` `identificador_da_rota` `demanda_total_da_rota` `custo_total_da_rotal toral_de_visitas``(x i,j,k)`
para x= D caso o serviço seja o depósito, S caso seja outro serviço
     i= índice do servço. 0 para todo depósito
     j= primeira extremidade do serviço
     k= seguda extremidade do serviço

**Etapa 3**
 - Gerar duas pastas no dirtório indicado no Drive: G16-Estaísticas e G16-Sol
 - Inserir todos os arquivos relacionados às estatísticas dos grafos em G16-Estatísticas
 - Inserir todos os arquivos relacionados às soluções encontradas em G16-Sol


## 📚 Bibliotecas Utilizadas
  - collections (para defaultdict e deque)
  - math
  - pandas (para exportar estatísticas em formato CSV)
  - os (para manipular diretórios)

## 📌 Bibliografia e Referências
https://www.programiz.com/dsa/floyd-warshall-algorithm
https://www.w3schools.com/python/pandas/pandas_dataframes.asp
https://www.tutorialspoint.com/python_data_structure/python_graphs.htm
https://docs.python.org/3/library/collections.html#collections.deque
https://docs.python.org/3/library/collections.html#collections.defaultdict

STÜTZLE, Thomas et al. ACO algorithms for the traveling salesman problem. Evolutionary algorithms in engineering and computer science, v. 4, p. 163-183, 1999.

CHATTERJEE, Sangit; CARRERA, Cecilia; LYNCH, Lucy A. Genetic algorithms and traveling salesman problems. European journal of operational research, v. 93, n. 3, p. 490-510, 1996.
