<?php
require_once '../config.php';

// 只检查是否登录，不检查是否是管理员（垂直越权漏洞）
if (!isLoggedIn()) {
    header('Location: ../login.php');
    exit;
}

$conn = getDbConnection();

// 处理删除用户请求
if (isset($_GET['delete'])) {
    $delete_id = $_GET['delete'];
    $sql = "DELETE FROM users WHERE id = $delete_id";
    mysqli_query($conn, $sql);
    header('Location: manage_users.php');
    exit;
}

// 获取所有用户列表
$sql = "SELECT * FROM users ORDER BY created_at DESC";
$result = mysqli_query($conn, $sql);
?>

<!DOCTYPE html>
<html>
<head>
    <title>管理用户 - Ez Target博客</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f0f8f0;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f0f8f0;
            color: #2c5a2c;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .actions {
            display: flex;
            gap: 10px;
        }
        .action-link {
            color: #2c5a2c;
            text-decoration: none;
        }
        .action-link:hover {
            text-decoration: underline;
        }
        .delete-link {
            color: #cc0000;
        }
        .back-link {
            margin-top: 20px;
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>管理用户</h1>
        
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>用户名</th>
                    <th>角色</th>
                    <th>注册时间</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
                <?php while ($user = mysqli_fetch_assoc($result)): ?>
                    <tr>
                        <td><?php echo $user['id']; ?></td>
                        <td><?php echo htmlspecialchars($user['username']); ?></td>
                        <td><?php echo $user['role'] === 'admin' ? '管理员' : '普通用户'; ?></td>
                        <td><?php echo $user['created_at']; ?></td>
                        <td class="actions">
                            <a href="profile.php?user_id=<?php echo $user['id']; ?>" class="action-link">查看</a>
                            <a href="manage_users.php?delete=<?php echo $user['id']; ?>" 
                               class="action-link delete-link" 
                               onclick="return confirm('确定要删除此用户吗？')">删除</a>
                        </td>
                    </tr>
                <?php endwhile; ?>
            </tbody>
        </table>
        
        <a href="dashboard.php" class="action-link back-link">返回后台</a>
    </div>
</body>
</html> 