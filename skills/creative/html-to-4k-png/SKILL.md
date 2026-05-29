---
name: html-to-4k-png
description: Render HTML designs to 4K (3840×2160) PNG via headless Chromium — no more blurry browser screenshots.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [design, png, render, high-res, html]
    related_skills: [claude-design, popular-web-designs]
---

# HTML to 4K PNG

Design in HTML, export to high-resolution PNG. Replaces the old browser screenshot approach (limited to viewport resolution, often blurry on WeChat).

## Pipeline

```
HTML design (any design system) → Playwright headless Chromium → 4K PNG → MEDIA delivery
```

Requires: `playwright` + `chromium` (installed via npm).

## Render Script

Located at: `/tmp/render-html.js`

```bash
NODE_PATH=/usr/local/lib/node_modules node /tmp/render-html.js <input.html> [output.png] [scale=2]
```

Default: 1920×1080 viewport × 2 device scale = 3840×2160 output.

## Workflow

1. Design HTML using `claude-design` + `popular-web-designs` skills
2. Write HTML file with `write_file`
3. Render to 4K PNG:
   ```bash
   NODE_PATH=/usr/local/lib/node_modules node /tmp/render-html.js /tmp/design.html /tmp/design-4k.png 2
   ```
4. Share via MEDIA:/tmp/design-4k.png

## Scale Options

| Scale | Output Resolution | Use Case |
|-------|-------------------|----------|
| 1 | 1920×1080 | Quick preview |
| 2 | 3840×2160 | Delivery quality (default) |
| 3 | 5760×3240 | Print / large screen |

## Pitfalls

- Must use `NODE_PATH=/usr/local/lib/node_modules` — playwright is installed globally but Node can't resolve it without this
- Fonts: use Google Fonts CDN links in HTML `<head>`, Playwright loads them automatically
- Wait 500ms after page load for font rendering before screenshot
- HTML file must be absolute path or relative to cwd

### B站 (Bilibili) 视频嵌入

当 HTML 文件通过 `file://` 协议打开时（用户直接双击 HTML），iframe 的 `src` **必须**用 `https://` 而不是 `//`：

```html
<!-- ❌ 错误：file:// 下 // 会解析为 file://player.bilibili.com → 打不开 -->
<iframe src="//player.bilibili.com/player.html?bvid=..."></iframe>

<!-- ✅ 正确 -->
<iframe src="https://player.bilibili.com/player.html?bvid=BVxxx&page=1&high_quality=1&autoplay=0"
        allowfullscreen loading="lazy"
        referrerpolicy="no-referrer"
        sandbox="allow-scripts allow-same-origin allow-popups allow-presentation"></iframe>
```

验证方法：
1. `curl -sI -H "Referer: https://www.bilibili.com" "https://player.bilibili.com/player.html?bvid=BVxxx"` 应返回 HTTP 200
2. B站播放器返回 `access-control-allow-origin: *`，允许跨域嵌入
3. BV 号必须直接从 B站搜索结果页提取，**严禁编造**
