<?php
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
