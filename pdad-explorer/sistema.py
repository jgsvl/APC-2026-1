import tkinter as tk # Biblioteca base para a interface gráfica
from tkinter import ttk # Widgets mais modernos (abas, combobox)
import matplotlib.pyplot as plt # Biblioteca para gerar os gráficos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Conecta o gráfico na tela do Tkinter

# Importa as nossas próprias funções criadas na pasta utils
from utils.carregar import carregar_dados
from utils.calcular import calcular_stats, preparar_graficos

# =============================================================================
# 1. CARGA DE DADOS INICIAL
# =============================================================================
# Lê os arquivos e salva o dataframe pronto.
df_moradores, df_domicilios = carregar_dados()

# Cria a lista de opções para a caixa suspensa (ordenada alfabeticamente)
opcoes_ra = ["Todas"] + sorted(list(df_moradores['nome_ra'].unique()))

# =============================================================================
# 2. CONSTRUÇÃO DA JANELA PRINCIPAL (Requisito 1)
# =============================================================================
root = tk.Tk()
root.title("Explorador PDAD - Escolaridade no DF")
root.geometry("950x650") # Largura x Altura

# Cria o sistema de abas e expande para ocupar a tela toda
abas = ttk.Notebook(root)
abas.pack(fill="both", expand=True)

# Cria as duas abas internas
tab_graficos = tk.Frame(abas)
tab_info = tk.Frame(abas)
abas.add(tab_graficos, text="Dashboard Analítico")
abas.add(tab_info, text="Informações do Recorte")

# Textos simples para a aba de informações
tk.Label(tab_info, text="Recorte A - Escolaridade", font=("Arial", 16, "bold")).pack(pady=20)
tk.Label(tab_info, text=f"Total de registros filtrados: {len(df_moradores)} moradores.").pack()

# =============================================================================
# 3. FILTROS E TEXTOS DA ABA PRINCIPAL (Requisitos 2 e 4)
# =============================================================================
frame_top = tk.Frame(tab_graficos)
frame_top.pack(pady=10)

# Filtro 1: Região Principal
tk.Label(frame_top, text="RA Principal:").pack(side="left")
ra1_var = ttk.Combobox(frame_top, values=opcoes_ra, state="readonly", width=20)
ra1_var.set("Todas")
ra1_var.pack(side="left", padx=5)

# Filtro 2: Região para Comparação (Diferencial 2)
tk.Label(frame_top, text="vs Comparar com:").pack(side="left", padx=(20,0))
ra2_var = ttk.Combobox(frame_top, values=["Nenhuma"] + opcoes_ra, state="readonly", width=20)
ra2_var.set("Nenhuma")
ra2_var.pack(side="left", padx=5)

# Área onde os números das estatísticas vão aparecer
lbl_stats = tk.Label(tab_graficos, text="", font=("Courier", 11, "bold"), fg="#333333")
lbl_stats.pack(pady=10)

# Frame que vai segurar os desenhos do Matplotlib
frame_grafico = tk.Frame(tab_graficos)
frame_grafico.pack(fill="both", expand=True, padx=10, pady=5)

# Variável de controle do gráfico atual na tela
canvas_atual = None

# =============================================================================
# 4. FUNÇÃO DE ATUALIZAÇÃO (Requisito 3)
# =============================================================================
def atualizar():
    """Lê os filtros, refaz as contas e redesenha a tela toda vez que o usuário interage."""
    global canvas_atual
    
    # Pega o texto que o usuário escolheu
    r1 = ra1_var.get()
    r2 = ra2_var.get()
    
    # Impede que o usuário compare "Gama" com "Gama", por exemplo
    if r1 == r2: 
        r2 = "Nenhuma"
        ra2_var.set("Nenhuma")

    # --- PARTE 1: ATUALIZA TEXTOS (Requisito 4) ---
    t1, med1 = calcular_stats(df_moradores, r1)
    texto = f"[{r1}] -> Total: {t1} adultos | Média Idade: {med1:.1f} anos"
    
    if r2 != "Nenhuma":
        t2, med2 = calcular_stats(df_moradores, r2)
        texto += f"\n[{r2}] -> Total: {t2} adultos | Média Idade: {med2:.1f} anos"
        
    lbl_stats.config(text=texto)

    # --- PARTE 2: ATUALIZA GRÁFICOS (Diferenciais 1 e 2) ---
    if canvas_atual:
        canvas_atual.get_tk_widget().destroy() # Apaga o gráfico velho
        
    # Puxa os dados traduzidos lá do nosso módulo calcular.py
    barras, pizza = preparar_graficos(df_moradores, r1, r2)
    
    # Cria os dois espaços de gráfico (1 linha, 2 colunas). O de barras fica mais largo (2 para 1)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), gridspec_kw={'width_ratios': [2, 1]})
    
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

# =============================================================================
# 5. EXECUÇÃO
# =============================================================================
# Diz para as Combobox dispararem a função atualizar() sempre que forem alteradas
ra1_var.bind("<<ComboboxSelected>>", lambda e: atualizar())
ra2_var.bind("<<ComboboxSelected>>", lambda e: atualizar())

# Força a primeira execução para o programa não abrir com a tela branca
atualizar() 

# Roda o programa e mantém a janela aberta
root.mainloop()