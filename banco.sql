CREATE DATABASE IF NOT EXISTS lisa CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE lisa;

CREATE TABLE IF NOT EXISTS usuarios (
  id           INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nome         VARCHAR(120) NOT NULL,
  email        VARCHAR(160) NOT NULL UNIQUE,
  senha_hash   VARCHAR(255) NULL,           -- NULL = usuário que entra só pelo Google
  ativo        TINYINT(1) NOT NULL DEFAULT 1,
  criado_em    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  ultimo_login DATETIME NULL
);
