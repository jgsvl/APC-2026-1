import logging
import sys # biblioteca para encerrar o programa com sys.exit() caso o usuário feche a tela de seleção de arquivos sem escolher nada
import tkinter as tk
from tkinter import filedialog # pacote necesssário para janela de seleção de arquivos

# Cria um logger específico para este arquivo (ele herda a configuração do sistema.py)
logger = logging.getLogger(__name__)

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
    janela_selecao.geometry("720x300")

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