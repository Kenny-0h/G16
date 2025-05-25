#from grafo import Grafo

#-------------Leitura do Arquivo------------------
def ler_grafo_de_arquivo(caminho_arquivo):
    grafo = Grafo()
    lendo_nos = lendo_arestas_req = lendo_arcos_req = lendo_arestas_nreq = lendo_arcos_nreq = False
    cabecalhos = ["FROM", "TO", "T.", "DEMAND", "S.", "N."]

    id_servico =1 #zero é reservado para depósito

    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if linha == "":
                continue
            if linha.startswith("#Vehicles:"):
                grafo.veiculos = int(linha.split(":")[1].strip())
                continue
            elif linha.startswith("Depot Node"):
                grafo.no_deposito = int(linha.split(":")[1].strip())
                continue
            elif linha.startswith("Capacity"):
                grafo.capacidade_veiculos = int(linha.split(":")[1].strip())
                continue
            elif linha.startswith("ReN."):
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
                grafo.adicionar_no_requerido(int(partes[0][1:]), int(partes[1]), int(partes[2]), id_servico)
            elif lendo_arestas_req and linha.startswith("E"):
                grafo.adicionar_aresta_requerida(int(partes[1]), int(partes[2]), int(partes[3]), int(partes[4]), int(partes[5]), id_servico)
            elif lendo_arcos_req and linha.startswith("A"):
                grafo.adicionar_arco_requerido(int(partes[1]), int(partes[2]), int(partes[3]), int(partes[4]), int(partes[5]), id_servico)
            elif lendo_arestas_nreq and linha.startswith("NrE"):
                grafo.adicionar_aresta_nao_requerida(int(partes[1]), int(partes[2]), int(partes[3]))
            elif lendo_arcos_nreq and linha.startswith("NrA"):
                grafo.adicionar_arco_nao_requerido(int(partes[1]), int(partes[2]), int(partes[3]))
    return grafo
#-------------Leitura do Arquivo------------------------
