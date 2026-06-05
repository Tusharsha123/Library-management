from pathlib import Path

files = {
    'index.php': """<?php
header('Location: admin/login.php');
exit();
?>""",
    'README.md': """# Library Management System

A complete Library Management System built with PHP, MySQL, HTML, CSS, JavaScript, and Bootstrap.

## Features

- Admin login with secure password hashing
- Dashboard with totals for books, members, issued books, returned books, and pending returns
- Full book management CRUD
- Full member management CRUD
- Book issue and return process with automatic fine calculation
- Reports with browser PDF export support
- Input validation and prepared statements to prevent SQL injection

## Installation

1. Install XAMPP and start Apache and MySQL.
2. Place this project folder inside `htdocs` (for example `C:\\xampp\\htdocs\\library-management`).
3. Import `database/library_management.sql` into MySQL using phpMyAdmin or the MySQL command line.
4. Update `config/db.php` if your MySQL username, password, or database name are different.
5. Open `http://localhost/library-management/` in your browser.

## Default Admin Credentials

- Username: `admin`
- Password: `admin123`

## Notes

- Use the `Reports` section to view books, members, issued books, and fines.
- Click `Export to PDF` on report pages to generate a printable PDF via browser print.
""",
    'includes/auth.php': """<?php
session_start();
if (!isset($_SESSION['admin'])) {
    header('Location: ../admin/login.php');
    exit();
}
?>""",
    'includes/header.php': """<?php
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
""",
    'includes/footer.php': """    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="../assets/js/app.js"></script>
</body>
</html>
""",
    'assets/css/style.css': """body {
    background-color: #f4f7fa;
}
.card {
    border-radius: 0.8rem;
}
.form-control, .form-select {
    border-radius: 0.45rem;
}
.table-responsive {
    overflow-x: auto;
}
@media print {
    .no-print {
        display: none !important;
    }
    .navbar, .footer, .btn {
        display: none !important;
    }
    body {
        background-color: #fff;
    }
}
""",
    'assets/js/app.js': """function exportPDF() {
    window.print();
}
""",
    'admin/login.php': """<?php
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
""",
    'admin/dashboard.php': """<?php
include('../includes/auth.php');
include('../config/db.php');

$books = $conn->query("SELECT COUNT(*) AS total FROM books")->fetch_assoc()['total'];
$members = $conn->query("SELECT COUNT(*) AS total FROM members")->fetch_assoc()['total'];
$issued = $conn->query("SELECT COUNT(*) AS total FROM book_issue WHERE status = 'Issued'")->fetch_assoc()['total'];
$returned = $conn->query("SELECT COUNT(*) AS total FROM book_issue WHERE status = 'Returned'")->fetch_assoc()['total'];
$pending = $conn->query("SELECT COUNT(*) AS total FROM book_issue WHERE status = 'Issued' AND due_date < CURDATE()")->fetch_assoc()['total'];
?>
<?php include('../includes/header.php'); ?>
<div class="row g-4">
    <div class="col-md-3">
        <div class="card shadow-sm border-0 text-white bg-primary">
            <div class="card-body">
                <h2><?= $books; ?></h2>
                <p class="mb-0">Total Books</p>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card shadow-sm border-0 text-white bg-success">
            <div class="card-body">
                <h2><?= $members; ?></h2>
                <p class="mb-0">Total Members</p>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card shadow-sm border-0 text-dark bg-warning">
            <div class="card-body">
                <h2><?= $issued; ?></h2>
                <p class="mb-0">Issued Books</p>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card shadow-sm border-0 text-white bg-info">
            <div class="card-body">
                <h2><?= $returned; ?></h2>
                <p class="mb-0">Returned Books</p>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card shadow-sm border-0 text-white bg-danger">
            <div class="card-body">
                <h2><?= $pending; ?></h2>
                <p class="mb-0">Pending Returns</p>
            </div>
        </div>
    </div>
</div>
<?php include('../includes/footer.php'); ?>
""",
    'books/add.php': """<?php
include('../includes/auth.php');
include('../config/db.php');

$message = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $isbn = trim($_POST['isbn'] ?? '');
    $book_name = trim($_POST['book_name'] ?? '');
    $author = trim($_POST['author'] ?? '');
    $publisher = trim($_POST['publisher'] ?? '');
    $category = trim($_POST['category'] ?? '');
    $quantity = intval($_POST['quantity'] ?? 0);

    if ($isbn === '' || $book_name === '' || $author === '' || $publisher === '' || $category === '' || $quantity < 0) {
        $message = 'Please complete the form and enter a valid quantity.';
    } else {
        $stmt = $conn->prepare('INSERT INTO books (isbn, book_name, author, publisher, category, quantity, available_copies) VALUES (?, ?, ?, ?, ?, ?, ?)');
        $stmt->bind_param('sssssss', $isbn, $book_name, $author, $publisher, $category, $quantity, $quantity);
        $stmt->execute();

        if ($stmt->affected_rows > 0) {
            $message = 'Book added successfully.';
        } else {
            $message = 'Unable to add book. Please try again.';
        }
    }
}
?>
<?php include('../includes/header.php'); ?>
<div class="card shadow-sm mb-4">
    <div class="card-header">
        <h4>Add New Book</h4>
    </div>
    <div class="card-body">
        <?php if ($message): ?>
            <div class="alert alert-info"><?= htmlspecialchars($message); ?></div>
        <?php endif; ?>
        <form method="POST">
            <div class="row g-3">
                <div class="col-md-6">
                    <label class="form-label">ISBN</label>
                    <input type="text" name="isbn" class="form-control" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Book Name</label>
                    <input type="text" name="book_name" class="form-control" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Author</label>
                    <input type="text" name="author" class="form-control" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Publisher</label>
                    <input type="text" name="publisher" class="form-control" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Category</label>
                    <input type="text" name="category" class="form-control" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Quantity</label>
                    <input type="number" name="quantity" class="form-control" min="0" value="1" required>
                </div>
            </div>
            <button type="submit" class="btn btn-primary mt-4">Save Book</button>
        </form>
    </div>
</div>
<?php include('../includes/footer.php'); ?>
""",
    'books/edit.php': """<?php
include('../includes/auth.php');
include('../config/db.php');

$id = intval($_GET['id'] ?? 0);
if ($id <= 0) {
    header('Location: list.php');
    exit();
}

$message = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $isbn = trim($_POST['isbn'] ?? '');
    $book_name = trim($_POST['book_name'] ?? '');
    $author = trim($_POST['author'] ?? '');
    $publisher = trim($_POST['publisher'] ?? '');
    $category = trim($_POST['category'] ?? '');
    $quantity = intval($_POST['quantity'] ?? 0);

    if ($isbn === '' || $book_name === '' || $author === '' || $publisher === '' || $category === '' || $quantity < 0) {
        $message = 'Please complete the form and enter a valid quantity.';
    } else {
        $stmt = $conn->prepare('UPDATE books SET isbn = ?, book_name = ?, author = ?, publisher = ?, category = ?, quantity = ?, available_copies = ? WHERE id = ?');
        $stmt->bind_param('sssssiii', $isbn, $book_name, $author, $publisher, $category, $quantity, $quantity, $id);
        $stmt->execute();

        if ($stmt->affected_rows >= 0) {
            $message = 'Book updated successfully.';
        } else {
            $message = 'Unable to update book. Please try again.';
        }
    }
}

$stmt = $conn->prepare('SELECT * FROM books WHERE id = ?');
$stmt->bind_param('i', $id);
$stmt->execute();
$result = $stmt->get_result();
$book = $result->fetch_assoc();
if (!$book) {
    header('Location: list.php');
    exit();
}
?>
<?php include('../includes/header.php'); ?>
<div class="card shadow-sm mb-4">
    <div class="card-header">
        <h4>Edit Book</h4>
    </div>
    <div class="card-body">
        <?php if ($message): ?>
            <div class="alert alert-info"><?= htmlspecialchars($message); ?></div>
        <?php endif; ?>
        <form method="POST">
            <div class="row g-3">
                <div class="col-md-6">
                    <label class="form-label">ISBN</label>
                    <input type="text" name="isbn" class="form-control" value="<?= htmlspecialchars($book['isbn']); ?>" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Book Name</label>
                    <input type="text" name="book_name" class="form-control" value="<?= htmlspecialchars($book['book_name']); ?>" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Author</label>
                    <input type="text" name="author" class="form-control" value="<?= htmlspecialchars($book['author']); ?>" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Publisher</label>
                    <input type="text" name="publisher" class="form-control" value="<?= htmlspecialchars($book['publisher']); ?>" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Category</label>
                    <input type="text" name="category" class="form-control" value="<?= htmlspecialchars($book['category']); ?>" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Quantity</label>
                    <input type="number" name="quantity" class="form-control" min="0" value="<?= htmlspecialchars($book['quantity']); ?>" required>
                </div>
            </div>
            <button type="submit" class="btn btn-primary mt-4">Update Book</button>
        </form>
    </div>
</div>
<?php include('../includes/footer.php'); ?>
""",
    'books/delete.php': """<?php
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
?>""",
    'books/list.php': """<?php
include('../includes/auth.php');
include('../config/db.php');

$search = trim($_GET['search'] ?? '');
$where = '';
$params = [];
$types = '';
if ($search !== '') {
    $where = "WHERE isbn LIKE ? OR book_name LIKE ? OR author LIKE ? OR publisher LIKE ? OR category LIKE ?";
    $value = '%' . $search . '%';
    $params = [$value, $value, $value, $value, $value];
    $types = 'sssss';
}

$sql = "SELECT * FROM books $where ORDER BY book_name ASC";
$stmt = $conn->prepare($sql);
if ($where !== '') {
    $stmt->bind_param($types, ...$params);
}
$stmt->execute();
$result = $stmt->get_result();
?>
<?php include('../includes/header.php'); ?>
<div class="d-flex justify-content-between align-items-center mb-4">
    <h4>Book List</h4>
    <a href="add.php" class="btn btn-success">Add New Book</a>
</div>
<div class="row mb-3">
    <div class="col-md-6">
        <form method="GET" class="d-flex" autocomplete="off">
            <input type="text" name="search" value="<?= htmlspecialchars($search); ?>" class="form-control me-2" placeholder="Search books...">
            <button class="btn btn-outline-primary">Search</button>
        </form>
    </div>
</div>
<div class="table-responsive">
    <table class="table table-hover table-bordered align-middle">
        <thead class="table-dark">
            <tr>
                <th>ID</th>
                <th>ISBN</th>
                <th>Book Name</th>
                <th>Author</th>
                <th>Publisher</th>
                <th>Category</th>
                <th>Quantity</th>
                <th>Available</th>
                <th class="no-print">Actions</th>
            </tr>
        </thead>
        <tbody>
            <?php while ($book = $result->fetch_assoc()): ?>
                <tr>
                    <td><?= htmlspecialchars($book['id']); ?></td>
                    <td><?= htmlspecialchars($book['isbn']); ?></td>
                    <td><?= htmlspecialchars($book['book_name']); ?></td>
                    <td><?= htmlspecialchars($book['author']); ?></td>
                    <td><?= htmlspecialchars($book['publisher']); ?></td>
                    <td><?= htmlspecialchars($book['category']); ?></td>
                    <td><?= htmlspecialchars($book['quantity']); ?></td>
                    <td><?= htmlspecialchars($book['available_copies']); ?></td>
                    <td class="no-print">
                        <a href="edit.php?id=<?= $book['id']; ?>" class="btn btn-sm btn-primary">Edit</a>
                        <a href="delete.php?id=<?= $book['id']; ?>" class="btn btn-sm btn-danger" onclick="return confirm('Delete this book?');">Delete</a>
                    </td>
                </tr>
            <?php endwhile; ?>
        </tbody>
    </table>
</div>
<?php include('../includes/footer.php'); ?>
""",
    'members/add.php': """<?php
include('../includes/auth.php');
include('../config/db.php');

$message = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['name'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $mobile = trim($_POST['mobile'] ?? '');
    $address = trim($_POST['address'] ?? '');

    if ($name === '' || $email === '' || $mobile === '' || $address === '') {
        $message = 'Please complete every field.';
    } else {
        $stmt = $conn->prepare('INSERT INTO members (name, email, mobile, address) VALUES (?, ?, ?, ?)');
        $stmt->bind_param('ssss', $name, $email, $mobile, $address);
        $stmt->execute();

        if ($stmt->affected_rows > 0) {
            $message = 'Member added successfully.';
        } else {
            $message = 'Unable to add member. Please try again.';
        }
    }
}
?>
<?php include('../includes/header.php'); ?>
<div class="card shadow-sm mb-4">
    <div class="card-header">
        <h4>Add New Member</h4>
    </div>
    <div class="card-body">
        <?php if ($message): ?>
            <div class="alert alert-info"><?= htmlspecialchars($message); ?></div>
        <?php endif; ?>
        <form method="POST">
            <div class="row g-3">
                <div class="col-md-6">
                    <label class="form-label">Name</label>
                    <input type="text" name="name" class="form-control" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Email</label>
                    <input type="email" name="email" class="form-control" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Mobile</label>
                    <input type="text" name="mobile" class="form-control" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Address</label>
                    <input type="text" name="address" class="form-control" required>
                </div>
            </div>
            <button type="submit" class="btn btn-primary mt-4">Save Member</button>
        </form>
    </div>
</div>
<?php include('../includes/footer.php'); ?>
""",
    'members/edit.php': """<?php
include('../includes/auth.php');
include('../config/db.php');

$id = intval($_GET['id'] ?? 0);
if ($id <= 0) {
    header('Location: list.php');
    exit();
}

$message = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['name'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $mobile = trim($_POST['mobile'] ?? '');
    $address = trim($_POST['address'] ?? '');

    if ($name === '' || $email === '' || $mobile === '' || $address === '') {
        $message = 'Please complete every field.';
    } else {
        $stmt = $conn->prepare('UPDATE members SET name = ?, email = ?, mobile = ?, address = ? WHERE id = ?');
        $stmt->bind_param('ssssi', $name, $email, $mobile, $address, $id);
        $stmt->execute();

        if ($stmt->affected_rows >= 0) {
            $message = 'Member updated successfully.';
        } else {
            $message = 'Unable to update member. Please try again.';
        }
    }
}

$stmt = $conn->prepare('SELECT * FROM members WHERE id = ?');
$stmt->bind_param('i', $id);
$stmt->execute();
$result = $stmt->get_result();
$member = $result->fetch_assoc();
if (!$member) {
    header('Location: list.php');
    exit();
}
?>
<?php include('../includes/header.php'); ?>
<div class="card shadow-sm mb-4">
    <div class="card-header">
        <h4>Edit Member</h4>
    </div>
    <div class="card-body">
        <?php if ($message): ?>
            <div class="alert alert-info"><?= htmlspecialchars($message); ?></div>
        <?php endif; ?>
        <form method="POST">
            <div class="row g-3">
                <div class="col-md-6">
                    <label class="form-label">Name</label>
                    <input type="text" name="name" class="form-control" value="<?= htmlspecialchars($member['name']); ?>" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Email</label>
                    <input type="email" name="email" class="form-control" value="<?= htmlspecialchars($member['email']); ?>" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Mobile</label>
                    <input type="text" name="mobile" class="form-control" value="<?= htmlspecialchars($member['mobile']); ?>" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Address</label>
                    <input type="text" name="address" class="form-control" value="<?= htmlspecialchars($member['address']); ?>" required>
                </div>
            </div>
            <button type="submit" class="btn btn-primary mt-4">Update Member</button>
        </form>
    </div>
</div>
<?php include('../includes/footer.php'); ?>
""",
    'members/delete.php': """<?php
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
?>""",
    'members/list.php': """<?php
include('../includes/auth.php');
include('../config/db.php');

$search = trim($_GET['search'] ?? '');
$where = '';
$params = [];
$types = '';
if ($search !== '') {
    $where = "WHERE name LIKE ? OR email LIKE ? OR mobile LIKE ? OR address LIKE ?";
    $value = '%' . $search . '%';
    $params = [$value, $value, $value, $value];
    $types = 'ssss';
}

$sql = "SELECT * FROM members $where ORDER BY reg_date DESC";
$stmt = $conn->prepare($sql);
if ($where !== '') {
    $stmt->bind_param($types, ...$params);
}
$stmt->execute();
$result = $stmt->get_result();
?>
<?php include('../includes/header.php'); ?>
<div class="d-flex justify-content-between align-items-center mb-4">
    <h4>Member List</h4>
    <a href="add.php" class="btn btn-success">Add New Member</a>
</div>
<div class="row mb-3">
    <div class="col-md-6">
        <form method="GET" class="d-flex" autocomplete="off">
            <input type="text" name="search" value="<?= htmlspecialchars($search); ?>" class="form-control me-2" placeholder="Search members...">
            <button class="btn btn-outline-primary">Search</button>
        </form>
    </div>
</div>
<div class="table-responsive">
    <table class="table table-hover table-bordered align-middle">
        <thead class="table-dark">
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Mobile</th>
                <th>Address</th>
                <th>Registered</th>
                <th class="no-print">Actions</th>
            </tr>
        </thead>
        <tbody>
            <?php while ($member = $result->fetch_assoc()): ?>
                <tr>
                    <td><?= htmlspecialchars($member['id']); ?></td>
                    <td><?= htmlspecialchars($member['name']); ?></td>
                    <td><?= htmlspecialchars($member['email']); ?></td>
                    <td><?= htmlspecialchars($member['mobile']); ?></td>
                    <td><?= htmlspecialchars($member['address']); ?></td>
                    <td><?= htmlspecialchars($member['reg_date']); ?></td>
                    <td class="no-print">
                        <a href="edit.php?id=<?= $member['id']; ?>" class="btn btn-sm btn-primary">Edit</a>
                        <a href="delete.php?id=<?= $member['id']; ?>" class="btn btn-sm btn-danger" onclick="return confirm('Delete this member?');">Delete</a>
                    </td>
                </tr>
            <?php endwhile; ?>
        </tbody>
    </table>
</div>
<?php include('../includes/footer.php'); ?>
""",
    'issue/issue_book.php': """<?php
include('../includes/auth.php');
include('../config/db.php');

$message = '';

$members = $conn->query('SELECT id, name FROM members ORDER BY name ASC');
$books = $conn->query('SELECT id, book_name, available_copies FROM books WHERE available_copies > 0 ORDER BY book_name ASC');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $member_id = intval($_POST['member_id'] ?? 0);
    $book_id = intval($_POST['book_id'] ?? 0);
    $issue_date = $_POST['issue_date'] ?? '';
    $due_date = $_POST['due_date'] ?? '';

    if ($member_id <= 0 || $book_id <= 0 || $issue_date === '' || $due_date === '') {
        $message = 'Please select a member, a book, and enter both dates.';
    } elseif (strtotime($due_date) < strtotime($issue_date)) {
        $message = 'Due date must be after or equal to issue date.';
    } else {
        $bookStmt = $conn->prepare('SELECT available_copies FROM books WHERE id = ?');
        $bookStmt->bind_param('i', $book_id);
        $bookStmt->execute();
        $available = $bookStmt->get_result()->fetch_assoc()['available_copies'] ?? 0;

        if ($available <= 0) {
            $message = 'Selected book is not available.';
        } else {
            $stmt = $conn->prepare('INSERT INTO book_issue (member_id, book_id, issue_date, due_date, status) VALUES (?, ?, ?, ?, "Issued")');
            $stmt->bind_param('iiss', $member_id, $book_id, $issue_date, $due_date);
            $stmt->execute();
            if ($stmt->affected_rows > 0) {
                $update = $conn->prepare('UPDATE books SET available_copies = available_copies - 1 WHERE id = ?');
                $update->bind_param('i', $book_id);
                $update->execute();
                $message = 'Book issued successfully.';
            } else {
                $message = 'Unable to issue book. Please try again.';
            }
        }
    }
}

$issuedList = $conn->query('SELECT bi.id, m.name AS member_name, b.book_name, bi.issue_date, bi.due_date, bi.status FROM book_issue bi JOIN members m ON bi.member_id = m.id JOIN books b ON bi.book_id = b.id ORDER BY bi.issue_date DESC');
?>
<?php include('../includes/header.php'); ?>
<div class="card shadow-sm mb-4">
    <div class="card-header">
        <h4>Issue Book</h4>
    </div>
    <div class="card-body">
        <?php if ($message): ?>
            <div class="alert alert-info"><?= htmlspecialchars($message); ?></div>
        <?php endif; ?>
        <form method="POST">
            <div class="row g-3">
                <div class="col-md-6">
                    <label class="form-label">Member</label>
                    <select name="member_id" class="form-select" required>
                        <option value="">Select Member</option>
                        <?php while ($member = $members->fetch_assoc()): ?>
                            <option value="<?= $member['id']; ?>"><?= htmlspecialchars($member['name']); ?></option>
                        <?php endwhile; ?>
                    </select>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Book</label>
                    <select name="book_id" class="form-select" required>
                        <option value="">Select Book</option>
                        <?php while ($book = $books->fetch_assoc()): ?>
                            <option value="<?= $book['id']; ?>"><?= htmlspecialchars($book['book_name']); ?> (<?= $book['available_copies']; ?> available)</option>
                        <?php endwhile; ?>
                    </select>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Issue Date</label>
                    <input type="date" name="issue_date" class="form-control" value="<?= date('Y-m-d'); ?>" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Due Date</label>
                    <input type="date" name="due_date" class="form-control" value="<?= date('Y-m-d', strtotime('+7 days')); ?>" required>
                </div>
            </div>
            <button type="submit" class="btn btn-primary mt-4">Issue Book</button>
        </form>
    </div>
</div>
<div class="card shadow-sm">
    <div class="card-header">
        <h4>Recent Issued Books</h4>
    </div>
    <div class="card-body table-responsive">
        <table class="table table-bordered align-middle mb-0">
            <thead class="table-dark">
                <tr>
                    <th>ID</th>
                    <th>Member</th>
                    <th>Book</th>
                    <th>Issue Date</th>
                    <th>Due Date</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <?php while ($row = $issuedList->fetch_assoc()): ?>
                    <tr>
                        <td><?= htmlspecialchars($row['id']); ?></td>
                        <td><?= htmlspecialchars($row['member_name']); ?></td>
                        <td><?= htmlspecialchars($row['book_name']); ?></td>
                        <td><?= htmlspecialchars($row['issue_date']); ?></td>
                        <td><?= htmlspecialchars($row['due_date']); ?></td>
                        <td><?= htmlspecialchars($row['status']); ?></td>
                    </tr>
                <?php endwhile; ?>
            </tbody>
        </table>
    </div>
</div>
<?php include('../includes/footer.php'); ?>
""",
    'issue/return_book.php': """<?php
include('../includes/auth.php');
include('../config/db.php');

$message = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['issue_id'])) {
    $issue_id = intval($_POST['issue_id']);

    $stmt = $conn->prepare('SELECT bi.*, b.id AS book_id, b.book_name, b.available_copies FROM book_issue bi JOIN books b ON bi.book_id = b.id WHERE bi.id = ? AND bi.status = "Issued"');
    $stmt->bind_param('i', $issue_id);
    $stmt->execute();
    $issue = $stmt->get_result()->fetch_assoc();

    if ($issue) {
        $return_date = date('Y-m-d');
        $due_date = $issue['due_date'];
        $days_overdue = max(0, (int) floor((strtotime($return_date) - strtotime($due_date)) / 86400));
        $fine_amount = $days_overdue * 5;

        $insert = $conn->prepare('INSERT INTO book_return (issue_id, return_date, fine_amount) VALUES (?, ?, ?)');
        $insert->bind_param('isd', $issue_id, $return_date, $fine_amount);
        $insert->execute();

        if ($insert->affected_rows > 0) {
            $return_id = $conn->insert_id;
            $fineStmt = $conn->prepare('INSERT INTO fines (return_id, member_id, book_id, days_overdue, fine_amount) VALUES (?, ?, ?, ?, ?)');
            $fineStmt->bind_param('iiiid', $return_id, $issue['member_id'], $issue['book_id'], $days_overdue, $fine_amount);
            $fineStmt->execute();

            $conn->query('UPDATE book_issue SET status = "Returned" WHERE id = ' . $issue_id);
            $conn->query('UPDATE books SET available_copies = available_copies + 1 WHERE id = ' . $issue['book_id']);
            $message = 'Book returned successfully. Fine amount: ₹' . number_format($fine_amount, 2);
        } else {
            $message = 'Unable to process return. Please try again.';
        }
    } else {
        $message = 'Selected issue record is not available for return.';
    }
}

$issuedBooks = $conn->query('SELECT bi.id, m.name AS member_name, b.book_name, bi.issue_date, bi.due_date, bi.status FROM book_issue bi JOIN members m ON bi.member_id = m.id JOIN books b ON bi.book_id = b.id WHERE bi.status = "Issued" ORDER BY bi.due_date ASC');
$returned = $conn->query('SELECT br.id, bi.id AS issue_id, m.name AS member_name, b.book_name, br.return_date, br.fine_amount FROM book_return br JOIN book_issue bi ON br.issue_id = bi.id JOIN members m ON bi.member_id = m.id JOIN books b ON bi.book_id = b.id ORDER BY br.return_date DESC');
?>
<?php include('../includes/header.php'); ?>
<div class="card shadow-sm mb-4">
    <div class="card-header">
        <h4>Return Book</h4>
    </div>
    <div class="card-body">
        <?php if ($message): ?>
            <div class="alert alert-info"><?= htmlspecialchars($message); ?></div>
        <?php endif; ?>
        <div class="table-responsive mb-4">
            <table class="table table-bordered align-middle mb-0">
                <thead class="table-dark">
                    <tr>
                        <th>ID</th>
                        <th>Member</th>
                        <th>Book</th>
                        <th>Issue Date</th>
                        <th>Due Date</th>
                        <th class="no-print">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <?php while ($row = $issuedBooks->fetch_assoc()): ?>
                        <tr>
                            <td><?= htmlspecialchars($row['id']); ?></td>
                            <td><?= htmlspecialchars($row['member_name']); ?></td>
                            <td><?= htmlspecialchars($row['book_name']); ?></td>
                            <td><?= htmlspecialchars($row['issue_date']); ?></td>
                            <td><?= htmlspecialchars($row['due_date']); ?></td>
                            <td class="no-print">
                                <form method="POST" class="d-inline">
                                    <input type="hidden" name="issue_id" value="<?= $row['id']; ?>">
                                    <button type="submit" class="btn btn-sm btn-success" onclick="return confirm('Return this book now?');">Return</button>
                                </form>
                            </td>
                        </tr>
                    <?php endwhile; ?>
                </tbody>
            </table>
        </div>
        <div class="card">
            <div class="card-header">Recent Returns</div>
            <div class="card-body table-responsive">
                <table class="table table-bordered align-middle mb-0">
                    <thead class="table-dark">
                        <tr>
                            <th>ID</th>
                            <th>Return Date</th>
                            <th>Member</th>
                            <th>Book</th>
                            <th>Fine (₹)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php while ($row = $returned->fetch_assoc()): ?>
                            <tr>
                                <td><?= htmlspecialchars($row['id']); ?></td>
                                <td><?= htmlspecialchars($row['return_date']); ?></td>
                                <td><?= htmlspecialchars($row['member_name']); ?></td>
                                <td><?= htmlspecialchars($row['book_name']); ?></td>
                                <td><?= htmlspecialchars(number_format($row['fine_amount'], 2)); ?></td>
                            </tr>
                        <?php endwhile; ?>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
<?php include('../includes/footer.php'); ?>
""",
    'reports/books_report.php': """<?php
include('../includes/auth.php');
include('../config/db.php');
$result = $conn->query('SELECT * FROM books ORDER BY book_name ASC');
?>
<?php include('../includes/header.php'); ?>
<div class="d-flex justify-content-between align-items-center mb-4 no-print">
    <h4>Books Report</h4>
    <button class="btn btn-secondary" onclick="exportPDF()">Export to PDF</button>
</div>
<div class="table-responsive">
    <table class="table table-bordered align-middle">
        <thead class="table-dark">
            <tr>
                <th>ID</th>
                <th>ISBN</th>
                <th>Book Name</th>
                <th>Author</th>
                <th>Publisher</th>
                <th>Category</th>
                <th>Quantity</th>
                <th>Available</th>
            </tr>
        </thead>
        <tbody>
            <?php while ($book = $result->fetch_assoc()): ?>
                <tr>
                    <td><?= htmlspecialchars($book['id']); ?></td>
                    <td><?= htmlspecialchars($book['isbn']); ?></td>
                    <td><?= htmlspecialchars($book['book_name']); ?></td>
                    <td><?= htmlspecialchars($book['author']); ?></td>
                    <td><?= htmlspecialchars($book['publisher']); ?></td>
                    <td><?= htmlspecialchars($book['category']); ?></td>
                    <td><?= htmlspecialchars($book['quantity']); ?></td>
                    <td><?= htmlspecialchars($book['available_copies']); ?></td>
                </tr>
            <?php endwhile; ?>
        </tbody>
    </table>
</div>
<?php include('../includes/footer.php'); ?>
""",
    'reports/members_report.php': """<?php
include('../includes/auth.php');
include('../config/db.php');
$result = $conn->query('SELECT * FROM members ORDER BY reg_date DESC');
?>
<?php include('../includes/header.php'); ?>
<div class="d-flex justify-content-between align-items-center mb-4 no-print">
    <h4>Members Report</h4>
    <button class="btn btn-secondary" onclick="exportPDF()">Export to PDF</button>
</div>
<div class="table-responsive">
    <table class="table table-bordered align-middle">
        <thead class="table-dark">
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Mobile</th>
                <th>Address</th>
                <th>Registration Date</th>
            </tr>
        </thead>
        <tbody>
            <?php while ($member = $result->fetch_assoc()): ?>
                <tr>
                    <td><?= htmlspecialchars($member['id']); ?></td>
                    <td><?= htmlspecialchars($member['name']); ?></td>
                    <td><?= htmlspecialchars($member['email']); ?></td>
                    <td><?= htmlspecialchars($member['mobile']); ?></td>
                    <td><?= htmlspecialchars($member['address']); ?></td>
                    <td><?= htmlspecialchars($member['reg_date']); ?></td>
                </tr>
            <?php endwhile; ?>
        </tbody>
    </table>
</div>
<?php include('../includes/footer.php'); ?>
""",
    'reports/issue_report.php': """<?php
include('../includes/auth.php');
include('../config/db.php');
$result = $conn->query('SELECT bi.id, m.name AS member_name, b.book_name, bi.issue_date, bi.due_date, bi.status FROM book_issue bi JOIN members m ON bi.member_id = m.id JOIN books b ON bi.book_id = b.id ORDER BY bi.issue_date DESC');
?>
<?php include('../includes/header.php'); ?>
<div class="d-flex justify-content-between align-items-center mb-4 no-print">
    <h4>Issued Books Report</h4>
    <button class="btn btn-secondary" onclick="exportPDF()">Export to PDF</button>
</div>
<div class="table-responsive">
    <table class="table table-bordered align-middle">
        <thead class="table-dark">
            <tr>
                <th>Issue ID</th>
                <th>Member</th>
                <th>Book</th>
                <th>Issue Date</th>
                <th>Due Date</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            <?php while ($row = $result->fetch_assoc()): ?>
                <tr>
                    <td><?= htmlspecialchars($row['id']); ?></td>
                    <td><?= htmlspecialchars($row['member_name']); ?></td>
                    <td><?= htmlspecialchars($row['book_name']); ?></td>
                    <td><?= htmlspecialchars($row['issue_date']); ?></td>
                    <td><?= htmlspecialchars($row['due_date']); ?></td>
                    <td><?= htmlspecialchars($row['status']); ?></td>
                </tr>
            <?php endwhile; ?>
        </tbody>
    </table>
</div>
<?php include('../includes/footer.php'); ?>
""",
    'reports/fine_report.php': """<?php
include('../includes/auth.php');
include('../config/db.php');
$result = $conn->query('SELECT f.id, m.name AS member_name, b.book_name, br.return_date, f.days_overdue, f.fine_amount FROM fines f JOIN book_return br ON f.return_id = br.id JOIN book_issue bi ON br.issue_id = bi.id JOIN members m ON f.member_id = m.id JOIN books b ON f.book_id = b.id ORDER BY br.return_date DESC');
?>
<?php include('../includes/header.php'); ?>
<div class="d-flex justify-content-between align-items-center mb-4 no-print">
    <h4>Fine Report</h4>
    <button class="btn btn-secondary" onclick="exportPDF()">Export to PDF</button>
</div>
<div class="table-responsive">
    <table class="table table-bordered align-middle">
        <thead class="table-dark">
            <tr>
                <th>ID</th>
                <th>Member</th>
                <th>Book</th>
                <th>Return Date</th>
                <th>Days Overdue</th>
                <th>Fine Amount (₹)</th>
            </tr>
        </thead>
        <tbody>
            <?php while ($row = $result->fetch_assoc()): ?>
                <tr>
                    <td><?= htmlspecialchars($row['id']); ?></td>
                    <td><?= htmlspecialchars($row['member_name']); ?></td>
                    <td><?= htmlspecialchars($row['book_name']); ?></td>
                    <td><?= htmlspecialchars($row['return_date']); ?></td>
                    <td><?= htmlspecialchars($row['days_overdue']); ?></td>
                    <td><?= htmlspecialchars(number_format($row['fine_amount'], 2)); ?></td>
                </tr>
            <?php endwhile; ?>
        </tbody>
    </table>
</div>
<?php include('../includes/footer.php'); ?>
""",
    'database/library_management.sql': """CREATE DATABASE IF NOT EXISTS library_management;
USE library_management;

CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(50) NOT NULL,
    book_name VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    publisher VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    available_copies INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    mobile VARCHAR(20) NOT NULL,
    address TEXT NOT NULL,
    reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS book_issue (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    book_id INT NOT NULL,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    status ENUM('Issued', 'Returned') NOT NULL DEFAULT 'Issued',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS book_return (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NOT NULL,
    return_date DATE NOT NULL,
    fine_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (issue_id) REFERENCES book_issue(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS fines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    return_id INT NOT NULL,
    member_id INT NOT NULL,
    book_id INT NOT NULL,
    days_overdue INT NOT NULL DEFAULT 0,
    fine_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (return_id) REFERENCES book_return(id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);

INSERT INTO admins (username, password) VALUES ('admin', '$2b$12$X6kZBT.oLIVmNp9FbE1so.KsUog7D6dcmFUMKLM2twcVMXLmjjygi');

INSERT INTO books (isbn, book_name, author, publisher, category, quantity, available_copies) VALUES
('9780140449136', 'The Odyssey', 'Homer', 'Penguin Classics', 'Classics', 5, 5),
('9780307277671', 'Sapiens', 'Yuval Noah Harari', 'Harper', 'History', 4, 4),
('9780596007126', 'Head First PHP & MySQL', 'Lynn Beighley', 'O'Reilly Media', 'Programming', 3, 3);

INSERT INTO members (name, email, mobile, address) VALUES
('Rohit Sharma', 'rohit@example.com', '9876543210', '123 Main Street, Delhi'),
('Meera Patel', 'meera@example.com', '9123456780', '45 Park Avenue, Mumbai');
"""
}

root = Path(__file__).parent
for relative_path, content in files.items():
    target = root / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding='utf-8')
print('Generated', len(files), 'files.')
