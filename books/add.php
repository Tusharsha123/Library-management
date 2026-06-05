<?php
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
        $stmt->bind_param('sssssii', $isbn, $book_name, $author, $publisher, $category, $quantity, $quantity);
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
