# Cron Job Prompt Design — Lessons from the Daily Briefing Disaster

## The Failure Pattern

A cron job with **only `web` tools** and a vague prompt like "search for GitHub trending, 考公 news, and global news" will:

1. Call web_search a few times
2. Get poor/no results (especially from Chinese servers where many foreign APIs are blocked)
3. Silently produce **nothing** — the model says "let me search" and then stops

This is a silent failure. The job reports `status: ok` but delivers garbage.

## The Fix: Pre-Fetch Script + Agent Formatting

Split the work into two layers:

### Layer 1: Script fetches data (fast, reliable)
```python
# gh-trending.py — 2 seconds, real GitHub API data
# Output goes to stdout, gets injected into agent's context
```

Script runs first (`script` field on cron job). stdout becomes context for the agent.

### Layer 2: Agent formats + enriches
The agent gets:
- **Pre-fetched data** (injected from script stdout)
- **web + terminal toolsets** for supplementary searches
- A clear formatting template

The agent's job is now: pick the best items, format them, add a sentence of commentary. Not "find everything from scratch."

## Prompt Template

```
你是每日早报编辑。下面是你已经拿到的数据。请用中文写一份简洁早报：

### 板块一：[名称]
从下方数据中精选 N 条，每条：**项目名**：一句话 [→](链接)

### 板块二：[名称]
用 web_search 搜索今日值得关注的新闻，精选 3-5 条。搜不到就说「暂无」。

**规则：**
- 宁缺毋滥，没内容就空着，不要凑数
- 格式干净，不要废话
```

## Why This Works

| Before | After |
|--------|-------|
| Agent searches blind, finds nothing | Script fetches real data in 2s |
| Agent panics, returns empty | Agent has data to work with |
| Web-only tools | Web + terminal for curl fallback |
| Vague "search for news" | Specific "pick from this list" |

## Cost Note

The script runs as `no_agent=false` — it's a lightweight Python process, not an LLM call. The data it fetches costs zero tokens. Only the final formatting step uses the LLM.

## Testing Cron Jobs

Always test with `cronjob(action='run', job_id='...')` before trusting the schedule. A `status: ok` does NOT mean the output was useful.
