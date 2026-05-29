# Content Extraction Pitfalls (Anti-Patterns)

Documenting what NOT to do when extracting content from links.

## Douyin (抖音)

**Problem:** SSR page has no `<video>` element. SSR page returned "视频数据加载中".

**What we tried (all failed):**
- `curl` + parsing JSON from page → no video data in static HTML
- Third-party download APIs (tikwm.com, api.douyin.wtf, snaptik.app) → all blocked/obfuscated
- Douyin iteminfo API (`iesdouyin.com/web/api/v2/aweme/iteminfo/`) → `encrypt_data_miss` error
- Playwright headless → page loaded SSR version with no video

**What worked:**
- `browser_navigate` with mobile user-agent → got page with ROUTER_DATA
- `vision_analyze` on screenshot → read text from thumbnail/cover image
- `yt-dlp` download → **FAILED** unless fresh cookies available (`ERROR: Fresh cookies are needed`). Douyin aggressively blocks anonymous yt-dlp downloads.
- B站 cross-search → same content often reposted on Bilibili with accessible API
- `r.jina.ai` proxy: `https://r.jina.ai/<target-url>` → sometimes bypasses blocks (timed out on Zhihu but worth trying)
- 知乎: search for same-topic article titles → often a text version exists on CSDN/Juejin

**🔥 User frustration signal:** when user says "暂停任务 先给我设置好" or "你为什么不听我的" — STOP researching immediately. Switch to executing what you already know. User prefers action over exhaustive search.

## B站 (Bilibili)

**What works:**
- API: `api.bilibili.com/x/web-interface/view?bvid=BVxxx` → title, desc, stats
- API: `api.bilibili.com/x/player/v2?bvid=BVxxx` → subtitle info
- Search: `search.bilibili.com/all?keyword=...` → BV list

**Pitfall:** Subtitle API `subtitles` array often empty (`[]`) — many videos have no CC.

## Bing Search

**Problem:** Chinese keyword tokenization breaks — "瑞幸咖啡" parsed as "瑞" + "幸" → returns dictionary definitions.

**Fix:** 
1. Use English keywords when possible
2. Or use `browser_navigate` + `browser_console` to extract results from rendered page

## MarketBeat / Yahoo Finance

**Problem:** Aggressive Cloudflare Turnstile / bot detection → "Performing security verification" page.

**No workaround found.** These sites specifically block headless browsers.

## Zhihu (知乎)

**Problem:** Aggressive anti-bot — returns 403 JSON `{"error":{"message":"您当前请求存在异常...","code":40362}}`.

**What failed:**
- `web_extract` → `Failed to fetch url`
- `browser_navigate` → single checkbox element, 40362 in body
- Google cache → cookie consent wall, no cached content
- `r.jina.ai` proxy → timed out
- `textise.iitty` → blocked

**What worked:**
- Search for same article title on CSDN/Juejin — many Zhihu articles are cross-posted
- In this session: searched "Hermes 7 步封神操作" → found on Zhihu but extraction failed → found related content on Douyin description + Reddit

## YouTube

**Problem:** `ERR_CONNECTION_TIMED_OUT` from this server (Alibaba Cloud, China). YouTube is blocked at network level.

**Workaround:** None from this server. Must use a different machine or VPN.

## Key Extraction Principle

When content extraction completely fails after 3 methods (browser → yt-dlp → cross-platform):
**STOP and tell the user.** Don't burn 10 turns trying Google Cache → Jina → textise → alternatives.
User's time is more valuable than the content.

## Date of session
2026-05-15
