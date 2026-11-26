<?php
require __DIR__ . '/config.php';

header('Referrer-Policy: no-referrer-when-downgrade');

if (!empty($_SESSION['usuario'])) { header('Location: painel.php'); exit; }
if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(32));

$erro  = $_SESSION['flash_erro'] ?? '';
unset($_SESSION['flash_erro']);
$email = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = trim($_POST['email'] ?? '');
    $senha = $_POST['senha'] ?? '';

    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
        $erro = 'Sessão expirada. Recarregue a página e tente de novo.';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL) || $senha === '') {
        $erro = 'Informe um e-mail válido e a senha.';
    } else {
        $st = db()->prepare('SELECT id, nome, email, senha_hash, perfil FROM usuarios WHERE email = ? AND ativo = 1');
        $st->execute([$email]);
        $u = $st->fetch();
        if ($u && $u['senha_hash'] && password_verify($senha, $u['senha_hash'])) {
            iniciar_sessao($u);
            header('Location: painel.php'); exit;
        }
        $erro = 'E-mail ou senha incorretos.';
    }
}

$base = (!empty($_SERVER['HTTPS']) ? 'https' : 'http') . '://' . $_SERVER['HTTP_HOST']
      . rtrim(dirname($_SERVER['SCRIPT_NAME']), '/\\');
?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Entrar · LISA</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
<script src="https://accounts.google.com/gsi/client" async defer></script>
<style>
:root{
  --creme-fundo:#FFFFFF; --creme-cartao:#FCF6EC;
  --marrom:#3B2A1C; --marrom-suave:#7A6350;
  --teal:#0F4743; --teal-escuro:#0A3330;
  --laranja:#F0A61E;
  --linha:#E6D7C1; --erro:#B3261E; --erro-bg:#FBEAE8;
}
*{box-sizing:border-box;margin:0}
html,body{height:100%}
body{
  font-family:'Manrope',system-ui,sans-serif;color:var(--marrom);background:var(--creme-fundo);
  background-image:radial-gradient(rgba(59,42,28,.09) 1.3px,transparent 1.4px);
  background-size:26px 26px;-webkit-font-smoothing:antialiased;
  display:flex;align-items:center;justify-content:space-between;gap:40px;
  min-height:100vh;padding:56px 64px;flex-wrap:wrap
}

/* ---- Logo / ilustração ---- */
.marca {
  flex: 1;
  min-width: 960px;
  max-width: 1920px;
  align-self: stretch;

  display: flex;
  flex-direction: column;
  justify-content: center; /* Centraliza verticalmente */
  align-items: flex-end;    /* Empurra o logo para a direita, aproximando-o do login */
  padding-right: 40px;     /* Cria uma margem confortável antes do card de login */
}

.marca img {
  width: 100%;
  max-width: 500px;        /* Define um tamanho limite para não estourar */
  height: auto;
  object-fit: contain;     /* IMPEDE A DISTORÇÃO da imagem */
}


/* ---- Cartão de login ---- */
.cartao{width:100%;max-width:390px;background:var(--creme-cartao);border-radius:20px;
  padding:40px 36px 44px;box-shadow:0 18px 40px rgba(59,42,28,.14)}
h1{font-size:1.45rem;font-weight:700;margin-bottom:6px}
.sub{color:var(--marrom-suave);font-size:.92rem;font-weight:600;margin-bottom:26px}
.campo{margin-bottom:18px}
label{display:block;font-size:.85rem;font-weight:700;color:var(--marrom);margin-bottom:6px}
.link-pequeno{font-size:.8rem;font-weight:700;color:var(--teal);text-decoration:none}
.link-pequeno:hover{text-decoration:underline}

