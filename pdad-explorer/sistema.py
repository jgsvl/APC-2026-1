import logging
import sys
import tkinter as tk # Biblioteca base para a interface gráfica
from tkinter import ttk # Widgets mais modernos (abas, combobox)
from tkinter import filedialog # Diálogo de seleção de arquivos (Requisito de upload via GUI)
import matplotlib.pyplot as plt # Biblioteca para gerar os gráficos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Conecta o gráfico na tela do Tkinter

# Importa as nossas próprias funções criadas na pasta utils
import utils.carregar
import utils.calcular
import utils.exportar

# configura o logging para exibir mensagens de informação no console, ao invés de usar print() espalhados pelo código
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

# mensagem de boas-vindas no console, usando ASCII art.
# o "r" antes da string indica que é uma raw string, então
# não precisamos escapar as barras invertidas.
print(r"""
     ____.                       ________      ___.         .__       .__   
    |    | _________    ____    /  _____/_____ \_ |_________|__| ____ |  |  
    |    |/  _ \__  \  /  _ \  /   \  ___\__  \ | __ \_  __ \  |/ __ \|  |  
/\__|    (  <_> ) __ \(  <_> ) \    \_\  \/ __ \| \_\ \  | \/  \  ___/|  |__
\________|\____(____  /\____/   \______  (____  /___  /__|  |__|\___  >____/
                    \/                 \/     \/    \/              \/       
            """)

def escolher_arquivo(variavel_destino, titulo, tipos):
    """Abre o diálogo de seleção de arquivo e guarda o caminho escolhido na variável de tela."""
    caminho = filedialog.askopenfilename(title=titulo, filetypes=tipos)
    # Se o usuário cancelar o diálogo, askopenfilename devolve string vazia, então não sobrescrevemos nada
    if caminho:
        variavel_destino.set(caminho)


def tela_selecao_arquivos():
    """Abre uma janela inicial para o usuário escolher os 3 arquivos antes do sistema carregar os dados."""
    logger.info("Aguardando o upload dos arquivos")
    janela_selecao = tk.Tk()
    janela_selecao.title("Explorador PDAD - Selecionar Arquivos")
    janela_selecao.geometry("620x300")

    tk.Label(
        janela_selecao,
        text="Selecione os arquivos de dados do PDAD 2024",
        font=("Arial", 13, "bold")
    ).pack(pady=(15, 10))

    # Guarda os caminhos escolhidos como texto, para exibir na tela e habilitar o botão de carregar
    var_moradores = tk.StringVar(value="")
    var_domicilios = tk.StringVar(value="")
    var_dicionario = tk.StringVar(value="")

    # Dicionário que vai guardar o resultado final, depois que a janela for fechada.
    # Usamos um dicionário, e não variáveis soltas, porque as funções internas (confirmar/verificar)
    # precisam escrever nesse valor e ele precisa "sobreviver" depois do janela_selecao.destroy()
    resultado = {}

    def montar_linha(rotulo, variavel, titulo_dialogo, tipos):
        """Monta uma linha padrão de 'rótulo + caminho escolhido + botão Procurar' na tela de seleção."""
        frame_linha = tk.Frame(janela_selecao)
        frame_linha.pack(fill="x", padx=20, pady=8)

        tk.Label(frame_linha, text=rotulo, width=16, anchor="w").pack(side="left")

        # Entry "readonly" só para mostrar o caminho escolhido; o usuário não digita nele diretamente
        entrada = tk.Entry(frame_linha, textvariable=variavel, state="readonly", width=45)
        entrada.pack(side="left", padx=5)

        tk.Button(
            frame_linha,
            text="Procurar...",
            command=lambda: escolher_arquivo(variavel, titulo_dialogo, tipos)
        ).pack(side="left")

    montar_linha("Moradores (.csv):", var_moradores, "Selecione o arquivo de Moradores",
                 [("Arquivo CSV", "*.csv")])
    montar_linha("Domicílios (.xlsx):", var_domicilios, "Selecione o arquivo de Domicílios",
                 [("Arquivo Excel", "*.xlsx")])
    montar_linha("Dicionário (.xlsx):", var_dicionario, "Selecione o Dicionário de Variáveis",
                 [("Arquivo Excel", "*.xlsx")])

    def confirmar_selecao():
        """Salva os caminhos escolhidos em 'resultado' e fecha a tela de seleção."""
        resultado["moradores"] = var_moradores.get()
        resultado["domicilios"] = var_domicilios.get()
        resultado["dicionario"] = var_dicionario.get()
        janela_selecao.destroy()

    btn_iniciar = tk.Button(
        janela_selecao,
        text="Carregar Sistema",
        font=("Arial", 11, "bold"),
        state="disabled",
        command=confirmar_selecao
    )
    btn_iniciar.pack(pady=20)

    def verificar_completo(*args):
        """Habilita o botão 'Carregar Sistema' somente quando os 3 arquivos tiverem sido escolhidos."""
        if var_moradores.get() and var_domicilios.get() and var_dicionario.get():
            btn_iniciar.config(state="normal")
        else:
            btn_iniciar.config(state="disabled")

    # trace_add dispara verificar_completo() toda vez que uma das 3 variáveis mudar de valor
    var_moradores.trace_add("write", verificar_completo)
    var_domicilios.trace_add("write", verificar_completo)
    var_dicionario.trace_add("write", verificar_completo)

    janela_selecao.mainloop()

    # Se o usuário fechar a janela no "X" sem escolher os arquivos, 'resultado' fica vazio.
    # Nesse caso encerramos o programa em vez de tentar carregar dados que não existem.
    if not resultado:
        logger.info("Nenhum arquivo selecionado. Encerrando o programa.")
        sys.exit()
    logger.info("Upload de arquivos finalizado")
    return resultado


