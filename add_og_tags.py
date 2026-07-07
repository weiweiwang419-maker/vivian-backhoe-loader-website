#!/usr/bin/env python3
"""Add Open Graph + Twitter Card meta tags to all HTML pages."""
import os
import re

website_dir = os.path.dirname(os.path.abspath(__file__))
base_url = "https://www.backhoemach.com"

# Page configurations: filename -> (og_type, og_image, og_title, og_description)
# Titles and descriptions are pulled from existing <title> and <meta description>
# We just need to map page -> image
page_configs = {
    "index.html": {
        "type": "website",
        "image": "og-default.jpg",
        "url": f"{base_url}/",
    },
    "products.html": {
        "type": "website",
        "image": "og-default.jpg",
        "url": f"{base_url}/products.html",
    },
    "about.html": {
        "type": "profile",
        "image": "og-default.jpg",
        "url": f"{base_url}/about.html",
    },
    "floor.html": {
        "type": "article",
        "image": "og-default.jpg",
        "url": f"{base_url}/floor.html",
    },
    "quote.html": {
        "type": "website",
        "image": "og-default.jpg",
        "url": f"{base_url}/quote.html",
    },
    "faq.html": {
        "type": "website",
        "image": "og-default.jpg",
        "url": f"{base_url}/faq.html",
    },
    "product-bl105-25.html": {
        "type": "product",
        "image": "og-product-bl105-25.jpg",
        "url": f"{base_url}/product-bl105-25.html",
    },
    "product-bl90-25.html": {
        "type": "product",
        "image": "og-product-bl90-25.jpg",
        "url": f"{base_url}/product-bl90-25.html",
    },
    "product-bl80-25.html": {
        "type": "product",
        "image": "og-product-bl80-25.jpg",
        "url": f"{base_url}/product-bl80-25.html",
    },
    "product-bl70-25.html": {
        "type": "product",
        "image": "og-product-bl70-25.jpg",
        "url": f"{base_url}/product-bl70-25.html",
    },
    "product-bl45-18.html": {
        "type": "product",
        "image": "og-product-bl45-18.jpg",
        "url": f"{base_url}/product-bl45-18.html",
    },
    "product-bl35-12.html": {
        "type": "product",
        "image": "og-product-bl35-12.jpg",
        "url": f"{base_url}/product-bl35-12.html",
    },
    "product-bl15-06.html": {
        "type": "product",
        "image": "og-product-bl15-06.jpg",
        "url": f"{base_url}/product-bl15-06.html",
    },
}

for fname, config in page_configs.items():
    fpath = os.path.join(website_dir, fname)
    if not os.path.exists(fpath):
        print(f"SKIP (not found): {fname}")
        continue

    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract existing title and description
    title_match = re.search(r"<title>(.*?)</title>", content, re.DOTALL)
    desc_match = re.search(r'<meta\s+name="description"\s+content="(.*?)"', content, re.DOTALL)

    title = title_match.group(1).strip() if title_match else "VIVIAN — Backhoe Loader Expert"
    description = desc_match.group(1).strip() if desc_match else "Your trusted backhoe loader consultant in China."

    image_url = f"{base_url}/{config['image']}"

    # Build OG + Twitter Card meta tags
    og_tags = f"""<!-- Open Graph / Social Share -->
<meta property="og:type" content="{config['type']}">
<meta property="og:url" content="{config['url']}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{image_url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:site_name" content="VIVIAN — Backhoe Loader Expert">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="{config['url']}">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{image_url}">"""

    # Check if OG tags already exist (idempotent)
    if "property=\"og:title\"" in content:
        # Remove old OG tags block
        content = re.sub(
            r"<!-- Open Graph / Social Share -->.*?<!-- /Open Graph -->",
            "",
            content,
            flags=re.DOTALL,
        )
        # Also remove any standalone og tags
        content = re.sub(r'<meta\s+property="og:[^"]*"\s+content="[^"]*">\s*\n?', "", content)
        content = re.sub(r'<meta\s+name="twitter:[^"]*"\s+content="[^"]*">\s*\n?', "", content)

    # Insert OG tags right after the <meta name="description"...> line
    # Find the description meta tag and insert after it
    desc_pattern = r'(<meta\s+name="description"\s+content="[^"]*">\s*\n)'
    if desc_match:
        content = re.sub(desc_pattern, r'\1' + og_tags + "\n", content, count=1)
    else:
        # Fallback: insert after viewport meta
        vp_pattern = r'(<meta\s+name="viewport"\s+content="[^"]*">\s*\n)'
        content = re.sub(vp_pattern, r'\1' + og_tags + "\n", content, count=1)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"OK: {fname}")

print(f"\n=== OG tags added to {len(page_configs)} pages ===")
