<?php
require __DIR__ . '/config.php';
if (empty($_SESSION['usuario'])) { header('Location: index.php'); exit; }
$u = $_SESSION['usuario'];
$pdo = db();

// --- Período e filtros (via GET, com padrão = mês atual) ---
$inicio = $_GET['inicio'] ?? (new DateTime('first day of this month'))->format('Y-m-d');
$fim    = $_GET['fim']    ?? (new DateTime('today'))->format('Y-m-d');
if (!DateTime::createFromFormat('Y-m-d', $inicio)) $inicio = (new DateTime('first day of this month'))->format('Y-m-d');
if (!DateTime::createFromFormat('Y-m-d', $fim))    $fim    = (new DateTime('today'))->format('Y-m-d');

$fLaboratorio = (int)($_GET['laboratorio_id'] ?? 0);
$fProjeto     = (int)($_GET['projeto_id'] ?? 0);

$laboratorios  = $pdo->query('SELECT id, nome FROM laboratorios ORDER BY nome')->fetchAll();
$projetosLista = $pdo->query('SELECT id, nome FROM projetos ORDER BY nome')->fetchAll();

// --- Monta as condições comuns (período + lab + projeto) ---
$condicoes = ['DATE(r.data_hora) BETWEEN ? AND ?'];
$parametros = [$inicio, $fim];
if ($fLaboratorio > 0) {
    $condicoes[] = 'COALESCE(t.laboratorio_id, p.laboratorio_id) = ?';
    $parametros[] = $fLaboratorio;
}
if ($fProjeto > 0) {
    $condicoes[] = 'r.projeto_id = ?';
    $parametros[] = $fProjeto;
}
$where = implode(' AND ', $condicoes);

$juncao = 'FROM registros_ponto r
           LEFT JOIN terminais t ON t.id = r.terminal_id
           LEFT JOIN projetos p ON p.id = r.projeto_id';

// --- Cartões de resumo ---
$st = $pdo->prepare("SELECT COUNT(*) $juncao WHERE $where");
$st->execute($parametros);
$total_registros = (int)$st->fetchColumn();

$st = $pdo->prepare("SELECT COUNT(DISTINCT r.usuario_id) $juncao WHERE $where");
$st->execute($parametros);
$participantes_ativos = (int)$st->fetchColumn();

$st = $pdo->prepare("SELECT COUNT(DISTINCT r.projeto_id) $juncao WHERE $where AND r.projeto_id IS NOT NULL");
$st->execute($parametros);
$projetos_com_atividade = (int)$st->fetchColumn();

