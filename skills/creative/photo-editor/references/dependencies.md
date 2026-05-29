# Photo Editor Dependencies

## Required Packages

```bash
pip3 install Pillow rembg opencv-python-headless numpy
```

On Chinese servers where pypi.org times out, use the Tsinghua mirror:

```bash
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple Pillow rembg opencv-python-headless numpy
```

Use `background=true, notify_on_complete=true` for long installs — `rembg` pulls
u2net model weights (~176MB) on first use, which can take 30-60 seconds.

## Package Roles

| Package | Used For |
|---------|----------|
| Pillow | Core image I/O, resize, crop, rotate, text overlay, filters |
| rembg | AI background removal (u2net model) |
| opencv-python-headless | Advanced filters, inpaint, color manipulations |
| numpy | Array operations backing OpenCV/scikit-image |

## Verification

```bash
python3 -c "from PIL import Image; print('Pillow:', Image.__version__)"
python3 -c "import rembg; print('rembg:', rembg.__version__)"
python3 -c "import cv2; print('OpenCV:', cv2.__version__)"
python3 -c "import numpy; print('numpy:', numpy.__version__)"
```

## Script Reference

`scripts/edit.py` handles all operations. CLI:

```
python3 scripts/edit.py <action> [args...]

Actions: remove-bg, change-bg, resize, crop, rotate, filter, text, collage, compress, convert, info
```

The script auto-detects available packages and degrades gracefully (e.g., 
filters still work with just Pillow if OpenCV is missing).
