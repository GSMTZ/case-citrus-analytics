-- =========================================================
-- CRIAÇÃO DA TABELA FATO_PRODUCAO
--
-- Objetivo:
-- Armazenar métricas de produção agrícola
-- de citros por município, produto e ano.
--
-- Granularidade:
-- Uma linha por:
-- - município
-- - produto
-- - ano
-- =========================================================

CREATE TABLE fato_producao (
    -- Código do município IBGE
    cod_municipio_ibge BIGINT,
    -- Código do produto agrícola
    cod_produto INT,
    -- Ano de referência da produção
    ano INT,
    -- Quantidade produzida em toneladas
    qtd_produzida_ton NUMERIC(18,2),
    -- Área colhida em hectares
    area_colhida_ha NUMERIC(18,2),
    -- Valor da produção em reais
    valor_producao_reais NUMERIC(18,2),
    -- Métrica derivada:
    -- produtividade = produção / área colhida
    produtividade_ton_ha NUMERIC(18,2),
    -- Chave estrangeira para dimensão geográfica
    CONSTRAINT fk_municipio
        FOREIGN KEY (cod_municipio_ibge)
        REFERENCES dim_municipio(cod_municipio_ibge)
);