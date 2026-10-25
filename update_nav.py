import os
import glob
import re

html_files = glob.glob('*.html')

active_cls = "px-space-md py-space-xs transition-all bg-primary-container text-on-primary-container font-semibold rounded-full"
inactive_cls = "px-space-md py-space-xs rounded-full font-label-lg text-label-lg text-on-surface-variant hover:text-on-surface hover:bg-surface-container transition-all"

for filename in html_files:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue

    def nav_replacer(match):
        # Determine which item is active based on filename
        is_index = "index.html" in filename
        is_products = "products.html" in filename or "product-detail.html" in filename
        is_about = "about.html" in filename
        is_contact = "contact.html" in filename
        
        c_index = active_cls if is_index else inactive_cls
        c_products = active_cls if is_products else inactive_cls
        c_about = active_cls if is_about else inactive_cls
        c_contact = active_cls if is_contact else inactive_cls
        
        new_nav = f"""<nav class="hidden xl:flex items-center gap-space-xs p-1" data-active-classes="bg-primary-container text-on-primary-container font-semibold rounded-full">
<a class="{c_index}" href="index.html">Trang chủ</a>
<a class="{c_products}" href="products.html">Danh mục sản phẩm</a>
<a class="{c_about}" href="about.html">Giới thiệu</a>
<a class="{c_contact}" href="contact.html">Hỗ trợ</a>
</nav>"""
        return new_nav

    # Use regex to find <nav> ... </nav> block
    content = re.sub(r'<nav[^>]*>.*?</nav>', nav_replacer, content, flags=re.DOTALL)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated nav bars.")
