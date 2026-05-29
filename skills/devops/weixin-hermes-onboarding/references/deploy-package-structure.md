# Hermes WeChat Deploy — 分发包结构与变现

## 目录结构

```
hermes-wechat-deploy/
├── GUIDE.md                # 完整图文教程（阿里云→DeepSeek→微信）
├── install.sh              # 一键安装（6步全自动）
├── onboard.py              # 通用微信扫码接入（零token）
├── .env.example            # 配置模板（填 Key 即可）
├── requirements.txt        # Python 依赖
├── README.md               # 英文简洁说明
├── skills/                 # 79 技能包（全部）
│   ├── photo-editor/       # AI修图
│   ├── daily-digest/       # 每日早报
│   ├── weixin-hermes-onboarding/
│   └── ... (76 more)
└── cron/
    └── obsidian-archive.py # 对话归档
```

## 安装流程（用户视角）

1. 阿里云买 ECS（68元/月，包年包月）
2. 注册 DeepSeek，获取 API Key（充10元够用数月）
3. SSH 连服务器
4. 复制粘贴 `install.sh` 或跑 `curl | bash`
5. 微信扫码 → 确认 → 完成

## 变现渠道

| 渠道 | 卖什么 | 定价 |
|------|--------|------|
| 闲鱼 | 教程 + 一键脚本（ZIP） | 19.9 元/份 |
| 闲鱼 | 代部署服务（远程安装） | 199 元/次 |
| 闲鱼 | 月租 Bot（帮你维护） | 99 元/月 |
| 朋友圈 | 内测免费 → 收费 | 首月免费 |
| 淘宝 | 店铺挂链接 | 同闲鱼 |

## 交付物

给买家发：
- `hermes-wechat-deploy/` ZIP 包
- `GUIDE.md` 图文教程
- 微信技术支持（遇到问题截图发你）

买家只需自己买服务器（68元/月）+ DeepSeek Key（10元充值），其余一键搞定。

## 成本分析

| 买家成本 | 金额 | 周期 |
|----------|------|------|
| 阿里云 ECS 2核2G | 68 元 | 每月 |
| DeepSeek API | 1-5 元 | 每月 |
| **买家总月成本** | **≈73 元** | —|
| 卖家代部署 | 199 元 | 一次性 |
| 卖家月租维护 | 99 元 | 每月 |

相比 ChatGPT Plus（20 美元/月 = ~145 元），功能更多还便宜一半。
