#!/usr/bin/env python3
"""Insert a <url> entry into sitemap.xml in the correct position."""
import sys
import xml.etree.ElementTree as ET
from datetime import date

if len(sys.argv) < 3:
    print("Usage: add_sitemap.py <loc> <changefreq> [priority]")
    sys.exit(1)

loc = sys.argv[1]
changefreq = sys.argv[2]
priority = sys.argv[3] if len(sys.argv) > 3 else "0.8"

tree = ET.parse('sitemap.xml')
root = tree.getroot()
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

# Already exists?
for url in root.findall('s:url', ns):
    existing = url.find('s:loc', ns)
    if existing is not None and existing.text == loc:
        print(f"Already exists: {loc}")
        sys.exit(0)

url = ET.SubElement(root, '{http://www.sitemaps.org/schemas/sitemap/0.9}url')
ET.SubElement(url, '{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text = loc
ET.SubElement(url, '{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod').text = date.today().isoformat()
ET.SubElement(url, '{http://www.sitemaps.org/schemas/sitemap/0.9}changefreq').text = changefreq
ET.SubElement(url, '{http://www.sitemaps.org/schemas/sitemap/0.9}priority').text = priority

# Pretty-print to keep file readable
ET.indent(tree, space="  ")
tree.write('sitemap.xml', encoding='UTF-8', xml_declaration=True)

# Verify
tree2 = ET.parse('sitemap.xml')
urls = tree2.findall('s:url', ns)
print(f"Total URLs: {len(urls)}")
print(f"Added: {loc}")