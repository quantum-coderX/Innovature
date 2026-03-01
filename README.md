# Adithyan Raj - Weekly Learning Journey

**CSE STUDENT @ MUTHOOT INSTITUTE OF TECHNOLOGY AND SCIENCE (MITS)**

This repository tracks my weekly learning and project development from Week 1 to Week 12. Each week contains new projects, skills, and accomplishments.

---

## Weekly Progress

### [Week 1: Data Science Portfolio](./week-1/README.md)
**Status:** In Progress

- **Project:** Personal Data Science Portfolio Website
- **Skills:** HTML, CSS, JavaScript, Web Design, Responsive Design
- **Highlights:**
	- Built modern, dark-themed portfolio website
	- Showcased 3 real projects (P2P Learning, Quantitative Finance, Gen Z Bot)
	- Professional design with animations and hover effects
	- Fully responsive mobile-first design

**View:** [Week 1 Portfolio](./week-1/index.html)

### [Week 2: Interactive Feedback Form](./week-2/README.md)
**Status:** Completed ✅

- **Project:** Modern Glassmorphism Feedback Collection System
- **Skills:** HTML5, CSS3 (Glassmorphism), JavaScript (ES6), Form Validation, localStorage
- **Highlights:**
	- Beautiful glassmorphism UI with frosted glass effects
	- Gmail address validation with case-insensitive regex
	- Real-time form validation with detailed error messages
	- localStorage-based data persistence
	- Responsive pagination for feedback display
	- Modern gradient backgrounds with smooth animations
	- Input sanitization and data security

### [Week 3: Library Management System](./week-3/README.md)
**Status:** Completed ✅

- **Project:** Command-Line Library Management System
- **Skills:** Python OOP, File I/O (CSV), Data Structures, CLI Development
- **Highlights:**
	- Complete library system with books, members, transactions
	- Object-oriented design with classes for Book, Member, Transaction
	- CSV-based data persistence
	- CLI interface for all operations (add, search, borrow, return)
	- Data validation and error handling
	- Comprehensive reporting features

**Run:** `python week-3/main.py`

### [Week 4: Student Database System](./week-4/README.md)
**Status:** Completed ✅

- **Project:** Student Management with Database & Web Interface
- **Skills:** Python, SQLite, SQLAlchemy, Flask, HTML/CSS, Database Design
- **Highlights:**
	- SQLite database with proper schema
	- CRUD operations for students
	- CLI interface for data management
	- Web interface with Flask
	- Data export functionality
	- Clean separation of concerns

**Run:** `python week-4/main.py` (CLI) or `python week-4/app.py` (Web)

### [Week 5: User Notes API](./week-5/README.md)
**Status:** Completed ✅

- **Project:** RESTful Notes API with Authentication
- **Skills:** Flask, JWT Authentication, PostgreSQL, Docker, API Design, Security
- **Highlights:**
	- JWT-based authentication system
	- Full CRUD operations for personal notes
	- PostgreSQL database with Docker setup
	- Comprehensive error handling and logging
	- Password security with hashing and validation
	- Postman collection for testing
	- Production-ready API with proper status codes

**Run:** `docker-compose up -d` then `python week-5/main.py`

---

## Quick Links

| Week | Project | Status |
|------|---------|--------|
| [1](./week-1) | Data Science Portfolio | Completed ✅ |
| [2](./week-2) | Interactive Feedback Form | Completed ✅ |
| [3](./week-3) | Library Management System | Completed ✅ |
| [4](./week-4) | Student Database System | Completed ✅ |
| [5](./week-5) | User Notes API | Completed ✅ |
| 6-12 | *Coming with tasks* | Pending |

**Note:** Weeks 1-5 completed. New week folders will be created as tasks are assigned.

---

## About Me

