-- =========================================================
-- INSERÇÃO DOS DADOS NA DIMENSÃO DE MUNICÍPIOS
--
-- Fonte:
-- Dados enriquecidos via API do IBGE.
-- =========================================================

INSERT INTO dim_municipio (
    cod_municipio_ibge,
    nome_municipio,
    uf,
    estado,
    mesorregiao,
    regiao_brasil
)
SELECT DISTINCT
    cod_municipio_ibge,
    nome_municipio,
    uf,
    estado,
    mesorregiao,
    regiao_brasil
FROM staging_municipios;