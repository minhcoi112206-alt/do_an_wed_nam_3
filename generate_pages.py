import re
import shutil
import os

products_html = "products.html"

# Base product template
product_template = """
<article class="group bg-surface-container-lowest rounded-[24px] p-space-lg shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col justify-between relative overflow-hidden">
<div class="flex items-center justify-between mb-space-sm">
<span class="inline-flex items-center gap-1 font-label-eyebrow text-label-eyebrow font-bold px-2 py-1 rounded-full {tag_bg} {tag_text} uppercase tracking-wider">
<span class="material-symbols-outlined text-xs">{tag_icon}</span>
                  {tag_label}
                </span>
<span class="font-label-eyebrow text-label-eyebrow px-2 py-1 rounded-full bg-error-container text-on-error-container font-semibold">
                  {discount}
                </span>
</div>
<div class="w-full h-56 flex items-center justify-center py-space-sm group-hover:scale-105 transition-transform duration-500">
<img class="max-h-full max-w-full object-contain" src="{img_src}" alt="{name}"/>
</div>
<div class="flex flex-col gap-space-xs mt-space-sm">
<div class="flex items-center justify-between">
<div class="flex items-center gap-1.5">
<span class="w-3.5 h-3.5 rounded-full bg-inverse-surface ring-1 ring-outline-variant inline-block"></span>
<span class="w-3.5 h-3.5 rounded-full bg-surface-container-lowest ring-1 ring-outline-variant inline-block"></span>
<span class="w-3.5 h-3.5 rounded-full bg-blue-300 ring-1 ring-outline-variant inline-block"></span>
</div>
<div class="flex gap-1">
<span class="px-1.5 py-0.5 rounded bg-surface-container font-label-eyebrow text-label-eyebrow text-on-surface-variant font-bold">{cap1}</span>
<span class="px-1.5 py-0.5 rounded bg-surface-container font-label-eyebrow text-label-eyebrow text-on-surface-variant">{cap2}</span>
</div>
</div>
<h3 class="font-headline-sm text-headline-sm text-on-surface font-bold leading-tight group-hover:text-primary transition-colors">
                  {name}
                </h3>
<p class="font-body-sm text-body-sm text-outline">{desc}</p>
<div class="mt-space-xs flex items-baseline gap-space-sm">
<span class="font-headline-md text-headline-md text-primary font-bold">{price}</span>
<span class="font-body-sm text-body-sm text-outline line-through">{old_price}</span>
</div>
<div class="mt-space-xs bg-surface-container-low p-2 rounded-xl flex items-center gap-2">
<span class="material-symbols-outlined text-primary text-sm">redeem</span>
<span class="font-label-eyebrow text-label-eyebrow text-on-surface-variant">{gift}</span>
</div>
</div>
<div class="grid grid-cols-2 gap-space-xs mt-space-md pt-space-xs">
<button class="w-full py-2.5 px-3 rounded-full bg-primary text-on-primary font-label-md text-label-md font-semibold hover:bg-primary-container transition-all active:scale-95 shadow-sm text-center">
                  Mua ngay
                </button>
<button class="w-full py-2.5 px-3 rounded-full bg-surface-container text-on-surface font-label-md text-label-md font-medium hover:bg-surface-container-high transition-all active:scale-95 flex items-center justify-center gap-1">
<span class="material-symbols-outlined text-base">add_shopping_cart</span>
                  Thêm giỏ
                </button>
</div>
</article>
"""

