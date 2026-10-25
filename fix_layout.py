import os
import glob
import re

# Replace broken logo in all html files
html_files = glob.glob('*.html')
apple_logo_svg = """<svg class="h-8 w-auto fill-current text-on-surface" viewBox="0 0 384 512" xmlns="http://www.w3.org/2000/svg"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"></path></svg>"""

for filename in html_files:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue
    
    # Replace the broken img tag. The img tag might span multiple lines or have a long googleusercontent src
    content = re.sub(r'<img[^>]*alt="Tao Store VN/A Logo"[^>]*>', apple_logo_svg, content)

    # In contact.html and about.html, fix the padding issue (pt-20 -> pt-32) so it's not hidden by the sticky header
    if filename in ["contact.html", "about.html", "index.html"]:
        # Let's just fix it globally for any main tag starting with w-full pt-20
        content = content.replace('<main class="w-full pt-20', '<main class="w-full pt-32')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixed logo and padding.")
