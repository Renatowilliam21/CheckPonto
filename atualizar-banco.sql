USE lisa;

-- ---------- Estrutura ----------

CREATE TABLE IF NOT EXISTS laboratorios (
  id    INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nome  VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS terminais (
  id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nome            VARCHAR(80) NOT NULL,
  laboratorio_id  INT UNSIGNED NOT NULL,
  FOREIGN KEY (laboratorio_id) REFERENCES laboratorios(id)
);

CREATE TABLE IF NOT EXISTS projetos (
  id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nome            VARCHAR(120) NOT NULL,
  laboratorio_id  INT UNSIGNED NOT NULL,
  ativo           TINYINT(1) NOT NULL DEFAULT 1,
  FOREIGN KEY (laboratorio_id) REFERENCES laboratorios(id)
);

-- quais usuários participam de quais projetos
CREATE TABLE IF NOT EXISTS participantes_projetos (
  usuario_id  INT UNSIGNED NOT NULL,
  projeto_id  INT UNSIGNED NOT NULL,
  PRIMARY KEY (usuario_id, projeto_id),
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
  FOREIGN KEY (projeto_id) REFERENCES projetos(id)
);

CREATE TABLE IF NOT EXISTS atividades (
  id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  titulo          VARCHAR(160) NOT NULL,
  projeto_id      INT UNSIGNED NULL,
  laboratorio_id  INT UNSIGNED NOT NULL,
  data            DATE NOT NULL,
  hora_inicio     TIME NOT NULL,
  hora_fim        TIME NOT NULL,
  FOREIGN KEY (projeto_id) REFERENCES projetos(id),
  FOREIGN KEY (laboratorio_id) REFERENCES laboratorios(id)
);

-- quais usuários devem ver quais atividades
CREATE TABLE IF NOT EXISTS participantes_atividades (
  usuario_id    INT UNSIGNED NOT NULL,
  atividade_id  INT UNSIGNED NOT NULL,
  PRIMARY KEY (usuario_id, atividade_id),
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
  FOREIGN KEY (atividade_id) REFERENCES atividades(id)
);

CREATE TABLE IF NOT EXISTS registros_ponto (
  id           INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  usuario_id   INT UNSIGNED NOT NULL,
  tipo         ENUM('entrada','saida') NOT NULL,
  data_hora    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  terminal_id  INT UNSIGNED NULL,   -- NULL = batida feita pelo site, sem leitor RFID
  projeto_id   INT UNSIGNED NULL,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
  FOREIGN KEY (terminal_id) REFERENCES terminais(id),
  FOREIGN KEY (projeto_id) REFERENCES projetos(id)
);

-- ---------- Dados de exemplo ----------

INSERT IGNORE INTO laboratorios (id, nome) VALUES (1,'Lab. 1'), (2,'Lab. 2'), (3,'Lab. 3');

INSERT IGNORE INTO terminais (id, nome, laboratorio_id) VALUES
  (1,'Terminal 1',1), (2,'Terminal 2',2), (3,'Terminal 3',3);

INSERT IGNORE INTO projetos (id, nome, laboratorio_id, ativo) VALUES
  (1,'IA na Saúde',2,1),
  (2,'Sensoriamento Remoto',3,1);

INSERT IGNORE INTO atividades (id, titulo, projeto_id, laboratorio_id, data, hora_inicio, hora_fim) VALUES
  (1,'Reunião do projeto IA',        1, 2, CURDATE(),                    '16:00:00','17:00:00'),
  (2,'Desenvolvimento de protótipo', 1, 2, CURDATE() + INTERVAL 1 DAY,   '14:00:00','17:00:00'),
  (3,'Estudo dirigido',              NULL, 1, CURDATE() + INTERVAL 3 DAY,'10:00:00','12:00:00');

-- IMPORTANTE: troque o e-mail abaixo pelo e-mail com que você faz login,
-- para ligar o SEU usuário ao projeto e às atividades de exemplo.
INSERT IGNORE INTO participantes_projetos (usuario_id, projeto_id)
SELECT id, 1 FROM usuarios WHERE email = 'coloque-seu-email-de-login-aqui';

INSERT IGNORE INTO participantes_atividades (usuario_id, atividade_id)
SELECT u.id, a.id FROM usuarios u, atividades a
WHERE u.email = 'coloque-seu-email-de-login-aqui';