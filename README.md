# README — Case Técnico BI | Citrus Analytics

## Objetivo do Projeto

Este projeto foi desenvolvido como solução para o case técnico da vaga de Analista de Business Intelligence. O objetivo principal foi construir um pipeline analítico completo para análise da produção de citros no Brasil, utilizando dados públicos do IBGE e técnicas de ETL, modelagem dimensional e visualização de dados.

O projeto contempla:

- Extração e limpeza de dados
- Integração com API pública do IBGE
- Tratamento de inconsistências
- Modelagem dimensional (fato e dimensão)
- Persistência em banco SQLite
- Preparação para consumo no Power BI

---

# Estrutura do Projeto

```txt
case-citrus-analytics/
│
├── data/
│   ├── producao_citros_bruto.csv
│   ├── dim_municipio.csv
│   ├── producao_citros_bruto_original.csv
│   └── fato_producao.csv
│
├── extraction/
│   ├── extract_ibge.py
│   └── load_sqlite.py
│
├── sql/
│   ├── 01_create_dim_municipio.sql
│   ├── 02_create_fato_producao.sql
│   ├── 03_insert_dim_municipio.sql
│   ├── 04_insert_fato_producao.sql
│   └── case_citrus.db
│
├── notebooks/
│   └── 01_eda_limpeza.ipynb
│
├── dashboard/
│
├── docs/
│
│
└── README.md
```

---

# 1. Análise Exploratória do CSV

A primeira etapa do projeto consistiu na análise exploratória do arquivo `producao_citros_bruto.csv`.

Foram realizadas validações para identificar:

- Estrutura do dataset
- Tipos de dados
- Valores nulos
- Valores inválidos
- Inconsistências nos nomes dos municípios
- Problemas de qualidade dos dados

Durante a análise foram identificados os seguintes problemas:

| Problema | Identificado |
|---|---|
| Valores `-` em colunas numéricas | Sim |
| Valores nulos | Sim |
| Municípios com capitalização inconsistente | Sim |
| Colunas numéricas importadas como texto | Sim |
| Registros inválidos com área igual a zero | Sim |

---

# 2. Limpeza e Tratamento dos Dados

Após a análise inicial, foi realizado o processo de limpeza dos dados utilizando Python e Pandas.

## Principais tratamentos aplicados

### Padronização de municípios

Os nomes dos municípios foram padronizados utilizando:

```python
.str.strip().str.title()
```

Objetivo:
- eliminar diferenças de capitalização
- facilitar integração com a API do IBGE

Exemplo:

| Original | Tratado |
|---|---|
| ARARAQUARA | Araraquara |
| araraquara | Araraquara |

---

### Tratamento de valores inválidos

Os valores representados por:

```txt
-
```

foram convertidos para:

```python
NaN
```

utilizando:

```python
df.replace('-', np.nan)
```

---

### Conversão de tipos numéricos

As colunas numéricas foram convertidas utilizando:

```python
pd.to_numeric(errors='coerce')
```

Objetivo:
- garantir consistência para cálculos
- permitir criação de métricas analíticas

---

### Remoção de registros inválidos

Conforme solicitado no case, registros com:

- `area_colhida_ha <= 0`
- `qtd_produzida_ton <= 0`

foram removidos.

Resultado:

| Situação | Quantidade |
|---|---|
| Registros originais | 3600 |
| Registros válidos finais | 3234 |

Total removido:
- 366 registros inválidos

---

### Criação da métrica derivada

Foi criada a métrica:

```txt
produtividade_ton_ha
```

utilizando:

```python
qtd_produzida_ton / area_colhida_ha
```

Essa métrica será utilizada posteriormente no dashboard analítico.

---

# 3. Integração com API do IBGE

Para enriquecer os dados com informações geográficas e regionais, foi utilizada a API pública de localidades do IBGE.

Endpoint utilizado:

```txt
https://servicodados.ibge.gov.br/api/v1/localidades/estados/{UF}/municipios
```

---

## Informações extraídas da API

Para cada município foram obtidos:

- Código IBGE do município
- Nome do município
- Mesorregião
- Região do Brasil

---

## Estratégia de extração

Foi desenvolvido o script:

```txt
extract_ibge.py
```

Responsável por:

- consumir a API para todas as UFs brasileiras
- consolidar os dados
- tratar possíveis retornos nulos
- gerar o arquivo `dim_municipio.csv`

---

## Resultado da integração

A dimensão final gerada possui:

| Informação | Quantidade |
|---|---|
| Municípios carregados | 5571 |
| Registros duplicados | 0 |

---

# 4. Modelagem de Dados

Após o tratamento dos dados, foi construída uma modelagem dimensional composta por:

- Tabela Fato
- Tabela Dimensão

---

# Tabela `dim_municipio`

Tabela responsável por armazenar os dados geográficos dos municípios brasileiros.

## Estrutura

| Campo | Descrição |
|---|---|
| cod_municipio_ibge | Código oficial do município |
| nome_municipio | Nome padronizado |
| uf | Sigla do estado |
| estado | Nome do estado |
| mesorregiao | Mesorregião IBGE |
| regiao_brasil | Região do Brasil |

Granularidade:
- uma linha por município

---

# Tabela `fato_producao`

Tabela responsável por armazenar os indicadores de produção agrícola.

## Estrutura

| Campo | Descrição |
|---|---|
| cod_municipio_ibge | Chave do município |
| cod_produto | Código do produto |
| ano | Ano de referência |
| qtd_produzida_ton | Produção em toneladas |
| area_colhida_ha | Área colhida |
| valor_producao_reais | Valor da produção |
| produtividade_ton_ha | Métrica derivada |

Granularidade:
- uma linha por município + produto + ano

---

# 5. Banco de Dados SQLite

Foi utilizado SQLite como banco relacional local para persistência das tabelas analíticas.

Banco criado:

```txt
case_citrus.db
```

---

## Tabelas criadas

| Tabela | Tipo |
|---|---|
| dim_municipio | Dimensão |
| fato_producao | Fato |

---

# 6. Automação da Carga

A carga dos dados foi automatizada utilizando Python.

Script utilizado:

```txt
load_sqlite.py
```

Responsável por:

- conectar ao SQLite
- carregar os CSVs tratados
- inserir dados nas tabelas finais
- validar quantidade de registros

---

# 7. Tecnologias Utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | ETL e tratamento de dados |
| Pandas | Manipulação de dados |
| Requests | Consumo da API |
| SQLite | Persistência relacional |
| SQL | Modelagem e consultas |
| Power BI | Dashboard analítico |

---

# 8. Resultado Final

O projeto resultou em um pipeline analítico completo contendo:

- ingestão de dados
- limpeza
- enriquecimento geográfico
- modelagem dimensional
- persistência em banco
- preparação para visualização executiva no Power BI

O objetivo principal foi construir uma solução analítica estruturada, reproduzível e preparada para tomada de decisão.