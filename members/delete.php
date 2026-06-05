<?php
include('../includes/auth.php');
include('../config/db.php');

$id = intval($_GET['id'] ?? 0);
if ($id > 0) {
    $stmt = $conn->prepare('DELETE FROM members WHERE id = ?');
    $stmt->bind_param('i', $id);
    $stmt->execute();
}
header('Location: list.php');
exit();
?>