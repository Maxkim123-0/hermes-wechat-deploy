# Model/Provider Switching Protocol

## Golden Rule (from real pain)

**ALWAYS verify a new API key BEFORE switching provider.**

```bash
# Test the key first
curl -s https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $NEW_KEY" \
  | head -5

# Only if that passes, change config
hermes config set model.provider openrouter
hermes config set model.default anthropic/claude-sonnet-4
hermes gateway restart
```

**Why:** Switching config + restarting gateway without verification can cause a 402 (insufficient credits) infinite retry loop. The gateway keeps retrying the failed API call, flooding the user with error messages. Recovery requires manually reverting config + restarting gateway.

## Current Recommended Stack (Price-Sensitive Chinese User)

| Layer | Provider | Model | Cost $/1M (in/out) | Purpose |
|-------|----------|-------|:---:|---------|
| 🥇 Default | DeepSeek | V4 Flash | $0.14 / $0.28 | Daily chat (fast, cheap) |
| 🥈 Complex | DeepSeek | V4 Pro | $0.30 / $0.50 | Deep reasoning, code |
| 🛡️ Fallback | Z.AI (智谱) | GLM-5 | Free (new user) | DeepSeek GFW'd |
| 🧿 Vision | Z.AI (智谱) | GLM-4V-Flash | Free | Image analysis |
| 🌐 GFW bypass | OpenRouter | V4 Flash | $0.14 / $0.28 (same!) | When DeepSeek blocked |

## Provider Price Reality Check

### OpenRouter vs Direct — the real story

**Most models ARE marked up on OpenRouter** (45-74% more expensive for many). BUT:
- **DeepSeek V4 Flash is NOT marked up** — same price as direct ($0.14/$0.28)
- **Other DeepSeek models** (V4 Pro, V3) — marked up 45-74%
- **Claude/GPT models** — marked up 10-30%

So the only case where OpenRouter makes sense cost-wise is V4 Flash as a GFW bypass.

### Chinese Providers (no GFW issues)

| Provider | Model | Cost | Notes |
|----------|-------|------|-------|
| Z.AI / 智谱 | GLM-5 | ~$0.69/1M (¥5) | Free credits for new users |
| DashScope / 阿里 | Qwen-Turbo | ~$0.11/$0.28 | Good price, no GFW |
| Kimi / Moonshot | kimi-vision | Free credits | Vision only |

## Switching Workflows

### Switch to OpenRouter (GFW bypass)
```bash
# 1. Verify key
curl -s https://openrouter.ai/api/v1/auth/key \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"

# 2. Config
hermes config set model.provider openrouter
hermes config set model.default deepseek/deepseek-v4-flash

# 3. Restart
hermes gateway restart
```

### Switch back to DeepSeek direct
```bash
hermes config set model.provider deepseek
hermes config set model.default deepseek-v4-flash
hermes gateway restart
```

### Verify fallback chain
```bash
hermes config | grep -A5 fallback
# Expected:
#   fallback_providers: ['zai']
#   fallback_model: glm-5
```

## Vision Configuration

Non-vision models (DeepSeek, most local models) will fail `vision_analyze` with `"unknown variant 'image_url'"`. Configure a vision fallback:

```bash
hermes config set auxiliary.vision.provider zai
hermes config set auxiliary.vision.model glm-4v-flash
```

## Pitfalls

- **Don't switch mid-session.** Config changes take effect on next session start (`/reset` in CLI, gateway restart for WeChat).
- **OpenRouter key with $0 balance = 402 infinite loop.** Always check credits first.
- **Fallback config can be silently lost** when rewriting model config. Always re-verify after making changes.
- **DeepSeek direct connection can be GFW'd** unpredictably in China. This manifests as timeouts or connection errors, not clear error messages.
