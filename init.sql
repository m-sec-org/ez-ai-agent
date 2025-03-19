-- 创建数据库
DROP DATABASE IF EXISTS ez_target;
CREATE DATABASE ez_target CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ez_target;

-- 设置连接字符集
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET character_set_connection = utf8mb4;
SET character_set_database = utf8mb4;
SET character_set_results = utf8mb4;
SET character_set_server = utf8mb4;

-- 创建用户表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    real_name VARCHAR(50),
    phone VARCHAR(20),
    profile_info TEXT,
    avatar_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建文章表
CREATE TABLE posts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    author_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入初始用户数据
INSERT INTO users (username, password, role, real_name, phone, profile_info) VALUES
('admin', '123456', 'admin', '管理员', '13800138000', '管理员账户'),
('test', 'test', 'user', '测试用户', '13900139000', '测试用户账户'),
('lili', 'password123', 'user', '李小明', '13700137000', '李小明的个人账户'),
('do9gy', 'do9gy123', 'user', '王小明', '13600136000', '王小明的个人账户'),
('loid', 'loid123', 'user', '周小明', '13500135000', '周小明的个人账户'),
('maktub', 'password123', 'user', '刘小明', '13400134000', '刘小明的个人账户');


-- 插入一些测试文章
INSERT INTO posts (title, content, author_id) VALUES
('EZ 介绍', 'EZ是一款集信息收集、端口扫描、服务爆破、指纹识别、被动扫描为一体的跨平台漏洞扫描器，渗透测试中，可辅助发现常见的SQL注入、XSS、XXE、SSRF之类的漏洞，通过内置的POC辅助发现Apache Shiro、RabbitMQ、Struts2之类的通用组件漏洞，以及某服VPN、通达OA以及泛微OA之类的被曝出已知漏洞的系统，可谓是外围打点，破局进内网，全面发现漏洞的渗透测试必备武器，EZ在手，shell我有。', 1),
('免责声明', '1、本软件仅用于经授权的渗透测试使用，请在使用本工具进行渗透测试前，必须获得直接测试目标单位的书面授权。非经被测试目标单位授权，禁止使用本工具实施任何未经许可的测试行为。\n 2、用户通过使用本软件所获取的任何资产或漏洞等信息，必须严格按照测试目标单位的要求予以处理，未经许可不得对信息另行加工、对外传输提供及非法公开。\n3、本软件通过提交申请信息，提供证书授权给用户使用，默认授权使用时间为1个月，禁止任何形式的复制、分发和传播该证书。用户应对授权期间的使用行为负责，如未取得被测试目标单位的授权或随意复制、分发及传播该证书致使本软件被他人恶意使用而导致的违法责任，用户应依法承担相应责任。\n4、禁止对本软件实施逆向工程、反编译、篡改软件认证流程和试图破译源代码等行为，通过前述行为恶意绕开软件使用的管控限制。\n5、如发现用户您有上述禁止行为，或者在使用本软件过程中存在任何非法行为，我们将保留追究用户您法律责任的权利，并将配合执法单位提供证据材料，追究违法责任。\n6、我们已对软件使用合规要件做了充分提示，具体详见前第1-4项内容，如用户违法前述要求导致的任何责任，与我们无关，将由用户自行承担全部责任。 为保证软件使用行为即渗透测试行为的可追溯，本软件在使用期间将有限收集个人PC信息，包括MAC地址、本机IP地址以及启动时间等，必要时将提供政府监管部门，请用户知悉。', 1),
('EZ 特性', '1. 多维度资产及信息搜集：子域名、IP端口、URL、指纹识别...EZ一网打尽，又快又全。\n2. 通用型漏洞检测：SQL注入、XSS、Java反序列化、Log4j2、命令注入...EZ让它无处藏身。\n3. 原生协议识别：通过协议交互的最底层获取服务信息，丰富的指纹识别广度和精确度，在EZ火眼金睛下一一显形！\n4. 多维度通用系统指纹探测识别：采用自主研发的基于主动HTTP畸形报文响应的指纹识别技术，精准识别到组件最核心的功能点。EZ妙不可言!\n5. HTTP Request Reduce技术：通过采用指纹识别后发送PoC、PoC发包数量优化等手段，将单个漏洞的HTTP请求数量控制在最小化程度，精准切入，最大程度规避在扫描时引发的业务连续性影响。EZ用的放心！\n6. POC自定义：支持基于YAML、Go 的自定义PoC 编写方案，开放PoC编写文档。可通过轻量代码快速构建Web漏洞扫描插件，此外还同时支持TCP层相关协议漏洞的插件开发。EZ用法灵活！\n7. M-SEC社区支持：依靠M-SEC社区每日最新漏洞情报，不断优化和提升EZ工具的插件和使用效率，增强实战应用。同时，加入M-SEC社区还可交流EZ使用技巧，分享技术文章，探索更多安全知识。', 1),
('大家好，我是loid', '这是我的第一篇文章！', 5); 