# Chinese Vision Provider Setup for Hermes

When the primary model lacks vision (e.g. DeepSeek, DeepSeek-V4), configure a domestic Chinese provider as vision fallback. This avoids OCR dependency and slow model downloads.

## Recommended: 智谱 GLM (Z.AI)

Free tier most generous, Chinese-native, no network issues.

### Setup

```bash
# 1. Register at https://bigmodel.cn → get API Key

# 2. Configure Hermes
hermes config set auxiliary.vision.provider zai
hermes config set auxiliary.vision.model glm-4v-flash

# 3. Add API key
echo "ZAI_API_KEY=your-key-here" >> ~/.hermes/profiles/<profile>/.env

# 4. Restart gateway (if running)
hermes gateway restart
```

### Verify

Send an image via WeChat or use `vision_analyze` — should get Chinese text recognition.

## Alternatives

| Provider | Model | Key Env Var | Free Tier |
|----------|-------|-------------|-----------|
| 智谱 GLM | glm-4v-flash | ZAI_API_KEY | ~18 yuan credits |
| 阿里百炼 | qwen-vl-max | DASHSCOPE_API_KEY | 1M tokens/month |
| Kimi | kimi-vision | KIMI_API_KEY | ~15 yuan credits |
| MiniMax | abab-vision | MINIMAX_CN_API_KEY | trial credits |

## Notes

- GLM-4V-Flash is the cheapest vision model, ~0.01 yuan per image
- The API key also grants access to chat models (GLM-5, GLM-5.1, etc.) — can serve as backup chat model
- Config changes take effect on gateway restart; env vars require process restart
- Network issues with HuggingFace/GitHub are bypassed since models run on provider's servers
