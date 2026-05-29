# Model Switching Diagnostics Quick Reference

## Root Cause Checklist (when user says "why is model switching/fallbacking")

1. **Check DeepSeek balance first** — most common cause
   Use the balance API with the auth header to check if account is available.
   Look for `"is_available": false` or negative balance → 402 errors trigger fallback attempts.

2. **Check if config was mid-conversation** — NEVER change model config while gateway is live.
   If you patched config.yaml during a session, the gateway picked it up and the user saw the model label change.

3. **Check fallback config** — empty fallback_providers + commented fallback_model = no actual fallback.
   The 402 errors just retry and fail, which looks like "fallback jumping" to the user.

4. **Check API key** — only DEEPSEEK_API_KEY in .env? No ZAI/OpenRouter key configured?
   Then there's no real fallback possible.

## Fixes

| Problem | Fix |
|---------|-----|
| Mid-conversation config change | NEVER do this. Always warn user + restart gateway. |
| DeepSeek balance negative (-0.47 CNY) | Recharge account OR configure a fallback provider |
| No fallback configured | Add fallback_model at root level of config.yaml |
| Cronjob using wrong model | Explicitly set model param on cronjob create |

## Golden Rule (memorize this)

**Any model change → needs gateway restart → tell user first → confirm → do it.**
**Never silently change model config mid-conversation.**
**Always curl-test the new key/balance before switching.**
