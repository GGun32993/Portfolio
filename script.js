/* ==========================================
   Main Script: Portfolio Interactions
   ========================================== */

document.addEventListener('DOMContentLoaded', () => {

    // ------------------------------------------
    // 0. Splash / Cover Screen
    // ------------------------------------------
    const splash = document.getElementById('splash');
    const splashBtn = document.getElementById('splashBtn');
    const splashTerminal = document.getElementById('splashTerminal');
    const splashParticles = document.getElementById('splashParticles');

    // Lock body scroll while splash is visible
    document.body.classList.add('splash-active');

    // Generate floating particles (Faster rise & quicker start)
    for (let i = 0; i < 30; i++) {
        const p = document.createElement('div');
        p.classList.add('splash-particle');
        p.style.left = Math.random() * 100 + '%';
        p.style.animationDuration = (2 + Math.random() * 3) + 's';
        p.style.animationDelay = Math.random() * 3 + 's';
        p.style.width = (1 + Math.random() * 2) + 'px';
        p.style.height = p.style.width;
        splashParticles.appendChild(p);
    }

    // Generate portfolio floating particles (gentle float for main page)
    const portfolioParticles = document.getElementById('portfolioParticles');
    if (portfolioParticles) {
        for (let i = 0; i < 40; i++) {
            const p = document.createElement('div');
            p.classList.add('portfolio-particle');
            p.style.left = Math.random() * 100 + '%';
            p.style.animationDuration = (6 + Math.random() * 8) + 's';
            p.style.animationDelay = Math.random() * 8 + 's';
            p.style.width = (1 + Math.random() * 2) + 'px';
            p.style.height = p.style.width;
            portfolioParticles.appendChild(p);
        }
    }

    // --- Pre-render all prompt labels so they don't shift ---
    const lines = splashTerminal.querySelectorAll('.splash-line');
    lines.forEach(lineEl => {
        const promptSpan = document.createElement('span');
        promptSpan.className = 's-prompt';
        promptSpan.textContent = lineEl.dataset.prompt;

        const textSpan = document.createElement('span');
        textSpan.className = 's-text';

        lineEl.appendChild(promptSpan);
        lineEl.appendChild(textSpan);
    });

    // --- Typewriter: type only the text part ---
    function typewriterLine(lineEl, isLast = false) {
        return new Promise(resolve => {
            const text = lineEl.dataset.text;
            const suffix = lineEl.dataset.suffix || '';
            const suffixClass = lineEl.dataset.suffixClass || '';
            const textSpan = lineEl.querySelector('.s-text');

            // Add blinking cursor
            const cursor = document.createElement('span');
            cursor.className = 's-cursor';
            lineEl.appendChild(cursor);

            let i = 0;
            const speed = 25;
            function type() {
                if (i < text.length) {
                    textSpan.textContent += text[i];
                    i++;
                    setTimeout(type, speed);
                } else {
                    if (suffix) {
                        const suffixSpan = document.createElement('span');
                        suffixSpan.className = suffixClass;
                        suffixSpan.textContent = suffix;
                        textSpan.appendChild(suffixSpan);
                    }
                    if (!isLast) {
                        cursor.classList.add('done');
                    }
                    resolve();
                }
            }
            type();
        });
    }

    // Run boot lines sequentially with a small pause between each
    async function runBootSequence() {
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const isLast = (i === lines.length - 1);
            await new Promise(r => setTimeout(r, 200));
            await typewriterLine(line, isLast);
        }
        setTimeout(() => {
            splashBtn.classList.add('show');
        }, 400);
    }

    runBootSequence();

    // --- Clean fade-out exit ---
    splashBtn.addEventListener('click', () => {
        splash.classList.add('exit');
        document.body.classList.remove('splash-active');

        setTimeout(() => {
            splash.remove();
            startRoleScramble();
        }, 700);
    });

    // --- Scramble/Glitch Text Effect for Terminal Role ---
    function scrambleText(element, targetWord, duration = 1200) {
        return new Promise((resolve) => {
            const chars = '!@#$%^&*()_+-=[]{}|;:,./<>?010101XYZ';
            const startWord = element.textContent;
            const startLen = startWord.length;
            const targetLen = targetWord.length;
            const startTime = performance.now();
            
            element.classList.add('scrambling');
            element.classList.remove('resolved');

            function update(now) {
                const elapsed = now - startTime;
                const progress = Math.min(elapsed / duration, 1);
                
                const freezeCount = Math.floor(progress * targetLen);
                const currentLen = Math.round(startLen + (targetLen - startLen) * progress);
                
                let result = '';
                for (let i = 0; i < currentLen; i++) {
                    if (i < freezeCount) {
                        result += targetWord[i];
                    } else if (i < targetLen) {
                        result += chars[Math.floor(Math.random() * chars.length)];
                    } else {
                        if (Math.random() > progress) {
                            result += chars[Math.floor(Math.random() * chars.length)];
                        }
                    }
                }
                
                element.textContent = result;
                
                if (progress < 1) {
                    requestAnimationFrame(update);
                } else {
                    element.textContent = targetWord;
                    element.classList.remove('scrambling');
                    element.classList.add('resolved');
                    resolve();
                }
            }
            
            requestAnimationFrame(update);
        });
    }

    async function startRoleScramble() {
        const roleWordEl = document.getElementById('terminal-role-word');
        if (!roleWordEl) return;

        // Start the scramble after 300ms delay to align with the terminal's fade-in animation
        await new Promise(resolve => setTimeout(resolve, 300));
        
        let currentWord = 'System';
        while (true) {
            await scrambleText(roleWordEl, currentWord, 1200);
            // Wait for 4 seconds before scrambling back
            await new Promise(resolve => setTimeout(resolve, 4000));
            currentWord = (currentWord === 'System') ? 'Network' : 'System';
        }
    }





    // ------------------------------------------
    // 1. Typing Animation (Hero Section)
    // ------------------------------------------
    const roles = [
        'System Engineer',
        'Network Engineer',
        'IT Admin & Support'
    ];

    const typedEl = document.getElementById('typedText');
    let roleIndex = 0;
    let charIndex = 0;
    let isDeleting = false;

    function typeText() {
        const current = roles[roleIndex];

        if (isDeleting) {
            typedEl.textContent = current.substring(0, charIndex - 1);
            charIndex--;
        } else {
            typedEl.textContent = current.substring(0, charIndex + 1);
            charIndex++;
        }

        let speed = isDeleting ? 40 : 80;

        if (!isDeleting && charIndex === current.length) {
            speed = 2000; // Pause at end
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            roleIndex = (roleIndex + 1) % roles.length;
            speed = 500; // Pause before next word
        }

        setTimeout(typeText, speed);
    }

    typeText();

    // ------------------------------------------
    // 2. Cursor Glow Effect
    // ------------------------------------------
    const glow = document.getElementById('cursorGlow');
    let mouseX = 0, mouseY = 0;
    let glowX = 0, glowY = 0;

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        glow.style.opacity = '1';
    });

    document.addEventListener('mouseleave', () => {
        glow.style.opacity = '0';
    });

    function animateGlow() {
        glowX += (mouseX - glowX) * 0.1;
        glowY += (mouseY - glowY) * 0.1;
        glow.style.left = glowX + 'px';
        glow.style.top = glowY + 'px';
        requestAnimationFrame(animateGlow);
    }
    animateGlow();

    // ------------------------------------------
    // 3. Navigation Scroll Effect
    // ------------------------------------------
    const nav = document.getElementById('nav');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    });

    // ------------------------------------------
    // 4. Mobile Menu Toggle
    // ------------------------------------------
    const navToggle = document.getElementById('navToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    let menuOpen = false;

    navToggle.addEventListener('click', () => {
        menuOpen = !menuOpen;
        mobileMenu.classList.toggle('open', menuOpen);
    });

    // Close mobile menu on link click
    document.querySelectorAll('.mobile-link').forEach(link => {
        link.addEventListener('click', () => {
            menuOpen = false;
            mobileMenu.classList.remove('open');
        });
    });

    // ------------------------------------------
    // 5. Scroll Reveal Animations
    // ------------------------------------------
    const revealElements = document.querySelectorAll('.reveal');

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const delay = entry.target.style.animationDelay || '0s';
                const delayMs = parseFloat(delay) * 1000;
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, delayMs);
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    revealElements.forEach(el => revealObserver.observe(el));

    // ------------------------------------------
    // 6. Skill Bar Animations
    // ------------------------------------------
    const skillBars = document.querySelectorAll('.skill-fill');

    const skillObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const width = entry.target.getAttribute('data-width');
                entry.target.style.width = width + '%';
                skillObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });

    skillBars.forEach(bar => skillObserver.observe(bar));

    // ------------------------------------------
    // 7. Counter Animation (Stats)
    // ------------------------------------------
    const statNumbers = document.querySelectorAll('.stat-number');

    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.getAttribute('data-count'));
                animateCounter(entry.target, target);
                counterObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    statNumbers.forEach(el => counterObserver.observe(el));

    function animateCounter(element, target) {
        let current = 0;
        const duration = 1500;
        const step = target / (duration / 16);

        function update() {
            current += step;
            if (current >= target) {
                element.textContent = target;
                return;
            }
            element.textContent = Math.floor(current);
            requestAnimationFrame(update);
        }
        update();
    }

    // ------------------------------------------
    // 8. Smooth Scroll for Anchor Links
    // ------------------------------------------
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

});
