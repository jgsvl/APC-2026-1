import pandas as pd # Importa o Pandas, nossa ferramenta principal para lidar com tabelas
import logging
import time

# Cria um logger específico para este arquivo (ele herda a configuração do sistema.py)
logger = logging.getLogger(__name__)

def carregar_dados():
    """Carrega os dataframes, remove valores sentinela e mapeia as RAs dinamicamente."""
    tempo_inicio = time.time() # marca o tempo de início do carregamento, para medir performance
    logger.info("Carregando os arquivos")
    # lê o arquivo CSV com os dados dos moradores
    # sep=";" e decimal="," garantem que o Pandas entenda o formato brasileiro
    # low_memory=False lê o arquivo inteiro de uma vez, evitando avisos de tipos mistos
    logger.info("Lendo moradores.csv")
    moradores = pd.read_csv("dados/moradores.csv", sep=";", decimal=",", low_memory=False)
    

    # lê o arquivo Excel com os dados dos domicílios, porém ainda não é usado no sistema
    logger.info("Lendo domicilios.xlsx")
    domicilios = pd.read_excel("dados/domicilios.xlsx")
    
    
    # filtra os moradores para remover valores sentinela (99999 e 88888) de idade, gênero e escolaridade
    # Cria uma máscara booleana. Só passam as linhas onde a idade,
    # o gênero e a escolaridade forem != 99999 e != 88888.
    # O .copy() cria uma cópia do dataframe filtrado
    logger.info("Iniciando fitro de sentinelas (valores 99999 e 88888)...")
    moradores_limpo = moradores[
        (moradores['id_genero'] != 99999) & (moradores['id_genero'] != 88888) &
        (moradores['escolaridade'] != 99999) & (moradores['escolaridade'] != 88888) &
        (moradores['idade_calculada'] != 99999) & (moradores['idade_calculada'] != 88888)
    ].copy()
    
    # mapeamento dinâmico das RAs usando o dicionário de dados
    # Lê a aba 'anexo_1' do Dicionário de Variáveis (onde estão os nomes das RAs)
    # Tentei evitar de deixar os códigos das RAs hardcoded no código, porém agora estamos
    # fortemente acoplados com o arquivo do dicionário, então se ele mudar de nome ou de formato, 
    # o programa vai quebrar.
    logger.info("Iniciando leitura do dicionário de variáveis para mapear as RAs...")
    caminho_dicionario = "dados/dicionario_de_variaveis_pdada_2024_público.xlsx"
    planilha_dicionario = pd.read_excel(caminho_dicionario, sheet_name="anexo_1")
    
    # Pega a coluna 'Valor' (códigos numéricos) e a 'Descrição do valor' (nomes em texto)
    # e junta as duas num dicionário Python usando zip() e dict().
    # realmente, ficamos muito acoplados com o nome das colunas do dicionário, mas foi 
    # a maneira que encontrei para nao deixar as RAs hardcoded.
    # Exemplo: {5301: 'Plano Piloto', 5302: 'Gama'}
    mapa_ra = dict(zip(planilha_dicionario['Valor'], planilha_dicionario['Descrição do valor']))
    
    # Cria a coluna 'nome_ra'. O .map() pega o código da 'localidade', procura no nosso mapa 
    # e escreve o nome da RA. Se faltar algum, o .fillna() coloca "Outra Localidade".
    logger.info("Adicionando coluna 'nome_ra' com os nomes das RAs no dataframe de moradores...")
    moradores_limpo['nome_ra'] = moradores_limpo['localidade'].map(mapa_ra).fillna("Outra Localidade")
    

    logger.info("Dados carregados e limpos com sucesso!")

    tempo_fim = time.time() # marca o tempo de fim do carregamento
    tempo_total = tempo_fim - tempo_inicio # calcula o tempo total de carregamento
    logger.info(f"Tempo total de carregamento dos arquivos: {tempo_total:.2f} segundos")

    # Retorna nossa base de dados limpa
    return moradores_limpo, domicilios