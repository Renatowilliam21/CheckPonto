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
if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(32));

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

function iniciais_nome(string $nome): string {
    $partes = preg_split('/\s+/', trim($nome));
    $i = mb_strtoupper(mb_substr($partes[0], 0, 1));
    if (count($partes) > 1) $i .= mb_strtoupper(mb_substr(end($partes), 0, 1));
    return $i;
}

function iniciar_sessao(array $u): void {
    session_regenerate_id(true);
    $_SESSION['usuario'] = [
        'id' => $u['id'], 'nome' => $u['nome'], 'email' => $u['email'],
        'perfil' => $u['perfil'] ?? 'participante',
    ];
    db()->prepare('UPDATE usuarios SET ultimo_login = NOW() WHERE id = ?')->execute([$u['id']]);
}

// 'Hoje', 'Amanhã' ou 'Seg, 25/04', a partir de uma data (YYYY-MM-DD)
function data_relativa(string $data): string {
    $hoje = new DateTime('today');
    $d = new DateTime($data);
    $diferenca = (int)$hoje->diff($d)->format('%r%a');
    if ($diferenca === 0) return 'Hoje';
    if ($diferenca === 1) return 'Amanhã';
    $dias = ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb'];
    return $dias[(int)$d->format('w')] . ', ' . $d->format('d/m');
}

// 'Hoje às 14:32' ou '25/04 às 14:32', a partir de um DATETIME
function registro_relativo(string $dataHora): string {
    $dt = new DateTime($dataHora);
    $hoje = (new DateTime('today'))->format('Y-m-d');
    $prefixo = $dt->format('Y-m-d') === $hoje ? 'Hoje' : $dt->format('d/m');
    return $prefixo . ' às ' . $dt->format('H:i');
}

function perfil_rotulo(string $perfil): string {
    return match ($perfil) {
        'coordenador'    => 'Coordenador',
        'tecnico'        => 'Técnico',
        'administrador'  => 'Administrador',
        default          => 'Participante',
    };
}

// Cor de fundo do avatar, variando por usuário (só estética)
function avatar_cor(int $id): string {
    $cores = ['#2F6FED', '#7C5CFC', '#1E9E6B', '#E2A33D', '#E24C4C'];
    return $cores[$id % count($cores)];
}