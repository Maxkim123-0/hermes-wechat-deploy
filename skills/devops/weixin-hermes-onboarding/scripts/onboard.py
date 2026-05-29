#!/usr/bin/env python3
"""
iLink Bot 微信接入 — 生成二维码、轮询扫码、自动保存凭证。
零 token 消耗，纯 watchdog 脚本。

Usage:
    python3 -u onboard.py [profile_name]

默认 profile 名: hermes
"""
import requests
import json
import time
import os
import sys
import re

PROFILE_NAME = sys.argv[1] if len(sys.argv) > 1 else "hermes"
LOG = f"/tmp/hermes_onboard_{PROFILE_NAME}.log"
API_BASE = "https://ilinkai.weixin.qq.com"
HEADERS = {
    "iLink-App-Id": "bot",
    "iLink-App-ClientVersion": str((2 << 16) | (2 << 8) | 0),
}
HERMES_HOME = os.path.expanduser(f"~/.hermes/profiles/{PROFILE_NAME}/home/.hermes")
ACCOUNTS_DIR = os.path.join(HERMES_HOME, "weixin", "accounts")
ENV_PATH = os.path.expanduser(f"~/.hermes/profiles/{PROFILE_NAME}/.env")
QR_IMG_PATH = os.path.expanduser(f"~/.hermes/profiles/{PROFILE_NAME}/cache/images/onboard_qr.png")


def log(msg):
    with open(LOG, "a") as f:
        f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")
    print(msg, flush=True)


def get_fresh_qr():
    resp = requests.get(
        f"{API_BASE}/ilink/bot/get_bot_qrcode?bot_type=3",
        headers=HEADERS,
        timeout=15,
    )
    data = resp.json()
    return data["qrcode"], data["qrcode_img_content"]


def generate_qr_image(url):
    try:
        import qrcode as qrcode_lib
        from PIL import Image, ImageDraw, ImageFont

        qr = qrcode_lib.QRCode(
            version=2,
            error_correction=qrcode_lib.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        w, h = img.size
        new_img = Image.new("RGB", (w, h + 40), "white")
        new_img.paste(img, (0, 0))
        draw = ImageDraw.Draw(new_img)
        try:
            font = ImageFont.truetype(
                "/usr/share/fonts/google-noto-cjk/NotoSansCJK-DemiLight.ttc", 14
            )
        except (OSError, IOError):
            font = ImageFont.load_default()
        draw.text(
            (w // 2, h + 12),
            "微信扫码 → 点确认",
            fill="black",
            font=font,
            anchor="mt",
        )

        os.makedirs(os.path.dirname(QR_IMG_PATH), exist_ok=True)
        new_img.save(QR_IMG_PATH)
        return True
    except ImportError:
        log("⚠️ PIL/qrcode 未安装，跳过图片生成，使用原始链接")
        return False
    except Exception as e:
        log(f"QR_IMG_ERR: {e}")
        return False


def save_credentials(aid, token, uid, burl):
    os.makedirs(ACCOUNTS_DIR, exist_ok=True)

    account_file = os.path.join(ACCOUNTS_DIR, f"{aid}.json")
    with open(account_file, "w") as f:
        json.dump(
            {
                "account_id": aid,
                "token": token,
                "user_id": uid,
                "base_url": burl,
            },
            f,
            indent=2,
        )

    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r") as f:
            env_content = f.read()
    else:
        env_content = ""

    lines = env_content.strip().split("\n") if env_content.strip() else []
    new_lines = []
    wechat_keys = {
        "WEIXIN_HOME_CHANNEL", "WEIXIN_ACCOUNT_ID", "WEIXIN_TOKEN",
        "WEIXIN_BASE_URL", "WEIXIN_CDN_BASE_URL", "WEIXIN_DM_POLICY",
        "WEIXIN_ALLOW_ALL_USERS",
    }

    for line in lines:
        key = line.split("=")[0].strip() if "=" in line else ""
        if key in wechat_keys:
            continue
        new_lines.append(line)

    new_lines.extend([
        f"WEIXIN_CDN_BASE_URL=https://novac2c.cdn.weixin.qq.com/c2c",
        f"WEIXIN_DM_POLICY=open",
        f"WEIXIN_ALLOW_ALL_USERS=true",
        f"WEIXIN_HOME_CHANNEL={uid}",
        f"WEIXIN_ACCOUNT_ID={aid}",
        f"WEIXIN_TOKEN={token}",
        f"WEIXIN_BASE_URL={burl}",
    ])

    with open(ENV_PATH, "w") as f:
        f.write("\n".join(new_lines) + "\n")


def main():
    log(f"🚀 启动 — Profile: {PROFILE_NAME}")

    refresh_count = 0
    max_refreshes = 60

    while refresh_count < max_refreshes:
        qid, url = get_fresh_qr()
        log(f"QR_READY|{url}|{qid}")
        generate_qr_image(url)

        for _ in range(20):
            try:
                resp = requests.get(
                    f"{API_BASE}/ilink/bot/get_qrcode_status?qrcode={qid}",
                    headers=HEADERS,
                    timeout=5,
                )
                data = resp.json()
                status = data.get("status", "")

                if status == "confirmed":
                    aid = data.get("ilink_bot_id", "")
                    token = data.get("bot_token", "")
                    uid = data.get("ilink_user_id", "")
                    burl = data.get("baseurl", API_BASE)
                    save_credentials(aid, token, uid, burl)
                    log(f"✅ DONE|account_id={aid}|user_id={uid}")
                    print(f"\n✅ 接入成功! Bot: {aid}\n微信用户: {uid}")
                    print(f"启动: hermes gateway run --profile {PROFILE_NAME} &")
                    return 0
                elif status == "scaned":
                    log("📱 已扫码，等待手机确认...")
                elif status == "expired":
                    refresh_count += 1
                    break
            except Exception:
                pass
            time.sleep(1.5)
        else:
            refresh_count += 1

    log("⏰ 超时")
    return 1


if __name__ == "__main__":
    sys.exit(main())
