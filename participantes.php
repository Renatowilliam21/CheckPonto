<?php
require __DIR__ . '/config.php';
if (empty($_SESSION['usuario'])) { header('Location: index.php'); exit; }
$u = $_SESSION['usuario'];
$pdo = db();

$rotulosPerfil = ['participante' => 'Participante', 'tecnico' => 'Técnico',
                  'coordenador' => 'Coordenador', 'administrador' => 'Administrador'];

// --- Cadastrar ou atualizar ---
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
        $_SESSION['flash_erro'] = 'Sessão expirada, tente novamente.';
    } else {
        $id = (int)($_POST['id'] ?? 0);
        $nome = trim($_POST['nome'] ?? '');
        $matricula = trim($_POST['matricula'] ?? '');
        $email = trim($_POST['email'] ?? '');
        $perfil = array_key_exists($_POST['perfil'] ?? '', $rotulosPerfil) ? $_POST['perfil'] : 'participante';
        $ativo = isset($_POST['ativo']) ? 1 : 0;
        $senha = $_POST['senha'] ?? '';

        if ($nome === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $_SESSION['flash_erro'] = 'Informe o nome e um e-mail válido.';
        } elseif ($id > 0) {
            if ($senha !== '') {
                $pdo->prepare('UPDATE usuarios SET nome=?, matricula=?, email=?, perfil=?, ativo=?, senha_hash=? WHERE id=?')
                    ->execute([$nome, $matricula ?: null, $email, $perfil, $ativo, password_hash($senha, PASSWORD_DEFAULT), $id]);
            } else {
                $pdo->prepare('UPDATE usuarios SET nome=?, matricula=?, email=?, perfil=?, ativo=? WHERE id=?')
                    ->execute([$nome, $matricula ?: null, $email, $perfil, $ativo, $id]);
            }
            $_SESSION['flash_sucesso'] = 'Participante atualizado.';
        } else {
            try {
                $pdo->prepare('INSERT INTO usuarios (nome, matricula, email, perfil, ativo, senha_hash) VALUES (?,?,?,?,?,?)')
                    ->execute([$nome, $matricula ?: null, $email, $perfil, $ativo,
                               $senha !== '' ? password_hash($senha, PASSWORD_DEFAULT) : null]);
                $_SESSION['flash_sucesso'] = 'Participante cadastrado.';
            } catch (PDOException $e) {
                $_SESSION['flash_erro'] = 'Não foi possível cadastrar: e-mail ou matrícula já usados por outro participante.';
            }
        }
    }
    header('Location: participantes.php'); exit;
}

// --- Dados para edição ---
$edicao = null;
if (isset($_GET['editar'])) {
    $st = $pdo->prepare('SELECT * FROM usuarios WHERE id = ?');
    $st->execute([(int)$_GET['editar']]);
    $edicao = $st->fetch() ?: null;
}

// --- Busca e filtros ---
$busca  = trim($_GET['busca'] ?? '');
$fPerfil = $_GET['perfil'] ?? '';
$fStatus = $_GET['status'] ?? '';

$condicoes = []; $parametros = [];
if ($busca !== '') {
    $condicoes[] = '(nome LIKE ? OR email LIKE ? OR matricula LIKE ?)';
    array_push($parametros, "%$busca%", "%$busca%", "%$busca%");
}
if (array_key_exists($fPerfil, $rotulosPerfil)) {
    $condicoes[] = 'perfil = ?';
    $parametros[] = $fPerfil;
}
if ($fStatus === 'ativo' || $fStatus === 'inativo') {
    $condicoes[] = 'ativo = ?';
    $parametros[] = $fStatus === 'ativo' ? 1 : 0;
}
$where = $condicoes ? 'WHERE ' . implode(' AND ', $condicoes) : '';

$st = $pdo->prepare("SELECT * FROM usuarios $where ORDER BY nome");
$st->execute($parametros);
$participantes = $st->fetchAll();

$erro = $_SESSION['flash_erro'] ?? ''; unset($_SESSION['flash_erro']);
$sucesso = $_SESSION['flash_sucesso'] ?? ''; unset($_SESSION['flash_sucesso']);

$tituloPagina = 'Participantes · CheckPonto';
$pagina_ativa = 'participantes';
require __DIR__ . '/includes/layout-topo.php';
?>

<h1 style="font-size:1.6rem;font-weight:700;margin-bottom:4px">Participantes</h1>
<p style="color:var(--suave);font-size:.92rem;margin-bottom:22px">Gerencie os membros dos laboratórios e projetos</p>

<?php if ($erro): ?><div class="aviso erro"><?= h($erro) ?></div><?php endif; ?>
<?php if ($sucesso): ?><div class="aviso sucesso"><?= h($sucesso) ?></div><?php endif; ?>

