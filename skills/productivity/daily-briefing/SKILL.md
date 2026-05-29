---
name: daily-briefing
description: Generate compelling daily briefing with GitHub trending + curated news — script-backed, model-curated.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [briefing, daily, cron, github, news]
---

# Daily Briefing

Generate a *compelling* daily briefing, delivered via WeChat. Not a stale auto-generated list — properly curated with personality.

## Philosophy

The user said the old briefing had "没有让人想看的欲望" (nothing makes you want to read it). The fix: **pre-fetch real data via script, let the model curate with voice.** Don't ask a blind model to search the web for news — it'll produce garbage or nothing.

## Architecture

```
Script pre-fetches data (fast, reliable)
    ↓
stdout injected as agent context
    ↓
Agent curates + formats + adds personality
    ↓
Delivered to WeChat
```

## Cron Job Setup

```bash
# The cron job runs gh-trending.py first, then the agent formats
hermes cron add \
  --name "每日精选早报 8:45" \
  --schedule "45 8 * * *" \
  --script gh-trending.py \
  --toolsets web,terminal \
  --deliver origin
```

### Script: `gh-trending.py`

Fetches repos created in last 3 days, sorted by stars, from GitHub API. Filters out game cheats/spam. Outputs formatted lines the agent can work with.

Location: `scripts/gh-trending.py` (in this skill's directory)

### Prompt template for the agent

```
你是每日早报编辑。下面是你已经拿到的 GitHub 热门项目数据。请用中文写一份简洁早报：

## ☕ 每日早报 {日期}

### 🔥 GitHub 热门
从数据中精选 5 个最有意思的项目，每条格式：
- **项目名**：一句话介绍 [→](链接)

### 📰 今日值得关注
用 web_search 搜索今日科技/互联网/中国新闻，3-5 条。搜不到就说「暂无」。

### 💡 今日一句
简短收尾（金句/冷笑话/冷知识）。

规则：宁缺毋滥，没内容就空着，不要凑数。格式干净。中文。
```

## Key Lessons

1. **Script-first, not web_search-first** — The model with only `web` tools will fail to produce real-time content. Scripts fetch data deterministically.
2. **Filter aggressively** — GitHub trending is full of game cheats and spam repos. Filter keywords: `cheat, aimbot, executor, esp, overlay, exploit, hack, bypass, spoofer, mod menu, crack, keygen`.
3. **Give it terminal tools** — The agent needs `terminal` + `web` toolsets. Terminal for curl fallback, web for supplementary search.
4. **Personality matters** — The curation voice makes the difference between "不想看" and "有意思". Short, punchy, opinionated.

## Pitfalls

- GitHub API rate limit: unauthenticated = 10 req/min. Caching recommended for production.
- HN is blocked from China servers — don't rely on it.
- gh-trending-api.herokuapp.com is slow/unreliable — use GitHub Search API directly.
- The agent will hallucinate if given no real data — always pre-fetch.
