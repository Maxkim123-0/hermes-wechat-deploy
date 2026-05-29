---
name: obsidian
description: Read, search, create, and edit notes in the Obsidian vault. Includes Hermes session auto-archive.
platforms: [linux, macos, windows]
---

# Obsidian Vault

Use this skill for filesystem-first Obsidian vault work: reading notes, listing notes, searching note files, creating notes, appending content, and adding wikilinks.

## Vault path

Use a known or resolved vault path before calling file tools.

The documented vault-path convention is the `OBSIDIAN_VAULT_PATH` environment variable, for example from `~/.hermes/.env`. If it is unset, use `~/Documents/Obsidian Vault`.

File tools do not expand shell variables. Do not pass paths containing `$OBSIDIAN_VAULT_PATH` to `read_file`, `write_file`, `patch`, or `search_files`; resolve the vault path first and pass a concrete absolute path. Vault paths may contain spaces, which is another reason to prefer file tools over shell commands.

If the vault path is unknown, `terminal` is acceptable for resolving `OBSIDIAN_VAULT_PATH` or checking whether the fallback path exists. Once the path is known, switch back to file tools.

## Read a note

Use `read_file` with the resolved absolute path to the note. Prefer this over `cat` because it provides line numbers and pagination.

## List notes

Use `search_files` with `target: "files"` and the resolved vault path. Prefer this over `find` or `ls`.

- To list all markdown notes, use `pattern: "*.md"` under the vault path.
- To list a subfolder, search under that subfolder's absolute path.

## Search

Use `search_files` for both filename and content searches. Prefer this over `grep`, `find`, or `ls`.

- For filenames, use `search_files` with `target: "files"` and a filename `pattern`.
- For note contents, use `search_files` with `target: "content"`, the content regex as `pattern`, and `file_glob: "*.md"` when you want to restrict matches to markdown notes.

## Create a note

Use `write_file` with the resolved absolute path and the full markdown content. Prefer this over shell heredocs or `echo` because it avoids shell quoting issues and returns structured results.

## Append to a note

Prefer a native file-tool workflow when it is not awkward:

- Read the target note with `read_file`.
- Use `patch` for an anchored append when there is stable context, such as adding a section after an existing heading or appending before a known trailing block.
- Use `write_file` when rewriting the whole note is clearer than constructing a fragile patch.

For an anchored append with `patch`, replace the anchor with the anchor plus the new content.

For a simple append with no stable context, `terminal` is acceptable if it is the clearest safe option.

## Targeted edits

Use `patch` for focused note changes when the current content gives you stable context. Prefer this over shell text rewriting.

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content.

## Hermes Session Auto-Archive

To turn the Obsidian vault into a permanent memory for all Hermes conversations (zero token cost), set up a daily cron job that exports sessions as markdown.

### One-time Setup

1. **Create vault directory:**
   ```bash
   mkdir -p ~/Documents/Obsidian\ Vault/hermes-archive
   ```

2. **Set env var** in `~/.hermes/profiles/<profile>/.env`:
   ```
   OBSIDIAN_VAULT_PATH=/root/Documents/Obsidian Vault
   ```
   ⚠️ `.env` is protected — use `terminal` with append (`echo ... >> .env`), not `write_file`/`patch`.

3. **Deploy the archive script** → see `references/hermes-archive-script.md` for the full Python script.

4. **Create cron job** with `no_agent=true`:
   ```
   cronjob create:
     name: "每日 Obsidian 对话归档"
     schedule: "0 2 * * *"
     script: "hermes-obsidian-archive.py"
     no_agent: true
     deliver: origin
   ```

### How It Works

- Cron runs daily (2 AM by default), invokes the script directly — **no LLM, zero tokens**.
- Script calls `hermes sessions export -`, parses JSONL, writes one `.md` per session into `<vault>/hermes-archive/`.
- Only sessions from today/yesterday are archived (idempotent — won't duplicate).
- If no new sessions, script is silent (no delivery).
