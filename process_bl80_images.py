"""
Process BL80-25 images:
- Resize to 1600px wide (preserves detail, keeps file small)
- Desaturate (remove yellow tint)
- Increase contrast slightly
- Increase brightness slightly
- Apply slight sharpening
- Save as bl80-25-{1-5}.jpg in images/products/
"""
from PIL import Image, ImageEnhance, ImageFilter
import os

SOURCE_DIR = '/Users/vivianwang/WorkBuddy/2026-07-01-16-58-56/vivian_website/images/products/source/bl80-25'
OUTPUT_DIR = '/Users/vivianwang/WorkBuddy/2026-07-01-16-58-56/vivian_website/images/products'

# Source files in order
sources = [
    ('bl80-25-1-original.jpg', 'bl80-25-front.jpg'),  # Used as primary front view
    ('bl80-25-2-original.jpg', 'bl80-25-2.jpg'),
    ('bl80-25-3-original.jpg', 'bl80-25-3.jpg'),
    ('bl80-25-4-original.jpg', 'bl80-25-4.jpg'),
    ('bl80-25-5-original.jpg', 'bl80-25-5.jpg'),
]

TARGET_WIDTH = 1600

for src_name, out_name in sources:
    src_path = os.path.join(SOURCE_DIR, src_name)
    out_path = os.path.join(OUTPUT_DIR, out_name)

    img = Image.open(src_path).convert('RGB')
    orig_w, orig_h = img.size
    print(f"\n{src_name}: {orig_w}x{orig_h}")

    # Resize to target width
    if orig_w > TARGET_WIDTH:
        ratio = TARGET_WIDTH / orig_w
        new_h = int(orig_h * ratio)
        img = img.resize((TARGET_WIDTH, new_h), Image.LANCZOS)
        print(f"  Resized to: {img.size[0]}x{img.size[1]}")

    # 1. Desaturate slightly (remove yellow/orange factory cast)
    # 0.85 = reduce saturation by 15%
    img = ImageEnhance.Color(img).enhance(0.88)

    # 2. Increase contrast
    img = ImageEnhance.Contrast(img).enhance(1.08)

    # 3. Increase brightness slightly
    img = ImageEnhance.Brightness(img).enhance(1.05)

    # 4. Sharpen
    img = img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=110, threshold=2))

    # Save
    img.save(out_path, 'JPEG', quality=88, optimize=True, progressive=True)
    size_kb = os.path.getsize(out_path) / 1024
    print(f"  Saved: {out_name} ({size_kb:.0f} KB)")

print("\nAll BL80-25 images processed!")
