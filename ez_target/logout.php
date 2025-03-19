<?php
require_once 'config.php';

// 清除所有会话数据
$_SESSION = array();

if (isset($_COOKIE[session_name()])) {
    setcookie(session_name(), '', time()-3600, '/');
}

session_destroy();

// 重定向到首页
header('Location: index.php');
exit(); 