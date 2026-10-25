import os
import re
import glob

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    # Replace includes
    def include_replacer(match):
        include_path = match.group(1)
        full_path = os.path.join(os.path.dirname(filepath), include_path)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as inc_f:
                return inc_f.read()
        return match.group(0)
    
    # Try multiple passes for nested includes if any, but once is usually enough for header/footer
    content = re.sub(r"<\?php\s+.*?require.*?__DIR__\s*\.\s*'/([^']+)'[^>]*\?>", include_replacer, content, flags=re.DOTALL)
    content = re.sub(r"<\?php\s+.*?require.*?__DIR__\s*\.\s*'([^']+)'[^>]*\?>", include_replacer, content, flags=re.DOTALL)

    # Convert app_url('some.php') to some.html
    content = re.sub(r"<\?=.*?app_url\(['\"]([^'\"]+)\.php['\"]\).*?\?>", r"\1.html", content)
    content = re.sub(r"<\?=.*?app_url\(['\"]([^'\"]+)['\"]\).*?\?>", r"\1", content)
    
    # Replace <?= e($var) ?> and similar with dummy text
    content = re.sub(r"<\?=.*?format_price.*?\?>", "1.000.000 đ", content)
    content = re.sub(r"<\?=.*?title.*?\?>", "Trang web", content, flags=re.IGNORECASE)
    content = re.sub(r"<\?=.*?\?>", "Dữ liệu mẫu", content)

    # Remove all other PHP blocks
    content = re.sub(r"<\?php.*?\?>", "", content, flags=re.DOTALL)

    # Replace .php links in HTML to .html
    content = re.sub(r'href="([^"]+)\.php([^"]*)"', r'href="\1.html\2"', content)
    content = re.sub(r"href='([^']+)\.php([^']*)'", r"href='\1.html\2'", content)
    
    # For action attributes in forms
    content = re.sub(r'action="([^"]+)\.php([^"]*)"', r'action="\1.html\2"', content)

    # Clean up excessive newlines
    content = re.sub(r'\n\s*\n', '\n\n', content)

    html_filepath = filepath[:-4] + '.html'
    try:
        with open(html_filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f"Created {html_filepath}")
        os.remove(filepath)
    except Exception as e:
        print(f"Error saving {html_filepath}: {e}")

if __name__ == '__main__':
    php_files = glob.glob('*.php')
    for f in php_files:
        process_file(f)
    print("Done!")
