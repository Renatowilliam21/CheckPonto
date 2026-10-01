<?php
require __DIR__ . '/config.php';
if (empty($_SESSION['usuario'])) { header('Location: index.php'); exit; }
$u  = $_SESSION['usuario'];
$id = $u['id'];
$pdo = db();

// Último registro define o status atual (dentro ou fora)
$st = $pdo->prepare('SELECT tipo, data_hora FROM registros_ponto WHERE usuario_id = ?
                      ORDER BY data_hora DESC LIMIT 1');
$st->execute([$id]);
$ultimo = $st->fetch();
$em_atividade = $ultimo && $ultimo['tipo'] === 'entrada';
$desde = $ultimo ? (new DateTime($ultimo['data_hora']))->format('H:i') : null;

// Registros de hoje
$st = $pdo->prepare("SELECT r.tipo, r.data_hora, t.nome AS terminal, l.nome AS laboratorio, p.nome AS projeto
                      FROM registros_ponto r
                      LEFT JOIN terminais t ON t.id = r.terminal_id
                      LEFT JOIN laboratorios l ON l.id = t.laboratorio_id
                      LEFT JOIN projetos p ON p.id = r.projeto_id
                      WHERE r.usuario_id = ? AND DATE(r.data_hora) = CURDATE()
                      ORDER BY r.data_hora DESC");
$st->execute([$id]);
$registros_hoje = $st->fetchAll();

$tituloPagina = 'Meu Ponto · CheckPonto';
$pagina_ativa = 'meu-ponto';
require __DIR__ . '/includes/layout-topo.php';
?>

<h1 style="font-size:1.6rem;font-weight:700;margin-bottom:4px">Meu Ponto</h1>
<p style="color:var(--suave);font-size:.92rem;margin-bottom:26px">Registros de presença e jornada</p>

<div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:30px">

  <form method="post" action="registrar-ponto.php" style="flex:2;min-width:260px;background:var(--verde);
        border-radius:14px;padding:28px;display:flex;flex-direction:column;align-items:center;gap:8px">
    <input type="hidden" name="csrf" value="<?= h($_SESSION['csrf']) ?>">
    <button type="submit" style="display:flex;align-items:center;gap:10px;background:#fff;color:var(--verde);
            border:0;border-radius:10px;padding:14px 28px;font:inherit;font-weight:700;font-size:1rem;cursor:pointer">
      <svg class="icone" viewBox="0 0 24 24" style="width:22px;height:22px">
        <path d="M12 3a9 9 0 1 0 9 9"/><path d="M12 3v4M17 4.5l-2 3.5"/>
      </svg>
      <?= $em_atividade ? 'Registrar Saída' : 'Registrar Ponto' ?>
    </button>
    <span style="color:#fff;opacity:.9;font-size:.82rem">ou utilize o terminal RFID</span>
  </form>

  <div style="flex:1;min-width:220px;background:var(--papel);border:1px solid var(--linha);border-radius:14px;
              padding:22px;display:flex;align-items:center;gap:14px">
    <span style="width:12px;height:12px;border-radius:50%;flex:none;
                 background:<?= $em_atividade ? 'var(--verde)' : '#C6CCD6' ?>"></span>
    <div>
      <div style="font-size:.8rem;color:var(--suave)">Status atual</div>
      <div style="font-size:1.1rem;font-weight:700;color:<?= $em_atividade ? 'var(--verde)' : 'var(--texto)' ?>">
        <?= $em_atividade ? 'Em atividade' : 'Fora do laboratório' ?>
      </div>
      <?php if ($desde): ?>
        <div style="font-size:.78rem;color:var(--suave)">Desde <?= h($desde) ?></div>
      <?php endif; ?>
    </div>
  </div>

</div>

<h2 style="font-size:1.1rem;font-weight:700;margin-bottom:14px">Registros de hoje</h2>

<div style="background:var(--papel);border:1px solid var(--linha);border-radius:14px;overflow:hidden;margin-bottom:20px">
  <table style="width:100%;border-collapse:collapse;font-size:.88rem">
    <thead>
      <tr style="text-align:left;color:var(--suave);font-size:.78rem;text-transform:uppercase;letter-spacing:.03em">
        <th style="padding:14px 18px">Horário</th>
        <th style="padding:14px 18px">Tipo</th>
        <th style="padding:14px 18px">Terminal</th>
        <th style="padding:14px 18px">Laboratório</th>
        <th style="padding:14px 18px">Projeto</th>
      </tr>
    </thead>
    <tbody>
      <?php if (!$registros_hoje): ?>
        <tr><td colspan="5" style="padding:18px;color:var(--suave)">Nenhum registro hoje ainda.</td></tr>
      <?php endif; ?>
      <?php foreach ($registros_hoje as $r): ?>
        <tr style="border-top:1px solid var(--linha)">
          <td style="padding:12px 18px"><?= h((new DateTime($r['data_hora']))->format('H:i')) ?></td>
          <td style="padding:12px 18px">
            <span style="display:inline-flex;align-items:center;gap:6px;font-weight:600;
                         color:<?= $r['tipo'] === 'entrada' ? 'var(--verde)' : '#D4483D' ?>">
              <span style="width:8px;height:8px;border-radius:50%;
                           background:<?= $r['tipo'] === 'entrada' ? 'var(--verde)' : '#D4483D' ?>"></span>
              <?= $r['tipo'] === 'entrada' ? 'Entrada' : 'Saída' ?>
            </span>
          </td>
          <td style="padding:12px 18px;color:var(--suave)"><?= h($r['terminal'] ?? 'Site') ?></td>
          <td style="padding:12px 18px;color:var(--suave)"><?= h($r['laboratorio'] ?? '—') ?></td>
          <td style="padding:12px 18px;color:var(--suave)"><?= h($r['projeto'] ?? '—') ?></td>
        </tr>
      <?php endforeach; ?>
    </tbody>
  </table>
</div>

<div style="display:flex;gap:10px;background:var(--azul-claro);color:var(--marinho);border-radius:10px;
            padding:14px 16px;font-size:.85rem;line-height:1.5">
  <svg class="icone" viewBox="0 0 24 24" style="flex:none;margin-top:2px"><circle cx="12" cy="12" r="9"/><path d="M12 8h.01M11 12h1v5h1"/></svg>
  <span>As batidas são automaticamente reinterpretadas para calcular sua jornada e vincular às atividades programadas.</span>
</div>

<?php require __DIR__ . '/includes/layout-rodape.php'; ?>