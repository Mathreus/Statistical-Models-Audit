WITH dados_faturamento AS (
  SELECT DISTINCT
    CONCAT(left(nf.bukrs, 2), right(nf.branch, 2)) as Centro,
    NF.PSTDAT AS Data_Lcto,
    CASE
      WHEN ped.spart = '01' THEN 'Consumo'
      WHEN ped.spart = '02' THEN 'Revenda' 
      WHEN ped.spart = '04' THEN 'Marketplace'
      ELSE 'Não Identificado'
    END Canal,
    NF.PARID AS ID_Externo,
    NF.NAME1 AS Cliente,
    PED.VBELN AS Pedido,
    NF.NFENUM AS Num_nfe,
    RIGHT(LIN.MATNR, 6) AS Codigo_Material,
    LIN.MAKTX AS Texto_Breve_Material,
    CAST(LIN.MENGE AS NUMERIC) AS Quantidade,  
    ROUND(CAST(LIN.NETWR AS NUMERIC), 2) AS Faturamento,
    ROUND(CAST(LIN.NETPR AS NUMERIC), 2) AS Valor_Unitario,
    RELV.PARTNER AS Cod_orig_vend, 
    CONCAT(VEND.BU_SORT2,' ',VEND.BU_SORT1) AS Vendedor
  FROM
    `production-servers-magnumtires.prdmgm_sap_cdc_processed.vbak` AS PED
  INNER JOIN  
    `production-servers-magnumtires.prdmgm_sap_cdc_processed.vbap` AS ITEM 
    ON ped.mandt = item.mandt 
    AND ped.vbeln = item.vbeln
  INNER JOIN 
    `production-servers-magnumtires.prdmgm_sap_cdc_processed.vbfa` AS FA 
    ON ped.mandt = fa.mandt  
    AND ped.vbeln = fa.vbelv 
    AND vbtyp_n = 'M'
  INNER JOIN 
    `production-servers-magnumtires.prdmgm_sap_cdc_processed.vbrk` AS FAT 
    ON fat.mandt = ped.mandt 
    AND fa.vbeln = fat.vbeln
  INNER JOIN 
    `production-servers-magnumtires.prdmgm_sap_cdc_processed.vbrp` AS RP
    ON rp.mandt = ped.mandt 
    AND fat.vbeln = rp.vbeln
  INNER JOIN 
    `production-servers-magnumtires.prdmgm_sap_cdc_processed.j_1bnflin` AS LIN
    ON lin.mandt = ped.mandt 
    AND rp.vbeln = lin.refkey 
    AND rp.matnr = lin.matnr
  INNER JOIN 
    `production-servers-magnumtires.prdmgm_sap_cdc_processed.j_1bnfdoc` AS NF 
    ON nf.mandt = ped.mandt 
    AND lin.docnum = nf.docnum
  INNER JOIN 
    `production-servers-magnumtires.prdmgm_sap_cdc_processed.but0id` AS RELV 
    ON ped.mandt = relv.client
    AND relv.idnumber = item.perve_ana
  INNER JOIN 
    `production-servers-magnumtires.prdmgm_sap_cdc_processed.but000` AS VEND 
    ON ped.mandt = vend.client 
    AND relv.partner = vend.partner
  WHERE
    nf.pstdat between '2025-03-01' and '2025-04-30' 
    AND nf.parid > '1000000000' 
    AND PED.SPART = '02'
    AND nf.nfenum <> 'NULL' 
    AND nf.cancel <> 'X'   
    AND nf.direct = '2'
    AND NF.NFTYPE = 'YC'
),

estatisticas_produto AS (
  SELECT
    Centro,
    Codigo_Material,
    ROUND(AVG(Valor_Unitario), 2) AS media_valor_unitario,
    ROUND(STDDEV(Valor_Unitario), 2) AS desvio_padrao_valor_unitario
  FROM
    dados_faturamento
  GROUP BY
    Centro,
    Codigo_Material
)

SELECT
  df.Centro,
  df.Data_Lcto,
  df.Canal,
  df.ID_Externo,
  df.Cliente,
  df.Pedido,
  df.Num_nfe,
  df.Codigo_Material,
  df.Texto_Breve_Material,
  df.Quantidade,
  df.Faturamento,
  df.Valor_Unitario,
  df.Cod_orig_vend,
  df.Vendedor,
  ep.media_valor_unitario,
  ep.desvio_padrao_valor_unitario,
  CASE
    WHEN ep.desvio_padrao_valor_unitario = 0 THEN 0
    ELSE ROUND((df.Valor_Unitario - ep.media_valor_unitario) / NULLIF(ep.desvio_padrao_valor_unitario, 0), 2)
  END AS zscore_valor_unitario,
  CASE
    WHEN (df.Valor_Unitario - ep.media_valor_unitario) / NULLIF(ep.desvio_padrao_valor_unitario, 0) > 3 THEN 'Valor muito alto'
    WHEN (df.Valor_Unitario - ep.media_valor_unitario) / NULLIF(ep.desvio_padrao_valor_unitario, 0) < -3 THEN 'Valor muito baixo'
    ELSE 'Dentro do esperado'
  END AS classificacao_zscore
FROM
  dados_faturamento df
JOIN
  estatisticas_produto ep
ON
  df.Codigo_Material = ep.Codigo_Material
  AND df.Centro = ep.Centro 
ORDER BY
  df.Data_Lcto ASC,
  ABS(ROUND((df.Valor_Unitario - ep.media_valor_unitario) / NULLIF(ep.desvio_padrao_valor_unitario, 0), 2)) DESC
