<?php
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