p1_extra = [
    {
        "name": "iPhone 14 Pro Max 128GB", "tag_bg": "bg-secondary-fixed", "tag_text": "text-on-secondary-fixed", "tag_icon": "thumb_up", "tag_label": "Like New 99%", "discount": "Bán chạy", "img_src": "https://lh3.googleusercontent.com/aida-public/AB6AXuADDXzcgAWHQEH424OVFbqZXd6WyfnJ2q8GPMJZM1zf5AniKz6Ym8ZYrUqsrk8slPSNnRRD5YZ0WYPePagtVvgRAaZfZ8ZDTMuavye5tgz3qmW3_kiFLFcddISRNrboGQBBVTQK64ZQbRisyVQrLD124HpW0op9-hPCo2M54FQPxjt5-TeYCFarnfdf9XmkKllZ1P_VgT9_uHiVtWI3CDihbpHb2Mk7rqAX5AXgrSA", "cap1": "128GB", "cap2": "256GB", "desc": "Dynamic Island • Pin cực trâu", "price": "18.590.000₫", "old_price": "22.000.000₫", "gift": "Tặng Cáp sạc C-to-C"
    },
    {
        "name": "iPhone 14 128GB VN/A", "tag_bg": "bg-primary-fixed", "tag_text": "text-on-primary-fixed", "tag_icon": "verified", "tag_label": "VN/A Chính Hãng", "discount": "-15%", "img_src": "https://lh3.googleusercontent.com/aida-public/AB6AXuBDqPCzBG9W4VQpoaVRyv43NHAfQluJil17jnp1hAfZZcpymMsldxC6x_6gGDNH2vbm8rPJ3GDq4BjQJzAUnJOh6Iu3BDBPcpCuKrSRoLb6ZueJayPuR-QZoN870KwWcMJi7np38INqOHPqE5b-pgHljhgtE_9_zxnon1iV17u23Q9FGaYa8yU1Rhwl3iKWQhrvIBhbJBE5RxU89F9bvMpKsoDJ1zufGSi7OhcIESE", "cap1": "128GB", "cap2": "256GB", "desc": "Camera kép xuất sắc • A15 Bionic", "price": "15.990.000₫", "old_price": "18.990.000₫", "gift": "Tặng Ốp lưng thời trang"
    }
]

