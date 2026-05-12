# 🤖 Hermes 微信 AI 助手

**5 分钟在微信部署你自己的 AI 助手**

> 扫码即用，P 图 / 查资料 / 写代码 / 定时早报，全在微信里搞定。

---

## 🚀 一键安装

```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USER/hermes-wechat-deploy/main/install.sh | bash
```

然后扫码，搞定。

---

## ✨ 功能

| 功能 | 描述 |
|------|------|
| 💬 AI 聊天 | DeepSeek 驱动，微信里自由对话 |
| 🎨 AI 修图 | 抠图、换背景、滤镜、拼图、加文字 |
| 📰 每日早报 | 早 8:45 自动推送 GitHub 热点 + 考公资讯 + 全球要闻 |
| 📝 对话归档 | 自动导出到 Obsidian，永久保存 |
| 🔒 安全隔离 | 每人独立 Bot + 独立 Profile，数据不串 |

---

## 📋 前置要求

- Linux 服务器（推荐 CentOS 7+ / Ubuntu 20.04+）
- Python 3.11+
- DeepSeek API Key（[免费注册](https://platform.deepseek.com)）
- 一个微信账号

---

## 🔧 手动安装

```bash
# 1. 克隆仓库
git clone https://github.com/YOUR_USER/hermes-wechat-deploy.git
cd hermes-wechat-deploy

# 2. 安装依赖
pip install hermes-agent Pillow qrcode

# 3. 运行安装
chmod +x install.sh
./install.sh

# 4. 或者手动分步
cp .env.example ~/.hermes/profiles/hermes/.env
# 编辑 .env 填入 DEEPSEEK_API_KEY
python3 onboard.py hermes
hermes gateway run --profile hermes &
```

---

## 📁 项目结构

```
hermes-wechat-deploy/
├── install.sh              # 一键安装脚本
├── onboard.py              # 微信扫码接入（零 token）
├── .env.example            # 配置模板
├── requirements.txt        # Python 依赖
├── skills/                 # 预装技能包
│   ├── photo-editor/       # AI 修图
│   ├── weixin-onboarding/  # 微信接入（给朋友用）
│   └── daily-digest/       # 每日早报
├── cron/                   # 定时任务脚本
│   └── obsidian-archive.py # 对话归档
└── README.md
```

---

## 🎨 技能详情

### AI 修图 (photo-editor)
微信里发图 + 一句话指令：
- "帮我把背景去掉" → AI 抠图
- "把背景换成蓝色" → 智能换背景
- "加文字'生日快乐'" → 文字叠加
- "三张图拼一起" → 自动拼图

### 微信接入 (weixin-onboarding)
帮朋友也接一个 AI 助手：
```bash
python3 onboard.py friend_name
```
生成二维码 → 朋友扫 → 自动配置完毕。

---

## ⏰ 定时任务

| 任务 | 时间 | 说明 |
|------|------|------|
| 对话归档 | 凌晨 2:00 | 导出到 Obsidian |
| 每日早报 | 早上 8:45 | GitHub 热点 + 考公 + 要闻 |

安装后自动创建，无需额外配置。

---

## 🔐 安全

- API Key 存在本地 `.env`，不上传
- 每人独立 Bot 账号，数据隔离
- 支持白名单 `WEIXIN_ALLOWED_USERS`

---

## ❓ 常见问题

**Q: 二维码过期了怎么办？**
A: 脚本会自动刷新，你等新二维码出来再扫就行。

**Q: 能给多人用吗？**
A: 每人需要一个独立 Bot。运行 `python3 onboard.py 朋友名` 给对方生成专属二维码。

**Q: 怎么停止？**
A: `pkill -f "hermes gateway"`

**Q: 支持其他模型吗？**
A: 支持。修改 `.env` 里的 `DEEPSEEK_API_KEY` 为 OpenAI / Anthropic 等。

---

## 📄 许可

MIT License

---

**Made with ❤️ by Hermes Agent**
