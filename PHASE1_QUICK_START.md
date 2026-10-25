# ⚡ QUICK START - Phase 1 (Days 1-3)

**Mục tiêu:** Fix SQL Injection, Input Validation, CSRF Protection  
**Ước tính:** 3 ngày  
**Bắt đầu:** Hôm nay (9/10/2026)

---

## 🎯 PHASE 1 OVERVIEW

### What You'll Accomplish
✅ Eliminate SQL injection vulnerabilities  
✅ Add input validation to all forms  
✅ Implement CSRF protection  
✅ Improve session security  

### Why It's Critical
🔴 Without these, your website can be:
- Database stolen/deleted
- User accounts hijacked
- Forms submitted by hackers
- Admin panel compromised

---

## 📝 STEP 1: AUDIT SQL INJECTION (2 hours)

### Task 1a: Scan All PHP Files

**Method 1: Manual (Recommended first time)**
```bash
# List all PHP files
Dir *.php /s
Dir admin/*.php

# Look for patterns like:
# - $_GET['..']
# - $_POST['..']
# - Direct string concatenation in SQL
# - Missing prepared statements
```

**Method 2: Using grep (if git bash installed)**
```bash
grep -r "SELECT.*\$" *.php admin/
grep -r "\$_GET\|\$_POST" *.php admin/ | grep -v "\?"
```

### Task 1b: Files to Check

**🔴 HIGH RISK files (likely to have SQL injection):**
```
1. products.php          (Line 30-50) ⚠️ BUILD DYNAMIC WHERE CLAUSE
2. search.php            (query building)
3. admin/products.php    (admin operations)
4. admin/orders.php      (order filtering)
5. admin/inventory.php   (inventory queries)
6. admin/reports.php     (report filtering)
7. admin/users.php       (user filtering)
```

**🟡 MEDIUM RISK files (partial):**
```
8. login.php             (email/username query)
9. checkout.php          (order creation)
10. cart.php             (if doing queries)
```

**🟢 LOW RISK files (already safe):**
```
✅ config/database.php   (connection only, no queries)
✅ includes/functions.php (helpers, not queries)
✅ index.php             (stitch template only)
```

### Task 1c: Example Vulnerable Code to Find

**Pattern 1: Direct string concatenation in WHERE clause**
```php
// ❌ VULNERABLE
$where[] = 'p.category_id = ' . $_GET['category_id'];
// Attacker: category_id = 1 OR 1=1 -- (returns all products)

// ✅ FIXED
$where[] = 'p.category_id = ?';
$params[] = (int) $_GET['category_id'];
```

**Pattern 2: User input in SELECT/FROM/ORDER BY**
```php
// ❌ VULNERABLE
$sort = $_GET['sort'];
$sql = "SELECT * FROM products ORDER BY " . $sort;
// Attacker: sort = RAND() UNION SELECT password FROM admins --

// ✅ FIXED
$sort = match($_GET['sort'] ?? '') {
    'price_asc' => 'price ASC',
    'price_desc' => 'price DESC',
    default => 'id DESC',
};
$sql = "SELECT * FROM products ORDER BY " . $sort;
```

**Pattern 3: LIKE with user input**
```php
// ❌ VULNERABLE
$q = $_GET['q'];
$sql = "SELECT * FROM products WHERE name LIKE '%$q%'";

// ✅ FIXED
$q = $_GET['q'];
$sql = "SELECT * FROM products WHERE name LIKE ?";
$stmt = db()->prepare($sql);
$stmt->execute(['%' . $q . '%']);
```

### Task 1d: Create Vulnerability Report

**Create file:** `SECURITY_AUDIT_PHASE1.md`

Document:
```markdown
## SQL Injection Audit Results

### Vulnerable Files Found

#### 1. products.php (Line 30-50)
Problem: WHERE clause built with string concatenation
Code:
    $where[] = 'p.category_id = ' . $_GET['category_id'];
Severity: CRITICAL
Fix: Use prepared statement parameter

#### 2. search.php
...

#### 3. admin/products.php
...
```

---

## 🛠️ STEP 2: CREATE VALIDATION FUNCTIONS (3-4 hours)

### Task 2a: Create validation.php

**File:** `includes/validation.php`

