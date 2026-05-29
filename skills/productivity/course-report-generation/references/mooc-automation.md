# MOOC 网课自动化刷课 — 完整指南

> 合并自 `mooc-automation` 技能 + `mooc-auto-study-tools.md` + 2026-05-14 会话记录
> 此文件是详细参考；SKILL.md 中的 "MOOC刷课工具" 节是快速入口

## 核心原则

**绝不自己造轮子。** 中国大学MOOC、智慧树、超星学习通都是热门平台，GitHub 上有大量成熟方案。自己手写 Playwright 脚本是最后的选择——平台的反爬（滑块验证码、行为检测）远比想象的复杂。

## 首次响应协议（收到刷课需求的第一反应）

**用户说"帮我刷课" → 永远不要走服务器端 Python 登录脚本路线。**

```
1. GitHub API 搜最新方案（2分钟封顶）
2. 首选：ocsjs 油猴脚本 → 引导用户在浏览器装 Tampermonkey + 安装
3. 备选：Console 注入脚本（16倍速+自动下一节）
4. 最后：Playwright 带 cookie 回放（需用户手动登录后导出 cookie）
5. 绝不：手写 Python 脚本硬刚滑块验证码登录页
```

**铁律：智慧树/中国大学MOOC的滑块验证码在设计上就需要真人浏览器交互。**
服务器端（无头浏览器/Python requests/curl）**全部必死**。不要尝试、不要轮换登录方式、不要浪费时间。每多一次失败尝试 = 多烧一轮 token = 用户暴怒。

搜索策略：
```bash
# GitHub REST API 可在国内服务器直接访问（前端被墙但 API 通）
curl -s "https://api.github.com/search/repositories?q=icourse163+mooc&sort=stars&per_page=10"
curl -s "https://api.github.com/search/repositories?q=zhihuishu&sort=stars&per_page=10"
curl -s "https://api.github.com/search/repositories?q=ocsjs&sort=stars"
```
Gitee 搜索结果少，直接用 GitHub API。

## 已知可用工具

| 平台 | 工具 | 方式 | ⭐ | 备注 |
|------|------|------|-----|------|
| 中国大学MOOC | ocsjs | 油猴脚本(浏览器) | 3008 | 首选，需装 Tampermonkey |
| 智慧树 | ocsjs | 油猴脚本(浏览器) | 3008 | 同上，支持多平台 |
| 智慧树 | fuckZHS | Python(requests) | 2014 | 服务器可跑，有滑块风险 |
| 智慧树 | Autovisor | Python(Playwright) | 771 | **仅Windows**，需GUI浏览器 |
| 中国大学MOOC | Moonyear817/MoocTools | Chrome扩展 | 1 | 小众 |
| 中国大学MOOC | Pu-NINE-9/MOOC-chrome-plugin | Chrome扩展 | 1 | 小众 |

## 工具详情

### ocsjs (推荐首选)
- 仓库: `github.com/ocsjs/ocsjs`
- 类型: 油猴脚本（通用，支持 icourse163 + 智慧树 + 超星学习通）
- 安装: Tampermonkey + https://scriptcat.org/script/install/367
- 特点: 用户浏览器侧运行，无需服务器，自动播放视频+答题

### fuckZHS（智慧树专用，服务器端）
- 仓库: `github.com/VermiIIi0n/fuckZHS`
- 类型: Python CLI，纯 HTTP 请求（无浏览器）
- 登录方式: 账号密码 / 二维码扫码 (`qrlogin: true`)
- 配置: `config.json` 中填用户名/密码
- 优点: 轻量，服务器可跑
- 缺点: 需要先解决滑块验证码拿到有效 session

### Autovisor（智慧树专用，仅Windows）
- 仓库: `github.com/CXRunfree/Autovisor`
- 类型: Python + Playwright 模拟浏览器
- 限制: **仅支持 Windows**（需要 GUI + X Server）

## 登录难点

### 智慧树滑块验证码（重点）

**登录页**: `https://passport.zhihuishu.com/login`

三种登录方式**全部弹出同一种滑块拼图验证码**：
- 手机号 + 密码 → 点登录 → 滑块
- 学号登录（学校名 → 学号 → 密码）→ 弹滑块
- 知到扫码 → 同样需要验证

**不要轮换登录方式尝试，全部一样。**

滑块在跨域 iframe 内：
- `browser_console` 无法访问（SecurityError: Blocked a frame with origin...）
- Playwright 可以访问跨域 iframe，但 headless 服务器无 X Server
- 直接 POST `/user/login` 返回 302（缺少滑块 token）

