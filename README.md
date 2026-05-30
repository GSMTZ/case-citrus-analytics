# README — Case Técnico BI | Citrus Analytics

## Objetivo do Projeto

Este projeto foi desenvolvido como solução para o case técnico da vaga de Analista de Business Intelligence.

O objetivo principal foi construir uma solução analítica ponta a ponta para análise da produção de citros no Brasil, contemplando todas as etapas do ciclo de dados:

* Extração
* Limpeza
* Enriquecimento
* Qualidade de Dados
* Modelagem Dimensional
* Persistência Relacional
* Visualização Analítica

A solução utiliza dados públicos do IBGE e foi estruturada seguindo boas práticas de engenharia e análise de dados.

---

# Estrutura do Projeto

```txt
case-citrus-analytics/
│
├── dashboard/
│   └── Case_Citrus.pbix
│
├── data/
│   ├── producao_citros_bruto_original.csv
│   ├── producao_citros_bruto.csv
│   ├── dim_municipio.csv
│   ├── fato_producao.csv
│   │
│   └── LOGs/
│       ├── correcoes_geograficas.csv
│       ├── LOG_correcoes_municipios.csv
│       ├── LOG_municipios_sem_match.csv
│       └── municipios_sem_regiao.csv
│
├── extraction/
│   ├── 1 - extract_ibge.py
│   ├── 2 - transform_fato_producao.py
│   └── 3 - load_sqlite.py
│
├── notebooks/
│   └── 01_eda_limpeza.ipynb
│
├── sql/
│   ├── 01_create_dim_municipio.sql
│   ├── 02_create_fato_producao.sql
│   ├── 03_insert_dim_municipio.sql
│   ├── 04_insert_fato_producao.sql
│   └── case_citrus.db
│
├── docs/
│
├── requirements.txt
│
└── README.md
```

---

# Camada de Dados (`/data`)

Responsável por armazenar os dados utilizados ao longo do pipeline.

## Arquivos

| Arquivo                            | Descrição                                        |
| ---------------------------------- | ------------------------------------------------ |
| producao_citros_bruto_original.csv | Base original recebida no case                   |
| producao_citros_bruto.csv          | Base tratada e padronizada                       |
| dim_municipio.csv                  | Dimensão geográfica enriquecida pela API do IBGE |
| fato_producao.csv                  | Tabela fato utilizada nas análises               |

---

# Camada de Qualidade de Dados (`/data/LOGs`)

Durante o desenvolvimento foram implementadas validações automáticas para identificação, correção e rastreabilidade de inconsistências.

## Arquivos de Log

| Arquivo                      | Descrição                                                |
| ---------------------------- | -------------------------------------------------------- |
| LOG_municipios_sem_match.csv | Municípios sem correspondência após integração com IBGE  |
| LOG_correcoes_municipios.csv | Correções automáticas aplicadas em municípios            |
| municipios_sem_regiao.csv    | Municípios retornados pela API sem hierarquia geográfica |
| correcoes_geograficas.csv    | Correções geográficas aplicadas manualmente              |

Objetivo:

* Garantir qualidade dos dados
* Permitir auditoria das correções
* Facilitar rastreabilidade do pipeline

---

# Camada de Transformação (`/extraction`)

Responsável pela execução do ETL.

Cada script possui uma responsabilidade específica.

---

## 1 - extract_ibge.py

Responsável por:

* Consumir a API pública do IBGE
* Obter informações geográficas dos municípios brasileiros
* Gerar a dimensão geográfica

Informações obtidas:

* Código IBGE
* Nome do município
* UF
* Estado
* Mesorregião
* Região do Brasil

Também realiza:

* Identificação de registros incompletos
* Geração de logs de inconsistência
* Correções geográficas controladas

---

## 2 - transform_fato_producao.py

Responsável por:

* Leitura da base original
* Limpeza dos dados
* Conversão de tipos
* Tratamento de valores inválidos
* Integração com dimensão de municípios
* Correção automática de divergências geográficas
* Criação da tabela fato

Métrica derivada criada:

```txt
produtividade_ton_ha
```

Cálculo:

```txt
qtd_produzida_ton / area_colhida_ha
```

Também gera logs de:

* Municípios não encontrados
* Correções automáticas aplicadas

---

## 3 - load_sqlite.py

Responsável por:

* Conectar ao banco SQLite
* Criar as tabelas analíticas
* Carregar os dados tratados
* Persistir o modelo dimensional

---

# Camada Analítica (`/notebooks`)

## 01_eda_limpeza.ipynb

Notebook utilizado para:

* Exploração inicial da base
* Entendimento do negócio
* Identificação de inconsistências
* Validação das transformações
* Documentação da análise exploratória

O notebook foi mantido separado dos scripts produtivos para diferenciar:

* Ambiente exploratório
* Ambiente operacional

---

# Modelagem de Dados

Foi adotado um modelo dimensional composto por:

* Uma tabela fato
* Uma dimensão geográfica

---

## Dimensão Município (`dim_municipio`)

Granularidade:

```txt
Uma linha por município
```

Campos:

