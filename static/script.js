// script.js - JavaScript for Doubt Sharing Platform

document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[required], textarea[required]');
            let isValid = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    showError(input, 'This field is required');
                } else {
                    clearError(input);

                }
            });

            if (!isValid) {
                e.preventDefault();
            }
        });
    });

    // Logout confirmation
    const logoutLinks = document.querySelectorAll('a[href="/logout"]');
    logoutLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to logout?')) {
                e.preventDefault();
            }
        });
    });

    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });

    // Add loading state to buttons (only for non-submit buttons)
    const buttons = document.querySelectorAll('.btn:not([type="submit"])');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const originalText = this.textContent;
            this.textContent = '⏳ Processing...';
            this.disabled = true;

            // Re-enable after 3 seconds (in case of error)
            setTimeout(() => {
                this.textContent = originalText;
                this.disabled = false;
            }, 3000);
        });
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Character counter for textareas
    const questionTextarea = document.getElementById('question');
    const answerTextarea = document.getElementById('answer');

    if (questionTextarea) {
        addCharCounter(questionTextarea, 1000);
    }

    if (answerTextarea) {
        addCharCounter(answerTextarea, 500);
    }
});

function showError(input, message) {
    clearError(input);
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    errorDiv.style.color = '#dc3545';
    errorDiv.style.fontSize = '0.875rem';
    errorDiv.style.marginTop = '0.25rem';
    input.parentNode.appendChild(errorDiv);
    input.style.borderColor = '#dc3545';
}

function clearError(input) {
    const existingError = input.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    input.style.borderColor = '#e1e5e9';
}

function addCharCounter(textarea, maxLength) {
    const counter = document.createElement('div');
    counter.className = 'char-counter';
    counter.style.fontSize = '0.875rem';
    counter.style.color = '#666';
    counter.style.textAlign = 'right';
    counter.style.marginTop = '0.25rem';

    textarea.parentNode.appendChild(counter);

    function updateCounter() {
        const remaining = maxLength - textarea.value.length;
        counter.textContent = `${remaining} characters remaining`;
        counter.style.color = remaining < 50 ? '#dc3545' : '#666';
    }

    textarea.addEventListener('input', updateCounter);
    updateCounter();
}

// Add some visual feedback for successful actions
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = message;
    successDiv.style.position = 'fixed';
    successDiv.style.top = '20px';
    successDiv.style.right = '20px';
    successDiv.style.background = '#28a745';
    successDiv.style.color = 'white';
    successDiv.style.padding = '1rem';
    successDiv.style.borderRadius = '8px';
    successDiv.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
    successDiv.style.zIndex = '1000';

    document.body.appendChild(successDiv);

    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}

// Check for success messages from server (you can set this in Flask routes)
const urlParams = new URLSearchParams(window.location.search);
if (urlParams.get('success')) {
    showSuccess(urlParams.get('success'));
}