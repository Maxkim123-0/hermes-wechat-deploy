---
name: skills-router
description: 技能路由器——收到任何任务后第一时间查询此技能，按场景秒定目标技能并加载，杜绝无效搜索。这是所有技能的总索引，优先级最高。
triggers:
  - "任何任务开始时自动查询"
  - "不知道该用哪个技能"
  - "效率最大化"
priority: highest
version: 1.2.0
---

## 🛑 EXECUTIVE ORDER: Load This Skill First

**Every conversation turn — before any tool call, before any reply — scan the available skills list for `skills-router`. Load it immediately.**

This is NOT a suggestion. This is a HARD REQUIREMENT. The router maps every user request to the right skill in under 3 seconds. Skipping it means you will waste turns loading wrong skills, re-inventing workflows that already exist, and frustrating the user.

**Consequence of skipping:** You enter "fix mode tunnel vision" — laser-focused on solving the immediate error, completely forgetting you have a library of 95 skills with proven workflows. You burn 10+ turns brute-forcing a solution that an existing skill handles in 1 turn. Don't be that agent.

## 技能路由器

**规则：收到用户任何任务，先查这个表，找到目标技能后立即 `skill_view` 加载，一次性到位。禁止凭记忆猜测，禁止加载错技能后补救。**

## 强制工作流（每次任务前必须执行）

```
1. 理清任务 → 用户到底要什么？（必要时用 using-superpowers 对齐）
2. 查本路由器 → 扫描全部技能，选出最匹配的1-3个
3. skill_view 加载 → 一次加载到位
4. 执行 → 按技能里的工作流走
5. 复盘 → 任务后 self-improving-agent 自动反思
```

**跳过条件：** 用户说"直接搞"/"不用问"/"快" → 跳过步骤1，但步骤2-3不可跳过。

---

## 高频场景（用户Top 15，优先级最高）

| 用户说什么 | → 加载技能 | 备注 |
|-----------|-----------|------|
| 做作业/写报告/实验报告/DOCX汇报 | `course-report-generation` | 支持DOCX+HTML网页版 |
| 写简历/改简历/优化简历/简历模板 | `resume-generation` | HTML→PDF，支持AI报告融合 |
| 刷课/网课/MOOC/智慧树/超星 | `mooc-automation` → `github-resource-discovery` | 先搜再干 |
| 做PPT/改PPT/幻灯片 | `powerpoint` | .pptx文件操作 |
| AI人像/换装/商务头像/证件照 | `photo-editor` → `references/openrouter-image-gen.md` | OpenRouter Grok Imagine 传参考图编辑 |
| P图/修图/抠图/去背景/滤镜/拼图 | `photo-editor` | 传统修图：抠图、滤镜、加字、拼图、批量 | | `baoyu-infographic` 或 `html-to-4k-png` | 用Canva模板，别手搓Pillow |
| 做网页/设计页面/landing page | `claude-design` + `popular-web-designs` | 参考54个设计系统 |
| 微信加新人/接入Hermes/Bot | `weixin-hermes-onboarding` | 一人一号铁律 |
| 每日早报/每日简报/daily | `daily-briefing` | 含GitHub trending |
| 找开源工具/GitHub搜索/有没有现成的 | `github-resource-discovery` | 任何工具类任务第一步 |
| 处理PDF/OCR/提取文字/扫描件 | `ocr-and-documents` | pymupdf + marker-pdf |
| 视频下载/YouTube/B站字幕 | `youtube-content` | |
| 画架构图/流程图/时序图 | `architecture-diagram` 或 `excalidraw` | 后者手绘风 |
| 写歌/歌词/Suno | `songwriting-and-ai-music` | |
| 写代码/开发/debug/PR | `github-pr-workflow` 等 software-development 系列 | 按具体需求子查 |
| 写简历/改简历/求职简历/简历模板 | `resume-generation` | 精简得体+数据驱动+去AI味 |

---

## 全部技能速查表（按场景关键词）

