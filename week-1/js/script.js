// ============================================
// Navigation & Hamburger Menu
// ============================================

const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');
const navLinks = document.querySelectorAll('.nav-link');

// Toggle hamburger menu
if (hamburger) {
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });
}

// Close menu when a link is clicked
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    });
});

// Highlight active navigation link
function updateActiveLink() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        const href = link.getAttribute('href');
        if (href === currentPage || (currentPage === '' && href === 'index.html')) {
            link.classList.add('active');
        }
    });
}

// Update active link on page load
document.addEventListener('DOMContentLoaded', updateActiveLink);

// ============================================
// Contact Form Validation & Submission
// ============================================

const contactForm = document.getElementById('contactForm');

if (contactForm) {
    // Form validation rules
    const validationRules = {
        name: {
            validate: (value) => value.trim().length >= 2,
            error: 'Please enter a valid name (at least 2 characters)'
        },
        email: {
            validate: (value) => {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                return emailRegex.test(value);
            },
            error: 'Please enter a valid email address'
        },
        phone: {
            validate: (value) => {
                if (value.trim() === '') return true; // Optional field
                const phoneRegex = /^[\d\s\-\+\(\)]+$/;
                return phoneRegex.test(value) && value.trim().length >= 10;
            },
            error: 'Please enter a valid phone number'
        },
        subject: {
            validate: (value) => value.trim().length >= 3,
            error: 'Please enter a subject (at least 3 characters)'
        },
        message: {
            validate: (value) => value.trim().length >= 10,
            error: 'Please enter a message (at least 10 characters)'
        }
    };

    // Validate individual field
    function validateField(fieldName) {
        const field = document.getElementById(fieldName);
        const errorElement = document.getElementById(fieldName + 'Error');
        const rule = validationRules[fieldName];

        if (field.type === 'email' && field.value.trim() === '' && !field.required) {
            // Skip validation for optional email fields
            field.classList.remove('error');
            if (errorElement) errorElement.textContent = '';
            return true;
        }

        const isValid = rule.validate(field.value);

        if (!isValid && (field.value.trim() || field.required)) {
            field.classList.add('error');
            if (errorElement) errorElement.textContent = rule.error;
            return false;
        } else {
            field.classList.remove('error');
            if (errorElement) errorElement.textContent = '';
            return true;
        }
    }

    // Real-time validation on input
    Object.keys(validationRules).forEach(fieldName => {
        const field = document.getElementById(fieldName);
        if (field) {
            field.addEventListener('blur', () => validateField(fieldName));
            field.addEventListener('input', () => {
                if (field.classList.contains('error')) {
                    validateField(fieldName);
                }
            });
        }
    });

    // Handle form submission
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();

        // Validate all fields
        let isFormValid = true;
        Object.keys(validationRules).forEach(fieldName => {
            if (!validateField(fieldName)) {
                isFormValid = false;
            }
        });

        if (isFormValid) {
            // Collect form data
            const formData = {
                name: document.getElementById('name').value.trim(),
                email: document.getElementById('email').value.trim(),
                phone: document.getElementById('phone').value.trim(),
                subject: document.getElementById('subject').value.trim(),
                message: document.getElementById('message').value.trim(),
                timestamp: new Date().toISOString()
            };

            // Log to console (dummy submission)
            console.log('Form submitted successfully!', formData);

            // Show success message
            const successMessage = document.getElementById('successMessage');
            if (successMessage) {
                successMessage.classList.add('show');

                // Hide success message after 5 seconds
                setTimeout(() => {
                    successMessage.classList.remove('show');
                }, 5000);
            }

            // Reset form
            contactForm.reset();

            // Optional: Send to a backend service (comment out for dummy submission)
            // sendFormData(formData);

            // Scroll to success message
            setTimeout(() => {
                successMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 100);
        } else {
            console.log('Form validation failed');
        }
    });
}

// ============================================
// Optional: Dummy API call (commented out)
// ============================================

/*
async function sendFormData(formData) {
    try {
        const response = await fetch('https://api.example.com/contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            console.log('Form data sent successfully');
        } else {
            console.error('Error sending form data');
        }
    } catch (error) {
        console.error('Network error:', error);
    }
}
*/

// ============================================
// Smooth Scrolling Enhancement
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    // Add smooth scrolling for anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            const target = document.querySelector(href);
            
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// ============================================
// Lazy Loading for Images (optional)
// ============================================

if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ============================================
// Utility: Log app initialization
// ============================================

console.log('Portfolio website loaded successfully!');
