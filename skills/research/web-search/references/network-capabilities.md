# 网络能力矩阵（阿里云上海服务器）

> 2026-05-15 实测。决定哪些搜索/数据获取方式可用。

## 模型 API 通路

| 服务 | 状态 | 备注 |
|------|------|------|
| DeepSeek 直连 | ✅ 通 | 主线模型 V4 Flash，余额约 ¥9.9 |
| OpenRouter (模型API) | ✅ 通 | 已充 $5，仅作 DeepSeek 被墙时的 fallback |
| 智谱 Z.AI (GLM) | ✅ 通 | 免费额度，vision/兜底用 |

**重要：OpenRouter 只解决模型 API 被墙（DeepSeek 连不上），
不能作为网络代理让浏览器访问被墙网站。**

## VPN/代理方案实测

| 方案 | 状态 | 备注 |
|------|------|------|
| Cloudflare WARP 手动隧道 | ❌ 不通 | WireGuard 握手成功但 0 B received。
                         阿里云内网深度封锁 WARP 数据流。 |
| Cloudflare WARP (wg-quick) | ❌ 导致断连 | wg-quick 会改 DNS 为 1.1.1.1，
                         导致模型 API 域名解析失败，网关断线。 |
| 机场/自建 VPS | ❓ 未测试 | 付费方案，¥15-30/月。

**结论：阿里云服务器无法通过免费方案翻墙。**
Cloudflare WARP 握手可通过但数据流被封锁。
不要在这台服务器上尝试 wg-quick（会改 DNS 导致网关断开）。

## 国内可访问网站

| 服务 | 状态 | 备注 |
|------|------|------|
| 百度图片 (`image.baidu.com`) | ✅ 通 | 搜截图首选 |
| 百度搜索 | ✅ 通 | 搜索可用但反爬严格 |
| B站 | ✅ 通 | 视频信息、字幕 |
| Yahoo (`yahoo.com`) | ✅ 通 | 支持 web_extract 解析文章 |
| Hermes 官网 (`hermes-agent.org`) | ✅ 通 | 正常加载 |
| GitHub API (`api.github.com`) | ✅ 通 | 搜仓库、读README |
| Bing (`www.bing.com`) | ✅ 通 | **用户明确要求不用 Bing，优先用 Tavily** |

## 被墙网站（不要尝试访问）

| 服务 | 状态 |
|------|------|
| X/Twitter (`x.com`) | ❌ 不通 |
| Google (`google.com`) | ❌ 不通 |
| YouTube (`youtube.com`) | ❌ 不通 |
| Reddit (`reddit.com`) | ❌ 不通 |
| GitHub 前端 (`github.com`) | ❌ 不通（但 API 可用） |
| raw.githubusercontent.com | ❌ 不通 |
| DuckDuckGo | ❌ 不通 |
| Imgur (`imgur.com`) | ❌ 不通 |
| Nitter (`nitter.net`) | ❌ 不通 |
| fxtwitter/vxtwitter | ❌ 不通 |
| Instagram | ❌ 不通（可能试时可通，不稳定） |
| Cloudflare 官网/API | ❌ 部分通 |

## 搜索引擎实际配置

| 引擎 | 状态 | 配置 |
|------|------|------|
| **Tavily**（主用） | ✅ 已配 key | `config.yaml: search_backend: tavily` |
| Bing HTML（回退） | ✅ 可用但用户要求优先不用 | 脚本 `/root/.hermes/profiles/.../scripts/web_search.py` |

**用户明确声明：「别用bing 以后都用tavily」。** 除非 Tavily 不可用，否则不要碰 Bing。

## pip 镜像

```bash
# 清华镜像（必需，直连超时）
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple <pkg>
```

## 浏览器工具策略

- Playwright headless 可打开国内网站
- 境外网站（Google/YouTube/Twitter）大概率超时，**不要尝试**
- Cloudflare Turnstile 无法绕过
- X/Twitter 之类已知被墙的站点，不要用 browser_navigate 试 5 次不同代理
