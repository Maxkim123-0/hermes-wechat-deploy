#!/usr/bin/env python3
"""
iLink Bot 新人接入脚本 — 生成二维码、轮询扫码、自动保存凭证。
修改 PROFILE_NAME 复用。

Usage:
    python3 -u scripts/onboard.py
"""
import requests, json, time, os, sys, re

LOG = "/tmp/hermes_onboard.log"
HEADERS = {'iLink-App-Id': 'bot', 'iLink-App-ClientVersion': str((2<<16)|(2<<8)|0)}
API_BASE = "https://ilinkai.weixin.qq.com"
ACCOUNTS_DIR = "/root/.hermes/profiles/xiaoxiaoxiong/home/.hermes/weixin/accounts"
PROFILE_NAME = "CHANGE_ME"  # ← 改这里为新人 profile 名

def log(msg):
    with open(LOG, "a") as f:
        f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")
    print(msg, flush=True)

def get_fresh_qr():
    resp = requests.get(f"{API_BASE}/ilink/bot/get_bot_qrcode?bot_type=3", headers=HEADERS, timeout=15)
    data = resp.json()
    return data["qrcode"], data["qrcode_img_content"]

def save_credentials(aid, token, uid, burl):
    os.makedirs(ACCOUNTS_DIR, exist_ok=True)
    with open(f"{ACCOUNTS_DIR}/{aid}.json", "w") as f:
        json.dump({"account_id": aid, "token": token, "user_id": uid, "base_url": burl}, f, indent=2)
    env_path = f"/root/.hermes/profiles/{PROFILE_NAME}/.env"
    with open(env_path, "r") as f:
        env = f.read()
    env = re.sub(r'WEIXIN_HOME_CHANNEL=.*', f'WEIXIN_HOME_CHANNEL={uid}', env)
    env = re.sub(r'WEIXIN_ACCOUNT_ID=.*', f'WEIXIN_ACCOUNT_ID={aid}', env)
    env = re.sub(r'WEIXIN_TOKEN=.*', f'WEIXIN_TOKEN={token}', env)
    env = re.sub(r'WEIXIN_BASE_URL=.*', f'WEIXIN_BASE_URL={burl}', env)
    with open(env_path, "w") as f:
        f.write(env)

log("🚀 启动")
refresh_count = 0
while refresh_count < 30:
    qid, url = get_fresh_qr()
    log(f"QR_READY|{url}|{qid}")
    
    try:
        import qrcode as qrcode_lib
        from PIL import Image, ImageDraw, ImageFont
        qr = qrcode_lib.QRCode(version=2, error_correction=qrcode_lib.constants.ERROR_CORRECT_M, box_size=10, border=2)
        qr.add_data(url); qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        img.save("/root/hermes/cache/images/onboard_qr.png")
        log("QR_IMG_SAVED")
    except Exception as e:
        log(f"QR_IMG_ERR: {e}")
    
    for _ in range(20):
        try:
            resp = requests.get(f"{API_BASE}/ilink/bot/get_qrcode_status?qrcode={qid}", headers=HEADERS, timeout=5)
            data = resp.json()
            s = data.get("status", "")
            if s == "confirmed":
                aid = data.get("ilink_bot_id", "")
                token = data.get("bot_token", "")
                uid = data.get("ilink_user_id", "")
                burl = data.get("baseurl", API_BASE)
                save_credentials(aid, token, uid, burl)
                log(f"DONE|account_id={aid}|user_id={uid}")
                sys.exit(0)
            elif s == "scaned":
                log("SCANNED|等待手机确认...")
            elif s == "expired":
                refresh_count += 1
                break
        except:
            pass
        time.sleep(1.5)
    else:
        refresh_count += 1

log("TIMEOUT")
