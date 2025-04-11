# Projeto_Grafos
Repositório destinado para as entregas das etapas do trabalho prático da disciplina de Grafos. A primeira etapa tem como objetivo ler, representar e analisar grafos com arestas e arcos que podem ser requeridos ou não, cada um com seus atributos de transporte, demanda e custo de serviço. O grafo é lido a partir de um arquivo `.dat` estruturado, e várias estatísticas são calculadas automaticamente.

## 📂 Estrutura do Projeto

- `Grafos.py` (arquivo principal): contém a implementação da classe `Grafo`, as funções de leitura de arquivo e geração de estatísticas.
- Arquivo `.dat`: contém os dados do grafo a ser lido.
- Saída no terminal e exportação das estatísticas para CSV.

## 📥 Entrada Esperada

O programa espera um arquivo `.dat` com seções identificadas pelas palavras-chave:

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

### 📊 Estatísticas calculadas:

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

### 💾 Exportação

Ao final do programa, é gerado um arquivo csv contendo uma tabela com as principais estatísticas calculadas (com excesão de intermediação) usando a função `exportar_estatisticas_para_csv(grafo, nome_arquivo)`.

## ▶️ Como Usar

1. Execute o script:

```bash
python Grafo.py
```bash

2. Pelo terminal, digite  nome do arquivo '.dat' quando solicitado

3. O programa irá:
  - Imprimir no terminal os daos dos nós, vértices e arestas (para fins de depuração)
  - Imprimir as estatísticas calculadas
  - Gerar um arquivo '.csv' contendo as estatísticas (exceto a intermediação)

## 🛠️ Bibliotecas Utilizadas
  - collections (para defaultdict e deque)

  - math

  - pandas (para exportar estatísticas em formato CSV)


## 📌 Observações
No programa, foi aplicado o algoritmo de Floyd-Warshall para a construção da matriz de distâncias.
