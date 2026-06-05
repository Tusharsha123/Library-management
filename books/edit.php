<?php
include('../includes/auth.php');
include('../config/db.php');

$id = intval($_GET['id'] ?? 0);
if ($id <= 0) {
    header('Location: list.php');
    exit();
}

$message = '';

$stmt = $conn->prepare('SELECT * FROM books WHERE id = ?');
$stmt->bind_param('i', $id);
$stmt->execute();
$result = $stmt->get_result();
$book = $result->fetch_assoc();
if (!$book) {
    header('Location: list.php');
    exit();
}

$issuedCount = max(0, $book['quantity'] - $book['available_copies']);

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $isbn = trim($_POST['isbn'] ?? '');
    $book_name = trim($_POST['book_name'] ?? '');
    $author = trim($_POST['author'] ?? '');
    $publisher = trim($_POST['publisher'] ?? '');
    $category = trim($_POST['category'] ?? '');
    $quantity = intval($_POST['quantity'] ?? 0);

    if ($isbn === '' || $book_name === '' || $author === '' || $publisher === '' || $category === '' || $quantity < 0) {
        $message = 'Please complete the form and enter a valid quantity.';
    } elseif ($quantity < $issuedCount) {
        $message = 'Quantity cannot be less than the number of already issued copies (' . $issuedCount . ').';
    } else {
        $availableCopies = $quantity - $issuedCount;
        $stmt = $conn->prepare('UPDATE books SET isbn = ?, book_name = ?, author = ?, publisher = ?, category = ?, quantity = ?, available_copies = ? WHERE id = ?');
        $stmt->bind_param('sssssiii', $isbn, $book_name, $author, $publisher, $category, $quantity, $availableCopies, $id);
        $stmt->execute();

        if ($stmt->affected_rows >= 0) {
            $message = 'Book updated successfully.';
            $book['isbn'] = $isbn;
            $book['book_name'] = $book_name;
            $book['author'] = $author;
            $book['publisher'] = $publisher;
            $book['category'] = $category;
            $book['quantity'] = $quantity;
            $book['available_copies'] = $availableCopies;
        } else {
            $message = 'Unable to update book. Please try again.';
        }
    }
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
