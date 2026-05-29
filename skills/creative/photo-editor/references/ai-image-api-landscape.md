# AI 图像生成/编辑 API 能力图谱

> 2026-05 实战整理。区分文生图和参考图编辑两大能力。

## 核心结论

**有参考图编辑能力的免费 API 极少。** 大部分免费生图 API 只做文生图。

## API 对比

| 服务 | API Key | 文生图 | 参考图编辑 | 费用 | 备注 |
|------|---------|:---:|:---:|------|------|
| 智谱 CogView-3-Flash | ZAI_API_KEY | ✅ | ❌ | 免费 | 速度快，质量一般 |
| 智谱 CogView-4 | ZAI_API_KEY | ✅ | ❌ | 付费 | 质量好，支持汉字，有水印 |
| 智谱 GLM-Image | ZAI_API_KEY | ✅ | ❌ | 付费 | 最高质量，~20s/张 |
| 阿里通义万相 wan2.6-t2i | DASHSCOPE_API_KEY | ✅ | ❌ | 免费额度 | 分辨率灵活 |
| 阿里通义万相 wan2.6-image | DASHSCOPE_API_KEY | ❌ | ✅ | 免费额度 | **支持多参考图编辑** |
| 阿里 Qwen-Image-Edit | DASHSCOPE_API_KEY | ❌ | ✅ | 免费额度 | **最强编辑，换装/换背景** |
| HuggingFace Qwen-Image-Edit | HF_TOKEN | — | ✅ | 付费推理 | 网页版免费试用 |
| deAPI.ai | DEAPI_KEY | ✅ | ✅ | $5 免费额度 | 聚合多个模型 |

## 智谱 API 调用示例 (CogView-4)

```bash
curl -s "https://open.bigmodel.cn/api/paas/v4/images/generations" \
  -H "Authorization: Bearer $ZAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "cogview-4",
    "prompt": "Professional corporate headshot...",
    "size": "1024x1344",
    "quality": "hd"
  }'
# 返回: {"data":[{"url":"https://..."}]}
# 图片临时链接有效期30天，需及时转存
# 注意：CogView-4 会自动加水印（"AI生成"在右下角）
```

## 阿里万相图像编辑示例 (Qwen-Image-Edit)

```bash
curl -s "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-image-2.0-pro",
    "input": {
      "messages": [{
        "role": "user",
        "content": [
          {"image": "https://你的参考图URL"},
          {"text": "给这个人换上深蓝色西装，白色衬衫，紫色领带，加金框眼镜，纯白背景"}
        ]
      }]
    },
    "parameters": {"n": 1, "watermark": false, "size": "2048*2048"}
  }'
```

## 关键教训

1. **文生图 ≠ 参考图编辑**。CogView 只能凭空画，没法照着照片改。
2. **需要参考图编辑 → 阿里万相/Qwen-Image-Edit 是唯一免费方案**。
3. **智谱 CogView-4 可以应急**生成通用商务人像，排版/风格能对齐，但人脸不是用户。
4. **DashScope 免费额度充足**，新用户注册即可用。
5. 图片 URL 有效期通常 30 天，产出后及时下载转存。
