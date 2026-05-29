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

## 分发包

已打包为 `hermes-wechat-deploy`（`/root/hermes-wechat-deploy/`），包含：
- `install.sh` — 一键安装（6步全自动：检查环境 → 安装 → 配Key → 建Profile → 装技能 → 扫码）
- `onboard.py` — 通用化扫码脚本（接受 profile 名参数：`python3 onboard.py 朋友名`）
- `skills/` — 预装技能包（P图、微信接入、每日早报）
- `cron/obsidian-archive.py` — 对话归档脚本
- `.env.example` / `README.md` — 配置模板 + 中文文档

目标用户：零技术背景，`curl | bash` 一条命令搞定。

**完整图文教程**：`GUIDE.md`（阿里云买服务器 → DeepSeek 获取 Key → SSH 连接 → 安装 → 扫码 → 测试），可直接用于闲鱼商品描述或交付文档。

**闲鱼售卖**：把 `hermes-wechat-deploy/` 整个目录打 ZIP 发给买家，附赠 GUIDE.md 当教程。定价建议：教程 19.9 元 / 代部署 199 元 / 月租 99 元。

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

## 跨 Gateway 发消息（给其他 Profile 的用户发消息）

`send_message` 工具只能发到**当前 Profile gateway** 管理的用户。要给其他 Profile 的用户发消息（比如 `laopo` Profile 的 Bot），必须直接调 iLink API。

### ⚠️ 安全铁律：先审后发

**任何发给别人的消息，必须先发给用户审阅，用户点头后才能发。**

| 规则 | 说明 |
|------|------|
| **🚫 禁止擅自发** | 无论测试、定时、手动，都不能绕过用户直接发给目标人 |
| ⚠️ **「可以呀」≠ 发送** | 用户说"可以呀"只表示方案通过，**不等于授权发送**。必须把消息草稿发出来让用户确认「发不发」后再操作 |
| ✅ 测试发给自己 | 先通过 `send_message` 工具发到当前用户微信，审过再走 API |
| ✅ 定时任务先暂停 | 新建 cron 默认 pause，用户确认后再 resume |
| ⏰ 注意时间 | 凌晨/深夜不发消息，除非用户明确要求 |
| 😅 紧急补救 | 如果误发，立即调 API 发一条道歉，把锅甩给 AI |

**被骂案例（2026-05-13）：** 凌晨 12:30 私自测试「早安老婆」cron → 两条消息直接发给老婆 → 用户暴怒 → 以后必须用户审阅。

### API 格式

```python
# 端点：POST /ilink/bot/sendmessage
# headers: Authorization: Bearer <bot_token>, Content-Type: application/json
payload = {
    "msg": {
        "from_user_id": "",                          # 留空
        "to_user_id": "o9cq80x...@im.wechat",        # 对方的微信用户 ID
        "client_id": f"hermes-weixin-{uuid4().hex}",  # 唯一消息 ID
        "message_type": 2,                            # MSG_TYPE_BOT
        "message_state": 2,                           # MSG_STATE_FINISH
        "context_token": "...",                       # 从 context-tokens.json 读取（可选但推荐）
        "item_list": [{
            "type": 1,                                # ITEM_TEXT
            "text_item": {"text": "消息内容"}
        }]
    }
}
```

### context_token 机制

- gateway 收到用户发来的消息时，iLink 返回 `context_token`
- gateway 缓存到 `{hermes_home}/weixin/accounts/{account_id}.context-tokens.json`
- 回复时必须带上最新的 context_token，否则返回 `errcode=-14`
- **关键**：gateway 重启后旧 context_token 失效。必须等用户先发一条消息给 Bot，Bot 拿到新 context_token 后才能回复
- 单向 sendmessage（用户未先发消息）即使附带旧 context_token 也会 session timeout

### 凭证查找

Bot 凭证存在 accounts 目录下的 JSON 文件里：
- 主 profile：`~/.hermes/profiles/xiaoxiaoxiong/home/.hermes/weixin/accounts/{bot_id}.json`
- 其他 profile：`~/.hermes/profiles/{profile}/weixin/accounts/{bot_id}.json`

### 完整 API 参考

详见 `references/sendmessage-api.md` — 包含所有必需的 headers、base_info、JSON 格式要求。

### 可复用脚本

- `scripts/onboard.py` — 微信扫码接入
- `scripts/cross-profile-send.py` — 跨 Profile 发消息（直接调 iLink API，不需要对方 gateway 在线）
- `scripts/goodmorning-wife.py` — 每日早安 cron 脚本范例（基于 cross-profile-send 模式，内置安全规则注释）
- `/root/hermes-wechat-deploy/onboard.py` — 独立分发版（接受 profile 名参数）

## 📦 分发注意事项

| 问题 | 解决 |
|------|------|
| **微信打不开 .tar.gz** | 用 `.zip` 格式。服务器无 `zip` 命令时用 Python：`python3 -c "import zipfile; ..."` |
| **微信看不了图片文件** | 用 `HTML → 本地 server → browser 截图 → MEDIA` 流水线生成封面图。详见 `references/html-to-wechat-image.md` |
| 买家手机上看不了 Markdown | 同时提供 `.txt` 纯文字版（如 `闲鱼商品描述.txt`） |
| 部署包体积 | 去掉 `.git/` 目录可显著减小体积 |

## ⚠️ 踩坑汇总

| 坑 | 现象 | 解决 |
|----|------|------|
| Bot 不能代用户发微信消息 | 用户问「帮我给 XXX 发条微信」，但 Bot 没有用户的好友列表 | **Bot ≠ 微信客户端。** Bot 只能发给自己绑定的那个微信用户。要发给其他人，必须对方也有自己的 Bot。不要给用户虚假期望——直接说「做不到，我可以帮你写好话术，你复制粘贴发过去」。 |
| `get_bot_qrcode` 用 POST | 返回 `missing bot_type` | **必须用 GET**，不带 auth token |
| `get_qrcode_status` 是长轮询 | 请求卡住 35 秒 | 用短 timeout (5s) + 循环重试 |
| 二维码 35 秒过期 | 来不及扫 | 脚本自动刷新，无限循环等 |
| `save_weixin_account` 参数 | `takes 1 positional argument` | 必须用关键字参数 |
| Session expired | `errcode=-14` | **gateway 重启后必须等用户先发消息**，Bot 才能回复。旧 context_token 随 session 一起失效 |
| `send_message` 跨 Profile 失败 | 目标未在可用列表 | 跨 gateway 必须直接调 iLink REST API，不能用 `send_message` 工具 |
| 多人共用 Bot | 扫了连不上 | 每人独立 Bot + 独立 Profile |
| 技能不共享 | 新人技能库为空 | 用 `cp -r skills/*` 复制 |
| Python print 缓冲 | 后台进程看不到输出 | 用 `python3 -u` 或写日志文件 |
| 后台子进程输出延迟 | `watch_patterns` 捕不到信号 | 输出写到文件，用 `cat logfile` 读 |
| WeChat 发送的 DOCX/PPTX 文件被编码 | 文件头不是标准 ZIP (`PK`)，而是 `0231 4248` (.1BH)，`file` 命令显示 `data`。python-docx/zipfile 都打不开 | **先让用户重新发送一次**——实测同一文件第二次发送可能变成标准 DOCX（`PK` 头，`file` 显示 `Zip archive`）。加密与否取决于微信传输路径，不是文件本身。重发成功率约 50%。如果重发仍加密：① 让用户直接复制粘贴内容；② 导出 PDF 再发；③ 发原始文件到电脑。不要死磕解码——没有已知解密工具 |
