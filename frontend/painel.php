<?php
require __DIR__ . '/config.php';

if (isset($_GET['sair'])) {
    $_SESSION = [];
    session_destroy();
    header('Location: index.php'); exit;
}
if (empty($_SESSION['usuario'])) { header('Location: index.php'); exit; }
$u  = $_SESSION['usuario'];
$id = $u['id'];
$pdo = db();

// --- Horas trabalhadas nesta semana ---
// Soma o tempo entre cada "entrada" e a "saida" seguinte; se o ponto ainda
// estiver aberto (entrou e não bateu saída), conta até agora.
$inicioSemana = (new DateTime('monday this week'))->format('Y-m-d 00:00:00');
$st = $pdo->prepare('SELECT tipo, data_hora FROM registros_ponto
                      WHERE usuario_id = ? AND data_hora >= ? ORDER BY data_hora ASC');
$st->execute([$id, $inicioSemana]);

$segundos = 0; $aberto = null;
foreach ($st->fetchAll() as $r) {
    if ($r['tipo'] === 'entrada') {
        $aberto = new DateTime($r['data_hora']);
    } elseif ($r['tipo'] === 'saida' && $aberto) {
        $segundos += (new DateTime($r['data_hora']))->getTimestamp() - $aberto->getTimestamp();
        $aberto = null;
    }
}
if ($aberto) $segundos += (new DateTime())->getTimestamp() - $aberto->getTimestamp();
$horas_semana = sprintf('%dh %02dmin', intdiv($segundos, 3600), intdiv($segundos % 3600, 60));

// --- Atividades desta semana (às quais o usuário está vinculado) ---
$st = $pdo->prepare("SELECT COUNT(*) FROM atividades a
                      JOIN participantes_atividades pa ON pa.atividade_id = a.id
                      WHERE pa.usuario_id = ? AND YEARWEEK(a.data, 1) = YEARWEEK(CURDATE(), 1)");
$st->execute([$id]);
$atividades_semana = (int)$st->fetchColumn();

// --- Projetos ativos do usuário ---
$st = $pdo->prepare("SELECT COUNT(*) FROM projetos p
                      JOIN participantes_projetos pp ON pp.projeto_id = p.id
                      WHERE pp.usuario_id = ? AND p.ativo = 1");
$st->execute([$id]);
$projetos_ativos = (int)$st->fetchColumn();

// --- Último registro de ponto ---
$st = $pdo->prepare('SELECT data_hora FROM registros_ponto WHERE usuario_id = ?
                      ORDER BY data_hora DESC LIMIT 1');
$st->execute([$id]);
$ultimo = $st->fetchColumn();
$ultimo_registro = $ultimo ? registro_relativo($ultimo) : 'Nenhum ainda';

// --- Próximas atividades (as 3 mais próximas, a partir de hoje) ---
$st = $pdo->prepare("SELECT a.titulo, a.data, a.hora_inicio, a.hora_fim, l.nome AS laboratorio
                      FROM atividades a
                      JOIN participantes_atividades pa ON pa.atividade_id = a.id
                      JOIN laboratorios l ON l.id = a.laboratorio_id
                      WHERE pa.usuario_id = ? AND a.data >= CURDATE()
                      ORDER BY a.data ASC, a.hora_inicio ASC LIMIT 3");
$st->execute([$id]);
$proximas_atividades = array_map(fn($r) => [
    'titulo'  => $r['titulo'],
    'quando'  => data_relativa($r['data']),
    'horario' => substr($r['hora_inicio'], 0, 5) . ' - ' . substr($r['hora_fim'], 0, 5),
    'local'   => $r['laboratorio'],
], $st->fetchAll());

$tituloPagina = 'Dashboard · CheckPonto';
$pagina_ativa = 'inicio';
require __DIR__ . '/includes/layout-topo.php';
?>

<h1 style="font-size:1.6rem;font-weight:700;margin-bottom:4px">Dashboard</h1>
<p style="color:var(--suave);font-size:.92rem;margin-bottom:26px">Visão geral da sua participação</p>

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:16px;margin-bottom:32px">

  <div style="background:var(--papel);border:1px solid var(--linha);border-radius:14px;padding:18px">
    <div style="width:38px;height:38px;border-radius:10px;background:var(--azul-claro);color:var(--azul);
                display:flex;align-items:center;justify-content:center;margin-bottom:14px">
      <svg class="icone" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.3"/><path d="M12 7.5v5l3.3 2"/></svg>
    </div>
    <div style="font-size:.82rem;color:var(--suave);margin-bottom:2px">Horas esta semana</div>
    <div style="font-size:1.4rem;font-weight:700"><?= h($horas_semana) ?></div>
  </div>

  <div style="background:var(--papel);border:1px solid var(--linha);border-radius:14px;padding:18px">
    <div style="width:38px;height:38px;border-radius:10px;background:var(--azul-claro);color:var(--azul);
                display:flex;align-items:center;justify-content:center;margin-bottom:14px">
      <svg class="icone" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="3"/><path d="m8.3 12.5 2.3 2.3 5.1-5.3"/></svg>
    </div>
    <div style="font-size:.82rem;color:var(--suave);margin-bottom:2px">Atividades esta semana</div>
    <div style="font-size:1.4rem;font-weight:700"><?= h((string)$atividades_semana) ?></div>
  </div>

  <div style="background:var(--papel);border:1px solid var(--linha);border-radius:14px;padding:18px">
    <div style="width:38px;height:38px;border-radius:10px;background:var(--azul-claro);color:var(--azul);
                display:flex;align-items:center;justify-content:center;margin-bottom:14px">
      <svg class="icone" viewBox="0 0 24 24"><path d="M3 7.5h6l1.8 2H21v10.5H3z"/></svg>
    </div>
    <div style="font-size:.82rem;color:var(--suave);margin-bottom:2px">Projetos ativos</div>
    <div style="font-size:1.4rem;font-weight:700"><?= h((string)$projetos_ativos) ?></div>
  </div>

  <div style="background:var(--papel);border:1px solid var(--linha);border-radius:14px;padding:18px">
    <div style="width:38px;height:38px;border-radius:10px;background:var(--verde-claro);color:var(--verde);
                display:flex;align-items:center;justify-content:center;margin-bottom:14px">
      <svg class="icone" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.5 2.5L16 9.5"/></svg>
    </div>
    <div style="font-size:.82rem;color:var(--suave);margin-bottom:2px">Último registro</div>
    <div style="font-size:1.4rem;font-weight:700"><?= h($ultimo_registro) ?></div>
  </div>

</div>

<h2 style="font-size:1.15rem;font-weight:700;margin-bottom:14px">Próximas atividades</h2>

<div style="display:flex;flex-direction:column;gap:10px">
  <?php if (!$proximas_atividades): ?>
    <p style="color:var(--suave);font-size:.9rem">Nenhuma atividade agendada.</p>
  <?php endif; ?>
  <?php foreach ($proximas_atividades as $a): ?>
    <div style="background:var(--papel);border:1px solid var(--linha);border-radius:12px;
                padding:16px 18px;display:flex;align-items:center;gap:14px;flex-wrap:wrap">
      <div style="width:36px;height:36px;border-radius:9px;background:var(--azul-claro);color:var(--azul);
                  display:flex;align-items:center;justify-content:center;flex:none">
        <svg class="icone" viewBox="0 0 24 24"><rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 9.5h17M8 3v4M16 3v4"/></svg>
      </div>
      <div style="flex:1;min-width:180px">
        <div style="font-weight:600;font-size:.94rem;margin-bottom:4px"><?= h($a['titulo']) ?></div>
        <div style="display:flex;flex-wrap:wrap;gap:14px;color:var(--suave);font-size:.82rem">
          <span style="display:flex;align-items:center;gap:5px">
            <svg class="icone" style="width:15px;height:15px" viewBox="0 0 24 24"><rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 9.5h17M8 3v4M16 3v4"/></svg>
            <?= h($a['quando']) ?>
          </span>
          <span style="display:flex;align-items:center;gap:5px">
            <svg class="icone" style="width:15px;height:15px" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.3"/><path d="M12 7.5v5l3.3 2"/></svg>
            <?= h($a['horario']) ?>
          </span>
          <span style="display:flex;align-items:center;gap:5px">
            <svg class="icone" style="width:15px;height:15px" viewBox="0 0 24 24"><path d="M12 21s7-6.1 7-11a7 7 0 1 0-14 0c0 4.9 7 11 7 11Z"/><circle cx="12" cy="10" r="2.3"/></svg>
            <?= h($a['local']) ?>
          </span>
        </div>
      </div>
      <a href="#" style="flex:none;border:1px solid var(--azul);color:var(--azul);font-weight:600;
                         font-size:.82rem;padding:8px 16px;border-radius:8px;text-decoration:none">Ver detalhes</a>
    </div>
  <?php endforeach; ?>
</div>

<?php require __DIR__ . '/includes/layout-rodape.php'; ?>