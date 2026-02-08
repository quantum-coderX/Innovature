document.getElementById('feedbackForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const message = document.getElementById('message').value.trim();
    
    // Validation
    if (!name) {
        alert('Name is required.');
        return;
    }
    if (!email || !isValidEmail(email)) {
        alert('Please enter a valid email.');
        return;
    }
    if (!message) {
        alert('Message is required.');
        return;
    }
    
    // Sanitization
    const sanitizedName = sanitizeInput(name);
    const sanitizedEmail = sanitizeInput(email);
    const sanitizedMessage = sanitizeInput(message);
    
    // Store in localStorage
    const feedback = {
        name: sanitizedName,
        email: sanitizedEmail,
        message: sanitizedMessage,
        timestamp: new Date().toISOString()
    };
    
    let feedbacks = JSON.parse(localStorage.getItem('feedbacks')) || [];
    feedbacks.push(feedback);
    localStorage.setItem('feedbacks', JSON.stringify(feedbacks));
    
    // Reset form
    this.reset();
    alert('Feedback submitted successfully!');
});

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function sanitizeInput(input) {
    // Basic sanitization: remove script tags and other potentially harmful content
    return input.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
                .replace(/<[^>]*>/g, ''); // Remove HTML tags
}