I'm a passionate **Data Scientist & Engineer** specializing in:
- Python & Data Analysis
- Machine Learning & Scikit-learn
- Quantitative Finance & Analytics
- Apache Airflow & ETL
- SQL & NoSQL Databases
- Statistical Modeling & Pandas
- **Web Development:** HTML, CSS, JavaScript, Flask, REST APIs
- **Database Design:** SQLite, PostgreSQL, SQLAlchemy
- **DevOps:** Docker, Containerization
- **Security:** JWT, Password Hashing, Authentication

**Education:** Computer Science Student at MITS
**GitHub:** [quantum-coderX](https://github.com/quantum-coderX)

---

## Repository Structure

```
Innovature/
├── week-1/              # Portfolio & Website Design
│   ├── index.html
│   ├── projects.html
│   ├── contact.html
│   ├── css/
│   ├── js/
│   └── assets/
├── week-2/              # Interactive Feedback Form
│   ├── index.html       # Feedback submission form
│   ├── feedback.html    # Feedback display page
│   ├── css/
│   │   └── style.css    # Glassmorphism styling
│   └── js/
│       ├── script.js    # Form validation & submission
│       └── feedback.js  # Feedback display logic
├── week-3/              # Library Management System
│   ├── main.py          # CLI application
│   ├── library.py       # Library class
│   ├── book.py          # Book class
│   ├── member.py        # Member class
│   ├── transaction.py   # Transaction class
│   └── data/            # CSV data files
├── week-4/              # Student Database System
│   ├── main.py          # CLI application
│   ├── student.py       # Student model
│   ├── database.py      # Database setup
│   ├── schema.sql       # Database schema
│   ├── requirements.txt
│   └── __pycache__/
├── week-5/              # User Notes API
│   ├── main.py          # Flask API
│   ├── models.py        # Database models
│   ├── auth.py          # Authentication
│   ├── crud.py          # CRUD operations
│   ├── config.py        # Configuration
│   ├── requirements.txt
│   ├── docker-compose.yml
│   ├── notes_api.postman_collection.json
│   └── README.md
├── week-6/              # (Upcoming)
├── ...
└── week-12/             # (Upcoming)
```

---

## How to Use This Repo

Each week folder contains:
- **README.md** - Week-specific project details
- **Source code** - All project files
- **Documentation** - What I learned & built

To view a specific week's work:
```bash
cd week-1/
# Open index.html in your browser
```

---

## Notes

This is an ongoing project tracking my learning journey. Each week, I'll add new projects, skills, and accomplishments. Follow along to see my growth as a data scientist and engineer!

---

**Last Updated:** February 9, 2026
**Current Week:** 2

## Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Innovature.git
cd Innovature
```

2. Open `index.html` in your browser to view locally

3. Or visit the live site: [GitHub Pages URL]

## Features in Detail

### Responsive Design
- **Mobile (< 768px)**: Single column layout, hamburger menu
- **Tablet (768px - 1023px)**: Two column grids, full navigation
- **Desktop (1024px+)**: Three column grids, optimized spacing

### Navigation
- Sticky header with hamburger menu on mobile
- Auto-highlighting of active page
- Smooth transitions and hover effects
- Closes menu on link click

### Contact Form Validation
- **Name**: Minimum 2 characters
- **Email**: Valid email format
- **Phone**: Optional, valid phone format if provided
- **Subject**: Minimum 3 characters
- **Message**: Minimum 10 characters
- Real-time validation feedback
- Success message on submission

### Browser Support
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## Customization

### Colors
Edit CSS variables in `week-1/css/style.css`:
```css
:root {
		--primary-color: #2563eb;
		--secondary-color: #1e40af;
		--accent-color: #dc2626;
}
```



## Performance

- Lightweight CSS (no frameworks)
- Vanilla JavaScript (no dependencies)
- Optimized images with placeholders
- Lazy loading support for images

## Accessibility

- Semantic HTML
- ARIA labels where needed
- Keyboard navigation support
- Color contrast compliance
- Reduced motion support for animations

## License

This project is open source and available under the MIT License.

## Author

Adithyan Raj - [GitHub](https://github.com/quantum-coderX) | [LinkedIn](https://linkedin.com)

---

**Last Updated**: March 1, 2026

