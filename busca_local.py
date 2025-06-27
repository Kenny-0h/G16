import time

def calcular_custo_rota_com_dist(grafo, dist, servicos):
    deposito = grafo.no_deposito
    rota = [deposito]
    posicao = deposito
    custo_total = 0
    demanda_total = 0

    for s in servicos:
        destino = s["de"]
        custo_total += dist[posicao][destino]
        custo_total += s["custo_servico"]
        demanda_total += s["demanda"]
        rota.append(destino)
        posicao = destino

    if posicao != deposito:
        custo_total += dist[posicao][deposito]
        rota.append(deposito)

    return {
        "rota": rota,
        "custo_total": custo_total,
        "demanda_total": demanda_total,
        "servicos_atendidos": servicos
    }

def busca_local(grafo, rotas, max_iteracoes=250):
    dist = grafo.floyd_warshall()
    tempo_melhor_solucao = None
    
    for iteracao in range(max_iteracoes):
        melhorou = False
        for i in range(len(rotas)):
            for j in range(len(rotas)):
                if i == j:
                    continue
                rota_i = rotas[i]
                rota_j = rotas[j]

                for idx, s in enumerate(rota_i["servicos_atendidos"]):
                    if rota_j["demanda_total"] + s["demanda"] <= grafo.capacidade_veiculos:
                    	# Remover s da rota_i
                        nova_servicos_i = rota_i["servicos_atendidos"][:idx] + rota_i["servicos_atendidos"][idx+1:]
                        nova_servicos_j = rota_j["servicos_atendidos"] + [s]

                        nova_rota_i = calcular_custo_rota_com_dist(grafo, dist, nova_servicos_i)
                        nova_rota_j = calcular_custo_rota_com_dist(grafo, dist, nova_servicos_j)

                        custo_antigo = rota_i["custo_total"] + rota_j["custo_total"]
                        custo_novo = nova_rota_i["custo_total"] + nova_rota_j["custo_total"]

                        if custo_novo < custo_antigo:
                            rotas[i] = nova_rota_i
                            rotas[j] = nova_rota_j
                            melhorou = True
                            tempo_melhor_solucao = time.perf_counter()
                            break
                if melhorou:
                    break
            if melhorou:
                break
    return rotas, tempo_melhor_solucao
