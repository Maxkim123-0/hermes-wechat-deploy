# Token-Cost-Conscious Cron Patterns

When setting up recurring tasks for cost-sensitive users, prefer these patterns
from cheapest to most expensive:

## Tier 0: Zero-Token Watchdog (`no_agent=true`)

For read-only or data-movement tasks that don't need reasoning, use
`no_agent=true` with a Python script. The script IS the job — no LLM
invocation at all, zero token cost.

```python
cronjob(
    action="create",
    name="daily archive",
    schedule="0 2 * * *",
    no_agent=True,
    script="my-script.py",
    deliver="origin"   # only delivers if stdout has content
)
```

The script runs in a fresh process with the same env vars as Hermes. 
If stdout is empty, nothing is delivered. If stdout has content, it's 
delivered as a message to the origin platform.

**Use cases:**
- Session exports to Obsidian/vault
- File cleanup
- Health checks
- Data syncing between services

**Script requirements:**
- Must be in `~/.hermes/profiles/<name>/scripts/`
- Must be executable Python
- Output goes to stdout (delivered) and stderr (logged)
- Use environment variables for paths, never hardcode `~/.hermes`

## Tier 1: Lightweight Agent (`enabled_toolsets` minimal)

When reasoning is needed but you want to minimize cost:

```python
cronjob(
    action="create",
    name="daily digest",
    schedule="45 8 * * *",
    enabled_toolsets=["web"],  # only grant what's needed
    prompt="...",
    deliver="origin"
)
```

**Cost savers:**
- Restrict `enabled_toolsets` to the minimum — fewer tools = smaller system prompt
- Use a cheap model override if available (`model="deepseek-chat"`)
- Keep the prompt focused and directive, not exploratory
- Use `deliver="origin"` to avoid multi-platform delivery overhead

## Tier 2: Full Agent (default)

Only when complex multi-step reasoning and tool orchestration is needed.

## Memory Cost Tradeoffs

When a user wants "permanent memory":

| Approach | Token Cost | Retrieval |
|----------|:---:|-----------|
| Aggressive memory (save everything) | 🔴 High | Automatic — but bloats every prompt |
| Selective memory (save important only) | 🟡 Low | Automatic — compact, relevant |
| Obsidian/vault archive (file export) | 🟢 Zero | Manual — `session_search` + file search |
| Session search (`session_search` tool) | 🟢 Per-query | On-demand — only costs when searching |

**Recommended stack for cost-sensitive users:**
1. Selective memory for preferences/corrections (auto-injected)
2. Obsidian vault for permanent conversation archive (zero prompt cost)
3. Daily cron-no_agent export job (zero token cost)
4. Session search for ad-hoc lookback (pay-per-query)

## Tsinghua Mirror for Chinese Servers

When `pip install` times out on pypi.org from a Chinese server:

```bash
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple <package>
```

Common packages that need this: `rembg`, `opencv-python-headless`, `numpy`, `scipy`.
Use `background=true` and `notify_on_complete=true` for long installs since
timeouts on the default 30s will kill the process before it finishes.
