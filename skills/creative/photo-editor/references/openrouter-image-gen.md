# OpenRouter 图片生成工作流

## 概述
OpenRouter 的 Chat Completions API 支持图片生成，通过 `modalities` 参数控制。中国服务器可访问的模型及其实战验证结果如下。

## 可用模型速查

| 模型 | 文生图 | 图生图(参考图) | 中国可访问 | 备注 |
|------|:---:|:---:|:---:|------|
| `x-ai/grok-imagine-image-quality` | ✅ | ✅ | ✅ | **推荐**，传参考图+指令编辑 |
| `black-forest-labs/flux.2-pro` | ✅ | ❌ | ✅ | 纯文生图，不支持图片输入 |
| `google/gemini-3.1-flash-image-preview` | ✅ | ✅ | ❌ | 地区限制(403) |
| `openai/gpt-5-image-mini` | ✅ | ✅ | ❌ | 地区限制(403) |
| `bytedance-seed/seedream-4.5` | ? | ? | ❌ | Chat Completions 端点不支持(404) |

## API 调用格式

### Grok Imagine 图生图（传参考图编辑）

```bash
# 1. 图片转 base64
IMG_B64=$(base64 -w0 photo.jpg)

# 2. 构建 payload（注意：用 modalities: ["image"]，不是 ["image", "text"]）
cat > /tmp/payload.json << EOF
{
  "model": "x-ai/grok-imagine-image-quality",
  "modalities": ["image"],
  "messages": [{
    "role": "user",
    "content": [
      {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,${IMG_B64}"}},
      {"type": "text", "text": "Edit: navy suit, white shirt, purple tie, gold glasses, white background, keep face"}
    ]
  }]
}
EOF

# 3. 调用 API
curl -s "https://openrouter.ai/api/v1/chat/completions" \
  -H "Authorization: Bearer ${OPENROUTER_API_KEY}" \
  -H "Content-Type: application/json" \
  -d @/tmp/payload.json --max-time 90

# 4. 解析响应：图片在 choices[0].message.images[0].image_url.url (base64 data URL)
```

### FLUX 文生图

```bash
# 同 Chat Completions 端点，modalities: ["image"]，不支持图片输入
# messages 中只需 text content
```

## 关键 Pitfalls

1. **modalities 只用 `["image"]`**：Grok Imagine 用 `["image", "text"]` 会报 404 "No endpoints found"
2. **响应结构特殊**：图片在 `choices[0].message.images[]` 而不是 `content[]`，每个 image 的 url 是 base64 data URL
3. **API key 获取**：不要用 `source .env && python3`（子进程拿不到 key）。直接用 bash：`KEY=$(grep OPENROUTER .env | cut -d= -f2)`
4. **超时设置**：生成一张图约 30-60 秒，curl 设置 `--max-time 90`
5. **图片大小**：base64 编码后约 100-150KB，写入临时 JSON 文件避免命令行参数过长
6. **输出格式**：Grok 输出 PNG，约 150-250KB，`880x1168` 或类似竖版尺寸
