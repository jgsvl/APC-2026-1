import pandas as pd

# Carrega os dados e remove valores sentinela (99999 e 88888) das variáveis principais
def carregar_dados(caminho_moradores="dados/moradores.csv", caminho_domicilios="dados/domicilios.xlsx"):
    
    moradores = pd.read_csv(caminho_moradores, sep=";", decimal=",", encoding="utf-8-sig", low_memory=False)
    domicilios = pd.read_excel(caminho_domicilios)
    
    moradores_limpo = moradores[
        (moradores['id_genero'] != 99999) & (moradores['id_genero'] != 88888) &
        (moradores['escolaridade'] != 99999) & (moradores['escolaridade'] != 88888) &
        (moradores['idade_calculada'] != 99999) & (moradores['idade_calculada'] != 88888)
    ].copy()
    
    return moradores_limpo, domicilios