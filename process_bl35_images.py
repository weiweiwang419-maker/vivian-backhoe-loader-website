"""
Process BL35-12 images: color correction + resize
"""
from PIL import Image, ImageEnhance, ImageFilter
import os

SOURCE_DIR = '/Users/vivianwang/WorkBuddy/2026-07-01-16-58-56/vivian_website/images/products/source/bl35-12'
OUTPUT_DIR = '/Users/vivianwang/WorkBuddy/2026-07-01-16-58-56/vivian_website/images/products'
TARGET_LONG_EDGE = 1600
QUALITY = 85

mapping = [
    ('bl35-12-1-original.jpg', 'bl35-12-front.jpg'),
    ('bl35-12-2-original.jpg', 'bl35-12-2.jpg'),
    ('bl35-12-3-original.jpg', 'bl35-12-3.jpg'),
    ('bl35-12-4-original.jpg', 'bl35-12-4.jpg'),
    ('bl35-12-5-original.jpg', 'bl35-12-5.jpg'),
]

def process_image(input_path, output_path):
    img = Image.open(input_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    w, h = img.size
    if max(w, h) > TARGET_LONG_EDGE:
        if w >= h:
            new_w = TARGET_LONG_EDGE
            new_h = int(h * TARGET_LONG_EDGE / w)
        else:
            new_h = TARGET_LONG_EDGE
            new_w = int(w * TARGET_LONG_EDGE / h)
        img = img.resize((new_w, new_h), Image.LANCZOS)
    img = ImageEnhance.Color(img).enhance(0.90)
    img = ImageEnhance.Contrast(img).enhance(1.15)
    img = ImageEnhance.Brightness(img).enhance(1.05)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=80, threshold=2))
    img.save(output_path, 'JPEG', quality=QUALITY, optimize=True)
    size_kb = os.path.getsize(output_path) / 1024
    print(f'  {os.path.basename(output_path)}: {img.size[0]}x{img.size[1]}, {size_kb:.0f} KB')

print('Processing BL35-12 images...')
for src_name, dst_name in mapping:
    src_path = os.path.join(SOURCE_DIR, src_name)
    dst_path = os.path.join(OUTPUT_DIR, dst_name)
    process_image(src_path, dst_path)
print('Done!')
