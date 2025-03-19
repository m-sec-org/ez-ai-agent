<?php
require_once '../config.php';

// 检查是否登录
if (!isLoggedIn()) {
    header('Location: ../login.php');
    exit;
}

$user_id = getCurrentUserId();
$conn = getDbConnection();
$sql = "SELECT * FROM users WHERE id = $user_id";
$result = mysqli_query($conn, $sql);
$user = mysqli_fetch_assoc($result);
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>用户后台 - Ez Target博客</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f0f8f0;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .menu {
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        .menu a {
            color: #2c5a2c;
            text-decoration: none;
            padding: 10px;
            border-radius: 4px;
            background-color: #f0f8f0;
        }
        .menu a:hover {
            background-color: #2c5a2c;
            color: white;
        }
        .welcome {
            margin-bottom: 20px;
            color: #2c5a2c;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>用户后台</h1>
            <a href="../logout.php" style="color: #2c5a2c;">退出登录</a>
        </div>

        <div class="welcome">
            欢迎回来，<?php echo htmlspecialchars($user['username']); ?>！
        </div>

        <div class="menu">
            <a href="profile.php?user_id=<?php echo getCurrentUserId(); ?>">查看个人资料</a>
            <a href="edit_profile.php">修改个人资料</a>
            <a href="change_password.php">修改密码</a>
            <a href="new_post.php">发布文章</a>
            <?php if ($user['role'] === 'admin'): ?>
                <a href="manage_users.php">管理用户</a>
            <?php endif; ?>
            <a href="../index.php">返回首页</a>
        </div>

        <div class="content">
            <h2>最近发布的文章</h2>
            <?php
            $sql = "SELECT * FROM posts WHERE author_id = $user_id ORDER BY created_at DESC LIMIT 5";
            $result = mysqli_query($conn, $sql);
            while ($post = mysqli_fetch_assoc($result)): ?>
                <div style="margin-bottom: 15px;">
                    <h3><?php echo htmlspecialchars($post['title']); ?></h3>
                    <div style="color: #666;">
                        发布时间: <?php echo $post['created_at']; ?>
                    </div>
                </div>
            <?php endwhile; ?>
        </div>
    </div>
</body>
</html> 