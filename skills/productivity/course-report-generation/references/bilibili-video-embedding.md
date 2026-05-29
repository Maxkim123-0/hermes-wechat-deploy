# B站 Video Embedding Reference

## Quick Verification Checklist

- [ ] Navigate to `https://www.bilibili.com/video/BVxxx` — verify page loads with title/views/uploader
- [ ] `curl -sI -H "Referer: https://www.bilibili.com" "https://player.bilibili.com/player.html?bvid=BVxxx&page=1&high_quality=1"` returns HTTP 200
- [ ] Iframe `src` uses `https://...` NOT `//...`
- [ ] Iframe has `referrerpolicy="no-referrer"` and `sandbox="allow-scripts allow-same-origin allow-popups allow-presentation"`
- [ ] Open HTML in browser, scroll to video section, check console for B站 player framework logs

## Critical Pitfall: Protocol-Relative URLs

```html
<!-- WRONG — breaks from file:// -->
<iframe src="//player.bilibili.com/player.html?bvid=..."></iframe>

<!-- CORRECT -->
<iframe src="https://player.bilibili.com/player.html?bvid=..."></iframe>
```

When HTML is opened from `file://`, `//` resolves to `file://player.bilibili.com/...` which is broken. Always use explicit `https://`.

## B站 Player Response Headers (verified 2026-05-14)

```
HTTP/2 200
content-type: text/html; charset=utf-8
access-control-allow-origin: *
access-control-allow-credentials: true
cross-origin-resource-policy: cross-origin
```

B站 allows cross-origin embedding. The player framework (jinkela-core, bili-fe-fp, bili-fe-mirror) loads in iframes fine. Headless browsers may show blank video player due to missing HTML5 codecs — this is NOT an embedding issue. In real Chrome/Edge, videos play correctly.

## Headless Browser Testing Limitation

Headless Chrome lacks HTML5 video codec support. The B站 player will show console logs like:
- `bili-fe-fp: 1.1.4` ✅
- `bili-fe-mirror v2.1.0` ✅  
- `白屏检测是否正常 {status: "ok"}` ✅
- Error about HTML5 playback not supported (codec issue, not embedding issue)

Use `curl` against the player endpoint as the definitive test. If it returns 200 with valid content-length, the video is embeddable.

## BV Number Search Strategy

To find relevant B站 videos:
1. Use `browser_navigate` to `https://search.bilibili.com/all?keyword=KEYWORD`
2. Scan results for relevant titles, check view counts
3. Extract BV numbers from result links (format: `https://www.bilibili.com/video/BVxxx`)
4. **Verify each BV number** by navigating to the video page
5. Never claim a BV number exists without visiting its page first

## Valid BV Numbers from This Session (verified 2026-05-14)

- `BV18aUrBpEqz` — 高敏感人群与大五人格, 百温心理, 2.3万播放, 2025-11-24
- `BV1NY411P7en` — 四种气质类型·林黛玉张飞王熙凤沙和尚, 校园整活王, 2.3万播放, 2022-04-25
