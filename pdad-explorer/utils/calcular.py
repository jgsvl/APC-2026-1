import pandas as pd

def filtrar_ra(df, ra):
    """
    Função que filtra a base de dados pela Região Administrativa (RA) escolhida.
    """
    # Se a opção selecionada for "Todas", o sistema retorna a base de dados completa, sem cortes.
    if ra == "Todas":
        return df
    
    # Caso contrário, aplica a máscara booleana para trazer só a RA solicitada.
    return df[df['nome_ra'] == ra]

def calcular_stats(df, ra):
    """
    Calcula as estatísticas numéricas exigidas no Requisito 4 do projeto.
    """
    df_ra = filtrar_ra(df, ra)
    
    # Trava de segurança: se o filtro não encontrar ninguém, retorna zero, para não ocorrer / por zero.
    if len(df_ra) == 0: 
        return 0, 0.0
        
    total_pessoas = len(df_ra)
    media_idade = df_ra['idade_calculada'].mean()
    
    return total_pessoas, media_idade

def calcular_acesso_internet(df_moradores, df_domicilios, ra):
    """Faz merge com os domicílios (D3) e calcula o % de acesso à internet, comparando responsáveis com e sem superior completo."""
    # Pega só os responsáveis pelo domicílio (E04 == 1) da RA escolhida, pois é a pessoa
    # que representa o domicílio na hora de cruzar com os dados de infraestrutura
    responsaveis = filtrar_ra(df_moradores, ra)
    responsaveis = responsaveis[responsaveis['E04'] == 1]

    # Trava de segurança: sem responsáveis nessa RA, não há o que cruzar
    if len(responsaveis) == 0:
        return 0.0, 0.0, 0.0

    # pd.merge() cruza a tabela de moradores (responsáveis) com a de domicílios,
    # trazendo a coluna C05 (acesso à internet) usando A01nficha como chave comum -> Diferencial D3
    cruzado = responsaveis.merge(df_domicilios[['A01nficha', 'C05']], on='A01nficha', how='left')

    # Filtra a sentinela 88888 ("Não sabe") da coluna de internet antes de calcular percentuais
    cruzado = cruzado[cruzado['C05'] != 88888]

    if len(cruzado) == 0:
        return 0.0, 0.0, 0.0

    # C05: 1 = "Sim, próprio" e 2 = "Sim, compartilhado" contam como "tem acesso à internet"
    tem_internet = cruzado['C05'].isin([1, 2])
    pct_geral = tem_internet.mean() * 100

    # Separa entre responsáveis com superior completo (escolaridade == 7) e os demais
    com_superior = cruzado[cruzado['escolaridade'] == 7]
    sem_superior = cruzado[cruzado['escolaridade'] != 7]

    pct_com_superior = com_superior['C05'].isin([1, 2]).mean() * 100 if len(com_superior) > 0 else 0.0
    pct_sem_superior = sem_superior['C05'].isin([1, 2]).mean() * 100 if len(sem_superior) > 0 else 0.0

    return pct_geral, pct_com_superior, pct_sem_superior


def preparar_graficos(df, ra1, ra2):
    """
    Prepara e contabiliza os dados que serão injetados no Matplotlib.
    """
    # filtra os dataframes de acordo com as RAs escolhidas
    df1 = filtrar_ra(df, ra1)
    
    # se não houver segunda RA, cria um dataframe vazio
    if ra2 == "Nenhuma":
        df2 = pd.DataFrame()
    else:
        df2 = filtrar_ra(df, ra2)
    
    # preparacão da barra de escolaridade
    # .value_counts() soma quantas vezes cada nível de escolaridade aparece
    barras = pd.DataFrame({ra1: df1['escolaridade'].value_counts()})
    

    # Adiciona a segunda RA lado a lado, se ela existir
    if not df2.empty:
        barras[ra2] = df2['escolaridade'].value_counts()
        
    # Mapeamento com os valores exatos do Dicionário do PDAD
    mapa_escola = {
        1: "Sem instrução", 
        2: "Fund. Incompleto", 
        3: "Fund. Completo",
        4: "Médio Incompleto", 
        5: "Médio Completo", 
        6: "Sup. Incompleto", 
        7: "Sup. Completo", 
        8: "Sem classificação"
    }
    # Substitui os números (1 a 8) pelos textos. O que fugir disso vira "Outros". Só por segurança, mas não deve acontecer.
    barras.index = barras.index.map(mapa_escola).fillna("Outros")
        
    # preparação da pizza de gênero, para termos dois gráficos diferentes na tela
    # value_counts() soma quantas vezes cada gênero aparece
    pizza = df1['id_genero'].value_counts()
    
    # Mapeamento com os valores exatos de Gênero do PDAD
    mapa_genero = {
        1: "Cisgênero", 
        2: "Transgênero", 
        3: "Outro"
    }

    # Substitui os números (1 a 3) pelos textos. O que fugir disso vira "Outro". Só por segurança, mas não deve acontecer.
    pizza.index = pizza.index.map(mapa_genero).fillna("Outro")
    
    return barras, pizza