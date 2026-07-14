"""Módulo principal do sistema de exploração de dados do PDAD 2024, recorte A - Perfil educacional por Região Administrativa."""
__author__ = "João Gabriel da Silva Vidal"
__email__ = "jgsvl@outlook.com"

import logging # biblioteca para exibir mensagens de log no console, ao invés de print() espalhados pelo código
import tkinter as tk # Biblioteca base para a interface gráfica
from tkinter import ttk # Widgets mais modernos (abas, combobox)

import matplotlib.pyplot as plt # Biblioteca para gerar os gráficos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Conecta o gráfico na tela do Tkinter

# Importa as nossas próprias funções criadas na pasta utils
import utils.carregar as carregar
import utils.calcular as calcular
import utils.exportar as exportar
import system.arte_console as arte
import system.upload_de_arquivos as upload

# configura o logging para exibir mensagens de informação no console com data e hora, 
# ao invés de usar print() espalhados pelo código
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

# Imprime o banner do sistema no console
arte.imprime_banner()

# Abre a tela de seleção de arquivos e só prossegue depois que o usuário escolher os 3 arquivos
caminhos = upload.tela_selecao_arquivos()

# Lê os arquivos escolhidos pelo usuário e salva o dataframe pronto.
df_moradores, df_domicilios = carregar.carregar_dados(
    caminhos["moradores"], caminhos["domicilios"], caminhos["dicionario"]
)

# Cria a lista de opções para a caixa suspensa (ordenada alfabeticamente)
# pega as RAs sem repetição, do próprio dataframe dos moradores, e adiciona a opção "Todas" no início da lista
# .unique() ignora os valores duplicados
# .sorted() ordena alfabeticamente
opcoes_ra = ["Todas"] + sorted(list(df_moradores['nome_ra'].unique()))

# constroi a janela principal
root = tk.Tk()
root.title("Explorador PDAD - Recorte A - Perfil educacional por Região Administrativa")
root.geometry("1000x600") # Largura x Altura

# Cria o sistema de abas e expande para ocupar a tela toda
# ttk.Notebook() é o widget que cria abas internas e coloca no root, que é a janela principal
abas = ttk.Notebook(root)

# fill="both" faz com que ele ocupe toda a largura e altura da janela
# expand=True faz com que ele se expanda quando a janela for redimensionada
abas.pack(fill="both", expand=True)


# Cria três abas internas
tab_graficos = tk.Frame(abas)
tab_info = tk.Frame(abas)
tab_sobre = tk.Frame(abas)

abas.add(tab_graficos, text="Gráficos")
abas.add(tab_info, text="Informações do Recorte")
abas.add(tab_sobre, text="Sobre")

# Textos para a aba de informações
tk.Label(tab_info, text="Recorte A - Escolaridade", font=("Arial", 16, "bold")).pack(pady=20)
tk.Label(tab_info, text=f"Total de registros filtrados: {len(df_moradores)} moradores.").pack()

# Textos para a aba Sobre (Identificação do Aluno)
tk.Label(tab_sobre, text="Disciplina: APC 2026/1 turma 07", font=("Arial", 16, "bold")).pack(pady=(40, 10))
tk.Label(tab_sobre, text="Aluno: João Gabriel da Silva Vidal", font=("Arial", 14)).pack(pady=5)
tk.Label(tab_sobre, text="Matrícula: 202053321", font=("Arial", 14)).pack(pady=5)

# filtros e textos da aba principal, de gráficos
frame_top = tk.Frame(tab_graficos)
frame_top.pack(pady=10)

# Filtro 1: Região Principal
tk.Label(frame_top, text="RA Principal:").pack(side="left")
ra1_var = ttk.Combobox(frame_top, values=opcoes_ra, state="readonly", width=20)
ra1_var.set("Todas")
ra1_var.pack(side="left", padx=5)

# Filtro 2: Região para Comparação
tk.Label(frame_top, text="Comparar com:").pack(side="left", padx=(20,0))
ra2_var = ttk.Combobox(frame_top, values=["Nenhuma"] + opcoes_ra, state="readonly", width=20)
ra2_var.set("Nenhuma")
ra2_var.pack(side="left", padx=5)

# Filtro 3: Gênero
tk.Label(frame_top, text="Gênero:").pack(side="left", padx=(20, 0))
genero_var = ttk.Combobox(frame_top, values=["Todos"] + list(calcular.DICIONARIO_GENERO.values()), state="readonly", width=15)
genero_var.set("Todos")
genero_var.pack(side="left", padx=5)


# "subframe" para as estatísticas, dentro da aba tab_graficos
frame_estatisticas = tk.Frame(tab_graficos)
frame_estatisticas.pack(pady=10)

# Área onde os textos das estatísticas vão aparecer

# estatisticas sobre a RA Principal
label_estatisticas_ra1 = tk.Label(frame_estatisticas, text="", font=("Courier", 11, "bold"), fg="#333333", justify="left")
label_estatisticas_ra1.pack(side="left", padx=20)

# estatisticas sobre a RA de comparação
label_estatisticas_ra2 = tk.Label(frame_estatisticas, text="", font=("Courier", 11, "bold"), fg="#333333", justify="left")
label_estatisticas_ra2.pack(side="left", padx=20)


