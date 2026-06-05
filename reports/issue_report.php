<?php
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