// --- Horas totais e horas por projeto (pareando entrada -> saída em PHP) ---
$st = $pdo->prepare("SELECT r.usuario_id, r.tipo, r.data_hora, r.projeto_id, p.nome AS projeto_nome,
                             COALESCE(t.laboratorio_id, p.laboratorio_id) AS lab_efetivo
                      $juncao
                      WHERE DATE(r.data_hora) BETWEEN ? AND ?
                      ORDER BY r.usuario_id, r.data_hora ASC");
$st->execute([$inicio, $fim]);

$segundos_totais = 0;
$segundos_por_projeto = []; // id => ['nome' => ..., 'segundos' => ...]
$abertos = []; // usuario_id => dados da entrada em aberto

foreach ($st->fetchAll() as $r) {
    if ($r['tipo'] === 'entrada') {
        $abertos[$r['usuario_id']] = $r;
        continue;
    }
    if ($r['tipo'] === 'saida' && isset($abertos[$r['usuario_id']])) {
        $entrada = $abertos[$r['usuario_id']];
        unset($abertos[$r['usuario_id']]);

        // aplica os filtros de laboratório/projeto com base na entrada da sessão
        if ($fLaboratorio > 0 && (int)$entrada['lab_efetivo'] !== $fLaboratorio) continue;
        if ($fProjeto > 0 && (int)$entrada['projeto_id'] !== $fProjeto) continue;

        $duracao = (new DateTime($r['data_hora']))->getTimestamp() - (new DateTime($entrada['data_hora']))->getTimestamp();
        $segundos_totais += $duracao;

        if ($entrada['projeto_id']) {
            $pid = $entrada['projeto_id'];
            if (!isset($segundos_por_projeto[$pid])) {
                $segundos_por_projeto[$pid] = ['nome' => $entrada['projeto_nome'], 'segundos' => 0];
            }
            $segundos_por_projeto[$pid]['segundos'] += $duracao;
        }
    }
}
usort($segundos_por_projeto, fn($a, $b) => $b['segundos'] <=> $a['segundos']);
$maior_segundos = $segundos_por_projeto ? $segundos_por_projeto[0]['segundos'] : 0;

$horas_totais_texto = sprintf('%dh %02dmin', intdiv($segundos_totais, 3600), intdiv($segundos_totais % 3600, 60));

$tituloPagina = 'Relatórios · CheckPonto';
$pagina_ativa = 'relatorios';
require __DIR__ . '/includes/layout-topo.php';
?>

<h1 style="font-size:1.6rem;font-weight:700;margin-bottom:4px">Relatórios</h1>
<p style="color:var(--suave);font-size:.92rem;margin-bottom:22px">Acompanhe a participação e gere relatórios</p>

<form method="get" action="relatorios.php" style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:26px">
  <input type="date" name="inicio" value="<?= h($inicio) ?>"
         style="height:42px;border:1px solid var(--linha);border-radius:8px;padding:0 12px;font:inherit">
  <input type="date" name="fim" value="<?= h($fim) ?>"
         style="height:42px;border:1px solid var(--linha);border-radius:8px;padding:0 12px;font:inherit">
  <select name="laboratorio_id" style="height:42px;border:1px solid var(--linha);border-radius:8px;padding:0 10px;font:inherit">
    <option value="0">Todos os laboratórios</option>
    <?php foreach ($laboratorios as $l): ?>
      <option value="<?= $l['id'] ?>" <?= $fLaboratorio === (int)$l['id'] ? 'selected' : '' ?>><?= h($l['nome']) ?></option>
    <?php endforeach; ?>
  </select>
  <select name="projeto_id" style="height:42px;border:1px solid var(--linha);border-radius:8px;padding:0 10px;font:inherit">
    <option value="0">Todos os projetos</option>
    <?php foreach ($projetosLista as $p): ?>
      <option value="<?= $p['id'] ?>" <?= $fProjeto === (int)$p['id'] ? 'selected' : '' ?>><?= h($p['nome']) ?></option>
    <?php endforeach; ?>
  </select>
  <button type="submit" class="btn-primario">Gerar Relatório</button>
</form>

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-bottom:30px">

  <div class="cartao">
    <div style="width:38px;height:38px;border-radius:10px;background:var(--azul-claro);color:var(--azul);
                display:flex;align-items:center;justify-content:center;margin-bottom:14px">
      <svg class="icone" viewBox="0 0 24 24"><rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 9.5h17M8 3v4M16 3v4"/></svg>
    </div>
    <div style="font-size:.82rem;color:var(--suave);margin-bottom:2px">Total de registros</div>
    <div style="font-size:1.4rem;font-weight:700"><?= $total_registros ?></div>
  </div>

  <div class="cartao">
    <div style="width:38px;height:38px;border-radius:10px;background:var(--azul-claro);color:var(--azul);
                display:flex;align-items:center;justify-content:center;margin-bottom:14px">
      <svg class="icone" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.3"/><path d="M12 7.5v5l3.3 2"/></svg>
    </div>
    <div style="font-size:.82rem;color:var(--suave);margin-bottom:2px">Horas totais</div>
    <div style="font-size:1.4rem;font-weight:700"><?= h($horas_totais_texto) ?></div>
  </div>

  <div class="cartao">
    <div style="width:38px;height:38px;border-radius:10px;background:var(--azul-claro);color:var(--azul);
                display:flex;align-items:center;justify-content:center;margin-bottom:14px">
      <svg class="icone" viewBox="0 0 24 24"><circle cx="9" cy="8.2" r="3.1"/><path d="M2.6 20c0-3.6 2.9-6 6.4-6s6.4 2.4 6.4 6"/><circle cx="17.8" cy="9" r="2.3"/><path d="M15.4 14.3c2.5.4 4.4 2.3 4.9 5.6"/></svg>
    </div>
    <div style="font-size:.82rem;color:var(--suave);margin-bottom:2px">Participantes ativos</div>
    <div style="font-size:1.4rem;font-weight:700"><?= $participantes_ativos ?></div>
  </div>

  <div class="cartao">
    <div style="width:38px;height:38px;border-radius:10px;background:var(--azul-claro);color:var(--azul);
                display:flex;align-items:center;justify-content:center;margin-bottom:14px">
      <svg class="icone" viewBox="0 0 24 24"><path d="M3 7.5h6l1.8 2H21v10.5H3z"/></svg>
    </div>
    <div style="font-size:.82rem;color:var(--suave);margin-bottom:2px">Projetos com atividade</div>
    <div style="font-size:1.4rem;font-weight:700"><?= $projetos_com_atividade ?></div>
  </div>

</div>

<div class="cartao">
  <h2 style="font-size:1.05rem;font-weight:700;margin-bottom:18px">Horas por projeto</h2>
  <?php if (!$segundos_por_projeto): ?>
    <p style="color:var(--suave);font-size:.9rem">Nenhuma hora registrada com esses filtros.</p>
  <?php endif; ?>
  <div style="display:flex;flex-direction:column;gap:14px">
    <?php foreach ($segundos_por_projeto as $linha):
        $horas = round($linha['segundos'] / 3600);
        $pct = $maior_segundos > 0 ? round($linha['segundos'] / $maior_segundos * 100) : 0;
    ?>
      <div style="display:flex;align-items:center;gap:12px">
        <div style="width:170px;flex:none;font-size:.85rem;color:var(--texto)"><?= h($linha['nome']) ?></div>
        <div style="flex:1;background:var(--azul-claro);border-radius:6px;height:10px;overflow:hidden">
          <div style="width:<?= $pct ?>%;background:var(--azul);height:100%;border-radius:6px"></div>
        </div>
        <div style="width:46px;flex:none;text-align:right;font-size:.85rem;color:var(--suave)"><?= $horas ?>h</div>
      </div>
    <?php endforeach; ?>
  </div>
</div>

<?php require __DIR__ . '/includes/layout-rodape.php'; ?>