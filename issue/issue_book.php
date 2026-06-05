<?php
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
