# 🤖 微信 AI 助手 — 从零部署完全指南

> **看完这篇，你就能在微信里拥有一个会聊天、会 P 图、会写文章的 AI 助手。**
> 
> 全程 30 分钟，零代码基础可操作。图文详解每一步。

---

## 📋 目录

1. [这是什么](#1-这是什么)
2. [准备清单](#2-准备清单)
3. [第一步：买阿里云服务器](#3-第一步买阿里云服务器)
4. [第二步：获取 DeepSeek API Key](#4-第二步获取-deepseek-api-key)
5. [第三步：连接服务器](#5-第三步连接服务器)
6. [第四步：一键安装 Hermes](#6-第四步一键安装-hermes)
7. [第五步：微信扫码接入](#7-第五步微信扫码接入)
8. [第六步：启动并测试](#8-第六步启动并测试)
9. [第七步：安装定时任务（可选）](#9-第七步安装定时任务可选)
10. [你能做什么](#10-你能做什么)
11. [常见问题](#11-常见问题)

---

## 1. 这是什么

**一个跑在微信里的 AI 助手**，基于 DeepSeek 大模型，拥有 **89 种技能**：

| 类别 | 能力 |
|------|------|
| 💬 聊天 | 日常对话、答疑解惑、写作翻译 |
| 🎨 修图 | AI 抠图、换背景、滤镜、拼图、加文字 |
| 📰 资讯 | 每日自动推送热点新闻、考公资讯 |
| 📝 办公 | PPT 制作、PDF 编辑、文档提取 |
| 🎵 创作 | AI 写歌、ASCII 艺术、知识漫画 |
| 📊 数据 | 信息图、Excalidraw 手绘流程图 |
| 🔧 开发 | 代码审查、GitHub 管理（程序员专属） |

**微信里发消息就能用，不需要打开任何 App。**

---

## 2. 准备清单

| 东西 | 费用 | 说明 |
|------|------|------|
| 阿里云服务器 | **约 68 元/月**（包年包月） | 2核2G，够用了 |
| DeepSeek API Key | **充值 10 元够用几个月** | 按量付费，极便宜 |
| 微信账号 | 免费 | 你自己的微信 |
| 电脑（用于初始配置） | — | 只需用一次，之后全在手机上 |

**总启动成本：不到 80 元。**

---

## 3. 第一步：买阿里云服务器

### 3.1 注册阿里云

打开 [aliyun.com](https://www.aliyun.com)，用支付宝/淘宝账号登录。

### 3.2 选服务器

搜索「**云服务器 ECS**」→ 点「**立即购买**」。

**配置如下（关键，别选错）：**

| 选项 | 选什么 | 为什么 |
|------|--------|--------|
| 付费方式 | **包年包月** ⚠️ | 别选按量付费！按量会每天扣钱 |
| 地域 | **离你近的** | 比如上海、杭州 |
| 实例规格 | **2 vCPU / 2 GiB** | 最便宜的够用 |
| 镜像 | **Alibaba Cloud Linux 3** | 免费 |
| 系统盘 | **40 GB 高效云盘** | 默认即可 |
| 带宽 | **按流量计费** | 流量很少，便宜 |
| 登录凭证 | **自定义密码** | 设一个复杂的，记住 |

> ⚠️ **最重要：选「包年包月」，不要选「按量付费」！** 按量付费会每小时扣一次钱，一个月可能跑掉三四百。包年包月固定价格。

### 3.3 下单

- 时长选 **1 个月** 先试试，满意了再续
- 约 **68 元/月**
- 支付 → 等 2 分钟创建完成

### 3.4 拿到服务器 IP

创建完成后，进入 [ECS 控制台](https://ecs.console.aliyun.com)：

你会看到：

```
实例 ID: i-xxxxxxxxxxxx
公网 IP: 47.xxx.xxx.xxx    ← 记住这个！
状态: 运行中
```

**把公网 IP 记下来，后面要用。**

---

## 4. 第二步：获取 DeepSeek API Key

### 4.1 注册 DeepSeek

打开 [platform.deepseek.com](https://platform.deepseek.com)，用手机号注册。

### 4.2 充值（最少 10 元）

点「充值」→ 支付宝扫码 → 充 **10 元** 就够用几个月。

DeepSeek 非常便宜：
- 聊天 1000 条 ≈ 几分钱
- 一个月正常使用 ≈ 1-5 元

### 4.3 创建 API Key

左侧菜单 → 「**API Keys**」→ 「**创建新的 API Key**」

你会得到一个类似这样的字符串：

```
sk-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

**⚠️ 复制下来，只显示一次！存到备忘录里。** 这就是你 AI 助手的「钥匙」。

---

## 5. 第三步：连接服务器

### Windows 用户

1. 下载 [PuTTY](https://www.putty.org) 或 [Termius](https://termius.com)
2. 打开后输入：
   - Host: 你的公网 IP
   - Port: 22
   - Username: root
3. 输入你设的密码
4. 连上后看到 `[root@xxx ~]#` 就成功了

### Mac 用户

打开「终端」App（在启动台搜索 Terminal），输入：

```bash
ssh root@你的公网IP
```

输入密码（输入时不显示，正常现象），回车。

### 手机也能操作

下载 Termius App（iOS/Android 都有），同样输入 IP、用户名 root、密码。

---

## 6. 第四步：一键安装 Hermes

连接到服务器后，**复制粘贴**下面这行命令，回车：

```bash
curl -fsSL https://raw.githubusercontent.com/nousresearch/hermes-agent/main/scripts/install.sh | bash
```

> 如果上面命令报错，用备用方案：
> ```bash
> pip install hermes-agent
> ```

等待 2-3 分钟，看到 `✅ Hermes Agent installed` 即成功。

---

## 7. 第五步：微信扫码接入

这一步让 AI 助手「住进」你的微信。

### 7.1 创建配置文件

```bash
mkdir -p ~/.hermes/profiles/hermes
```

创建 `.env` 文件，**把 sk-xxx 换成你自己的 Key**：

```bash
cat > ~/.hermes/profiles/hermes/.env << 'EOF'
DEEPSEEK_API_KEY=sk-你的Key粘贴在这里

WEIXIN_CDN_BASE_URL=https://novac2c.cdn.weixin.qq.com/c2c
WEIXIN_DM_POLICY=open
WEIXIN_ALLOW_ALL_USERS=true
EOF
```

### 7.2 生成扫码二维码

```bash
python3 -u -c "
import requests, json, time, os

API='https://ilinkai.weixin.qq.com'
H={'iLink-App-Id':'bot','iLink-App-ClientVersion':'131584'}

r = requests.get(f'{API}/ilink/bot/get_bot_qrcode?bot_type=3', headers=H, timeout=15)
d = r.json()
qid, url = d['qrcode'], d['qrcode_img_content']
print(f'扫码链接: {url}')
print(f'二维码ID: {qid}')

# 轮询等待扫码
for i in range(40):
    r = requests.get(f'{API}/ilink/bot/get_qrcode_status?qrcode={qid}', headers=H, timeout=5)
    s = r.json().get('status','')
    if s == 'confirmed':
        d = r.json()
        aid = d['ilink_bot_id']
        token = d['bot_token']
        uid = d['ilink_user_id']
        burl = d.get('baseurl', API)
        
        # 保存凭证
        os.makedirs(os.path.expanduser('~/.hermes/profiles/hermes/home/.hermes/weixin/accounts'), exist_ok=True)
        with open(os.path.expanduser(f'~/.hermes/profiles/hermes/home/.hermes/weixin/accounts/{aid}.json'), 'w') as f:
            json.dump({'account_id':aid,'token':token,'user_id':uid,'base_url':burl}, f)
        
        env = open(os.path.expanduser('~/.hermes/profiles/hermes/.env')).read()
        env += f'\nWEIXIN_HOME_CHANNEL={uid}\nWEIXIN_ACCOUNT_ID={aid}\nWEIXIN_TOKEN={token}\nWEIXIN_BASE_URL={burl}\n'
        open(os.path.expanduser('~/.hermes/profiles/hermes/.env'), 'w').write(env)
        
        print(f'\n✅ 接入成功！Bot: {aid}')
        print(f'用户: {uid}')
        exit(0)
    elif s == 'scaned':
        print('📱 已扫码，请在手机上点确认...')
    elif s == 'expired':
        print('⏰ 过期，正在刷新...')
        r = requests.get(f'{API}/ilink/bot/get_bot_qrcode?bot_type=3', headers=H, timeout=15)
        d = r.json()
        qid, url = d['qrcode'], d['qrcode_img_content']
        print(f'新链接: {url}')
    time.sleep(1.5)
print('超时，请重新运行')
"
```

运行后屏幕上会出现一个 **扫码链接**，复制 → 微信打开 → 扫码 → 点「确认」。

看到 `✅ 接入成功！` 就完成了。

---

## 8. 第六步：启动并测试

### 8.1 启动微信网关

```bash
hermes gateway run --profile hermes &
```

看到 `gateway running` 即启动成功。

### 8.2 测试

拿起手机，在微信里给刚才扫的那个 Bot 发消息：

```
你好
```

**如果它回复了，恭喜！🎉 你的微信 AI 助手已经上线了。**

试试这些命令：
```
帮我查一下今天的天气
给我写一首诗
帮我抠图（然后发一张图片）
今天有什么新闻
```

---

## 9. 第七步：安装定时任务（可选）

### 9.1 每日早报（早上 8:45 推送）

```bash
hermes cronjob create \
  --name "每日早报" \
  --schedule "45 8 * * *" \
  --prompt "你是每日早报编辑。请用中文编写一份精选早报，分三块：🔥 GitHub热点、📚 考公资讯、🌍 全球要闻。每块最多10条，宁缺毋滥，简洁有力。" \
  --deliver origin \
  --toolsets web
```

### 9.2 对话自动归档

```bash
hermes cronjob create \
  --name "对话归档" \
  --schedule "0 2 * * *" \
  --script hermes-obsidian-archive.py \
  --no-agent
```

---

## 10. 你能做什么

部署完成后，你的微信 AI 助手拥有 **79 种技能**，以下是最常用的：

### 🎨 AI 修图
```
帮我把这张图背景去掉
把这张照片的背景换成蓝色
这三张图横向拼在一起
给这张图加滤镜
```

### ✍️ 写作创作
```
帮我写一封辞职信
写一篇关于AI的公众号文章
把这段文字改得更生动
写一首关于夏天的诗
```

### 📰 信息获取
```
今天有什么新闻
最近GitHub上有什么热门项目
帮我查一下比特币价格
搜索关于XXX的最新论文
```

### 📝 办公助手
```
帮我做一个PPT大纲
把这份PDF转成文字
帮我写一封商务邮件
做个会议纪要模板
```

### 🎵 娱乐
```
帮我写一首流行歌的歌词
生成一张知识漫画
画一幅ASCII艺术图
```

---

## 11. 常见问题

### Q: 会不会很贵？
**A:** 服务器 68 元/月 + DeepSeek API 约 1-5 元/月 = **每月不到 75 元**。比 ChatGPT Plus（20 美元/月）便宜，功能还多。

### Q: 需要一直开着电脑吗？
**A:** 不需要。服务器 24 小时运行，你手机微信上随时用。

### Q: 安全吗？我的聊天记录会泄露吗？
**A:** 服务器在你自己的阿里云账号下，API Key 只有你自己知道。数据不会传给第三方。

### Q: 能给别人用吗？
**A:** 可以！运行 `python3 onboard.py 朋友名` 生成二维码给朋友扫，每人独立使用，数据隔离。

### Q: 服务器关机了怎么办？
**A:** 登录阿里云控制台 → ECS → 找到实例 → 点「启动」。如果网关断了，SSH 上去重新跑 `hermes gateway run --profile hermes &`。

### Q: 二维码过期了怎么办？
**A:** 重新运行第五步的命令，生成新二维码。

### Q: 支持其他 AI 模型吗？
**A:** 支持。修改 `.env` 里的 `DEEPSEEK_API_KEY` 为 OpenAI Key 即可切换模型。

---

## 📦 附：完整技能清单

| # | 技能 | 用途 |
|---|------|------|
| 1 | **photo-editor** | AI 修图：抠图、滤镜、拼图、加文字 |
| 2 | **daily-digest** | 每日精选早报 |
| 3 | **youtube-content** | YouTube 视频转文字摘要 |
| 4 | **songwriting** | AI 写歌、作曲 |
| 5 | **baoyu-comic** | 知识漫画生成 |
| 6 | **baoyu-infographic** | 21×21 布局信息图 |
| 7 | **powerpoint** | PPT 制作与编辑 |
| 8 | **nano-pdf** | PDF 编辑 |
| 9 | **ocr-and-documents** | 文档 OCR 提取 |
| 10 | **humanizer** | 文字润色 |
| 11 | **gif-search** | GIF 搜索下载 |
| 12 | **ascii-art** | ASCII 艺术 |
| 13 | **pixel-art** | 像素画（NES/GameBoy 风格） |
| 14 | **spotify** | Spotify 音乐控制 |
| 15 | **maps** | 地图查询、路线规划 |
| 16 | **polymarket** | 预测市场查询 |
| 17 | **notion** | Notion 笔记管理 |
| 18 | **google-workspace** | Gmail/日历/文档 |
| 19 | **linear** | 项目管理 |
| 20 | **obsidian** | Obsidian 笔记 |
| 21 | **arxiv** | 学术论文搜索 |
| 22 | **llm-wiki** | LLM 知识库 |
| 23 | **blogwatcher** | 博客/RSS 监控 |
| ... | ... | 还有 57 种开发/运维/研究技能 |

**完整 79 种技能，一次部署全部拥有。**

---

> 📞 技术支持：遇到问题截图发我微信
> 
> 💡 提示：这份教程 + 部署包 = **你的闲鱼产品**。别人买的就是这份教程 + 一键脚本。

---

**© 2024 Hermes Agent. MIT License.**