<div class="cartao" style="margin-bottom:26px">
  <h2 style="font-size:1rem;font-weight:700;margin-bottom:16px">
    <?= $edicao ? 'Editar participante' : 'Novo participante' ?>
  </h2>
  <form method="post" action="participantes.php">
    <input type="hidden" name="csrf" value="<?= h($_SESSION['csrf']) ?>">
    <?php if ($edicao): ?><input type="hidden" name="id" value="<?= $edicao['id'] ?>"><?php endif; ?>
    <div class="grade-form" style="margin-bottom:16px">
      <div class="campo">
        <label for="nome">Nome</label>
        <input type="text" id="nome" name="nome" required value="<?= h($edicao['nome'] ?? '') ?>">
      </div>
      <div class="campo">
        <label for="matricula">Matrícula</label>
        <input type="text" id="matricula" name="matricula" value="<?= h($edicao['matricula'] ?? '') ?>">
      </div>
      <div class="campo">
        <label for="email">E-mail</label>
        <input type="text" id="email" name="email" required value="<?= h($edicao['email'] ?? '') ?>">
      </div>
      <div class="campo">
        <label for="perfil">Perfil</label>
        <select id="perfil" name="perfil">
          <?php foreach ($rotulosPerfil as $valor => $rotulo): ?>
            <option value="<?= $valor ?>" <?= ($edicao['perfil'] ?? 'participante') === $valor ? 'selected' : '' ?>><?= $rotulo ?></option>
          <?php endforeach; ?>
        </select>
      </div>
      <div class="campo">
        <label for="senha"><?= $edicao ? 'Nova senha (opcional)' : 'Senha (opcional)' ?></label>
        <input type="password" id="senha" name="senha" placeholder="<?= $edicao ? 'Deixe em branco para manter' : 'Deixe em branco p/ login só por Google' ?>">
      </div>
      <div class="campo" style="display:flex;align-items:flex-end;padding-bottom:10px">
        <label style="display:flex;align-items:center;gap:8px;font-weight:500">
          <input type="checkbox" name="ativo" <?= ($edicao['ativo'] ?? 1) ? 'checked' : '' ?> style="width:16px;height:16px"> Participante ativo
        </label>
      </div>
    </div>
    <button type="submit" class="btn-primario"><?= $edicao ? 'Salvar alterações' : 'Cadastrar participante' ?></button>
    <?php if ($edicao): ?>
      <a class="acao-link" href="participantes.php" style="margin-left:14px">Cancelar edição</a>
    <?php endif; ?>
  </form>
</div>

<form method="get" action="participantes.php" style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px">
  <input type="text" name="busca" placeholder="Buscar por nome, e-mail ou matrícula..." value="<?= h($busca) ?>"
         style="flex:2;min-width:220px;height:42px;padding:0 12px;border:1px solid var(--linha);border-radius:8px;font:inherit">
  <select name="perfil" style="height:42px;border:1px solid var(--linha);border-radius:8px;padding:0 10px;font:inherit">
    <option value="">Todos os perfis</option>
    <?php foreach ($rotulosPerfil as $valor => $rotulo): ?>
      <option value="<?= $valor ?>" <?= $fPerfil === $valor ? 'selected' : '' ?>><?= $rotulo ?></option>
    <?php endforeach; ?>
  </select>
  <select name="status" style="height:42px;border:1px solid var(--linha);border-radius:8px;padding:0 10px;font:inherit">
    <option value="">Todos os status</option>
    <option value="ativo" <?= $fStatus === 'ativo' ? 'selected' : '' ?>>Ativo</option>
    <option value="inativo" <?= $fStatus === 'inativo' ? 'selected' : '' ?>>Inativo</option>
  </select>
  <button type="submit" class="btn-primario">Filtrar</button>
</form>

<div class="cartao" style="padding:0;overflow:hidden">
  <table class="tabela">
    <thead><tr><th>Nome</th><th>Matrícula</th><th>E-mail</th><th>Perfil</th><th>Status</th><th>Ações</th></tr></thead>
    <tbody>
      <?php if (!$participantes): ?><tr><td colspan="6" style="padding:18px;color:var(--suave)">Nenhum participante encontrado.</td></tr><?php endif; ?>
      <?php foreach ($participantes as $p): ?>
        <tr>
          <td>
            <div style="display:flex;align-items:center;gap:10px">
              <div style="width:30px;height:30px;border-radius:50%;background:<?= h(avatar_cor((int)$p['id'])) ?>;
                          color:#fff;display:flex;align-items:center;justify-content:center;font-size:.72rem;font-weight:700;flex:none">
                <?= h(iniciais_nome($p['nome'])) ?>
              </div>
              <span style="font-weight:600"><?= h($p['nome']) ?></span>
            </div>
          </td>
          <td style="color:var(--suave)"><?= h($p['matricula'] ?? '—') ?></td>
          <td style="color:var(--suave)"><?= h($p['email']) ?></td>
          <td><span class="pilula <?= h($p['perfil']) ?>"><?= h($rotulosPerfil[$p['perfil']]) ?></span></td>
          <td><span class="pilula <?= $p['ativo'] ? 'ativo' : 'inativo' ?>"><?= $p['ativo'] ? 'Ativo' : 'Inativo' ?></span></td>
          <td><a class="acao-link" href="participantes.php?editar=<?= $p['id'] ?>">Editar</a></td>
        </tr>
      <?php endforeach; ?>
    </tbody>
  </table>
</div>

<?php require __DIR__ . '/includes/layout-rodape.php'; ?>