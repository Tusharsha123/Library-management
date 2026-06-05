<?php
session_start();
include('../config/db.php');

if (isset($_SESSION['admin'])) {
    header('Location: dashboard.php');
    exit();
}

$message = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username'] ?? '');
    $password = trim($_POST['password'] ?? '');

    if ($username === '' || $password === '') {
        $message = 'Please enter username and password.';
    } else {
        $stmt = $conn->prepare('SELECT * FROM admins WHERE username = ?');
        $stmt->bind_param('s', $username);
        $stmt->execute();
        $result = $stmt->get_result();

        if ($row = $result->fetch_assoc()) {
            if (password_verify($password, $row['password'])) {
                session_regenerate_id(true);
                $_SESSION['admin'] = $row['username'];
                header('Location: dashboard.php');
                exit();
            }
        }
        $message = 'Invalid username or password.';
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body class="bg-light">
    <div class="container d-flex align-items-center justify-content-center vh-100">
        <div class="card shadow-sm w-100" style="max-width: 420px;">
            <div class="card-header bg-primary text-white">
                <h4 class="mb-0">Admin Login</h4>
            </div>
            <div class="card-body">
                <form method="POST" novalidate>
                    <div class="mb-3">
                        <label class="form-label">Username</label>
                        <input type="text" name="username" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" name="password" class="form-control" required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Login</button>
                </form>
                <?php if ($message): ?>
                    <div class="alert alert-danger mt-3" role="alert"><?= htmlspecialchars($message); ?></div>
                <?php endif; ?>
            </div>
        </div>
    </div>
</body>
</html>
