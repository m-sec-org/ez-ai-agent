<?php
// 开启session（必须在任何输出之前）
if (session_status() == PHP_SESSION_NONE) {
    session_start();
}

// 数据库配置
define('DB_HOST', 'test-target-db');
define('DB_PORT', '3306');
define('DB_USER', 'root');
define('DB_PASS', 'Password123');
define('DB_NAME', 'ez_target');

// 建立数据库连接
function getDbConnection() {
    static $conn = null;
    if ($conn === null) {
        $conn = mysqli_connect(DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT);
        if (!$conn) {
            die("连接失败: " . mysqli_connect_error());
        }
        // 设置字符集
        mysqli_query($conn, "SET NAMES utf8mb4");
        mysqli_set_charset($conn, "utf8mb4");
    }
    return $conn;
}

// 检查用户是否登录
function isLoggedIn() {
    return isset($_SESSION['user_id']);
}

// 获取当前登录用户ID
function getCurrentUserId() {
    return $_SESSION['user_id'] ?? null;
}
?>