.entrada{position:relative}
input{width:100%;height:46px;padding:0 14px;font:inherit;font-size:.95rem;color:var(--marrom);
  background:#fff;border:1px solid var(--linha);border-radius:10px;transition:border-color .15s,box-shadow .15s}
input::placeholder{color:#B7A890}
input:hover{border-color:#D8C4A5}
input:focus{outline:none;border-color:var(--teal);box-shadow:0 0 0 3px rgba(15,71,67,.14)}
.entrada input{padding-right:70px}
.ver{position:absolute;right:6px;top:6px;height:34px;padding:0 10px;border:0;background:none;
  font:inherit;font-size:.78rem;font-weight:700;color:var(--teal);border-radius:6px;cursor:pointer}
.ver:hover{text-decoration:underline}
.ver:focus-visible,.btn:focus-visible,.google-falso:focus-visible{outline:2px solid var(--teal);outline-offset:2px}

.btn{width:100%;height:48px;margin-top:10px;border:0;border-radius:10px;background:var(--teal);color:#fff;
  font:inherit;font-weight:700;font-size:.95rem;cursor:pointer;transition:background .15s}
.btn:hover{background:var(--teal-escuro)}

.ou{display:flex;align-items:center;gap:14px;margin:22px 0;color:var(--marrom-suave);font-size:.8rem;font-weight:600}
.ou::before,.ou::after{content:"";flex:1;height:1px;background:var(--linha)}

.google-caixa{position:relative;height:48px}
.google-caixa .g_id_signin{position:absolute;inset:0;opacity:.01;overflow:hidden}
.google-falso{position:absolute;inset:0;pointer-events:none;display:flex;align-items:center;
  justify-content:center;gap:10px;background:#fff;border:1px solid var(--linha);border-radius:10px;
  font:inherit;font-weight:700;font-size:.92rem;color:var(--marrom)}

.erro{background:var(--erro-bg);color:var(--erro);border-radius:10px;padding:11px 14px;
  font-size:.86rem;line-height:1.4;margin-bottom:18px;font-weight:600}

@media (max-width:860px){ .marca{display:none} body{justify-content:center;padding:32px 20px} }
</style>
</head>
<body>

<img class="marca" src="assets/logo-lisa.png" alt="LISA · Laboratório de Inovação para Desenvolvimento do Semiárido">


<div class="cartao">
  <h1>Bem-vindo ao LISA</h1>
  <p class="sub">Entre para acessar seu laboratório</p>

  <?php if ($erro): ?>
    <div class="erro" role="alert"><?= h($erro) ?></div>
  <?php endif; ?>

  <form method="post" action="index.php" novalidate>
    <input type="hidden" name="csrf" value="<?= h($_SESSION['csrf']) ?>">
    <div class="campo">
      <label for="email">E-mail</label>
      <input id="email" name="email" type="email" autocomplete="username" required autofocus
             value="<?= h($email) ?>" placeholder="nome@instituicao.br">
    </div>
    <div class="campo">
      <label for="senha">Senha</label>
      <div class="entrada">
        <input id="senha" name="senha" type="password" autocomplete="current-password" required>
        <button class="ver" type="button" aria-controls="senha">Mostrar</button>
      </div>
      <a class="link-pequeno" href="esqueci-senha.php" style="display:inline-block;margin-top:8px">Esqueci minha senha</a>
    </div>
    <button class="btn" type="submit">Entrar</button>
  </form>

  <div class="ou">ou</div>

  <div id="g_id_onload"
       data-client_id="<?= h(GOOGLE_CLIENT_ID) ?>"
       data-login_uri="<?= h($base) ?>/google-callback.php"
       data-ux_mode="redirect" data-auto_prompt="false"></div>
  <div class="google-caixa">
    <div class="g_id_signin" data-type="standard" data-shape="rectangular" data-theme="outline"
         data-text="continue_with" data-size="large" data-logo_alignment="left"
         data-width="320" data-locale="pt-BR"></div>
    <button type="button" class="google-falso" tabindex="-1" aria-hidden="true">
      <svg width="18" height="18" viewBox="0 0 18 18">
        <path fill="#4285F4" d="M17.6 9.2c0-.6-.1-1.2-.2-1.8H9v3.4h4.8c-.2 1.1-.8 2-1.8 2.7v2.2h2.9c1.7-1.6 2.7-3.9 2.7-6.5z"/>
        <path fill="#34A853" d="M9 18c2.4 0 4.5-.8 6-2.2l-2.9-2.2c-.8.5-1.8.9-3.1.9-2.4 0-4.4-1.6-5.1-3.7H.9v2.3C2.5 15.9 5.5 18 9 18z"/>
        <path fill="#FBBC05" d="M3.9 10.8c-.2-.5-.3-1.2-.3-1.8s.1-1.3.3-1.8V4.9H.9C.3 6.1 0 7.5 0 9s.3 2.9.9 4.1l3-2.3z"/>
        <path fill="#EA4335" d="M9 3.6c1.3 0 2.5.4 3.4 1.3l2.6-2.6C13.5.9 11.4 0 9 0 5.5 0 2.5 2.1.9 4.9l3 2.3C4.6 5.1 6.6 3.6 9 3.6z"/>
      </svg>
      Continuar com Google
    </button>
  </div>
</div>

<script>
const s = document.getElementById('senha'), b = document.querySelector('.ver');
b.addEventListener('click', () => {
  const mostrar = s.type === 'password';
  s.type = mostrar ? 'text' : 'password';
  b.textContent = mostrar ? 'Ocultar' : 'Mostrar';
});
</script>
</body>
</html>