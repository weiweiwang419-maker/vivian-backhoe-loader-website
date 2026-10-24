"""
Process BL85-25 images (same pipeline as process_bl80_images.py):
- Resize to 1600px wide
- Desaturate slightly (remove yellow/orange cast)
- Contrast +1.08, Brightness +1.05, Unsharp mask
- Save as bl85-25-{front,2,3,4,5}.jpg in images/products/
Also build og-product-bl85-25.jpg (1200x630 crop from hero).
"""
from PIL import Image, ImageEnhance, ImageFilter
import os

SOURCE_DIR = 'images/products/source/bl85-25'
OUTPUT_DIR = 'images/products'

sources = [
    ('bl85-25-1-original.jpg', 'bl85-25-front.jpg'),  # front-left 45° — hero
    ('bl85-25-2-original.jpg', 'bl85-25-2.jpg'),      # rear 3/4, backhoe extended
    ('bl85-25-3-original.jpg', 'bl85-25-3.jpg'),      # left side profile
    ('bl85-25-4-original.jpg', 'bl85-25-4.jpg'),      # straight front — loader bucket
    ('bl85-25-5-original.jpg', 'bl85-25-5.jpg'),      # straight rear — factory behind
]

TARGET_WIDTH = 1600

def enhance(img):
    img = ImageEnhance.Color(img).enhance(0.88)
    img = ImageEnhance.Contrast(img).enhance(1.08)
    img = ImageEnhance.Brightness(img).enhance(1.05)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=110, threshold=2))
    return img

hero = None
for src_name, out_name in sources:
    img = Image.open(os.path.join(SOURCE_DIR, src_name)).convert('RGB')
    w, h = img.size
    if w > TARGET_WIDTH:
        img = img.resize((TARGET_WIDTH, int(h * TARGET_WIDTH / w)), Image.LANCZOS)
    img = enhance(img)
    out_path = os.path.join(OUTPUT_DIR, out_name)
    img.save(out_path, 'JPEG', quality=88, optimize=True, progressive=True)
    print(f"{src_name} {w}x{h} -> {out_name} {img.size[0]}x{img.size[1]} ({os.path.getsize(out_path)/1024:.0f} KB)")
    if out_name == 'bl85-25-front.jpg':
        hero = img.copy()

# OG image 1200x630 from hero
hw, hh = hero.size            # 1600 x 1200
crop_h = int(1200 / (1200/630))  # = 630 at width 1200
og = hero.resize((1200, int(hh * 1200 / hw)), Image.LANCZOS)  # 1200x900
ow, oh = og.size
top = (oh - 630) // 2
og = og.crop((0, top, 1200, top + 630))
og.save('og-product-bl85-25.jpg', 'JPEG', quality=88, optimize=True, progressive=True)
print(f"og-product-bl85-25.jpg 1200x630 ({os.path.getsize('og-product-bl85-25.jpg')/1024:.0f} KB)")
