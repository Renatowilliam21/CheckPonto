<?php
require __DIR__ . '/config.php';
if (empty($_SESSION['usuario'])) { header('Location: index.php'); exit; }
$u = $_SESSION['usuario'];
$pdo = db();

// --- Excluir ---
if (isset($_GET['excluir'])) {
    $lid = (int)$_GET['excluir'];
    $emUso = false;
    foreach (['projetos', 'atividades', 'terminais'] as $tabela) {
        $st = $pdo->prepare("SELECT COUNT(*) FROM $tabela WHERE laboratorio_id = ?");
        $st->execute([$lid]);
        if ($st->fetchColumn() > 0) { $emUso = true; break; }
    }
    if ($emUso) {
        $_SESSION['flash_erro'] = 'Não é possível excluir: este laboratório está em uso por projetos, atividades ou terminais.';
    } else {
        $pdo->prepare('DELETE FROM laboratorios WHERE id = ?')->execute([$lid]);
        $_SESSION['flash_sucesso'] = 'Laboratório excluído.';
    }
    header('Location: laboratorios.php'); exit;
}

// --- Cadastrar ou atualizar ---
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
        $_SESSION['flash_erro'] = 'Sessão expirada, tente novamente.';
    } else {
        $id = (int)($_POST['id'] ?? 0);
        $nome = trim($_POST['nome'] ?? '');
        $localizacao = trim($_POST['localizacao'] ?? '');
        $capacidade = $_POST['capacidade'] !== '' ? (int)$_POST['capacidade'] : null;
        $status = in_array($_POST['status'] ?? '', ['ativo', 'manutencao', 'inativo'], true) ? $_POST['status'] : 'ativo';

        if ($nome === '') {
            $_SESSION['flash_erro'] = 'Informe o nome do laboratório.';
        } elseif ($id > 0) {
            $pdo->prepare('UPDATE laboratorios SET nome=?, localizacao=?, capacidade=?, status=? WHERE id=?')
                ->execute([$nome, $localizacao ?: null, $capacidade, $status, $id]);
            $_SESSION['flash_sucesso'] = 'Laboratório atualizado.';
        } else {
            $pdo->prepare('INSERT INTO laboratorios (nome, localizacao, capacidade, status) VALUES (?,?,?,?)')
                ->execute([$nome, $localizacao ?: null, $capacidade, $status]);
            $_SESSION['flash_sucesso'] = 'Laboratório cadastrado.';
        }
    }
    header('Location: laboratorios.php'); exit;
}

// --- Carrega dados para edição, se veio ?editar=ID ---
$edicao = null;
if (isset($_GET['editar'])) {
    $st = $pdo->prepare('SELECT * FROM laboratorios WHERE id = ?');
    $st->execute([(int)$_GET['editar']]);
    $edicao = $st->fetch() ?: null;
}

$laboratorios = $pdo->query('SELECT * FROM laboratorios ORDER BY nome')->fetchAll();

$erro = $_SESSION['flash_erro'] ?? ''; unset($_SESSION['flash_erro']);
$sucesso = $_SESSION['flash_sucesso'] ?? ''; unset($_SESSION['flash_sucesso']);

$rotulosStatus = ['ativo' => 'Ativo', 'manutencao' => 'Manutenção', 'inativo' => 'Inativo'];

$tituloPagina = 'Laboratórios · CheckPonto';
$pagina_ativa = 'laboratorios';
require __DIR__ . '/includes/layout-topo.php';
?>

<h1 style="font-size:1.6rem;font-weight:700;margin-bottom:4px">Laboratórios</h1>
<p style="color:var(--suave);font-size:.92rem;margin-bottom:22px">Gerencie os laboratórios e seus recursos</p>

<?php if ($erro): ?><div class="aviso erro"><?= h($erro) ?></div><?php endif; ?>
<?php if ($sucesso): ?><div class="aviso sucesso"><?= h($sucesso) ?></div><?php endif; ?>

<div class="cartao" style="margin-bottom:26px">
  <h2 style="font-size:1rem;font-weight:700;margin-bottom:16px">
    <?= $edicao ? 'Editar laboratório' : 'Novo laboratório' ?>
  </h2>
  <form method="post" action="laboratorios.php">
    <input type="hidden" name="csrf" value="<?= h($_SESSION['csrf']) ?>">
    <?php if ($edicao): ?><input type="hidden" name="id" value="<?= $edicao['id'] ?>"><?php endif; ?>
    <div class="grade-form" style="margin-bottom:18px">
      <div class="campo">
        <label for="nome">Nome</label>
        <input type="text" id="nome" name="nome" required placeholder="Ex.: Lab. 1 - Inteligência Artificial"
               value="<?= h($edicao['nome'] ?? '') ?>">
      </div>
      <div class="campo">
        <label for="localizacao">Localização</label>
        <input type="text" id="localizacao" name="localizacao" placeholder="Ex.: Sala 101, Bloco A"
               value="<?= h($edicao['localizacao'] ?? '') ?>">
      </div>
      <div class="campo">
        <label for="capacidade">Capacidade</label>
        <input type="number" id="capacidade" name="capacidade" min="1" placeholder="Ex.: 20"
               value="<?= h((string)($edicao['capacidade'] ?? '')) ?>">
      </div>
      <div class="campo">
        <label for="status">Status</label>
        <select id="status" name="status">
          <?php foreach ($rotulosStatus as $valor => $rotulo): ?>
            <option value="<?= $valor ?>" <?= ($edicao['status'] ?? 'ativo') === $valor ? 'selected' : '' ?>><?= $rotulo ?></option>
          <?php endforeach; ?>
        </select>
      </div>
    </div>
    <button type="submit" class="btn-primario"><?= $edicao ? 'Salvar alterações' : 'Cadastrar laboratório' ?></button>
    <?php if ($edicao): ?>
      <a class="acao-link" href="laboratorios.php" style="margin-left:14px">Cancelar edição</a>
    <?php endif; ?>
  </form>
</div>

<div class="cartao" style="padding:0;overflow:hidden">
  <table class="tabela">
    <thead><tr><th>Nome</th><th>Localização</th><th>Capacidade</th><th>Status</th><th>Ações</th></tr></thead>
    <tbody>
      <?php if (!$laboratorios): ?><tr><td colspan="5" style="padding:18px;color:var(--suave)">Nenhum laboratório cadastrado.</td></tr><?php endif; ?>
      <?php foreach ($laboratorios as $l): ?>
        <tr>
          <td style="font-weight:600"><?= h($l['nome']) ?></td>
          <td style="color:var(--suave)"><?= h($l['localizacao'] ?? '—') ?></td>
          <td style="color:var(--suave)"><?= h($l['capacidade'] !== null ? (string)$l['capacidade'] : '—') ?></td>
          <td><span class="pilula <?= h($l['status']) ?>"><?= h($rotulosStatus[$l['status']]) ?></span></td>
          <td>
            <a class="acao-link" href="laboratorios.php?editar=<?= $l['id'] ?>">Editar</a>
            &nbsp;·&nbsp;
            <a class="acao-link perigo" href="laboratorios.php?excluir=<?= $l['id'] ?>" onclick="return confirm('Excluir este laboratório?')">Excluir</a>
          </td>
        </tr>
      <?php endforeach; ?>
    </tbody>
  </table>
</div>

<?php require __DIR__ . '/includes/layout-rodape.php'; ?>