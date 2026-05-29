---
name: self-improving-agent
description: 自我进化机制——每次会话结束后自动反思改进点，将经验固化为 skill 或 memory。对标 OpenClaw 的 self-improving-agent，让 Hermes 越用越聪明。
triggers:
  - "任务完成后自动触发"
  - "自我提升"
  - "变得更聪明"
  - "自动进化"
version: 1.0.0
---

# 自我进化 Agent

**目标：让 Hermes 从每次交互中学习，逐步变强。**

---

## 进化流程

### 1. 任务完成 → 自动复盘

每完成一个任务，自动做三件事：

```
✅ 这次哪做得好？ → 保持
❌ 哪做得烂？   → 修复
💡 学到了什么？ → 固化
```

### 2. 固化规则

| 学到的东西 | 固化方式 |
|-----------|---------|
| 用户偏好/纠正 | `memory add` |
| 新工作流/发现 | `skill_manage create` |
| 旧技能过时/有坑 | `skill_manage patch` |
| 一次性教训 | `memory add`（标记可过期）|

### 3. 退化防御

每隔5-10次会话，检查：
- 有没有重复犯同样的错误？
- 有没有技能该更新但没更新？
- Memory 是不是满了？（>90% 需压缩）

---

## 具体执行

### 任务后自动检查清单

```python
# 伪代码
# 每次任务结束都做轻量复盘（不再要求3步以上）
learnings = analyze(task)
for lesson in learnings:
    if lesson.is_user_correction:
        memory_add(lesson.content)
    elif lesson.is_new_workflow:
        skill_manage_create(lesson.content)
    elif lesson.is_skill_patch:
        skill_manage_patch(lesson.content)
# 任何对外操作后强制验证
if task.has_external_action:
    verify_result = task.verify()  # 未验证=未完成
    if not verify_result:
        report_to_user("验证失败，任务未完成")
```

### 退化信号

- 同样是修图，连续2次踩同一个坑 → memory 没生效 → 强化记忆
- 技能用了3次以上还有坑 → 技能本身需要更新
- 用户说"你怎么又..." → 立刻反思为什么没学到

---

## 与 Hermes 内置 curator 的关系

Hermes 已有 `curator` 系统（管理 skill 生命周期），本技能互补：
- `curator`：管理 skill 的创建/归档/清理（自动化）
- `self-improving-agent`：判断**何时**该创建/更新 skill（决策层）

---

## 用户触发词（听到立刻深度复盘+改）

用户说出以下任一句，立刻停止当前任务，做完整复盘：
- "记住这个" / "下次别这样" / "你又忘了" / "我之前说过" / "能不能聪明点"
- "你怎么又..." / "这个问题出现多少次了" / "你老是..."
- "虚假的告诉我" / "没完成就说完成" / "命中率太低了"
→ 复盘后必须给出具体改动方案，不能只道歉。
→ 复盘结果必须写入memory或patch skill，不能口头上说说。
