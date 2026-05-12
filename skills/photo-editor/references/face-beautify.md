# 基础面部美化方案

> ⚠️ 仅限基础磨皮+美白+轻微瘦脸。精细面部精修（瘦脸针级别）请用豆包/美图秀秀。

## 可用技术栈

| 技术 | 效果 | 局限 |
|------|------|------|
| Haar Cascade | 检测人脸矩形框 | 只有 x,y,w,h，无线索点 |
| 双边滤波 (bilateralFilter) | 磨皮去噪，保留边缘 | 参数不好会假面感 |
| LAB 颜色空间提亮 L 通道 | 美白自然 | 过度提亮会惨白 |
| 简单水平 resize | 轻微瘦脸 | 没有局部变形，一刀切 |

## 工作流程

```python
# 1. 人脸检测
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
faces = face_cascade.detectMultiScale(gray, 1.1, 5)

# 2. 提取面部区域（加 margin 用于羽化）
margin = int(fw * 0.3)
face_region = img[y-margin:y+fh+margin, x-margin:x+fw+margin]

# 3. 磨皮（双边滤波）
smoothed = cv2.bilateralFilter(face_region, d=9, sigmaColor=75, sigmaSpace=75)

# 4. 美白（LAB L 通道提亮）
lab = cv2.cvtColor(smoothed, cv2.COLOR_BGR2LAB)
l, a, b = cv2.split(lab)
l = cv2.add(l, 20)  # 提亮 20
l = np.clip(l, 0, 255).astype(np.uint8)
whitened_lab = cv2.merge([l, a, b])
whitened = cv2.cvtColor(whitened_lab, cv2.COLOR_LAB2BGR)

# 5. 瘦脸（简单宽度压缩）
slim_factor = 0.92  # 92% 宽度
slimmed = cv2.resize(whitened, (int(rw*0.92), rh))
# 补回原尺寸 + 羽化 mask 混合
```

## 参数调优

| 需求 | 调整 |
|------|------|
| 更白 | `cv2.add(l, 30)` 或更高 |
| 更小脸 | `slim_factor = 0.88` 或更低 |
| 更磨皮 | `sigmaColor=100, sigmaSpace=100`（但会丢细节） |
| 更自然 | `sigmaColor=50, sigmaSpace=50` + 降低 margin |

## 完整脚本

见 `scripts/edit.py` 中的 `remove_bg` → `beautify_face` 相关逻辑。
本方案已在实际会话中测试通过（1280×1707 照片，检测到左侧人脸，处理时间 <5 秒）。

## 为什么不如豆包

豆包/美图秀秀用的是 **dlib 68 点模型** 或 **mediapipe Face Mesh (468 点)**：
- 瘦脸：基于下巴轮廓点的局部 warp，不缩五官
- 大眼：基于眼部 12 点的局部放大
- 美妆：精确的唇部/眉毛区域上色

Hermes 没有内置这些模型，需要 `pip install dlib`（编译复杂）或 `mediapipe`（可能不兼容）。不建议为了修图强行装。
