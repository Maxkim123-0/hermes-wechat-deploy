# Hermes Obsidian Archive Script

Copy this to `~/.hermes/profiles/<profile>/scripts/hermes-obsidian-archive.py`, then reference it in a `no_agent=true` cron job.

```python
#!/usr/bin/env python3
"""
Daily archive: exports recent Hermes sessions to Obsidian vault as markdown.
Zero token cost — runs as a cron watchdog script (no_agent=True).
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

# Config
VAULT_PATH = os.environ.get(
    "OBSIDIAN_VAULT_PATH",
    os.path.expanduser("~/Documents/Obsidian Vault")
)
ARCHIVE_DIR = os.path.join(VAULT_PATH, "hermes-archive")
HERMES_BIN = "hermes"

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def export_sessions():
    """Export all sessions as JSONL from stdout."""
    try:
        result = subprocess.run(
            [HERMES_BIN, "sessions", "export", "-"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            print(f"Export failed: {result.stderr}", file=sys.stderr)
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"Export error: {e}", file=sys.stderr)
        return None

def session_id_to_date(session_id):
    """Session IDs are typically like 20260512_183800_abc123 — extract date."""
    try:
        date_part = session_id.split("_")[0]
        return datetime.strptime(date_part, "%Y%m%d").date()
    except (ValueError, IndexError):
        return None

def convert_to_markdown(session_data):
    """Convert a session JSONL entry to Obsidian-compatible markdown."""
    sid = session_data.get("session_id", "unknown")
    created = session_data.get("created_at", "")
    source = session_data.get("source", "unknown")
    title = session_data.get("title", sid)
    
    # Messages
    messages = session_data.get("messages", [])
    
    lines = []
    lines.append("---")
    lines.append(f"session_id: {sid}")
    lines.append(f"created: {created}")
    lines.append(f"source: {source}")
    lines.append("tags: [hermes-archive]")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"**Session:** `{sid}` | **Source:** {source} | **Created:** {created}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        
        if not content:
            continue
        
        if role == "user":
            lines.append("## 🧑 User")
        elif role == "assistant":
            lines.append("## 🤖 Hermes")
        elif role == "tool":
            lines.append("## 🔧 Tool")
        else:
            lines.append(f"## {role}")
        
        lines.append("")
        # Truncate very long tool outputs
        if role == "tool" and len(content) > 2000:
            content = content[:2000] + "\n\n... (truncated)"
        lines.append(content)
        lines.append("")
        lines.append("---")
        lines.append("")
    
    return "\n".join(lines)

def main():
    ensure_dir(ARCHIVE_DIR)
    
    raw = export_sessions()
    if not raw:
        print("No sessions to export or export failed.")
        return 0
    
    count = 0
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    for line in raw.split("\n"):
        if not line.strip():
            continue
        try:
            session = json.loads(line)
        except json.JSONDecodeError:
            continue
        
        sid = session.get("session_id", "")
        session_date = session_id_to_date(sid)
        
        # Only archive yesterday and today's sessions
        if session_date and session_date < yesterday:
            continue
        
        md_content = convert_to_markdown(session)
        filename = f"{sid}.md"
        filepath = os.path.join(ARCHIVE_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        count += 1
    
    if count > 0:
        print(f"Archived {count} session(s) to {ARCHIVE_DIR}")
    else:
        print("No new sessions to archive.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## Key Design Decisions

- **`no_agent=true`** — script runs as pure watchdog, zero LLM tokens
- **Date filtering** — only archives yesterday and today's sessions, idempotent
- **Tool output truncation** — caps tool messages at 2000 chars to keep markdown readable
- **frontmatter** — each note has YAML frontmatter with `tags: [hermes-archive]` for Obsidian graph view
- **Silent on empty** — no stdout = no delivery to user, only notifies when sessions were archived