# Abre a tela de seleção de arquivos e só prossegue depois que o usuário escolher os 3 arquivos
caminhos = tela_selecao_arquivos()

# Lê os arquivos escolhidos pelo usuário e salva o dataframe pronto.
df_moradores, df_domicilios = utils.carregar.carregar_dados(
    caminhos["moradores"], caminhos["domicilios"], caminhos["dicionario"]
)

# Cria a lista de opções para a caixa suspensa (ordenada alfabeticamente)
# pega as RAs sem repetição, do próprio dataframe dos moradores, e adiciona a opção "Todas" no início da lista
# .unique() ignora os valores duplicados
# .sorted() ordena alfabeticamente
opcoes_ra = ["Todas"] + sorted(list(df_moradores['nome_ra'].unique()))

# constroi a janela principal
root = tk.Tk()
root.title("Explorador PDAD - Perfil educacional por Região Administrativa")
root.geometry("950x650") # Largura x Altura

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

# Área onde os números das estatísticas vão aparecer
lbl_stats = tk.Label(tab_graficos, text="", font=("Courier", 11, "bold"), fg="#333333")
lbl_stats.pack(pady=10)

# botão de exportar relatório, que chama a função exportar_relatorio() do exportar.py
btn_exportar = tk.Button(
    tab_graficos, 
    text="Exportar Relatório (.txt)", 
    command=lambda: utils.exportar.exportar_relatorio(df_moradores, ra1_var.get(), ra2_var.get(), lbl_stats.cget("text"))
)
btn_exportar.pack(pady=5)

