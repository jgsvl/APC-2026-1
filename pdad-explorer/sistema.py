import pandas as pd

def carregarDados():
    moradores = pd.read_csv("dados/moradores.csv", sep=";", decimal=",", encoding="utf-8-sig", low_memory=False)
    domicilios = pd.read_excel("dados/domicilios.xlsx")
    return moradores, domicilios

print(carregarDados())    