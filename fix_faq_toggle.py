#!/usr/bin/env python3
"""Fix FAQ toggle conflict: remove inline onclick that conflicts with addEventListener."""
import os
import re

website_dir = os.path.dirname(os.path.abspath(__file__))

# All HTML files with FAQ
files = [
    'faq.html',
    'product-bl105-25.html',
    'product-bl90-25.html',
    'product-bl80-25.html',
    'product-bl35-12.html',
    'product-bl45-18.html',
    'product-bl15-06.html',
    'product-bl70-25.html',
]

for fname in files:
    fpath = os.path.join(website_dir, fname)
    if not os.path.exists(fpath):
        print(f"SKIP (not found): {fname}")
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove the inline onclick from faq-question divs
    # Pattern: onclick="this.parentElement.classList.toggle('open')"
    old_attr = """ onclick="this.parentElement.classList.toggle('open')" """
    count = content.count(old_attr)

    # Also try without trailing space
    old_attr2 = """onclick="this.parentElement.classList.toggle('open')" """
    count2 = content.count(old_attr2)

    # Use regex to be safe with spacing
    new_content = re.sub(
        r'\s*onclick="this\.parentElement\.classList\.toggle\(\'open\'\)"',
        '',
        content
    )

    actual_count = content.count('onclick="this.parentElement.classList.toggle(')

    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"FIXED: {fname} - removed {actual_count} inline onclick(s)")
    else:
        print(f"NO CHANGE: {fname}")

print("\nDone! All FAQ toggles fixed.")
