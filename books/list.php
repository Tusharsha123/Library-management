<?php
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
