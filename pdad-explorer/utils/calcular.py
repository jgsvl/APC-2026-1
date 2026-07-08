import pandas as pd

def calcular_estatisticas_ra(df, ra_selecionada):
    """Calcula total, média e mediana de idade para a RA especificada."""
    if ra_selecionada != "Todas" and ra_selecionada != "Nenhuma":
        df = df[df['nome_ra'] == ra_selecionada]
        
    total_pessoas = len(df)
    if total_pessoas == 0:
        return 0, 0.0, 0.0
        
    idade_media = df['idade_calculada'].mean()
    idade_mediana = df['idade_calculada'].median()
    
    return total_pessoas, idade_media, idade_mediana

def obter_distribuicao_escolaridade(df, ra_selecionada):
    """Retorna a série com a contagem de escolaridade para uma RA (Para o Gráfico de Barras)."""
    if ra_selecionada != "Todas" and ra_selecionada != "Nenhuma":
        df = df[df['nome_ra'] == ra_selecionada]
        
    mapa_escolaridade = {
        1: "Sem instrução", 2: "Fund. Incomp.", 3: "Fund. Comp.",
        4: "Médio Incomp.", 5: "Médio Comp.", 6: "Sup. Incomp.", 7: "Sup. Comp."
    }
    
    contagem = df['escolaridade'].value_counts().sort_index()
    contagem.index = contagem.index.map(mapa_escolaridade).fillna("Outros")
    
    return contagem

def obter_distribuicao_genero(df, ra_selecionada):
    """Retorna a contagem de gênero para uma RA (Para o Gráfico de Pizza)."""
    if ra_selecionada != "Todas" and ra_selecionada != "Nenhuma":
        df = df[df['nome_ra'] == ra_selecionada]
        
    # Códigos 1 e 2 baseados na variável E03 do dicionário
    mapa_genero = {1.0: "Masculino", 2.0: "Feminino"}
    
    df_genero = df.copy()
    df_genero['desc_genero'] = df_genero['id_genero'].map(mapa_genero).fillna("Outro")
    
    return df_genero['desc_genero'].value_counts()