```php
<?php
declare(strict_types=1);

/**
 * Validation & Sanitization Functions
 */

/**
 * Validate email format
 */
function validate_email(string $email): bool
{
    return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
}

/**
 * Validate phone (Vietnam format: 10-11 digits)
 */
function validate_phone(string $phone): bool
{
    $phone = preg_replace('/[^0-9]/', '', $phone);
    return strlen($phone) >= 10 && strlen($phone) <= 11;
}

/**
 * Validate address (min 10 chars, max 255)
 */
function validate_address(string $address): bool
{
    $len = strlen(trim($address));
    return $len >= 10 && $len <= 255;
}

/**
 * Validate product quantity
 */
function validate_quantity(mixed $qty): bool
{
    $qty = (int)$qty;
    return $qty > 0 && $qty <= 1000;
}

/**
 * Validate price (positive number)
 */
function validate_price(mixed $price): bool
{
    $price = (float)$price;
    return $price > 0;
}

/**
 * Validate URL format
 */
function validate_url(string $url): bool
{
    return filter_var($url, FILTER_VALIDATE_URL) !== false;
}

/**
 * Validate required fields
 * 
 * @param array $required List of field names required
 * @param array $data POST/GET data
 * @return array List of missing fields
 */
function validate_required(array $required, array $data): array
{
    $missing = [];
    foreach ($required as $field) {
        $value = trim((string)($data[$field] ?? ''));
        if (empty($value)) {
            $missing[] = $field;
        }
    }
    return $missing;
}

/**
 * Sanitize string (remove potentially harmful characters)
 */
function sanitize_string(string $input): string
{
    return trim(htmlspecialchars($input, ENT_QUOTES, 'UTF-8'));
}

/**
 * Sanitize integer
 */
function sanitize_int(mixed $input): int
{
    return (int)filter_var($input, FILTER_SANITIZE_NUMBER_INT);
}

/**
 * Sanitize float
 */
function sanitize_float(mixed $input): float
{
    return (float)filter_var($input, FILTER_SANITIZE_NUMBER_FLOAT, 
        FILTER_FLAG_ALLOW_FRACTION);
}

/**
 * Validate file upload
 */
function validate_file_upload(array $file, array $config = []): array
{
    $errors = [];
    
    // Check if file was uploaded
    if ($file['error'] !== UPLOAD_ERR_OK) {
        $errors[] = 'File upload failed';
        return $errors;
    }
    
    // Get config
    $max_size = $config['max_size'] ?? 5242880; // 5MB default
    $allowed_types = $config['allowed_types'] ?? ['image/jpeg', 'image/png'];
    $allowed_ext = $config['allowed_ext'] ?? ['jpg', 'jpeg', 'png'];
    
    // Check file size
    if ($file['size'] > $max_size) {
        $errors[] = 'File too large (max ' . round($max_size/1024/1024) . 'MB)';
    }
    
    // Check MIME type (proper way, not extension)
    $finfo = finfo_open(FILEINFO_MIME_TYPE);
    $mime = finfo_file($finfo, $file['tmp_name']);
    finfo_close($finfo);
    
    if (!in_array($mime, $allowed_types)) {
        $errors[] = 'File type not allowed (allowed: ' . implode(', ', $allowed_types) . ')';
    }
    
    // Check extension as secondary check
    $ext = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
    if (!in_array($ext, $allowed_ext)) {
        $errors[] = 'File extension not allowed';
    }
    
    return $errors;
}

/**
 * Validate input against custom regex
 */
function validate_regex(string $value, string $pattern, string $error_msg = 'Invalid format'): array
{
    $errors = [];
    if (!preg_match($pattern, $value)) {
        $errors[] = $error_msg;
    }
    return $errors;
}

/**
 * Batch validate form data
 * 
 * @param array $data Form data
 * @param array $rules Validation rules
 * @return array Errors array
 * 
 * @example
 * $rules = [
 *     'email' => ['required', 'email'],
 *     'phone' => ['required', 'phone'],
 *     'password' => ['required', 'min:6'],
 * ];
 * $errors = validate_batch($_POST, $rules);
 */
function validate_batch(array $data, array $rules): array
{
    $errors = [];
    
    foreach ($rules as $field => $rule_list) {
        $value = $data[$field] ?? '';
        
        foreach ($rule_list as $rule) {
            if ($rule === 'required') {
                if (empty(trim((string)$value))) {
                    $errors[$field] = "Trường {$field} bắt buộc";
                }
            } elseif (str_starts_with($rule, 'min:')) {
                $min = (int)substr($rule, 4);
                if (strlen((string)$value) < $min) {
                    $errors[$field] = "Trường {$field} tối thiểu {$min} ký tự";
                }
            } elseif (str_starts_with($rule, 'max:')) {
                $max = (int)substr($rule, 4);
                if (strlen((string)$value) > $max) {
                    $errors[$field] = "Trường {$field} tối đa {$max} ký tự";
                }
            } elseif ($rule === 'email') {
                if (!validate_email((string)$value)) {
                    $errors[$field] = "Email không hợp lệ";
                }
            } elseif ($rule === 'phone') {
                if (!validate_phone((string)$value)) {
                    $errors[$field] = "Số điện thoại không hợp lệ";
                }
            }
        }
    }
    
    return $errors;
}
```

