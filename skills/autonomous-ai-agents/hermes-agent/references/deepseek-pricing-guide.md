# DeepSeek 模型选择 & 降本指南

> 实测数据 2026-05-14 | 用户：学生预算有限，月费控制在 ¥50 以内

## 模型对比（每百万 token，美元）

| 模型 | 输入 $/1M | 输出 $/1M | 月费估算(¥) | 适合场景 |
|------|----------|----------|-----------|---------|
| **V4 Flash** | $0.14 | $0.28 | ¥30-50 | ✅ 日常主力：聊天、搜索、简单任务 |
| **V4 Pro** | $0.30 | $0.50 | ¥70-100 | 复杂推理、长代码、论文 |
| **V3** | $0.27 | $0.27 | ¥50-70 | 通用，但 Flash 更便宜 |

## OpenRouter 中转（贵 45-74%，不推荐）

| 模型 | OpenRouter $/1M | 直连 $/1M | 溢价 |
|------|----------------|----------|------|
| V4 Pro | $0.435/$0.870 | $0.30/$0.50 | +45-74% |
| V4 Flash | $0.28 | $0.14 | +100% |

**结论：用 DeepSeek 模型时永远直连，不要走 OpenRouter。**

## 推荐策略

```
日常  → V4 Flash（¥30-50/月）
复杂  → 临时切 V4 Pro（`/model deepseek-v4-pro`）
兜底  → 智谱 GLM-5 免费额度（DeepSeek 被墙时自动切）
```

## 兜底配置（DeepSeek 挂了自动切智谱）

```bash
hermes config set model.fallback_providers "['zai']"
hermes config set model.fallback_model glm-5
```

## 其他省钱手段

- **压缩阈值调低**：`hermes config set compression.threshold 0.40`（默认 0.50）
- **视觉回退用免费模型**：智谱 GLM-4V-Flash（免费额度），别用 Claude 看小图
- **避免反复重试**：工具调用失败 2 次就换方案，不要同一种方式试第 3 次
- **长对话主动 `/compress`**：上下文越长越贵

## 余额检查

```bash
curl -s https://api.deepseek.com/user/balance \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY"
```

## 切换命令

```bash
# 切 Flash
hermes config set model.default deepseek-v4-flash
# 重启
hermes gateway restart
```
