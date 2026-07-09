from tkinter import filedialog, messagebox

def exportar_relatorio(df, ra1, ra2, texto_stats):
    """
    Gera um arquivo .txt com os dados selecionados e as estatísticas exibidas na tela.
    """
    # Abre a janela do sistema para o usuário escolher onde salvar
    # O filedialog retorna a string do caminho ou uma string vazia se o usuário cancelar
    arquivo = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Arquivo de Texto", "*.txt")],
        title="Salvar Relatório"
    )
    
    # Se o caminho for diferente de vazio, prossegue com a escrita
    if arquivo != "":
        # Abre o arquivo em modo de escrita ('w')
        # 'utf-8' garante que acentos e caracteres especiais sejam salvos corretamente
        f = open(arquivo, "w", encoding="utf-8")
        
        f.write("--- RELATÓRIO DE PERFIL EDUCACIONAL PDAD 2024 ---\n\n")
        f.write(f"Filtros aplicados:\nRA Principal: {ra1}\nRA Comparação: {ra2}\n\n")
        f.write("--- Estatísticas ---\n")
        f.write(texto_stats + "\n\n")
        f.write("--- Observação ---\n")
        f.write("Dados filtrados de sentinelas (99999 e 88888).\n")
        
        f.close() # Fecha o arquivo para liberar a memória
        
        # Mostra a mensagem de sucesso usando o messagebox padrão do tkinter
        messagebox.showinfo("Sucesso", "Relatório exportado com sucesso!")