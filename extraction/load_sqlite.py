# =========================================================
# CASE TÉCNICO - CITRUS ANALYTICS
# CARGA DOS DADOS NO SQLITE
#
# Objetivo:
# Carregar os datasets tratados no banco SQLite
# para construção do modelo analítico final.
# =========================================================


# =========================================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# =========================================================

import pandas as pd
import sqlite3


# =========================================================
# CONEXÃO COM O BANCO SQLITE
# =========================================================

conn = sqlite3.connect('../sql/case_citrus.db')


# =========================================================
# LEITURA DOS CSVs
# =========================================================

df_dim = pd.read_csv('../data/dim_municipio.csv')

df_fato = pd.read_csv('../data/fato_producao.csv')


# =========================================================
# CARGA DA DIMENSÃO DE MUNICÍPIOS
# =========================================================

df_dim.to_sql(
    'dim_municipio',
    conn,
    if_exists='append',
    index=False
)

print('Dimensão de municípios carregada com sucesso!')


# =========================================================
# CARGA DA TABELA FATO
# =========================================================

df_fato.to_sql(
    'fato_producao',
    conn,
    if_exists='append',
    index=False
)

print('Tabela fato carregada com sucesso!')


# =========================================================
# VALIDAÇÃO DAS CARGAS
# =========================================================

cursor = conn.cursor()

# Quantidade de municípios
cursor.execute(
    'SELECT COUNT(*) FROM dim_municipio'
)

print(
    f'Registros dim_municipio: '
    f'{cursor.fetchone()[0]}'
)

# Quantidade de registros da fato
cursor.execute(
    'SELECT COUNT(*) FROM fato_producao'
)

print(
    f'Registros fato_producao: '
    f'{cursor.fetchone()[0]}'
)


# =========================================================
# FECHAMENTO DA CONEXÃO
# =========================================================

conn.close()

print('Processo finalizado com sucesso!')
