#!/usr/bin/env python3
"""
AI Photo Editor — Hermes P图 Skill
Usage: python3 edit.py <action> [args...]
"""
import argparse
import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont, ImageOps
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
    print("⚠️ Pillow not installed. Run: pip install Pillow", file=sys.stderr)

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

try:
    from rembg import remove
    HAS_REMBG = True
except ImportError:
    HAS_REMBG = False


def ensure_output(path: str) -> str:
    """Ensure output directory exists, return resolved path."""
    p = Path(path).resolve()
    p.parent.mkdir(parents=True, exist_ok=True)
    return str(p)


def load_image(path: str) -> Image.Image:
    """Load image with Pillow."""
    img = Image.open(path)
    if img.mode != "RGB" and img.mode != "RGBA":
        img = img.convert("RGB")
    return img


def save_image(img: Image.Image, path: str, quality: int = 95):
    """Save image, auto-handle format."""
    path = ensure_output(path)
    ext = Path(path).suffix.lower()
    
    save_kwargs = {}
    if ext in (".jpg", ".jpeg"):
        if img.mode == "RGBA":
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            img = bg
        save_kwargs["quality"] = quality
    elif ext == ".png":
        save_kwargs["optimize"] = True
    
    img.save(path, **save_kwargs)
    print(f"✅ Saved: {path}")


# ===== Actions =====

def remove_bg(input_path: str, output_path: str):
    """AI background removal."""
    if not HAS_REMBG:
        print("❌ rembg not installed. Run: pip install rembg")
        sys.exit(1)
    
    print("🔄 Removing background (AI model)...")
    with open(input_path, "rb") as f:
        input_bytes = f.read()
    
    output_bytes = remove(input_bytes)
    
    output_path = ensure_output(output_path)
    with open(output_path, "wb") as f:
        f.write(output_bytes)
    
    print(f"✅ Background removed: {output_path}")


def change_bg(input_path: str, output_path: str, color: str = "white", blur: bool = False):
    """Remove background and replace with solid color or blur."""
    if not HAS_REMBG:
        print("❌ rembg not installed.")
        sys.exit(1)
    
    print("🔄 Removing background...")
    with open(input_path, "rb") as f:
        input_bytes = f.read()
    
    no_bg_bytes = remove(input_bytes)
    
    # Load as RGBA
    import io
    fg = Image.open(io.BytesIO(no_bg_bytes)).convert("RGBA")
    bg = Image.new("RGBA", fg.size, (0, 0, 0, 0))
    
    color_map = {
        "white": (255, 255, 255, 255),
        "black": (0, 0, 0, 255),
        "red": (255, 0, 0, 255),
        "blue": (0, 0, 255, 255),
        "green": (0, 255, 0, 255),
        "gray": (128, 128, 128, 255),
    }
    
    if color in color_map:
        bg = Image.new("RGBA", fg.size, color_map[color])
    elif color.startswith("#") and len(color) == 7:
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        bg = Image.new("RGBA", fg.size, (r, g, b, 255))
    else:
        bg = Image.new("RGBA", fg.size, color_map.get("white", (255, 255, 255, 255)))
    
    bg.paste(fg, (0, 0), fg)
    result = bg.convert("RGB")
    save_image(result, output_path)
    print(f"✅ Background replaced with {color}")


def resize(input_path: str, output_path: str, width: int = None, height: int = None, scale: float = None):
    """Resize image."""
    img = load_image(input_path)
    w, h = img.size
    
    if scale:
        new_w, new_h = int(w * scale), int(h * scale)
    elif width and height:
        new_w, new_h = width, height
    elif width:
        ratio = width / w
        new_w, new_h = width, int(h * ratio)
    elif height:
        ratio = height / h
        new_w, new_h = int(w * ratio), height
    else:
        print("❌ Must specify width, height, or scale")
        sys.exit(1)
    
    img = img.resize((new_w, new_h), Image.LANCZOS)
    save_image(img, output_path)
    print(f"✅ Resized: {w}x{h} → {new_w}x{new_h}")


def crop(input_path: str, output_path: str, left: int, top: int, right: int, bottom: int):
    """Crop image."""
    img = load_image(input_path)
    img = img.crop((left, top, right, bottom))
    save_image(img, output_path)
    print(f"✅ Cropped to ({left},{top},{right},{bottom})")


def rotate(input_path: str, output_path: str, degrees: float):
    """Rotate image."""
    img = load_image(input_path)
    img = img.rotate(degrees, expand=True, resample=Image.BICUBIC)
    save_image(img, output_path)
    print(f"✅ Rotated {degrees}°")


