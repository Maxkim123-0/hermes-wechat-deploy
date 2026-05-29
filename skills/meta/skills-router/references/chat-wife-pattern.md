# 定时聊天消息池模式（Chat-with-Pool Pattern）

用于「每N小时给某人发聊天消息」场景，支持根据用户反馈持续优化内容。

## 架构

```
no_agent=true cronjob
  → Python 脚本 (chat-wife.py / chat-xiaoxiong.py)
    → 消息池 (MESSAGES 列表)
    → 历史记录 (XXX-history.json) — 避免重复
    → print(msg) → cronjob deliver
```

## 核心文件

| 文件 | 说明 |
|------|------|
| `scripts/chat-wife.py` | 老婆聊天消息生成器，8-20点每2h |
| `scripts/chat-wife-history.json` | 发送历史（自动生成） |
| `scripts/chat-xiaoxiong.py` | 小熊定时问候，8-20点每2h |
| `scripts/chat-xiaoxiong-history.json` | 发送历史（自动生成） |

## 升级机制（关键）

消息池不应该是静态的。当用户反馈对方的回复后，执行：

1. **分析反馈** — 对方喜欢什么风格、不喜欢什么话题
2. **增删消息** — 加新消息到对应类别，删掉无效/惹人烦的
3. **调整策略** — 比如对方喜欢撒娇→多加温柔类；回避某个话题→删掉

示例消息池分类：
```python
MESSAGES = [
    # 日常关心
    "吃饭了吗～",
    "今天忙不忙呀",
    # 撒娇调情
    "想我没有～",
    "嘿嘿突然想你了",
    # 下班/回家
    "快下班了吧～等你回家",
    # 随缘
    "今天有什么开心的事吗",
]
```

## 适用场景

- 伴侣定时聊天（当前使用）
- 家人每日问候
- 朋友定期联络
- 客户/用户定期跟进（需定制内容）

## Cron 配置

```bash
# 老婆聊天（发送到老婆微信）
cronjob create name="老婆聊天" schedule="0 8,10,12,14,16,18,20 * * *" \
  script="chat-wife.py" no_agent=true \
  deliver="weixin:o9cq80xLB_74e_zHR6fJCVW-gOow@im.wechat"

# 小熊问候（发回当前对话）
cronjob create name="小熊定时问候" schedule="10 8,10,12,14,16,18,20 * * *" \
  script="chat-xiaoxiong.py" no_agent=true \
  deliver="origin"
```

## 注意事项

- 脚本中的消息池直接修改（更新后无需重启gateway）
- 历史文件自动保留最近100条
- cronjob schedule间隔灵活可调
- 给老婆发消息仍需遵守铁律：展示内容→用户确认→才发
