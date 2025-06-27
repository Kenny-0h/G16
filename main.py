import os
import time

from manipularArquivo import ler_grafo_de_arquivo, exportar_estatisticas_para_csv, exportar_rotas
from rotas import construir_rotas
from busca_local import busca_local
from depuracao import verificar_demanda_rotas

# Identificação dos diretórios
diretorio_entrada = input("Digite o caminho do diretório com os arquivos .dat: ").strip()
diretorio_saida_rotas = "Saidas/G16-Sol"
diretorio_saida_estatisticas = "Saidas/G16-estatisticas"

os.makedirs(diretorio_saida_rotas, exist_ok=True)
os.makedirs(diretorio_saida_estatisticas, exist_ok=True)

# Processamento dos arquivos
for nome_arquivo in os.listdir(diretorio_entrada):
    if nome_arquivo.endswith(".dat"):
        caminho_entrada = os.path.join(diretorio_entrada, nome_arquivo)
        nome_sem_extensao = os.path.splitext(nome_arquivo)[0]
        caminho_saida_rotas = os.path.join(diretorio_saida_rotas, f"sol-{nome_sem_extensao}.dat")
        caminho_saida_estatisticas = os.path.join(diretorio_saida_estatisticas, f"{nome_sem_extensao}.csv")

        print(f"\n------------------------ Processando: {nome_arquivo} -------------------------")
        inicio = time.perf_counter()  # início da contagem de clock por arquivo

        grafo = ler_grafo_de_arquivo(caminho_entrada)

        # Exportar estatísticas
        exportar_estatisticas_para_csv(grafo, caminho_saida_estatisticas)

        # Construir rotas
        rotas = construir_rotas(grafo)
        tempo_solucao_inicial = time.perf_counter()

        # Depuração do erro de demandas
        # verificar_demanda_rotas(grafo, rotas)

        # Melhorar valores das rotas
        rotas, tempo_melhor_solucao = busca_local(grafo, rotas)

        # Fim das contagens de clock
        if tempo_melhor_solucao is None:
            tempoMS = tempo_solucao_inicial - inicio
        else:
            tempoMS = tempo_melhor_solucao - inicio

        tempoFP = time.perf_counter() - inicio  # tempo final do programa

        exportar_rotas(rotas, grafo.no_deposito, caminho_saida_rotas, tempoFP, tempoMS)

        #print(f"-> Arquivo de rotas salvo em: '{caminho_saida_rotas}'")
        #print(f"-> Estatísticas exportadas para: '{caminho_saida_estatisticas}'")

