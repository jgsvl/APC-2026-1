import pandas as pd

# Mapeamento com os valores exatos do Dicionário do PDAD
DICIONARIO_ESCOLARIDADE = {
    1: "Sem instrução",
    2: "Fund. Incompleto",
    3: "Fund. Completo",
    4: "Médio Incompleto",
    5: "Médio Completo",
    6: "Sup. Incompleto",
    7: "Sup. Completo",
    8: "Sem classificação",
}
# Mapeamento com os valores exatos do Dicionário do PDAD
DICIONARIO_GENERO = {
    1: "Cisgênero",
    2: "Transgênero",
    3: "Outro",
}


def filtrar_ra(dataframe_moradores, regiao_administrativa):
    """
    Função que filtra a base de dados pela Região Administrativa escolhida.
    :param dataframe_moradores: DataFrame do Pandas com os dados de moradores
    :param regiao_administrativa: string com o nome da RA escolhida, ou "Todas" para não filtrar
    :return: DataFrame filtrado pela RA escolhida
    """
    # Se a opção selecionada for "Todas", o sistema retorna a base de dados completa, sem cortes.
    if regiao_administrativa == "Todas":
        return dataframe_moradores
    
    # Caso contrário, aplica a máscara booleana para trazer só a RA solicitada.
    return dataframe_moradores[dataframe_moradores['nome_ra'] == regiao_administrativa]

def filtrar_genero(dataframe_moradores, genero):
    """
    Função que filtra a base de dados pelo gênero escolhido.
    :param dataframe_moradores: DataFrame do Pandas com os dados de moradores
    :param genero: string com o nome do gênero escolhido, ou "Todos" para não filtrar
    :return: DataFrame filtrado pelo gênero escolhido
    """
    # Se a opção selecionada for "Todos", o sistema retorna a base de dados completa, sem cortes.
    if genero == "Todos":
        return dataframe_moradores
    
    # Inverte a chave e valor do dicionário de gênero, para 
    # poder buscar o ID a partir do texto no filtro de gênero.
    genero_para_id = {}
    for chave, valor in DICIONARIO_GENERO.items():
        genero_para_id[valor] = chave
    genero_id = genero_para_id.get(genero)
    
    # aplica a máscara booleana para trazer só o gênero solicitado.
    return dataframe_moradores[dataframe_moradores['id_genero'] == genero_id]


def calcula_porcentagem_escolaridade(dataframe_moradores):
    """
    Função que calcula a porcentagem de cada nível de escolaridade na base de dados de moradores.
    :param dataframe_moradores: DataFrame do Pandas com os dados de moradores
    :return: pandas.Series com a porcentagem de cada escolaridade
    """
    # conta quanto cada nivel de escolaridade aparece no dataframe 
    # retornando uma Series do pandas por exemplo:
    # 1   20
    # 2   10
    # 3   15
    contagem_de_escolaridade = dataframe_moradores['escolaridade'].value_counts()

    # o pandas pega cada escolaridade da série, divide pela soma de
    # elementos e multiplica por 100, retornando uma Series com a 
    # porcentagem de cada escolaridade
    
    if contagem_de_escolaridade.sum() > 0:
        # pega a contagem de escolaridade, divide pela soma do total e multiplica por 100 para
        # obter a porcentagem de cada escolaridade
        porcentagem = contagem_de_escolaridade / contagem_de_escolaridade.sum() * 100
    else:
        # se a soma de contagem de escolaridade for zero, retorna a série vazia, para evitar divisão por zero
        porcentagem = contagem_de_escolaridade

    # pega cada código de escolaridade e substitui pelo texto correpondente do DICIONARIO_ESCOLARIDADE, 
    # e se não encontrar o código, substitui por "Outros", o que nao deve acontecer
    porcentagem.index = porcentagem.index.map(DICIONARIO_ESCOLARIDADE).fillna("Outros")

    return porcentagem

