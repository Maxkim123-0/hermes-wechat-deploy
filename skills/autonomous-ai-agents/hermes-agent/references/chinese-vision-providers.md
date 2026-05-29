# Chinese Vision Providers for Hermes

When the main model (e.g. DeepSeek) lacks vision capabilities, configure an auxiliary vision provider from a Chinese AI platform.

## Quick Setup

```bash
# 1. Get API key from one of the providers below
# 2. Set env var + config
echo "ZAI_API_KEY=your-key" >> ~/.hermes/profiles/<profile>/.env
hermes config set auxiliary.vision.provider zai
hermes config set auxiliary.vision.model glm-4v-flash
# Restart gateway for env var to take effect
```

## Providers

| Provider | Model | Cost | Config Key | Signup |
|----------|-------|------|-----------|--------|
| **智谱 GLM (Z.AI)** | glm-4v-flash | Free tier (18¥+ tokens) | `ZAI_API_KEY` | bigmodel.cn |
| 阿里百炼 (DashScope) | qwen-vl-plus | Free tier (1M tokens) | `DASHSCOPE_API_KEY` | dashscope.aliyun.com |
| 月之暗面 Kimi | kimi-vision | Free 15¥ signup | `KIMI_API_KEY` | platform.moonshot.cn |
| MiniMax | minimax-vl | Pay per use | `MINIMAX_API_KEY` | minimax.com |

## GLM/Z.AI (Recommended for Students)

- New users get ~18¥ worth of tokens + dedicated vision package (6-10M tokens)
- One image ≈ 1,000-3,000 tokens → vision pack alone lasts 5,000-15,000 images
- Also usable as fallback chat model (`glm-5`) when main model fails

### Setup GLM fallback

```bash
hermes config set model.fallback_providers "['zai']"
hermes config set model.fallback_model glm-5
hermes config set providers.zai.api_key_env ZAI_API_KEY
hermes config set providers.zai.base_url "https://open.bigmodel.cn/api/paas/v4"
```

## Verify

Send an image via WeChat and check that `vision_analyze` returns Chinese text. Check agent logs for provider routing.

## Pitfalls

- GLM-4V-Flash may not appear in the model list API but works for vision
- Gateway must be restarted after adding env vars
- If `vision_analyze` returns JSON deserialization error, the model doesn't support vision — check `auxiliary.vision.model` matches provider