def apply_filter(input_path: str, output_path: str, filter_type: str, amount: float = 1.0):
    """Apply artistic filters."""
    img = load_image(input_path)
    
    if filter_type == "grayscale" or filter_type == "黑白":
        img = ImageOps.grayscale(img)
    elif filter_type == "sepia" or filter_type == "复古":
        gray = ImageOps.grayscale(img)
        # Sepia effect
        img = Image.merge("RGB", (
            gray.point(lambda x: min(255, x * 1.2)),
            gray.point(lambda x: min(255, x * 0.95)),
            gray.point(lambda x: min(255, x * 0.7)),
        ))
    elif filter_type == "blur" or filter_type == "模糊":
        img = img.filter(ImageFilter.GaussianBlur(radius=amount * 5))
    elif filter_type == "sharpen" or filter_type == "锐化":
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(amount * 2)
    elif filter_type == "brighten" or filter_type == "提亮":
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.0 + amount)
    elif filter_type == "contrast" or filter_type == "对比度":
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.0 + amount)
    elif filter_type == "vintage" or filter_type == "胶片":
        # Warm, slightly faded look
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(0.7)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.1)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(0.8)
    elif filter_type == "cool" or filter_type == "冷色调":
        r, g, b = img.split()
        b = b.point(lambda x: min(255, x * 1.1))
        img = Image.merge("RGB", (r, g, b))
    elif filter_type == "warm" or filter_type == "暖色调":
        r, g, b = img.split()
        r = r.point(lambda x: min(255, x * 1.1))
        g = g.point(lambda x: min(255, x * 1.05))
        img = Image.merge("RGB", (r, g, b))
    else:
        print(f"❌ Unknown filter: {filter_type}")
        print("Available: grayscale, sepia, blur, sharpen, brighten, contrast, vintage, cool, warm")
        sys.exit(1)
    
    save_image(img, output_path)
    print(f"✅ Filter '{filter_type}' applied")


