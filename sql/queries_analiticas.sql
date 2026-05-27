-- =========================================================
-- EVOLUÇÃO DA PRODUÇÃO TOTAL DE CITROS
-- =========================================================

SELECT
    ano,
    SUM(qtd_produzida_ton) AS producao_total_ton
FROM fato_producao
GROUP BY ano
ORDER BY ano;

-- =========================================================
-- PRODUTIVIDADE MÉDIA POR ESTADO
-- =========================================================

SELECT
    d.uf,
    AVG(f.produtividade_ton_ha) AS produtividade_media
FROM fato_producao f
LEFT JOIN dim_municipio d
    ON f.cod_municipio_ibge = d.cod_municipio_ibge
GROUP BY d.uf
ORDER BY produtividade_media DESC;

-- =========================================================
-- PRODUÇÃO TOTAL POR REGIÃO DO BRASIL
-- =========================================================

SELECT
    d.regiao_brasil,
    SUM(f.qtd_produzida_ton) AS producao_total
FROM fato_producao f
LEFT JOIN dim_municipio d
    ON f.cod_municipio_ibge = d.cod_municipio_ibge
GROUP BY d.regiao_brasil
ORDER BY producao_total DESC;