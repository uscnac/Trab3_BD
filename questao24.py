import matplotlib.pyplot as plt
import numpy as np

# Ler os dados do arquivo
def ler_dados_simulacao(nome_arquivo):
    with open(nome_arquivo, 'r') as file:
        linhas = file.readlines()

    dados = {
        "unica_rc": [],
        "unica_s": [],
        "separada_rc": [],
        "separada_s": []
    }

    for i, linha in enumerate(linhas):
        if 'Tempo total' in linha:
            tempo = float(linha.split(': ')[1].split(' segundos')[0])
            if 'Estratégia: unica' in linhas[i - 1]:
                if 'READ COMMITTED' in linhas[i - 1]:
                    dados["unica_rc"].append(tempo)
                elif 'SERIALIZABLE' in linhas[i - 1]:
                    dados["unica_s"].append(tempo)
            elif 'Estratégia: separada' in linhas[i - 1]:
                if 'READ COMMITTED' in linhas[i - 1]:
                    dados["separada_rc"].append(tempo)
                elif 'SERIALIZABLE' in linhas[i - 1]:
                    dados["separada_s"].append(tempo)

    return dados

# Função para gerar gráficos de linha
def gerar_graficos_por_linha(dados, threads):
    nomes_arquivos = {
        "unica_rc": "grafico_a_rc.png",
        "unica_s": "grafico_a_s.png",
        "separada_rc": "grafico_b_rc.png",
        "separada_s": "grafico_b_s.png"
    }

    titulos = {
        "unica_rc": "Tempo (Versão a - READ COMMITTED)",
        "unica_s": "Tempo reservas (Versão a - SERIALIZABLE)",
        "separada_rc": "Tempo reservas (Versão b - READ COMMITTED)",
        "separada_s": "Tempo (Versão b - SERIALIZABLE)"
    }

    for categoria, valores in dados.items():
        plt.figure(figsize=(8, 6))
        plt.plot(threads, valores, marker='o', label=titulos[categoria])
        plt.xlabel("Número de Agentes (k)")
        plt.ylabel("Tempo necessário (segundos)")
        plt.title(titulos[categoria])
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Salvar o gráfico
        plt.savefig(nomes_arquivos[categoria])
        print(f"Gráfico salvo como {nomes_arquivos[categoria]}")
        plt.clf()

# Nome do arquivo
nome_arquivo = 'saida_simulacao.txt'

# Número de threads (k)
threads = [1, 2, 4, 6, 8, 10]

# Ler os dados e gerar os gráficos por linha
dados_simulacao = ler_dados_simulacao(nome_arquivo)
gerar_graficos_por_linha(dados_simulacao, threads)