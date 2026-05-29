#!/usr/bin/env python3
"""
跨 Profile / 跨 Gateway 发消息通用脚本。
适用于：用当前 Bot 给其他 Profile 的用户发消息（不需要对方 gateway 在线）。

Usage:
    python3 cross-profile-send.py <message_text>
    
Requires:
    - Bot JSON at: accounts/{bot_id}.json
    - Context token at: accounts/{bot_id}.context-tokens.json (optional)
    - Modify BOT_JSON, CTX_JSON, BASE_URL below for your setup
"""
import json, requests, uuid, secrets, base64, struct, os, sys

# ── Config (modify these) ──
BOT_JSON = os.path.expanduser("~/.hermes/profiles/xiaoxiaoxiong/home/.hermes/weixin/accounts/YOUR_BOT.json")
CTX_JSON = os.path.expanduser("~/.hermes/profiles/TARGET_PROFILE/weixin/accounts/YOUR_BOT.context-tokens.json")
BASE_URL = "https://ilinkai.weixin.qq.com"


def send_ilink_message(text: str) -> bool:
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
    x_wechat_uin = base64.b64encode(str(uin_value).encode()).decode()

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
    ok = resp.status_code == 200 and resp.text.strip() in ("", "{}")
    print(f"{'✅' if ok else '❌'} Status={resp.status_code} Body={resp.text[:100]}")
    return ok


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 cross-profile-send.py <message>")
        sys.exit(1)
    send_ilink_message(sys.argv[1])
