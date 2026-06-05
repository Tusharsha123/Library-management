<?php
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
