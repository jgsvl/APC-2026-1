# Explorador PDAD 2024 — Perfil Educacional por Região Administrativa

Sistema com interface gráfica em Tkinter para explorar os microdados da Pesquisa Distrital por Amostra de Domicílios (PDAD) 2024, com foco no perfil educacional da população do Distrito Federal (Recorte A). O usuário pode filtrar os dados por Região Administrativa (RA) e por gênero, comparar duas RAs lado a lado, e visualizar a distribuição de escolaridade e gênero em gráficos. O usuário pode exportar um relatório com as estatísticas calculadas. Os valores sentinela do PDAD (`99999` e `88888`) são filtrados automaticamente antes de qualquer cálculo.

## Como executar

1. Instale as dependências (veja abaixo).
2. Rode o sistema principal:
   ```
   python sistema.py
   ```
3. Na tela inicial, selecione os três arquivos de dados pedidos (Moradores, Domicílios e Dicionário de Variáveis) e clique em **Carregar Sistema**.

## Dependências

```
pip install -r requirements.txt
```

Bibliotecas utilizadas: `pandas`, `matplotlib`, `logging` ,`tkinter` e `sys`.

## Arquivos de dados necessários

O sistema pede três arquivos na tela inicial:

- **Moradores** (`.csv`) — ex: `PDAD_2024-Moradores.csv`
- **Domicílios** (`.xlsx`) — ex: `PDAD_2024-Domicilios.xlsx`
- **Dicionário de Variáveis** (`.xlsx`) — ex: `Dicionario_de_variaveis_PDAD_2024.xlsx`

Os arquivos completos podem ser baixados em: https://pdad.ipe.df.gov.br/

## Autor

- João Gabriel da Silva Vidal — matrícula 202053321

---
*APC 2026/1 — Turma 07 — Licenciatura em Computação — UnB/CIC*