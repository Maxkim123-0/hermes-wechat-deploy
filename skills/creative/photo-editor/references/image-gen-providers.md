# 图片生成能力速查

罗列当前可用的图片生成/编辑 API，按能力分层。

## 能力对比

| 能力 | CogView-3 | 万相 wan2.6 | ComfyUI 本地 | ComfyUI Cloud |
|------|:---------:|:----------:|:-----------:|:------------:|
| 文生图 | ✅ | ✅ | ✅ | ✅ |
| 参考图输入 | ❌ | ✅ | ✅ | ✅ |
| 面部精修 | ❌ | ✅ 人像美化 | ✅ | ✅ |
| 换装/换背景 | ❌ | ✅ 图像编辑 | ✅ | ✅ |
| 文字叠加 | ❌ | ❌ | ❌ | ❌ |
| 费用 | 免费 | 免费 tier | 免费(需GPU) | 付费 |

## 阿里通义万相 (推荐)

**场景**：需要参考用户照片做编辑（换装、换背景、美化）。

- **API Key**: `DASHSCOPE_API_KEY`（注册 dashscope.aliyun.com 获取）
- **端点**: `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
- **模型**: `wan2.6-image`（图像编辑）, `wan2.6-t2i`（文生图）
- **关键能力**: 
  - `messages` 中可传 `image` 字段作为参考图
  - 支持人像美化、风格迁移、局部重绘
- **限制**: 无文字叠加能力，出图后需 Pillow/HTML 叠加文字

### 调用示例

```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "wan2.6-image",
    "input": {
      "messages": [{
        "role": "user",
        "content": [
          {"text": "参考图中的人物，换成深蓝色西装、白色衬衫、深紫色领带，纯白背景，专业商务照风格"},
          {"image": "https://example.com/photo.jpg"}
        ]
      }]
    },
    "parameters": {
      "prompt_extend": true,
      "watermark": false,
      "n": 1,
      "size": "1280*1280"
    }
  }'
```

## 智谱 CogView-3-Flash

**场景**：纯文生图，无需参考照片。

- **API Key**: `ZAI_API_KEY`（已配置）
- **端点**: `POST https://open.bigmodel.cn/api/paas/v4/images/generations`
- **模型**: `cogview-3-flash`
- **关键限制**: 不支持参考图输入，无法基于用户照片生成
- **适合**: Logo、海报、场景图等"凭空画"的场景

## ComfyUI

- **本地**: 需要 NVIDIA GPU ≥6GB VRAM。当前服务器无 GPU，不可用。
- **Cloud**: 需要付费订阅。免费 tier 只读，不可执行。

## 文字叠加方案

上述生图 API 都不支持文字排版。出图后用以下方式叠加：

1. **HTML → 4K PNG**: 最高质量，适合复杂排版（文字+logo+渐变背景）
2. **Pillow**: 简单场景（加几行字、水印），比 HTML 方案快
3. **photo-editor scripts/edit.py**: 批量文字叠加
