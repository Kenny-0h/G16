import math

def construir_rotas(grafo):
    distancias = grafo.floyd_warshall()
    servicos_pendentes = []

    # Generaliza todos os serviços requeridos (nós, arestas, arcos)
    for no, dados in grafo.nos_requeridos.items():
        servicos_pendentes.append({
            "tipo": "nó",
            "de": no,
            "para": no,
            "demanda": dados["demanda"],
            "custo_servico": dados["custo_servico"],
            "id_servico": dados["id_servico"]
        })

    for a in grafo.arestas_requeridas:
        servicos_pendentes.append({
            "tipo": "aresta",
            "de": a["de"],
            "para": a["para"],
            "demanda": a["demanda"],
            "custo_servico": a["custo_servico"],
            "id_servico": a["id_servico"]
        })

    for a in grafo.arcos_requeridos:
        servicos_pendentes.append({
            "tipo": "arco",
            "de": a["de"],
            "para": a["para"],
            "demanda": a["demanda"],
            "custo_servico": a["custo_servico"],
            "id_servico": a["id_servico"]
        })

    demanda_total_esperada = sum(s["demanda"] for s in servicos_pendentes)
     # Depuração
    #print(f"\nDemanda total esperada: {demanda_total_esperada}\n")

    rotas = []
    rota_numero = 1

    while servicos_pendentes:
        carga_atual = 0
        custo_total = 0
        rota = [grafo.no_deposito]
        posicao_atual = grafo.no_deposito
        servicos_da_rota = []
        servicos_restantes = []

        # Depuração
        #print(f"Demanda da rota {rota_numero}:")

        for s in servicos_pendentes:
            if s["tipo"] == "nó":
                destinos = [s["de"]]
            else:
                destinos = [s["de"], s["para"]]

            custo_transporte = 0
            pos = posicao_atual
            caminho_valido = True

            for d in destinos:
                if distancias[pos][d] == math.inf:
                    caminho_valido = False
                    break
                custo_transporte += distancias[pos][d]
                pos = d

            if not caminho_valido:
                servicos_restantes.append(s)
                continue

            if carga_atual + s["demanda"] > grafo.capacidade_veiculos:
                servicos_restantes.append(s)
                continue

            # Depuração
            #print(f"  Serviço {s['id_servico']} ({s['tipo']}) de {s['de']} para {s['para']} - Demanda: {s['demanda']}")

            carga_atual += s["demanda"]
            custo_total += custo_transporte + s["custo_servico"]

            for d in destinos:
                if rota[-1] != d:
                    rota.append(d)

            posicao_atual = destinos[-1]
            servicos_da_rota.append(s)

        servicos_pendentes = servicos_restantes

        if len(rota) > 1:
            custo_volta = distancias[posicao_atual][grafo.no_deposito]
            if custo_volta < math.inf:
                custo_total += custo_volta
                rota.append(grafo.no_deposito)
            else:
                print(f"  [!] Não foi possível retornar do nó {posicao_atual} para o depósito {grafo.no_deposito}")

            rotas.append({
                "rota": rota,
                "custo_total": custo_total,
                "demanda_total": carga_atual,
                "servicos_atendidos": servicos_da_rota
            })
            #print(f"  Total da rota {rota_numero}: {carga_atual}\n")
        else:
            print(f"  [!] Rota {rota_numero} não teve serviços atendidos\n")

        rota_numero += 1

    demanda_total_calculada = sum(r["demanda_total"] for r in rotas)
    #print(f"Demanda total nas rotas: {demanda_total_calculada}\n")

    return rotas

