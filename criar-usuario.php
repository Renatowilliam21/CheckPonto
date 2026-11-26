<?php
// Uso (no terminal): php criar-usuario.php "Nome" email@dominio.br senha
// Para usuários que entram só pelo Google, omita a senha.
if (PHP_SAPI !== 'cli') { http_response_code(403); exit('Somente via linha de comando.'); }
require __DIR__ . '/config.php';

[, $nome, $email] = $argv + [null, null, null];
$senha = $argv[3] ?? null;
if (!$nome || !$email) exit("Uso: php criar-usuario.php \"Nome\" email senha\n");

db()->prepare('INSERT INTO usuarios (nome, email, senha_hash) VALUES (?,?,?)')
    ->execute([$nome, $email, $senha ? password_hash($senha, PASSWORD_DEFAULT) : null]);
echo "Usuário criado: $email\n";
