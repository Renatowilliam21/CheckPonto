-- CHECKPONTO
-- Seed inicial dos tipos de vinculo.
--
-- Duracoes sao armazenadas em minutos.

INSERT INTO tipo_vinculo (
    nome,
    carga_semanal_padrao_min,
    carga_diaria_minima_min,
    carga_diaria_maxima_min,
    ativo
)
VALUES
    (
        'BOLSISTA',
        960,
        240,
        360,
        TRUE
    ),
    (
        'ESTAGIARIO',
        0,
        240,
        480,
        TRUE
    )
ON CONFLICT (nome) DO NOTHING;
