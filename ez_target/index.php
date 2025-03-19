<?php
require_once 'config.php';

// 获取文章详情（存在SQL注入漏洞）
if (isset($_GET['id'])) {
    $id = $_GET['id'];
    $conn = getDbConnection();
    // 故意使用不安全的SQL查询
    $sql = "SELECT p.*, u.username as author_name FROM posts p 
            LEFT JOIN users u ON p.author_id = u.id 
            WHERE p.id = $id";
    $result = mysqli_query($conn, $sql);
    $post = mysqli_fetch_assoc($result);
}
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>EZ 的博客</title>
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
        .post {
            border-bottom: 1px solid #eee;
            padding: 10px 0;
        }
        .post h2 {
            margin: 0;
            color: #2c5a2c;
        }
        .post-meta {
            color: #666;
            font-size: 0.9em;
        }
        .login-link {
            color: #2c5a2c;
            text-decoration: none;
        }
        .login-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>EZ 的博客</h1>
            <div>
                <?php if (isLoggedIn()): ?>
                    <a href="user/dashboard.php" class="login-link">进入后台</a>
                <?php else: ?>
                    <a href="login.php" class="login-link">登录</a>
                <?php endif; ?>
            </div>
        </div>

        <?php if (isset($post)): ?>
            <!-- 文章详情页 -->
            <div class="post">
                <h2><?php echo htmlspecialchars($post['title']); ?></h2>
                <div class="post-meta">
                    作者: <?php echo htmlspecialchars($post['author_name']); ?> | 
                    发布时间: <?php echo $post['created_at']; ?>
                </div>
                <div class="post-content">
                    <?php echo nl2br(htmlspecialchars($post['content'])); ?>
                </div>
                <p><a href="index.php">返回首页</a></p>
            </div>
        <?php else: ?>
            <!-- 文章列表页 -->
            <?php
            $conn = getDbConnection();
            $sql = "SELECT p.*, u.username as author_name FROM posts p 
                    LEFT JOIN users u ON p.author_id = u.id 
                    ORDER BY p.created_at DESC";
            $result = mysqli_query($conn, $sql);
            while ($row = mysqli_fetch_assoc($result)): ?>
                <div class="post">
                    <h2><a href="index.php?id=<?php echo $row['id']; ?>" class="login-link">
                        <?php echo htmlspecialchars($row['title']); ?>
                    </a></h2>
                    <div class="post-meta">
                        作者: <?php echo htmlspecialchars($row['author_name']); ?> | 
                        发布时间: <?php echo $row['created_at']; ?>
                    </div>
                </div>
            <?php endwhile; ?>
        <?php endif; ?>
    </div>
</body>
</html> 