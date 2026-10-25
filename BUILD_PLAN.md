# 🚀 BUILD PLAN - MINH PHONE STORE

**Thời gian ước tính:** 12-15 ngày  
**Bắt đầu:** Ngày 9/10/2026  
**Dự kiến hoàn thành:** Ngày 24/10/2026

---

## PHASE 1: SECURITY AUDIT & FIXES (Days 1-3)
**Mục tiêu:** Eliminate SQL Injection, CSRF, Input Validation vulnerabilities

### Task 1.1: SQL Injection Prevention
**File cần sửa:**
- [ ] `products.php` - Line 30-50 (query building)
- [ ] `search.php`
- [ ] `admin/products.php`
- [ ] `admin/orders.php`
- [ ] `admin/inventory.php`
- [ ] `admin/reports.php`

**Action:**
```php
// ❌ BEFORE (Unsafe)
$sql = "SELECT * FROM products WHERE category_id = " . $_GET['category_id'];

// ✅ AFTER (Safe with prepared statements)
$stmt = db()->prepare("SELECT * FROM products WHERE category_id = ?");
$stmt->execute([(int)$_GET['category_id']]);
$products = $stmt->fetchAll();
```

### Task 1.2: Input Validation Function Library
**File:** `includes/functions.php`

**Add functions:**
```php
function validate_email(string $email): bool
function validate_phone(string $phone): bool
function validate_address(string $address): bool
function sanitize_string(string $input): string
function sanitize_int(mixed $input): int
function validate_required(array $fields, array $data): array // Returns errors
function csrf_token(): string
function verify_csrf(string $token = null): bool
function generate_csrf_token(): string
function flash(string $type, string $message): void
function get_flash(): array
```

### Task 1.3: CSRF Protection on All Forms
**File cần kiểm tra:**
- [ ] `login.php` - Form login
- [ ] `register.php` - Form register
- [ ] `checkout.php` - Form order
- [ ] `profile.php` - Form update profile
- [ ] `admin/login.php` - Admin login
- [ ] `admin/product-add.php` - Form add product
- [ ] `admin/product-edit.php` - Form edit
- [ ] `admin/categories.php` - Category forms
- [ ] `admin/users.php` - User forms

**Action:**
```php
// Trong form HTML
<form method="POST">
    <input type="hidden" name="csrf_token" value="<?= htmlspecialchars($_SESSION['csrf_token'] ?? '') ?>">
    <!-- form fields -->
</form>

// Trong file xử lý form
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!verify_csrf($_POST['csrf_token'] ?? '')) {
        die('CSRF token invalid');
    }
    // Process form...
}
```

### Task 1.4: HTTPOnly Cookies & Session Security
**File:** `includes/functions.php`

**Add:**
```php
ini_set('session.cookie_httponly', 1);
ini_set('session.cookie_secure', 1); // HTTPS only
ini_set('session.cookie_samesite', 'Strict');
ini_set('session.gc_maxlifetime', 1800); // 30 mins
```

---

## PHASE 2: DATABASE & PERFORMANCE (Days 4-6)
**Mục tiêu:** Add indexes, optimize queries, improve response time

### Task 2.1: Add Database Indexes
**File:** `database/schema.sql` + execute in MySQL

```sql
ALTER TABLE products ADD INDEX idx_category (category_id);
ALTER TABLE products ADD INDEX idx_status (status);
ALTER TABLE products ADD INDEX idx_featured (is_featured);
ALTER TABLE product_variants ADD INDEX idx_product (product_id);
ALTER TABLE product_variants ADD INDEX idx_sku (sku);
ALTER TABLE product_variants ADD INDEX idx_stock (stock_quantity);
ALTER TABLE orders ADD INDEX idx_user (user_id);
ALTER TABLE orders ADD INDEX idx_status (status);
ALTER TABLE orders ADD INDEX idx_created (created_at);
ALTER TABLE order_details ADD INDEX idx_order (order_id);
ALTER TABLE order_details ADD INDEX idx_variant (variant_id);
ALTER TABLE reviews ADD INDEX idx_product (product_id);
ALTER TABLE reviews ADD INDEX idx_user (user_id);
ALTER TABLE users ADD INDEX idx_email (email);
ALTER TABLE users ADD INDEX idx_status (status);
```

