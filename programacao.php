<?php
require __DIR__ . '/config.php';
if (empty($_SESSION['usuario'])) { header('Location: index.php'); exit; }
$u = $_SESSION['usuario'];
$pdo = db();

// --- Semana selecionada (sempre ajustada para começar numa segunda-feira) ---
$dataRef = $_GET['semana'] ?? (new DateTime('today'))->format('Y-m-d');
if (!DateTime::createFromFormat('Y-m-d', $dataRef)) $dataRef = (new DateTime('today'))->format('Y-m-d');
$segunda = new DateTime($dataRef);
$segunda->modify('monday this week');

$dias = [];
for ($i = 0; $i < 5; $i++) $dias[] = (clone $segunda)->modify("+$i day");
$sexta = $dias[4];

$fLaboratorio = (int)($_GET['laboratorio_id'] ?? 0);
$fProjeto     = (int)($_GET['projeto_id'] ?? 0);

$laboratorios  = $pdo->query('SELECT id, nome FROM laboratorios ORDER BY nome')->fetchAll();
$projetosLista = $pdo->query('SELECT id, nome FROM projetos ORDER BY nome')->fetchAll();

$condicoes = ['a.data BETWEEN ? AND ?'];
$parametros = [$segunda->format('Y-m-d'), $sexta->format('Y-m-d')];
if ($fLaboratorio > 0) { $condicoes[] = 'a.laboratorio_id = ?'; $parametros[] = $fLaboratorio; }
if ($fProjeto > 0)     { $condicoes[] = 'a.projeto_id = ?';     $parametros[] = $fProjeto; }
$where = implode(' AND ', $condicoes);

$st = $pdo->prepare("SELECT a.*, l.nome AS laboratorio_nome
                      FROM atividades a
                      JOIN laboratorios l ON l.id = a.laboratorio_id
                      WHERE $where
                      ORDER BY a.data, a.hora_inicio");
$st->execute($parametros);
$atividades = $st->fetchAll();

// --- Organiza as atividades numa grade [dia 0-4][hora de início] ---
$horaMin = 7; $horaMax = 19; // janela da agenda: 07:00 às 19:00
$grade = array_fill(0, 5, []);
foreach ($atividades as $a) {
    $diaIndex = (int)(new DateTime($a['data']))->format('N') - 1; // 0 = Segunda ... 4 = Sexta
    if ($diaIndex < 0 || $diaIndex > 4) continue;
    $horaInicio = max($horaMin, (int)substr($a['hora_inicio'], 0, 2));
    $duracaoBruta = (int)ceil((strtotime($a['hora_fim']) - strtotime($a['hora_inicio'])) / 3600);
    $duracao = max(1, min($duracaoBruta, $horaMax - $horaInicio));
    $grade[$diaIndex][$horaInicio] = ['dados' => $a, 'duracao' => $duracao];
}

$rotulosDia = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex'];

$tituloPagina = 'Programação · CheckPonto';
$pagina_ativa = 'programacao';
require __DIR__ . '/includes/layout-topo.php';
?>

<h1 style="font-size:1.6rem;font-weight:700;margin-bottom:4px">Programação Semanal</h1>
<p style="color:var(--suave);font-size:.92rem;margin-bottom:22px">Veja as atividades da semana em formato de agenda</p>

<div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:22px">
  <form method="get" action="programacao.php" style="display:flex;gap:10px;flex-wrap:wrap;align-items:center">
    <label style="font-size:.85rem;color:var(--suave)">Semana de</label>
    <input type="date" name="semana" value="<?= h($segunda->format('Y-m-d')) ?>"
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
    <button type="submit" class="btn-primario">Ver</button>
  </form>
  <a href="atividades.php#form-atividade" class="btn-primario"
     style="display:inline-flex;align-items:center;text-decoration:none">+ Nova Atividade</a>
</div>

<div class="cartao" style="padding:0;overflow-x:auto">
  <table style="width:100%;border-collapse:collapse;font-size:.82rem;min-width:760px">
    <thead>
      <tr>
        <th style="padding:10px 12px;text-align:left;color:var(--suave);font-size:.74rem;text-transform:uppercase;border-bottom:1px solid var(--linha)">Hora</th>
        <?php foreach ($dias as $d): ?>
          <th style="padding:10px 12px;text-align:left;border-bottom:1px solid var(--linha)">
            <?= $rotulosDia[(int)$d->format('N') - 1] ?><br>
            <span style="font-weight:400;color:var(--suave);font-size:.74rem"><?= $d->format('d/m') ?></span>
          </th>
        <?php endforeach; ?>
      </tr>
    </thead>
    <tbody>
      <?php $ocupado = array_fill(0, 5, []); ?>
      <?php for ($hora = $horaMin; $hora < $horaMax; $hora++): ?>
        <tr>
          <td style="padding:10px 12px;color:var(--suave);border-top:1px solid var(--linha);white-space:nowrap">
            <?= sprintf('%02d:00', $hora) ?>
          </td>
          <?php for ($dia = 0; $dia < 5; $dia++): ?>
            <?php if (!empty($ocupado[$dia][$hora])): ?>
              <?php continue; // célula já coberta pelo rowspan de uma atividade iniciada antes ?>
            <?php endif; ?>
            <?php if (isset($grade[$dia][$hora])):
                $item = $grade[$dia][$hora]['dados'];
                $duracao = $grade[$dia][$hora]['duracao'];
                for ($k = 1; $k < $duracao; $k++) $ocupado[$dia][$hora + $k] = true;
                $corId = $item['projeto_id'] ?: $item['laboratorio_id'];
                $cor = cor_atividade_pastel((int)$corId);
            ?>
              <td rowspan="<?= $duracao ?>" style="padding:6px;border-top:1px solid var(--linha);vertical-align:top">
                <div style="background:<?= h($cor['fundo']) ?>;color:<?= h($cor['texto']) ?>;border-radius:8px;
                            padding:8px 10px;height:100%;line-height:1.35">
                  <div style="font-weight:700"><?= h($item['titulo']) ?></div>
                  <div style="opacity:.85"><?= h($item['laboratorio_nome']) ?></div>
                  <div style="opacity:.7;font-size:.74rem">
                    <?= h(substr($item['hora_inicio'], 0, 5) . ' - ' . substr($item['hora_fim'], 0, 5)) ?>
                  </div>
                </div>
              </td>
            <?php else: ?>
              <td style="border-top:1px solid var(--linha)"></td>
            <?php endif; ?>
          <?php endfor; ?>
        </tr>
      <?php endfor; ?>
    </tbody>
  </table>
</div>

<?php require __DIR__ . '/includes/layout-rodape.php'; ?>