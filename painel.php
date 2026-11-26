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

// --- Registros desta semana (usados nas horas totais e no gráfico por dia) ---
$segunda = new DateTime('monday this week');
$st = $pdo->prepare('SELECT tipo, data_hora FROM registros_ponto
                      WHERE usuario_id = ? AND data_hora >= ? ORDER BY data_hora ASC');
$st->execute([$id, $segunda->format('Y-m-d 00:00:00')]);

$segundos_semana = 0;
$segundos_por_dia = array_fill(0, 5, 0); // 0=Seg ... 4=Sex
$aberto = null;
foreach ($st->fetchAll() as $r) {
    if ($r['tipo'] === 'entrada') {
        $aberto = new DateTime($r['data_hora']);
    } elseif ($r['tipo'] === 'saida' && $aberto) {
        $duracao = (new DateTime($r['data_hora']))->getTimestamp() - $aberto->getTimestamp();
        $segundos_semana += $duracao;
        $diaIndex = (int)$aberto->format('N') - 1;
        if ($diaIndex >= 0 && $diaIndex <= 4) $segundos_por_dia[$diaIndex] += $duracao;
        $aberto = null;
    }
}
if ($aberto) {
    $duracao = (new DateTime())->getTimestamp() - $aberto->getTimestamp();
    $segundos_semana += $duracao;
    $diaIndex = (int)$aberto->format('N') - 1;
    if ($diaIndex >= 0 && $diaIndex <= 4) $segundos_por_dia[$diaIndex] += $duracao;
}
$horas_semana = sprintf('%dh %02dmin', intdiv($segundos_semana, 3600), intdiv($segundos_semana % 3600, 60));
$maior_segundos_dia = max($segundos_por_dia) ?: 1;

// --- Atividades desta semana ---
$st = $pdo->prepare("SELECT COUNT(*) FROM atividades a
                      JOIN participantes_atividades pa ON pa.atividade_id = a.id
                      WHERE pa.usuario_id = ? AND YEARWEEK(a.data, 1) = YEARWEEK(CURDATE(), 1)");
$st->execute([$id]);
$atividades_semana = (int)$st->fetchColumn();

// --- Meus projetos ---
$st = $pdo->prepare("SELECT p.nome, p.ativo, l.nome AS laboratorio_nome
                      FROM projetos p
                      JOIN participantes_projetos pp ON pp.projeto_id = p.id
                      JOIN laboratorios l ON l.id = p.laboratorio_id
                      WHERE pp.usuario_id = ? ORDER BY p.ativo DESC, p.nome");
$st->execute([$id]);
$meus_projetos = $st->fetchAll();
$projetos_ativos = count(array_filter($meus_projetos, fn($p) => $p['ativo']));

// --- Último registro e atividade recente de ponto ---
$st = $pdo->prepare('SELECT tipo, data_hora FROM registros_ponto WHERE usuario_id = ?
                      ORDER BY data_hora DESC LIMIT 5');
$st->execute([$id]);
$atividade_recente = $st->fetchAll();
$ultimo_registro = $atividade_recente ? registro_relativo($atividade_recente[0]['data_hora']) : 'Nenhum ainda';

// --- Próximas atividades ---
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
$saudacaoTopo = saudacao_horario() . ', ' . primeiro_nome($u['nome']);
require __DIR__ . '/includes/layout-topo.php';

$rotulosDia = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex'];
?>

<h1 style="font-size:1.6rem;font-weight:700;margin-bottom:4px">Dashboard</h1>
<p style="color:var(--suave);font-size:.92rem;margin-bottom:26px">Visão geral da sua participação</p>

<?php if (!empty($_SESSION['flash_erro'])): ?>
  <div class="aviso erro"><?= h($_SESSION['flash_erro']) ?></div>
  <?php unset($_SESSION['flash_erro']); ?>
<?php endif; ?>

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:16px;margin-bottom:24px">
  <div class="cartao">
    <div style="width:38px;height:38px;border-radius:10px;background:var(--azul-claro);color:var(--azul);
                display:flex;align-items:center;justify-content:center;margin-bottom:14px">
      <svg class="icone" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.3"/><path d="M12 7.5v5l3.3 2"/></svg>
    </div>
    <div style="font-size:.82rem;color:var(--suave);margin-bottom:2px">Horas esta semana</div>
    <div style="font-size:1.4rem;font-weight:700"><?= h($horas_semana) ?></div>
  </div>
  <div class="cartao">
    <div style="width:38px;height:38px;border-radius:10px;background:var(--azul-claro);color:var(--azul);
                display:flex;align-items:center;justify-content:center;margin-bottom:14px">
      <svg class="icone" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="3"/><path d="m8.3 12.5 2.3 2.3 5.1-5.3"/></svg>
    </div>
    <div style="font-size:.82rem;color:var(--suave);margin-bottom:2px">Atividades esta semana</div>
    <div style="font-size:1.4rem;font-weight:700"><?= h((string)$atividades_semana) ?></div>
  </div>
  <div class="cartao">
    <div style="width:38px;height:38px;border-radius:10px;background:var(--azul-claro);color:var(--azul);
                display:flex;align-items:center;justify-content:center;margin-bottom:14px">
      <svg class="icone" viewBox="0 0 24 24"><path d="M3 7.5h6l1.8 2H21v10.5H3z"/></svg>
    </div>
    <div style="font-size:.82rem;color:var(--suave);margin-bottom:2px">Projetos ativos</div>
    <div style="font-size:1.4rem;font-weight:700"><?= h((string)$projetos_ativos) ?></div>
  </div>
  <div class="cartao">
    <div style="width:38px;height:38px;border-radius:10px;background:var(--verde-claro);color:var(--verde);
                display:flex;align-items:center;justify-content:center;margin-bottom:14px">
      <svg class="icone" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.5 2.5L16 9.5"/></svg>
    </div>
    <div style="font-size:.82rem;color:var(--suave);margin-bottom:2px">Último registro</div>
    <div style="font-size:1.4rem;font-weight:700"><?= h($ultimo_registro) ?></div>
  </div>
</div>

<div style="display:grid;grid-template-columns:2fr 1fr;gap:20px;align-items:start">
  <div>
    <!-- Horas por dia -->
    <div class="cartao" style="margin-bottom:20px">
      <h2 style="font-size:1rem;font-weight:700;margin-bottom:18px">Horas trabalhadas na semana</h2>
      <div style="display:flex;gap:14px;align-items:flex-end;height:120px">
        <?php foreach ($rotulosDia as $i => $rotulo):
            $altura = max(4, round($segundos_por_dia[$i] / $maior_segundos_dia * 100));
            $horasDia = round($segundos_por_dia[$i] / 3600, 1);
        ?>
          <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;height:100%;justify-content:flex-end">
            <span style="font-size:.74rem;color:var(--suave)"><?= $horasDia > 0 ? $horasDia . 'h' : '' ?></span>
            <div style="width:100%;max-width:34px;height:<?= $altura ?>%;background:var(--azul);border-radius:6px 6px 0 0"></div>
            <span style="font-size:.76rem;color:var(--suave);font-weight:600"><?= $rotulo ?></span>
          </div>
        <?php endforeach; ?>
      </div>
    </div>

    <!-- Próximas atividades -->
    <div class="cartao">
      <h2 style="font-size:1rem;font-weight:700;margin-bottom:16px">Próximas atividades</h2>
      <?php if (!$proximas_atividades): ?>
        <p style="color:var(--suave);font-size:.9rem">Nenhuma atividade agendada.</p>
      <?php endif; ?>
      <div style="display:flex;flex-direction:column;gap:10px">
        <?php foreach ($proximas_atividades as $a): ?>
          <div style="border:1px solid var(--linha);border-radius:12px;padding:14px 16px;display:flex;align-items:center;gap:14px;flex-wrap:wrap">
            <div style="width:36px;height:36px;border-radius:9px;background:var(--azul-claro);color:var(--azul);
                        display:flex;align-items:center;justify-content:center;flex:none">
              <svg class="icone" viewBox="0 0 24 24"><rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 9.5h17M8 3v4M16 3v4"/></svg>
            </div>
            <div style="flex:1;min-width:160px">
              <div style="font-weight:600;font-size:.92rem;margin-bottom:3px"><?= h($a['titulo']) ?></div>
              <div style="color:var(--suave);font-size:.8rem"><?= h($a['quando']) ?> · <?= h($a['horario']) ?> · <?= h($a['local']) ?></div>
            </div>
          </div>
        <?php endforeach; ?>
      </div>
    </div>
  </div>

  <div>
    <!-- Meus projetos -->
    <div class="cartao" style="margin-bottom:20px">
      <h2 style="font-size:1rem;font-weight:700;margin-bottom:14px">Meus projetos</h2>
      <?php if (!$meus_projetos): ?>
        <p style="color:var(--suave);font-size:.88rem">Você ainda não está em nenhum projeto.</p>
      <?php endif; ?>
      <div style="display:flex;flex-direction:column;gap:10px">
        <?php foreach ($meus_projetos as $p): ?>
          <div style="display:flex;justify-content:space-between;align-items:center;gap:10px">
            <div>
              <div style="font-weight:600;font-size:.88rem"><?= h($p['nome']) ?></div>
              <div style="color:var(--suave);font-size:.78rem"><?= h($p['laboratorio_nome']) ?></div>
            </div>
            <span class="pilula <?= $p['ativo'] ? 'ativo' : 'inativo' ?>"><?= $p['ativo'] ? 'Ativo' : 'Inativo' ?></span>
          </div>
        <?php endforeach; ?>
      </div>
    </div>

    <!-- Atividade recente (ponto) -->
    <div class="cartao">
      <h2 style="font-size:1rem;font-weight:700;margin-bottom:14px">Atividade recente</h2>
      <?php if (!$atividade_recente): ?>
        <p style="color:var(--suave);font-size:.88rem">Nenhum registro de ponto ainda.</p>
      <?php endif; ?>
      <div style="display:flex;flex-direction:column;gap:12px">
        <?php foreach ($atividade_recente as $r):
            $cor = $r['tipo'] === 'entrada' ? 'var(--verde)' : '#D4483D';
        ?>
          <div style="display:flex;align-items:center;gap:10px">
            <span style="width:8px;height:8px;border-radius:50%;background:<?= $cor ?>;flex:none"></span>
            <span style="font-size:.85rem;font-weight:600;color:<?= $cor ?>"><?= $r['tipo'] === 'entrada' ? 'Entrada' : 'Saída' ?></span>
            <span style="font-size:.8rem;color:var(--suave);margin-left:auto"><?= h(registro_relativo($r['data_hora'])) ?></span>
          </div>
        <?php endforeach; ?>
      </div>
    </div>
  </div>
</div>

<?php require __DIR__ . '/includes/layout-rodape.php'; ?>