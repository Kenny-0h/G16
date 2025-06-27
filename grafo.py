from collections import defaultdict, deque
import math
import pandas as pd
 #------------Definição do grafo-------------
class Grafo:
    def __init__(self):
        self.veiculos = 0;
        self.capacidade_veiculos = 0;
        self.no_deposito = None;
        self.vertices = set()
        self.nos_requeridos = {}

        self.arestas_requeridas = []
        self.arcos_requeridos = []

        self.arestas_nao_requeridas = []
        self.arcos_nao_requeridos = []

    def adicionar_no_requerido(self, id_no, demanda, custo_servico, id_servico):
        self.nos_requeridos[id_no] = {
            "demanda": demanda,
            "custo_servico": custo_servico,
            "id_servico": id_servico
        }
        self.vertices.add(id_no)

    def adicionar_aresta_requerida(self, de, para, custo_transporte, demanda, custo_servico, id_servico):
        self.arestas_requeridas.append({
            "de": de,
            "para": para,
            "custo_transporte": custo_transporte,
            "demanda": demanda,
            "custo_servico": custo_servico,
            "id_servico": id_servico
        })
        self.vertices.update([de, para])

    def adicionar_arco_requerido(self, de, para, custo_transporte, demanda, custo_servico, id_servico):
        self.arcos_requeridos.append({
            "de": de,
            "para": para,
            "custo_transporte": custo_transporte,
            "demanda": demanda,
            "custo_servico": custo_servico,
            "id_servico": id_servico
        })
        self.vertices.update([de, para])

    def adicionar_aresta_nao_requerida(self, de, para, custo_transporte):
        self.arestas_nao_requeridas.append({
            "de": de,
            "para": para,
            "custo_transporte": custo_transporte
        })
        self.vertices.update([de, para])

    def adicionar_arco_nao_requerido(self, de, para, custo_transporte):
        self.arcos_nao_requeridos.append({
            "de": de,
            "para": para,
            "custo_transporte": custo_transporte
        })
        self.vertices.update([de, para])

#------------Definição do grafo---------------------



#-------------Calculos Estatísticos------------------
    def total_vertices(self):
        return len(self.vertices)

    def total_arestas(self):
        return len(self.arestas_requeridas) + len(self.arestas_nao_requeridas)

    def total_arcos(self):
        return len(self.arcos_requeridos) + len(self.arcos_nao_requeridos)

    def total_vertices_requeridos(self):
        return len(self.nos_requeridos)

    def total_arestas_requeridas(self):
        return len(self.arestas_requeridas)

    def total_arcos_requeridos(self):
        return len(self.arcos_requeridos)

    def densidade(self):
        n = self.total_vertices()
        e = self.total_arestas() + self.total_arcos()
        if n <= 1:
            return 0
        return e / (n * (n - 1))

    def construir_grafo_nao_direcionado(self):
        grafo = defaultdict(list)
        for a in self.arestas_requeridas + self.arestas_nao_requeridas:
            grafo[a["de"]].append(a["para"])
            grafo[a["para"]].append(a["de"])
        for a in self.arcos_requeridos + self.arcos_nao_requeridos:
            grafo[a["de"]].append(a["para"])
        return grafo

    def componentes_conectados(self):
        grafo = self.construir_grafo_nao_direcionado()
        visitados = set()
        componentes = 0

        for v in self.vertices:
            if v not in visitados:
                componentes += 1
                fila = deque([v])
                while fila:
                    atual = fila.popleft()
                    if atual in visitados:
                        continue
                    visitados.add(atual)
                    fila.extend(grafo[atual])
        return componentes

    def grau_dos_vertices(self):
        graus = defaultdict(int)
        for a in self.arestas_requeridas + self.arestas_nao_requeridas:
            graus[a["de"]] += 1
            graus[a["para"]] += 1
        for a in self.arcos_requeridos + self.arcos_nao_requeridos:
            graus[a["de"]] += 1
        return graus

    def grau_minimo(self):
        graus = self.grau_dos_vertices()
        return min(graus.values()) if graus else 0

    def grau_maximo(self):
        graus = self.grau_dos_vertices()
        return max(graus.values()) if graus else 0

    def matriz_adjacencia_pesos(self):
        n = max(self.vertices) + 1
        dist = [[math.inf] * n for _ in range(n)]
        for i in self.vertices:
            dist[i][i] = 0
        for a in self.arestas_requeridas + self.arestas_nao_requeridas:
            dist[a["de"]][a["para"]] = a["custo_transporte"]
            dist[a["para"]][a["de"]] = a["custo_transporte"]
        for a in self.arcos_requeridos + self.arcos_nao_requeridos:
            dist[a["de"]][a["para"]] = a["custo_transporte"]
        return dist

    def floyd_warshall(self):
        dist = self.matriz_adjacencia_pesos()
        n = len(dist)
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        return dist

    def caminho_medio(self):
        dist = self.floyd_warshall()
        total = 0
        cont = 0
        for i in self.vertices:
            for j in self.vertices:
                if i != j and dist[i][j] < math.inf:
                    total += dist[i][j]
                    cont += 1
        return total / cont if cont > 0 else 0

    def diametro(self):
        dist = self.floyd_warshall()
        maior = 0
        for i in self.vertices:
            for j in self.vertices:
                if i != j and dist[i][j] < math.inf:
                    maior = max(maior, dist[i][j])
        return maior

    def intermediacao(self):
        dist = self.floyd_warshall()
        intermed = defaultdict(float)
        for s in self.vertices:
            for t in self.vertices:
                if s == t:
                    continue
                caminho_min = dist[s][t]
                for v in self.vertices:
                    if v != s and v != t:
                        if dist[s][v] + dist[v][t] == caminho_min:
                            intermed[v] += 1
        return intermed
#-------------Calculos Estatísticos------------------

