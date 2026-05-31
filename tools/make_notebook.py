"""Gera o notebook Jupyter a partir do script principal."""

from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
SCRIPT_PATH = BASE_DIR / "salesinsight.py"
NOTEBOOK_PATH = BASE_DIR / "salesinsight.ipynb"


def code_cell(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def markdown_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }


def main() -> None:
    codigo = SCRIPT_PATH.read_text(encoding="utf-8")
    codigo_sem_main = codigo.replace('if __name__ == "__main__":\n    main()\n', "")

    notebook = {
        "cells": [
            markdown_cell(
                "# SalesInsight PY\n\n"
                "Notebook do mini-projeto avaliativo. Execute as celulas em ordem para gerar o dataset, "
                "limpar os dados, calcular metricas, criar visualizacoes e exportar os relatorios."
            ),
            markdown_cell("## Codigo do pipeline\n\nAs funcoes e classes abaixo sao as mesmas do arquivo `salesinsight.py`."),
            code_cell(codigo_sem_main),
            markdown_cell("## Execucao completa\n\nEsta celula roda o pipeline de ponta a ponta."),
            code_cell("main()"),
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.10",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    NOTEBOOK_PATH.write_text(json.dumps(notebook, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
