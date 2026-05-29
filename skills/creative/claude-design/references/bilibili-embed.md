# B站 (Bilibili) Video Embedding in Portable HTML

## Standard Embed Pattern

```html
<iframe
  src="https://player.bilibili.com/player.html?bvid=VIDEO_BVID&page=1&high_quality=1&autoplay=0"
  title="视频标题"
  allowfullscreen
  loading="lazy"
  referrerpolicy="no-referrer"
  sandbox="allow-scripts allow-same-origin allow-popups allow-presentation"
></iframe>
```

## Critical Gotcha: `//` Protocol-Relative URLs

**Never use `//player.bilibili.com/...` in standalone HTML files.**

When the user opens the HTML from disk (`file:///path/to/file.html`), the browser resolves `//player.bilibili.com` to `file://player.bilibili.com` — which doesn't exist. The iframe loads a blank page.

**Always use explicit `https://`.**

## Verification Checklist

Since headless browsers lack HTML5 video codecs, a blank iframe in the test environment is expected. Verify instead with:

1. **BV number validity** — navigate browser to `https://www.bilibili.com/video/BV...` and confirm the page loads with title, view count, and metadata visible.

2. **Player endpoint** — `curl -sI -H "Referer: https://www.bilibili.com" "https://player.bilibili.com/player.html?bvid=...&page=1&high_quality=1"` should return HTTP 200 with `access-control-allow-origin: *`.

3. **Player framework init** — open the HTML in the browser tool, scroll to the iframe, and check the console for B站 init messages:
   - `bili-fe-fp: 1.1.4`
   - `bili-fe-mirror v2.1.0`
   - `白屏检测是否正常 {status: "ok"}`
   - B站 ASCII art logo
   - `@bilibili/jinkela-core@2.8.14`

   If these appear, the player JS loaded successfully. The user's real browser (Chrome/Edge with video codecs) will render the video.

4. **Disclose limitations** — tell the user exactly: "Player framework loaded (console confirms), headless test browser can't decode video, your real Chrome will play it fine."

## Finding Valid BV Numbers

- Search B站 directly: navigate to `https://search.bilibili.com/all?keyword=YOUR_QUERY`
- Extract BV numbers from the search results page (they appear in video card links as `/video/BV...`)
- **Never invent or guess BV numbers.** A fabricated BV either resolves to a nonexistent video or, worse, resolves to a random unrelated video.