p2_products = [
    {
        "name": "iPhone 12 Pro Max 128GB", "tag_bg": "bg-secondary-fixed", "tag_text": "text-on-secondary-fixed", "tag_icon": "thumb_up", "tag_label": "Like New 99%", "discount": "Giá Sốc", "img_src": "https://lh3.googleusercontent.com/aida-public/AB6AXuADDXzcgAWHQEH424OVFbqZXd6WyfnJ2q8GPMJZM1zf5AniKz6Ym8ZYrUqsrk8slPSNnRRD5YZ0WYPePagtVvgRAaZfZ8ZDTMuavye5tgz3qmW3_kiFLFcddISRNrboGQBBVTQK64ZQbRisyVQrLD124HpW0op9-hPCo2M54FQPxjt5-TeYCFarnfdf9XmkKllZ1P_VgT9_uHiVtWI3CDihbpHb2Mk7rqAX5AXgrSA", "cap1": "128GB", "cap2": "256GB", "desc": "Màn hình 6.7 inch • Camera 3 ống kính", "price": "11.290.000₫", "old_price": "14.500.000₫", "gift": "Tặng Củ sạc 20W"
    },
    {
        "name": "iPhone 12 64GB", "tag_bg": "bg-secondary-fixed", "tag_text": "text-on-secondary-fixed", "tag_icon": "thumb_up", "tag_label": "Cũ Đẹp 99%", "discount": "Bán chạy", "img_src": "https://lh3.googleusercontent.com/aida-public/AB6AXuCDYuksGiSGmOWYS6flD1rzDlWzwNtf5qtBdPOn64gfCLZIo4aXv-wplunfXOX0es-giWB7ItxwrGOfEhoYM9FjQ6oHZkSG0v5jJmomSFuVLTuyMcrrQhv-Ro1uYbbvN0D6616XhfNXHejuExlKDX8Fp2dnEeKktFUG0CHHB45GsXuxzyha_o0IgGgc5LLa1dhy3B79TjdxReDcynla7cTQIbgmTcJF3WUauF-213k", "cap1": "64GB", "cap2": "128GB", "desc": "Thiết kế vuông vức • 5G siêu tốc", "price": "7.890.000₫", "old_price": "9.990.000₫", "gift": "Bảo hành 6 tháng"
    },
    {
        "name": "iPhone 11 Pro Max 64GB", "tag_bg": "bg-secondary-fixed", "tag_text": "text-on-secondary-fixed", "tag_icon": "thumb_up", "tag_label": "Like New 99%", "discount": "Hot", "img_src": "https://lh3.googleusercontent.com/aida-public/AB6AXuBDqPCzBG9W4VQpoaVRyv43NHAfQluJil17jnp1hAfZZcpymMsldxC6x_6gGDNH2vbm8rPJ3GDq4BjQJzAUnJOh6Iu3BDBPcpCuKrSRoLb6ZueJayPuR-QZoN870KwWcMJi7np38INqOHPqE5b-pgHljhgtE_9_zxnon1iV17u23Q9FGaYa8yU1Rhwl3iKWQhrvIBhbJBE5RxU89F9bvMpKsoDJ1zufGSi7OhcIESE", "cap1": "64GB", "cap2": "256GB", "desc": "Pin cực trâu • 3 Camera sắc nét", "price": "8.490.000₫", "old_price": "11.000.000₫", "gift": "Tặng Ốp lưng + Kính cường lực"
    },
    {
        "name": "iPhone 11 64GB", "tag_bg": "bg-secondary-fixed", "tag_text": "text-on-secondary-fixed", "tag_icon": "thumb_up", "tag_label": "Cũ 98%", "discount": "Giá rẻ", "img_src": "https://lh3.googleusercontent.com/aida-public/AB6AXuCDYuksGiSGmOWYS6flD1rzDlWzwNtf5qtBdPOn64gfCLZIo4aXv-wplunfXOX0es-giWB7ItxwrGOfEhoYM9FjQ6oHZkSG0v5jJmomSFuVLTuyMcrrQhv-Ro1uYbbvN0D6616XhfNXHejuExlKDX8Fp2dnEeKktFUG0CHHB45GsXuxzyha_o0IgGgc5LLa1dhy3B79TjdxReDcynla7cTQIbgmTcJF3WUauF-213k", "cap1": "64GB", "cap2": "128GB", "desc": "Màn hình 6.1 inch • Face ID nhạy", "price": "5.990.000₫", "old_price": "7.500.000₫", "gift": "Bảo hành 6 tháng"
    },
    {
        "name": "iPhone SE 2022 (Gen 3)", "tag_bg": "bg-primary-fixed", "tag_text": "text-on-primary-fixed", "tag_icon": "verified", "tag_label": "Mới 100%", "discount": "Sale", "img_src": "https://lh3.googleusercontent.com/aida-public/AB6AXuBLf3Vo3xvsV_5V4cShJ-ZXLqFUrfoGoiN0-8sA796NzCsNNq5VJNheetrJdeg6ZjMthCsGCtQjiXAhrKy4DyRu5T-AV0HmM3m2Ak-sbBWYbJTdvz8rCAwG_8EdpoZQTJi2QSrNBUS9DSyESPzF2GS10bjraNBMMubafPxvkRbvqy6HA1GTxrqpYV_l3F37C0hLAcIPyVUFg29s2mJK-2wdHHNQnJOsPxt1pHIBd6I", "cap1": "64GB", "cap2": "128GB", "desc": "Chip A15 Bionic • Nhỏ gọn mạnh mẽ", "price": "8.990.000₫", "old_price": "10.990.000₫", "gift": "Tặng Củ sạc 20W"
    },
    {
        "name": "iPhone XS Max 64GB", "tag_bg": "bg-secondary-fixed", "tag_text": "text-on-secondary-fixed", "tag_icon": "thumb_up", "tag_label": "Cũ Đẹp 99%", "discount": "Classic", "img_src": "https://lh3.googleusercontent.com/aida-public/AB6AXuADDXzcgAWHQEH424OVFbqZXd6WyfnJ2q8GPMJZM1zf5AniKz6Ym8ZYrUqsrk8slPSNnRRD5YZ0WYPePagtVvgRAaZfZ8ZDTMuavye5tgz3qmW3_kiFLFcddISRNrboGQBBVTQK64ZQbRisyVQrLD124HpW0op9-hPCo2M54FQPxjt5-TeYCFarnfdf9XmkKllZ1P_VgT9_uHiVtWI3CDihbpHb2Mk7rqAX5AXgrSA", "cap1": "64GB", "cap2": "256GB", "desc": "Màn hình OLED 6.5 inch • Loa kép", "price": "6.290.000₫", "old_price": "7.990.000₫", "gift": "Bảo hành 3 tháng"
    },
    {
        "name": "iPhone X 64GB", "tag_bg": "bg-secondary-fixed", "tag_text": "text-on-secondary-fixed", "tag_icon": "thumb_up", "tag_label": "Cũ 97%", "discount": "Giá Sốc", "img_src": "https://lh3.googleusercontent.com/aida-public/AB6AXuBDqPCzBG9W4VQpoaVRyv43NHAfQluJil17jnp1hAfZZcpymMsldxC6x_6gGDNH2vbm8rPJ3GDq4BjQJzAUnJOh6Iu3BDBPcpCuKrSRoLb6ZueJayPuR-QZoN870KwWcMJi7np38INqOHPqE5b-pgHljhgtE_9_zxnon1iV17u23Q9FGaYa8yU1Rhwl3iKWQhrvIBhbJBE5RxU89F9bvMpKsoDJ1zufGSi7OhcIESE", "cap1": "64GB", "cap2": "256GB", "desc": "Kỷ niệm 10 năm • Viền thép", "price": "4.490.000₫", "old_price": "5.500.000₫", "gift": "Tặng Dán màn hình"
    },
    {
        "name": "iPhone 8 Plus 64GB", "tag_bg": "bg-secondary-fixed", "tag_text": "text-on-secondary-fixed", "tag_icon": "thumb_up", "tag_label": "Cũ 99%", "discount": "Học sinh", "img_src": "https://lh3.googleusercontent.com/aida-public/AB6AXuCDYuksGiSGmOWYS6flD1rzDlWzwNtf5qtBdPOn64gfCLZIo4aXv-wplunfXOX0es-giWB7ItxwrGOfEhoYM9FjQ6oHZkSG0v5jJmomSFuVLTuyMcrrQhv-Ro1uYbbvN0D6616XhfNXHejuExlKDX8Fp2dnEeKktFUG0CHHB45GsXuxzyha_o0IgGgc5LLa1dhy3B79TjdxReDcynla7cTQIbgmTcJF3WUauF-213k", "cap1": "64GB", "cap2": "128GB", "desc": "Touch ID tiện lợi • Chụp chân dung", "price": "3.590.000₫", "old_price": "4.500.000₫", "gift": "Bảo hành 3 tháng"
    }
]

