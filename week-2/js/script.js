document.getElementById('feedbackForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    const email = document.getElementById('email').value.trim();
    const suggestions = document.getElementById('suggestions').value.trim();
    
    // Validation
    if (!firstName || !lastName) {
        alert('Full name is required.');
        return;
    }
    if (!email) {
        alert('Email is required.');
        return;
    }
    if (!isValidGmail(email)) {
        alert('Please enter a valid Gmail address (must end with @gmail.com). Current: ' + email);
        return;
    }
    
    // Sanitization
    const sanitizedFirstName = sanitizeInput(firstName);
    const sanitizedLastName = sanitizeInput(lastName);
    const sanitizedEmail = sanitizeInput(email);
    const sanitizedSuggestions = sanitizeInput(suggestions);
    
    // Store in localStorage
    const feedback = {
        firstName: sanitizedFirstName,
        lastName: sanitizedLastName,
        email: sanitizedEmail,
        suggestions: sanitizedSuggestions,
        timestamp: new Date().toISOString()
    };
    
    let feedbacks = JSON.parse(localStorage.getItem('feedbacks')) || [];
    feedbacks.push(feedback);
    localStorage.setItem('feedbacks', JSON.stringify(feedbacks));
    
    // Reset form
    this.reset();
    
    // Show success message with data
    const successMessage = `Feedback submitted successfully!\n\nName: ${feedback.firstName} ${feedback.lastName}\nEmail: ${feedback.email}\nSuggestions: ${feedback.suggestions || 'None'}\n\nTotal submissions: ${feedbacks.length}`;
    alert(successMessage);
});

function isValidGmail(email) {
    const gmailRegex = /^[^\s@]+@gmail\.com$/i;
    return gmailRegex.test(email);
}

function sanitizeInput(input) {
    // Basic sanitization: remove script tags and other potentially harmful content
    return input.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
                .replace(/<[^>]*>/g, ''); // Remove HTML tags
}