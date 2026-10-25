# Minh Phone Store (iStore VN/A - Apple Premium Reseller)

Website bán điện thoại/iPhone với **Frontend 100% HTML, CSS (Tailwind) & JavaScript thuần**, có hệ thống quản trị admin backend PHP & MySQL.

## Cấu trúc Frontend (100% HTML / CSS / JS)

Toàn bộ giao diện khách hàng (Storefront) đã được chuẩn hóa **100% HTML** với thiết kế hiện đại, tương thích tốt trên mọi thiết bị và không yêu cầu máy chủ PHP để hiển thị:

- [index.html](file:///index.html): Trang chủ Apple Storefront cao cấp (Hero Billboard, iPhone 17/16, khuyến mãi giao 2h, so sánh).
- [products.html](file:///products.html), [products-2.html](file:///products-2.html), [products-3.html](file:///products-3.html): Danh sách sản phẩm (iPhone mới VN/A, máy Like New 99%, phụ kiện Apple).
- [product-detail.html](file:///product-detail.html): Trang chi tiết sản phẩm đầy đủ cấu hình, chọn màu, chọn dung lượng, nút "Mua ngay" và "Thêm vào giỏ".
- [categories.html](file:///categories.html): Phân loại danh mục theo từng series iPhone và hệ sinh thái Apple.
- [cart.html](file:///cart.html): Giỏ hàng tương tác 100% HTML/JS (tăng giảm số lượng, xóa sản phẩm, áp dụng voucher `MINH500`, `MINHPHONE10`, `APPLEVIP`).
- [checkout.html](file:///checkout.html): Thanh toán đơn hàng với 4 phương thức (COD, VietQR tự động, Thẻ tín dụng, Trả góp 0%), lưu đơn hàng vào `localStorage`.
- [login.html](file:///login.html): Đăng nhập tài khoản khách hàng (hỗ trợ nút 1-chạm đăng nhập tài khoản mẫu).
- [register.html](file:///register.html): Đăng ký tài khoản thành viên mới.
- [profile.html](file:///profile.html): Quản lý hồ sơ cá nhân, đổi mật khẩu, xem thống kê chi tiêu và lịch sử đơn hàng.
- [logout.html](file:///logout.html): Đăng xuất tài khoản an toàn và chuyển về trang chủ.
- [my-orders.html](file:///my-orders.html): Quản lý danh sách đơn hàng đã đặt, trạng thái giao vận.
- [order-detail.html](file:///order-detail.html): Chi tiết từng đơn hàng, hành trình vận chuyển hỏa tốc.
- [compare.html](file:///compare.html): Công cụ so sánh thông số kỹ thuật các đời iPhone.
- [search.html](file:///search.html): Tìm kiếm sản phẩm theo tên và phân loại.
- [about.html](file:///about.html): Giới thiệu hệ thống cửa hàng.
- [contact.html](file:///contact.html): Thông tin hỗ trợ và liên hệ CSKH.
- [warranty.html](file:///warranty.html): Chính sách bảo hành 12 tháng 1-đổi-1.
- [returns.html](file:///returns.html): Chính sách đổi trả 30 ngày.

## Quản lý trạng thái Frontend (Client Store)

- File lưu trữ: `assets/js/store.js`
- Quản lý đồng bộ:
  - Giỏ hàng (`localStorage: minhphone_cart`)
  - Tài khoản đăng nhập (`localStorage: minhphone_user`)
  - Danh sách đơn hàng (`localStorage: minhphone_orders`)
  - Mã giảm giá (`localStorage: minhphone_coupon`)
  - Badge số lượng giỏ hàng tự động cập nhật trên toàn bộ các trang.

## Cách chạy dự án

1. **Chạy Frontend (100% HTML)**:
   - Có thể mở trực tiếp file `index.html` trên trình duyệt bằng cách nhấp đúp chuột hoặc dùng Live Server / bất kỳ static web server nào (VSCode Live Server, http-server, serve,...).
   - Hoặc mở qua PowerShell:
     ```powershell
     Start-Process "index.html"
     ```

2. **Chạy Backend Quản trị (Admin PHP + MySQL)**:
   - Mở XAMPP Control Panel và bật Apache + MySQL.
   - Import CSDL từ file `database/schema.sql`.
   - Cấu hình kết nối MySQL trong `config/database.php`.
   - Đăng nhập admin: `http://127.0.0.1:8000/admin/login.php` (tài khoản: `admin` / `admin123`).

## Tài khoản mẫu thử nghiệm

- **Khách hàng**: `minh@example.com` / `admin123` (có nút đăng nhập nhanh 1 chạm tại `login.html`)
- **Admin**: `admin` / `admin123`