p3_products = [
    {
        "name": "iPhone 8 64GB", "tag_bg": "bg-secondary-fixed", "tag_text": "text-on-secondary-fixed", "tag_icon": "thumb_up", "tag_label": "Cũ 98%", "discount": "Rẻ vô địch", "img_src": "https://lh3.googleusercontent.com/aida-public/AB6AXuBLf3Vo3xvsV_5V4cShJ-ZXLqFUrfoGoiN0-8sA796NzCsNNq5VJNheetrJdeg6ZjMthCsGCtQjiXAhrKy4DyRu5T-AV0HmM3m2Ak-sbBWYbJTdvz8rCAwG_8EdpoZQTJi2QSrNBUS9DSyESPzF2GS10bjraNBMMubafPxvkRbvqy6HA1GTxrqpYV_l3F37C0hLAcIPyVUFg29s2mJK-2wdHHNQnJOsPxt1pHIBd6I", "cap1": "64GB", "cap2": "128GB", "desc": "Nhỏ gọn 4.7 inch • Kính mặt lưng", "price": "2.890.000₫", "old_price": "3.500.000₫", "gift": "Tặng Cáp sạc"
    },
    {
        "name": "iPhone 7 Plus 32GB", "tag_bg": "bg-secondary-fixed", "tag_text": "text-on-secondary-fixed", "tag_icon": "thumb_up", "tag_label": "Cũ 99%", "discount": "Sale", "img_src": "https://lh3.googleusercontent.com/aida-public/AB6AXuADDXzcgAWHQEH424OVFbqZXd6WyfnJ2q8GPMJZM1zf5AniKz6Ym8ZYrUqsrk8slPSNnRRD5YZ0WYPePagtVvgRAaZfZ8ZDTMuavye5tgz3qmW3_kiFLFcddISRNrboGQBBVTQK64ZQbRisyVQrLD124HpW0op9-hPCo2M54FQPxjt5-TeYCFarnfdf9XmkKllZ1P_VgT9_uHiVtWI3CDihbpHb2Mk7rqAX5AXgrSA", "cap1": "32GB", "cap2": "128GB", "desc": "Camera kép • Vỏ nhôm nguyên khối", "price": "2.490.000₫", "old_price": "3.200.000₫", "gift": "Tặng Ốp lưng"
    },
    {
        "name": "iPhone 7 32GB", "tag_bg": "bg-secondary-fixed", "tag_text": "text-on-secondary-fixed", "tag_icon": "thumb_up", "tag_label": "Cũ 97%", "discount": "Phổ thông", "img_src": "https://lh3.googleusercontent.com/aida-public/AB6AXuBDqPCzBG9W4VQpoaVRyv43NHAfQluJil17jnp1hAfZZcpymMsldxC6x_6gGDNH2vbm8rPJ3GDq4BjQJzAUnJOh6Iu3BDBPcpCuKrSRoLb6ZueJayPuR-QZoN870KwWcMJi7np38INqOHPqE5b-pgHljhgtE_9_zxnon1iV17u23Q9FGaYa8yU1Rhwl3iKWQhrvIBhbJBE5RxU89F9bvMpKsoDJ1zufGSi7OhcIESE", "cap1": "32GB", "cap2": "128GB", "desc": "Nút Home cảm ứng • Loa Stereo", "price": "1.990.000₫", "old_price": "2.500.000₫", "gift": "Dán màn hình"
    },
    {
        "name": "iPhone 6s Plus 64GB", "tag_bg": "bg-secondary-fixed", "tag_text": "text-on-secondary-fixed", "tag_icon": "thumb_up", "tag_label": "Cũ 98%", "discount": "Sưu tầm", "img_src": "https://lh3.googleusercontent.com/aida-public/AB6AXuCDYuksGiSGmOWYS6flD1rzDlWzwNtf5qtBdPOn64gfCLZIo4aXv-wplunfXOX0es-giWB7ItxwrGOfEhoYM9FjQ6oHZkSG0v5jJmomSFuVLTuyMcrrQhv-Ro1uYbbvN0D6616XhfNXHejuExlKDX8Fp2dnEeKktFUG0CHHB45GsXuxzyha_o0IgGgc5LLa1dhy3B79TjdxReDcynla7cTQIbgmTcJF3WUauF-213k", "cap1": "16GB", "cap2": "64GB", "desc": "Có jack 3.5mm • 3D Touch", "price": "1.790.000₫", "old_price": "2.200.000₫", "gift": "Bảo hành 1 tháng"
    },
    {
        "name": "iPhone 6s 16GB", "tag_bg": "bg-secondary-fixed", "tag_text": "text-on-secondary-fixed", "tag_icon": "thumb_up", "tag_label": "Cũ 97%", "discount": "Thanh lý", "img_src": "https://lh3.googleusercontent.com/aida-public/AB6AXuBLf3Vo3xvsV_5V4cShJ-ZXLqFUrfoGoiN0-8sA796NzCsNNq5VJNheetrJdeg6ZjMthCsGCtQjiXAhrKy4DyRu5T-AV0HmM3m2Ak-sbBWYbJTdvz8rCAwG_8EdpoZQTJi2QSrNBUS9DSyESPzF2GS10bjraNBMMubafPxvkRbvqy6HA1GTxrqpYV_l3F37C0hLAcIPyVUFg29s2mJK-2wdHHNQnJOsPxt1pHIBd6I", "cap1": "16GB", "cap2": "32GB", "desc": "Máy phụ • Chạy ổn các tác vụ", "price": "1.390.000₫", "old_price": "1.800.000₫", "gift": "Tặng cáp sạc"
    },
    {
        "name": "iPhone 6 Plus 16GB", "tag_bg": "bg-secondary-fixed", "tag_text": "text-on-secondary-fixed", "tag_icon": "thumb_up", "tag_label": "Cũ 95%", "discount": "Clear stock", "img_src": "https://lh3.googleusercontent.com/aida-public/AB6AXuADDXzcgAWHQEH424OVFbqZXd6WyfnJ2q8GPMJZM1zf5AniKz6Ym8ZYrUqsrk8slPSNnRRD5YZ0WYPePagtVvgRAaZfZ8ZDTMuavye5tgz3qmW3_kiFLFcddISRNrboGQBBVTQK64ZQbRisyVQrLD124HpW0op9-hPCo2M54FQPxjt5-TeYCFarnfdf9XmkKllZ1P_VgT9_uHiVtWI3CDihbpHb2Mk7rqAX5AXgrSA", "cap1": "16GB", "cap2": "64GB", "desc": "Màn to 5.5 inch • Xem Youtube", "price": "1.190.000₫", "old_price": "1.500.000₫", "gift": "Bao test 7 ngày"
    },
    {
        "name": "iPhone 6 16GB", "tag_bg": "bg-secondary-fixed", "tag_text": "text-on-secondary-fixed", "tag_icon": "thumb_up", "tag_label": "Cũ 95%", "discount": "Rẻ nhất", "img_src": "https://lh3.googleusercontent.com/aida-public/AB6AXuBDqPCzBG9W4VQpoaVRyv43NHAfQluJil17jnp1hAfZZcpymMsldxC6x_6gGDNH2vbm8rPJ3GDq4BjQJzAUnJOh6Iu3BDBPcpCuKrSRoLb6ZueJayPuR-QZoN870KwWcMJi7np38INqOHPqE5b-pgHljhgtE_9_zxnon1iV17u23Q9FGaYa8yU1Rhwl3iKWQhrvIBhbJBE5RxU89F9bvMpKsoDJ1zufGSi7OhcIESE", "cap1": "16GB", "cap2": "32GB", "desc": "Nhỏ gọn • Nghe gọi tốt", "price": "890.000₫", "old_price": "1.200.000₫", "gift": "Bao test 7 ngày"
    }
]

