# File Recovery for Course Assignments

When user asks to retrieve a previously generated assignment file ("我作业呢", "把我XX作业发我", "之前的文件呢", "找不到文件", "作业不见了", "恢复作业"), follow this standardized search order. **Stop at the first success — do not continue digging if found.**

## Search Order (exactly 6 steps)

1. **Cache dir** — `~/.hermes/profiles/xiaoxiaoxiong/cache/` (most recent output)
2. **Git repo log** — `~/hermes-wechat-deploy/` — `git log --all --oneline -- '*keyword*'`
3. **Full disk sweep** — `find /root -maxdepth 5 -name "*keyword*" -type f 2>/dev/null`
4. **Obsidian vault** — `find ~/Documents/Obsidian* -name "*keyword*" -type f`
5. **Session history** — `session_search` tool for file names and context
6. **Git deleted-files log** — `git log --all --diff-filter=D -- '*keyword*'`

All 6 steps return nothing → file is gone. Tell user immediately, offer to regenerate. Do not keep digging.

## Performance Note

When user complains "为什么这么慢" during file search: it's usually NOT the model — it's too many sequential tool calls. Check your own tool call count; if >3 sequential searches, you're the bottleneck. Verify model config once: `hermes config get model.default` (usually already correct). Only suggest model switching if config confirms a wrong model.

## Post-Generation Protection

After generating any assignment, save to git for durability:
```bash
mkdir -p ~/hermes-wechat-deploy/assignments/
cp <file> ~/hermes-wechat-deploy/assignments/
cd ~/hermes-wechat-deploy
git add assignments/ && git commit -m "archive: <name>" && git push
```

## Known Losses
- 2026-05-18: `气质与性格_网页版.html` (心理学) — unrecoverable from disk and git

## Related
- Main skill: `course-report-generation` — for regenerating lost assignments
- `powerpoint` skill — if the lost file was PPTX format
