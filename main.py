from collections import defaultdict, deque
import math
import pandas as pd


 #------------Definição do grafo-------------
class Grafo:
    def __init__(self):
        self.vertices = set()
        self.nos_requeridos = {}

        self.arestas_requeridas = []
        self.arcos_requeridos = []

        self.arestas_nao_requeridas = []
        self.arcos_nao_requeridos = []
        
    def adicionar_no_requerido(self, id_no, demanda, custo_servico):
        self.nos_requeridos[id_no] = {
            "demanda": demanda,
            "custo_servico": custo_servico
        }
        self.vertices.add(id_no)

    def adicionar_aresta_requerida(self, de, para, custo_transporte, demanda, custo_servico):
        self.arestas_requeridas.append({
            "de": de,
            "para": para,
            "custo_transporte": custo_transporte,
            "demanda": demanda,
            "custo_servico": custo_servico
        })
        self.vertices.update([de, para])

    def adicionar_arco_requerido(self, de, para, custo_transporte, demanda, custo_servico):
        self.arcos_requeridos.append({
            "de": de,
            "para": para,
            "custo_transporte": custo_transporte,
            "demanda": demanda,
            "custo_servico": custo_servico
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



#-------------Leitura do Arquivo------------------
def ler_grafo_de_arquivo(caminho_arquivo):
    grafo = Grafo()
    lendo_nos = lendo_arestas_req = lendo_arcos_req = lendo_arestas_nreq = lendo_arcos_nreq = False
    cabecalhos = ["FROM", "TO", "T.", "DEMAND", "S.", "N."]

    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if linha == "":
                continue
            if linha.startswith("ReN."):
                lendo_nos = True
                lendo_arestas_req = lendo_arcos_req = lendo_arestas_nreq = lendo_arcos_nreq = False
                continue
            elif linha.startswith("ReE."):
                lendo_arestas_req = True
                lendo_nos = lendo_arcos_req = lendo_arestas_nreq = lendo_arcos_nreq = False
                continue
            elif linha.startswith("ReA."):
                lendo_arcos_req = True
                lendo_nos = lendo_arestas_req = lendo_arestas_nreq = lendo_arcos_nreq = False
                continue
            elif linha.startswith("EDGE"):
                lendo_arestas_nreq = True
                lendo_nos = lendo_arestas_req = lendo_arcos_req = lendo_arcos_nreq = False
                continue
            elif linha.startswith("ARC"):
                lendo_arcos_nreq = True
                lendo_nos = lendo_arestas_req = lendo_arcos_req = lendo_arestas_nreq = False
                continue

            if any(p in linha.upper() for p in cabecalhos):
                continue

            partes = linha.split()
            if lendo_nos and linha.startswith("N"):
                grafo.adicionar_no_requerido(int(partes[0][1:]), int(partes[1]), int(partes[2]))
            elif lendo_arestas_req and linha.startswith("E"):
                grafo.adicionar_aresta_requerida(int(partes[1]), int(partes[2]), int(partes[3]), int(partes[4]), int(partes[5]))
            elif lendo_arcos_req and linha.startswith("A"):
                grafo.adicionar_arco_requerido(int(partes[1]), int(partes[2]), int(partes[3]), int(partes[4]), int(partes[5]))
            elif lendo_arestas_nreq and linha.startswith("NrE"):
                grafo.adicionar_aresta_nao_requerida(int(partes[1]), int(partes[2]), int(partes[3]))
            elif lendo_arcos_nreq and linha.startswith("NrA"):
                grafo.adicionar_arco_nao_requerido(int(partes[1]), int(partes[2]), int(partes[3]))
    return grafo
#-------------Leitura do Arquivo------------------------




#-------------Gerar csv---------------------------------
def exportar_estatisticas_para_csv(grafo, nome_arquivo):
    dados = {
        "Total de vértices": grafo.total_vertices(),
        "Total de arestas": grafo.total_arestas(),
        "Total de arcos": grafo.total_arcos(),
        "Total de vértices requeridos": grafo.total_vertices_requeridos(),
        "Total de arestas requeridas": grafo.total_arestas_requeridas(),
        "Total de arcos requeridos": grafo.total_arcos_requeridos(),
        "Densidade": grafo.densidade(),
        "Componentes conectados": grafo.componentes_conectados(),
        "Grau mínimo": grafo.grau_minimo(),
        "Grau máximo": grafo.grau_maximo(),
        "Caminho médio": grafo.caminho_medio(),
        "Diâmetro": grafo.diametro()
    }

    df = pd.DataFrame(dados.items(), columns=["Estatística", "Valor"])
    df.to_csv(nome_arquivo, index=False)
    print(f"\nEstatísticas exportadas para '{nome_arquivo}' com sucesso.")
