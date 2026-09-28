/**
 * FlowerPower — Основной JavaScript
 * Все интерактивные функции сайта
 */

document.addEventListener('DOMContentLoaded', function() {

    // ============================================================
    // 1. FAQ — АККОРДЕОН
    // ============================================================
    function toggleFaq(element) {
        const item = element.closest('.faq-item');
        const isActive = item.classList.contains('active');

        // Закрываем все открытые
        document.querySelectorAll('.faq-item.active').forEach(el => {
            if (el !== item) {
                el.classList.remove('active');
            }
        });

        // Переключаем текущий
        if (isActive) {
            item.classList.remove('active');
        } else {
            item.classList.add('active');
        }
    }

    // Автоматически открываем первый FAQ
    const firstFaq = document.querySelector('.faq-item');
    if (firstFaq) {
        firstFaq.classList.add('active');
    }

    // Делаем функцию глобальной для onclick в HTML
    window.toggleFaq = toggleFaq;


    // ============================================================
    // 2. КНОПКИ КОЛИЧЕСТВА В КАТАЛОГЕ
    // ============================================================
    function changeQuantity(btn, delta) {
        const input = btn.closest('.quantity-selector').querySelector('.qty-input');
        if (!input) return;

        let val = parseInt(input.value) || 1;
        val = val + delta;

        if (val < 1) val = 1;
        if (val > 99) val = 99;

        input.value = val;
    }

    // Делаем функцию глобальной
    window.changeQuantity = changeQuantity;

    // Также добавляем обработчики для ручного ввода
    document.querySelectorAll('.qty-input').forEach(input => {
        input.addEventListener('change', function() {
            let val = parseInt(this.value) || 1;
            if (val < 1) val = 1;
            if (val > 99) val = 99;
            this.value = val;
        });

        input.addEventListener('blur', function() {
            let val = parseInt(this.value) || 1;
            if (val < 1) val = 1;
            if (val > 99) val = 99;
            this.value = val;
        });
    });


    // ============================================================
    // 4. ПОИСК — АВТОФОКУС ПО НАЖАТИЮ "/"
    // ============================================================
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        document.addEventListener('keydown', function(e) {
            if (e.key === '/' && !['INPUT', 'TEXTAREA'].includes(e.target.tagName)) {
                e.preventDefault();
                searchInput.focus();
            }
        });
    }


    // ============================================================
    // 5. ОТЗЫВЫ — ЗВЁЗДНЫЙ РЕЙТИНГ
    // ============================================================
    const ratingInputs = document.querySelectorAll('.rating-input input[type="radio"]');
    ratingInputs.forEach(input => {
        input.addEventListener('change', function() {
            const labels = this.closest('.rating-input').querySelectorAll('label');
            const value = parseInt(this.value);

            labels.forEach((label, index) => {
                const starValue = labels.length - index;
                if (starValue <= value) {
                    label.style.color = '#f5a623';
                } else {
                    label.style.color = '#ddd';
                }
            });
        });
    });


    // ============================================================
    // 6. УВЕДОМЛЕНИЯ — АВТО-СКРЫТИЕ ЧЕРЕЗ 5 СЕКУНД
    // ============================================================
    const messages = document.querySelectorAll('.message');
    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.transition = 'opacity 0.5s ease';
            msg.style.opacity = '0';
            setTimeout(() => {
                if (msg.parentNode) {
                    msg.remove();
                }
            }, 500);
        }, 5000);
    });


    // ============================================================
    // 7. КНОПКА "НАВЕРХ"
    // ============================================================
    const scrollBtn = document.createElement('button');
    scrollBtn.innerHTML = '↑';
    scrollBtn.className = 'scroll-top-btn';
    scrollBtn.setAttribute('aria-label', 'Наверх');
    scrollBtn.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 48px;
        height: 48px;
        background: #1a1a1a;
        color: #fff;
        border: none;
        border-radius: 50%;
        font-size: 22px;
        cursor: pointer;
        z-index: 999;
        opacity: 0;
        transition: opacity 0.3s ease, transform 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        transform: scale(0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Inter', sans-serif;
    `;

    document.body.appendChild(scrollBtn);

    window.addEventListener('scroll', function() {
        if (window.scrollY > 400) {
            scrollBtn.style.opacity = '1';
            scrollBtn.style.transform = 'scale(1)';
        } else {
            scrollBtn.style.opacity = '0';
            scrollBtn.style.transform = 'scale(0.8)';
        }
    });

    scrollBtn.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    scrollBtn.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.1)';
        this.style.background = '#333';
    });

    scrollBtn.addEventListener('mouseleave', function() {
        if (window.scrollY > 400) {
            this.style.transform = 'scale(1)';
        }
        this.style.background = '#1a1a1a';
    });


    // ============================================================
    // 8. ПЛАВНАЯ ПРОКРУТКА ДЛЯ ЯКОРНЫХ ССЫЛОК
    // ============================================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });


    // ============================================================
    // 9. АНИМАЦИЯ ПОЯВЛЕНИЯ ЭЛЕМЕНТОВ ПРИ СКРОЛЛЕ
    // ============================================================
    if ('IntersectionObserver' in window) {
        const animateElements = document.querySelectorAll(
            '.feature-card, .category-card, .product-card, .review-card, .faq-item'
        );

        const animationObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    animationObserver.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        animateElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            animationObserver.observe(el);
        });
    }


    // ============================================================
    // 10. ЛЕНИВАЯ ЗАГРУЗКА ИЗОБРАЖЕНИЙ
    // ============================================================
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });

        lazyImages.forEach(img => {
            imageObserver.observe(img);
        });
    }

    // ============================================================
    // 12. ДОБАВЛЕНИЕ В КОРЗИНУ С АНИМАЦИЕЙ
    // ============================================================
    document.querySelectorAll('.add-to-cart-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const btn = this.querySelector('.btn-add-cart');
            if (btn) {
                const originalText = btn.textContent;
                btn.textContent = '✓ Добавлено!';
                btn.style.background = '#1a7a3a';

                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.style.background = '#1a1a1a';
                }, 2000);
            }
        });
    });


    // ============================================================
    // 13. КОРЗИНА — ОБНОВЛЕНИЕ КОЛИЧЕСТВА ЧЕРЕЗ КНОПКИ
    // ============================================================
    document.querySelectorAll('.cart-item-quantity .qty-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const form = this.closest('form');
            if (form) {
                const action = this.value || 'set';
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'action';
                input.value = action;
                form.appendChild(input);
                form.submit();
            }
        });
    });


    // ============================================================
    // 14. НАВБАР — ИЗМЕНЕНИЕ ПРИ СКРОЛЛЕ
    // ============================================================
    const navbar = document.querySelector('.navbar');
    let lastScrollY = window.scrollY;

    window.addEventListener('scroll', function() {
        const currentScrollY = window.scrollY;
        
        if (currentScrollY > 50) {
            navbar.style.boxShadow = '0 8px 40px rgba(0, 0, 0, 0.08)';
            navbar.style.background = 'rgba(255, 255, 255, 0.9)';
        } else {
            navbar.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.06)';
            navbar.style.background = 'rgba(255, 255, 255, 0.75)';
        }

        lastScrollY = currentScrollY;
    });


    // ============================================================
    // 15. ФИЛЬТРЫ В КАТАЛОГЕ — ПОДСКАЗКА
    // ============================================================
    const filterSelects = document.querySelectorAll('.catalog-filters select');
    filterSelects.forEach(select => {
        select.addEventListener('change', function() {
            // Стилизация при выборе
            if (this.value) {
                this.style.borderColor = '#1a1a1a';
            } else {
                this.style.borderColor = '#e0e0e0';
            }
        });
    });


    // ============================================================
    // 16. ПАРАЛЛАКС ЭФФЕКТ ДЛЯ HERO (ОСТРОВОК)
    // ============================================================
    const hero = document.querySelector('.hero');
    if (hero) {
        const heroImage = hero.querySelector('.hero-image');
        const glassOverlay = hero.querySelector('.glass-overlay');
        
        if (heroImage) {
            window.addEventListener('scroll', function() {
                const scrolled = window.scrollY;
                if (scrolled < hero.offsetHeight) {
                    const speed = 0.3;
                    const translateY = scrolled * speed;
                    heroImage.style.transform = `translateY(${translateY}px)`;
                    
                    if (glassOverlay) {
                        const opacity = 1 - (scrolled / hero.offsetHeight) * 0.4;
                        glassOverlay.style.opacity = Math.max(opacity, 0.3);
                    }
                }
            });
        }
    }


    // ============================================================
    // 17. КОРЗИНА — ПОДСЧЕТ ИТОГО ПРИ ИЗМЕНЕНИИ
    // ============================================================
    const cartQuantityInputs = document.querySelectorAll('.cart-item-quantity input[type="number"]');
    cartQuantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const form = this.closest('form');
            if (form) {
                const actionInput = document.createElement('input');
                actionInput.type = 'hidden';
                actionInput.name = 'action';
                actionInput.value = 'set';
                form.appendChild(actionInput);
            }
        });
    });


    // ============================================================
    // 18. ФОРМА ОТЗЫВА — ВАЛИДАЦИЯ
    // ============================================================
    const reviewForm = document.querySelector('.review-form form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', function(e) {
            const text = this.querySelector('textarea[name="text"]');
            if (text && text.value.trim().length < 10) {
                e.preventDefault();
                alert('Пожалуйста, напишите более подробный отзыв (минимум 10 символов).');
                text.focus();
            }
        });
    }


    // ============================================================
    // 19. КОРЗИНА — ПРОВЕРКА ПЕРЕД ОФОРМЛЕНИЕМ
    // ============================================================
    const checkoutBtn = document.querySelector('.btn-checkout-cart, .btn-checkout');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', function(e) {
            const cartItems = document.querySelectorAll('.cart-item');
            if (cartItems.length === 0) {
                e.preventDefault();
                alert('Ваша корзина пуста. Добавьте товары перед оформлением заказа.');
            }
        });
    }


    // ============================================================
    // 20. СТИЛИЗАЦИЯ АКТИВНЫХ ФИЛЬТРОВ
    // ============================================================
    const activeFilters = document.querySelectorAll('.catalog-filters select option:checked');
    activeFilters.forEach(option => {
        if (option.value) {
            const select = option.closest('select');
            if (select) {
                select.style.borderColor = '#1a1a1a';
            }
        }
    });


    console.log('✦ FlowerPower — сайт успешно загружен!');
});