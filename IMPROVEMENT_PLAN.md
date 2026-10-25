# 📋 KẾ HOẠCH CẢI THIỆN - MINH PHONE STORE

**Ngày phân tích:** 9/10/2026  
**Phiên bản dự án:** 1.0  
**Trạng thái:** Cơ bản hoàn chỉnh → Cần tối ưu hóa

---

## 1. 🔴 CÁC VẤN ĐỀ QUAN TRỌNG (CRITICAL)

### 1.1 Không có Prepared Statements nhất quán
**Vị trí:** Nhiều file PHP (products.php, admin/products.php, v.v.)  
**Mức độ:** ⚠️ CRITICAL - Nguy cơ SQL Injection  
**Giải pháp:**
- Kiểm tra toàn bộ file PHP có sử dụng `$_GET`, `$_POST` trực tiếp
- Thay thế bằng prepared statements với placeholder `?`
- Audit tất cả queries

### 1.2 Không có Validation Input
**Vị trí:** Form đăng ký, checkout, admin  
**Mức độ:** ⚠️ CRITICAL  
**Giải pháp:**
- Thêm hàm `validate_email()`, `validate_phone()`, `validate_address()`
- Kiểm tra độ dài, format, required fields
- Server-side validation (không chỉ client)

### 1.3 CSRF Protection chưa đầy đủ
**Vị trí:** Tất cả form POST  
**Mức độ:** 🔴 HIGH  
**Giải pháp:**
- Kiểm tra token CSRF có được generate + verify ở tất cả form
- Thêm `<input type="hidden" name="csrf_token" value="<?= $_SESSION['csrf_token'] ?>">`
- Implement xoay CSRF token sau mỗi request

### 1.4 Không mã hóa Sensitive Data
**Vị trí:** Cookies, session  
**Mức độ:** 🔴 HIGH  
**Giải pháp:**
- Thêm `SameSite=Strict` cho cookies
- Set `httponly` flag cho session cookies
- Mã hóa dữ liệu nhạy cảm (SSN, credit card nếu có)

---

## 2. 🟡 CÁC VẤN ĐỀ HIỆU SUẤT (PERFORMANCE)

### 2.1 Không có Database Indexes
**Vị trí:** database/schema.sql  
**Mức độ:** 🟡 MEDIUM  
**Giải pháp:**
```sql
-- Thêm indexes
ALTER TABLE products ADD INDEX idx_category (category_id);
ALTER TABLE products ADD INDEX idx_status (status);
ALTER TABLE product_variants ADD INDEX idx_product (product_id);
ALTER TABLE product_variants ADD INDEX idx_sku (sku);
ALTER TABLE orders ADD INDEX idx_user (user_id);
ALTER TABLE orders ADD INDEX idx_status (status);
ALTER TABLE reviews ADD INDEX idx_product (product_id);
```

### 2.2 N+1 Query Problem
**Vị trí:** Loop qua products mà query từng product  
**Giải pháp:**
- Sử dụng JOIN thay vì loop query
- Ví dụ trong products.php đã sử dụng GROUP BY JOIN - tốt ✅
- Kiểm tra admin/products.php, admin/orders.php

### 2.3 Không có Caching
**Mức độ:** 🟡 MEDIUM  
**Giải pháp:**
- Cache categories ở header
- Cache popular products
- APCu hoặc Redis

### 2.4 Image Upload không tối ưu
**Vị trí:** admin/product-add.php  
**Mức độ:** 🟡 MEDIUM  
**Giải pháp:**
- Validate file type (mime check, không chỉ extension)
- Resize images (thumbnail, display, full size)
- Lưu vào storage/uploads/ với tên ngẫu nhiên
- Cleanup expired session files

---

## 3. 🟠 CÁC VẤN ĐỀ THIẾT KẾ CODE (CODE QUALITY)

### 3.1 Không có MVC Structure rõ ràng
**Hiện tại:** Procedural + inline SQL  
**Giải pháp:**
- Tạo folder `app/Models/` cho Database classes
- Tạo folder `app/Controllers/` cho logic
- Tạo `app/Services/` cho business logic

