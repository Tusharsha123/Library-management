<?php
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
