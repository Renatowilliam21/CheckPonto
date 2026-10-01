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
        $st = db()->prepare('SELECT id, nome, email, senha_hash FROM usuarios WHERE email = ? AND ativo = 1');
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
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;800&display=swap" rel="stylesheet">
<script src="https://accounts.google.com/gsi/client" async defer></script>
<style>
:root{
  --papel:#F5F7F8; --tinta:#13232B; --suave:#5A6B73; --linha:#D3DCE0;
  --lab:#0E4F61; --lab-escuro:#0A3A48; --erro:#B3261E; --erro-bg:#FBEAE8;
}
*{box-sizing:border-box;margin:0}
html,body{height:100%}
body{font-family:'Manrope',system-ui,sans-serif;color:var(--tinta);background:var(--papel);
  display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);-webkit-font-smoothing:antialiased}

/* Coluna do formulário */
main{display:flex;align-items:center;justify-content:center;padding:32px 24px}
.caixa{width:100%;max-width:360px}
.marca{font-weight:800;letter-spacing:.14em;font-size:1rem;color:var(--lab);margin-bottom:56px}
h1{font-size:1.75rem;font-weight:600;letter-spacing:-.01em;margin-bottom:8px}
.sub{color:var(--suave);font-size:.95rem;line-height:1.5;margin-bottom:32px}

.campo{margin-bottom:18px}
label{display:block;font-size:.85rem;font-weight:500;margin-bottom:6px}
.entrada{position:relative}
input{width:100%;height:46px;padding:0 14px;font:inherit;font-size:.95rem;color:var(--tinta);
  background:#fff;border:1px solid var(--linha);border-radius:8px;transition:border-color .15s,box-shadow .15s}
input:hover{border-color:#B5C2C8}
input:focus{outline:none;border-color:var(--lab);box-shadow:0 0 0 3px rgba(14,79,97,.16)}
.entrada input{padding-right:64px}
.ver{position:absolute;right:6px;top:6px;height:34px;padding:0 10px;border:0;background:none;
  font:inherit;font-size:.8rem;font-weight:600;color:var(--suave);border-radius:6px;cursor:pointer}
.ver:hover{color:var(--lab)}
.ver:focus-visible,.btn:focus-visible{outline:2px solid var(--lab);outline-offset:2px}

.btn{width:100%;height:46px;margin-top:8px;border:0;border-radius:8px;background:var(--lab);color:#fff;
  font:inherit;font-weight:600;font-size:.95rem;cursor:pointer;transition:background .15s}
.btn:hover{background:var(--lab-escuro)}

.ou{display:flex;align-items:center;gap:14px;margin:26px 0;color:var(--suave);font-size:.85rem}
.ou::before,.ou::after{content:"";flex:1;height:1px;background:var(--linha)}
.google{display:flex;justify-content:center;min-height:44px}

.erro{background:var(--erro-bg);color:var(--erro);border-radius:8px;padding:11px 14px;
  font-size:.88rem;line-height:1.4;margin-bottom:20px}
.rodape{margin-top:40px;font-size:.8rem;color:var(--suave)}

/* Painel lateral: o único gesto visual da página */
aside{position:relative;overflow:hidden;background:var(--lab);color:#fff;display:flex;
  align-items:flex-end;padding:56px;
  background-image:radial-gradient(rgba(255,255,255,.16) 1.2px,transparent 1.3px);background-size:22px 22px}
aside::after{content:"";position:absolute;inset:0;
  background:linear-gradient(200deg,transparent 35%,var(--lab-escuro) 100%)}
.grande{position:relative;z-index:1;font-weight:800;font-size:clamp(5rem,13vw,11rem);
  line-height:.85;letter-spacing:-.03em}
.grande small{display:block;margin-top:20px;font-size:1rem;font-weight:500;letter-spacing:0;opacity:.8}

@media (max-width:860px){
  body{grid-template-columns:1fr}
  aside{display:none}
  .marca{margin-bottom:40px}
}
</style>
</head>
<body>
<main>
  <div class="caixa">
    <div class="marca">LISA</div>
    <h1>Entrar</h1>
    <p class="sub">Acesse o sistema de controle de acesso do laboratório.</p>

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
      </div>
      <button class="btn" type="submit">Entrar</button>
    </form>

    <div class="ou">ou</div>

    <div id="g_id_onload"
         data-client_id="<?= h(GOOGLE_CLIENT_ID) ?>"
         data-login_uri="<?= h($base) ?>/google-callback.php"
         data-ux_mode="redirect" data-auto_prompt="false"></div>
    <div class="google">
      <div class="g_id_signin" data-type="standard" data-shape="rectangular" data-theme="outline"
           data-text="signin_with" data-size="large" data-logo_alignment="left"
           data-width="360" data-locale="pt-BR"></div>
    </div>

    <p class="rodape">Problemas para entrar? Fale com a coordenação do LISA.</p>
  </div>
</main>

<aside aria-hidden="true">
  <div class="grande">LISA<small>Laboratório</small></div>
</aside>

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
