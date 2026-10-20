<?php
require __DIR__ . '/config.php';
if (empty($_SESSION['usuario'])) { header('Location: index.php'); exit; }
exigir_perfil(['administrador']);
$u = $_SESSION['usuario'];
$pdo = db();

// --- Cadastrar terminal ---
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['acao']) && $_POST['acao'] === 'novo_terminal') {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
        $_SESSION['flash_erro'] = 'Sessão expirada, tente novamente.';
    } else {
        $nome = trim($_POST['nome'] ?? '');
        $laboratorio_id = (int)($_POST['laboratorio_id'] ?? 0);
        if ($nome === '' || $laboratorio_id === 0) {
            $_SESSION['flash_erro'] = 'Informe o nome do terminal e o laboratório.';
        } else {
            $pdo->prepare('INSERT INTO terminais (nome, laboratorio_id) VALUES (?,?)')->execute([$nome, $laboratorio_id]);
            $_SESSION['flash_sucesso'] = 'Terminal cadastrado.';
        }
    }
    header('Location: administracao.php'); exit;
}

// --- Excluir terminal ---
if (isset($_GET['excluir_terminal'])) {
    $tid = (int)$_GET['excluir_terminal'];
    $st = $pdo->prepare('SELECT COUNT(*) FROM registros_ponto WHERE terminal_id = ?');
    $st->execute([$tid]);
    if ($st->fetchColumn() > 0) {
        $_SESSION['flash_erro'] = 'Não é possível excluir: já existem registros de ponto feitos por este terminal.';
    } else {
        $pdo->prepare('DELETE FROM terminais WHERE id = ?')->execute([$tid]);
        $_SESSION['flash_sucesso'] = 'Terminal excluído.';
    }
    header('Location: administracao.php'); exit;
}

// --- Excluir um registro de ponto incorreto ---
if (isset($_GET['excluir_registro'])) {
    $pdo->prepare('DELETE FROM registros_ponto WHERE id = ?')->execute([(int)$_GET['excluir_registro']]);
    $_SESSION['flash_sucesso'] = 'Registro de ponto excluído.';
    $manterFiltros = $_GET; unset($manterFiltros['excluir_registro']);
    header('Location: administracao.php?' . http_build_query($manterFiltros)); exit;
}

$erro = $_SESSION['flash_erro'] ?? ''; unset($_SESSION['flash_erro']);
$sucesso = $_SESSION['flash_sucesso'] ?? ''; unset($_SESSION['flash_sucesso']);

// --- Visão geral ---
$participantes_ativos = (int)$pdo->query('SELECT COUNT(*) FROM usuarios WHERE ativo = 1')->fetchColumn();
$projetos_ativos      = (int)$pdo->query('SELECT COUNT(*) FROM projetos WHERE ativo = 1')->fetchColumn();
$registros_hoje        = (int)$pdo->query('SELECT COUNT(*) FROM registros_ponto WHERE DATE(data_hora) = CURDATE()')->fetchColumn();
$ultimoGeral           = $pdo->query('SELECT MAX(data_hora) FROM registros_ponto')->fetchColumn();
$ultimo_registro_geral = $ultimoGeral ? registro_relativo($ultimoGeral) : 'Nenhum ainda';

// --- Filtros da lista de registros de ponto ---
$filtroData         = $_GET['data'] ?? (new DateTime('today'))->format('Y-m-d');
if (!DateTime::createFromFormat('Y-m-d', $filtroData)) $filtroData = (new DateTime('today'))->format('Y-m-d');
$filtroParticipante = (int)($_GET['participante_id'] ?? 0);
$filtroLaboratorio  = (int)($_GET['laboratorio_id'] ?? 0);

$condicoes = ['DATE(r.data_hora) = ?'];
$parametros = [$filtroData];
if ($filtroParticipante > 0) { $condicoes[] = 'r.usuario_id = ?'; $parametros[] = $filtroParticipante; }
if ($filtroLaboratorio > 0)  { $condicoes[] = 'COALESCE(t.laboratorio_id, p.laboratorio_id) = ?'; $parametros[] = $filtroLaboratorio; }
$whereRegistros = implode(' AND ', $condicoes);

