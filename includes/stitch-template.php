<?php
declare(strict_types=1);

function render_stitch_template(string $screen): never
{
    $file = __DIR__ . '/../stitch_buildmart_premium_b2b_platform/' . $screen . '/code.html';
    if (!is_file($file)) {
        http_response_code(404);
        exit('Không tìm thấy template Stitch.');
    }

    $html = file_get_contents($file);
    $bridge = <<<'HTML'
<script>
(() => {
  const routeByText = [
    [/^iPhone$/i, 'products.php'],
    [/^So Sánh$/i, 'compare.php'],
    [/^Phụ Kiện$/i, 'categories.php'],
    [/^Thu Cũ Đổi Mới$/i, 'products.php'],
    [/^Khuyến Mãi$/i, 'products.php?sort=price_asc'],
    [/^Hỗ Trợ$/i, 'contact.php'],
    [/Trang chủ/i, 'index.php'],
    [/Tất cả sản phẩm|Xem 18 Ưu Đãi|Xem ưu đãi/i, 'products.php'],
    [/Chi tiết cấu hình|Tìm hiểu thêm|Chi tiết/i, 'product-detail.php?id=1'],
    [/Chính sách|Bảo hành/i, 'warranty.php'],
    [/Điều khoản|Bảo mật|Tra cứu/i, 'contact.php'],
    [/iPhone\s?\d|Like New|AirPods|Phụ kiện/i, 'products.php']
  ];

  const toast = (message, tone = 'success') => {
    let box = document.getElementById('stitch-toast');
    if (!box) {
      box = document.createElement('div');
      box.id = 'stitch-toast';
      box.style.cssText = 'position:fixed;left:50%;bottom:28px;transform:translateX(-50%);z-index:9999;max-width:min(520px,calc(100% - 32px));padding:14px 18px;border-radius:999px;font:600 14px Inter,system-ui;box-shadow:0 20px 44px rgba(0,0,0,.18);transition:opacity .2s ease;background:#1d1d1f;color:#fff';
      document.body.appendChild(box);
    }
    box.textContent = message;
    box.style.background = tone === 'error' ? '#ba1a1a' : '#1d1d1f';
    box.style.opacity = '1';
    clearTimeout(window.__stitchToastTimer);
    window.__stitchToastTimer = setTimeout(() => { box.style.opacity = '0'; }, 2600);
  };

  const updateCartBadges = (count) => {
    document.querySelectorAll('#cartCountBadge').forEach((el) => { el.textContent = String(count); });
    document.querySelectorAll('button[aria-label="Giỏ hàng"] span.absolute, .cart-link strong').forEach((el) => {
      if (/^\d+$/.test((el.textContent || '').trim())) el.textContent = String(count);
    });
  };

  fetch('stitch-action.php?action=count')
    .then((res) => res.json())
    .then((data) => data.ok && updateCartBadges(data.count))
    .catch(() => {});

  const addToServerCart = async (name, price, redirectTo = '') => {
    const body = new URLSearchParams({ action: 'add', product_name: name || 'iPhone', quantity: '1' });
    const response = await fetch('stitch-action.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body
    });
    const data = await response.json();
    if (!data.ok) throw new Error(data.message || 'Không thể thêm vào giỏ hàng.');
    updateCartBadges(data.count);
    toast(`${name || 'Sản phẩm'} đã được thêm vào giỏ hàng${price ? ' - ' + price : ''}.`);
    if (redirectTo) setTimeout(() => { window.location.href = redirectTo; }, 450);
    return data;
  };

  window.addToCartMock = (name, price) => {
    addToServerCart(name, price).then(() => {
      if (typeof window.toggleCartDrawer === 'function') window.toggleCartDrawer();
    }).catch((error) => toast(error.message, 'error'));
  };

  document.querySelectorAll('a').forEach((link) => {
    const text = (link.textContent || '').replace(/\s+/g, ' ').trim();
    for (const [pattern, href] of routeByText) {
      if (pattern.test(text)) {
        link.setAttribute('href', href);
        break;
      }
    }
  });

  document.querySelectorAll('input[placeholder*="Tìm"]').forEach((input) => {
    input.addEventListener('keydown', (event) => {
      if (event.key !== 'Enter') return;
      event.preventDefault();
      const query = input.value.trim();
      window.location.href = 'products.php' + (query ? `?q=${encodeURIComponent(query)}` : '');
    });
  });

  document.querySelectorAll('button[aria-label="Giỏ hàng"]').forEach((button) => {
    button.addEventListener('click', (event) => {
      event.preventDefault();
      if (typeof window.toggleCartDrawer === 'function' && document.getElementById('miniCartDrawer')) {
        window.toggleCartDrawer();
      } else {
        window.location.href = 'cart.php';
      }
    });
  });

  document.querySelectorAll('img[alt="Profile"]').forEach((avatar) => {
    avatar.style.cursor = 'pointer';
    avatar.addEventListener('click', () => { window.location.href = 'login.php'; });
  });

  document.querySelectorAll('.series-tab, #seriesTabs button').forEach((button) => {
    button.addEventListener('click', () => {
      const label = (button.textContent || '').replace(/\s+/g, ' ').trim();
      window.location.href = 'products.php?series=' + encodeURIComponent(label);
    });
  });

  document.querySelectorAll('button').forEach((button) => {
    const label = (button.textContent || '').replace(/\s+/g, ' ').trim();
    let handled = false;
    if (/^(Mua ngay|Mua ngay VN\/A)/i.test(label)) {
      handled = true;
      button.addEventListener('click', (event) => {
        event.preventDefault();
        const card = button.closest('article, .group, section, main') || document;
        const title = card.querySelector('h1,h2,h3')?.textContent?.trim() || document.querySelector('h1')?.textContent?.trim() || 'iPhone';
        const price = card.querySelector('.text-primary, #price-display')?.textContent?.trim() || '';
        addToServerCart(title, price, 'checkout.php').catch((error) => toast(error.message, 'error'));
      });
    }
    if (/Thêm vào giỏ/i.test(label) && !button.getAttribute('onclick')) {
      handled = true;
      button.addEventListener('click', (event) => {
        event.preventDefault();
        const card = button.closest('article, .group, section, main') || document;
        const title = card.querySelector('h1,h2,h3')?.textContent?.trim() || 'iPhone';
        const price = card.querySelector('.text-primary, #price-display')?.textContent?.trim() || '';
        addToServerCart(title, price).catch((error) => toast(error.message, 'error'));
      });
    }
    if (/Đặt lịch|Chat Zalo|Tổng đài|Đánh giá/i.test(label)) {
      handled = true;
      button.addEventListener('click', () => toast('Cảm ơn bạn. Nhân viên Minh Phone sẽ liên hệ hỗ trợ.'));
    }
    if (!handled && !button.getAttribute('onclick') && button.type !== 'submit') {
      button.addEventListener('click', () => {
        const text = label || button.title || button.getAttribute('aria-label') || 'Tùy chọn';
        if (/Bán chạy|Ưu đãi|Trả góp|Sẵn hàng|Series|GB|Titan|Màu|Lọc|sao|Đã mua/i.test(text)) {
          button.parentElement?.querySelectorAll('button').forEach((btn) => btn.classList.remove('ring-2', 'ring-primary', 'bg-primary', 'text-on-primary'));
          button.classList.add('ring-2', 'ring-primary');
          toast(`Đã chọn: ${text}.`);
        }
      });
    }
  });

  document.querySelectorAll('a').forEach((link) => {
    const label = (link.textContent || '').replace(/\s+/g, ' ').trim();
    if (/Chat Zalo/i.test(label)) {
      link.addEventListener('click', (event) => {
        event.preventDefault();
        toast('Zalo CSKH đã sẵn sàng. Bạn có thể gọi hotline 1800 6868 để được hỗ trợ nhanh.');
      });
    }
  });

  const priceRange = document.getElementById('price-range');
  const priceDisplay = document.getElementById('price-display');
  if (priceRange && priceDisplay) {
    const updatePrice = () => { priceDisplay.textContent = `10Tr - ${Number(priceRange.value).toFixed(0)}Tr`; };
    priceRange.addEventListener('input', updatePrice);
    updatePrice();
  }

  document.getElementById('reset-filter-btn')?.addEventListener('click', () => {
    document.querySelectorAll('input[type="checkbox"]').forEach((input, index) => { input.checked = index < 2; });
    document.querySelectorAll('input[type="radio"]').forEach((input, index) => { input.checked = index === 0; });
    if (priceRange) priceRange.value = priceRange.max || '50';
    if (priceRange) priceRange.dispatchEvent(new Event('input'));
    toast('Đã đặt lại bộ lọc.');
  });

  document.querySelectorAll('aside input, aside button, #sort-select').forEach((control) => {
    control.addEventListener('change', () => toast('Bộ lọc đã được cập nhật.'));
    control.addEventListener('click', () => {
      if (control.tagName === 'BUTTON' && !/Đặt lại/.test(control.textContent || '')) {
        control.parentElement?.querySelectorAll('button').forEach((b) => b.classList.remove('bg-primary', 'text-on-primary', 'bg-primary-fixed'));
        control.classList.add('bg-primary', 'text-on-primary');
      }
    });
  });

  document.querySelectorAll('[aria-label*="Trang"], button').forEach((button) => {
    const text = (button.textContent || '').trim();
    if (/^[2-9]$|Trang tiếp theo|Trang trước/.test(text) || button.getAttribute('aria-label')?.includes('Trang')) {
      button.addEventListener('click', () => toast('Phân trang demo đã được chọn. Dữ liệu sản phẩm nằm trong trang hiện tại.'));
    }
  });

  if (typeof window.changeAngle !== 'function') {
    window.changeAngle = (index, button) => {
      const main = document.getElementById('main-product-img');
      const img = button?.querySelector('img');
      if (main && img?.src) main.src = img.src;
      document.querySelectorAll('.gallery-thumb').forEach((thumb) => thumb.classList.remove('active-thumb'));
      button?.classList.add('active-thumb');
    };
  }

  if (typeof window.selectColor !== 'function') {
    window.selectColor = (name, button) => {
      const label = document.getElementById('color-name-label');
      if (label) label.textContent = name;
      document.querySelectorAll('.color-btn').forEach((btn) => btn.classList.remove('active-color'));
      button?.classList.add('active-color');
    };
  }

  if (typeof window.selectStorage !== 'function') {
    window.selectStorage = (storage, price, original, button) => {
      const priceEl = document.getElementById('price-display');
      const originalEl = document.getElementById('original-price');
      if (priceEl) priceEl.textContent = price;
      if (originalEl) originalEl.textContent = original;
      document.querySelectorAll('.storage-btn').forEach((btn) => btn.classList.remove('active-storage'));
      button?.classList.add('active-storage');
    };
  }

  if (typeof window.updateDevice !== 'function') {
    window.updateDevice = () => toast('Đã đổi mẫu iPhone trong bảng so sánh.');
  }
  if (typeof window.toggleOnlyDifferences !== 'function') {
    window.toggleOnlyDifferences = () => toast('Đang hiển thị các điểm khác biệt nổi bật.');
  }
  if (typeof window.showAllSpecs !== 'function') {
    window.showAllSpecs = () => toast('Đã hiển thị toàn bộ thông số.');
  }

  if (typeof window.calculateTradeIn !== 'function') {
    window.calculateTradeIn = () => {
      const model = document.getElementById('tradein-model');
      const base = document.getElementById('baseValDisplay');
      const total = document.getElementById('totalBenefitDisplay');
      const value = model?.value || '';
      const amount = value.includes('15') ? 16500000 : value.includes('14') ? 12500000 : 8500000;
      if (base) base.textContent = amount.toLocaleString('vi-VN') + '₫';
      if (total) total.textContent = (amount + 2000000).toLocaleString('vi-VN') + '₫';
    };
  }
  if (typeof window.setCondition !== 'function') {
    window.setCondition = (ratio, button) => {
      document.querySelectorAll('.cond-btn').forEach((btn) => btn.classList.remove('bg-primary', 'text-on-primary'));
      button?.classList.add('bg-primary', 'text-on-primary');
      window.calculateTradeIn?.();
      toast(`Đã chọn tình trạng máy, hệ số định giá ${Math.round(ratio * 100)}%.`);
    };
  }
})();
</script>
HTML;

    echo str_replace('</body>', $bridge . '</body>', $html);
    exit;
}
