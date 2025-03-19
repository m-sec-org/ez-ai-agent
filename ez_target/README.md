# Ez Target 博客 CTF 靶场

这是一个简单的 PHP 博客系统，专门设计用于 CTF 练习，包含多个常见的 Web 安全漏洞。

## 漏洞说明

1. **SQL 注入漏洞**
   - 位置：首页文章详情页
   - 参数：GET 参数 `id`
   - 漏洞代码：直接拼接 SQL 语句，未进行参数过滤

2. **水平越权漏洞**
   - 位置：用户资料页面
   - 参数：GET 参数 `user_id`
   - 漏洞描述：只验证登录状态，未验证用户身份

3. **垂直越权漏洞**
   - 位置：管理用户页面
   - 漏洞描述：只验证登录状态，未验证管理员权限

## 默认用户账号

1. 管理员账号
   - 用户名：admin
   - 密码：123456

2. 测试用户账号
   - 用户名：test
   - 密码：test

3. 普通用户账号
   - 用户名：lili
   - 密码：password123

## 环境要求

- PHP 7.0+
- MySQL 5.6+
- Web 服务器（Apache/Nginx）

## 安装步骤

1. 创建数据库并导入 `init.sql`
2. 修改 `config.php` 中的数据库配置
3. 确保 `uploads` 目录可写
4. 访问首页开始使用

## 目录结构

```
.
├── config.php          # 配置文件
├── index.php          # 首页
├── login.php          # 登录页面
├── logout.php         # 退出登录
├── init.sql           # 数据库初始化脚本
├── uploads/           # 上传文件目录
│   └── avatars/      # 用户头像目录
└── user/             # 用户后台目录
    ├── dashboard.php     # 后台首页
    ├── profile.php       # 个人资料
    ├── edit_profile.php  # 修改资料
    ├── new_post.php      # 发布文章
    └── manage_users.php  # 管理用户
```

## 注意事项

1. 本项目仅用于学习和练习 Web 安全测试
2. 请勿在生产环境中使用
3. 使用本项目造成的任何问题由使用者自行承担 