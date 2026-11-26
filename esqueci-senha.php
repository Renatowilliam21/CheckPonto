<?php
require __DIR__ . '/config.php';
if (!empty($_SESSION['usuario'])) { header('Location: painel.php'); exit; }
if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(32));

$mensagem = ''; $erro = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
        $erro = 'Sessão expirada. Recarregue a página e tente de novo.';
    } else {
        $email = trim($_POST['email'] ?? '');
        if (filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $pdo = db();
            $st = $pdo->prepare('SELECT id, nome FROM usuarios WHERE email = ? AND ativo = 1');
            $st->execute([$email]);
            $u = $st->fetch();
            if ($u) {
                $token = bin2hex(random_bytes(32));
                $expira = (new DateTime('+2 hours'))->format('Y-m-d H:i:s');
                $pdo->prepare('UPDATE usuarios SET reset_token = ?, reset_expira = ? WHERE id = ?')
                    ->execute([$token, $expira, $u['id']]);

                $base = (!empty($_SERVER['HTTPS']) ? 'https' : 'http') . '://' . $_SERVER['HTTP_HOST']
                      . rtrim(dirname($_SERVER['SCRIPT_NAME']), '/\\');
                $link = "$base/redefinir-senha.php?token=$token";

                $assunto = 'Redefinição de senha - CheckPonto LISA';
                $corpo   = "Olá, {$u['nome']}!\n\n"
                         . "Recebemos um pedido para redefinir sua senha no CheckPonto.\n"
                         . "Clique no link abaixo para criar uma nova senha (válido por 2 horas):\n\n"
                         . "$link\n\n"
                         . "Se você não pediu isso, pode ignorar este e-mail com segurança.";
                enviar_email($email, $u['nome'], $assunto, $corpo);
            }
        }
        // Mensagem sempre igual, para não revelar se o e-mail existe ou não no sistema
        $mensagem = 'Pedido registrado! Se esse e-mail estiver cadastrado, o link de redefinição será enviado a você por e-mail ou entregue pelo professor responsável. O link vale por 2 horas.';
        $_SESSION['csrf'] = bin2hex(random_bytes(32));
    }
}
?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Esqueci minha senha · LISA</title>
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
  font-size:.88rem;line-height:1.45;margin-bottom:18px;font-weight:600}
.voltar{display:block;text-align:center;margin-top:20px;font-size:.85rem;font-weight:700;
  color:var(--teal);text-decoration:none}
.voltar:hover{text-decoration:underline}
</style>
</head>
<body>
<div class="cartao">
  <h1>Esqueci minha senha</h1>
  <p class="sub">Informe seu e-mail de login. Vamos enviar um link para você criar uma senha nova.</p>

  <?php if ($erro): ?><div class="erro" role="alert"><?= h($erro) ?></div><?php endif; ?>
  <?php if ($mensagem): ?><div class="sucesso"><?= h($mensagem) ?></div><?php endif; ?>

  <form method="post" action="esqueci-senha.php" novalidate>
    <input type="hidden" name="csrf" value="<?= h($_SESSION['csrf']) ?>">
    <div class="campo">
      <label for="email">E-mail</label>
      <input id="email" name="email" type="email" required autofocus placeholder="nome@instituicao.br">
    </div>
    <button class="btn" type="submit">Enviar link de redefinição</button>
  </form>

  <a class="voltar" href="index.php">Voltar para o login</a>
</div>
</body>
</html>