#!/usr/bin/env python3
"""
每日对话归档 — 导出 Hermes 会话到 Obsidian Vault 为 Markdown。
零 token 消耗，纯脚本，配合 cronjob (no_agent=true) 使用。
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta

VAULT_PATH = os.environ.get(
    "OBSIDIAN_VAULT_PATH",
    os.path.expanduser("~/Documents/Obsidian Vault"),
)
ARCHIVE_DIR = os.path.join(VAULT_PATH, "hermes-archive")
HERMES_BIN = "hermes"


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def export_sessions():
    try:
        result = subprocess.run(
            [HERMES_BIN, "sessions", "export", "-"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            print(f"Export failed: {result.stderr}", file=sys.stderr)
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"Export error: {e}", file=sys.stderr)
        return None


def session_id_to_date(session_id):
    try:
        date_part = session_id.split("_")[0]
        return datetime.strptime(date_part, "%Y%m%d").date()
    except (ValueError, IndexError):
        return None


def convert_to_markdown(session_data):
    sid = session_data.get("session_id", "unknown")
    created = session_data.get("created_at", "")
    source = session_data.get("source", "unknown")
    title = session_data.get("title", sid)

    messages = session_data.get("messages", [])
    lines = [
        f"---",
        f"session_id: {sid}",
        f"created: {created}",
        f"source: {source}",
        f"tags: [hermes-archive]",
        f"---",
        "",
        f"# {title}",
        "",
        f"**Session:** `{sid}` | **Source:** {source} | **Created:** {created}",
        "",
        "---",
        "",
    ]

    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        if not content:
            continue

        role_emojis = {"user": "🧑 User", "assistant": "🤖 Hermes", "tool": "🔧 Tool"}
        lines.append(f"## {role_emojis.get(role, role)}")
        lines.append("")

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

        if session_date and session_date < yesterday:
            continue

        md_content = convert_to_markdown(session)
        filepath = os.path.join(ARCHIVE_DIR, f"{sid}.md")

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