def generate_html(product_data):
    html = ""
    for p in product_data:
        html += product_template.format(**p)
    return html

def update_pagination(content, current_page):
    # Quick regex to update pagination buttons
    for p in range(1, 4):
        if p == current_page:
            content = re.sub(
                f'<a href="products(?:-[0-9]+)?\\.html"[^>]*>\\s*{p}\\s*</a>',
                f'<button aria-current="page" class="w-10 h-10 rounded-full flex items-center justify-center bg-primary text-on-primary font-label-md text-label-md font-bold shadow-sm">{p}</button>',
                content
            )
            content = re.sub(
                f'<button class="w-10 h-10 rounded-full flex items-center justify-center bg-surface-container-lowest text-on-surface font-label-md text-label-md font-medium hover:bg-surface-container transition-colors shadow-sm">\\s*{p}\\s*</button>',
                f'<button aria-current="page" class="w-10 h-10 rounded-full flex items-center justify-center bg-primary text-on-primary font-label-md text-label-md font-bold shadow-sm">{p}</button>',
                content
            )
        else:
            href = "products.html" if p == 1 else f"products-{p}.html"
            content = re.sub(
                f'<button aria-current="page" class="w-10 h-10 rounded-full flex items-center justify-center bg-primary text-on-primary font-label-md text-label-md font-bold shadow-sm">\\s*{p}\\s*</button>',
                f'<a href="{href}" class="w-10 h-10 rounded-full flex items-center justify-center bg-surface-container-lowest text-on-surface font-label-md text-label-md font-medium hover:bg-surface-container transition-colors shadow-sm">{p}</a>',
                content
            )
            content = re.sub(
                f'<button class="w-10 h-10 rounded-full flex items-center justify-center bg-surface-container-lowest text-on-surface font-label-md text-label-md font-medium hover:bg-surface-container transition-colors shadow-sm">\\s*{p}\\s*</button>',
                f'<a href="{href}" class="w-10 h-10 rounded-full flex items-center justify-center bg-surface-container-lowest text-on-surface font-label-md text-label-md font-medium hover:bg-surface-container transition-colors shadow-sm">{p}</a>',
                content
            )
            
    # Fix Prev/Next
    prev_href = "products.html" if current_page == 2 else (f"products-{current_page-1}.html" if current_page > 2 else "#")
    next_href = f"products-{current_page+1}.html" if current_page < 3 else "#"
    
    if current_page == 1:
        content = re.sub(r'<button aria-label="Trang trước"[^>]*>[\s\S]*?</button>', f'<button aria-label="Trang trước" class="w-10 h-10 rounded-full flex items-center justify-center bg-surface-container-lowest text-on-surface-variant hover:bg-surface-container transition-colors shadow-sm disabled:opacity-40" disabled=""><span class="material-symbols-outlined text-base">chevron_left</span></button>', content)
    else:
        content = re.sub(r'<button aria-label="Trang trước"[^>]*>[\s\S]*?</button>', f'<a href="{prev_href}" aria-label="Trang trước" class="w-10 h-10 rounded-full flex items-center justify-center bg-surface-container-lowest text-on-surface font-label-md text-label-md font-medium hover:bg-surface-container transition-colors shadow-sm"><span class="material-symbols-outlined text-base">chevron_left</span></a>', content)
        content = re.sub(r'<a href="[^"]+" aria-label="Trang trước"[^>]*>[\s\S]*?</a>', f'<a href="{prev_href}" aria-label="Trang trước" class="w-10 h-10 rounded-full flex items-center justify-center bg-surface-container-lowest text-on-surface font-label-md text-label-md font-medium hover:bg-surface-container transition-colors shadow-sm"><span class="material-symbols-outlined text-base">chevron_left</span></a>', content)

    if current_page == 3:
        content = re.sub(r'<button aria-label="Trang tiếp theo"[^>]*>[\s\S]*?</button>', f'<button aria-label="Trang tiếp theo" class="px-space-md h-10 rounded-full flex items-center gap-1 bg-surface-container-lowest text-on-surface-variant hover:bg-surface-container transition-colors shadow-sm disabled:opacity-40" disabled="">Tiếp theo<span class="material-symbols-outlined text-base">chevron_right</span></button>', content)
        content = re.sub(r'<a href="[^"]+" aria-label="Trang tiếp theo"[^>]*>[\s\S]*?</a>', f'<button aria-label="Trang tiếp theo" class="px-space-md h-10 rounded-full flex items-center gap-1 bg-surface-container-lowest text-on-surface-variant hover:bg-surface-container transition-colors shadow-sm disabled:opacity-40" disabled="">Tiếp theo<span class="material-symbols-outlined text-base">chevron_right</span></button>', content)
    else:
        content = re.sub(r'<button aria-label="Trang tiếp theo"[^>]*>[\s\S]*?</button>', f'<a href="{next_href}" aria-label="Trang tiếp theo" class="px-space-md h-10 rounded-full flex items-center gap-1 bg-surface-container-lowest text-on-surface font-label-md text-label-md font-semibold hover:bg-surface-container transition-colors shadow-sm">Tiếp theo<span class="material-symbols-outlined text-base">chevron_right</span></a>', content)
        content = re.sub(r'<a href="[^"]+" aria-label="Trang tiếp theo"[^>]*>[\s\S]*?</a>', f'<a href="{next_href}" aria-label="Trang tiếp theo" class="px-space-md h-10 rounded-full flex items-center gap-1 bg-surface-container-lowest text-on-surface font-label-md text-label-md font-semibold hover:bg-surface-container transition-colors shadow-sm">Tiếp theo<span class="material-symbols-outlined text-base">chevron_right</span></a>', content)

    return content

