# 老婆定时提醒 Cron 模式

## 使用场景
给老婆/家人设置每天定时消息提醒（饭点、吃药、上下班等），支持做一休一等排班判断。

## 架构

```
cron job (no_agent=true)
  → shell 包装脚本 (.sh)
    → Python 判断脚本 (laopo_reminder.py)
      → 输出消息文本 (stdout)
        → deliver 到 weixin:user_id
```

## 文件清单

| 文件 | 作用 |
|------|------|
| `scripts/laopo_reminder.py` | 核心逻辑：做一休一判断、消息模板 |
| `scripts/laopo_breakfast.sh` | 早饭包装脚本 |
| `scripts/laopo_lunch.sh` | 午饭包装脚本 |
| `scripts/laopo_dinner.sh` | 晚饭包装脚本 |
| `scripts/laopo_waimai.sh` | 外卖提醒脚本（发给用户） |

## Cron 配置

```bash
# 早饭 7:30 → 老婆
cronjob create name="老婆早饭提醒" schedule="30 7 * * *" script="laopo_breakfast.sh" \
  deliver="weixin:o9cq80xLB_74e_zHR6fJCVW-gOow@im.wechat" no_agent=true

# 午饭 12:00 → 老婆
cronjob create name="老婆午饭提醒" schedule="0 12 * * *" script="laopo_lunch.sh" \
  deliver="weixin:o9cq80xLB_74e_zHR6fJCVW-gOow@im.wechat" no_agent=true

# 晚饭 18:30 → 老婆
cronjob create name="老婆晚饭提醒" schedule="30 18 * * *" script="laopo_dinner.sh" \
  deliver="weixin:o9cq80xLB_74e_zHR6fJCVW-gOow@im.wechat" no_agent=true

# 外卖 13:00 → 用户
cronjob create name="老婆外卖提醒" schedule="0 13 * * *" script="laopo_waimai.sh" \
  deliver="origin" no_agent=true
```

## 做一休一判断逻辑

```python
from datetime import date
BASE = date(2026, 5, 14)  # 基准：上班
is_workday = (date.today() - BASE).days % 2 == 0
```

## Gateway Session 问题

iLink gateway 重启后 session 会断，老婆必须先发消息激活。
**解法：** 早安消息末尾加互动引导（「回我个表情～」），让她每天回复保持 session 活着。

## 暂停/恢复模式

```bash
# 批量暂停
cronjob action=pause job_id=xxx

# 定时恢复（创建一次性 cron）
cronjob create schedule="2026-05-16T07:25:00+08:00" repeat="once" \
  prompt="恢复以下cron job: xxx, yyy, zzz"
```

## 老婆信息

- 用户ID: o9cq80xLB_74e_zHR6fJCVW-gOow@im.wechat
- 地铁: 4号线
- 排班: 做一休一，基准 2026-05-14 上班
- 鱼油+维生素每天提醒
- 少吃笋