# botão de exportar relatório, que chama a função exportar_relatorio() do exportar.py
btn_exportar = tk.Button(
    tab_graficos, 
    text="Exportar Relatório (.txt)", 
    command=lambda: exportar.exportar_relatorio(
        df_moradores, 
        ra1_var.get(), 
        ra2_var.get(), 
        genero_var.get(), 
        f"{label_estatisticas_ra1.cget("text")}\n\n{'='*30}\n\n{label_estatisticas_ra2.cget("text")}"
))
btn_exportar.pack(pady=5)

# botão de exportar CSV com os moradores filtrados pela RA Principal
# filtrar_ra() vem do calcular.py, o mesmo usado internamente pelas outras funções de estatística
btn_exportar_csv = tk.Button(
    tab_graficos,
    text="Exportar CSV Filtrado",
    command=lambda: exportar.exportar_csv_filtrado(calcular.filtrar_ra(df_moradores, ra1_var.get()), ra1_var.get())
)
btn_exportar_csv.pack(pady=5)

# Frame que vai segurar os desenhos do Matplotlib
# frames são necessários para organizar os widgets dentro da janela do Tkinter, e não haver conflito de posicionamento
frame_grafico = tk.Frame(tab_graficos)
frame_grafico.pack(fill="both", expand=True, padx=10, pady=5)

# Variáveis de controle do gráfico atual na tela
# canvas_atual: o widget do Tkinter que exibe o gráfico (precisa ser destruído para não sobrepor)
# figura_atual: a Figure do matplotlib em si (precisa ser fechada com plt.close(), senão
# o pyplot mantém ela na memória mesmo depois do widget ser destruído -> vazamento de memória
# a cada vez que o usuário troca o filtro)
canvas_atual = None
figura_atual = None

# função de atualização da tela, que é chamada sempre que o usuário muda algum filtro
def atualizar():
    """Lê os filtros, refaz as contas e redesenha a tela toda vez que o usuário interage."""

    # canvas_atual e figura_atual são variáveis globais, então precisamos declarar que vamos usá-las dentro da função
    global canvas_atual, figura_atual
    
    # Pega o texto que o usuário escolheu
    r1 = ra1_var.get()
    r2 = ra2_var.get()
    genero = genero_var.get()

    # Impede que o usuário escolha a mesma RA para os dois filtros, substituindo por "Nenhuma"
    if r1 == r2: 
        r2 = "Nenhuma"
        ra2_var.set("Nenhuma")


    # estatísticas de escolaridade da RA principal
    total1, porcentagem_com_superior1, porcentagem_com_superior_incompl1, porcentagem_com_medio_compl1, porcentagem_com_medio_incompl1, porcentagem_com_fundamental_compl1, porcentagem_com_fundamental_incompl1, porcentagem_sem_instrucao1 = calcular.calcular_estatisticas_escolaridade(df_moradores, r1, genero)
   
    texto_ra1 = (
        f"Total de pessoal da RA/Cidade [{r1}] do gênero [{genero}]: {total1} pessoas"
        f"\nSuperior completo: {porcentagem_com_superior1:.1f}%"
        f"\nSuperior incompleto: {porcentagem_com_superior_incompl1:.1f}%"
        f"\nMédio completo: {porcentagem_com_medio_compl1:.1f}%"
        f"\nMédio incompleto: {porcentagem_com_medio_incompl1:.1f}%"
        f"\nFundamental completo: {porcentagem_com_fundamental_compl1:.1f}%"
        f"\nFundamental incompleto: {porcentagem_com_fundamental_incompl1:.1f}%"
        f"\nSem instrução: {porcentagem_sem_instrucao1:.1f}%"
    )

    # atualiza o texto das estatísticas da RA principal na tela
    label_estatisticas_ra1.config(text=texto_ra1)

    if r2 != "Nenhuma":
        total2, porcentagem_com_superior2, porcentagem_com_superior_incompl2, porcentagem_com_medio_compl2, porcentagem_com_medio_incompl2, porcentagem_com_fundamental_compl2, porcentagem_com_fundamental_incompl2, porcentagem_sem_instrucao2 = calcular.calcular_estatisticas_escolaridade(df_moradores, r2, genero)
   
        texto_ra2 = (
            f"Total de pessoal da RA/Cidade [{r2}] do gênero [{genero}]: {total2} pessoas"
            f"\nSuperior completo: {porcentagem_com_superior2:.1f}%"
            f"\nSuperior incompleto: {porcentagem_com_superior_incompl2:.1f}%"
            f"\nMédio completo: {porcentagem_com_medio_compl2:.1f}%"
            f"\nMédio incompleto: {porcentagem_com_medio_incompl2:.1f}%"
            f"\nFundamental completo: {porcentagem_com_fundamental_compl2:.1f}%"
            f"\nFundamental incompleto: {porcentagem_com_fundamental_incompl2:.1f}%"
            f"\nSem instrução: {porcentagem_sem_instrucao2:.1f}%"
        )

        # atualiza o texto das estatísticas da RA de comparação na tela
        label_estatisticas_ra2.config(text=texto_ra2)
    else:
        # se não houver RA de comparação, limpa o texto da RA2
        label_estatisticas_ra2.config(text="")

    # atualiza gráficos
    # usa canvas_atual para controlar o gráfico atual na tela, e apagar o antigo antes de desenhar o novo
    if canvas_atual:
        canvas_atual.get_tk_widget().destroy()

    # Fecha a Figure antiga do matplotlib. Só destruir o widget acima (destroy()) não é
    # suficiente: o pyplot mantém a Figure guardada internamente até alguém mandar fechar.
    # Sem essa linha, a cada troca de filtro sobra uma Figure "fantasma" na memória.
    if figura_atual:
        plt.close(figura_atual)

    # Puxa os dados traduzidos do calcular.py
    barras, faixas_etarias = calcular.preparar_graficos(df_moradores, r1, r2, genero)

    # Cria três espaços de gráfico (1 linha, 3 colunas). O grafico 1 fica mais largo (3 para 2)
    graficos, (grafico1, grafico2, grafico3) = plt.subplots(
        1, 3,
        figsize=(12, 4.5),
        gridspec_kw={'width_ratios': [3, 2, 2]})
    
    # guarda a referência para poder fechar essa Figure na próxima chamada de atualizar()
    figura_atual = graficos 

    # Gráfico 1: barras horizontais com % de escolaridade + rótulo percentual em cada barra
    barras.plot(kind='barh', ax=grafico1, edgecolor='black', colormap='tab10')
    grafico1.set_title(f"Porcentagem de escolaridade dentro do grupo ({genero})")
    grafico1.set_ylabel("")
    grafico1.set_xlabel("% de pessoas")
    for container in grafico1.containers:
        grafico1.bar_label(container, fmt='%.1f%%', padding=3, fontsize=8)

    # Gráfico 2: grafico de pizza de faixas etárias da RA principal
    faixas_etarias[r1].plot(
        kind='pie', 
        ax=grafico2, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=['#4CAF50', '#FF9800', '#9C27B0', "#FF0000", "#001EFF", "#00FFDD", "#1C401F"])
    grafico2.set_ylabel("")
    grafico2.set_title(f"Faixas etárias\n({r1})", fontsize=10)

    # Gráfico 3: grafico de pizza de faixas etárias da RA de comparação
    if r2 != "Nenhuma":
        faixas_etarias[r2].plot(
            kind='pie', 
            ax=grafico3, 
            autopct='%1.1f%%', 
            startangle=90, 
            colors=['#4CAF50', '#FF9800', '#9C27B0', "#FF0000", "#001EFF", "#00FFDD", "#1C401F"])
        grafico3.set_ylabel("")
        grafico3.set_title(f"Faixas etárias\n({r2})", fontsize=10)
    else:
        grafico3.axis('off')  # se não houver RA de comparação, esconde o gráfico 3
        
    # Ajusta o layout para não cortar títulos e rótulos
    plt.tight_layout()

    # Injeta a figura do Matplotlib dentro da janela do Tkinter
    canvas_atual = FigureCanvasTkAgg(graficos, master=frame_grafico)
    canvas_atual.draw()
    canvas_atual.get_tk_widget().pack(fill="both", expand=True)

