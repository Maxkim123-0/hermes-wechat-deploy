# HTML Classroom Presentation Pattern

When a .pptx can't deliver (embedded videos, real interactivity, scroll pacing), build a single self-contained HTML page. This pattern was developed for a psychology classroom presentation on 气质与性格 and generalizes to any lecture.

## Why HTML over PPTX

| PPTX limitation | HTML solution |
|----------------|---------------|
| Can't embed streaming video | `<iframe>` B站/YouTube directly |
| Static slides, no real interactivity | JS quiz with instant feedback |
| Linear slide-by-slide | Scroll-snap sections with nav dots |
| Font/color limited | Full CSS design system |
| OS-dependent rendering | Any browser |

## Template Structure

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>...</title>
  <style>
    /* CSS custom properties for theme */
    :root { --primary: #6D2E46; --accent: #D4A574; ... }
    /* Scroll-snap for slide-like navigation */
    html { scroll-snap-type: y mandatory; }
    section { scroll-snap-align: start; min-height: 100vh; }
    /* Responsive bento grid for content cards */
    .bento { display: grid; grid-template-columns: repeat(6, 1fr); gap: 16px; }
  </style>
</head>
<body>
  <nav class="nav"><!-- Fixed right-side dot navigation --></nav>
  <section id="hero"><!-- Title slide --></section>
  <section id="quiz"><!-- Interactive quiz --></section>
  <section id="content-1"><!-- Content section --></section>
  <!-- ... more sections ... -->
  <script>
    // Quiz logic, scroll spy for nav dots
  </script>
</body>
</html>
```

## ⛔ CRITICAL: Never Fabricate BV IDs

**This is a zero-tolerance rule.** BV IDs, URLs, API endpoints, statistics, citations — never invent them. If you don't have a real verified ID, say so. The user will catch fabricated data immediately.

## B站 Video Embedding

Replace YouTube embeds with B站 iframes for Chinese classroom use:

```html
<iframe src="//player.bilibili.com/player.html?bvid=REAL_BV_ID&page=1&high_quality=1&autoplay=0"
  allowfullscreen loading="lazy"></iframe>
```

Key params: `bvid=`, `page=1`, `high_quality=1`, `autoplay=0` (classroom control).

## Finding BV IDs — Verified Workflow

1. Search B站: `https://search.bilibili.com/all?keyword=KEYWORD&order=click`
2. Extract BV IDs from DOM (browser console):
   ```js
   document.querySelectorAll('a[href*="video/BV"]').forEach(a => {
     const bv = a.href.match(/BV[a-zA-Z0-9]+/);
     const title = (a.querySelector('h3')||a).textContent.slice(0,60);
     if (bv) console.log(bv[0], title);
   });
   ```
3. Filter out "第五人格" game content (pollutes psychology searches)
4. Pick videos with high play count + appropriate duration (3-8 min for class)
5. **Verified BV IDs (extracted 2026-05-14):**
   - 大五人格: `BV18aUrBpEqz` (2.3万播放, 5:20, 百温心理)
   - 四种气质类型: `BV1NY411P7en` (2.3万播放, 5:01, 林黛玉·张飞·王熙凤·沙和尚)
   - Backup 大五: `BV1qw411H7KZ` (8743播放, 5:55)
   - Backup 气质: `BV1VA411N7kq` (2.0万播放, 3:41)

## Interactive Quiz Pattern

```javascript
document.querySelectorAll('.quiz-option').forEach(opt => {
  opt.addEventListener('click', function() {
    // Highlight selected
    document.querySelectorAll('.quiz-option').forEach(o => o.classList.remove('selected'));
    this.classList.add('selected');
    // Show typed result
    const type = this.dataset.type;
    const result = results[type]; // Pre-defined result map
    document.getElementById('quiz-result').innerHTML = result;
    document.getElementById('quiz-result').classList.add('show');
  });
});
```

## Design Principles

1. **Dark background + one warm accent** — premium feel, easy on projector eyes
2. **Bento grid** for content cards — `grid-template-columns: repeat(6, 1fr)` with `.span-2` to `.span-4` classes
3. **Scroll-snap** sections — feels like slides but scrolls naturally
4. **Right-side nav dots** — `position: fixed` with IntersectionObserver scroll spy
5. **Stats as big numbers** — `.stat-big { font-size: 3.5rem }` for impact

## Rendering Preview

Use the html-to-4k-png pipeline for a preview image:

```bash
NODE_PATH=/usr/local/lib/node_modules node \
  /root/.hermes/profiles/xiaoxiaoxiong/skills/creative/html-to-4k-png/scripts/render.js \
  input.html output.png 2
```

## Delivery

- Send the `.html` file directly — it's self-contained (all CSS/JS inline)
- Classroom: open in Chrome/Firefox, F11 fullscreen, scroll through
- Also provide a `.md` script file with speaker notes timed to each section
