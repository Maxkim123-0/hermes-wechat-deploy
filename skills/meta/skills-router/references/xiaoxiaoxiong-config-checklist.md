# 小熊 Hermes 配置优化记录

用户熊正阳（小熊），DeepSeek 预算有限。

## 七项优化（2026-05-15）

1. compression.threshold: 0.5 → **0.35**（更早压缩省 token）
2. tool_loop_guardrails.hard_stop_enabled: false → **true**（防死循环）
3. skills.guard_agent_created: false → **true**（防自动建冗余 skill）
4. display.show_cost: false → **true**（可见花费）
5. curator.interval_hours: 24 → **12h**（更快巡检）
6. curator.stale_after_days: 7 → **5d**（更快标记 stale）
7. curator.min_idle_hours: 3 → **2h**（更早观察闲置）

## SOUL.md

铁律写在了 SOUL.md 顶部，确保注入时立刻可见。

## 生图

服务器无 GPU（Cirrus Logic GD 5446），ComfyUI 无法跑。
OpenRouter 生图模型从国内被墙。目前无可用的生图后端。
