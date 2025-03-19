<?php
require_once '../config.php';

if (!isLoggedIn()) {
    header('Location: ../login.php');
    exit;
}

$user_id = getCurrentUserId();
$conn = getDbConnection();

// 处理表单提交
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $profile_info = $_POST['profile_info'] ?? '';
    $real_name = $_POST['real_name'] ?? '';
    $phone = $_POST['phone'] ?? '';
    
    // 处理头像上传
    if (isset($_FILES['avatar']) && $_FILES['avatar']['error'] === UPLOAD_ERR_OK) {
        $upload_dir = '../uploads/avatars/';
        if (!file_exists($upload_dir)) {
            mkdir($upload_dir, 0777, true);
        }
        
        $file_extension = pathinfo($_FILES['avatar']['name'], PATHINFO_EXTENSION);
        $file_name = $_FILES['avatar']['name'];
        $upload_path = $upload_dir . $file_name;
        
        if (move_uploaded_file($_FILES['avatar']['tmp_name'], $upload_path)) {
            $avatar_path = 'uploads/avatars/' . $file_name;
            $sql = "UPDATE users SET avatar_path = '$avatar_path' WHERE id = $user_id";
            mysqli_query($conn, $sql);
        }
    }
    
    // 更新个人资料
    $sql = "UPDATE users SET 
            profile_info = '$profile_info',
            real_name = '$real_name',
            phone = '$phone'
            WHERE id = $user_id";
            
    if (mysqli_query($conn, $sql)) {
        $success = "个人资料更新成功！";
    } else {
        $error = "更新失败：" . mysqli_error($conn);
    }
}

// 获取当前用户信息
$sql = "SELECT * FROM users WHERE id = $user_id";
$result = mysqli_query($conn, $sql);
$user = mysqli_fetch_assoc($result);
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>修改个人资料 - Ez Target博客</title>
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
            height: 100px;
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
        .avatar-preview {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            margin: 10px 0;
            background-color: #eee;
            overflow: hidden;
        }
        .avatar-preview img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>修改个人资料</h1>
        
        <?php if (isset($success)): ?>
            <div class="success"><?php echo $success; ?></div>
        <?php endif; ?>
        
        <?php if (isset($error)): ?>
            <div class="error"><?php echo $error; ?></div>
        <?php endif; ?>
        
        <form method="POST" enctype="multipart/form-data">
            <div class="form-group">
                <label>当前头像</label>
                <div class="avatar-preview">
                    <?php if ($user['avatar_path']): ?>
                        <img src="<?php echo '../' . htmlspecialchars($user['avatar_path']); ?>" alt="当前头像">
                    <?php endif; ?>
                </div>
                <label for="avatar">上传新头像</label>
                <input type="file" id="avatar" name="avatar" accept="image/*">
            </div>
            
            <div class="form-group">
                <label for="real_name">姓名</label>
                <input type="text" id="real_name" name="real_name" value="<?php echo htmlspecialchars($user['real_name']); ?>">
            </div>
            
            <div class="form-group">
                <label for="phone">电话</label>
                <input type="text" id="phone" name="phone" value="<?php echo htmlspecialchars($user['phone']); ?>">
            </div>
            
            <div class="form-group">
                <label for="profile_info">个人简介</label>
                <textarea id="profile_info" name="profile_info"><?php echo htmlspecialchars($user['profile_info']); ?></textarea>
            </div>
            
            <button type="submit">保存修改</button>
            <a href="dashboard.php" style="margin-left: 10px; color: #2c5a2c;">返回后台</a>
        </form>
    </div>
</body>
</html> 