# iLink QR Login — 可独立运行的参考脚本

此脚本在同一进程内完成「生成 QR → 轮询 → 确认 → 自动保存凭证」。支持自动刷新过期码。

```python
#!/usr/bin/env python3
"""持续生成新鲜 QR，等用户扫码确认，自动保存凭证。"""
import requests, json, time, os, sys

LOG = "/tmp/qr_login.log"
HEADERS = {"iLink-App-Id": "bot", "iLink-App-ClientVersion": str((2<<16)|(2<<8)|0)}
API_BASE = "https://ilinkai.weixin.qq.com"

def log(msg):
    with open(LOG, "a") as f:
        f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")
    print(msg, flush=True)

def get_fresh_qr():
    """获取新二维码。GET + headers，不带 token。"""
    resp = requests.get(
        f"{API_BASE}/ilink/bot/get_bot_qrcode?bot_type=3",
        headers=HEADERS, timeout=15
    )
    # ⚠️ 不能用 resp.json()，Content-Type 是 application/octet-stream
    data = json.loads(resp.text)
    return data["qrcode"], data["qrcode_img_content"]

def save_credentials(aid, token, uid, burl, accounts_dir, env_path, api_key):
    """保存到 accounts/ 目录，写入 profile .env。"""
    os.makedirs(accounts_dir, exist_ok=True)
    with open(f"{accounts_dir}/{aid}.json", "w") as f:
        json.dump({
            "account_id": aid, "token": token,
            "user_id": uid, "base_url": burl
        }, f, indent=2)

    # 从主 profile 复制 .env，只替换 Weixin 相关字段
    env_content = f"""DEEPSEEK_API_KEY={api_key}
WEIXIN_CDN_BASE_URL=https://novac2c.cdn.weixin.qq.com/c2c
WEIXIN_DM_POLICY=open
WEIXIN_ALLOW_ALL_USERS=true
WEIXIN_HOME_CHANNEL={uid}
WEIXIN_ACCOUNT_ID={aid}
WEIXIN_TOKEN={token}
WEIXIN_BASE_URL={burl}
"""
    with open(env_path, "w") as f:
        f.write(env_content)

def main(accounts_dir, env_path, api_key, qr_img_path=None):
    log("🚀 启动")
    refresh_count = 0

    while refresh_count < 30:  # 最多刷新 30 次
        qid, url = get_fresh_qr()
        log(f"QR_READY|{url}|{qid}")

        # 可选：生成 QR 图片
        if qr_img_path:
            try:
                import qrcode
                from PIL import Image, ImageDraw, ImageFont
                qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_M,
                                   box_size=10, border=2)
                qr.add_data(url); qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
                w, h = img.size
                ni = Image.new("RGB", (w, h+40), "white")
                ni.paste(img, (0, 0))
                img = ImageDraw.Draw(ni)
                font = ImageFont.truetype(
                    "/usr/share/fonts/google-noto-cjk/NotoSansCJK-DemiLight.ttc", 14)
                img.text((w//2, h+12), "扫码点确认", fill="black", font=font, anchor="mt")
                ni.save(qr_img_path)
            except Exception:
                pass

        # 短超时轮询（不用 35s 长轮询，避免阻塞）
        for _ in range(20):
            try:
                resp = requests.get(
                    f"{API_BASE}/ilink/bot/get_qrcode_status?qrcode={qid}",
                    headers=HEADERS, timeout=5
                )
                data = json.loads(resp.text)
                s = data.get("status", "")

                if s == "confirmed":
                    aid = data.get("ilink_bot_id", "")
                    token = data.get("bot_token", "")
                    uid = data.get("ilink_user_id", "")
                    burl = data.get("baseurl", API_BASE)
                    save_credentials(aid, token, uid, burl, accounts_dir, env_path, api_key)
                    log(f"DONE|account_id={aid}|user_id={uid}")
                    return 0
                elif s == "scaned":
                    log("SCANNED|等待手机确认...")
                elif s == "expired":
                    log("EXPIRED|自动刷新...")
                    refresh_count += 1
                    break
            except Exception:
                pass
            time.sleep(1.5)
        else:
            log("EXPIRED|自动刷新...")
            refresh_count += 1

    log("TIMEOUT|超过最大刷新次数")
    return 1

if __name__ == "__main__":
    main(
        accounts_dir=sys.argv[1] if len(sys.argv) > 1 else "./weixin/accounts",
        env_path=sys.argv[2] if len(sys.argv) > 2 else "./.env",
        api_key=sys.argv[3] if len(sys.argv) > 3 else "",
        qr_img_path=sys.argv[4] if len(sys.argv) > 4 else None,
    )
```
