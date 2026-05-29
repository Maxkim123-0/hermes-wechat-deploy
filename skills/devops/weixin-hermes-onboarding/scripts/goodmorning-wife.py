#!/usr/bin/env python3
"""
每日早安 — 通过 iLink API 给老婆发早安消息。
作为 cron watchdog 脚本运行 (no_agent=true)，零 token 消耗。

⚠️ 安全规则：
  1. 默认应 PAUSE 状态，用户确认内容后再 resume
  2. 测试时先改 target 为用户本人，确认无误再切换到老婆
  3. 不在深夜/凌晨发送
  4. 每次修改内容后先发给用户审阅
"""
import json, requests, uuid, secrets, base64, struct, os, random

# ── Config ──
BOT_JSON = os.path.expanduser("~/.hermes/profiles/xiaoxiaoxiong/home/.hermes/weixin/accounts/2b53f435e794@im.bot.json")
CTX_JSON = os.path.expanduser("~/.hermes/profiles/laopo/weixin/accounts/2b53f435e794@im.bot.context-tokens.json")
BASE_URL = "https://ilinkai.weixin.qq.com"

MESSAGES = [
    "🌞 早安呀～今天的阳光和你都很甜。记得吃早餐哦！❤️",
    "☀️ 新的一天开始啦！无论今天要做什么，都加油呀～你是最棒的！💪❤️",
    "🌸 早安！希望你今天遇到的都是好事，想到的都是开心的事。么么哒～😘",
    "✨ 早上好！偷偷告诉你一个秘密：今天的你会很幸运哦～🍀❤️",
    "🌻 起床啦起床啦～世界在等你闪闪发光呢！早安宝贝～💕",
    "🦋 早安！生活就像一盒巧克力，今天这颗肯定是甜的～🍫❤️",
    "💫 每一个早晨都是新的开始。愿你今天眼里有光，心里有爱。早安～✨",
]

def send_message(text):
    with open(BOT_JSON) as f:
        creds = json.load(f)
    token = creds["token"]
    uid = creds["user_id"]

    context_token = ""
    if os.path.exists(CTX_JSON):
        with open(CTX_JSON) as f:
            ctx = json.load(f)
        context_token = ctx.get(uid, "")

    client_id = f"hermes-weixin-{uuid.uuid4().hex}"
    msg = {
        "from_user_id": "",
        "to_user_id": uid,
        "client_id": client_id,
        "message_type": 2,
        "message_state": 2,
        "item_list": [{"type": 1, "text_item": {"text": text}}],
    }
    if context_token:
        msg["context_token"] = context_token

    payload = {"msg": msg, "base_info": {"channel_version": "2.2.0"}}
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))

    uin_value = struct.unpack(">I", secrets.token_bytes(4))[0]
    x_wechat_uin = base64.b64encode(str(uin_value).encode("utf-8")).decode("ascii")

    headers = {
        "Content-Type": "application/json",
        "AuthorizationType": "ilink_bot_token",
        "Content-Length": str(len(body.encode("utf-8"))),
        "X-WECHAT-UIN": x_wechat_uin,
        "iLink-App-Id": "bot",
        "iLink-App-ClientVersion": "131584",
        "Authorization": f"Bearer {token}",
    }

    resp = requests.post(f"{BASE_URL}/ilink/bot/sendmessage", data=body, headers=headers, timeout=10)
    if resp.status_code == 200 and resp.text.strip() in ("", "{}"):
        print(f"✅ 早安已发送: {text[:30]}...")
    else:
        print(f"❌ 发送失败: {resp.status_code} {resp.text[:100]}")

if __name__ == "__main__":
    send_message(random.choice(MESSAGES))