**解决方案**：
1. 用户手动登录一次 → 导出 cookies → 服务端用 cookies 继续自动化
2. 微信扫码登录 → 抓取登录后的 session
3. 直接给用户浏览器端油猴脚本方案（推荐，最省事）

### 中国大学MOOC 登录

**校园用户登录**：
- 学校选择器是 Ant Design Select（`#basic_schoolId`）
- 需先 click 打开下拉框，再搜索/选择学校
- 字段: 学校 → 身份(学生/老师 radio) → 学号(`#basic_number`) → 认证码(`#basic_authCode`，默认身份证后6位) → 手机号(`#basic_phone`) → 下一步

**爱课程登录**：
- 账号 + 密码
- 直接 POST 可能绕过验证码
- 两种方式都可能有验证码

### pip 安装（国内服务器）

```bash
# 清华镜像（必需，直连 PyPI 大概率超时）
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple playwright
playwright install chromium
```

## OCS 油猴脚本安装验证流程

**每一步确认后再发下一步，不要连续发送多条指令等用户反馈。**

1. 装 Tampermonkey（Chrome/Edge 扩展商店）→ 确认安装成功
2. 打开 https://scriptcat.org/script/install/367 → 点「安装」→ 确认 Tampermonkey 弹出安装页面
3. 登录目标平台（icourse163 用校园用户登录）→ 确认已登录
4. 打开课程页面 → **刷新页面（F5 或 location.reload()）** 后等 5 秒
5. 检查右下角是否出现 OCS 控制面板（有播放倍速、自动答题等选项）

**常见问题**：
- 脚本安装了但不激活 → 刷新页面，检查 Tampermonkey 图标是否显示脚本计数
- Tampermonkey 菜单里 OCS 前面绿灯不亮 → 点图标 → 管理面板 → 确认开关是开的
- 控制面板不出现 → Console 执行 `location.reload()` 强制刷新
- icourse163 课程页显示「课程详情」而非「学习页面」→ 课程已结束，选「立即自学」进入学习模式

## 控制台快速脚本

`scripts/console-auto-study.js` — 粘贴到浏览器 Console 即可，16倍速静音播放当前视频，自动切下一节。
适用：中国大学MOOC、智慧树等 HTML5 视频平台。

## 工作流决策树

```
收到刷课需求
  ↓
GitHub API 搜现成方案（5分钟内）
  ↓
有成熟工具？
  ├── YES → 首选 ocsjs 油猴脚本（最通用最成熟）
  │          → 引导用户浏览器端安装
  │          → 每步确认
  └── NO  → 评估是否值得自己写（大概率不值）
             → 告诉用户手动完成成本更低
```

## 预算意识（关键）

用户 DeepSeek 余额有限（通常 < 10 元），每轮对话都在耗 token：
- 搜索结果直接给结论，不过度分析
- 失败一次后立刻换方案，不重复相同操作
- 用户说「继续」= 立即执行，不是继续分析
- 浏览器 click/type/vision 轮次尽量精简，合并操作

## 反模式（禁止）

- ❌ 花超过 5 分钟手动写登录自动化 → 大概率撞滑块，浪费时间
- ❌ 反复用 browser_console 碎片化操作同一个页面 → 写完整 Playwright 脚本
- ❌ 分析工具超过 2 轮不执行 → 用户要的是结果，不是分析报告
- ❌ 用户说「继续」就继续分析 → 「继续」= 立刻部署执行
- ❌ 遇到滑块后换一种登录方式再试（手机号 → 学号 → 知到）→ 全都有滑块
- ❌ 用户明显不耐烦时还在分析选项 → 直接给结论和下一步行动

## 2026-05-14 会话踩坑记录

### Playwright 在无头服务器
- `headless=False` → 需要 X Server（`Missing X server or $DISPLAY`）
- `headless=True` → Chromium headless shell 有 EPIPE 稳定性问题
- 即使 Playwright 能跑，滑块验证码仍需图像识别 + 鼠标拖拽，不现实

### 智慧树移动端
- `https://onlineweb.zhihuishu.com/onlinestuh5/login` → 重定向到同样的 passport 登录页
- `https://studyh5.zhihuishu.com/login` → 500
- 移动端入口不绕过滑块

### GitHub 搜索结果
找到的关键工具（按 ⭐ 排序）：
- ocsjs/ocsjs (3008) — 油猴通用脚本
- VermiIIi0n/fuckZHS (2014) — 智慧树 Python
- Foair/course-crawler (809) — 课程下载
- CXRunfree/Autovisor (771) — 智慧树 Playwright
- PyJun/Mooc_Downloader (500) — 下载器
