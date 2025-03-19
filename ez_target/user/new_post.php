<?php
require_once '../config.php';

if (!isLoggedIn()) {
    header('Location: ../login.php');
    exit;
}

$user_id = getCurrentUserId();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $title = $_POST['title'] ?? '';
    $content = $_POST['content'] ?? '';
    
    if ($title && $content) {
        $conn = getDbConnection();
        $sql = "INSERT INTO posts (title, content, author_id) VALUES ('$title', '$content', $user_id)";
        
        if (mysqli_query($conn, $sql)) {
            $success = "文章发布成功！";
        } else {
            $error = "发布失败：" . mysqli_error($conn);
        }
    } else {
        $error = "标题和内容不能为空！";
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>发布文章 - Ez Target博客</title>
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
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #2c5a2c;
        }
        input[type="text"],
        textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        textarea {
            height: 300px;
            resize: vertical;
        }
        button {
            background-color: #2c5a2c;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #1f3f1f;
        }
        .success {
            color: green;
            margin-bottom: 15px;
        }
        .error {
            color: red;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>发布文章</h1>
        
        <?php if (isset($success)): ?>
            <div class="success"><?php echo $success; ?></div>
        <?php endif; ?>
        
        <?php if (isset($error)): ?>
            <div class="error"><?php echo $error; ?></div>
        <?php endif; ?>
        
        <form method="POST">
            <div class="form-group">
                <label for="title">文章标题</label>
                <input type="text" id="title" name="title" required>
            </div>
            
            <div class="form-group">
                <label for="content">文章内容</label>
                <textarea id="content" name="content" required></textarea>
            </div>
            
            <button type="submit">发布文章</button>
            <a href="dashboard.php" style="margin-left: 10px; color: #2c5a2c;">返回后台</a>
        </form>
    </div>
</body>
</html> 