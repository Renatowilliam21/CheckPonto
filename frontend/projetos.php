<?php
require __DIR__ . '/config.php';
if (empty($_SESSION['usuario'])) { header('Location: index.php'); exit; }
$u = $_SESSION['usuario'];
$pdo = db();

// --- Ativar/Desativar ---
if (isset($_GET['alternar'])) {
    $pdo->prepare('UPDATE projetos SET ativo = NOT ativo WHERE id = ?')->execute([(int)$_GET['alternar']]);
    header('Location: projetos.php'); exit;
}

// --- Excluir ---
if (isset($_GET['excluir'])) {
    $pid = (int)$_GET['excluir'];
    $st = $pdo->prepare('SELECT COUNT(*) FROM atividades WHERE projeto_id = ?');
    $st->execute([$pid]);
    if ($st->fetchColumn() > 0) {
        $_SESSION['flash_erro'] = 'Não é possível excluir: existem atividades vinculadas a este projeto. Desative-o em vez de excluir.';
    } else {
        $pdo->prepare('DELETE FROM participantes_projetos WHERE projeto_id = ?')->execute([$pid]);
        $pdo->prepare('DELETE FROM projetos WHERE id = ?')->execute([$pid]);
        $_SESSION['flash_sucesso'] = 'Projeto excluído.';
    }
    header('Location: projetos.php'); exit;
}

// --- Cadastrar novo projeto ---
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
        $_SESSION['flash_erro'] = 'Sessão expirada, tente novamente.';
    } else {
        $nome = trim($_POST['nome'] ?? '');
        $laboratorio_id = (int)($_POST['laboratorio_id'] ?? 0);
        $ativo = isset($_POST['ativo']) ? 1 : 0;
        $participantes = array_map('intval', $_POST['participantes'] ?? []);

        if ($nome === '' || $laboratorio_id === 0) {
            $_SESSION['flash_erro'] = 'Informe o nome do projeto e o laboratório.';
        } else {
            $pdo->prepare('INSERT INTO projetos (nome, laboratorio_id, ativo) VALUES (?,?,?)')
                ->execute([$nome, $laboratorio_id, $ativo]);
            $projeto_id = $pdo->lastInsertId();
            $ins = $pdo->prepare('INSERT IGNORE INTO participantes_projetos (usuario_id, projeto_id) VALUES (?,?)');
            foreach ($participantes as $uid) $ins->execute([$uid, $projeto_id]);
            $_SESSION['flash_sucesso'] = 'Projeto cadastrado.';
        }
    }
    header('Location: projetos.php'); exit;
}

$laboratorios = $pdo->query('SELECT id, nome FROM laboratorios ORDER BY nome')->fetchAll();
$usuarios = $pdo->query('SELECT id, nome FROM usuarios WHERE ativo = 1 ORDER BY nome')->fetchAll();
$projetos = $pdo->query("SELECT p.*, l.nome AS laboratorio_nome, COUNT(pp.usuario_id) AS total_participantes
                          FROM projetos p
                          JOIN laboratorios l ON l.id = p.laboratorio_id
                          LEFT JOIN participantes_projetos pp ON pp.projeto_id = p.id
                          GROUP BY p.id ORDER BY p.nome")->fetchAll();

$erro = $_SESSION['flash_erro'] ?? ''; unset($_SESSION['flash_erro']);
$sucesso = $_SESSION['flash_sucesso'] ?? ''; unset($_SESSION['flash_sucesso']);

$tituloPagina = 'Projetos · CheckPonto';
$pagina_ativa = 'projetos';
require __DIR__ . '/includes/layout-topo.php';
?>

<h1 style="font-size:1.6rem;font-weight:700;margin-bottom:4px">Projetos</h1>
<p style="color:var(--suave);font-size:.92rem;margin-bottom:22px">Cadastre os projetos do laboratório e quem participa de cada um</p>

<?php if ($erro): ?><div class="aviso erro"><?= h($erro) ?></div><?php endif; ?>
<?php if ($sucesso): ?><div class="aviso sucesso"><?= h($sucesso) ?></div><?php endif; ?>

<?php if (!$laboratorios): ?>
  <div class="aviso erro">Cadastre pelo menos um laboratório na tabela <code>laboratorios</code> antes de criar projetos.</div>
<?php else: ?>
<div class="cartao" style="margin-bottom:26px">
  <h2 style="font-size:1rem;font-weight:700;margin-bottom:16px">Novo projeto</h2>
  <form method="post" action="projetos.php">
    <input type="hidden" name="csrf" value="<?= h($_SESSION['csrf']) ?>">
    <div class="grade-form" style="margin-bottom:16px">
      <div class="campo">
        <label for="nome">Nome do projeto</label>
        <input type="text" id="nome" name="nome" required placeholder="Ex.: IA na Saúde">
      </div>
      <div class="campo">
        <label for="laboratorio_id">Laboratório</label>
        <select id="laboratorio_id" name="laboratorio_id" required>
          <option value="">Selecione...</option>
          <?php foreach ($laboratorios as $l): ?>
            <option value="<?= $l['id'] ?>"><?= h($l['nome']) ?></option>
          <?php endforeach; ?>
        </select>
      </div>
      <div class="campo" style="display:flex;align-items:flex-end;padding-bottom:10px">
        <label style="display:flex;align-items:center;gap:8px;font-weight:500">
          <input type="checkbox" name="ativo" checked style="width:16px;height:16px"> Projeto ativo
        </label>
      </div>
    </div>
    <div class="campo" style="margin-bottom:18px">
      <label>Participantes</label>
      <div class="checkboxes">
        <?php if (!$usuarios): ?><span style="color:var(--suave);font-size:.85rem">Nenhum usuário cadastrado ainda.</span><?php endif; ?>
        <?php foreach ($usuarios as $usr): ?>
          <label><input type="checkbox" name="participantes[]" value="<?= $usr['id'] ?>"> <?= h($usr['nome']) ?></label>
        <?php endforeach; ?>
      </div>
    </div>
    <button type="submit" class="btn-primario">Cadastrar projeto</button>
  </form>
</div>
<?php endif; ?>

<div class="cartao" style="padding:0;overflow:hidden">
  <table class="tabela">
    <thead><tr><th>Nome</th><th>Laboratório</th><th>Participantes</th><th>Status</th><th>Ações</th></tr></thead>
    <tbody>
      <?php if (!$projetos): ?><tr><td colspan="5" style="padding:18px;color:var(--suave)">Nenhum projeto cadastrado.</td></tr><?php endif; ?>
      <?php foreach ($projetos as $p): ?>
        <tr>
          <td style="font-weight:600"><?= h($p['nome']) ?></td>
          <td style="color:var(--suave)"><?= h($p['laboratorio_nome']) ?></td>
          <td style="color:var(--suave)"><?= (int)$p['total_participantes'] ?></td>
          <td><span class="pilula <?= $p['ativo'] ? 'ativo' : 'inativo' ?>"><?= $p['ativo'] ? 'Ativo' : 'Inativo' ?></span></td>
          <td>
            <a class="acao-link" href="projetos.php?alternar=<?= $p['id'] ?>"><?= $p['ativo'] ? 'Desativar' : 'Ativar' ?></a>
            &nbsp;·&nbsp;
            <a class="acao-link perigo" href="projetos.php?excluir=<?= $p['id'] ?>" onclick="return confirm('Excluir este projeto?')">Excluir</a>
          </td>
        </tr>
      <?php endforeach; ?>
    </tbody>
  </table>
</div>

<?php require __DIR__ . '/includes/layout-rodape.php'; ?>