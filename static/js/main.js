/* PASIFIQ STORE — Main JS */

document.addEventListener('DOMContentLoaded', () => {
    // ============ THEME TOGGLE ============
    const themeToggle = document.getElementById('themeToggle');
    const htmlElement = document.documentElement;
    const sunIcon = document.querySelector('.sun-icon');
    const moonIcon = document.querySelector('.moon-icon');

    const updateIcons = (theme) => {
        if (theme === 'dark') {
            if (sunIcon) sunIcon.style.display = 'none';
            if (moonIcon) moonIcon.style.display = 'block';
        } else {
            if (sunIcon) sunIcon.style.display = 'block';
            if (moonIcon) moonIcon.style.display = 'none';
        }
    };

    const applyTheme = (theme) => {
        htmlElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        updateIcons(theme);
    };

    // Initialize icons based on current theme (set by head script)
    updateIcons(htmlElement.getAttribute('data-theme'));

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = htmlElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            applyTheme(newTheme);
        });
    }

    // ============ MOBILE MENU ============
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('active');
            mobileMenuBtn.classList.toggle('active');
            document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
        });

        mobileMenu.addEventListener('click', (e) => {
            if (e.target === mobileMenu) {
                mobileMenu.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }

    // ============ FLASH MESSAGES ============
    document.querySelectorAll('.flash').forEach(el => {
        setTimeout(() => {
            el.style.opacity = '0';
            el.style.transform = 'translateX(100%)';
            setTimeout(() => el.remove(), 300);
        }, 5000);
    });

    // ============ SEARCH SUGGESTIONS ============
    const searchInput = document.getElementById('searchInput');
    const suggestionsBox = document.getElementById('searchSuggestions');

    if (searchInput && suggestionsBox) {
        let debounceTimer;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);
            const q = e.target.value.trim();
            if (q.length < 2) {
                suggestionsBox.innerHTML = '';
                suggestionsBox.classList.remove('visible');
                return;
            }
            debounceTimer = setTimeout(async () => {
                try {
                    const res = await fetch(`/search/suggestions/?q=${encodeURIComponent(q)}`);
                    const data = await res.json();
                    if (data.suggestions && data.suggestions.length > 0) {
                        suggestionsBox.innerHTML = data.suggestions.map(s => `<a class="suggestion-item" href="${s.url}">${s.name}</a>`).join('');
                        suggestionsBox.classList.add('visible');
                    } else {
                        suggestionsBox.innerHTML = '';
                        suggestionsBox.classList.remove('visible');
                    }
                } catch { }
            }, 300);
        });

        document.addEventListener('click', (e) => {
            if (!e.target.closest('.nav-search')) {
                suggestionsBox.classList.remove('visible');
            }
        });
    }

    // ============ WISHLIST AJAX ============
    document.querySelectorAll('.wishlist-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const productId = btn.dataset.productId;
            try {
                const res = await fetch(`/wishlist/toggle/${productId}/`, {
                    method: 'GET',
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });
                const data = await res.json();
                if (data.action === 'added') {
                    btn.classList.add('active');
                    btn.querySelector('svg').setAttribute('fill', 'currentColor');
                } else {
                    btn.classList.remove('active');
                    btn.querySelector('svg').setAttribute('fill', 'none');
                }
                // Update badge counts
                document.querySelectorAll('.nav-action-btn .badge').forEach(b => {
                    if (b.parentElement.href && b.parentElement.href.includes('wishlist')) {
                        b.textContent = data.count;
                        b.style.display = data.count > 0 ? 'flex' : 'none';
                    }
                });
            } catch { }
        });
    });

    // ============ COMPARE AJAX ============
    document.querySelectorAll('.compare-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const productId = btn.dataset.productId;
            try {
                const res = await fetch(`/compare/add/${productId}/`, {
                    method: 'GET',
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });
                const data = await res.json();
                if (data.error) { alert(data.error); return; }
                btn.classList.add('active');
                if (typeof showToast === 'function') {
                    showToast(`Added to comparison (${data.count})`);
                }
            } catch { }
        });
    });

    // ============ PRODUCT CARD CLICKABLE ============
    document.querySelectorAll('.product-card').forEach(card => {
        card.addEventListener('click', (e) => {
            // Prevent navigation if clicking on action buttons
            if (e.target.closest('.card-action-btn')) {
                return;
            }
            const url = card.dataset.url;
            if (url) {
                window.location.href = url;
            }
        });
    });

    // ============ WHATSAPP LINKS ============
    const storeWhatsapp = document.querySelector('meta[name="store-whatsapp"]')?.content || '';
    document.querySelectorAll('[id^="whatsapp"], [id*="WhatsApp"]').forEach(el => {
        if (storeWhatsapp) el.href = `https://wa.me/${storeWhatsapp.replace('+', '')}`;
    });

    // ============ SMOOTH SCROLL ============
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // ============ MOBILE FOOTER ACCORDION ============
    document.querySelectorAll('.footer-heading').forEach(header => {
        header.addEventListener('click', () => {
            if (window.innerWidth < 768) {
                const col = header.parentElement;
                col.classList.toggle('open');
            }
        });
    });
});

// Helper: Toast function (defined outside to be globally accessible)
function showToast(msg, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<span>${msg}</span><button class="toast-close" onclick="this.parentElement.remove()">✕</button>`;
    let container = document.querySelector('.toast-container');
    if (!container) {
        co