# botão de exportar CSV com os moradores filtrados pela RA Principal
# filtrar_ra() vem do calcular.py, o mesmo usado internamente pelas outras funções de estatística
btn_exportar_csv = tk.Button(
    tab_graficos,
    text="Exportar CSV Filtrado",
    command=lambda: utils.exportar.exportar_csv_filtrado(utils.calcular.filtrar_ra(df_moradores, ra1_var.get()), ra1_var.get())
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
    
    # Impede que o usuário escolha a mesma RA para os dois filtros, pois isso não faz sentido
    if r1 == r2: 
        r2 = "Nenhuma"
        ra2_var.set("Nenhuma")

    # atualiza texto
    t1, med1 = utils.calcular.calcular_stats(df_moradores, r1)
    # calcular_acesso_internet cruza (merge) moradores e domicílios -> gera a 3ª estatística e o Diferencial D3
    net1, net_sup1, net_semsup1 = utils.calcular.calcular_acesso_internet(df_moradores, df_domicilios, r1)
    texto = (
        f"[{r1}] -> Total: {t1} adultos | Média Idade: {med1:.1f} anos\n"
        f"[{r1}] -> Domicílios c/ internet: {net1:.1f}% "
     #   f"(responsável c/ superior: {net_sup1:.1f}% | sem superior: {net_semsup1:.1f}%)"
    )
    
    if r2 != "Nenhuma":
        t2, med2 = utils.calcular.calcular_stats(df_moradores, r2)
        net2, net_sup2, net_semsup2 = utils.calcular.calcular_acesso_internet(df_moradores, df_domicilios, r2)
        texto += (
            f"\n[{r2}] -> Total: {t2} adultos | Média Idade: {med2:.1f} anos"
            f"\n[{r2}] -> Domicílios c/ internet: {net2:.1f}% "
            f"(responsável c/ superior: {net_sup2:.1f}% | sem superior: {net_semsup2:.1f}%)"
        )
        
    lbl_stats.config(text=texto)

    # atualiza gráficos
    # usa canvas_atual para controlar o gráfico atual na tela, e apagar o antigo antes de desenhar o novo
    if canvas_atual:
        canvas_atual.get_tk_widget().destroy() # Apaga o widget do gráfico velho da tela

    # Fecha a Figure antiga do matplotlib. Só destruir o widget acima (destroy()) não é
    # suficiente: o pyplot mantém a Figure guardada internamente até alguém mandar fechar.
    # Sem essa linha, a cada troca de filtro sobra uma Figure "fantasma" na memória.
    if figura_atual:
        plt.close(figura_atual)

    # Puxa os dados traduzidos do calcular.py
    barras, pizza = utils.calcular.preparar_graficos(df_moradores, r1, r2)
    
    # Cria os dois espaços de gráfico (1 linha, 2 colunas). O de barras fica mais largo (2 para 1)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), gridspec_kw={'width_ratios': [2, 1]})
    figura_atual = fig # guarda a referência para poder fechar essa Figure na próxima chamada de atualizar()
    
    # Desenha o Gráfico de Barras Agrupadas
    barras.plot(kind='barh', ax=ax1, edgecolor='black', colormap='tab10')
    ax1.set_title("Nível de Escolaridade")
    ax1.set_ylabel("")
    ax1.set_xlabel("Quantidade de Pessoas")
    
    # Desenha o Gráfico de Pizza (Gênero da RA Principal)
    if not pizza.empty:
        pizza.plot(kind='pie', ax=ax2, autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#FF9800', '#9C27B0'])
        ax2.set_ylabel("")
        ax2.set_title(f"Distribuição de Gênero\n({r1})", fontsize=10)
        
    plt.tight_layout()
    
    # Injeta a figura do Matplotlib dentro da janela do Tkinter
    canvas_atual = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas_atual.draw()
    canvas_atual.get_tk_widget().pack(fill="both", expand=True)

# execução inicial do programa, para desenhar a tela com os filtros padrão
# Diz para as Combobox dispararem a função atualizar() sempre que forem alteradas
# isso é necessário para que o usuário veja os gráficos mudarem em tempo real, sem precisar apertar nenhum botão
# lambda e: atualizar() é uma função anônima que chama atualizar() sem argumentos, pois o bind passa um evento como argumento
# semelhante a classes anonomas e lambdas (->) do Java
ra1_var.bind("<<ComboboxSelected>>", lambda e: atualizar())
ra2_var.bind("<<ComboboxSelected>>", lambda e: atualizar())

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