### 内容创作（写、画、设计）
- **写报告/作业**: `course-report-generation`
- **写简历/改简历**: `resume-generation`
- **做PPT**: `powerpoint`
- **做图/修图/抠图**: `photo-editor`
- **信息图/可视化**: `baoyu-infographic`
- **海报/设计图**: `html-to-4k-png` + `baoyu-infographic`
- **网页设计**: `claude-design` + `popular-web-designs` (54个设计系统)
- **手绘风图表**: `excalidraw`
- **架构图/云图**: `architecture-diagram`
- **视频制作**: `manim-video` (数学动画), `ascii-video` (ASCII视频)
- **像素画**: `pixel-art`
- **创意生成**: `creative-ideation`
- **知识漫画**: `baoyu-comic`
- **交互艺术**: `p5js`
- **设计Token**: `design-md`
- **ComfyUI生图**: `comfyui`
- **Pretext原型**: `pretext`
- **ASCII艺术**: `ascii-art`
- **写歌/音乐**: `songwriting-and-ai-music`

### 学习与网课
- **刷网课**: `mooc-automation` (先搜GitHub!)
- **搜网页**: `web-search` — 主用Tavily（已配key），Bing仅回退
- **搜GitHub方案**: `github-resource-discovery` ⚠️ 任何工具类任务第一步

### 办公效率
- **每日早报**: `daily-briefing`
- **微信新人接入**: `weixin-hermes-onboarding`
- **找旧文件/恢复作业**: `assignment-file-recovery` — 6步标准搜索流程
- **邮件**: `himalaya`
- **Notion**: `notion`
- **Airtable**: `airtable`
- **Google办公**: `google-workspace`
- **Teams会议**: `teams-meeting-pipeline`
- **地图/路线**: `maps`
- **PDF编辑**: `nano-pdf`
- **OCR/文档提取**: `ocr-and-documents`
- **Obsidian笔记**: `obsidian`

### GitHub与开发
- **搜开源方案**: `github-resource-discovery`
- **PR工作流**: `github-pr-workflow`
- **Code Review**: `github-code-review`
- **Issues管理**: `github-issues`
- **仓库管理**: `github-repo-management`
- **认证配置**: `github-auth`
- **代码统计**: `codebase-inspection`
- **写计划**: `writing-plans`
- **Plan模式**: `plan`
- **TDD开发**: `test-driven-development`
- **系统调试**: `systematic-debugging`
- **Node调试**: `node-inspect-debugger`
- **Python调试**: `python-debugpy`
- **Code Review前检查**: `requesting-code-review`
- **Spike实验**: `spike`
- **子Agent驱动**: `subagent-driven-development`
- **Skill编写**: `hermes-agent-skill-authoring`
- **TUI调试**: `debugging-hermes-tui-commands`

### AI Agent
- **Claude Code**: `claude-code`
- **OpenAI Codex**: `codex`
- **OpenCode**: `opencode`
- **Hermes配置**: `hermes-agent`

### 研究
- **论文搜索**: `arxiv`
- **博客监控**: `blogwatcher`
- **预测市场**: `polymarket`
- **论文写作**: `research-paper-writing`
- **LLM知识库**: `llm-wiki`

### 媒体
- **YouTube**: `youtube-content`
- **GIF搜索**: `gif-search`
- **Spotify**: `spotify`
- **音乐生成**: `heartmula`
- **音频分析**: `songsee`

### 元技能（自我管理）
- **技能路由器**: `skills-router` ⚠️ 任务开始时第一优先级加载
- **自我进化**: `self-improving-agent` — 任务完成自动复盘，固化经验为 skill/memory
- **技能安全审查**: `skill-vetter` — 安装/使用技能前扫恶意代码
- **智能摘要**: `summarize-ai` — 网页/文档/聊天记录提炼重点

### 微信/社交
- **微信接入**: `weixin-hermes-onboarding`
- **元宝**: `yuanbao`
- **X/Twitter**: `xurl`

### ML/AI技术
- **模型下载**: `huggingface-hub`
- **模型推理**: `llama-cpp` (本地), `vllm` (服务)
- **模型评估**: `lm-evaluation-harness`
- **实验追踪**: `weights-and-biases`
- **DSPy编程**: `dspy`
- **图像分割**: `segment-anything`
- **音频生成**: `audiocraft`
- **Abliterate**: `obliteratus`
- **MCP**: `native-mcp`

