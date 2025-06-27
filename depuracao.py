def verificar_demanda_rotas(grafo, rotas):
    erros_encontrados = False

    for i, rota in enumerate(rotas, start=1):
        demanda_calculada = 0

        for s in rota["servicos_atendidos"]:
            # Recupera a demanda original a partir dos dados do grafo
            demanda_original = None
            if s["tipo"] == "nó":
                no = s["de"]
                demanda_original = grafo.nos_requeridos.get(no, {}).get("demanda", None)
            elif s["tipo"] == "aresta":
                demanda_original = next((a["demanda"] for a in grafo.arestas_requeridas if a["id_servico"] == s["id_servico"]), None)
            elif s["tipo"] == "arco":
                demanda_original = next((a["demanda"] for a in grafo.arcos_requeridos if a["id_servico"] == s["id_servico"]), None)

            if demanda_original is None:
                print(f"[!] Serviço {s['id_servico']} não encontrado no grafo.")
                continue

            demanda_calculada += demanda_original

        demanda_armazenada = rota["demanda_total"]
        print(f"Rota {i}: demanda armazenada = {demanda_armazenada}, demanda real = {demanda_calculada}")

        if demanda_calculada != demanda_armazenada:
            erros_encontrados = True
            print(f"  [ERRO] Diferença detectada na rota {i}.")

    if not erros_encontrados:
        print("\nNenhum erro de demanda detectado nas rotas.")
    else:
        print("\n[!] Foram encontrados erros nas demandas das rotas.")