### Task 2.2: Optimize Product Queries
**File:** `products.php`

**Analysis:** Querie đã optimize tốt (GROUP BY, JOIN) ✅

**Task:** Kiểm tra thêm:
- [ ] Pagination limit (LIMIT clause)
- [ ] Query explain plan
- [ ] Add query result caching

### Task 2.3: Image Optimization
**File:** Create `includes/image-handler.php`

**Features:**
- Validate MIME type (not just extension)
- Resize image to 3 sizes: thumb (150px), display (400px), full (1200px)
- Compress with ImageMagick/GD
- Save with random hash name: `uploads/products/abc123def456.jpg`

```php
function handle_product_image(array $file): array|false
{
    // Check size < 5MB
    if ($file['size'] > 5242880) {
        return false;
    }
    
    // Check MIME type
    $finfo = finfo_open(FILEINFO_MIME_TYPE);
    $mime = finfo_file($finfo, $file['tmp_name']);
    if (!in_array($mime, ['image/jpeg', 'image/png', 'image/webp'])) {
        return false;
    }
    
    // Generate unique name
    $name = bin2hex(random_bytes(16)) . pathinfo($file['name'], PATHINFO_EXTENSION);
    $path = __DIR__ . '/../uploads/products/' . $name;
    
    // Resize & compress
    $image = imagecreatefromstring(file_get_contents($file['tmp_name']));
    // ... resize logic
    
    return ['path' => $path, 'url' => '/uploads/products/' . $name];
}
```

### Task 2.4: Add Caching Layer
**File:** `config/cache.php`

```php
// Simple APCu cache wrapper
function cache_get(string $key): mixed {
    return apcu_fetch($key, $hit) ? apcu_fetch($key) : null;
}

function cache_set(string $key, mixed $value, int $ttl = 3600): void {
    apcu_store($key, $value, $ttl);
}

function cache_delete(string $key): void {
    apcu_delete($key);
}
```

**Usage:**
- Cache categories on homepage
- Cache "Featured Products" 
- Cache popular searches

### Task 2.5: Error Handling & Logging
**File:** Create `config/logger.php`

```php
function log_error(Throwable $exception, string $level = 'error'): void
{
    $timestamp = date('Y-m-d H:i:s');
    $message = sprintf(
        "[%s] %s: %s (File: %s, Line: %d)\n",
        $timestamp,
        $level,
        $exception->getMessage(),
        $exception->getFile(),
        $exception->getLine()
    );
    
    error_log($message, 3, __DIR__ . '/../storage/logs/error.log');
}

// Usage in try-catch blocks
try {
    // code
} catch (PDOException $e) {
    log_error($e, 'database');
    http_response_code(500);
    die('Database error. Admin notified.');
}
```

---

## PHASE 3: FEATURES IMPLEMENTATION (Days 7-9)
**Mục tiêu:** Implement missing features from spec

### Task 3.1: Product Comparison Feature
**File:** `compare.php` (New implementation)

**Features:**
- Add button "Compare" on product cards
- Store variant_ids in session: `$_SESSION['compare'][]`
- Display comparison table
- Side-by-side specs

```php
<?php
$pageTitle = 'So sánh sản phẩm';
require_once __DIR__ . '/includes/header.php';

$compare_ids = $_SESSION['compare'] ?? [];

if (count($compare_ids) < 2) {
    echo '<p>Chọn ít nhất 2 sản phẩm để so sánh</p>';
} else {
    $stmt = db()->prepare("
        SELECT pv.*, p.product_name, p.description, p.warranty_months
        FROM product_variants pv
        JOIN products p ON p.product_id = pv.product_id
        WHERE pv.variant_id IN (" . implode(',', array_fill(0, count($compare_ids), '?')) . ")
    ");
    $stmt->execute($compare_ids);
    $variants = $stmt->fetchAll();
    
    // Display comparison table
}

require_once __DIR__ . '/includes/footer.php';
?>
```

