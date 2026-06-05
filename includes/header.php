<?php
if (session_status() !== PHP_SESSION_ACTIVE) {
    session_start();
}
$adminUser = $_SESSION['admin'] ?? 'Administrator';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Library Management System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
        <a class="navbar-brand" href="../admin/dashboard.php">Library System</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNav" aria-controls="mainNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="mainNav">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item"><a class="nav-link" href="../admin/dashboard.php">Dashboard</a></li>
                <li class="nav-item"><a class="nav-link" href="../books/list.php">Books</a></li>
                <li class="nav-item"><a class="nav-link" href="../members/list.php">Members</a></li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Transactions</a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="../issue/issue_book.php">Issue Book</a></li>
                        <li><a class="dropdown-item" href="../issue/return_book.php">Return Book</a></li>
                    </ul>
                </li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Reports</a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="../reports/books_report.php">Books Report</a></li>
                        <li><a class="dropdown-item" href="../reports/members_report.php">Members Report</a></li>
                        <li><a class="dropdown-item" href="../reports/issue_report.php">Issue Report</a></li>
                        <li><a class="dropdown-item" href="../reports/fine_report.php">Fine Report</a></li>
                    </ul>
                </li>
            </ul>
            <span class="navbar-text text-white me-3">Signed in as: <?php echo htmlspecialchars($adminUser); ?></span>
            <a class="btn btn-outline-light" href="../admin/logout.php">Logout</a>
        </div>
    </div>
</nav>
<div class="container mt-4">
