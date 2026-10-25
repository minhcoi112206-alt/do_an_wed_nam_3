import os
import re

files = ["index.html", "products.html", "product-detail.html", "compare.html"]

for filename in files:
    if not os.path.exists(filename): continue
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Link mappings for navigation
    # It might be in format <a ... data-path="iphone" href="#">iPhone</a>
    # Or just href="#"
    
    # Let's replace the navigation links by data-path if present
    content = re.sub(r'(data-path="iphone"[^>]*href=")[^"]*(")', r'\1products.html\2', content)
    content = re.sub(r'(data-path="so-sanh"[^>]*href=")[^"]*(")', r'\1compare.html\2', content)
    content = re.sub(r'(data-path="phu-kien"[^>]*href=")[^"]*(")', r'\1products.html\2', content)
    content = re.sub(r'(data-path="thu-cu-doi-moi"[^>]*href=")[^"]*(")', r'\1products.html\2', content)
    content = re.sub(r'(data-path="khuyen-mai"[^>]*href=")[^"]*(")', r'\1products.html\2', content)
    content = re.sub(r'(data-path="ho-tro"[^>]*href=")[^"]*(")', r'\1index.html\2', content)

    # Logo link
    content = re.sub(r'(<a[^>]*class="[^"]*logo[^"]*"[^>]*href=")[^"]*(")', r'\1index.html\2', content)

    # All 'Mua ngay' buttons or links should go to product-detail.html or checkout.html.
    # We can just change all buttons to act as links to product-detail if they don't have it.
    # E.g. <button ...>Mua ngay</button> -> <a href="product-detail.html" ...>Mua ngay</a>
    content = re.sub(r'<button([^>]*)>(\s*<span[^>]*>Mua ngay</span>\s*<span[^>]*>arrow_forward</span>\s*)</button>', r'<a href="product-detail.html"\1>\2</a>', content)
    
    # Generic product cards clicking on image or title -> product-detail
    content = re.sub(r'<a([^>]*)href="#"([^>]*)>(.*?iPhone.*?)</a>', r'<a\1href="product-detail.html"\2>\3</a>', content, flags=re.IGNORECASE)

    # Other # links -> index.html to avoid broken jumps, but let's just do it for typical links
    content = content.replace('href="#"', 'href="index.html"')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("Links updated.")