### Task 3.2: Reviews & Ratings System
**File:** Create `includes/reviews.php`

**Database:**
```sql
-- Already in schema, just need UI implementation
SELECT * FROM reviews;
```

**Features:**
- Rate 1-5 stars
- Write review text
- Show average rating on product page
- Admin moderation (approve/reject)

**Files to create:**
- [ ] `includes/review-form.php` - Form component
- [ ] `includes/review-display.php` - Display component
- [ ] `product-detail.php` - Add review section
- [ ] `admin/reviews.php` - Admin moderation

### Task 3.3: Warranty Information Display
**File:** `warranty.php` (Enhance existing)

**Features:**
- Show warranty period
- Generate warranty certificate
- Track warranty claims
- Warranty expiry calculator

```php
function get_warranty_expiry(string $purchase_date, int $warranty_months): string
{
    $expiry = date('Y-m-d', strtotime($purchase_date . " +$warranty_months months"));
    return $expiry;
}

function is_within_warranty(string $purchase_date, int $warranty_months): bool
{
    $expiry = get_warranty_expiry($purchase_date, $warranty_months);
    return strtotime('now') <= strtotime($expiry);
}
```

### Task 3.4: Enhanced Search & Autocomplete
**File:** Create `api/search-autocomplete.php`

**API Endpoint:** `GET /api/search-autocomplete.php?q=iphone`

```php
<?php
header('Content-Type: application/json');

$q = trim($_GET['q'] ?? '');
if (strlen($q) < 2) {
    echo json_encode(['results' => []]);
    exit;
}

$stmt = db()->prepare("
    SELECT DISTINCT product_name, COUNT(*) as count
    FROM products
    WHERE product_name LIKE ? AND status = 1
    GROUP BY product_name
    LIMIT 10
");
$stmt->execute(['%' . $q . '%']);

echo json_encode(['results' => $stmt->fetchAll()]);
?>
```

### Task 3.5: Advanced Filtering
**File:** Enhance `products.php`

**Add filters:**
- [ ] RAM (if applicable)
- [ ] Brand
- [ ] Warranty period
- [ ] Availability (stock)
- [ ] Multiple colors/storage selection

---

## PHASE 4: TESTING & OPTIMIZATION (Days 10-12)
**Mục tiêu:** Unit tests, integration tests, performance testing

### Task 4.1: Unit Tests
**File:** Create `tests/` folder

**Using PHPUnit:**
```bash
composer require --dev phpunit/phpunit
```

**Tests to write:**
- [ ] `tests/Unit/ValidationTest.php` - Test validators
- [ ] `tests/Unit/ProductTest.php` - Test product logic
- [ ] `tests/Unit/OrderTest.php` - Test order logic

### Task 4.2: Integration Tests
**Files:**
- [ ] `tests/Integration/DatabaseTest.php`
- [ ] `tests/Integration/AuthTest.php`
- [ ] `tests/Integration/CartTest.php`

### Task 4.3: Performance Testing
**Tools:** Apache JMeter, Lighthouse

**Metrics:**
- [ ] Homepage load time < 2s
- [ ] Product list < 1.5s
- [ ] Product detail < 1s
- [ ] Checkout < 1.5s

### Task 4.4: Security Testing
**Checklist:**
- [ ] SQL Injection tests - PASS
- [ ] XSS tests - PASS
- [ ] CSRF tests - PASS
- [ ] Auth bypass tests - PASS
- [ ] Input validation tests - PASS

### Task 4.5: Mobile/Responsive Testing
**Devices to test:**
- [ ] iPhone 12/13/14 (375px width)
- [ ] iPad (768px width)
- [ ] Desktop (1920px width)

---

