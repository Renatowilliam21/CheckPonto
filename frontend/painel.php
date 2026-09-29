<?php
require __DIR__ . '/config.php';

if (isset($_GET['sair'])) {
    $_SESSION = [];
    session_destroy();
    header('Location: index.php'); exit;
}
if (empty($_SESSION['usuario'])) { header('Location: index.php'); exit; }
$u = $_SESSION['usuario'];
?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Painel · LISA</title>
<style>
body{font-family:system-ui,sans-serif;background:#F5F7F8;color:#13232B;margin:0;padding:48px 24px}
.c{max-width:640px;margin:0 auto} a{color:#0E4F61;font-weight:600}
</style>
</head>
<body>
<div class="c">
  <h1>Olá, <?= h($u['nome']) ?></h1>
  <p>Login realizado. Aqui entra o painel de acessos.</p>
  <p><a href="painel.php?sair=1">Sair</a></p>
</div>
</body>
</html>
