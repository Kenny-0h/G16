from grafo import Grafo
import pandas as pd


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
                id_servico += 1
            elif lendo_arestas_req and linha.startswith("E"):
                grafo.adicionar_aresta_requerida(int(partes[1]), int(partes[2]), int(partes[3]), int(partes[4]), int(partes[5]), id_servico)
                id_servico += 1
            elif lendo_arcos_req and linha.startswith("A"):
                grafo.adicionar_arco_requerido(int(partes[1]), int(partes[2]), int(partes[3]), int(partes[4]), int(partes[5]), id_servico)
                id_servico += 1
            elif lendo_arestas_nreq and linha.startswith("NrE"):
                grafo.adicionar_aresta_nao_requerida(int(partes[1]), int(partes[2]), int(partes[3]))
            elif lendo_arcos_nreq and linha.startswith("NrA"):
                grafo.adicionar_arco_nao_requerido(int(partes[1]), int(partes[2]), int(partes[3]))
    return grafo
#-------------Leitura do Arquivo------------------------


#-------------Gerar csv---------------------------------
def exportar_estatisticas_para_csv(grafo, nome_arquivo):
    dados = {
        "Numero de veículo": grafo.veiculos,
        "Capacidade de veículo": grafo.capacidade_veiculos,
        "No deposito": grafo.no_deposito,
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
    #print(f"\nEstatísticas exportadas para '{nome_arquivo}' com sucesso.")


#-------------Gerar csv---------------------------------

#------------Exportar rotas------------------------------
def exportar_rotas(rotas, no_deposito, caminho_saida, tempo_fp, tempo_ms):
    with open(caminho_saida, "w") as arquivo_saida:
        print(f"{sum(r['custo_total'] for r in rotas)}", file=arquivo_saida)
        print(f"{len(rotas)}", file=arquivo_saida)
        print(f"{int(tempo_fp * 3.0 * 1e9)}", file=arquivo_saida)
        print(f"{int(tempo_ms * 3.0 * 1e9)}", file=arquivo_saida)

        for i, r in enumerate(rotas):
            linha = f" 0 1 {i+1} {r['demanda_total']} {r['custo_total']}  {len(r['servicos_atendidos'])}"
            if r["rota"][0] == no_deposito:
                linha += f" (D 0,{no_deposito},{no_deposito})"
            for s in r["servicos_atendidos"]:
                linha += f" (S {s['id_servico']},{s['de']},{s['para']})"
            if r["rota"][-1] == no_deposito:
                linha += f" (D 0,{no_deposito},{no_deposito})"
            print(linha, file=arquivo_saida)
#------------Exportar rotas------------------------------

