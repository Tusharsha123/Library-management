<?php
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