def add_text(input_path: str, output_path: str, text: str, 
             position: str = "bottom-right", font_size: int = 36,
             color: str = "white", opacity: float = 1.0,
             shadow: bool = False):
    """Add text overlay."""
    img = load_image(input_path).convert("RGBA")
    
    # Create text layer
    txt_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(txt_layer)
    
    # Font
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except (IOError, OSError):
        try:
            # Try common Chinese font paths
            for fp in [
                "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
                "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                "/System/Library/Fonts/PingFang.ttc",
            ]:
                if os.path.exists(fp):
                    font = ImageFont.truetype(fp, font_size)
                    break
            else:
                font = ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()
    
    # Parse color
    if color == "white":
        rgb = (255, 255, 255)
    elif color == "black":
        rgb = (0, 0, 0)
    elif color == "red":
        rgb = (255, 0, 0)
    elif color.startswith("#") and len(color) == 7:
        rgb = (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16))
    else:
        rgb = (255, 255, 255)
    
    rgba = rgb + (int(255 * opacity),)
    
    # Text size
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    margin = 20
    iw, ih = img.size
    
    # Position
    pos_map = {
        "top-left": (margin, margin),
        "top-center": ((iw - tw) // 2, margin),
        "top-right": (iw - tw - margin, margin),
        "center": ((iw - tw) // 2, (ih - th) // 2),
        "bottom-left": (margin, ih - th - margin),
        "bottom-center": ((iw - tw) // 2, ih - th - margin),
        "bottom-right": (iw - tw - margin, ih - th - margin),
    }
    x, y = pos_map.get(position, pos_map["bottom-right"])
    
    if shadow:
        draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0, int(128 * opacity)))
    
    draw.text((x, y), text, font=font, fill=rgba)
    
    result = Image.alpha_composite(img, txt_layer)
    save_image(result, output_path)
    print(f"✅ Text added: '{text}'")


def collage(input_paths: list, output_path: str, direction: str = "horizontal", 
            spacing: int = 10, bg_color: str = "white"):
    """Combine multiple images into a collage."""
    images = [load_image(p) for p in input_paths]
    
    if direction == "horizontal":
        max_h = max(img.size[1] for img in images)
        total_w = sum(img.size[0] for img in images) + spacing * (len(images) - 1)
        
        canvas = Image.new("RGB", (total_w, max_h), bg_color)
        x = 0
        for img in images:
            y = (max_h - img.size[1]) // 2
            canvas.paste(img, (x, y))
            x += img.size[0] + spacing
    
    elif direction == "vertical":
        max_w = max(img.size[0] for img in images)
        total_h = sum(img.size[1] for img in images) + spacing * (len(images) - 1)
        
        canvas = Image.new("RGB", (max_w, total_h), bg_color)
        y = 0
        for img in images:
            x = (max_w - img.size[0]) // 2
            canvas.paste(img, (x, y))
            y += img.size[1] + spacing
    
    elif direction == "grid":
        cols = int(len(images) ** 0.5)
        rows = (len(images) + cols - 1) // cols
        
        cell_w = max(img.size[0] for img in images)
        cell_h = max(img.size[1] for img in images)
        
        total_w = cell_w * cols + spacing * (cols - 1)
        total_h = cell_h * rows + spacing * (rows - 1)
        
        canvas = Image.new("RGB", (total_w, total_h), bg_color)
        for i, img in enumerate(images):
            row, col = i // cols, i % cols
            x = col * (cell_w + spacing) + (cell_w - img.size[0]) // 2
            y = row * (cell_h + spacing) + (cell_h - img.size[1]) // 2
            canvas.paste(img, (x, y))
    
    save_image(canvas, output_path)
    print(f"✅ Collage created: {len(images)} images → {direction}")


def compress(input_path: str, output_path: str, quality: int = 85, max_width: int = None):
    """Compress and optionally resize image."""
    img = load_image(input_path)
    
    if max_width and img.size[0] > max_width:
        ratio = max_width / img.size[0]
        new_h = int(img.size[1] * ratio)
        img = img.resize((max_width, new_h), Image.LANCZOS)
        print(f"   Resized to {max_width}x{new_h}")
    
    orig_size = os.path.getsize(input_path)
    save_image(img, output_path, quality=quality)
    new_size = os.path.getsize(output_path)
    
    reduction = (1 - new_size / orig_size) * 100
    print(f"✅ Compressed: {orig_size//1024}KB → {new_size//1024}KB ({reduction:.1f}% smaller)")


def convert(input_path: str, output_path: str):
    """Convert image format."""
    img = load_image(input_path)
    save_image(img, output_path)
    print(f"✅ Converted to {Path(output_path).suffix}")


def info(input_path: str):
    """Show image info."""
    img = Image.open(input_path)
    w, h = img.size
    mode = img.mode
    size_kb = os.path.getsize(input_path) // 1024
    print(f"📷 {input_path}")
    print(f"   Size: {w}x{h} | Mode: {mode} | File: {size_kb}KB")
    print(f"   Format: {img.format}")


# ===== CLI =====

def main():
    parser = argparse.ArgumentParser(description="AI Photo Editor")
    sub = parser.add_subparsers(dest="action")
    
    # remove-bg
    p = sub.add_parser("remove-bg", help="AI remove background")
    p.add_argument("input")
    p.add_argument("output")
    
    # change-bg
    p = sub.add_parser("change-bg", help="Remove bg and replace with color")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--color", default="white")
    
    # resize
    p = sub.add_parser("resize", help="Resize image")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--width", type=int)
    p.add_argument("--height", type=int)
    p.add_argument("--scale", type=float)
    
    # crop
    p = sub.add_parser("crop", help="Crop image")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--left", type=int, required=True)
    p.add_argument("--top", type=int, required=True)
    p.add_argument("--right", type=int, required=True)
    p.add_argument("--bottom", type=int, required=True)
    
    # rotate
    p = sub.add_parser("rotate", help="Rotate image")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--degrees", type=float, required=True)
    
    # filter
    p = sub.add_parser("filter", help="Apply filter")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--type", required=True)
    p.add_argument("--amount", type=float, default=1.0)
    
    # text
    p = sub.add_parser("text", help="Add text overlay")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--text", required=True)
    p.add_argument("--position", default="bottom-right")
    p.add_argument("--font-size", type=int, default=36)
    p.add_argument("--color", default="white")
    p.add_argument("--opacity", type=float, default=1.0)
    p.add_argument("--shadow", action="store_true")
    
    # collage
    p = sub.add_parser("collage", help="Combine images")
    p.add_argument("inputs", nargs="+")
    p.add_argument("output")
    p.add_argument("--direction", default="horizontal")
    p.add_argument("--spacing", type=int, default=10)
    p.add_argument("--bg-color", default="white")
    
    # compress
    p = sub.add_parser("compress", help="Compress image")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--quality", type=int, default=85)
    p.add_argument("--max-width", type=int)
    
    # convert
    p = sub.add_parser("convert", help="Convert format")
    p.add_argument("input")
    p.add_argument("output")
    
    # info
    p = sub.add_parser("info", help="Show image info")
    p.add_argument("input")
    
    args = parser.parse_args()
    
    if not args.action:
        parser.print_help()
        sys.exit(1)
    
    action_map = {
        "remove-bg": lambda: remove_bg(args.input, args.output),
        "change-bg": lambda: change_bg(args.input, args.output, args.color),
        "resize": lambda: resize(args.input, args.output, args.width, args.height, args.scale),
        "crop": lambda: crop(args.input, args.output, args.left, args.top, args.right, args.bottom),
        "rotate": lambda: rotate(args.input, args.output, args.degrees),
        "filter": lambda: apply_filter(args.input, args.output, args.type, args.amount),
        "text": lambda: add_text(args.input, args.output, args.text, args.position, args.font_size, args.color, args.opacity, args.shadow),
        "collage": lambda: collage(args.inputs, args.output, args.direction, args.spacing, args.bg_color),
        "compress": lambda: compress(args.input, args.output, args.quality, args.max_width),
        "convert": lambda: convert(args.input, args.output),
        "info": lambda: info(args.input),
    }
    
    action_map[args.action]()


if __name__ == "__main__":
    main()
