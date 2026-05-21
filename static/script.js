// Work4U - JavaScript + Animations

// ── Page Load ──────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {

    // Auto-dismiss alerts after 4 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 4000);
    });

    // ── Scroll Reveal ────────────────────────────────────────────
    const revealElements = document.querySelectorAll(
        '.card, .category-card, h2, .btn-lg, table, .badge'
    );

    revealElements.forEach(el => {
        el.classList.add('reveal');
    });

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, i) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, i * 60); // stagger delay
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    revealElements.forEach(el => observer.observe(el));

    // ── Navbar active link highlight ─────────────────────────────
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // ── Smooth page exit transition ──────────────────────────────
    document.querySelectorAll('a').forEach(link => {
        if (
            link.href &&
            link.href.startsWith(window.location.origin) &&
            !link.href.includes('#') &&
            link.target !== '_blank'
        ) {
            link.addEventListener('click', function (e) {
                const href = this.href;
                e.preventDefault();
                document.body.style.transition = 'opacity 0.25s ease';
                document.body.style.opacity = '0';
                setTimeout(() => {
                    window.location.href = href;
                }, 250);
            });
        }
    });

    // ── Counter Animation for stats (homepage) ───────────────────
    document.querySelectorAll('h3.fw-bold').forEach(el => {
        const text = el.innerText.trim();
        const match = text.match(/^(\d+)/);
        if (match) {
            const target = parseInt(match[1]);
            const suffix = text.replace(match[1], '');
            let count = 0;
            const duration = 800;
            const step = Math.ceil(target / (duration / 16));
            const timer = setInterval(() => {
                count = Math.min(count + step, target);
                el.innerText = count + suffix;
                if (count >= target) clearInterval(timer);
            }, 16);
        }
    });

});