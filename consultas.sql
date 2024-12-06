--Recordes detidos por atletas que possuem objetivos de desenvolvimento em progresso 
SELECT 
    a.NOME AS ATLETA,
    r.MODALIDADE,
    r.DATA,
    r.INFORMACAO
FROM 
    RECORDES_DETIDOS rd
JOIN 
    RECORDES r ON rd.MODALIDADE = r.MODALIDADE AND rd.DATA = r.DATA
JOIN 
    ATLETA a ON rd.ATLETA = a.PESSOA
JOIN 
    OBJETIVO_DE_DESENVOLVIMENTO od ON od.ATLETA = a.PESSOA
WHERE 
    od.STATUS = 'EM PROGRESSO';




--Mentores que nunca treinaram atletas com doenças 
SELECT 
    m.NOME AS MENTOR
FROM 
    MENTOR m
INNER JOIN 
    ATLETA a ON a.MENTOR = m.PESSOA
LEFT JOIN 
    DOENCAS_ATLETA da ON da.ATLETA = a.PESSOA
WHERE 
    da.DOENCA IS NULL;




--esportes praticados por atletas com obj de desenvolvimento concluidos
SELECT 
    ep.NOME_DO_ESPORTE,
    ep.CATEGORIA_DO_ESPORTE,
    COUNT(a.PESSOA) AS NUMERO_DE_ATLETAS
FROM 
    ESPORTES_PRATICADOS ep
JOIN 
    ATLETA a ON ep.ATLETA = a.PESSOA
JOIN 
    OBJETIVO_DE_DESENVOLVIMENTO od ON od.ATLETA = a.PESSOA
WHERE 
    od.STATUS = 'CONCLUIDO'
GROUP BY 
    ep.NOME_DO_ESPORTE, ep.CATEGORIA_DO_ESPORTE;




--atletas com menos de 25 anos que tem recordes
SELECT 
    a.NOME AS ATLETA,
    a.DATA_NASC,
    r.MODALIDADE,
    r.DATA AS DATA_RECORDES,
    r.INFORMACAO
FROM 
    ATLETA a
JOIN 
    RECORDES_DETIDOS rd ON rd.ATLETA = a.PESSOA
JOIN 
    RECORDES r ON rd.MODALIDADE = r.MODALIDADE AND rd.DATA = r.DATA
WHERE 
    ROUND(MONTHS_BETWEEN(SYSDATE, a.DATA_NASC) / 12, 0) < 25;




--todos os mentores que deram menos de 3 mentorias 
SELECT 
    m.NOME AS MENTOR,
    COUNT(sm.DATA) AS TOTAL_MENTORIAS
FROM 
    MENTOR m
LEFT JOIN 
    ATLETA a ON m.PESSOA = a.MENTOR
LEFT JOIN 
    SESSAO_DE_MENTORIA sm ON sm.ATLETA = a.PESSOA
GROUP BY 
    m.NOME
HAVING 
    COUNT(sm.DATA) < 3;
