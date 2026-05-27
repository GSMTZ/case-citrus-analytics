-- =========================================================
-- INSERÇÃO DOS DADOS NA TABELA FATO
--
-- Regras aplicadas:
-- - Apenas registros válidos
-- - Área colhida maior que zero
-- - Quantidade produzida maior que zero
-- - Cálculo da produtividade
-- =========================================================

INSERT INTO fato_producao (
    cod_municipio_ibge,
    cod_produto,
    ano,
    qtd_produzida_ton,
    area_colhida_ha,
    valor_producao_reais,
    produtividade_ton_ha
)
SELECT
    d.cod_municipio_ibge,
    p.cod_produto,
    p.ano,
    p.qtd_produzida_ton,
    p.area_colhida_ha,
    p.valor_producao_reais,
    -- Cálculo da produtividade agrícola
    (
        p.qtd_produzida_ton /
        p.area_colhida_ha
    ) AS produtividade_ton_ha
FROM staging_producao p
LEFT JOIN dim_municipio d
    ON p.municipio = d.nome_municipio
    AND p.uf = d.uf
WHERE
    -- Apenas registros válidos
    p.qtd_produzida_ton > 0
    AND p.area_colhida_ha > 0;