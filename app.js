// Language Switcher
function switchLanguage(lang) {
    document.body.setAttribute('lang', lang);
    
    // Update active button
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');

    // Store preference
    localStorage.setItem('preferredLanguage', lang);
}

// Load saved language preference
window.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('preferredLanguage');
    if (savedLang && savedLang !== 'en') {
        const button = document.querySelector(`.lang-btn[onclick*="${savedLang}"]`);
        if (button) button.click();
    }
});

// Mobile Menu Toggle
function toggleMobileMenu() {
    const navLinks = document.getElementById('navLinks');
    navLinks.classList.toggle('mobile-open');
}

// Form Submission
document.getElementById('contactForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        name: this.name.value,
        company: this.company.value,
        email: this.email.value,
        message: this.message.value,
        language: document.body.getAttribute('lang') || 'en',
        timestamp: new Date().toISOString()
    };
    const toast = document.getElementById('toast');
    const toastMessage = toast.querySelector('.toast-message');
    
    try {
        const response = await fetch('https://techmirai-backend.onrender.com/api/contact', {
        //  const response = await fetch('http://localhost:8000/api/contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            const lang = document.body.getAttribute('lang');
            const message = lang === 'ja' 
                ? 'お問い合わせありがとうございます。<br>24時間以内にご返信いたします。'
                : 'Thank you for your inquiry!<br>We will respond within 24 hours.';
            
            showToast(message, 'success');
            this.reset();
        } else {
            throw new Error(result.message || 'Failed to submit');
        }
    } catch (error) {
        console.error('Error:', error);
        const lang = document.body.getAttribute('lang');
        const errorMsg = lang === 'ja'
            ? 'エラーが発生しました。<br>もう一度お試しください。'
            : 'An error occurred.<br>Please try again.';
        showToast(errorMsg, 'error');
    }
});
// Toast Function
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastContent = toast.querySelector('.toast-message');
    
    toastContent.innerHTML = message;
    toast.className = `toast ${type} show`;
    
    // Auto hide after 4 seconds
    setTimeout(() => {
        toast.classList.remove('show');
    }, 4000);
}

// Smooth Scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            // Close mobile menu after clicking
            const navLinks = document.getElementById('navLinks');
            navLinks.classList.remove('mobile-open');
        }
    });
});

// Close mobile menu when clicking outside
document.addEventListener('click', function(e) {
    const navLinks = document.getElementById('navLinks');
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    
    if (!navLinks.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
        navLinks.classList.remove('mobile-open');
    }
});