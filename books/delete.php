<?php
include('../includes/auth.php');
include('../config/db.php');

$id = intval($_GET['id'] ?? 0);
if ($id > 0) {
    $stmt = $conn->prepare('DELETE FROM books WHERE id = ?');
    $stmt->bind_param('i', $id);
    $stmt->execute();
}
header('Location: list.php');
exit();
?>