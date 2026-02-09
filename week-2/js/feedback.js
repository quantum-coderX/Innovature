const itemsPerPage = 5;
let currentPage = 1;
let feedbacks = [];

document.addEventListener('DOMContentLoaded', function() {
    feedbacks = JSON.parse(localStorage.getItem('feedbacks')) || [];
    displayFeedbacks();
});

function displayFeedbacks() {
    const feedbackList = document.getElementById('feedbackList');
    const emptyState = document.getElementById('emptyState');
    feedbackList.innerHTML = '';

    if (feedbacks.length === 0) {
        emptyState.style.display = 'block';
        return;
    } else {
        emptyState.style.display = 'none';
    }

    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const pageFeedbacks = feedbacks.slice(start, end);

    pageFeedbacks.forEach((feedback, index) => {
        const feedbackDiv = document.createElement('div');
        feedbackDiv.className = 'feedback-item';

        // Get first letter of name for avatar
        const firstLetter = feedback.firstName ? feedback.firstName.charAt(0).toUpperCase() : 'U';

        const headerDiv = document.createElement('div');
        headerDiv.className = 'feedback-item-header';

        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'feedback-avatar';
        avatarDiv.textContent = firstLetter;

        const metaDiv = document.createElement('div');
        metaDiv.className = 'feedback-meta';

        const nameP = document.createElement('p');
        nameP.className = 'feedback-name';
        nameP.textContent = `${feedback.firstName} ${feedback.lastName}`;

        const emailP = document.createElement('p');
        emailP.className = 'feedback-email';
        emailP.textContent = feedback.email;

        metaDiv.appendChild(nameP);
        metaDiv.appendChild(emailP);

        headerDiv.appendChild(avatarDiv);
        headerDiv.appendChild(metaDiv);

        const suggestionsP = document.createElement('p');
        suggestionsP.className = 'feedback-suggestions';
        suggestionsP.textContent = feedback.suggestions ? `Suggestions: ${feedback.suggestions}` : 'No suggestions provided';

        const timestampP = document.createElement('p');
        timestampP.className = 'feedback-timestamp';
        timestampP.textContent = new Date(feedback.timestamp).toLocaleString();

        feedbackDiv.appendChild(headerDiv);
        feedbackDiv.appendChild(suggestionsP);
        feedbackDiv.appendChild(timestampP);

        feedbackList.appendChild(feedbackDiv);
    });

    displayPagination();
}

function displayPagination() {
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = '';
    
    const totalPages = Math.ceil(feedbacks.length / itemsPerPage);
    
    for (let i = 1; i <= totalPages; i++) {
        const button = document.createElement('button');
        button.textContent = i;
        button.onclick = () => {
            currentPage = i;
            displayFeedbacks();
        };
        if (i === currentPage) {
            button.disabled = true;
        }
        pagination.appendChild(button);
    }
}