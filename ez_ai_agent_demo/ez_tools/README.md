# EZ 工具存放目录


## 智能表单暴破工具 (Demo 测试版)

`ez_brute_tools` 工具是 EZ 内部 **智能表单破解工具** 的独立版本。为了方便 AI Agent 调用，EZ 团队特别将其独立提取出来。未来，EZ 团队计划逐步开放更多强大的渗透测试工具，以助力 Agent 实现更精细化的工具调用。

目前，该工具为 **Demo 测试版**，仅内置了以下几组账号密码用于表单破解：

```USER
"admin", "test", "root"
```

```PASSWORD
"password", "123456", "test", "user", "Password@123", "admin123"
```

如需体验完整功能，请使用 EZ 工具，并通过 `--pocs --web-brute-active` 和 `--pocs web-brute-passive` 参数指定调用。
