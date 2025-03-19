<?php
require_once '../config.php';

// 只检查是否登录，不检查用户身份（水平越权漏洞）
if (!isLoggedIn()) {
    header('Location: ../login.php');
    exit;
}

// 获取要查看的用户ID，如果没有指定则查看当前用户
$view_user_id = $_GET['user_id'] ?? getCurrentUserId();

$conn = getDbConnection();
// 直接查询指定用户的信息，没有权限验证
$sql = "SELECT * FROM users WHERE id = $view_user_id";
$result = mysqli_query($conn, $sql);
$user = mysqli_fetch_assoc($result);

if (!$user) {
    die("用户不存在");
}
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>用户资料 - Ez Target博客</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f0f8f0;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .profile-header {
            display: flex;
            align-items: center;
            margin-bottom: 30px;
        }
        .avatar {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            margin-right: 20px;
            background-color: #eee;
        }
        .profile-info {
            flex-grow: 1;
        }
        .info-item {
            margin-bottom: 15px;
        }
        .label {
            color: #666;
            margin-bottom: 5px;
        }
        .value {
            color: #2c5a2c;
            font-size: 1.1em;
        }
        .back-link {
            margin-top: 20px;
        }
        .back-link a {
            color: #2c5a2c;
            text-decoration: none;
        }
        .back-link a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="profile-header">
            <div class="avatar">
                <?php if ($user['avatar_path']): ?>
                    <img src="../<?php echo htmlspecialchars($user['avatar_path']); ?>" alt="头像" style="width: 100%; height: 100%; object-fit: cover;">
                <?php endif; ?>
            </div>
            <div class="profile-info">
                <h1><?php echo htmlspecialchars($user['username']); ?></h1>
                <div>角色: <?php echo $user['role'] === 'admin' ? '管理员' : '普通用户'; ?></div>
            </div>
        </div>

        <div class="info-item">
            <div class="label">姓名</div>
            <div class="value"><?php echo htmlspecialchars($user['real_name'] ?: '未设置'); ?></div>
        </div>

        <div class="info-item">
            <div class="label">电话</div>
            <div class="value"><?php echo htmlspecialchars($user['phone'] ?: '未设置'); ?></div>
        </div>

        <div class="info-item">
            <div class="label">个人简介</div>
            <div class="value"><?php echo nl2br(htmlspecialchars($user['profile_info'])); ?></div>
        </div>

        <div class="info-item">
            <div class="label">注册时间</div>
            <div class="value"><?php echo $user['created_at']; ?></div>
        </div>

        <div class="back-link">
            <a href="dashboard.php">返回后台</a>
        </div>
    </div>
</body>
</html> 