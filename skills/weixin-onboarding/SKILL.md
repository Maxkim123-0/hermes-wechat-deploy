---
name: weixin-hermes-onboarding
description: 微信接入 Hermes 新人全流程——生成Bot、扫码确认、自动保存、启动gateway。已实战验证。
triggers:
  - 添加微信新用户
  - 微信 bot 新人接入
  - 微信 onboarding
  - 帮别人接 Hermes
---

# 微信 Hermes 新人接入（实战版）

## 核心原理

- iLink Bot 一个号只能绑定一个微信用户
- 每人需要独立 Bot 账号 + 独立 Profile + 独立 Gateway
- `get_bot_qrcode` 用 GET（非 POST），无需 auth token
- `get_qrcode_status` 是长轮询（35秒超时），扫码后秒返回

## 完整步骤

> 📜 可复用脚本：`scripts/onboard.py`（改 `PROFILE_NAME` 后直接跑）

### 1. 创建新 profile

```bash
hermes profile create <用户名>
```

### 2. 复制基础配置

```bash
cp /root/.hermes/profiles/xiaoxiaoxiong/.env /root/.hermes/profiles/<用户名>/.env
cp -r /root/.hermes/profiles/xiaoxiaoxiong/skills/* /root/.hermes/profiles/<用户名>/skills/
```

### 3. 生成二维码并轮询确认（⚠️ 关键步骤）

不要用 `hermes gateway setup`，二维码 35 秒过期来不及。

**直接跑脚本：** `python3 -u scripts/onboard.py`（修改脚本内 `PROFILE_NAME` 变量为新 profile 名）。

脚本流程：GET 获取 QR → 生成 PNG → 轮询 `get_qrcode_status` → 确认后自动保存凭证到 `.env`。

### 4. 扫码确认

- 把 `/root/hermes/cache/images/onboard_qr.png` 发给对方
- 或者发原始链接（`/tmp/hermes_onboard.log` 里的 `QR_READY` 行）
- 对方微信扫码 → 点确认
- 脚本自动检测 `confirmed` → 保存凭证到 `.env`

### 5. 启动 gateway

```bash
hermes gateway run --profile <用户名> &
```

### 6. 验证

让新人微信发消息给 Bot，gateway 日志出现 `inbound from=xxx` 即成功。

## ⚠️ 踩坑汇总

| 坑 | 现象 | 解决 |
|----|------|------|
| `get_bot_qrcode` 用 POST | 返回 `missing bot_type` | **必须用 GET**，不带 auth token |
| `get_qrcode_status` 是长轮询 | 请求卡住 35 秒 | 用短 timeout (5s) + 循环重试 |
| 二维码 35 秒过期 | 来不及扫 | 脚本自动刷新，无限循环等 |
| `save_weixin_account` 参数 | `takes 1 positional argument` | 必须用关键字参数 |
| Session expired | `errcode=-14` | 重启 gateway 即可 |
| 多人共用 Bot | 扫了连不上 | 每人独立 Bot + 独立 Profile |
| 技能不共享 | 新人技能库为空 | 用 `cp -r skills/*` 复制 |
| Python print 缓冲 | 后台进程看不到输出 | 用 `python3 -u` 或写日志文件 |
| 后台子进程输出延迟 | `watch_patterns` 捕不到信号 | 输出写到文件，用 `cat logfile` 读 |
