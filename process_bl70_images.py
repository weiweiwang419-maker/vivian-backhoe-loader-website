"""
Process BL70-25 images: color correction + resize
"""
from PIL import Image, ImageEnhance, ImageFilter
import os

SOURCE_DIR = '/Users/vivianwang/WorkBuddy/2026-07-01-16-58-56/vivian_website/images/products/source/bl70-25'
OUTPUT_DIR = '/Users/vivianwang/WorkBuddy/2026-07-01-16-58-56/vivian_website/images/products'
TARGET_LONG_EDGE = 1600
QUALITY = 85

# Map source files to output names
mapping = [
    ('bl70-25-1-original.jpg', 'bl70-25-front.jpg'),  # main front view
    ('bl70-25-2-original.jpg', 'bl70-25-2.jpg'),
    ('bl70-25-3-original.jpg', 'bl70-25-3.jpg'),
    ('bl70-25-4-original.jpg', 'bl70-25-4.jpg'),
    ('bl70-25-5-original.jpg', 'bl70-25-5.jpg'),
]

def process_image(input_path, output_path):
    img = Image.open(input_path)
    # Convert to RGB
    if img.mode != 'RGB':
        img = img.convert('RGB')
    # Resize: keep aspect ratio, long edge -> TARGET_LONG_EDGE
    w, h = img.size
    if max(w, h) > TARGET_LONG_EDGE:
        if w >= h:
            new_w = TARGET_LONG_EDGE
            new_h = int(h * TARGET_LONG_EDGE / w)
        else:
            new_h = TARGET_LONG_EDGE
            new_w = int(w * TARGET_LONG_EDGE / h)
        img = img.resize((new_w, new_h), Image.LANCZOS)
    # Color correction: desaturate 10% + contrast +15% + brightness +5% + sharpen
    img = ImageEnhance.Color(img).enhance(0.90)
    img = ImageEnhance.Contrast(img).enhance(1.15)
    img = ImageEnhance.Brightness(img).enhance(1.05)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=80, threshold=2))
    # Save as JPEG
    img.save(output_path, 'JPEG', quality=QUALITY, optimize=True)
    size_kb = os.path.getsize(output_path) / 1024
    print(f'  {os.path.basename(output_path)}: {img.size[0]}x{img.size[1]}, {size_kb:.0f} KB')

print('Processing BL70-25 images...')
for src_name, dst_name in mapping:
    src_path = os.path.join(SOURCE_DIR, src_name)
    dst_path = os.path.join(OUTPUT_DIR, dst_name)
    process_image(src_path, dst_path)
print('Done!')
