-- =========================================================
-- CRIAÇÃO DA TABELA DIM_MUNICIPIO
--
-- Objetivo:
-- Armazenar informações geográficas e regionais
-- dos municípios brasileiros.
--
-- Granularidade:
-- Uma linha por município.
-- =========================================================

CREATE TABLE dim_municipio (
    -- Código oficial IBGE do município
    cod_municipio_ibge BIGINT PRIMARY KEY,
    -- Nome do município padronizado
    nome_municipio VARCHAR(255),
    -- Sigla da unidade federativa
    uf CHAR(2),
    -- Nome do estado
    estado VARCHAR(255),
    -- Nome da mesorregião
    mesorregiao VARCHAR(255),
    -- Região do Brasil
    regiao_brasil VARCHAR(100)
);