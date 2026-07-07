"""
Process BL15-06 images: color-correct, resize, save to images/products/
"""
from PIL import Image, ImageEnhance, ImageFilter
import os

SOURCE_DIR = '/Users/vivianwang/WorkBuddy/2026-07-01-16-58-56/vivian_website/images/products/source/bl15-06'
OUT_DIR = '/Users/vivianwang/WorkBuddy/2026-07-01-16-58-56/vivian_website/images/products'

# 5 images: front, 3/4, side, full-profile, rear-3/4
NAMES = [
    ('bl15-06-1-original.jpg', 'bl15-06-front.jpg', 1600, 1200),  # main hero
    ('bl15-06-2-original.jpg', 'bl15-06-2.jpg', 1200, 900),       # detail
    ('bl15-06-3-original.jpg', 'bl15-06-3.jpg', 1200, 900),       # detail
    ('bl15-06-4-original.jpg', 'bl15-06-4.jpg', 1200, 900),       # detail
    ('bl15-06-5-original.jpg', 'bl15-06-5.jpg', 1200, 900),       # detail
]

def process(src, dst, max_w, max_h):
    img = Image.open(src)
    # Convert to RGB if needed
    if img.mode != 'RGB':
        img = img.convert('RGB')
    # Color correction: desaturate slightly + boost contrast + brighten
    img = ImageEnhance.Color(img).enhance(0.92)
    img = ImageEnhance.Contrast(img).enhance(1.10)
    img = ImageEnhance.Brightness(img).enhance(1.05)
    img = ImageEnhance.Sharpness(img).enhance(1.15)
    # Resize keeping aspect ratio
    img.thumbnail((max_w, max_h), Image.LANCZOS)
    # Save
    img.save(dst, 'JPEG', quality=85, optimize=True)
    print(f'  ✓ {os.path.basename(dst)}: {img.size[0]}x{img.size[1]} ({os.path.getsize(dst)/1024:.0f}KB)')

print('Processing BL15-06 images...')
for src_name, dst_name, w, h in NAMES:
    src = os.path.join(SOURCE_DIR, src_name)
    dst = os.path.join(OUT_DIR, dst_name)
    process(src, dst, w, h)

# Also update the related card image (was bl15-06-1.jpg - but using front.jpg as primary)
# Note: bl15-06-1.jpg was used in some places. Let's make bl15-06-1.jpg same as front.jpg for compatibility
import shutil
shutil.copy(os.path.join(OUT_DIR, 'bl15-06-front.jpg'), os.path.join(OUT_DIR, 'bl15-06-1.jpg'))
print(f'  ✓ bl15-06-1.jpg: copied from front.jpg (related card compatibility)')

print('\n✓ All BL15-06 images processed!')
