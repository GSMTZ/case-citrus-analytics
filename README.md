# README — Case Técnico BI | Citrus Analytics

## Objetivo do Projeto

Este projeto foi desenvolvido como solução para o case técnico da vaga de Analista de Business Intelligence.

O objetivo principal foi construir um pipeline analítico completo para análise da produção de citros no Brasil, utilizando dados públicos do IBGE e técnicas de:

* ETL
* modelagem dimensional
* persistência relacional
* preparação para visualização analítica

O projeto contempla:

* extração e limpeza de dados
* integração com API pública do IBGE
* tratamento de inconsistências
* modelagem dimensional (fato e dimensão)
* persistência em banco SQLite
* preparação para consumo no Power BI

---

# Estrutura do Projeto

```txt
case-citrus-analytics/
│
├── data/
│   ├── producao_citros_bruto_original.csv
│   ├── producao_citros_bruto.csv
│   ├── dim_municipio.csv
│   └── fato_producao.csv
│
├── extraction/
│   ├── transform_fato_producao.py
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
└── README.md
```

---

# Arquitetura do Pipeline

O projeto foi estruturado em camadas independentes para separar responsabilidades e facilitar:

* manutenção
* rastreabilidade
* escalabilidade
* organização do pipeline analítico

---

## Camada de Dados (`/data`)

Responsável por armazenar:

* base original recebida no case
* bases tratadas
* dimensão geográfica
* tabela fato final

### Arquivos

| Arquivo                            | Descrição                                       |
| ---------------------------------- | ----------------------------------------------- |
| producao_citros_bruto_original.csv | Base original sem alterações                    |
| producao_citros_bruto.csv          | Base utilizada no processo analítico            |
| dim_municipio.csv                  | Dimensão geográfica enriquecida via API do IBGE |
| fato_producao.csv                  | Tabela fato final utilizada no modelo analítico |

---

## Camada de Transformação (`/extraction`)

Responsável pelos processos de ETL e automação do pipeline.

Cada script possui uma responsabilidade específica.

---

### `transform_fato_producao.py`

Responsável por:

* leitura do CSV bruto
* análise inicial dos dados
* tratamento de inconsistências
* conversão de tipos numéricos
* remoção de registros inválidos
* criação da métrica de produtividade
* geração da tabela `fato_producao.csv`

---

### `extract_ibge.py`

Responsável por:

* consumo da API pública do IBGE
* extração dos municípios brasileiros
* obtenção de:
  * código IBGE
  * estado
  * mesorregião
  * região do Brasil
* tratamento de possíveis valores nulos da API
* geração da dimensão `dim_municipio.csv`

---

### `load_sqlite.py`

Responsável por:

* conexão com banco SQLite
* leitura das tabelas tratadas
* persistência das tabelas analíticas
* carga final no banco relacional

---

## Camada Analítica (`/notebooks`)

Responsável pela análise exploratória dos dados (EDA).

---

### `01_eda_limpeza.ipynb`

Notebook utilizado para:

* exploração inicial do dataset
* validação de qualidade dos dados
* identificação de inconsistências
* documentação do processo analítico
* testes e validações das transformações

O notebook foi mantido separado dos scripts produtivos para diferenciar:

* análise exploratória
* pipeline operacional

---

## Camada SQL (`/sql`)

Responsável pela modelagem relacional e documentação das estruturas analíticas.

### Scripts SQL

| Arquivo                     | Objetivo                                    |
| --------------------------- | ------------------------------------------- |
| 01_create_dim_municipio.sql | Criação da dimensão geográfica              |
| 02_create_fato_producao.sql | Criação da tabela fato                      |
| 03_insert_dim_municipio.sql | Documentação da lógica de carga da dimensão |
| 04_insert_fato_producao.sql | Documentação da lógica de carga da fato     |

---

## Camada de Persistência (`SQLite`)

Banco utilizado:

```txt
case_citrus.db
```

Objetivo:

* armazenar o modelo dimensional
* persistir os dados tratados
* permitir consultas SQL analíticas
* servir como fonte para o Power BI

---

# Fluxo do Pipeline

```txt
CSV Original
    ↓
Transformação e Limpeza
    ↓
Criação da Tabela Fato
    ↓
Integração com API IBGE
    ↓
Criação da Dimensão Município
    ↓
Persistência no SQLite
    ↓
Consumo no Power BI
```

---

# 1. Análise Exploratória do CSV