### 3.2 Hàm helpers chưa đầy đủ
**Vị trí:** includes/functions.php  
**Giải pháp:**
- Thêm `validate_*()` functions
- Thêm `sanitize_*()` functions
- Thêm `csrf_token()`, `verify_csrf()`
- Thêm `flash()`, `get_flash()` cho messages

### 3.3 Error Handling chưa professional
**Vị trí:** Tất cả file  
**Giải pháp:**
- Thêm try-catch blocks
- Log errors (file, database)
- Hiển thị friendly error messages cho user
- Không expose DB errors

### 3.4 Không có Constants & Config
**Giải pháp:**
- Tạo `config/constants.php`
- Tạo `.env` file cho credentials (production)
- Define PAGINATION_SIZE, UPLOAD_LIMIT, v.v.

---

## 4. 🔵 CÁC VẤN ĐỀ TÍNH NĂNG (FEATURES)

### 4.1 Giỏ hàng chỉ dùng SESSION
**Vị trí:** Session variables  
**Vấn đề:** Mất giỏ khi xóa cookies  
**Giải pháp:**
- Lưu giỏ vào database nếu user login
- Sync session với DB khi login
- Add "Save for later" feature

### 4.2 Không có Product Comparison
**Spec yêu cầu:** "So sánh sản phẩm"  
**Status:** ❌ Tính năng chưa implement  
**Giải pháp:**
- Tạo compare.php (đã có file nhưng trống)
- Lưu compare list ở session
- Hiển thị bảng so sánh specs

### 4.3 Không có Reviews/Ratings
**Vị trị:** Database có bảng reviews nhưng chưa dùng  
**Status:** ❌ Tính năng chưa implement  
**Giải pháp:**
- Tạo UI để submit review
- Moderation admin reviews
- Display review stars trên product

### 4.4 Không có Warranty Tracking
**Spec yêu cầu:** Thông tin bảo hành  
**Status:** ⚠️ Chưa tích hợp hoàn toàn  
**Giải pháp:**
- Tạo warranty.php (đã có)
- Link warranty với order details
- Show warranty expiry date

### 4.5 Tìm kiếm chưa advanced
**Giải pháp:**
- Thêm full-text search
- Autocomplete suggestions
- Save search history

---

## 5. 🎯 VỀ GIAO DIỆN (UI/UX)

### 5.1 Responsive Design
**Vị trí:** assets/css/style.css  
**Status:** ⚠️ Cần kiểm tra  
**Giải pháp:**
- Audit mobile view
- Thêm media queries
- Test trên Chrome DevTools

### 5.2 Loading Performance
**Giải pháp:**
- Minify CSS/JS
- Enable gzip compression
- Lazy load images
- Remove unused assets

### 5.3 Accessibility (a11y)
**Giải pháp:**
- Thêm alt text cho images
- Semantic HTML (nav, main, section, v.v.)
- ARIA labels
- Keyboard navigation

---

## 6. ✅ ĐIỂM CÓ LỢI

- ✅ Database schema hợp lý (12 bảng)
- ✅ PDO connection pool pattern
- ✅ `declare(strict_types=1)` sử dụng
- ✅ Responsive products.php query (GROUP BY, JOIN)
- ✅ Helper functions hữu ích (format_price, e(), media_url)
- ✅ Có session management
- ✅ Có prepared statements (nhưng chưa tất cả)

---

## 7. 📊 PRIORITY MATRIX

| Priority | Tasks | Effort | Impact |
|----------|-------|--------|--------|
| 🔴 CRITICAL | Input validation, SQL injection audit | 3 days | CRITICAL |
| 🟡 HIGH | CSRF all forms, DB indexes, Error handling | 2 days | HIGH |
| 🟠 MEDIUM | Caching, Image optimization, MVC refactor | 4 days | MEDIUM |
| 🟢 LOW | Accessibility, UI improvements | 2 days | LOW |

---

## 8. 📅 BUILD PLAN (Chi tiết trong BUILD_PLAN.md)

**Total Estimated Time:** 12-15 ngày làm việc

**Phases:**
1. **Phase 1 (Days 1-3):** Security Audit & Fixes
2. **Phase 2 (Days 4-6):** Database & Performance
3. **Phase 3 (Days 7-9):** Features Implementation
4. **Phase 4 (Days 10-12):** Testing & Optimization
5. **Phase 5 (Days 13-15):** Deployment & Documentation
