<?php
require __DIR__ . '/config.php';
if (empty($_SESSION['usuario'])) { header('Location: index.php'); exit; }
$u = $_SESSION['usuario'];
$pdo = db();

// --- Excluir ---
if (isset($_GET['excluir'])) {
    $aid = (int)$_GET['excluir'];
    $pdo->prepare('DELETE FROM participantes_atividades WHERE atividade_id = ?')->execute([$aid]);
    $pdo->prepare('DELETE FROM atividades WHERE id = ?')->execute([$aid]);
    $_SESSION['flash_sucesso'] = 'Atividade excluída.';
    header('Location: atividades.php'); exit;
}

// --- Cadastrar nova atividade ---
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
        $_SESSION['flash_erro'] = 'Sessão expirada, tente novamente.';
    } else {
        $titulo = trim($_POST['titulo'] ?? '');
        $laboratorio_id = (int)($_POST['laboratorio_id'] ?? 0);
        $projeto_id = ($_POST['projeto_id'] ?? '') !== '' ? (int)$_POST['projeto_id'] : null;
        $data = $_POST['data'] ?? '';
        $hora_inicio = $_POST['hora_inicio'] ?? '';
        $hora_fim = $_POST['hora_fim'] ?? '';
        $participantes = array_map('intval', $_POST['participantes'] ?? []);

        if ($titulo === '' || $laboratorio_id === 0 || $data === '' || $hora_inicio === '' || $hora_fim === '') {
            $_SESSION['flash_erro'] = 'Preencha título, laboratório, data e horário.';
        } else {
            $pdo->prepare('INSERT INTO atividades (titulo, projeto_id, laboratorio_id, data, hora_inicio, hora_fim)
                            VALUES (?,?,?,?,?,?)')
                ->execute([$titulo, $projeto_id, $laboratorio_id, $data, $hora_inicio, $hora_fim]);
            $atividade_id = $pdo->lastInsertId();
            $ins = $pdo->prepare('INSERT IGNORE INTO participantes_atividades (usuario_id, atividade_id) VALUES (?,?)');
            foreach ($participantes as $uid) $ins->execute([$uid, $atividade_id]);
            $_SESSION['flash_sucesso'] = 'Atividade cadastrada.';
        }
    }
    header('Location: atividades.php'); exit;
}

$laboratorios = $pdo->query('SELECT id, nome FROM laboratorios ORDER BY nome')->fetchAll();
$projetosOpcoes = $pdo->query('SELECT id, nome FROM projetos ORDER BY nome')->fetchAll();
$usuarios = $pdo->query('SELECT id, nome FROM usuarios WHERE ativo = 1 ORDER BY nome')->fetchAll();

$atividades = $pdo->query("SELECT a.*, l.nome AS laboratorio_nome, p.nome AS projeto_nome,
                                   COUNT(pa.usuario_id) AS total_participantes
                            FROM atividades a
                            JOIN laboratorios l ON l.id = a.laboratorio_id
                            LEFT JOIN projetos p ON p.id = a.projeto_id
                            LEFT JOIN participantes_atividades pa ON pa.atividade_id = a.id
                            GROUP BY a.id ORDER BY a.data ASC, a.hora_inicio ASC")->fetchAll();

$erro = $_SESSION['flash_erro'] ?? ''; unset($_SESSION['flash_erro']);
$sucesso = $_SESSION['flash_sucesso'] ?? ''; unset($_SESSION['flash_sucesso']);

$tituloPagina = 'Atividades · CheckPonto';
$pagina_ativa = 'atividades';
require __DIR__ . '/includes/layout-topo.php';
?>

<h1 style="font-size:1.6rem;font-weight:700;margin-bottom:4px">Atividades</h1>
<p style="color:var(--suave);font-size:.92rem;margin-bottom:22px">Agende atividades e defina quem participa de cada uma</p>

<?php if ($erro): ?><div class="aviso erro"><?= h($erro) ?></div><?php endif; ?>
<?php if ($sucesso): ?><div class="aviso sucesso"><?= h($sucesso) ?></div><?php endif; ?>

<?php if (!$laboratorios): ?>
  <div class="aviso erro">Cadastre pelo menos um laboratório na tabela <code>laboratorios</code> antes de criar atividades.</div>
<?php else: ?>
<div class="cartao" style="margin-bottom:26px">
  <h2 style="font-size:1rem;font-weight:700;margin-bottom:16px">Nova atividade</h2>
  <form method="post" action="atividades.php">
    <input type="hidden" name="csrf" value="<?= h($_SESSION['csrf']) ?>">
    <div class="grade-form" style="margin-bottom:16px">
      <div class="campo" style="grid-column:1/-1">
        <label for="titulo">Título da atividade</label>
        <input type="text" id="titulo" name="titulo" required placeholder="Ex.: Reunião do projeto IA">
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
      <div class="campo">
        <label for="projeto_id">Projeto (opcional)</label>
        <select id="projeto_id" name="projeto_id">
          <option value="">Nenhum</option>
          <?php foreach ($projetosOpcoes as $p): ?>
            <option value="<?= $p['id'] ?>"><?= h($p['nome']) ?></option>
          <?php endforeach; ?>
        </select>
      </div>
      <div class="campo">
        <label for="data">Data</label>
        <input type="date" id="data" name="data" required>
      </div>
      <div class="campo">
        <label for="hora_inicio">Início</label>
        <input type="time" id="hora_inicio" name="hora_inicio" required>
      </div>
      <div class="campo">
        <label for="hora_fim">Fim</label>
        <input type="time" id="hora_fim" name="hora_fim" required>
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
    <button type="submit" class="btn-primario">Cadastrar atividade</button>
  </form>
</div>
<?php endif; ?>

<div class="cartao" style="padding:0;overflow:hidden">
  <table class="tabela">
    <thead><tr><th>Título</th><th>Projeto</th><th>Laboratório</th><th>Data</th><th>Horário</th><th>Participantes</th><th>Ações</th></tr></thead>
    <tbody>
      <?php if (!$atividades): ?><tr><td colspan="7" style="padding:18px;color:var(--suave)">Nenhuma atividade cadastrada.</td></tr><?php endif; ?>
      <?php foreach ($atividades as $a): ?>
        <tr>
          <td style="font-weight:600"><?= h($a['titulo']) ?></td>
          <td style="color:var(--suave)"><?= h($a['projeto_nome'] ?? '—') ?></td>
          <td style="color:var(--suave)"><?= h($a['laboratorio_nome']) ?></td>
          <td style="color:var(--suave)"><?= h((new DateTime($a['data']))->format('d/m/Y')) ?></td>
          <td style="color:var(--suave)"><?= h(substr($a['hora_inicio'],0,5) . ' - ' . substr($a['hora_fim'],0,5)) ?></td>
          <td style="color:var(--suave)"><?= (int)$a['total_participantes'] ?></td>
          <td>
            <a class="acao-link perigo" href="atividades.php?excluir=<?= $a['id'] ?>" onclick="return confirm('Excluir esta atividade?')">Excluir</a>
          </td>
        </tr>
      <?php endforeach; ?>
    </tbody>
  </table>
</div>

<?php require __DIR__ . '/includes/layout-rodape.php'; ?>