A primeira etapa do projeto consistiu na análise exploratória do arquivo:

```txt
producao_citros_bruto.csv
```

Foram realizadas validações para identificar:

* estrutura do dataset
* tipos de dados
* valores nulos
* valores inválidos
* inconsistências nos nomes dos municípios
* problemas de qualidade dos dados

Durante a análise foram identificados os seguintes problemas:

| Problema                                   |
| ------------------------------------------ |
| Valores `-` em colunas numéricas           |
| Valores nulos                              |
| Municípios com capitalização inconsistente |
| Colunas numéricas importadas como texto    |
| Registros inválidos com área igual a zero  |

---

# 2. Limpeza e Tratamento dos Dados

Após a análise inicial, foi realizado o processo de limpeza utilizando Python e Pandas.

## Principais tratamentos aplicados

### Padronização de municípios

Padronização utilizando:

```python
.str.strip().str.title()
```

Objetivo:

* eliminar inconsistências de capitalização
* facilitar futuras integrações

---

### Tratamento de valores inválidos

Conversão de valores:

```txt
-
```

para:

```python
NaN
```

utilizando:

```python
df.replace('-', np.nan)
```

---

### Conversão de tipos numéricos

Conversão utilizando:

```python
pd.to_numeric(errors='coerce')
```

Objetivo:

* garantir consistência nos cálculos
* permitir criação de métricas analíticas

---

### Remoção de registros inválidos

Foram removidos registros com:

* `area_colhida_ha <= 0`
* `qtd_produzida_ton <= 0`

Resultado:

| Situação                 | Quantidade |
| ------------------------ | ---------- |
| Registros originais      | 3600       |
| Registros válidos finais | 3234       |

Total removido:

* 366 registros inválidos

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

---

# 3. Integração com API do IBGE

Foi utilizada a API pública do IBGE para enriquecimento geográfico da dimensão de municípios.

Endpoint utilizado:

```txt
https://servicodados.ibge.gov.br/api/v1/localidades/estados/{UF}/municipios
```

Informações obtidas:

* código IBGE
* estado
* mesorregião
* região do Brasil

Resultado:

| Informação            | Quantidade |
| --------------------- | ---------- |
| Municípios carregados | 5571       |
| Registros duplicados  | 0          |

---

# 4. Modelagem de Dados

Após o tratamento dos dados, foi construída uma modelagem dimensional composta por:

* tabela fato
* tabela dimensão

---

# Tabela `dim_municipio`

Tabela responsável por armazenar os dados geográficos dos municípios brasileiros.

## Estrutura

| Campo              | Descrição                   |
| ------------------ | --------------------------- |
| cod_municipio_ibge | Código oficial do município |
| nome_municipio     | Nome padronizado            |
| uf                 | Sigla do estado             |
| estado             | Nome do estado              |
| mesorregiao        | Mesorregião IBGE            |
| regiao_brasil      | Região do Brasil            |

Granularidade:

* uma linha por município

---

# Tabela `fato_producao`

Tabela responsável por armazenar os indicadores de produção agrícola.

## Estrutura

| Campo                | Descrição             |
| -------------------- | --------------------- |
| cod_municipio_ibge   | Chave do município    |
| cod_produto          | Código do produto     |
| ano                  | Ano de referência     |
| qtd_produzida_ton    | Produção em toneladas |
| area_colhida_ha      | Área colhida          |
| valor_producao_reais | Valor da produção     |
| produtividade_ton_ha | Métrica derivada      |

Granularidade:

* uma linha por município + produto + ano

---

# 5. Tecnologias Utilizadas

| Tecnologia | Finalidade                |
| ---------- | ------------------------- |
| Python     | ETL e tratamento de dados |
| Pandas     | Manipulação de dados      |
| Requests   | Consumo da API            |
| SQLite     | Persistência relacional   |
| SQL        | Modelagem e consultas     |
| Power BI   | Dashboard analítico       |

---

# 6. Resultado Final

O projeto resultou em uma solução analítica ponta a ponta contendo:

* pipeline ETL automatizado
* tratamento e padronização de dados
* integração com API pública
* modelagem dimensional
* persistência em banco relacional
* estrutura pronta para consumo analítico no Power BI

A solução foi desenvolvida seguindo separação de responsabilidades entre:

* exploração analítica
* transformação de dados
* modelagem SQL
* persistência
* visualização

O objetivo principal foi construir uma arquitetura analítica organizada, reproduzível e preparada para tomada de decisão.
