<?php
require __DIR__ . '/config.php';

if (session_status() !== PHP_SESSION_ACTIVE) {
    session_start();
}

function voltar(string $msg): never {
    $_SESSION['flash_erro'] = $msg;
    header('Location: index.php');
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    voltar('Requisição inválida.');
}

// Proteção CSRF do Google: cookie e campo do POST precisam coincidir
$cookie = $_COOKIE['g_csrf_token'] ?? '';
$corpo  = $_POST['g_csrf_token'] ?? '';
if ($cookie === '' || !hash_equals($cookie, $corpo)) {
    voltar('Não foi possível validar o login com Google.');
}

$idToken = trim((string) ($_POST['credential'] ?? ''));
if ($idToken === '') {
    voltar('Login com Google cancelado.');
}

// Valida o token junto ao Google
$url = 'https://oauth2.googleapis.com/tokeninfo?id_token=' . urlencode($idToken);
$ch = curl_init($url);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT        => 10,
]);
$resp = curl_exec($ch);
$curlErro = curl_error($ch);
$http = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($resp === false) {
    error_log('Erro cURL ao validar token Google: ' . $curlErro);
    voltar('Erro de comunicação ao validar o login com Google.');
}

$dados = json_decode($resp, true);
$iss = $dados['iss'] ?? '';
$emailVerificado = filter_var($dados['email_verified'] ?? false, FILTER_VALIDATE_BOOLEAN);
$exp = (int) ($dados['exp'] ?? 0);

if (
    $http !== 200
    || !is_array($dados)
    || ($dados['aud'] ?? '') !== GOOGLE_CLIENT_ID
    || !in_array($iss, ['accounts.google.com', 'https://accounts.google.com'], true)
    || !$emailVerificado
    || $exp <= time()
    || empty($dados['email'])
) {
    voltar('Token do Google inválido.');
}

$email = mb_strtolower(trim((string) $dados['email']));

// Só entra quem já está cadastrado e ativo no sistema
$st = db()->prepare('SELECT id, nome, email, perfil FROM usuarios WHERE LOWER(email) = ? AND ativo = 1');
$st->execute([$email]);
$u = $st->fetch();

if (!$u) {
    voltar('Este e-mail Google não tem acesso ao sistema. Fale com a coordenação.');
}

iniciar_sessao($u);
header('Location: painel.php');
exit;