# execução inicial do programa, para desenhar a tela com os filtros padrão
# Diz para as Combobox dispararem a função atualizar() sempre que forem alteradas
# isso é necessário para que o usuário veja os gráficos mudarem em tempo real, sem precisar apertar nenhum botão
# lambda e: atualizar() é uma função anônima que chama atualizar() sem argumentos, pois o bind passa um evento como argumento
# semelhante a classes anonomas e lambdas (->) do Java
ra1_var.bind("<<ComboboxSelected>>", lambda e: atualizar())
ra2_var.bind("<<ComboboxSelected>>", lambda e: atualizar())
genero_var.bind("<<ComboboxSelected>>", lambda e: atualizar())

# Força a primeira execução para o programa não abrir com a tela branca
atualizar() 

def ao_fechar_janela():
    """Fecha as figuras do matplotlib antes de destruir a janela, para o processo encerrar corretamente ao clicar no X."""
    # Sem isso, o pyplot mantém a última Figure "presa" com uma referência para um widget
    # do Tkinter que já não existe mais, e o console/terminal não volta ao prompt depois
    # que a janela é fechada -- o programa fica pendurado em segundo plano.
    if figura_atual:
        plt.close(figura_atual)
    plt.close('all')  # segurança extra: fecha qualquer outra figura órfã que o pyplot ainda tenha registrada
    root.quit()     # interrompe o mainloop() explicitamente
    root.destroy()  # libera os recursos da janela

# Registra ao_fechar_janela() para ser chamada quando o usuário clicar no X da janela,
# em vez de deixar o Tkinter usar o comportamento padrão (que não fecha as figuras do matplotlib)
root.protocol("WM_DELETE_WINDOW", ao_fechar_janela)

# Roda o programa e mantém a janela aberta
# mainloop() é o loop principal do Tkinter, que mantém a janela aberta e escuta eventos do usuário
root.mainloop()