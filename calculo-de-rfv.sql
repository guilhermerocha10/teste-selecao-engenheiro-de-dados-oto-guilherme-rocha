SELECT 
    Cliente, 
    DATEDIFF(day, MAX(Data), GETDATE()) AS Recencia, 
    COUNT(*) AS Frequencia, 
    SUM(Valor) AS Valor 
FROM tabela_compras
GROUP BY Cliente;