<?php
include('../includes/auth.php');
include('../config/db.php');

$search = trim($_GET['search'] ?? '');
$where = '';
$params = [];
$types = '';
if ($search !== '') {
    $where = "WHERE name LIKE ? OR email LIKE ? OR mobile LIKE ? OR address LIKE ?";
    $value = '%' . $search . '%';
    $params = [$value, $value, $value, $value];
    $types = 'ssss';
}

$sql = "SELECT * FROM members $where ORDER BY reg_date DESC";
$stmt = $conn->prepare($sql);
if ($where !== '') {
    $stmt->bind_param($types, ...$params);
}
$stmt->execute();
$result = $stmt->get_result();
?>
<?php include('../includes/header.php'); ?>
<div class="d-flex justify-content-between align-items-center mb-4">
    <h4>Member List</h4>
    <a href="add.php" class="btn btn-success">Add New Member</a>
</div>
<div class="row mb-3">
    <div class="col-md-6">
        <form method="GET" class="d-flex" autocomplete="off">
            <input type="text" name="search" value="<?= htmlspecialchars($search); ?>" class="form-control me-2" placeholder="Search members...">
            <button class="btn btn-outline-primary">Search</button>
        </form>
    </div>
</div>
<div class="table-responsive">
    <table class="table table-hover table-bordered align-middle">
        <thead class="table-dark">
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Mobile</th>
                <th>Address</th>
                <th>Registered</th>
                <th class="no-print">Actions</th>
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
                    <td class="no-print">
                        <a href="edit.php?id=<?= $member['id']; ?>" class="btn btn-sm btn-primary">Edit</a>
                        <a href="delete.php?id=<?= $member['id']; ?>" class="btn btn-sm btn-danger" onclick="return confirm('Delete this member?');">Delete</a>
                    </td>
                </tr>
            <?php endwhile; ?>
        </tbody>
    </table>
</div>
<?php include('../includes/footer.php'); ?>
