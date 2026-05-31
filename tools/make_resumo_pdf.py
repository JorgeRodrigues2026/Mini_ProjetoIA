"""Gera o arquivo Resumo.PDF com as informacoes principais do projeto."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


BASE_DIR = Path(__file__).resolve().parents[1]
PDF_PATH = BASE_DIR / "Resumo.PDF"


def paragraph(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text.replace("\n", "<br/>"), style)


def main() -> None:
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="TituloProjeto",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#1F4E5F"),
            spaceAfter=16,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Secao",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#2E4057"),
            spaceBefore=10,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Texto",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Codigo",
            parent=styles["Code"],
            fontName="Courier",
            fontSize=9,
            leading=12,
            backColor=colors.HexColor("#F4F6F8"),
            borderColor=colors.HexColor("#D7DEE6"),
            borderWidth=0.5,
            borderPadding=6,
            spaceBefore=4,
            spaceAfter=8,
        )
    )

    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title="Resumo - SalesInsight PY",
        author="Codex",
    )

    story = []
    story.append(paragraph("Resumo do Projeto - SalesInsight PY", styles["TituloProjeto"]))
    story.append(
        paragraph(
            "Projeto montado em C:\\Users\\User\\Documents\\Projeto_Estudos\\salesinsight-py. "
            "O objetivo e entregar um pipeline de analise e visualizacao de dados de vendas para o "
            "mini-projeto avaliativo do Modulo 1.",
            styles["Texto"],
        )
    )

    story.append(paragraph("Arquivos principais criados", styles["Secao"]))
    arquivos = [
        ["Arquivo", "Descricao"],
        ["salesinsight.py", "Script principal do pipeline."],
        ["salesinsight.ipynb", "Notebook Jupyter para executar no VS Code, Jupyter ou Colab."],
        ["README.md", "Documentacao com objetivo, execucao, conceitos e checklist."],
        ["requirements.txt", "Dependencias: pandas, numpy, matplotlib e seaborn."],
        ["vendas.csv", "Dataset sintetico de vendas usado pelo projeto."],
        ["planejamento/tarefas-kanban.md", "Quadro Kanban em Markdown."],
        ["outputs/", "Relatorios CSV, estatisticas JSON e graficos PNG."],
    ]
    tabela = Table(arquivos, colWidths=[5.2 * cm, 9.2 * cm])
    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E5F")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C7D0D9")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F9FB")]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(tabela)
    story.append(Spacer(1, 8))

    story.append(paragraph("Funcionalidades implementadas", styles["Secao"]))
    story.append(
        paragraph(
            "- Geracao e leitura do dataset vendas.csv.<br/>"
            "- Inspecao inicial com shape, colunas, tipos, nulos e estatisticas.<br/>"
            "- Limpeza de nulos, datas invalidas e strings com espacos extras.<br/>"
            "- Uso de expressoes regulares para limpar e validar clientes.<br/>"
            "- Criacao de colunas derivadas: receita_total, mes, mes_nome, trimestre, ano e faixa_receita_item.<br/>"
            "- Metricas agregadas com groupby por mes, produto, categoria e regiao.<br/>"
            "- Segmentacao de clientes em Bronze, Prata e Ouro com lambda.<br/>"
            "- Estatisticas com NumPy, operacoes vetorizadas e broadcasting.<br/>"
            "- Visualizacoes com Matplotlib e Seaborn exportadas em PNG.<br/>"
            "- Programacao orientada a objetos com AnalisadorDeVendas.<br/>"
            "- Heranca com AnalisadorComProjecao e uso de super().<br/>"
            "- Exportacao de relatorios CSV e estatisticas JSON.",
            styles["Texto"],
        )
    )

    story.append(paragraph("Como abrir no VS Code", styles["Secao"]))
    story.append(paragraph("cd C:\\Users\\User\\Documents\\Projeto_Estudos\\salesinsight-py\ncode .", styles["Codigo"]))

    story.append(paragraph("Como executar", styles["Secao"]))
    story.append(paragraph("pip install -r requirements.txt\npython salesinsight.py", styles["Codigo"]))

    story.append(paragraph("Como executar no Jupyter Notebook", styles["Secao"]))
    story.append(
        paragraph(
            "Abra o arquivo salesinsight.ipynb no VS Code, Jupyter Notebook ou Google Colab e execute as celulas em ordem. "
            "A ultima celula chama main() e roda o pipeline completo.",
            styles["Texto"],
        )
    )

    story.append(paragraph("Validacao realizada", styles["Secao"]))
    story.append(
        paragraph(
            "O pipeline foi executado com sucesso. Resultado final exibido: 218 vendas analisadas, "
            "receita total de R$ 1.608.604,60, 7 produtos unicos e 49 clientes unicos. "
            "Foram gerados relatorios CSV, um arquivo JSON e quatro graficos PNG.",
            styles["Texto"],
        )
    )

    story.append(paragraph("Outputs gerados", styles["Secao"]))
    story.append(
        paragraph(
            "- outputs/metricas_por_mes.csv<br/>"
            "- outputs/projecao_receita.csv<br/>"
            "- outputs/receita_por_categoria.csv<br/>"
            "- outputs/receita_por_regiao.csv<br/>"
            "- outputs/segmentacao_clientes.csv<br/>"
            "- outputs/top_produtos.csv<br/>"
            "- outputs/estatisticas_gerais.json<br/>"
            "- outputs/graficos/vendas_por_mes.png<br/>"
            "- outputs/graficos/top_produtos.png<br/>"
            "- outputs/graficos/distribuicao_regioes.png<br/>"
            "- outputs/graficos/boxplot_categorias.png",
            styles["Texto"],
        )
    )

    story.append(paragraph("Pendencias para entrega no AVA", styles["Secao"]))
    story.append(
        paragraph(
            "- Criar repositorio publico no GitHub.<br/>"
            "- Criar ou publicar o quadro Kanban online, caso o professor exija link externo.<br/>"
            "- Fazer commits e branches descritivas.<br/>"
            "- Gravar video de ate 5 minutos demonstrando o projeto.<br/>"
            "- Enviar no AVA os links do GitHub, Kanban e video.",
            styles["Texto"],
        )
    )

    doc.build(story)
    print(PDF_PATH)


if __name__ == "__main__":
    main()
