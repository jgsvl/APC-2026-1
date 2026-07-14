from tkinter import filedialog, messagebox

def exportar_relatorio(df, ra1, ra2, genero, texto_estatisticas):
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
        # Abre o arquivo em modo de escrita ('w' = write))
        # 'utf-8' garante que acentos e caracteres especiais sejam salvos corretamente
        f = open(arquivo, "w", encoding="utf-8")
        
        f.write("--- Perfil educacional por Região Administrativa ---\n\n")
        f.write(f"Filtros aplicados:\nRA Principal: {ra1}\nRA Comparação: {ra2}\nGênero: {genero}\n\n")
        f.write("--- Estatísticas ---\n")
        f.write(texto_estatisticas + "\n\n")
        f.write("--- Observação ---\n")
        f.write("Dados do tipo \"não sabe\"/\"não se aplica\" com relação à idade calculada, gênero e escolaridade foram filtrados.\n")
        
        f.close() # Fecha o arquivo para liberar a memória
        
        # Mostra a mensagem de sucesso usando o messagebox padrão do tkinter
        messagebox.showinfo("Sucesso", "Relatório exportado com sucesso!")


def exportar_csv_filtrado(df_filtrado, ra):
    """
    Exporta os registros de moradores já filtrados pela RA selecionada para um arquivo .csv.
    """
    # Trava de segurança: se o filtro não trouxe nenhum morador, não faz sentido abrir o diálogo de salvar
    if len(df_filtrado) == 0:
        messagebox.showwarning("Aviso", "Não há registros para exportar com esse filtro.")
        return

    # Sugere um nome de arquivo já com a RA no nome (ex: moradores_Varjão.csv), trocando
    # espaços por "_" para o nome do arquivo ficar mais limpo
    nome_sugerido = f"moradores_{ra}.csv".replace(" ", "_")

    arquivo = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Arquivo CSV", "*.csv")],
        title="Salvar CSV Filtrado",
        initialfile=nome_sugerido
    )

    if arquivo != "":
        # sep=";" e decimal="," mantêm o mesmo formato do arquivo original do PDAD,
        # para o CSV exportado poder ser reaberto (ou reimportado no sistema) sem estranhezas
        df_filtrado.to_csv(arquivo, sep=";", decimal=",", index=False, encoding="utf-8")

        messagebox.showinfo("Sucesso", f"CSV com {len(df_filtrado)} registros exportado com sucesso!")