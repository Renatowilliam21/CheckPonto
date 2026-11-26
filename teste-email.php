<?php
require __DIR__ . '/vendor/autoload.php';
require __DIR__ . '/config.php';







use PHPMailer\PHPMailer\PHPMailer;

echo "<pre>";

if (!class_exists(PHPMailer::class)) {
    echo "A biblioteca PHPMailer não foi encontrada em /libs/PHPMailer/src/.\n";
    echo "Confira se os 3 arquivos (Exception.php, PHPMailer.php, SMTP.php) estão nesse caminho.";
    exit;
}

$mail = new PHPMailer(true);
try {
    $mail->isSMTP();
    $mail->Host = 'smtp.gmail.com';
    $mail->SMTPAuth = true;
    $mail->Username = SMTP_USUARIO;
    $mail->Password = SMTP_SENHA_APP;
    $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
    $mail->Port = 587;
    $mail->CharSet = 'UTF-8';
    $mail->SMTPDebug = 2;          // mostra a conversa com o servidor do Gmail, passo a passo
    $mail->Debugoutput = 'html';

    $mail->setFrom(SMTP_USUARIO, 'CheckPonto LISA');
    $mail->addAddress(SMTP_USUARIO, 'Teste');
    $mail->Subject = 'Teste CheckPonto';
    $mail->Body = 'Se você recebeu isso, o envio está funcionando.';

    $mail->send();
    echo "\nE-MAIL ENVIADO COM SUCESSO.";
} catch (Exception $e) {
    echo "\nFALHOU. Mensagem do PHPMailer: " . $mail->ErrorInfo;
}
echo "</pre>";