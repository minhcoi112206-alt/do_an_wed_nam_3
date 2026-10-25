import os
import re

filename = "about.html"
with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

new_main = """<main class="w-full pt-20 bg-surface">
    <!-- Phân cảnh 1: Ảnh nền lớn -->
    <section class="relative w-full h-[80vh] flex items-center justify-center bg-black overflow-hidden">
        <img src="https://images.unsplash.com/photo-1512054502232-10a0a035d672?auto=format&fit=crop&w=1920&q=80" alt="Apple Store Interior" class="absolute inset-0 w-full h-full object-cover opacity-60">
        <div class="relative z-10 text-center max-w-4xl px-4">
            <h1 class="text-5xl md:text-7xl font-bold text-white mb-6 tracking-tight">Khởi nguồn của sự hoàn mỹ.</h1>
            <p class="text-xl md:text-2xl text-gray-200 font-light">iStore VN/A - Nơi hội tụ tinh hoa công nghệ Apple.</p>
        </div>
    </section>

    <!-- Phân cảnh 2: Nội dung -->
    <section class="py-24 px-6 md:px-12 max-w-5xl mx-auto text-center">
        <h2 class="text-3xl md:text-5xl font-semibold text-on-surface mb-8">Tầm nhìn & Sứ mệnh</h2>
        <p class="text-lg md:text-xl text-on-surface-variant leading-relaxed mb-6">
            Chúng tôi sinh ra với một mục tiêu duy nhất: Mang những sản phẩm công nghệ tiên tiến nhất thế giới đến gần hơn với người dùng Việt Nam. 
            Mỗi thiết bị không chỉ là một cỗ máy, mà là cánh cửa mở ra sự sáng tạo không giới hạn.
        </p>
        <p class="text-lg md:text-xl text-on-surface-variant leading-relaxed">
            Là đối tác ủy quyền cao cấp, chúng tôi cam kết mọi sản phẩm bán ra đều là hàng chính hãng 100% VN/A với quy trình kiểm định khắt khe nhất.
        </p>
    </section>

    <!-- Phân cảnh 3: Ảnh nền lớn 2 -->
    <section class="relative w-full h-[80vh] flex items-center justify-center bg-black overflow-hidden">
        <img src="https://images.unsplash.com/photo-1491933382434-500287f9b54b?auto=format&fit=crop&w=1920&q=80" alt="Apple Products" class="absolute inset-0 w-full h-full object-cover opacity-60">
        <div class="relative z-10 text-center max-w-4xl px-4 text-white">
            <h2 class="text-4xl md:text-6xl font-bold mb-6 tracking-tight">Trải nghiệm đẳng cấp.</h2>
            <p class="text-xl text-gray-200 font-light">Không gian mua sắm được thiết kế dành riêng cho bạn.</p>
        </div>
    </section>

    <!-- Phân cảnh 4: Nội dung 2 -->
    <section class="py-24 px-6 md:px-12 max-w-5xl mx-auto text-center">
        <h2 class="text-3xl md:text-5xl font-semibold text-on-surface mb-8">Dịch vụ chuẩn 5 sao</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-12 mt-12">
            <div>
                <span class="material-symbols-outlined text-5xl text-primary mb-4">verified</span>
                <h3 class="text-2xl font-semibold mb-3">Chính hãng VN/A</h3>
                <p class="text-on-surface-variant">Bảo hành 12 tháng tại tất cả trung tâm bảo hành ủy quyền toàn quốc.</p>
            </div>
            <div>
                <span class="material-symbols-outlined text-5xl text-primary mb-4">local_shipping</span>
                <h3 class="text-2xl font-semibold mb-3">Giao hàng 2h</h3>
                <p class="text-on-surface-variant">Nhận máy ngay trong ngày miễn phí vận chuyển trên toàn quốc.</p>
            </div>
            <div>
                <span class="material-symbols-outlined text-5xl text-primary mb-4">autorenew</span>
                <h3 class="text-2xl font-semibold mb-3">Thu cũ đổi mới</h3>
                <p class="text-on-surface-variant">Trợ giá lên đời cao nhất thị trường. Đổi mới nhanh chóng, tiện lợi.</p>
            </div>
        </div>
    </section>

    <!-- Phân cảnh 5: Ảnh nền lớn 3 -->
    <section class="relative w-full h-[80vh] flex items-center justify-center bg-black overflow-hidden">
        <img src="https://images.unsplash.com/photo-1556656793-08538906a9f8?auto=format&fit=crop&w=1920&q=80" alt="iPhone" class="absolute inset-0 w-full h-full object-cover opacity-60">
        <div class="relative z-10 text-center max-w-4xl px-4 text-white">
            <h2 class="text-4xl md:text-6xl font-bold mb-6 tracking-tight">Sẵn sàng phục vụ.</h2>
            <p class="text-xl text-gray-200 font-light mb-8">Khám phá thế giới Apple ngay hôm nay.</p>
            <a href="products.html" class="inline-block bg-white text-black font-semibold text-lg px-8 py-4 rounded-full hover:bg-gray-200 transition-colors">
                Xem sản phẩm
            </a>
        </div>
    </section>
</main>"""

content = re.sub(r'<main.*?</main>', new_main, content, flags=re.DOTALL)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated about.html design.")
