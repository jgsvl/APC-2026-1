def selection_sort_ranking(lista_dados):
    """
    Ordena uma lista de tuplas [(RA, valor), ...] de forma decrescente pelo valor.
    """
    n = len(lista_dados)
    # Transforma em lista de listas para permitir mutabilidade (troca de posições)
    dados = [list(item) for item in lista_dados]
    
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            # Compara o segundo elemento da tupla (o percentual numérico)
            if dados[j][1] > dados[max_idx][1]:
                max_idx = j
        
        # Realiza o swap (troca) das posições
        dados[i], dados[max_idx] = dados[max_idx], dados[i]
        
    return dados

def gerar_ranking_escolaridade(df):
    """Gera um ranking bruto das RAs pelo % de pessoas com Ensino Superior+."""
    ranking = []
    # Pega todas as RAs, exceto "Todas" e "Outra"
    ras = [ra for ra in df['nome_ra'].unique() if ra not in ["Todas", "Outra"]]
    
    for ra in ras:
        df_ra = df[df['nome_ra'] == ra]
        total = len(df_ra)
        if total > 0:
            # Códigos 7 (Superior) e 8 (Pós/Mestrado/Doutorado)
            qtd_sup = len(df_ra[df_ra['escolaridade'] >= 7])
            percentual = (qtd_sup / total) * 100
            ranking.append((ra, percentual))
            
    return ranking

def obter_distribuicao_genero(df_filtrado):
    """Prepara os dados de gênero para o segundo gráfico."""
    if df_filtrado.empty:
        return pd.Series(dtype=int)
        
    # Considerando 1 = Masculino, 2 = Feminino no dicionário do PDAD
    mapa_genero = {1.0: "Masculino", 2.0: "Feminino"}
    
    df_genero = df_filtrado.copy()
    df_genero['desc_genero'] = df_genero['id_genero'].map(mapa_genero).fillna("Outro")
    
    return df_genero['desc_genero'].value_counts()