$st = $pdo->prepare("SELECT r.id, r.tipo, r.data_hora, usr.nome AS usuario_nome, t.nome AS terminal_nome,
                             l.nome AS laboratorio_nome, p.nome AS projeto_nome
                      FROM registros_ponto r
                      JOIN usuarios usr ON usr.id = r.usuario_id
                      LEFT JOIN terminais t ON t.id = r.terminal_id
                      LEFT JOIN projetos p ON p.id = r.projeto_id
                      LEFT JOIN laboratorios l ON l.id = COALESCE(t.laboratorio_id, p.laboratorio_id)
                      WHERE $whereRegistros
                      ORDER BY r.data_hora DESC");
$st->execute($parametros);
$registros = $st->fetchAll();

$participantesLista = $pdo->query('SELECT id, nome FROM usuarios ORDER BY nome')->fetchAll();
$laboratorios       = $pdo->query('SELECT id, nome FROM laboratorios ORDER BY nome')->fetchAll();

// --- Terminais cadastrados ---
$terminais = $pdo->query('SELECT t.*, l.nome AS laboratorio_nome
                           FROM terminais t JOIN laboratorios l ON l.id = t.laboratorio_id
                           ORDER BY l.nome, t.nome')->fetchAll();

// --- Último login de cada participante ---
$logins = $pdo->query("SELECT nome, email, perfil, ultimo_login FROM usuarios ORDER BY ultimo_login IS NULL, ultimo_login DESC")->fetchAll();

$tituloPagina = 'Administração · CheckPonto';
$pagina_ativa = 'administracao';
require __DIR__ . '/includes/layout-topo.php';
?>

<h1 style="font-size:1.6rem;font-weight:700;margin-bottom:4px">Administração</h1>
<p style="color:var(--suave);font-size:.92rem;margin-bottom:22px">Visão geral e supervisão do sistema</p>

<?php if ($erro): ?><div class="aviso erro"><?= h($erro) ?></div><?php endif; ?>
<?php if ($sucesso): ?><div class="aviso sucesso"><?= h($sucesso) ?></div><?php endif; ?>

<!-- Visão geral -->
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-bottom:32px">
  <div class="cartao">
    <div style="font-size:.82rem;color:var(--suave);margin-bottom:2px">Participantes ativos</div>
    <div style="font-size:1.4rem;font-weight:700"><?= $participantes_ativos ?></div>
  </div>
  <div class="cartao">
    <div style="font-size:.82rem;color:var(--suave);margin-bottom:2px">Projetos ativos</div>
    <div style="font-size:1.4rem;font-weight:700"><?= $projetos_ativos ?></div>
  </div>
  <div class="cartao">
    <div style="font-size:.82rem;color:var(--suave);margin-bottom:2px">Registros hoje</div>
    <div style="font-size:1.4rem;font-weight:700"><?= $registros_hoje ?></div>
  </div>
  <div class="cartao">
    <div style="font-size:.82rem;color:var(--suave);margin-bottom:2px">Último registro (geral)</div>
    <div style="font-size:1.4rem;font-weight:700"><?= h($ultimo_registro_geral) ?></div>
  </div>
</div>

<!-- Registros de ponto de todos os participantes -->
<h2 style="font-size:1.1rem;font-weight:700;margin-bottom:14px">Registros de ponto</h2>
<form method="get" action="administracao.php" style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px">
  <input type="date" name="data" value="<?= h($filtroData) ?>"
         style="height:42px;border:1px solid var(--linha);border-radius:8px;padding:0 12px;font:inherit">
  <select name="participante_id" style="height:42px;border:1px solid var(--linha);border-radius:8px;padding:0 10px;font:inherit">
    <option value="0">Todos os participantes</option>
    <?php foreach ($participantesLista as $p): ?>
      <option value="<?= $p['id'] ?>" <?= $filtroParticipante === (int)$p['id'] ? 'selected' : '' ?>><?= h($p['nome']) ?></option>
    <?php endforeach; ?>
  </select>
  <select name="laboratorio_id" style="height:42px;border:1px solid var(--linha);border-radius:8px;padding:0 10px;font:inherit">
    <option value="0">Todos os laboratórios</option>
    <?php foreach ($laboratorios as $l): ?>
      <option value="<?= $l['id'] ?>" <?= $filtroLaboratorio === (int)$l['id'] ? 'selected' : '' ?>><?= h($l['nome']) ?></option>
    <?php endforeach; ?>
  </select>
  <button type="submit" class="btn-primario">Filtrar</button>
</form>

<div class="cartao" style="padding:0;overflow:hidden;margin-bottom:32px">
  <table class="tabela">
    <thead><tr><th>Participante</th><th>Horário</th><th>Tipo</th><th>Terminal</th><th>Laboratório</th><th>Projeto</th><th>Ações</th></tr></thead>
    <tbody>
      <?php if (!$registros): ?><tr><td colspan="7" style="padding:18px;color:var(--suave)">Nenhum registro com esses filtros.</td></tr><?php endif; ?>
      <?php foreach ($registros as $r): ?>
        <tr>
          <td style="font-weight:600"><?= h($r['usuario_nome']) ?></td>
          <td style="color:var(--suave)"><?= h((new DateTime($r['data_hora']))->format('d/m H:i')) ?></td>
          <td>
            <span style="font-weight:600;color:<?= $r['tipo'] === 'entrada' ? 'var(--verde)' : '#D4483D' ?>">
              <?= $r['tipo'] === 'entrada' ? 'Entrada' : 'Saída' ?>
            </span>
          </td>
          <td style="color:var(--suave)"><?= h($r['terminal_nome'] ?? 'Site') ?></td>
          <td style="color:var(--suave)"><?= h($r['laboratorio_nome'] ?? '—') ?></td>
          <td style="color:var(--suave)"><?= h($r['projeto_nome'] ?? '—') ?></td>
          <td>
            <a class="acao-link perigo"
               href="administracao.php?excluir_registro=<?= $r['id'] ?>&data=<?= h($filtroData) ?>&participante_id=<?= $filtroParticipante ?>&laboratorio_id=<?= $filtroLaboratorio ?>"
               onclick="return confirm('Excluir este registro de ponto?')">Excluir</a>
          </td>
        </tr>
      <?php endforeach; ?>
    </tbody>
  </table>
</div>

<!-- Terminais RFID -->
<h2 style="font-size:1.1rem;font-weight:700;margin-bottom:14px">Terminais RFID</h2>
<div class="cartao" style="margin-bottom:20px">
  <form method="post" action="administracao.php" style="display:flex;gap:10px;flex-wrap:wrap;align-items:flex-end">
    <input type="hidden" name="csrf" value="<?= h($_SESSION['csrf']) ?>">
    <input type="hidden" name="acao" value="novo_terminal">
    <div class="campo" style="flex:1;min-width:160px">
      <label for="nome_terminal">Nome do terminal</label>
      <input type="text" id="nome_terminal" name="nome" required placeholder="Ex.: Terminal 4">
    </div>
    <div class="campo" style="flex:1;min-width:160px">
      <label for="lab_terminal">Laboratório</label>
      <select id="lab_terminal" name="laboratorio_id" required>
        <option value="">Selecione...</option>
        <?php foreach ($laboratorios as $l): ?>
          <option value="<?= $l['id'] ?>"><?= h($l['nome']) ?></option>
        <?php endforeach; ?>
      </select>
    </div>
    <button type="submit" class="btn-primario">Cadastrar terminal</button>
  </form>
</div>
<div class="cartao" style="padding:0;overflow:hidden;margin-bottom:32px">
  <table class="tabela">
    <thead><tr><th>Terminal</th><th>Laboratório</th><th>Ações</th></tr></thead>
    <tbody>
      <?php if (!$terminais): ?><tr><td colspan="3" style="padding:18px;color:var(--suave)">Nenhum terminal cadastrado.</td></tr><?php endif; ?>
      <?php foreach ($terminais as $t): ?>
        <tr>
          <td style="font-weight:600"><?= h($t['nome']) ?></td>
          <td style="color:var(--suave)"><?= h($t['laboratorio_nome']) ?></td>
          <td><a class="acao-link perigo" href="administracao.php?excluir_terminal=<?= $t['id'] ?>" onclick="return confirm('Excluir este terminal?')">Excluir</a></td>
        </tr>
      <?php endforeach; ?>
    </tbody>
  </table>
</div>

<!-- Histórico de login -->
<h2 style="font-size:1.1rem;font-weight:700;margin-bottom:14px">Último acesso de cada participante</h2>
<div class="cartao" style="padding:0;overflow:hidden">
  <table class="tabela">
    <thead><tr><th>Nome</th><th>E-mail</th><th>Perfil</th><th>Último login</th></tr></thead>
    <tbody>
      <?php foreach ($logins as $lg): ?>
        <tr>
          <td style="font-weight:600"><?= h($lg['nome']) ?></td>
          <td style="color:var(--suave)"><?= h($lg['email']) ?></td>
          <td><span class="pilula <?= h($lg['perfil']) ?>"><?= h(perfil_rotulo($lg['perfil'])) ?></span></td>
          <td style="color:var(--suave)"><?= $lg['ultimo_login'] ? h(registro_relativo($lg['ultimo_login'])) : 'Nunca' ?></td>
        </tr>
      <?php endforeach; ?>
    </tbody>
  </table>
</div>

<?php require __DIR__ . '/includes/layout-rodape.php'; ?>