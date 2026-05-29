# HTML → WeChat 图片生成流水线

在不能直接用 vision API 的模型上，通过 HTML + 浏览器截图生成可交付的图片。

## 适用场景

- 生成闲鱼/小红书封面图
- 需要纯文字 + 设计感的海报
- 无图片编辑工具时的替代方案

## 完整流水线

### 1. 写 HTML

```html
<!DOCTYPE html>
<html lang="zh">
<head><meta charset="UTF-8"><meta name="viewport" content="width=800">
<style>
body {
  width: 800px; height: 800px;           /* 正方形封面 */
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  font-family: 'PingFang SC', sans-serif;
  background: linear-gradient(135deg, #0f0f23, #1a1a3e);
  color: #00d4ff;
}
.title { font-size: 56px; font-weight: 900; }
</style></head>
<body>
  <div class="title">标题文字</div>
  <div class="sub">副标题</div>
</body></html>
```

### 2. 启动本地 HTTP 服务器

```bash
cd /path/to/html/dir
python3 -m http.server 8899 &
```

### 3. 浏览器截图

```python
browser_navigate(url="http://localhost:8899/cover.html")
browser_vision(question="screenshot")
```

**关键**: `browser_vision` 即使 vision analysis 失败（非 vision 模型），截图文件仍会保存到：
```
~/.hermes/profiles/<profile>/cache/screenshots/browser_screenshot_<uuid>.png
```

error 消息中会给出 `screenshot_path`，直接用 MEDIA 标签发送。

### 4. 交付

```markdown
MEDIA:/path/to/screenshot.png
```

## 注意事项

- HTML 必须自包含（inline CSS），不依赖外部资源
- 中文字体用 `'PingFang SC', 'Noto Sans CJK', sans-serif` 确保渲染
- 使用 `width=800` viewport 保证截图尺寸一致
- `browser_vision` 失败是正常的，截图仍然可用
- 本地 HTTP server 用完后可以 kill