## PHASE 5: DEPLOYMENT & DOCUMENTATION (Days 13-15)
**Mục tiêu:** Production readiness, documentation, deployment

### Task 5.1: Create .env Configuration
**File:** `.env` (Create, add to .gitignore)

```env
DB_HOST=127.0.0.1
DB_NAME=iphone_store
DB_USER=root
DB_PASS=

SITE_URL=http://127.0.0.1:8000
SITE_NAME=Minh Phone Store

SESSION_TIMEOUT=1800
LOG_LEVEL=info

UPLOAD_MAX_SIZE=5242880
ALLOWED_EXTENSIONS=jpg,jpeg,png,webp
```

### Task 5.2: Production Checklist
- [ ] Set `display_errors = 0` in php.ini
- [ ] Enable HTTPS
- [ ] Set up database backups
- [ ] Configure error logging
- [ ] Set up monitoring/alerts
- [ ] Create admin recovery procedures
- [ ] Document API endpoints

### Task 5.3: API Documentation
**File:** Create `API.md`

**Document endpoints:**
- POST /api/products/search
- POST /api/cart/add
- POST /api/orders/create
- GET /api/user/profile
- etc.

### Task 5.4: User Documentation
**Files to create:**
- [ ] `USER_GUIDE.md` - For customers
- [ ] `ADMIN_GUIDE.md` - For admin
- [ ] `DEVELOPER_GUIDE.md` - For developers

### Task 5.5: Version Control & Release
- [ ] Initialize Git repository (if not already)
- [ ] Create meaningful commit history
- [ ] Tag release v1.1.0
- [ ] Create CHANGELOG.md

---

## 📊 EXECUTION CHECKLIST

### Day 1: Security Audit
- [ ] Identify all SQL injection points
- [ ] Document CSRF vulnerabilities
- [ ] Create validation function library
- [ ] List all input validation needs

### Day 2-3: Security Fixes
- [ ] Implement prepared statements across all files
- [ ] Add CSRF tokens to all forms
- [ ] Implement input validation
- [ ] Security test suite

### Day 4-5: Database Optimization
- [ ] Create index migration script
- [ ] Execute indexes
- [ ] Test query performance
- [ ] Implement caching

### Day 6: Performance Testing
- [ ] Load testing
- [ ] Identify bottlenecks
- [ ] Optimize slow queries
- [ ] Memory profiling

### Day 7-8: Feature Development
- [ ] Product comparison
- [ ] Reviews system
- [ ] Enhanced search
- [ ] Warranty tracking

### Day 9: Feature Testing
- [ ] Functional testing
- [ ] Edge case testing
- [ ] User acceptance testing

### Day 10-11: Full Test Suite
- [ ] Unit tests
- [ ] Integration tests
- [ ] Performance tests
- [ ] Security tests

### Day 12: Bug Fixes & Optimization
- [ ] Fix identified issues
- [ ] Optimize performance
- [ ] Code cleanup

### Day 13-14: Documentation
- [ ] API documentation
- [ ] User guides
- [ ] Developer guides
- [ ] Deployment manual

### Day 15: Release Preparation
- [ ] Final QA
- [ ] Deployment test
- [ ] Backup procedures
- [ ] Go-live checklist

---

## 🎯 SUCCESS CRITERIA

- ✅ Zero SQL injection vulnerabilities
- ✅ 100% CSRF protection on forms
- ✅ All inputs validated server-side
- ✅ Database indexes applied
- ✅ Homepage load < 2s
- ✅ All missing features implemented
- ✅ 80%+ test coverage
- ✅ Security audit passed
- ✅ Complete documentation
- ✅ Deployment automation ready

---

## 📞 SUPPORT & QUESTIONS

For questions about this plan, review:
1. IMPROVEMENT_PLAN.md - High-level issues
2. This BUILD_PLAN.md - Detailed tasks
3. Each file mentioned - For specific implementation details

**Next Step:** Start with Phase 1, Task 1.1 (SQL Injection Prevention)
