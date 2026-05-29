# =========================================================
# CASE TÉCNICO - CITRUS ANALYTICS
# TRANSFORMAÇÃO DA TABELA FATO
#
# Objetivo:
# - Ler a base de produção
# - Tratar inconsistências
# - Calcular produtividade
# - Integrar com a dimensão de municípios
# - Identificar municípios sem correspondência
# - Gerar a tabela fato_producao
# =========================================================

# =========================================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# =========================================================

import pandas as pd
import numpy as np
from pathlib import Path

# =========================================================
# CONFIGURAÇÕES
# =========================================================

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================
# LEITURA DOS ARQUIVOS
# =========================================================

print("Lendo arquivos...")

df = pd.read_csv(
    BASE_DIR / "data" / "producao_citros_bruto.csv"
)

df_municipios = pd.read_csv(
    BASE_DIR / "data" / "dim_municipio.csv"
)

print(f"Registros produção: {df.shape[0]}")
print(f"Municípios IBGE: {df_municipios.shape[0]}")

# =========================================================
# PADRONIZAÇÃO DOS MUNICÍPIOS
# =========================================================

print("\nPadronizando municípios...")

df["municipio"] = (
    df["municipio"]
    .astype(str)
    .str.strip()
    .str.title()
)

df_municipios["nome_municipio"] = (
    df_municipios["nome_municipio"]
    .astype(str)
    .str.strip()
    .str.title()
)

# =========================================================
# TRATAMENTO DE VALORES INVÁLIDOS
# =========================================================

print("Tratando valores inválidos...")

df = df.replace("-", np.nan)

# =========================================================
# CONVERSÃO DE COLUNAS NUMÉRICAS
# =========================================================

colunas_numericas = [
    "qtd_produzida_ton",
    "area_colhida_ha",
    "valor_producao_reais"
]

for coluna in colunas_numericas:

    df[coluna] = pd.to_numeric(
        df[coluna],
        errors="coerce"
    )

# =========================================================
# REMOÇÃO DE REGISTROS INVÁLIDOS
# =========================================================

print("Removendo registros inválidos...")

df = df[
    (df["qtd_produzida_ton"] > 0) &
    (df["area_colhida_ha"] > 0)
]

print(f"Registros válidos: {df.shape[0]}")

# =========================================================
# CÁLCULO DA PRODUTIVIDADE
# =========================================================

print("Calculando produtividade...")

df["produtividade_ton_ha"] = (
    df["qtd_produzida_ton"] /
    df["area_colhida_ha"]
)

# =========================================================
# INTEGRAÇÃO COM DIMENSÃO DE MUNICÍPIOS
# =========================================================

print("Integrando com dimensão IBGE...")

df_final = df.merge(
    df_municipios[
        [
            "cod_municipio_ibge",
            "nome_municipio",
            "uf"
        ]
    ],
    left_on=["municipio", "uf"],
    right_on=["nome_municipio", "uf"],
    how="left"
)

# =========================================================
# CORREÇÃO AUTOMÁTICA DE MUNICÍPIOS NÃO LOCALIZADOS
#
# Objetivo:
# Corrigir divergências entre a base de origem e a
# dimensão do IBGE utilizando apenas o nome do
# município quando o match por município + UF falhar.
# =========================================================

print("\nAplicando correções automáticas...")

sem_match = df_final[
    df_final["cod_municipio_ibge"].isna()
].copy()

print(
    f"Registros sem correspondência encontrados: "
    f"{sem_match.shape[0]}"
)

correcoes = []

for idx, row in sem_match.iterrows():

    municipio = row["municipio"]

    match_ibge = df_municipios[
        df_municipios["nome_municipio"] == municipio
    ]

    if len(match_ibge) == 1:

        registro = match_ibge.iloc[0]

        df_final.loc[idx, "cod_municipio_ibge"] = (
            registro["cod_municipio_ibge"]
        )

        df_final.loc[idx, "uf"] = (
            registro["uf"]
        )

        correcoes.append({

            "municipio": municipio,

            "uf_original": row["uf"],

            "uf_corrigida": registro["uf"],

            "cod_municipio_ibge": (
                registro["cod_municipio_ibge"]
            )
        })

# =========================================================
# LOG DAS CORREÇÕES
# =========================================================

df_correcoes = pd.DataFrame(correcoes)

print(
    f"\nCorreções automáticas realizadas: "
    f"{len(df_correcoes)}"
)

if len(df_correcoes) > 0:

    print("\nCorreções aplicadas:\n")

    print(
        df_correcoes
        .drop_duplicates()
        .to_string(index=False)
    )

    df_correcoes.to_csv(
        BASE_DIR / "data" / "LOGs" / "LOG_correcoes_municipios.csv",
        index=False
    )

# =========================================================
# VALIDAÇÃO FINAL DOS MUNICÍPIOS
# =========================================================

municipios_sem_match = (
    df_final[
        df_final["cod_municipio_ibge"].isna()
    ][["municipio", "uf"]]
    .drop_duplicates()
    .sort_values(["uf", "municipio"])
)

print("\n===================================")
print("MUNICÍPIOS SEM CORRESPONDÊNCIA")
print("===================================\n")

print(municipios_sem_match)

print(
    f"\nTotal de municípios sem correspondência: "
    f"{municipios_sem_match.shape[0]}"
)

municipios_sem_match.to_csv(
    BASE_DIR / "data" / "LOGs" / "LOG_municipios_sem_match.csv",
    index=False
)

print(
    f"\nRegistros sem código IBGE após correção: "
    f"{df_final['cod_municipio_ibge'].isna().sum()}"
)

# =========================================================
# CRIAÇÃO DA TABELA FATO
# =========================================================

print("\nCriando tabela fato...")

fato_producao = df_final[
    [
        "cod_municipio_ibge",
        "cod_produto",
        "ano",
        "qtd_produzida_ton",
        "area_colhida_ha",
        "valor_producao_reais",
        "produtividade_ton_ha"
    ]
]

# =========================================================
# VALIDAÇÃO FINAL
# =========================================================

print("\nInformações da tabela fato:\n")

print(fato_producao.info())

print("\nRegistros com código IBGE nulo:")

print(
    fato_producao["cod_municipio_ibge"]
    .isna()
    .sum()
)

# =========================================================
# EXPORTAÇÃO
# =========================================================

print("\nExportando tabela fato...")

fato_producao.to_csv(
    BASE_DIR / "data" / "fato_producao.csv",
    index=False
)

print("Arquivo fato_producao.csv salvo com sucesso!")

# =========================================================
# FINALIZAÇÃO
# =========================================================

print("\nProcesso finalizado com sucesso!")
