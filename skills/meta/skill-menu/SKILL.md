---
name: skill-menu
description: 小熊自助技能面板——精简分类菜单，自己挑技能，Hermes补充说明后确认执行
version: 1.1.0
trigger: "用户说\"调技能\"\"/menu\"\"/skills\"\"技能菜单\"\"选项栏\""
---

## 工作流

当用户触发此技能时：

1. **展示菜单** — 输出下方精简菜单（只输出菜单，不加额外说明）
2. **用户选** — 用户发编号（如 `1-2` = 分类1的第2项）
3. **补充说明** — 我调出对应的 skill_view，看有没有pitfall/限制/注意事项，告诉小熊
4. **确认执行** — 问"要开搞吗？"，他确认后才执行

---

## 📋 小熊技能面板（精简版）

```
━━━ 小熊技能面板 ━━━
① 作业报告   ② 做图海报
③ PPT文档    ④ 网页设计
⑤ 开发GitHub ⑥ 学习工具
⑦ 微信相关   ⑧ 日常工具
━━━━━━━━━━━━━━━━━
发编号选分类，如"①"
```

### ① 作业报告
```
1-1 写作业/实验报告  → 格式完整的DOCX+HTML
1-2 写论文/文献      → arxiv搜论文+辅助写作
```
→ 加载：`course-report-generation` / `arxiv`

### ② 做图海报
```
2-1 信息图/海报      → 21种布局x21种风格
2-2 HTML设计图→4K    → 浏览器渲染高精度PNG
2-3 修图/抠图/滤镜   → 去背景、调色、拼图
2-4 架构图/流程图    → 暗色主题SVG图
2-5 手绘风图表       → Excalidraw手绘风
```
→ ⚠️ 注意：面部精修（瘦脸美白大眼）不是强项，会推荐专业App
→ 加载：`baoyu-infographic` / `html-to-4k-png` / `photo-editor` / `architecture-diagram` / `excalidraw`

### ③ PPT文档
```
3-1 做PPT/改PPT      → .pptx文件操作（内容/模板）
3-2 讲义/课堂汇报    → 带B站视频嵌入+交互网页
```
→ 加载：`powerpoint` / `course-report-generation`

### ④ 网页设计
```
4-1 设计网页/落地页   → 参考Stripe/Linear等54个设计系统
4-2 设计原型/展示     → 一次性的HTML交互页面
```
→ 加载：`claude-design` + `popular-web-designs` / ~

### ⑤ 开发GitHub
```
5-1 PR工作流         → 分支→提交→开PR→合入
5-2 Code Review      → 审代码、写inline评论
5-3 搜开源方案       → GitHub搜现成工具（任何开发任务第一步）
5-4 TDD开发          → 测试驱动开发
5-5 debug/调试       → 系统定位bug
5-6 写计划           → 拆任务、写实施方案
```
→ 加载：根据具体选 `github-pr-workflow` / `github-code-review` / `github-resource-discovery` / `test-driven-development` / `systematic-debugging` / `writing-plans`

### ⑥ 学习工具
```
6-1 搜网页/查资料     → Tavily智能搜索
6-2 视频转文字       → YouTube/B站字幕提取+摘要
6-3 OCR/文档提取     → PDF/扫描件转文字
6-4 智能摘要         → 网页/文档一键提炼重点
```
→ 加载：`web-search` / `youtube-content` / `ocr-and-documents` / `summarize-ai`

### ⑦ 微信相关
```
7-1 微信接入新用户    → Bot生成→扫码→配置gateway
7-2 元宝群操作       → @人、查信息
7-3 老婆相关         → 查状态、发消息、定时智聊
```
→ ⚠️ 老婆：绝对铁律，发消息必须先展示内容等用户明确说"发"
→ 加载：`weixin-hermes-onboarding` / `yuanbao`

### ⑧ 日常工具
```
8-1 每日早报         → GitHub trending+资讯汇总
8-2 闹钟/定时提醒    → 用cronjob设置
8-3 Obsidian笔记     → 读写查笔记
8-4 写歌/音乐        → Suno AI写词作曲
```
→ 加载：`daily-briefing` / 直接cronjob / `obsidian` / `songwriting-and-ai-music`

---

## 注意事项

- 菜单只包含高频技能，其他冷门技能直接说需求我帮你找
- 选完后我会先看skill内容，如果有坑/限制会提前说
- 你确认"搞"之后我才动手
- 如果直接说需求（不通过菜单），我按铁律自动走skills-router
- 模型锁定铁律见 `references/model-diagnostics.md`