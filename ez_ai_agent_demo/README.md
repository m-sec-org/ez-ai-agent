# EZ AI Agent(Demo)

使用前需在 `.env` 中配置大模型的 `api_key` 和 `base_url`。

还需配置 EZ 工具被动代理的端口，由于被动代理需要 docker 网络访问使用，因此**需要使用本机的内网地址**而不是 localhost.

## 大模型 api 申请和注意事项

国内可以使用`阿里云百炼`平台申请`api_key`，使用其提供的 `deepseek` 和 `qwen-vl-max-0125` 模型。

对于 browser-use 的调用，Google 的 `gemini-2.0-flash` 模型速度和精准度优于`qwen-vl-max-0125`，且提示词在`gemini-2.0-flash`模型上进行了优化，因此采用`gemini`模型会有更好的体验。

Gemini Api 申请地址(需科学上网)：https://aistudio.google.com/

