# 🚀 LLM-Net-Probe (AI 大模型网络探针)

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![Platform](https://img.shields.io/badge/Platform-WSL2%20%7C%20Linux%20%7C%20Windows-lightgrey)

## 📌 项目简介 (Purpose)

**LLM-Net-Probe** 是一个专为 AI 开发者打造的轻量级、跨平台网络诊断工具。

在进行本地 AI 部署和大模型 API 调用时，开发者经常会遭遇宿主机与虚拟机（如 WSL2）之间的网络隔离问题，导致大模型 API (如 Groq, Gemini, Anthropic) 无法正常连通。本项目旨在提供一个一键式的诊断探针，精准验证：
1. 本地网络是否成功穿透并连接到国际节点。
2. LLM API 的鉴权 (API Key) 是否生效。
3. 指定的大模型 (Model ID) 是否存在且可用。

## 🎯 核心特性
- **穿透 WSL2 网络隔离**：兼容传统 NAT 模式与新版镜像模式，自适应抓取 Windows 宿主机动态 IP，解决 WSL2 每次重启 IP 变更导致的代理失效问题。
- **深度透视 HTTP 状态**：不再是简单的 Timeout，而是精准返回底层 JSON 报错（如 403 权限拦截、404 模型下架），大幅缩短排错时间。

---

## 🛠️ 快速开始 (Quick Start)

### 1. 环境准备
确保您的环境中已安装 **Python 3.8 及以上版本（亲测完美兼容最新的 Python 3.12 / 3.14）**，并且宿主机已开启本地代理软件（如 Clash / v2rayN）。

### 2. 克隆项目
```bash
git clone https://github.com/TheIanLi/LLM-Net-Probe.git
cd LLM-Net-Probe
```

### 3. 配置网络环境 (WSL2 代理穿透)

> [!IMPORTANT]
> **架构师提示：针对 WSL2 用户的网络配置区分**
> - **若启用 Win11 镜像网络 (`networkingMode=mirrored`)**：WSL 与宿主机共享 Localhost，直接使用 `127.0.0.1` 即可。
> - **若使用默认 NAT 模式**：由于隔离特性，请**勿**直接使用 `127.0.0.1`。请使用以下命令动态注入：

针对 **NAT 模式**，请在终端执行以下命令，动态获取宿主机真实 IP 并注入代理（此处以 Clash Verge 默认的 7897 端口为例，若使用传统 Clash 请改为 7890，v2rayN 请改为 10808）：
```bash
# 获取 WSL2 的宿主机真实网关 IP
export HOST_IP=$(ip route | grep default | awk '{print $3}')

# 注入全局代理变量
export HTTP_PROXY="http://$HOST_IP:7897"
export HTTPS_PROXY="http://$HOST_IP:7897"
```

### 4. 配置 API 鉴权 (安全注入)
基于 DevOps 安全规范，本项目严格禁止在代码或终端明文硬编码 API 密钥（会被记录至 `.bash_history` 导致泄露风险）。请通过 `.env` 环境变量文件安全注入您的凭证：
```bash
# 创建并编辑 .env 文件
# 在文件中写入：GROQ_API_KEY="gsk_在此处填入您的真实密钥"
nano .env
```

### 5. 启动验证
```bash
python3 probe.py
```
若网络链路与鉴权均无异常，系统将输出绿色 `[SUCCESS]` 连通提示与毫秒级的极速延迟响应。

---

## 💡 诊断与排错指南 (Troubleshooting)

在实际部署中，若遭遇错误响应，请依据本探针捕获的 HTTP 状态码进行定位：

- ⛔ **HTTP 403 (Forbidden)**
  - **现象：** 节点连接成功，但被 API 服务器拒绝。
  - **原因：** 当前代理 IP 命中了厂商风控（被拉黑），或 API Key 权限不足。
  - **对策：** 切换至更冷门的代理节点，或检查密钥账户状态。
- 🔍 **HTTP 404 (Not Found)**
  - **现象：** 鉴权通过，但找不到请求的资源。
  - **原因：** Model ID 拼写错误，或该模型已官方退役（如旧版 `llama3-8b-8192` 已被官方下架）。
  - **对策：** 查阅官方最新文档，更新目标模型标识符。
- 📡 **Ping 丢包假象**
  - **说明：** `ping` 基于 ICMP 协议，无法被 HTTP 代理接管。即使终端代理配置正确，ping 依然可能超时。验证代理连通性，请严格使用 `curl -I https://www.google.com`。

---

## 📄 开源协议 (License)
本项目基于 [MIT License](LICENSE) 许可，欢迎 Fork、修改与探讨。
