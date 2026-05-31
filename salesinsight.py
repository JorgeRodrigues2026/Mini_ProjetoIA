"""SalesInsight PY: pipeline de analise e visualizacao de vendas."""

from __future__ import annotations

import json
import os
import random
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd().resolve()



OUTPUTS_DIR = BASE_DIR / "outputs"
GRAFICOS_DIR = OUTPUTS_DIR / "graficos"

OUTPUTS_DIR.mkdir(parents=True, exist_ok=True) # Assim as pastas são criadas automaticamente caso não existam
GRAFICOS_DIR.mkdir(parents=True, exist_ok=True) # Assim as pastas são criadas automaticamente caso não existam

os.environ.setdefault("MPLCONFIGDIR", str(OUTPUTS_DIR / ".matplotlib"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


CAMINHO_DADOS = BASE_DIR / "vendas.csv"


def gerar_dataset_vendas(n_registros: int = 200, seed: int = 42) -> pd.DataFrame:
    """Gera um dataset sintetico de vendas com pequenas inconsistencias."""
    random.seed(seed)
    np.random.seed(seed)

    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor", "Teclado", "Mouse", "Headset"]
    categorias = {
        "Notebook": "Computadores",
        "Smartphone": "Celulares",
        "Tablet": "Celulares",
        "Monitor": "Computadores",
        "Teclado": "Perifericos",
        "Mouse": "Perifericos",
        "Headset": "Perifericos",
    }
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    clientes = [f"Cliente_{i:03d}" for i in range(1, 51)]
    precos_base = {
        "Notebook": 3500,
        "Smartphone": 2200,
        "Tablet": 1800,
        "Monitor": 1200,
        "Teclado": 250,
        "Mouse": 120,
        "Headset": 350,
    }

    data_inicio = datetime(2024, 1, 1)
    dados = []

    for i in range(n_registros):
        produto = random.choice(produtos)
        quantidade = random.randint(1, 10)
        preco = round(precos_base[produto] * random.uniform(0.85, 1.15), 2)
        data = data_inicio + timedelta(days=random.randint(0, 364))
        cliente = random.choice(clientes)

        if random.random() < 0.05:
            quantidade = None
        if random.random() < 0.04:
            preco = None
        if random.random() < 0.03:
            produto = "  " + produto
        if random.random() < 0.03:
            cliente = cliente + "#"

        dados.append(
            {
                "id_venda": i + 1,
                "data_venda": data.strftime("%Y-%m-%d") if random.random() > 0.02 else "DATA INVALIDA",
                "cliente": cliente,
                "produto": produto,
                "categoria": categorias.get(produto.strip(), "Outros"),
                "regiao": random.choice(regioes),
                "quantidade": quantidade,
                "preco_unitario": preco,
            }
        )

    return pd.DataFrame(dados)


def inspecionar_dados(df: pd.DataFrame) -> None:
    """Exibe informacoes basicas do DataFrame."""
    print("\n=== INSPECAO INICIAL DO DATASET ===")
    print(f"Shape: {df.shape}")
    print(f"\nColunas: {list(df.columns)}")
    print(f"\nTipos de dados:\n{df.dtypes}")
    print(f"\nValores nulos por coluna:\n{df.isnull().sum()}")
    print(f"\nPrimeiros registros:\n{df.head()}")
    print(f"\nEstatisticas descritivas:\n{df.describe(include='all')}")


def limpar_dados(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Limpa o DataFrame, remove dados invalidos e retorna um relatorio."""
    df = df.copy()
    n_inicial = len(df)
    relatorio: dict[str, int] = {}

    colunas_texto = df.select_dtypes(include=["object", "string"]).columns
    for coluna in colunas_texto:
        df[coluna] = df[coluna].astype(str).str.strip()

    df["data_venda"] = pd.to_datetime(df["data_venda"], errors="coerce")
    n_datas_invalidas = int(df["data_venda"].isna().sum())
    df = df.dropna(subset=["data_venda"])
    relatorio["datas_invalidas_removidas"] = n_datas_invalidas

    n_antes_nulos = len(df)
    df = df.dropna(subset=["quantidade", "preco_unitario"])
    relatorio["linhas_nulas_removidas"] = n_antes_nulos - len(df)

    df["quantidade"] = df["quantidade"].astype(int)
    df["preco_unitario"] = df["preco_unitario"].astype(float)

    relatorio["registros_iniciais"] = n_inicial
    relatorio["registros_finais"] = len(df)
    relatorio["registros_removidos_total"] = n_inicial - len(df)

    print("\n=== RELATORIO DE LIMPEZA ===")
    for chave, valor in relatorio.items():
        print(f"  {chave}: {valor}")

    return df.reset_index(drop=True), relatorio


def limpar_strings_com_regex(df: pd.DataFrame) -> pd.DataFrame:
    """Usa regex para limpar clientes e validar o padrao Cliente_XXX."""
    df = df.copy()
    df["cliente_limpo"] = df["cliente"].apply(lambda s: re.sub(r"[^a-zA-Z0-9_ ]", "", str(s)).strip())

    padrao_cliente = re.compile(r"^Cliente_\d{3}$")
    df["cliente_valido"] = df["cliente_limpo"].apply(lambda s: bool(padrao_cliente.match(s)))

    n_invalidos = int((~df["cliente_valido"]).sum())
    print("\n=== LIMPEZA COM REGEX ===")
    print(f"  Clientes com formato invalido encontrados: {n_invalidos}")
    print(f"  Amostra de clientes limpos: {df['cliente_limpo'].head(5).tolist()}")
    return df


def criar_colunas_derivadas(df: pd.DataFrame) -> pd.DataFrame:
    """Cria colunas de receita, data e classificacao condicional."""
    df = df.copy()
    df["receita_total"] = df["quantidade"] * df["preco_unitario"]
    df["mes"] = df["data_venda"].dt.month
    df["mes_nome"] = df["data_venda"].dt.strftime("%B")
    df["trimestre"] = df["data_venda"].dt.quarter.apply(lambda trimestre: f"Q{trimestre}")
    df["ano"] = df["data_venda"].dt.year

    condicoes = [
        df["receita_total"] < 500,
        (df["receita_total"] >= 500) & (df["receita_total"] < 5000),
        df["receita_total"] >= 5000,
    ]
    classificacoes = ["Baixo Valor", "Medio Valor", "Alto Valor"]
    df["faixa_receita_item"] = np.select(condicoes, classificacoes, default="Nao Classificado")

    print("\n=== COLUNAS DERIVADAS CRIADAS ===")
    print(df[["data_venda", "receita_total", "mes", "trimestre", "faixa_receita_item"]].head())
    return df


def calcular_metricas(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Calcula metricas agregadas com groupby."""
    metricas: dict[str, pd.DataFrame] = {}

    metricas["por_mes"] = (
        df.groupby("mes")
        .agg(receita_total=("receita_total", "sum"), quantidade=("quantidade", "sum"), n_vendas=("id_venda", "count"))
        .reset_index()
        .sort_values("mes")
    )

    metricas["top_produtos"] = (
        df.groupby("produto")["receita_total"].sum().sort_values(ascending=False).head(5).reset_index()
    )

    metricas["por_categoria"] = (
        df.groupby("categoria")["receita_total"].sum().reset_index().sort_values("receita_total", ascending=False)
    )

    metricas["por_regiao"] = (
        df.groupby("regiao")
        .agg(receita_total=("receita_total", "sum"), media_ticket=("receita_total", "mean"))
        .reset_index()
        .sort_values("receita_total", ascending=False)
    )

    for nome, tabela in metricas.items():
        print(f"\n=== {nome.upper().replace('_', ' ')} ===")
        print(tabela.to_string(index=False))

    return metricas


def segmentar_clientes(df: pd.DataFrame) -> pd.DataFrame:
    """Segmenta clientes pelo gasto total usando lambda."""
    clientes = df.groupby("cliente_limpo")["receita_total"].sum().reset_index()
    clientes.columns = ["cliente", "total_gasto"]
    clientes["segmento"] = clientes["total_gasto"].apply(
        lambda gasto: "Ouro" if gasto > 15000 else ("Prata" if gasto >= 5000 else "Bronze")
    )
    clientes = clientes.sort_values("total_gasto", ascending=False)

    print("\n=== SEGMENTACAO DE CLIENTES ===")
    print(clientes.head(10).to_string(index=False))
    print(f"\nDistribuicao de segmentos:\n{clientes['segmento'].value_counts()}")
    return clientes


def calcular_estatisticas_numpy(df: pd.DataFrame) -> dict[str, float]:
    """Calcula estatisticas com NumPy e demonstra broadcasting."""
    print("\n=== ESTATISTICAS COM NUMPY ===")
    receitas = df["receita_total"].to_numpy()
    quantidades = df["quantidade"].to_numpy()
    ticket_unitario_estimado = receitas / quantidades

    denominador = np.max(receitas) - np.min(receitas)
    receitas_normalizadas = (receitas - np.min(receitas)) / denominador

    estatisticas = {
        "media": np.mean(receitas),
        "mediana": np.median(receitas),
        "desvio_padrao": np.std(receitas),
        "total": np.sum(receitas),
        "percentil_25": np.percentile(receitas, 25),
        "percentil_75": np.percentile(receitas, 75),
        "media_ticket_unitario_estimado": np.mean(ticket_unitario_estimado),
        "media_receita_normalizada": np.mean(receitas_normalizadas),
    }

    for chave, valor in estatisticas.items():
        print(f"  {chave}: R$ {valor:.2f}" if "normalizada" not in chave else f"  {chave}: {valor:.4f}")

    return {chave: float(valor) for chave, valor in estatisticas.items()}


def processar_coluna(df: pd.DataFrame, coluna: str, funcao: Callable[[object], object]) -> pd.Series:
    """Funcao de ordem superior: recebe uma funcao e aplica a uma coluna."""
    return df[coluna].apply(funcao)


def gerar_visualizacoes(metricas: dict[str, pd.DataFrame], df: pd.DataFrame) -> None:
    """Gera e salva graficos em PNG."""
    GRAFICOS_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=metricas["por_mes"], x="mes", y="receita_total", marker="o", color="#246B73")
    plt.title("Receita total por mes")
    plt.xlabel("Mes")
    plt.ylabel("Receita total (R$)")
    plt.tight_layout()
    plt.savefig(GRAFICOS_DIR / "vendas_por_mes.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 5))
    sns.barplot(data=metricas["top_produtos"], x="receita_total", y="produto", palette="viridis", hue="produto", legend=False)
    plt.title("Top 5 produtos por receita")
    plt.xlabel("Receita total (R$)")
    plt.ylabel("Produto")
    plt.tight_layout()
    plt.savefig(GRAFICOS_DIR / "top_produtos.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 5))
    sns.barplot(data=metricas["por_regiao"], x="regiao", y="receita_total", palette="mako", hue="regiao", legend=False)
    plt.title("Receita total por regiao")
    plt.xlabel("Regiao")
    plt.ylabel("Receita total (R$)")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(GRAFICOS_DIR / "distribuicao_regioes.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 5))
    sns.boxplot(data=df, x="categoria", y="receita_total", hue="categoria", palette="Set2", legend=False)
    plt.title("Distribuicao de receita por categoria")
    plt.xlabel("Categoria")
    plt.ylabel("Receita total (R$)")
    plt.tight_layout()
    plt.savefig(GRAFICOS_DIR / "boxplot_categorias.png", dpi=160)
    plt.close()

    print("\n=== GRAFICOS EXPORTADOS ===")
    for arquivo in sorted(GRAFICOS_DIR.glob("*.png")):
        print(f"  {arquivo.relative_to(BASE_DIR)}")


def exportar_resultados(
    metricas: dict[str, pd.DataFrame],
    clientes: pd.DataFrame,
    stats_numpy: dict[str, float],
    projecao: pd.DataFrame | None = None,
) -> None:
    """Exporta resultados em CSV e JSON e confirma leitura do JSON."""
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    metricas["por_mes"].to_csv(OUTPUTS_DIR / "metricas_por_mes.csv", index=False, encoding="utf-8-sig")
    metricas["top_produtos"].to_csv(OUTPUTS_DIR / "top_produtos.csv", index=False, encoding="utf-8-sig")
    metricas["por_categoria"].to_csv(OUTPUTS_DIR / "receita_por_categoria.csv", index=False, encoding="utf-8-sig")
    metricas["por_regiao"].to_csv(OUTPUTS_DIR / "receita_por_regiao.csv", index=False, encoding="utf-8-sig")
    clientes.to_csv(OUTPUTS_DIR / "segmentacao_clientes.csv", index=False, encoding="utf-8-sig")

    if projecao is not None:
        projecao.to_csv(OUTPUTS_DIR / "projecao_receita.csv", index=False, encoding="utf-8-sig")

    caminho_json = OUTPUTS_DIR / "estatisticas_gerais.json"
    with caminho_json.open("w", encoding="utf-8") as arquivo:
        json.dump({k: round(v, 2) for k, v in stats_numpy.items()}, arquivo, indent=4, ensure_ascii=False)

    with caminho_json.open("r", encoding="utf-8") as arquivo:
        dados_lidos = json.load(arquivo)

    print("\n=== ARQUIVOS EXPORTADOS ===")
    for arquivo in sorted(OUTPUTS_DIR.glob("*.csv")):
        print(f"  CSV: {arquivo.relative_to(BASE_DIR)}")
    print(f"  JSON: {caminho_json.relative_to(BASE_DIR)}")
    print(f"  Conteudo do JSON lido: {json.dumps(dados_lidos, ensure_ascii=False)}")


class AnalisadorDeVendas:
    """Pipeline orientado a objetos para analise de vendas."""

    def __init__(self, caminho_csv: str | Path):
        self.caminho_csv = Path(caminho_csv)
        self.df_bruto: pd.DataFrame | None = None
        self.df_limpo: pd.DataFrame | None = None
        self.metricas: dict[str, pd.DataFrame] = {}
        self.clientes: pd.DataFrame | None = None
        self.relatorio_limpeza: dict[str, int] = {}

    def carregar(self) -> "AnalisadorDeVendas":
        self.df_bruto = pd.read_csv(self.caminho_csv)
        inspecionar_dados(self.df_bruto)
        return self

    def limpar(self) -> "AnalisadorDeVendas":
        self._validar_df_bruto()
        self.df_limpo, self.relatorio_limpeza = limpar_dados(self.df_bruto)
        self.df_limpo = limpar_strings_com_regex(self.df_limpo)
        return self

    def transformar(self) -> "AnalisadorDeVendas":
        self._validar_df_limpo()
        self.df_limpo = criar_colunas_derivadas(self.df_limpo)
        self.df_limpo["produto_maiusculo"] = processar_coluna(self.df_limpo, "produto", lambda valor: str(valor).upper())
        return self

    def analisar(self) -> "AnalisadorDeVendas":
        self._validar_df_limpo()
        self.metricas = calcular_metricas(self.df_limpo)
        self.clientes = segmentar_clientes(self.df_limpo)
        return self

    def visualizar(self) -> "AnalisadorDeVendas":
        self._validar_df_limpo()
        gerar_visualizacoes(self.metricas, self.df_limpo)
        return self

    def exportar_relatorio(self) -> "AnalisadorDeVendas":
        self._validar_df_limpo()
        stats = calcular_estatisticas_numpy(self.df_limpo)
        exportar_resultados(self.metricas, self.clientes, stats)
        return self

    def resumo(self) -> None:
        self._validar_df_limpo()
        receita_total = self.df_limpo["receita_total"].sum()
        print("\n=== RESUMO FINAL ===")
        print(f"  Vendas analisadas: {len(self.df_limpo)}")
        print(f"  Receita total: R$ {receita_total:,.2f}")
        print(f"  Produtos unicos: {self.df_limpo['produto'].nunique()}")
        print(f"  Clientes unicos: {self.df_limpo['cliente_limpo'].nunique()}")

    def _validar_df_bruto(self) -> None:
        if self.df_bruto is None:
            raise ValueError("Carregue os dados antes de continuar.")

    def _validar_df_limpo(self) -> None:
        if self.df_limpo is None:
            raise ValueError("Limpe os dados antes de continuar.")


class AnalisadorComProjecao(AnalisadorDeVendas):
    """Estende o analisador com uma projecao simples de tendencia."""

    def __init__(self, caminho_csv: str | Path, meses_projecao: int = 3):
        super().__init__(caminho_csv)
        self.meses_projecao = meses_projecao
        self.projecao: pd.DataFrame | None = None

    def projetar_tendencia(self) -> "AnalisadorComProjecao":
        if "por_mes" not in self.metricas:
            raise ValueError("Calcule as metricas antes de projetar tendencia.")

        por_mes = self.metricas["por_mes"].sort_values("mes")
        x = por_mes["mes"].to_numpy()
        y = por_mes["receita_total"].to_numpy()
        coeficiente_angular, intercepto = np.polyfit(x, y, 1)

        ultimo_mes = int(x.max())
        meses_futuros = np.arange(ultimo_mes + 1, ultimo_mes + self.meses_projecao + 1)
        receitas_previstas = coeficiente_angular * meses_futuros + intercepto
        receitas_previstas = np.maximum(receitas_previstas, 0)

        self.projecao = pd.DataFrame(
            {
                "mes_projetado": meses_futuros,
                "receita_prevista": receitas_previstas.round(2),
            }
        )

        print("\n=== PROJECAO SIMPLES DE TENDENCIA ===")
        print(self.projecao.to_string(index=False))
        return self

    def exportar_relatorio(self) -> "AnalisadorComProjecao":
        self._validar_df_limpo()
        stats = calcular_estatisticas_numpy(self.df_limpo)
        exportar_resultados(self.metricas, self.clientes, stats, self.projecao)
        return self

    def exibir_projecao_detalhada(self) -> None:
        if self.projecao is None:
            print("\nNenhuma projecao calculada.")
            return
        print("\n=== PROJECAO DETALHADA ===")
        for _, linha in self.projecao.iterrows():
            print(f"  Mes {int(linha['mes_projetado'])}: R$ {linha['receita_prevista']:,.2f}")


def preparar_dataset(caminho_csv: Path = CAMINHO_DADOS) -> None:
    """Gera vendas.csv quando o arquivo ainda nao existe."""
    if caminho_csv.exists():
        print(f"\n[INFO] Dataset encontrado: {caminho_csv.name}")
        return

    print("\n[INFO] Gerando dataset sintetico...")
    df_gerado = gerar_dataset_vendas(n_registros=240)
    df_gerado.to_csv(caminho_csv, index=False, encoding="utf-8-sig")
    print(f"[INFO] Dataset gerado com {len(df_gerado)} registros em {caminho_csv.name}.")


def main() -> None:
    """Executa o pipeline completo."""
    print("\n" + "=" * 64)
    print("   SALESINSIGHT PY - Pipeline de Analise de Dados de Vendas")
    print("=" * 64)

    preparar_dataset()
    analisador = AnalisadorComProjecao(CAMINHO_DADOS, meses_projecao=3)
    (
        analisador.carregar()
        .limpar()
        .transformar()
        .analisar()
        .projetar_tendencia()
        .visualizar()
        .exportar_relatorio()
    )
    analisador.resumo()
    analisador.exibir_projecao_detalhada()

    print("\n[CONCLUIDO] Pipeline finalizado com sucesso!")


if __name__ == "__main__":
    main()
