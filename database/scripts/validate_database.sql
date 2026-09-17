\echo '============================================================'
\echo ' CHECKPONTO - VALIDACAO DO BANCO'
\echo '============================================================'

SELECT current_database() AS banco_atual;

SELECT COUNT(*) AS tabelas_checkponto
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE';

\echo ''
\echo 'Tipos de vinculo:'

SELECT
    id,
    nome,
    carga_semanal_padrao_min,
    carga_diaria_minima_min,
    carga_diaria_maxima_min,
    ativo
FROM tipo_vinculo
ORDER BY id;

\echo ''
\echo 'Verificando event_uuid UNIQUE:'

SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'evento_rfid'
  AND indexdef ILIKE '%event_uuid%';

\echo ''
\echo 'Tabelas:'

SELECT tablename
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;
