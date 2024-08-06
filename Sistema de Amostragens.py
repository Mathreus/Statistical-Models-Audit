import pandas as pd
import numpy as np


# Carregar os dados a partir de uma arquivo .csv
def carregar_dados(filepath):
    return pd.read_csv(filepath)


# Amostragem Aleatória Simples: Cada elemento de uma população tem a mesma probabilidade de ser escolhido.
def amostragem_aleatoria_simples(data, sample_size):
    return data.sample(n=sample_size, random_state=1)


# Amostragem Sistemática: Os elementos da população são selecionados a intervalos regulares após um ponto de início aleatório
def amostragem_sistematica(data, sample_size):
    interval = len(data) // sample_size
    indices = np.arange(0, len(data), interval)
    return data.iloc[indices]


# Amostragem Estratificada: A população é dividida em subgrupos homogêneos, e amostras aleatórias são selecionadas de cada estrato proporcionalmente ao seu tamanho na população
def amostragem_estratificada(data, strata_column, sample_size):
    strata = data[strata_column].unique()
    amostra_estratificada = pd.DataFrame()

    for stratum in strata:
        stratum_data = data[data[strata_column] == stratum]
        stratum_sample = stratum_data.sample(n=sample_size // len(strata), random_state=1)
        amostra_estratificada = pd.concat([amostra_estratificada, stratum_sample])

    return amostra_estratificada


# Interface Simples para o Sistema
def menu():
    filepath = input("Digite o caminho do arquivo CSV: ")
    dados = carregar_dados(filepath)

    print("Selecione o tipo de amostragem:")
    print("1. Amostragem Aleatória Simples")
    print("2. Amostragem Sistemática")
    print("3. Amostragem Estratificada")
    choice = int(input("Digite a opção (1/2/3): "))
    sample_size = int(input("Digite o tamanho da amostra: "))

    if choice == 1:
        amostra = amostragem_aleatoria_simples(dados, sample_size)
    elif choice == 2:
        amostra = amostragem_sistematica(dados, sample_size)
    elif choice == 3:
        strata_column = input("Digite a coluna de estratificação: ")
        amostra = amostragem_estratificada(dados, strata_column, sample_size)
    else:
        print("Opção inválida!")
        return

    print("Amostra gerada:")
    print(amostra)

# Executar o menu
menu()