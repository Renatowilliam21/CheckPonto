<?php
require __DIR__ . '/config.php';
$pdo = db();

$token = $_GET['token'] ?? $_POST['token'] ?? '';
$erro = ''; $sucesso = false;

$u = null;
if ($token !== '') {
    $st = $pdo->prepare('SELECT id, nome, reset_expira FROM usuarios WHERE reset_token = ?');
    $st->execute([$token]);
    $u = $st->fetch() ?: null;
}
$valido = $u && new DateTime($u['reset_expira']) > new DateTime();

if ($_SERVER['REQUEST_METHOD'] === 'POST' && $valido) {
    if (!hash_equals($_SESSION['csrf'] ?? '', $_POST['csrf'] ?? '')) {
        $erro = 'Sessão expirada. Recarregue a página e tente de novo.';
    } else {
        $senha = $_POST['senha'] ?? '';
        $confirmar = $_POST['confirmar'] ?? '';
        if (strlen($senha) < 6) {
            $erro = 'A senha precisa ter pelo menos 6 caracteres.';
        } elseif ($senha !== $confirmar) {
            $erro = 'As senhas não coincidem.';
        } else {
            $pdo->prepare('UPDATE usuarios SET senha_hash = ?, reset_token = NULL, reset_expira = NULL WHERE id = ?')
                ->execute([password_hash($senha, PASSWORD_DEFAULT), $u['id']]);
            $sucesso = true;
        }
    }
}
if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(32));
?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Criar nova senha · LISA</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --creme-fundo:#FFFFFF; --creme-cartao:#FCF6EC;
  --marrom:#3B2A1C; --marrom-suave:#7A6350;
  --teal:#0F4743; --teal-escuro:#0A3330;
  --linha:#E6D7C1; --erro:#B3261E; --erro-bg:#FBEAE8;
  --sucesso:#1E7A43; --sucesso-bg:#E3F3E8;
}
*{box-sizing:border-box;margin:0}
html,body{height:100%}
body{font-family:'Manrope',system-ui,sans-serif;color:var(--marrom);background:var(--creme-fundo);
  background-image:radial-gradient(rgba(59,42,28,.09) 1.3px,transparent 1.4px);background-size:26px 26px;
  -webkit-font-smoothing:antialiased;display:flex;align-items:center;justify-content:center;
  min-height:100vh;padding:32px}
.cartao{width:100%;max-width:390px;background:var(--creme-cartao);border-radius:20px;
  padding:40px 36px 44px;box-shadow:0 18px 40px rgba(59,42,28,.14)}
h1{font-size:1.45rem;font-weight:700;margin-bottom:6px}
.sub{color:var(--marrom-suave);font-size:.92rem;font-weight:600;margin-bottom:26px;line-height:1.4}
.campo{margin-bottom:18px}
label{display:block;font-size:.85rem;font-weight:700;color:var(--marrom);margin-bottom:6px}
input{width:100%;height:46px;padding:0 14px;font:inherit;font-size:.95rem;color:var(--marrom);
  background:#fff;border:1px solid var(--linha);border-radius:10px}
input:focus{outline:none;border-color:var(--teal);box-shadow:0 0 0 3px rgba(15,71,67,.14)}
.btn{width:100%;height:48px;margin-top:6px;border:0;border-radius:10px;background:var(--teal);color:#fff;
  font:inherit;font-weight:700;font-size:.95rem;cursor:pointer}
.btn:hover{background:var(--teal-escuro)}
.erro{background:var(--erro-bg);color:var(--erro);border-radius:10px;padding:11px 14px;
  font-size:.86rem;line-height:1.4;margin-bottom:18px;font-weight:600}
.sucesso{background:var(--sucesso-bg);color:var(--sucesso);border-radius:10px;padding:14px;
  font-size:.88rem;line-height:1.45;margin-bottom:6px;font-weight:600}
.voltar{display:block;text-align:center;margin-top:20px;font-size:.85rem;font-weight:700;
  color:var(--teal);text-decoration:none}
.voltar:hover{text-decoration:underline}
</style>
</head>
<body>
<div class="cartao">

  <?php if ($sucesso): ?>
    <h1>Senha atualizada!</h1>
    <div class="sucesso" style="margin-top:14px">Sua senha foi alterada com sucesso. Você já pode entrar com ela.</div>
    <a class="voltar" href="index.php">Ir para o login</a>

  <?php elseif (!$valido): ?>
    <h1>Link inválido ou expirado</h1>
    <p class="sub">Esse link de redefinição não existe mais, ou o prazo de 2 horas já passou. Peça um novo.</p>
    <a class="voltar" href="esqueci-senha.php" style="margin-top:0">Pedir novo link</a>

  <?php else: ?>
    <h1>Criar nova senha</h1>
    <p class="sub">Olá, <?= h($u['nome']) ?>. Escolha uma nova senha para sua conta.</p>

    <?php if ($erro): ?><div class="erro" role="alert"><?= h($erro) ?></div><?php endif; ?>

    <form method="post" action="redefinir-senha.php" novalidate>
      <input type="hidden" name="csrf" value="<?= h($_SESSION['csrf']) ?>">
      <input type="hidden" name="token" value="<?= h($token) ?>">
      <div class="campo">
        <label for="senha">Nova senha</label>
        <input id="senha" name="senha" type="password" required autofocus autocomplete="new-password">
      </div>
      <div class="campo">
        <label for="confirmar">Confirmar nova senha</label>
        <input id="confirmar" name="confirmar" type="password" required autocomplete="new-password">
      </div>
      <button class="btn" type="submit">Salvar nova senha</button>
    </form>
    <a class="voltar" href="index.php">Cancelar e voltar ao login</a>
  <?php endif; ?>

</div>
</body>
</html>