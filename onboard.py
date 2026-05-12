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

# ── Config ─────────────────────────────────────────────────
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
    """获取新二维码，返回 (qrcode_id, qrcode_url)"""
    resp = requests.get(
        f"{API_BASE}/ilink/bot/get_bot_qrcode?bot_type=3",
        headers=HEADERS,
        timeout=15,
    )
    data = resp.json()
    return data["qrcode"], data["qrcode_img_content"]


def generate_qr_image(url):
    """生成二维码 PNG 图片（含提示文字）"""
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

        # Add label below QR code
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
    """保存 Bot 凭证到 accounts/ 和 .env"""
    os.makedirs(ACCOUNTS_DIR, exist_ok=True)

    # Save account JSON
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

    # Update .env
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r") as f:
            env_content = f.read()
    else:
        env_content = ""

    # Add/update WeChat config lines
    lines = env_content.strip().split("\n") if env_content.strip() else []
    new_lines = []
    keys_seen = set()
    wechat_keys = {
        "WEIXIN_HOME_CHANNEL",
        "WEIXIN_ACCOUNT_ID",
        "WEIXIN_TOKEN",
        "WEIXIN_BASE_URL",
        "WEIXIN_CDN_BASE_URL",
        "WEIXIN_DM_POLICY",
        "WEIXIN_ALLOW_ALL_USERS",
    }

    for line in lines:
        key = line.split("=")[0].strip() if "=" in line else ""
        if key in wechat_keys:
            continue  # skip old weixin lines, will re-add
        new_lines.append(line)

    new_lines.extend(
        [
            f"WEIXIN_CDN_BASE_URL=https://novac2c.cdn.weixin.qq.com/c2c",
            f"WEIXIN_DM_POLICY=open",
            f"WEIXIN_ALLOW_ALL_USERS=true",
            f"WEIXIN_HOME_CHANNEL={uid}",
            f"WEIXIN_ACCOUNT_ID={aid}",
            f"WEIXIN_TOKEN={token}",
            f"WEIXIN_BASE_URL={burl}",
        ]
    )

    with open(ENV_PATH, "w") as f:
        f.write("\n".join(new_lines) + "\n")


# ── Main ───────────────────────────────────────────────────
def main():
    log(f"🚀 启动 — Profile: {PROFILE_NAME}")

    refresh_count = 0
    max_refreshes = 60  # 60 qr codes × 30s = 30 minutes

    while refresh_count < max_refreshes:
        # Get fresh QR
        qid, url = get_fresh_qr()
        log(f"QR_READY|{url}|{qid}")
        generate_qr_image(url)

        # Poll for scan
        for _ in range(20):  # ~30 seconds
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
                    log(f"📱 微信用户已绑定! Bot: {aid}")

                    print("\n" + "=" * 50)
                    print(f"  ✅ 接入成功！")
                    print(f"  Bot 账号: {aid}")
                    print(f"  微信用户: {uid}")
                    print(f"  二维码图片: {QR_IMG_PATH}")
                    print("=" * 50)
                    print()
                    print("  下一步: 启动 Gateway")
                    print(f"    hermes gateway run --profile {PROFILE_NAME} &")
                    return 0

                elif status == "scaned":
                    log("📱 已扫码，等待手机确认...")

                elif status == "expired":
                    refresh_count += 1
                    log("⏰ 二维码过期，自动刷新...")
                    break

            except Exception as e:
                pass

            time.sleep(1.5)
        else:
            # Inner loop exhausted without break (expired naturally)
            refresh_count += 1
            log("⏰ 二维码过期，自动刷新...")

    log("⏰ 超时 — 30 分钟未扫码")
    print("\n⚠️ 超时未扫码，请重新运行: python3 onboard.py")
    return 1


if __name__ == "__main__":
    sys.exit(main())
