/* =====================================================
   Portfolio Website - JavaScript Interactions
   Shiva Pandey | StaxTech Internship
   ===================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initTypewriter();
    initScrollAnimations();
    initStatsCounter();
    initSkillBars();
    initProjectFilter();
    initContactForm();
    initSmoothScroll();
});

/* ---------- Navbar ---------- */
function initNavbar() {
    const navbar = document.getElementById('navbar');
    const toggle = document.getElementById('nav-toggle');
    const menu = document.getElementById('nav-menu');

    // Scroll effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Mobile toggle
    if (toggle && menu) {
        toggle.addEventListener('click', () => {
            toggle.classList.toggle('active');
            menu.classList.toggle('active');
        });

        // Close menu on link click
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                toggle.classList.remove('active');
                menu.classList.remove('active');
            });
        });
    }
}

/* ---------- Typewriter Effect ---------- */
function initTypewriter() {
    const element = document.getElementById('typewriter');
    if (!element) return;

    const words = ['Python Developer', 'Backend Engineer', 'Flask Developer', 'Problem Solver', 'B.Sc. IT Student'];
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typingSpeed = 100;

    function type() {
        const currentWord = words[wordIndex];

        if (isDeleting) {
            element.textContent = currentWord.substring(0, charIndex - 1);
            charIndex--;
            typingSpeed = 50;
        } else {
            element.textContent = currentWord.substring(0, charIndex + 1);
            charIndex++;
            typingSpeed = 100;
        }

        if (!isDeleting && charIndex === currentWord.length) {
            typingSpeed = 2000;
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            wordIndex = (wordIndex + 1) % words.length;
            typingSpeed = 500;
        }

        setTimeout(type, typingSpeed);
    }

    type();
}

/* ---------- Scroll Animations ---------- */
function initScrollAnimations() {
    const elements = document.querySelectorAll('.animate-on-scroll');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, index * 100);
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    elements.forEach(el => observer.observe(el));
}

/* ---------- Stats Counter ---------- */
function initStatsCounter() {
    const stats = document.querySelectorAll('.stat-number');
    if (!stats.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.getAttribute('data-count'));
                animateCounter(entry.target, target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    stats.forEach(stat => observer.observe(stat));
}

function animateCounter(element, target) {
    let current = 0;
    const increment = target / 50;
    const duration = 1500;
    const stepTime = duration / 50;

    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, stepTime);
}

/* ---------- Skill Bars ---------- */
function initSkillBars() {
    const bars = document.querySelectorAll('.skill-bar-fill, .exp-bar-fill');
    if (!bars.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const width = entry.target.getAttribute('data-width');
                setTimeout(() => {
                    entry.target.style.width = width + '%';
                }, 200);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });

    bars.forEach(bar => observer.observe(bar));
}

/* ---------- Project Filter ---------- */
function initProjectFilter() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-showcase-card');

    if (!filterBtns.length || !projectCards.length) return;

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active button
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.getAttribute('data-filter');

            projectCards.forEach((card, index) => {
                const category = card.getAttribute('data-category');

                if (filter === 'all' || category === filter) {
                    card.classList.remove('hidden');
                    card.style.animationDelay = `${index * 0.1}s`;
                } else {
                    card.classList.add('hidden');
                }
            });
        });
    });
}

/* ---------- Contact Form Validation ---------- */
function initContactForm() {
    const form = document.getElementById('contact-form');
    if (!form) return;

    const fields = [
        { id: 'name', errorId: 'name-error', validate: (v) => v.length >= 2 ? '' : 'Name must be at least 2 characters' },
        { id: 'email', errorId: 'email-error', validate: (v) => /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(v) ? '' : 'Enter a valid email address' },
        { id: 'subject', errorId: 'subject-error', validate: (v) => v.length > 0 ? '' : 'Subject is required' },
        { id: 'message', errorId: 'message-error', validate: (v) => v.length >= 10 ? '' : 'Message must be at least 10 characters' },
    ];

    // Real-time validation
    fields.forEach(field => {
        const input = document.getElementById(field.id);
        const error = document.getElementById(field.errorId);

        if (input && error) {
            input.addEventListener('blur', () => {
                const msg = field.validate(input.value.trim());
                error.textContent = msg;
                input.classList.toggle('error', !!msg);
            });

            input.addEventListener('input', () => {
                if (input.classList.contains('error')) {
                    const msg = field.validate(input.value.trim());
                    error.textContent = msg;
                    if (!msg) input.classList.remove('error');
                }
            });
        }
    });

    // Form submission validation
    form.addEventListener('submit', (e) => {
        let hasErrors = false;

        fields.forEach(field => {
            const input = document.getElementById(field.id);
            const error = document.getElementById(field.errorId);
            const msg = field.validate(input.value.trim());
            error.textContent = msg;
            input.classList.toggle('error', !!msg);
            if (msg) hasErrors = true;
        });

        if (hasErrors) {
            e.preventDefault();
            // Shake the submit button
            const btn = document.getElementById('submit-btn');
            btn.style.animation = 'shake 0.5s ease';
            setTimeout(() => btn.style.animation = '', 500);
        }
    });
}

/* ---------- Smooth Scroll ---------- */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

/* ---------- Shake Animation (for form errors) ---------- */
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        20% { transform: translateX(-8px); }
        40% { transform: translateX(8px); }
        60% { transform: translateX(-4px); }
        80% { transform: translateX(4px); }
    }
`;
document.head.appendChild(style);
