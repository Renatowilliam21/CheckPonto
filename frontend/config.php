<?php
// ---- Ajuste aqui ----
const DB_HOST = 'localhost';
const DB_NAME = 'lisa';
const DB_USER = 'root';
const DB_PASS = '';
// Client ID criado no Google Cloud Console (OAuth 2.0 > ID do cliente da Web)
const GOOGLE_CLIENT_ID = '159228944010-6kdnvrqh7qq1c4dk3abht8ernvp15kid.apps.googleusercontent.com';
// ---------------------

session_set_cookie_params(['httponly' => true, 'samesite' => 'Lax']);
session_start();

function db(): PDO {
    static $pdo = null;
    if (!$pdo) {
        $pdo = new PDO(
            'mysql:host=' . DB_HOST . ';dbname=' . DB_NAME . ';charset=utf8mb4',
            DB_USER, DB_PASS,
            [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]
        );
    }
    return $pdo;
}

function h(?string $s): string {
    return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8');
}

function iniciar_sessao(array $u): void {
    session_regenerate_id(true);
    $_SESSION['usuario'] = ['id' => $u['id'], 'nome' => $u['nome'], 'email' => $u['email']];
    db()->prepare('UPDATE usuarios SET ultimo_login = NOW() WHERE id = ?')->execute([$u['id']]);
}
