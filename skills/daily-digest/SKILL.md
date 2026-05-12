---
name: daily-digest
description: "每日精选早报 — GitHub 热点、考公资讯、全球要闻，每个板块最多 10 条，宁缺毋滥。"
triggers:
  - 早报
  - 每日简报
  - 今天有什么新闻
  - daily digest
---

# 每日精选早报

每天早上 8:45 自动推送，三大板块：

1. **GitHub 热点** — Trending repos，最多 10 条
2. **考公资讯** — 公务员考试相关新闻，最多 10 条
3. **全球要闻** — 当日重要新闻，最多 10 条

**原则：宁缺毋滥，没有好内容就空着，不要凑数。**

## 安装定时任务

```bash
hermes cronjob create \
  --name "每日精选早报 8:45" \
  --schedule "45 8 * * *" \
  --prompt "你是每日早报编辑。请用中文编写一份精选早报，分三大板块，每板块最多 10 条，宁缺毋滥..." \
  --deliver origin \
  --toolsets web
```

## 格式示例

```
📰 每日早报 | 2026-05-13

## 🔥 GitHub 热点
1. [repo] 一句话概括 — github.com/xxx/yyy

## 📚 考公资讯
1. 一句话概括 — 来源链接

## 🌍 全球要闻
1. 一句话概括 — 来源链接
```
