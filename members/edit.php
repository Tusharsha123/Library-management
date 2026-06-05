<?php
include('../includes/auth.php');
include('../config/db.php');

$id = intval($_GET['id'] ?? 0);
if ($id <= 0) {
    header('Location: list.php');
    exit();
}

$message = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['name'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $mobile = trim($_POST['mobile'] ?? '');
    $address = trim($_POST['address'] ?? '');

    if ($name === '' || $email === '' || $mobile === '' || $address === '') {
        $message = 'Please complete every field.';
    } else {
        $stmt = $conn->prepare('UPDATE members SET name = ?, email = ?, mobile = ?, address = ? WHERE id = ?');
        $stmt->bind_param('ssssi', $name, $email, $mobile, $address, $id);
        $stmt->execute();

        if ($stmt->affected_rows >= 0) {
            $message = 'Member updated successfully.';
        } else {
            $message = 'Unable to update member. Please try again.';
        }
    }
}

$stmt = $conn->prepare('SELECT * FROM members WHERE id = ?');
$stmt->bind_param('i', $id);
$stmt->execute();
$result = $stmt->get_result();
$member = $result->fetch_assoc();
if (!$member) {
    header('Location: list.php');
    exit();
}
?>
<?php include('../includes/header.php'); ?>
<div class="card shadow-sm mb-4">
    <div class="card-header">
        <h4>Edit Member</h4>
    </div>
    <div class="card-body">
        <?php if ($message): ?>
            <div class="alert alert-info"><?= htmlspecialchars($message); ?></div>
        <?php endif; ?>
        <form method="POST">
            <div class="row g-3">
                <div class="col-md-6">
                    <label class="form-label">Name</label>
                    <input type="text" name="name" class="form-control" value="<?= htmlspecialchars($member['name']); ?>" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Email</label>
                    <input type="email" name="email" class="form-control" value="<?= htmlspecialchars($member['email']); ?>" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Mobile</label>
                    <input type="text" name="mobile" class="form-control" value="<?= htmlspecialchars($member['mobile']); ?>" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Address</label>
                    <input type="text" name="address" class="form-control" value="<?= htmlspecialchars($member['address']); ?>" required>
                </div>
            </div>
            <button type="submit" class="btn btn-primary mt-4">Update Member</button>
        </form>
    </div>
</div>
<?php include('../includes/footer.php'); ?>
