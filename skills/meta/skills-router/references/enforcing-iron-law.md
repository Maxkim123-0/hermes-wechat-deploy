# 铁律执行检查清单

本文记录了用户要求强制执行的技能检索铁律及其配置方法。

## 铁律内容

收到用户任何任务后：
1. `skill_view(name='skills-router')` — 加载路由器
2. 扫描匹配技能 — 从映射表找最匹配的1-3个
3. `skill_view(name='匹配到的技能')` — 加载目标技能
4. 按技能执行 — 有现成skill直接用，没有则GitHub搜，再没有才自己写
5. 任务后复盘 — self-improving-agent自动反思

严禁：不查路由器直接干活、凭记忆猜技能、跳过前三步造轮子。

## 配置方法

将铁律写入 `SOUL.md` 最顶部（非仅memory），格式：

```
# ⚠️ 铁律（最高优先级，每次回复前强制执行）
```

然后重启gateway生效。如果 `hermes gateway restart` 超时，用 `systemctl restart hermes-gateway-<profile>`。

## 触发场景

当用户说"你为什么不查skill""你又跳步了""我让你做任务先搜索你记到哪里去了"——说明铁律配置不到位或SOUL.md未加载。立刻检查SOUL.md并重启gateway。
