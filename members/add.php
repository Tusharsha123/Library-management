<?php
include('../includes/auth.php');
include('../config/db.php');

$message = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['name'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $mobile = trim($_POST['mobile'] ?? '');
    $address = trim($_POST['address'] ?? '');

    if ($name === '' || $email === '' || $mobile === '' || $address === '') {
        $message = 'Please complete every field.';
    } else {
        $stmt = $conn->prepare('INSERT INTO members (name, email, mobile, address) VALUES (?, ?, ?, ?)');
        $stmt->bind_param('ssss', $name, $email, $mobile, $address);
        $stmt->execute();

        if ($stmt->affected_rows > 0) {
            $message = 'Member added successfully.';
        } else {
            $message = 'Unable to add member. Please try again.';
        }
    }
}
?>
<?php include('../includes/header.php'); ?>
<div class="card shadow-sm mb-4">
    <div class="card-header">
        <h4>Add New Member</h4>
    </div>
    <div class="card-body">
        <?php if ($message): ?>
            <div class="alert alert-info"><?= htmlspecialchars($message); ?></div>
        <?php endif; ?>
        <form method="POST">
            <div class="row g-3">
                <div class="col-md-6">
                    <label class="form-label">Name</label>
                    <input type="text" name="name" class="form-control" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Email</label>
                    <input type="email" name="email" class="form-control" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Mobile</label>
                    <input type="text" name="mobile" class="form-control" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Address</label>
                    <input type="text" name="address" class="form-control" required>
                </div>
            </div>
            <button type="submit" class="btn btn-primary mt-4">Save Member</button>
        </form>
    </div>
</div>
<?php include('../includes/footer.php'); ?>
