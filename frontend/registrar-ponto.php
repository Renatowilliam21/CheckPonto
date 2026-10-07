<?php
require __DIR__ . '/config.php';

if (empty($_SESSION['usuario'])) { header('Location: index.php'); exit; }
if ($_SERVER['REQUEST_METHOD'] !== 'POST' || !hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
    header('Location: meuponto.php'); exit;
}

$pdo = db();
$id  = $_SESSION['usuario']['id'];

// Alterna: se a última batida foi "entrada", esta é "saida", e vice-versa
$st = $pdo->prepare('SELECT tipo FROM registros_ponto WHERE usuario_id = ? ORDER BY data_hora DESC LIMIT 1');
$st->execute([$id]);
$tipo = $st->fetchColumn() === 'entrada' ? 'saida' : 'entrada';

// Uma batida feita pelo site (sem leitor) não tem terminal; tentamos vincular
// ao primeiro projeto do participante, só para fins de exemplo.
$st = $pdo->prepare('SELECT projeto_id FROM participantes_projetos WHERE usuario_id = ? LIMIT 1');
$st->execute([$id]);
$projeto_id = $st->fetchColumn() ?: null;

$pdo->prepare('INSERT INTO registros_ponto (usuario_id, tipo, terminal_id, projeto_id) VALUES (?, ?, NULL, ?)')
    ->execute([$id, $tipo, $projeto_id]);

header('Location: meuponto.php');