def calcular_estatisticas_escolaridade(dataframe_moradores, regiao_administrativa, genero):
    """Calcula as estatísticas de escolaridade para a RA e gênero escolhidos."""
    dataframe_moradores_filtrado_por_genero_e_ra = filtrar_genero(filtrar_ra(dataframe_moradores, regiao_administrativa), genero)

    if len(dataframe_moradores_filtrado_por_genero_e_ra) == 0:
        return 0, 0.0, 0.0, "-"

    # total de moradores filtrados por RA e gênero
    total = len(dataframe_moradores_filtrado_por_genero_e_ra)

    # % com superior completo (escolaridade == 7)
    porcentagem_com_superior = (dataframe_moradores_filtrado_por_genero_e_ra['escolaridade'] == 7).mean() * 100

    # % com superior incompleto (escolaridade == 6)
    porcentagem_com_superior_incompl = (dataframe_moradores_filtrado_por_genero_e_ra['escolaridade'] == 6).mean() * 100

    # % com médio completo (escolaridade == 5)
    porcentagem_com_medio_compl = (dataframe_moradores_filtrado_por_genero_e_ra['escolaridade'] == 5).mean() * 100

    # % com medio incompleto (escolaridade == 4)
    porcentagem_com_medio_incompl = (dataframe_moradores_filtrado_por_genero_e_ra['escolaridade'] == 4).mean() * 100

    # % com fundamental completo (escolaridade == 3)
    porcentagem_com_fundamental_compl = (dataframe_moradores_filtrado_por_genero_e_ra['escolaridade'] == 3).mean() * 100

    # % com fundamental incompleto (escolaridade == 2)
    porcentagem_com_fundamental_incompl = (dataframe_moradores_filtrado_por_genero_e_ra['escolaridade'] == 2).mean() * 100

    # % sem instrução (escolaridade == 1)
    porcentagem_sem_instrucao = (dataframe_moradores_filtrado_por_genero_e_ra['escolaridade'] == 1).mean() * 100

    return total, porcentagem_com_superior, porcentagem_com_superior_incompl, porcentagem_com_medio_compl, porcentagem_com_medio_incompl, porcentagem_com_fundamental_compl, porcentagem_com_fundamental_incompl, porcentagem_sem_instrucao


def calcular_stats(df, ra):
    """
    Calcula as estatísticas.
    """
    df_ra = filtrar_ra(df, ra)
    
    # Trava de segurança: se o filtro não encontrar ninguém, retorna zero, para não ocorrer / por zero.
    if len(df_ra) == 0: 
        return 0, 0.0
    
    # pega o total de pessoas (len() da lista) e faz a média de idades (.mean()) automaticamente 
    # a partir da coluna idade_calculada
    total_pessoas = len(df_ra)
    media_idade = df_ra['idade_calculada'].mean()
    
    return total_pessoas, media_idade


def preparar_graficos(dataframe_moradores, ra1, ra2, genero):
    """
    Prepara e contabiliza os dados que serão injetados no Matplotlib.
    :return: barras (DataFrame com % de escolaridade) e idades (dicionário com listas de idades)
    """
    # filtra os dataframes de acordo com as RAs escolhidas e generos escolhidos
    df1 = filtrar_genero(filtrar_ra(dataframe_moradores, ra1), genero)   
    
    if ra2 == "Nenhuma":
        # se não houver segunda RA, cria um dataframe vazio
        df2 = pd.DataFrame()
    else:
        df2 = filtrar_genero(filtrar_ra(dataframe_moradores, ra2), genero)
    

    # preparacão da barra de escolaridade
    barras = pd.DataFrame({ra1: calcula_porcentagem_escolaridade(df1)})

    # Adiciona a segunda RA lado a lado, se ela existir
    if not df2.empty:
        barras[ra2] = calcula_porcentagem_escolaridade(df2)
        

    # criação das faixas etárias para o gráfico
    # definimos os limites das idades e os nomes das etiquetas (labels)
    # O limite inferior é 17 para incluir o 18
    # O limite superior é infinito (float('inf'))
    limites = [17, 30, 40, 50, 60, 70, 80, float('inf')]
    etiquetas = ['18 a 30', '30 a 40', '40 a 50', '50 a 60', '60 a 70', '70 a 80', '>80']
    
    # cria um DataFrame vazio com as etiquetas como índice, para armazenar as faixas etárias
    faixas_etarias = pd.DataFrame(index=etiquetas)

    # Calcula para a RA principal
    if not df1.empty:
        idades_ra1 = pd.cut(df1['idade_calculada'], bins=limites, labels=etiquetas)
        faixas_etarias[ra1] = idades_ra1.value_counts()
    else:
        faixas_etarias[ra1] = 0 # Preenche com zero se estiver vazio
        
    # Calcula para a RA2 (se ela existir e tiver dados)
    if not df2.empty:
        idades_ra2 = pd.cut(df2['idade_calculada'], bins=limites, labels=etiquetas)
        faixas_etarias[ra2] = idades_ra2.value_counts()

    # insere 0 nos possiveis valores ausentes
    faixas_etarias = faixas_etarias.fillna(0)

    return barras, faixas_etarias