### Task 2b: Update includes/functions.php

**Add at top of file:**
```php
<?php
declare(strict_types=1);

// ... existing code ...

// Add after other includes
require_once __DIR__ . '/validation.php';
```

### Task 2c: Test Validation Functions

**Create file:** `test_validation.php`

```php
<?php
require_once __DIR__ . '/includes/functions.php';

// Test email validation
echo "Email test: " . (validate_email('test@example.com') ? 'PASS' : 'FAIL') . "\n";
echo "Email test (invalid): " . (!validate_email('invalid-email') ? 'PASS' : 'FAIL') . "\n";

// Test phone validation
echo "Phone test: " . (validate_phone('0987654321') ? 'PASS' : 'FAIL') . "\n";
echo "Phone test (invalid): " . (!validate_phone('123') ? 'PASS' : 'FAIL') . "\n";

// Test batch validation
$data = ['email' => 'test@example.com', 'phone' => '0987654321'];
$rules = ['email' => ['required', 'email'], 'phone' => ['required', 'phone']];
$errors = validate_batch($data, $rules);
echo "Batch validation: " . (empty($errors) ? 'PASS' : 'FAIL') . "\n";
```

---

## 🔐 STEP 3: FIX SQL INJECTION IN products.php (2 hours)

### Current Code (Line 1-60)
Review and identify unsafe patterns

### Fix Example

**Current (Unsafe):**
```php
$where = ['p.status = 1'];
$params = [];

if (!empty($_GET['category_id'])) {
    $where[] = 'p.category_id = ' . $_GET['category_id'];  // ❌ UNSAFE
}
```

**Fixed (Safe):**
```php
$where = ['p.status = 1'];
$params = [];

if (!empty($_GET['category_id'])) {
    $where[] = 'p.category_id = ?';
    $params[] = (int) $_GET['category_id'];  // ✅ SAFE
}
```

**Pattern for all similar cases:**
```php
// ❌ Before
$where[] = 'column = ' . $_GET['value'];

// ✅ After
$where[] = 'column = ?';
$params[] = $_GET['value'];  // or (int)$_GET['value'] if integer
```

### Files to Fix (Same Pattern)

Apply this pattern to:
1. ✅ products.php - Line 30-50
2. ⏳ search.php (if it has similar code)
3. ⏳ admin/products.php
4. ⏳ admin/orders.php
5. ⏳ admin/inventory.php

---

## 🛡️ STEP 4: ADD CSRF PROTECTION (2-3 hours)

### Task 4a: Add CSRF Functions to functions.php

**Add to includes/functions.php:**
```php
/**
 * Generate CSRF token
 */
function generate_csrf_token(): string
{
    if (!isset($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

/**
 * Verify CSRF token
 */
function verify_csrf(string $token = null): bool
{
    if ($token === null) {
        $token = $_POST['csrf_token'] ?? $_SERVER['HTTP_X_CSRF_TOKEN'] ?? '';
    }
    
    $session_token = $_SESSION['csrf_token'] ?? '';
    return $token !== '' && hash_equals($session_token, $token);
}

/**
 * Get CSRF token for use in forms
 */
function csrf_token(): string
{
    return e(generate_csrf_token());
}

/**
 * Flash message helper
 */
function flash(string $type, string $message): void
{
    $_SESSION['flash'] = [
        'type' => $type,
        'message' => $message
    ];
}

/**
 * Get and clear flash message
 */
function get_flash(): ?array
{
    $flash = $_SESSION['flash'] ?? null;
    unset($_SESSION['flash']);
    return $flash;
}
```

### Task 4b: Add CSRF Token to Forms

**Example 1: Login form**

