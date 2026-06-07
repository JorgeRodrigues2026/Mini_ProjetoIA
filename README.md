# Desenvolvedor(a) em IA para Análise Preditiva - Mini projeto avaliativo - Modulo I

# SalesInsight PY: Pipeline de Análise e Visualização de Dados de Vendas

Pipeline de analise e visualizacao de dados de vendas desenvolvido para o mini-projeto avaliativo do Modulo 1. O projeto le, limpa, transforma, analisa e visualiza um dataset de vendas, gerando metricas, segmentacao de clientes, projecao simples de tendencia e arquivos de saida em CSV, JSON e PNG.

## Objetivo

Simular o trabalho de um Analista de Dados Junior em uma empresa de varejo. O sistema responde perguntas sobre comportamento de vendas por mes, produtos e categorias com maior receita, desempenho por regiao, clientes mais valiosos e tendencia simples para os proximos periodos.

## Como executar no VS Code

1. Abra a pasta `salesinsight-py` no VS Code.
2. Crie e ative um ambiente virtual, se desejar.
3. Instale as dependencias:

```bash
pip install -r requirements.txt
```

4. Execute:

```bash
python salesinsight.py
```

## Como executar no Jupyter Notebook

1. Abra o arquivo `salesinsight.ipynb` no VS Code, Jupyter Notebook ou Google Colab.
2. Execute as celulas em ordem.
3. A ultima celula roda o pipeline completo e cria os arquivos em `outputs/`.

## Estrutura do projeto

```text
salesinsight-py/
├── README.md
├── requirements.txt
├── salesinsight.py
├── salesinsight.ipynb
├── vendas.csv
├── outputs/
│   ├── estatisticas_gerais.json
│   ├── metricas_por_mes.csv
│   ├── projecao_receita.csv
│   ├── receita_por_categoria.csv
│   ├── receita_por_regiao.csv
│   ├── segmentacao_clientes.csv
│   ├── top_produtos.csv
│   └── graficos/
│       ├── boxplot_categorias.png
│       ├── distribuicao_regioes.png
│       ├── top_produtos.png
│       └── vendas_por_mes.png
└── planejamento/
    └── tarefas-kanban.md
```

## Conceitos aplicados

- Logica de programacao com variaveis, tipos de dados, operadores e condicionais.
- Estruturas de repeticao com `for`.
- Funcoes com parametros, retorno e docstrings.
- Funcoes lambda em segmentacao e transformacao de colunas.
- Funcao de ordem superior em `processar_coluna`.
- Leitura e escrita de CSV com Pandas.
- Escrita e leitura de JSON com `json.dump` e `json.load`.
- Manipulacao de datas com `datetime` e `pd.to_datetime`.
- Expressoes regulares com `re.sub` e `re.compile`.
- Pandas com DataFrames, filtros, transformacoes e `groupby`.
- NumPy com arrays, operacoes vetorizadas, broadcasting, `np.select`, `mean`, `std`, `median` e `percentile`.
- Visualizacoes com Matplotlib e Seaborn exportadas em PNG.
- Programacao orientada a objetos com `AnalisadorDeVendas`.
- Heranca e `super()` com `AnalisadorComProjecao`.

## Ferramentas utilizadas

- Python 3.10+
- VS Code com extensoes Python e Jupyter
- Jupyter Notebook ou Google Colab
- Pandas, NumPy, Matplotlib e Seaborn
- Git, GitHub e GitHub Desktop
- Kanban em GitHub Projects, Trello, Notion ou arquivo Markdown

## Internet e arquitetura cliente-servidor

Neste projeto, os dados sao lidos de um arquivo local `vendas.csv`. Em um cenario real, esses dados poderiam vir de uma API REST: o script Python seria o cliente, enviaria uma requisicao HTTP para um servidor e receberia dados em JSON para analise. Esse modelo segue a arquitetura cliente-servidor, em que o cliente solicita recursos e o servidor processa e responde.

## GitFlow simplificado sugerido

- `main`: versao final estavel.
- `develop`: integracao das funcionalidades.
- `feat/pipeline-dados`: leitura, limpeza, transformacao e metricas.
- `feat/visualizacoes`: graficos e exportacoes.
- `docs/readme`: documentacao e checklist final.

## Video de demonstracao

Insira aqui o link do Google Drive ou YouTube nao listado apos gravar o video de ate 5 minutos.

## Checklist final

- [x] Criar arquivo `salesinsight.py`
- [x] Criar notebook `salesinsight.ipynb`
- [x] Gerar ou incluir `vendas.csv`
- [x] Inspecionar dados com shape, tipos e nulos
- [x] Limpar nulos, datas invalidas e strings sujas
- [x] Usar regex para limpeza de clientes
- [x] Criar colunas derivadas
- [x] Calcular metricas com `groupby`
- [x] Segmentar clientes com lambda
- [x] Usar NumPy com vetorizacao e broadcasting
- [x] Criar classe, metodos, atributos e heranca
- [x] Exportar CSV, JSON e PNG
- [ ] Criar repositorio publico no GitHub
- [ ] Criar quadro Kanban online ou anexar o Markdown
- [ ] Fazer commits e branches descritivas
- [ ] Gravar video de demonstracao
- [ ] Enviar links no AVA
