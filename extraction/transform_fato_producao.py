# =========================================================
# CASE TÉCNICO - CITRUS ANALYTICS
# LIMPEZA E TRANSFORMAÇÃO DOS DADOS
#
# Objetivo:
# - Ler o dataset bruto
# - Tratar inconsistências
# - Padronizar os dados
# - Criar métrica de produtividade
# - Gerar tabela fato_producao
# =========================================================

# =========================================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# =========================================================

import pandas as pd
import numpy as np

# =========================================================
# CONFIGURAÇÕES DO PANDAS
# =========================================================

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

# =========================================================
# LEITURA DO DATASET BRUTO
# =========================================================

print('Lendo dataset bruto...')

df = pd.read_csv('../data/producao_citros_bruto.csv')

print(f'Registros originais: {df.shape[0]}')

# =========================================================
# ANÁLISE INICIAL DO DATASET
# =========================================================

print('\nInformações iniciais do dataset:\n')

print(df.info())

# =========================================================
# PADRONIZAÇÃO DOS MUNICÍPIOS
#
# Objetivo:
# Corrigir inconsistências de capitalização
# para facilitar futuras integrações.
# =========================================================

print('\nPadronizando municípios...')

df['municipio'] = (
    df['municipio']
    .str.strip()
    .str.title()
)

# =========================================================
# TRATAMENTO DE VALORES INVÁLIDOS
#
# Objetivo:
# Converter valores "-" para NaN.
# =========================================================

print('Tratando valores inválidos...')

df = df.replace('-', np.nan)

# =========================================================
# CONVERSÃO DAS COLUNAS NUMÉRICAS
#
# Objetivo:
# Garantir consistência para cálculos
# e análises posteriores.
# =========================================================

colunas_numericas = [
    'qtd_produzida_ton',
    'area_colhida_ha',
    'valor_producao_reais'
]

for coluna in colunas_numericas:

    df[coluna] = pd.to_numeric(
        df[coluna],
        errors='coerce'
    )

# =========================================================
# IDENTIFICAÇÃO DE REGISTROS INVÁLIDOS
#
# Regras:
# - Produção maior que zero
# - Área colhida maior que zero
# =========================================================

print('\nIdentificando registros inválidos...')

registros_invalidos = df[
    (df['qtd_produzida_ton'] <= 0) |
    (df['area_colhida_ha'] <= 0)
]

print(
    f'Registros inválidos encontrados: '
    f'{registros_invalidos.shape[0]}'
)

# =========================================================
# REMOÇÃO DE REGISTROS INVÁLIDOS
# =========================================================

print('Removendo registros inválidos...')

df = df[
    (df['qtd_produzida_ton'] > 0) &
    (df['area_colhida_ha'] > 0)
]

print(f'Registros válidos finais: {df.shape[0]}')

# =========================================================
# CRIAÇÃO DA MÉTRICA DE PRODUTIVIDADE
#
# Fórmula:
# produtividade = produção / área colhida
# =========================================================

print('\nCalculando produtividade...')

df['produtividade_ton_ha'] = (
    df['qtd_produzida_ton'] /
    df['area_colhida_ha']
)

# =========================================================
# CRIAÇÃO DA TABELA FATO
#
# Granularidade:
# Uma linha por:
# - município
# - produto
# - ano
# =========================================================

print('Criando tabela fato_producao...')

fato_producao = df[[

    'cod_produto',

    'ano',

    'uf',

    'estado',

    'municipio',

    'qtd_produzida_ton',

    'area_colhida_ha',

    'valor_producao_reais',

    'produtividade_ton_ha'
]]

# =========================================================
# VALIDAÇÃO FINAL DA TABELA FATO
# =========================================================

print('\nInformações da tabela fato:\n')

print(fato_producao.info())

# =========================================================
# EXPORTAÇÃO DO CSV FINAL
# =========================================================

print('\nExportando tabela fato...')

fato_producao.to_csv(
    '../data/fato_producao.csv',
    index=False
)

print('Arquivo fato_producao.csv salvo com sucesso!')

# =========================================================
# FINALIZAÇÃO
# =========================================================

print('\nProcesso de limpeza finalizado com sucesso!')