**File:** `login.php`
```php
<form method="POST">
    <input type="hidden" name="csrf_token" value="<?= csrf_token() ?>">
    
    <input type="email" name="email" required>
    <input type="password" name="password" required>
    <button type="submit">Đăng nhập</button>
</form>
```

**Example 2: Checkout form**

**File:** `checkout.php`
```php
<form method="POST">
    <input type="hidden" name="csrf_token" value="<?= csrf_token() ?>">
    
    <input type="text" name="recipient_name" required>
    <input type="text" name="phone" required>
    <textarea name="shipping_address" required></textarea>
    
    <button type="submit">Đặt hàng</button>
</form>
```

### Task 4c: Verify CSRF in Form Handler

**In each POST handler:**
```php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Verify CSRF immediately
    if (!verify_csrf($_POST['csrf_token'] ?? '')) {
        flash('error', 'CSRF token không hợp lệ');
        redirect('form-page.php');
    }
    
    // Then process form
    // ...
}
```

### Files to Update (All forms)

```
1. login.php                  (Add CSRF token, verify in POST)
2. register.php               (Add CSRF token, verify in POST)
3. checkout.php               (Add CSRF token, verify in POST)
4. profile.php                (Add CSRF token, verify in POST)
5. cart-action.php            (Add CSRF token, verify in POST)
6. admin/login.php            (Add CSRF token, verify in POST)
7. admin/product-add.php      (Add CSRF token, verify in POST)
8. admin/product-edit.php     (Add CSRF token, verify in POST)
9. admin/categories.php       (Add CSRF token, verify in POST)
10. admin/users.php           (Add CSRF token, verify in POST)
```

---

## ✅ PHASE 1 COMPLETION CHECKLIST

### By End of Day 1
- [ ] SQL injection audit completed
- [ ] Created SECURITY_AUDIT_PHASE1.md
- [ ] 2-3 vulnerable files identified

### By End of Day 2
- [ ] validation.php created
- [ ] Validation functions tested
- [ ] CSRF functions added to functions.php
- [ ] SQL injection fixed in products.php

### By End of Day 3
- [ ] CSRF tokens added to all forms
- [ ] All forms verified for CSRF
- [ ] Error logging implemented
- [ ] Phase 1 testing completed

### Security Tests
```
Test 1: SQL Injection
  Input: category_id = 1 OR 1=1
  Expected: Only 1 product, not all
  Status: ✅ PASS

Test 2: CSRF Attack
  Try submitting form from different domain
  Expected: Form rejected with error
  Status: ✅ PASS

Test 3: Invalid Email
  Input: "not-an-email"
  Expected: Error message
  Status: ✅ PASS

Test 4: Empty Required Fields
  Input: (empty)
  Expected: Error message
  Status: ✅ PASS
```

---

## 🎯 SUCCESS CRITERIA (Phase 1)

✅ **All SQL injection vulnerabilities fixed**
- [ ] No user input directly in SQL strings
- [ ] All WHERE clauses use prepared statements
- [ ] Tested with malicious input

✅ **Input validation on all forms**
- [ ] Email validation working
- [ ] Phone validation working
- [ ] Address validation working
- [ ] Quantity validation working

✅ **CSRF protection complete**
- [ ] All POST forms have CSRF token
- [ ] All POST handlers verify token
- [ ] Tested from different domain

✅ **No critical security issues**
- [ ] Scan with security tools
- [ ] Manual code review
- [ ] Penetration test basic checks

---

## 🆘 TROUBLESHOOTING

### Error: "CSRF token invalid"
**Solution:** Make sure:
1. Token generated in form: `<?= csrf_token() ?>`
2. Token sent in form: `<input name="csrf_token" value="...">`
3. Token verified in handler: `verify_csrf($_POST['csrf_token'] ?? '')`

### Error: "File not found: validation.php"
**Solution:** Make sure:
1. File created at: `includes/validation.php`
2. Required in functions.php: `require_once __DIR__ . '/validation.php';`
3. Session started before calling functions

### Validation not working
**Solution:** Test functions independently:
```php
// Add to test file
var_dump(validate_email('test@example.com')); // Should be true
var_dump(validate_phone('0987654321'));       // Should be true
```

---

## 📞 NEED HELP?

1. Check IMPROVEMENT_PLAN.md for background
2. Check BUILD_PLAN.md for full details
3. Check SUMMARY.md for priorities
4. Review code examples above
5. Test functions independently first

**Next:** After completing Phase 1, start Phase 2: Database Optimization

Generated: 9/10/2026
