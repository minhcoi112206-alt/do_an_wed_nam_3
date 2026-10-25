import glob, re
import os

files = glob.glob('products*.html')
pattern = re.compile(r'<div class="w-full bg-surface-container-low/60 py-space-sm backdrop-blur-md">\s*<div class="max-w-\[1280px\] mx-auto px-gutter">\s*<nav class="hidden xl:flex items-center gap-space-xs p-1".*?</nav>\s*</div>\s*</div>', re.DOTALL)

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    new_content = pattern.sub('', content)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(new_content)
print(f'Fixed duplicate navs in {len(files)} files')
