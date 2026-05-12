#!/usr/bin/env python3
"""为新用户生成 iLink Bot 二维码，轮询等待扫码，自动保存凭证到指定 Profile。

用法：
    python3 new_user_qr.py <profile_name>

流程：
    1. 调用 iLink GET API 获取二维码（无需 auth token）
    2. 生成 PNG 二维码图片
    3. 轮询 get_qrcode_status 等待扫码确认
    4. 确认后自动写入 Profile 的 .env 文件

注意：
    - QR 约 35 秒过期，脚本会自动刷新（最多 3 次）
    - iLink 一个 Bot 只能绑一个微信用户，每次扫码创建新 Bot
    - save_weixin_account 必须使用关键字参数！
"""

import asyncio, aiohttp, json, time, os, sys, ssl, certifi
from PIL import Image, ImageDraw, ImageFont
import qrcode as qrcode_lib

ILINK_BASE = "https://ilinkai.weixin.qq.com"
BOT_TYPE = "3"
QR_TIMEOUT = 35000
WAIT_MINUTES = 5

def make_ssl():
    ctx = ssl.create_default_context(cafile=certifi.where())
    return aiohttp.TCPConnector(ssl=ctx)

async def api_get(session, endpoint, timeout_ms=QR_TIMEOUT):
    url = f"{ILINK_BASE}/{endpoint}"
    headers = {"iLink-App-Id": "bot", "iLink-App-ClientVersion": str((2<<16)|(2<<8)|0)}
    timeout = aiohttp.ClientTimeout(total=timeout_ms/1000)
    async with session.get(url, headers=headers, timeout=timeout) as resp:
        text = await resp.text()  # Content-Type may be octet-stream despite JSON body
        return json.loads(text)

def save_qr_image(qr_url, label, path):
    qr = qrcode_lib.QRCode(version=2, error_correction=qrcode_lib.constants.ERROR_CORRECT_M,
                          box_size=10, border=2)
    qr.add_data(qr_url); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    w, h = img.size
    ni = Image.new("RGB", (w, h+50), "white")
    ni.paste(img, (0, 0))
    draw = ImageDraw.Draw(ni)
    try:
        font = ImageFont.truetype("/usr/share/fonts/google-noto-cjk/NotoSansCJK-DemiLight.ttc", 14)
    except:
        font = ImageFont.load_default()
    draw.text((w//2, h+8), label, fill="black", font=font, anchor="mt")
    draw.text((w//2, h+30), "扫完在手机确认即可", fill="gray", font=font, anchor="mt")
    ni.save(path)
    return path

async def main():
    if len(sys.argv) < 2:
        print("用法: python3 new_user_qr.py <profile_name>")
        return 1
    
    profile_name = sys.argv[1]
    hermes_home = f"/root/.hermes/profiles/{profile_name}/home/.hermes"
    output_dir = f"/root/hermes/cache/images"
    os.makedirs(output_dir, exist_ok=True)
    
    connector = make_ssl()
    async with aiohttp.ClientSession(connector=connector, trust_env=True) as session:
        print(f"📡 为 {profile_name} 获取二维码...")
        qr_resp = await api_get(session, f"ilink/bot/get_bot_qrcode?bot_type={BOT_TYPE}")
        qrcode_value = qr_resp.get("qrcode", "")
        qrcode_url = qr_resp.get("qrcode_img_content", "")
        
        if not qrcode_value:
            print("❌ 获取二维码失败:", json.dumps(qr_resp, ensure_ascii=False))
            return 1
        
        qr_path = os.path.join(output_dir, f"{profile_name}_qr.png")
        save_qr_image(qrcode_url, f"{profile_name} 扫码添加 Hermes", qr_path)
        print(f"✅ 二维码: {qr_path}")
        print(f"🔗 链接: {qrcode_url}")
        print(f"\n⏳ 等待扫码确认（最长 {WAIT_MINUTES} 分钟）...\n")
        
        deadline = time.monotonic() + WAIT_MINUTES * 60
        refresh_count = 0
        
        while time.monotonic() < deadline:
            try:
                status_resp = await api_get(session, f"ilink/bot/get_qrcode_status?qrcode={qrcode_value}")
            except Exception as e:
                await asyncio.sleep(1)
                continue
            
            status = status_resp.get("status", "wait")
            
            if status == "wait":
                print(".", end="", flush=True)
            elif status == "scaned":
                print("\n📱 已扫码！请在手机上点击确认...")
            elif status == "expired":
                refresh_count += 1
                if refresh_count > 3:
                    print("\n❌ 二维码多次过期")
                    return 1
                print(f"\n🔄 刷新 ({refresh_count}/3)...")
                qr_resp = await api_get(session, f"ilink/bot/get_bot_qrcode?bot_type={BOT_TYPE}")
                qrcode_value = qr_resp.get("qrcode", "")
                qrcode_url = qr_resp.get("qrcode_img_content", "")
                save_qr_image(qrcode_url, f"{profile_name} 扫码添加 Hermes", qr_path)
            elif status == "confirmed":
                print("\n🎉 确认成功！")
                account_id = status_resp.get("ilink_bot_id", "")
                token = status_resp.get("bot_token", "")
                base_url = status_resp.get("baseurl", ILINK_BASE)
                user_id = status_resp.get("ilink_user_id", "")
                
                if not account_id or not token:
                    print("❌ 凭证不完整")
                    return 1
                
                # 保存到 accounts 目录
                accounts_dir = os.path.join(hermes_home, "weixin", "accounts")
                os.makedirs(accounts_dir, exist_ok=True)
                with open(os.path.join(accounts_dir, f"{account_id}.json"), "w") as f:
                    json.dump({"account_id": account_id, "token": token, "base_url": base_url, "user_id": user_id}, f, indent=2)
                
                # 写入 Profile .env
                env_path = f"/root/.hermes/profiles/{profile_name}/.env"
                env_content = f"""WEIXIN_CDN_BASE_URL=https://novac2c.cdn.weixin.qq.com/c2c
WEIXIN_DM_POLICY=open
WEIXIN_ALLOW_ALL_USERS=true
WEIXIN_ALLOWED_USERS=
WEIXIN_GROUP_POLICY=disabled
WEIXIN_GROUP_ALLOWED_USERS=
WEIXIN_HOME_CHANNEL={user_id}
WEIXIN_ACCOUNT_ID={account_id}
WEIXIN_TOKEN={token}
WEIXIN_BASE_URL={base_url}
WEIXIN_DM_POLICY=open
WEIXIN_ALLOW_ALL_USERS=true
"""
                os.makedirs(os.path.dirname(env_path), exist_ok=True)
                with open(env_path, "w") as f:
                    f.write(env_content)
                
                print(f"\n✅ {profile_name} 接入完成！")
                print(f"   account_id: {account_id}")
                print(f"   user_id:    {user_id}")
                print(f"   Profile:    {env_path}")
                return 0
            
            await asyncio.sleep(1)
        
        print(f"\n⏰ 超时（{WAIT_MINUTES} 分钟）")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
