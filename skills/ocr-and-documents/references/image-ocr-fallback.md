# Image OCR Fallback for Non-Vision Models

When `vision_analyze` returns `"unknown variant 'image_url', expected 'text'"` — this means the active model (e.g. deepseek-v4-pro) does not support native vision. Fall back to local OCR.

## Quick Path

```bash
# 1. Install tesseract (if missing)
yum install -y tesseract   # RHEL/Alibaba Linux
# apt install tesseract-ocr  # Debian/Ubuntu

# 2. Check available languages
tesseract --list-langs

# 3. Run OCR (English-only if Chinese tessdata unavailable)
tesseract /path/to/image.jpg stdout -l eng

# 4. For Chinese, download chi_sim.traineddata to /usr/share/tesseract/tessdata/
#    If GitHub is blocked, use a mirror or skip — English OCR still picks up
#    numbers, IDs, and ASCII text from Chinese screenshots.
```

## What works without Chinese tessdata

English OCR on a Chinese billing/console screenshot still yields:
- Numbers (prices, instance IDs, GB sizes)
- English keywords (ECS, ESSD, CPU, GB, Mbps, Linux)
- Alphanumeric IDs

This is often enough to identify what the screenshot shows and guide the user to the right page.

## Pitfalls

- OCR quality on screenshots is poor — set expectations ("OCR quality limited but here's what I found")
- GitHub may be unreachable from some servers (e.g. Alibaba Cloud CN) — tessdata download can time out
- Don't spend more than 2 attempts downloading tessdata; fall back to English OCR + user guidance
