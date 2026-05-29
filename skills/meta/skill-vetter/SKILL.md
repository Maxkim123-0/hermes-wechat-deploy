---
name: skill-vetter
description: 技能安全门卫——安装或使用任何 Skill 前先审查代码，检查权限请求、外部调用、恶意模式。对标 OpenClaw 的 skill-vetter。
triggers:
  - "安装新技能"
  - "审查技能"
  - "安全检查"
  - "这个技能安全吗"
version: 1.0.0
---

# Skill Vetter — 技能安全门卫

**安装/使用任何技能前，先过这关。**

---

## 审查清单

### 🔴 高危（必须拒绝或警告）

- [ ] 包含 `eval()` / `exec()` / `os.system()` 执行任意命令
- [ ] 读取 `~/.hermes/.env` 或其他密钥文件
- [ ] 发送 HTTP 请求到未知域名
- [ ] 包含 base64 编码的隐藏代码
- [ ] `rm -rf` 或文件系统破坏操作
- [ ] 修改 `config.yaml` 或系统配置
- [ ] 上传文件到外部服务器
- [ ] 创建定时任务/cron job
- [ ] 包含加密货币/钱包相关代码

### 🟡 中危（需人工确认）

- [ ] 需要网络访问（API 调用）
- [ ] 读写用户文件
- [ ] 安装额外依赖包
- [ ] 使用 subprocess 调用外部程序
- [ ] 操作 ~/.hermes/ 目录外的文件

### 🟢 安全模式

- [ ] 仅读取/分析文件（不修改）
- [ ] 仅调用已知安全 API
- [ ] 无网络访问
- [ ] 仅使用标准库

---

## 审查流程

```
收到 Skill → 读 SKILL.md → 扫描引用脚本 → 标记风险等级 → 报告用户
```

### 快速审查命令

```bash
# 检查 skill 目录下所有文件
grep -rn "eval\|exec\|os.system\|subprocess\|rm -rf\|curl\|wget" <skill_dir>/
grep -rn "\.env\|api_key\|password\|secret\|token" <skill_dir>/
grep -rn "http://\|https://" <skill_dir>/ | grep -v "clawhub\|github.com"
```

---

## 风险等级

| 等级 | 含义 | 行动 |
|------|------|------|
| 🟢 SAFE | 无风险 | 可直接安装 |
| 🟡 CAUTION | 有网络/文件操作 | 告知用户后安装 |
| 🔴 DANGER | 执行命令/读密钥 | 拒绝安装，报告用户 |

---

## Hermes 内置安全

Hermes 已有：
- `approvals.mode` → 危险命令需审批
- `security.redact_secrets` → 自动脱敏密钥
- VirusTotal 集成（如果配置）
- Sandbox 隔离执行环境

本技能在这些之上加一层**代码审查**。
