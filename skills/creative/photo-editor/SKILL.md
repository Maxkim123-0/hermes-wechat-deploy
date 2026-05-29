---
name: photo-editor
description: "AI-powered photo editing: background removal, filters, text overlay, collage, resize/compress. Exceeds Doubao P图 capabilities."
triggers:
  - P图
  - 修图
  - 改图
  - 抠图
  - 去背景
  - 换背景
  - 加文字
  - 水印
  - 拼图
  - 滤镜
  - 调色
  - 压缩图片
---

# AI 修图技能

> 底层能力远超豆包 — AI 抠图、智能修图、批量处理

## 快速使用

```
给我修图：[描述要做什么] + 图片路径
```

## 能力清单

| 功能 | 实现 | 状态 |
|------|------|:---:|
| 🎯 AI 抠图 | rembg (u2net) | ✅ |
| ✂️ 裁剪/旋转/缩放 | Pillow | ✅ |
| 🎨 滤镜 (灰阶/复古/锐化) | OpenCV + Pillow | ✅ |
| 📝 文字叠加 | Pillow | ✅ |
| 🖼️ 拼图/拼接 | Pillow | ✅ |
| 📦 批量处理 | Python 脚本 | ✅ |
| 🔧 格式转换/压缩 | Pillow | ✅ |
| 🧹 去水印/消除物体 | OpenCV inpaint | ✅ |
| 🤖 AI 人像生成/换装 | OpenRouter + Grok Imagine | ✅ NEW |
| 😊 传统面部精修(瘦脸/大眼) | — | ⚠️ 不推荐 |
| 🎨 AI 文生图 | OpenRouter+FLUX 或 CogView-4 | ✅ |
| 😊 面部精修 | — | ⚠️ 不推荐 |
| 🤖 AI 生图/换装/编辑 | 外部 API | ⚠️ 见 `references/ai-image-api-landscape.md` |

## ⚠️ 面部精修/AI 人像生成

**传统面部精修（瘦脸/大眼/美妆）仍不推荐**，但 AI 人像生成/换装已有可用方案：

### 方案 A：OpenRouter + xAI Grok Imagine（推荐，已实战验证）
- 传参考图 + 文字指令，直接生成编辑后的商务头像
- 模型：`x-ai/grok-imagine-image-quality`
- API：标准 Chat Completions，`modalities: ["image"]`
- 不锁区，现有 OpenRouter key 即可
- 支持：换装、加眼镜、换背景、保持人脸特征
- 详见 `references/openrouter-image-gen.md`

### 方案 B：CogView-4（智谱，仅文生图）
- 不支持传参考图，只能凭空生成通用人像
- 适合不需要像本人的场景

### 方案 C：阿里万相 / 豆包 Seedream（需新 key）
- 支持参考图编辑，能力更强
- 但需要单独注册 API key

我能做的传统修图：抠图、裁剪、滤镜、加文字、拼图。

## 🆕 AI 人像编辑（OpenRouter + xAI Grok）

**通过 OpenRouter 调用 xAI Grok Imagine 可实现 AI 人像编辑**，包括换装、换背景、加眼镜等：

| 能力 | 实现 | 状态 |
|------|------|:---:|
| AI 换装/换背景/加配饰 | OpenRouter + Grok Imagine | ✅ |
| 文生图 | OpenRouter + FLUX.2 Pro 或 智谱 CogView-4 | ✅ |

### 调用方式

```python
# 核心：通过 OpenRouter Chat Completions API
payload = {
    "model": "x-ai/grok-imagine-image-quality",
    "modalities": ["image"],  # 只输出图片
    "messages": [{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}},
            {"type": "text", "text": "编辑指令..."}
        ]
    }]
}
# 结果在 response.choices[0].message.images[]
```

### 关键踩坑

- **必须用文件传参**：大 base64（>100KB）会导致 shell "Argument list too long"，用 `-d @/tmp/payload.json`
- **modalities 只用 ["image"]**：`["image","text"]` 对 Grok 会 404
- **图片在 message.images**：不是 message.content
- **Google/OpenAI 图片模型锁区**：不要用 gemini-*-image 或 gpt-*-image
- **适用模型**：`x-ai/grok-imagine-image-quality`, `black-forest-labs/flux.2-pro`

### 替代方案（按推荐顺序）

| 方案 | 适用场景 | 费用 |
|------|---------|------|
| **阿里通义万相 (wan2.6-image)** | 参考图编辑、换装、换背景、人像美化 | 免费 tier |
| 智谱 CogView-3-Flash | 纯文生图（无法参考照片） | 免费 tier |
| 豆包/美图秀秀 App | 面部精修、美颜 | 免费 |

> **万相是最佳 API 方案**：支持图像编辑模式，可传用户照片作参考图，修改服装/背景/发型。API 走 DashScope，新用户有免费额度。详见 `references/image-gen-providers.md`。

## 使用示例

### 1. AI 抠图
```
帮我把这张图的背景去掉，保存为 PNG
```

### 2. 换背景
```
把这张人像的背景换成白色/蓝色/渐变色
```

### 3. 加文字
```
在这张图右下角加文字，白色半透明
```

### 4. 拼图
```
把这三张图横排拼接在一起，间距 20px
```

### 5. 批量处理
```
把 /photos/ 下所有 jpg 压缩到 800px 宽
```

### 6. 滤镜
```
给这张图加复古胶片滤镜 / 黑白 / 模糊背景
```

## ⚠️ 能力边界

**面部精修（瘦脸/大眼/美妆）不是强项。** 当前依赖 OpenCV Haar 级联检测（精度低），缺少 dlib/mediapipe 人脸关键点检测模型。瘦脸/美白效果粗糙，不如豆包/美图秀秀。遇到这类需求直接告知用户：「P脸找豆包，搞技术找我」。

**拿手的：** 抠图、裁剪、滤镜、加字、拼图、压缩 — 这些用 Pillow + rembg + OpenCV 效果稳定。
