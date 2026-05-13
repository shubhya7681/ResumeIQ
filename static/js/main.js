/**
 * ResumeIQ - Main JavaScript
 * Handles navigation, animations, and interactive UI components.
 */

// ─── Navbar Scroll Effect ──────────────────────────────────────────────
const navbar = document.getElementById('mainNav');
window.addEventListener('scroll', () => {
    if (navbar) {
        navbar.classList.toggle('scrolled', window.scrollY > 50);
    }
});

// ─── Mobile Navigation Toggle ──────────────────────────────────────────
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');
if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('open');
        navToggle.classList.toggle('active');
    });
    // Close on link click
    navLinks.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('open');
            navToggle.classList.remove('active');
        });
    });
}

// ─── Scroll Animations (Intersection Observer) ────────────────────────
const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));

// ─── Flash Message Auto-dismiss ────────────────────────────────────────
document.querySelectorAll('.flash-message').forEach(msg => {
    setTimeout(() => {
        msg.style.opacity = '0';
        msg.style.transform = 'translateX(100%)';
        setTimeout(() => msg.remove(), 400);
    }, 5000);
});

// ─── Password Toggle ──────────────────────────────────────────────────
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = input.parentElement.querySelector('.password-toggle i');
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.replace('fa-eye-slash', 'fa-eye');
    }
}

// ─── Smooth Scroll for Anchor Links ────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// ─── Counter Animation for Hero Stats ──────────────────────────────────
function animateCounters() {
    document.querySelectorAll('.hero-stat-number').forEach(el => {
        const target = parseInt(el.dataset.count);
        if (!target) return;
        const suffix = el.textContent.includes('+') ? '+' : el.textContent.includes('%') ? '%' : '';
        let current = 0;
        const increment = target / 60;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            el.textContent = Math.floor(current).toLocaleString() + suffix;
        }, 20);
    });
}

// Run counter animation when hero is visible
const heroSection = document.getElementById('hero');
if (heroSection) {
    const heroObserver = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) {
            animateCounters();
            heroObserver.disconnect();
        }
    });
    heroObserver.observe(heroSection);
}

// ─── Job Match Bar Animation ───────────────────────────────────────────
document.querySelectorAll('.job-match-fill').forEach(bar => {
    const observer = new IntersectionObserver(entries => {
        if (entries[0].isIntersecting) {
            // Width is set inline, just trigger the CSS transition
            observer.disconnect();
        }
    });
    observer.observe(bar);
});

console.log('⚡ ResumeIQ loaded successfully');

// ─── Chatbot Logic ────────────────────────────────────────────────────────
const chatbotToggle = document.getElementById('chatbotToggle');
const chatbotContainer = document.getElementById('chatbotContainer');
const chatbotClose = document.getElementById('chatbotClose');
const chatbotInput = document.getElementById('chatbotInput');
const chatbotSend = document.getElementById('chatbotSend');
const chatbotMessages = document.getElementById('chatbotMessages');

if (chatbotToggle && chatbotContainer) {
    // Toggle chat visibility
    function toggleChat() {
        const isHidden = chatbotContainer.style.display === 'none';
        if (isHidden) {
            chatbotContainer.style.display = 'flex';
            chatbotToggle.querySelector('.fa-comment-dots').style.display = 'none';
            chatbotToggle.querySelector('.fa-times').style.display = 'block';
            setTimeout(() => chatbotInput.focus(), 300);
            
            // Auto-scroll to bottom on open
            chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        } else {
            chatbotContainer.style.display = 'none';
            chatbotToggle.querySelector('.fa-comment-dots').style.display = 'block';
            chatbotToggle.querySelector('.fa-times').style.display = 'none';
        }
    }

    chatbotToggle.addEventListener('click', toggleChat);
    chatbotClose.addEventListener('click', toggleChat);

    // Add a message to the UI
    function appendMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-message ${sender}-message`;
        
        // Convert Markdown-style bold and lists to basic HTML for rendering
        let formattedText = text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n/g, '<br>');
            
        msgDiv.innerHTML = `<div class="message-content">${formattedText}</div>`;
        chatbotMessages.appendChild(msgDiv);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // Show typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chatbot-typing';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = '<span></span><span></span><span></span>';
        chatbotMessages.appendChild(typingDiv);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // Remove typing indicator
    function removeTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.remove();
        }
    }

    // Handle sending message
    async function sendMessage() {
        const text = chatbotInput.value.trim();
        if (!text) return;

        // Add user message
        appendMessage(text, 'user');
        chatbotInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();

        try {
            // Call API
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();
            
            // Remove typing indicator
            removeTypingIndicator();
            
            // Show bot response
            appendMessage(data.response, 'bot');
        } catch (error) {
            console.error('Chat error:', error);
            removeTypingIndicator();
            appendMessage("Sorry, I'm having trouble connecting to the server right now.", 'bot');
        }
    }

    // Event listeners for sending
    chatbotSend.addEventListener('click', sendMessage);
    chatbotInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
}