# Read original
with open(products_html, "r", encoding="utf-8") as f:
    orig_content = f.read()

# Add p1_extra to products.html
grid_end_idx = orig_content.find('</div>\n<div class="mt-space-xl flex items-center justify-center gap-space-xs">')
if grid_end_idx == -1:
    grid_end_idx = orig_content.find('</div>\n<div class="mt-space-xl')

if grid_end_idx != -1:
    p1_content = orig_content[:grid_end_idx] + generate_html(p1_extra) + orig_content[grid_end_idx:]
    p1_content = update_pagination(p1_content, 1)
    with open(products_html, "w", encoding="utf-8") as f:
        f.write(p1_content)
else:
    print("Could not find grid end in products.html")

# Generate products-2.html and products-3.html by replacing the grid contents
grid_start_idx = orig_content.find('<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-space-md">') + len('<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-space-md">')
if grid_start_idx > len('<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-space-md">') - 1:
    
    # Page 2
    p2_content = orig_content[:grid_start_idx] + generate_html(p2_products) + orig_content[grid_end_idx:]
    p2_content = update_pagination(p2_content, 2)
    with open("products-2.html", "w", encoding="utf-8") as f:
        f.write(p2_content)
        
    # Page 3
    p3_content = orig_content[:grid_start_idx] + generate_html(p3_products) + orig_content[grid_end_idx:]
    p3_content = update_pagination(p3_content, 3)
    with open("products-3.html", "w", encoding="utf-8") as f:
        f.write(p3_content)

print("Done generating pages.")