| Campo              | Descrição                   |
| ------------------ | --------------------------- |
| cod_municipio_ibge | Código oficial IBGE         |
| nome_municipio     | Nome do município           |
| uf                 | Sigla da unidade federativa |
| estado             | Nome completo do estado     |
| mesorregiao        | Mesorregião IBGE            |
| regiao_brasil      | Região do Brasil            |

---

## Tabela Fato (`fato_producao`)

Granularidade:

```txt
Uma linha por município + produto + ano
```

Campos:

| Campo                | Descrição                   |
| -------------------- | --------------------------- |
| cod_municipio_ibge   | Chave do município          |
| cod_produto          | Código do produto           |
| ano                  | Ano de referência           |
| qtd_produzida_ton    | Produção em toneladas       |
| area_colhida_ha      | Área colhida                |
| valor_producao_reais | Valor monetário da produção |
| produtividade_ton_ha | Produtividade calculada     |

---

# Processo de Limpeza dos Dados

Durante a análise exploratória foram identificadas inconsistências que exigiram tratamento.

## Problemas encontrados

* Valores "-" em colunas numéricas
* Valores nulos
* Colunas numéricas importadas como texto
* Municípios com capitalização inconsistente
* Registros com área igual a zero
* Registros com produção igual a zero

---

## Tratamentos aplicados

### Padronização de municípios

Utilizando:

```python
.str.strip().str.title()
```

---

### Conversão de valores inválidos

Substituição de:

```txt
-
```

por:

```txt
NaN
```

---

### Conversão de tipos

Utilizando:

```python
pd.to_numeric(errors='coerce')
```

---

### Remoção de registros inválidos

Critérios:

```txt
area_colhida_ha <= 0
qtd_produzida_ton <= 0
```

Resultado:

| Métrica             | Quantidade |
| ------------------- | ---------- |
| Registros originais | 3600       |
| Registros válidos   | 3234       |
| Registros removidos | 366        |

---

# Integração com API do IBGE

API utilizada:

```txt
https://servicodados.ibge.gov.br/api/v1/localidades/estados/{UF}/municipios
```

Objetivo:

Enriquecer a base com informações geográficas oficiais.

Resultado:

| Métrica               | Quantidade |
| --------------------- | ---------- |
| Municípios carregados | 5571       |
| Duplicidades          | 0          |

---

# Tratamento de Inconsistências Geográficas

Durante o desenvolvimento foram identificadas divergências entre a base original e a base oficial do IBGE.

## Caso 1 — Divergência de UF

Foi identificado o município:

```txt
Petrolina
```

com UF divergente na base original.

Foi implementada uma correção automática utilizando a dimensão oficial do IBGE.

---

## Caso 2 — Município sem hierarquia geográfica

Foi identificado o município:

```txt
Boa Esperança do Norte (MT)
```

retornado pela API sem informações completas de:

* Estado
* Mesorregião
* Região

Foi implementada:

* Detecção automática
* Registro em log
* Correção controlada

---

# Banco de Dados

Banco utilizado:

```txt
SQLite
```

Arquivo:

```txt
case_citrus.db
```

Objetivos:

* Persistir o modelo dimensional
* Armazenar dados tratados
* Disponibilizar fonte para Power BI
* Permitir consultas SQL analíticas

---

# Dashboard Executivo

Foi desenvolvido um dashboard executivo no Power BI para responder às perguntas de negócio propostas no case.

---

## Perguntas Respondidas

### Evolução da produção

Qual foi a evolução da produção de citros entre 2015 e 2023?

Visual:

* Série temporal anual
* Indicador de variação acumulada

---

### Estados mais produtivos

Quais estados apresentam maior produtividade média?

Visual:

* Ranking de estados por produtividade

---

### Distribuição geográfica

Como a produção está distribuída pelo território nacional?

Visual:

* Mapa coroplético por estado

---

## Indicadores Principais

* Produção Total
* Área Colhida
* Produtividade Média
* Melhor Região em Produtividade
* Variação da Produção

---

## Visualizações

* Mapa Coroplético
* Evolução Temporal da Produção
* Ranking de Regiões por Produção
* Ranking de Estados por Produtividade

---

# Tecnologias Utilizadas

| Tecnologia | Finalidade              |
| ---------- | ----------------------- |
| Python     | ETL                     |
| Pandas     | Manipulação de dados    |
| Requests   | Consumo da API          |
| SQLite     | Persistência relacional |
| SQL        | Modelagem               |
| Power BI   | Visualização analítica  |
| DAX        | Indicadores e métricas  |

---

# Resultado Final

A solução entrega um pipeline analítico completo contemplando:

* ETL automatizado
* Qualidade e governança de dados
* Integração com API pública
* Modelagem dimensional
* Persistência relacional
* Dashboard executivo
* Rastreabilidade das correções realizadas

O projeto foi estruturado para reproduzir um cenário real de Business Intelligence, separando claramente as camadas de:

* Exploração
* Transformação
* Qualidade de Dados
* Modelagem
* Persistência
* Visualização

com foco em organização, manutenção e tomada de decisão baseada em dados.
