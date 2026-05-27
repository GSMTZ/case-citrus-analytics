# =========================================================
# CASE TÉCNICO - CITRUS ANALYTICS
# Extração de dados geográficos da API do IBGE
#
# Objetivo:
# Consumir a API pública do IBGE para obter:
# - Código IBGE do município
# - Nome do município
# - Mesorregião
# - Região do Brasil
#
# O resultado será utilizado para criar a dimensão
# de municípios do modelo analítico.
# =========================================================


# =========================================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# =========================================================

# Biblioteca para manipulação de dados
import pandas as pd

# Biblioteca para realizar requisições HTTP
import requests

# Biblioteca utilizada para criar pausas entre requisições
import time


# =========================================================
# LISTA DE UFs BRASILEIRAS
#
# A API do IBGE exige consultas por estado.
# Será realizada uma requisição para cada UF.
# =========================================================

ufs = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF',
    'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA',
    'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS',
    'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
]


# =========================================================
# LISTA RESPONSÁVEL POR ARMAZENAR TODOS
# OS MUNICÍPIOS RETORNADOS PELA API
# =========================================================

lista_municipios = []


# =========================================================
# LOOP PRINCIPAL DE CONSUMO DA API
# =========================================================

for uf in ufs:

    print(f'Coletando dados do estado: {uf}')

    # =====================================================
    # MONTAGEM DINÂMICA DA URL DA API
    # =====================================================

    url = (
        f'https://servicodados.ibge.gov.br/api/v1/'
        f'localidades/estados/{uf}/municipios'
    )

    # =====================================================
    # REALIZA REQUISIÇÃO GET
    # =====================================================

    response = requests.get(url)

    # =====================================================
    # VALIDAÇÃO DA RESPOSTA DA API
    #
    # Status code 200 = sucesso
    # =====================================================

    if response.status_code == 200:

        # =================================================
        # CONVERTE RETORNO JSON PARA OBJETO PYTHON
        # =================================================

        dados = response.json()

        # =================================================
        # PERCORRE TODOS OS MUNICÍPIOS RETORNADOS
        # =================================================

        for item in dados:

            # =============================================
            # TRATAMENTO DE POSSÍVEIS VALORES NULOS
            # RETORNADOS PELA API DO IBGE
            # =============================================

            if item.get('microrregiao'):

                mesorregiao = (
                    item['microrregiao']
                        ['mesorregiao']
                        ['nome']
                )

                regiao_brasil = (
                    item['microrregiao']
                        ['mesorregiao']
                        ['UF']
                        ['regiao']
                        ['nome']
                )

            else:

                mesorregiao = None
                regiao_brasil = None

            # =============================================
            # ESTRUTURAÇÃO E PADRONIZAÇÃO DOS DADOS
            # =============================================

            municipio = {

                # Código IBGE oficial do município
                'cod_municipio_ibge': item['id'],

                # Nome padronizado do município
                'nome_municipio': (
                    item['nome']
                    .strip()
                    .title()
                ),

                # UF consultada
                'uf': uf,

                # Mesorregião tratada
                'mesorregiao': mesorregiao,

                # Região do Brasil tratada
                'regiao_brasil': regiao_brasil
            }

            # =============================================
            # ADICIONA MUNICÍPIO À LISTA CONSOLIDADA
            # =============================================

            lista_municipios.append(municipio)

    else:

        # =================================================
        # EXIBE ERRO CASO A REQUISIÇÃO FALHE
        # =================================================

        print(f'Erro ao coletar dados da UF: {uf}')

    # =====================================================
    # PEQUENA PAUSA ENTRE REQUISIÇÕES
    #
    # Evita sobrecarga na API pública do IBGE
    # =====================================================

    time.sleep(0.5)


# =========================================================
# CRIAÇÃO DO DATAFRAME FINAL
# =========================================================

df_municipios = pd.DataFrame(lista_municipios)


# =========================================================
# VALIDAÇÃO INICIAL DOS DADOS COLETADOS
# =========================================================

print('\nPreview dos dados coletados:\n')

print(df_municipios.head())


# =========================================================
# INFORMAÇÕES GERAIS DO DATAFRAME
# =========================================================

print('\nInformações do DataFrame:\n')

print(df_municipios.info())


# =========================================================
# VERIFICAÇÃO DE DUPLICIDADES
# =========================================================

duplicados = df_municipios.duplicated().sum()

print(f'\nQuantidade de registros duplicados: {duplicados}')


# =========================================================
# EXPORTAÇÃO DO CSV FINAL
# =========================================================

df_municipios.to_csv(
    '../data/dim_municipio.csv',
    index=False
)


# =========================================================
# MENSAGEM FINAL
# =========================================================

print('\nArquivo dim_municipio.csv salvo com sucesso!')