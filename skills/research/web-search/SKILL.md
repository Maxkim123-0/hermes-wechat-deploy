---
name: web-search
description: 网页搜索——主用 Tavily，Bing HTML 解析仅作回退。用户已配置 Tavily key，明确要求「别用bing 以后都用tavily」。
triggers:
  - "搜索"
  - "查一下"
  - "搜一下"
  - "帮我找"
  - "网上有没有"
  - "web search"
version: 1.1.0
---

# Web Search — 网页搜索

**主搜索后端为 Tavily（已配 key，config.yaml `search_backend: tavily`）。Bing 仅作最终回退。**

---

## 使用方法

`web_search` 工具自动使用 `search_backend: tavily`，无需额外脚本。Bing HTML
脚本保留在 `/root/.hermes/profiles/xiaoxiaoxiong/scripts/web_search.py` 仅供回退。

---

## 回退机制

1. **Tavily**（主用，已配 key，config.yaml 设定）
2. **Bing HTML 解析**（Bing 中国版偶发搜索结果被劫持/返回无关内容，
   如搜「瑞幸咖啡」返回故宫文物。用户明确要求 **优先用 Tavily**，
   Bing 只在 Tavily 不可用时才尝试。）
3. 都失败 → 用 browser 手动搜国内可访问的站点（百度等），
   console 提取结果

**⛔ 不要多次尝试 Bing。** 用户已对搜索被劫持的问题表达不耐烦。
一次 Bing 失败后立即告知用户或换方案。

---

## 搜索后端对比

| | Tavily（主用） | Bing HTML |
|:--|:--|:--|
| 费用 | 免费1000次/月 | 免费 |
| 质量 | AI优化，准确 | 通用搜索，国内版偶发劫持 |
| 可用性 | 国内通（Tavily API 不翻墙） | 国内通 |
| 配置 | config.yaml `search_backend: tavily` | 脚本墙 |

**注意：** 用户已部署 Tavily key，日常搜索请勿主动切换回 Bing。`

---

## 脚本位置

`/root/.hermes/profiles/xiaoxiaoxiong/scripts/web_search.py`

## 网络限制

国内服务器外网受限。详细可达性矩阵见 `references/network-capabilities.md`。

**⛔ 铁律：已知被墙的站点，不要尝试通过 browser 访问。** 直接告诉用户原因并换方案。

## 被墙站点的处理协议

当需要从被墙站点获取内容时（大量工具调用在此浪费且用户会暴怒）：

0. **先快速判断**：X/Twitter、Google、YouTube、Reddit、Imgur、GitHub前端 → 已知被墙，**不要尝试**
1. **立即告知用户**：直接说"X 被墙了"（不要用"网络连接超时""CDP timeout""ERR_CONNECTION_TIMED_OUT"等黑话）
2. **0.5 秒内决定换路线**：不要顺序尝试 5 种代理（nitter → vxtwitter → fxtwitter → reddit → 重试）——这是用户最烦的行为
3. **可选替代方案**（优先级从高到低）：
   - `web_search`（Tavily）搜文章/第三方截图（Yahoo新闻、Reddit搬运）
   - 百度图片搜截图（`image.baidu.com`）
   - Instagram（国内偶尔通，不一定）
   - 直接认怂："这个我确实拿不到"（比硬撑好）

### 关键沟通原则

- 被墙了就直说"被墙了"，**不要用技术黑话**
- 技术上一个需要实物图/截图的请求拿不到 → 直接讲清楚原因 + 给替代方案
- **⚠️ 绝不能误导用户**：AI模型代理（OpenRouter）≠ 网络代理（VPN）。
  OpenRouter 只解决「模型被墙」（DeepSeek 连不上时自动切 OR 继续聊天），
  **不能**让浏览器访问被墙网站。向用户解释时必须分清这两个概念。
  写/说的时候不要用「等于给 XX 套了个 VPN」这种比喻——用户会当真去充钱，
  然后发现网站还是打不开，这是信任损失。
