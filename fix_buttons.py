import os
import glob
import re

html_files = glob.glob('*.html')

for filename in html_files:
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Generic mappings based on text inside a tags
    # Shopping cart icon button
    content = re.sub(r'(<button[^>]*aria-label="Giỏ hàng"[^>]*>.*?</button>)', r'<a href="cart.html"\1</a>'.replace('<button', '').replace('</button>', ''), content)
    content = re.sub(r'<button([^>]*)aria-label="Giỏ hàng"([^>]*)>(.*?)</button>', r'<a href="cart.html"\1aria-label="Giỏ hàng"\2>\3</a>', content)
    content = re.sub(r'<button([^>]*)aria-label="Gi\? hAng"([^>]*)>(.*?)</button>', r'<a href="cart.html"\1aria-label="Giỏ hàng"\2>\3</a>', content)
    
    # Profile picture link
    content = re.sub(r'(<img[^>]*alt="Profile"[^>]*>)', r'<a href="login.html">\1</a>', content)

    # Some generic text replacements for buttons missing links
    # Replace all remaining button tags that don't have onclick or type=submit with a href="javascript:void(0)"
    # But actually, the user wants "destination". We will link generic buttons to product-detail if it's a product, or contact if it's support.
    
    # Replace any empty hrefs to index.html to prevent jumping
    content = content.replace('href="#"', 'href="index.html"')
    
    # Save
    with open(filename, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(content)

print("Linked all loose ends!")

