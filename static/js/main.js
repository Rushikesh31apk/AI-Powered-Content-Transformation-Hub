// Main JavaScript file for AI Hub

// Copy to clipboard function
function copyToClipboard() {
    const textarea = document.querySelector('.result-box textarea');
    if (textarea) {
        textarea.select();
        document.execCommand('copy');
        
        // Show feedback
        const btn = event.target;
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="bi bi-check2 me-2"></i>Copied!';
        btn.classList.remove('btn-secondary');
        btn.classList.add('btn-success');
        
        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.classList.remove('btn-success');
            btn.classList.add('btn-secondary');
        }, 2000);
    }
}

// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});

// File upload preview
const fileInputs = document.querySelectorAll('input[type="file"]');
fileInputs.forEach(input => {
    input.addEventListener('change', function(e) {
        const fileName = e.target.files[0]?.name;
        if (fileName) {
            console.log('File selected:', fileName);
        }
    });
});

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Add animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.feature-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'all 0.5s ease-out';
    observer.observe(card);
});

// Console welcome message
console.log('%cAI Hub', 'color: #f5c518; font-size: 24px; font-weight: bold;');
console.log('%cWelcome to AI-Powered Content Transformation Hub!', 'color: #f5c518; font-size: 14px;');
console.log('%cSavitribai Phule Pune University', 'color: #999; font-size: 12px;');