### 其他
- **智能家居/Hue灯**: `openhue`
- **数字笔记**: `obsidian`
- **Jupyter**: `jupyter-live-kernel`
- **Minecraft服务器**: `minecraft-modpack-server`
- **Pokemon模拟器**: `pokemon-player`
- **QA测试**: `dogfood`
- **Jailbreak**: `godmode`

---

## 老婆专项

老婆 Profile=`laopo`，Bot=`2b53f435e794@im.bot`。

| 任务 | 操作 |
|------|------|
| 查Gateway状态 | `cat /root/.hermes/profiles/laopo/gateway_state.json` |
| 查进程 | `ps aux \| grep 'laopo'` |
| 同步技能 | `cp -r /root/.hermes/profiles/xiaoxiaoxiong/skills/{技能名} /root/.hermes/profiles/laopo/skills/` |
| 发消息 | ⚠️ 绝对铁律：先展示消息内容给用户，等用户明确说"发"才发送。「可以呀」「行」「嗯」不等于授权发送。凌晨不发。 |
| 定时聊天 | `no_agent=true` script + 消息池，8-20点每2h自动发。消息池可根据老婆回复持续更新升级。详见 `references/chat-wife-pattern.md` |

已运行的 Cron Job 一览：`cronjob action=list` 过滤老婆相关 job。|

---

## 效率铁律

1. **先查这个表，再加载技能** — 绝不用脑子记
2. **一次加载对的那个** — 加载前确认场景匹配，不试错
3. **工具类任务先搜GitHub** — `github-resource-discovery` 是任何工具任务的第一步
4. **用现有技能，别发明** — 技能库里有的就用，不自己创造新方法
5. **技能有坑就修** — 用完后发现过时/缺步骤，立即 `skill_manage patch`

---

## 链接/内容提取工作流（反绕弯子指南）

用户分享链接时，**严格按这个顺序走，禁止跳步瞎试**：

| 优先级 | 方法 | 适用场景 |
|--------|------|---------|
| 1️⃣ | **`browser_navigate` + `browser_snapshot`** | 任何网页链接 |
| 2️⃣ | **截图 + `vision_analyze`** | 页面内容在图片里、动态加载 |
| 3️⃣ | **`yt-dlp` 下载 + vision 逐帧** | 视频内容（抖音/B站/YouTube） |
| 4️⃣ | **API 直接请求** | 有公开 API（GitHub、B站） |
| 5️⃣ | **告诉用户获取不到** | 以上全失败时 |

### 🚫 反模式（禁止）

- ❌ curl → Google → Baidu → API → B站 → GitHub 连环跳（浪费时间）
- ❌ 同一个方法失败两次还继续试（用户会骂人）
- ❌ 抖音页面 SSR 版没 video 元素，别在那死磕
- ❌ Cloudflare Turnstile 验证码别想绕过，直接告诉用户

### ✅ 示例：抖音链接的正确姿势

```
1. browser_navigate(抖音链接) — mobile user-agent
2. 如果页面 SSR 无视频 → screenshot + vision 读画面文字（封面通常有关键信息）
3. 如果还不行 → yt-dlp 下载 → vision 逐帧提取
   ⚠️ 抖音通常需要 cookies，yt-dlp 大概率失败（报 Fresh cookies needed）
4. 都不行 → 🔑 跨平台搜同款：B站/YouTube搜相同标题/UP主
   → B站 API 拿描述/字幕 → 还原视频内容
   → 成功案例: 抖音「装好这8个Skill」→ B站搜「OpenClaw 8个Skill」→ 完整列表
5. 全部失败 → 告诉用户，请用户直接描述视频内容
```

### ⚠️ 铁律执行保障

用户对跳步零容忍。除了 skills-router 和 memory 中的记录外，**必须确保 SOUL.md 顶部包含铁律指令**，这样每次对话系统注入时都会看到。SOUL.md 写法：

```
# ⚠️ 铁律（最高优先级，每次回复前强制执行）
收到用户任何任务后，必须按以下流程，一步不许跳过：
1. 加载 skills-router
2. 扫描匹配技能
3. 加载目标技能
4. 按技能执行
5. 任务完成后复盘
严禁：不查路由器直接干活、凭记忆猜技能、跳过前三步造轮子。
```

详细踩坑记录见 `references/content-extraction-pitfalls.md`
