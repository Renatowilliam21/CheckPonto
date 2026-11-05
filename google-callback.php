<?php
require __DIR__ . '/config.php';

function voltar(string $msg): never {
    $_SESSION['flash_erro'] = $msg;
    header('Location: index.php'); exit;
}

// Proteção CSRF do Google: cookie e campo do POST precisam coincidir
$cookie = $_COOKIE['g_csrf_token'] ?? '';
$corpo  = $_POST['g_csrf_token'] ?? '';
if ($cookie === '' || !hash_equals($cookie, $corpo)) voltar('Não foi possível validar o login com Google.');

$idToken = $_POST['credential'] ?? '';
if ($idToken === '') voltar('Login com Google cancelado.');

// Valida o token junto ao Google
$ch = curl_init('https://oauth2.googleapis.com/tokeninfo?id_token=' . urlencode($idToken));
curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 10]);
$resp = curl_exec($ch);
$http = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

$dados = $resp ? json_decode($resp, true) : null;
if ($http !== 200 || !$dados
    || ($dados['aud'] ?? '') !== GOOGLE_CLIENT_ID
    || ($dados['email_verified'] ?? '') !== 'true') {
    voltar('Token do Google inválido.');
}

// Só entra quem já está cadastrado e ativo no sistema
$st = db()->prepare('SELECT id, nome, email, perfil FROM usuarios WHERE email = ? AND ativo = 1');
$st->execute([$dados['email']]);
$u = $st->fetch();
if (!$u) voltar('Este e-mail Google não tem acesso ao sistema. Fale com a coordenação.');

iniciar_sessao($u);
header('Location: painel.php');