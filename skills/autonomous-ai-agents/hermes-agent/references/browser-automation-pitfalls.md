# Browser Automation Pitfalls & Patterns

## Regional Issues: Chinese Websites

Chinese search engines and major platforms aggressively detect headless/automated browsers. Expect captchas or blank pages on:

| Site | Behavior | Workaround |
|------|----------|------------|
| **Baidu** (baidu.com) | Immediate captcha wall (`wappass.baidu.com`) | Don't use; prefer Bing or direct site access |
| **Bing China** (cn.bing.com) | Returns empty snapshot or irrelevant results | Use `browser_console` to extract `document.body.innerText`; snapshot alone is unreliable |
| **WeChat articles** | JS-rendered, bot detection | Better to use direct API or manual share |
| **Taobao/JD** | Heavy anti-bot, requires login | Not suitable for automation |

**Rule of thumb:** When targeting Chinese web content, prefer API-based approaches (web_search, direct HTTP) over browser automation. Browser is best for English/international sites and authenticated dashboards.

## Tool Reliability Hierarchy

From most to least reliable for content extraction:

1. **`browser_navigate` snapshot** — structured DOM with refs, always reliable when page loads
2. **`browser_console` + JS** — `document.body.innerText`, `document.querySelector()`, etc. Direct DOM access, bypasses rendering issues
3. **`browser_vision`** — AI image analysis. **Can hallucinate content confidently.** Vision model may describe wrong page content or invent details. Use as last resort or for visual-only tasks (layout check, screenshot capture)

**Pattern: fallback chain**
```
browser_navigate → snapshot empty? → browser_console to extract text → still nothing? → browser_vision as final check
```

## `browser_vision` Hallucination

Observed case: Bing CN search results page was correctly rendered, but vision analysis described it as "Palace Museum Digital Cultural Relic Library" with unrelated URLs. The actual page content (confirmed via `browser_console`) was Bing search results.

**Mitigation:**
- Always cross-check vision output with console-extracted text when possible
- For content verification, prefer `browser_console` over `browser_vision`
- Vision is best for: layout/debugging screenshots, verifying visual elements exist, reading CAPTCHAs
- Vision is unreliable for: reading and transcribing page text, identifying specific URLs or links

## Snapshot Element References

`browser_navigate` returns `ref` attributes (e.g., `ref=e8`) that can be used with `browser_click(ref="e8")`. These are stable within a page load but reset on navigation. Always capture the snapshot after navigating before clicking.
