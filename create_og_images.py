#!/usr/bin/env python3
"""Create Open Graph share images (1200x630) for all pages."""
import os
from PIL import Image, ImageDraw, ImageFont

website_dir = os.path.dirname(os.path.abspath(__file__))
base_url = "https://www.backhoemach.com"

# --- 1. Create og-default.jpg from factory drone shot ---
factory_img = os.path.join(website_dir, "images", "factory", "dji_01_奥力特工厂_橙色装载机队伍.jpg")
og_default_path = os.path.join(website_dir, "og-default.jpg")

if os.path.exists(factory_img):
    img = Image.open(factory_img)
    print(f"Factory image: {img.size}")

    # Crop to 1200x630 (center crop)
    target_w, target_h = 1200, 630
    img_ratio = img.width / img.height
    target_ratio = target_w / target_h

    if img_ratio > target_ratio:
        # Image is wider, crop sides
        new_width = int(img.height * target_ratio)
        left = (img.width - new_width) // 2
        img = img.crop((left, 0, left + new_width, img.height))
    else:
        # Image is taller, crop top/bottom
        new_height = int(img.width / target_ratio)
        top = (img.height - new_height) // 2
        img = img.crop((0, top, img.width, top + new_height))

    img = img.resize((target_w, target_h), Image.LANCZOS)

    # Add subtle dark gradient at bottom for text readability
    overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for i in range(180):
        alpha = int(180 * (i / 180) * 0.7)
        draw.rectangle([0, target_h - 180 + i, target_w, target_h - 180 + i + 1], fill=(0, 0, 0, alpha))

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    # Add brand text
    draw = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 42)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Brand name
    brand_text = "VIVIAN"
    brand_sub = "Backhoe Loader Expert — China"
    bbox = draw.textbbox((0, 0), brand_text, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((target_w - tw) // 2, target_h - 110), brand_text, fill=(255, 255, 255), font=font_title)
    bbox2 = draw.textbbox((0, 0), brand_sub, font=font_sub)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((target_w - tw2) // 2, target_h - 55), brand_sub, fill=(220, 220, 220), font=font_sub)

    img.save(og_default_path, "JPEG", quality=88, optimize=True)
    print(f"Created og-default.jpg ({os.path.getsize(og_default_path) // 1024}KB)")
else:
    print(f"WARNING: Factory image not found at {factory_img}")

# --- 2. Create product OG images ---
products = {
    "product-bl105-25": ("images/products/bl105-25-front.jpg", "BL 105-25 Backhoe Loader", "73kW · 4m dig depth · The workhorse"),
    "product-bl90-25": ("images/products/bl90-25-front.jpg", "BL 90-25 Backhoe Loader", "73kW · Telescopic arm · The all-rounder"),
    "product-bl80-25": ("images/products/bl80-25-front.jpg", "BL 80-25 Backhoe Loader", "73kW · Balanced size · Best value"),
    "product-bl70-25": ("images/products/bl70-25-front.jpg", "BL 70-25 Backhoe Loader", "55kW · Compact · Farm & small sites"),
    "product-bl45-18": ("images/products/bl45-18-front.jpg", "BL 45-18 Backhoe Loader", "48kW · Municipal work · Tight sites"),
    "product-bl35-12": ("images/products/bl35-12-front.jpg", "BL 35-12 Backhoe Loader", "37kW · Entry level · Light work"),
    "product-bl15-06": ("images/products/bl15-06-front.jpg", "BL 15-06 Mini Electric", "72V/120V · Indoor & urban · Electric"),
}

for page_name, (img_src, title, subtitle) in products.items():
    img_path = os.path.join(website_dir, img_src)
    og_path = os.path.join(website_dir, f"og-{page_name}.jpg")

    if not os.path.exists(img_path):
        # Try backup folder
        backup_name = img_src.split("/")[-1]
        backup_path = os.path.join(website_dir, "images", "products_backup", backup_name)
        if os.path.exists(backup_path):
            img_path = backup_path
        else:
            print(f"SKIP {page_name}: image not found")
            continue

    img = Image.open(img_path)
    print(f"\n{page_name}: {img.size} -> 1200x630")

    # Crop to 1200x630 (center crop)
    target_w, target_h = 1200, 630
    img_ratio = img.width / img.height
    target_ratio = target_w / target_h

    if img_ratio > target_ratio:
        new_width = int(img.height * target_ratio)
        left = (img.width - new_width) // 2
        img = img.crop((left, 0, left + new_width, img.height))
    else:
        new_height = int(img.width / target_ratio)
        top = (img.height - new_height) // 2
        img = img.crop((0, top, img.width, top + new_height))

    img = img.resize((target_w, target_h), Image.LANCZOS)

    # Add dark gradient at bottom
    overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for i in range(160):
        alpha = int(160 * (i / 160) * 0.65)
        draw.rectangle([0, target_h - 160 + i, target_w, target_h - 160 + i + 1], fill=(0, 0, 0, alpha))

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 38)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw.text((40, target_h - 100), title, fill=(255, 255, 255), font=font_title)
    draw.text((40, target_h - 50), subtitle, fill=(220, 220, 220), font=font_sub)

    img.save(og_path, "JPEG", quality=85, optimize=True)
    print(f"  -> og-{page_name}.jpg ({os.path.getsize(og_path) // 1024}KB)")

print("\n=== All OG images created ===")
