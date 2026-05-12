# iLink Bot QR Code Generation

Complete recipe for generating a scannable WeChat QR code to add a bot contact.

## Prerequisites

```bash
pip install qrcode[pil] requests
```

## Full Script

```python
import requests
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

# === Config ===
TOKEN = "a54e296c8079@im.bot:060000e05d5c7a921d69f8727f207c5ffd0c78"
BASE_URL = "https://ilinkai.weixin.qq.com"
BOT_TYPE = "3"
OUTPUT = "bot_qr_share.png"

# === Step 1: Get QR data from iLink ===
resp = requests.post(
    f"{BASE_URL}/ilink/bot/get_bot_qrcode?bot_type={BOT_TYPE}",
    json={"token": TOKEN},
    timeout=15
)
data = resp.json()
assert data["ret"] == 0, f"API error: {data}"

liteapp_url = data["qrcode_img_content"]
# Example: https://liteapp.weixin.qq.com/q/7GiQu1?qrcode=xxxx&bot_type=3

# === Step 2: Generate QR image from URL ===
qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_M,
                    box_size=10, border=2)
qr.add_data(liteapp_url)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

### Step 3 (optional): Add label below QR

**Chinese font path** (this server): `/usr/share/fonts/google-noto-cjk/NotoSansCJK-DemiLight.ttc`

```python
w, h = img.size
new_img = Image.new("RGB", (w, h + 60), "white")
new_img.paste(img, (0, 0))
draw = ImageDraw.Draw(new_img)
try:
    font = ImageFont.truetype(
        "/usr/share/fonts/google-noto-cjk/NotoSansCJK-DemiLight.ttc", 16
    )
except OSError:
    font = ImageFont.load_default()
draw.text((w // 2, h + 10), "扫码添加 Hermes Bot", fill="black", font=font, anchor="mt")
draw.text((w // 2, h + 35), f"Bot 账号", fill="gray", font=font, anchor="mt")
w, h = img.size
new_img = Image.new("RGB", (w, h + 60), "white")
new_img.paste(img, (0, 0))
draw = ImageDraw.Draw(new_img)
try:
    font = ImageFont.truetype(
        "/usr/share/fonts/google-noto-cjk/NotoSansCJK-DemiLight.ttc", 16
    )
except OSError:
    font = ImageFont.load_default()
draw.text((w // 2, h + 10), "扫码添加 Hermes Bot", fill="black", font=font, anchor="mt")

new_img.save(OUTPUT)
print(f"QR saved: {OUTPUT}")
```

## API Response Format

```json
{
  "qrcode": "af56425ef5966f7eb1f2eeae159506e3",
  "qrcode_img_content": "https://liteapp.weixin.qq.com/q/7GiQu1?qrcode=xxx&bot_type=3",
  "ret": 0
}
```

## Pitfalls

- **bot_type=3 is required** as a query parameter. Missing it returns `{"err_msg": "missing bot_type", "ret": 1}`
- **qrcode_img_content is a URL, NOT an image**. You MUST use qrcode library to convert it to an image.
- **QR codes expire**. Generate fresh when needed.
- The liteapp URL is NOT a standard WeChat QR — scanning it opens a liteapp confirmation page.
