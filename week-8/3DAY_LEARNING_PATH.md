# Week 8: Two-Factor Authentication - 3-Day Incremental Learning

**Approach:** Study → Understand → Build → Test (Each Day)

---

## 📅 3-Day Learning Structure

### **Day 1: User Roles & Permissions + Password Hashing**
### **Day 2: Middleware Basics & OTP Implementation**  
### **Day 3: 2FA with Account Lockout & Audit Logging**

Each day includes:
- 📚 **Study**: Core concepts and best practices
- 💻 **Hands-On**: Build working code
- ✅ **Assignment**: Complete mini-project
- 🧪 **Test**: Verify your implementation

---

# 🌅 DAY 1: User Roles & Permissions + Password Hashing

## 📚 Study Topics

### 1. User Roles & Permissions (30 min read)

**What are User Roles?**
```
Roles are permission levels assigned to users:
- ADMIN: Full system access, user management
- MODERATOR: View users, edit some features
- USER: Basic access to own resources
```

**Permission Matrix Example:**
```
┌─────────────────┬───────┬──────────┬──────┐
│ Permission      │ Admin │ Moderator│ User │
├─────────────────┼───────┼──────────┼──────┤
│ View all users  │  ✅   │    ✅    │  ❌  │
│ Edit users      │  ✅   │    ✅    │  ❌  │
│ Delete users    │  ✅   │    ❌    │  ❌  │
│ View own data   │  ✅   │    ✅    │  ✅  │
│ Edit own data   │  ✅   │    ✅    │  ✅  │
└─────────────────┴───────┴──────────┴──────┘
```

**Resources:**
- RBAC vs ABAC: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- Role-Based vs Attribute-Based Access Control

### 2. Password Hashing (30 min read)

**Why Hash Passwords?**
- Never store plaintext passwords
- Hashing is one-way (can't reverse)
- Salting prevents rainbow table attacks

**Popular Algorithms:**

| Algorithm | Speed | Security | Status |
|-----------|-------|----------|--------|
| PBKDF2 | Medium | ⭐⭐⭐⭐ | Recommended |
| bcrypt | Slow | ⭐⭐⭐⭐⭐ | Excellent |
| scrypt | Very Slow | ⭐⭐⭐⭐⭐ | Very Good |
| Argon2 | Slow | ⭐⭐⭐⭐⭐ | Best |
| MD5 | Very Fast | ☠️ | Never use |
| SHA-256 | Fast | ⚠️ | Use with salt |

**PBKDF2 Example:**
```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hashing
hashed = generate_password_hash("MyPassword123", method='pbkdf2:sha256', salt_length=16)
# Output: pbkdf2:sha256:260000$...

# Verification
check_password_hash(hashed, "MyPassword123")  # True
check_password_hash(hashed, "WrongPassword")  # False
```

**Key Concepts:**
- **Salt**: Random data added to password before hashing (prevents rainbow tables)
- **Iterations**: How many times hash function runs (makes brute force slow)
- **Constant-Time Comparison**: Prevents timing attacks

**Resources:**
- NIST Password Guidelines: https://pages.nist.gov/800-63-3/sp800-63b.html
- Werkzeug Security: https://werkzeug.palletsprojects.com/security/

---

## 💻 Hands-On: Database Models

### Step 1: Create User Model with Roles

**File: `models.py`**

```python
from database import db
from datetime import datetime

class User(db.Model):
    """User model with role-based access"""
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Role field
    role = db.Column(db.String(20), nullable=False, default='user')  # admin, user, moderator
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username} [{self.role}]>'
```

**Questions to Consider:**
1. Why use `unique=True` for username and email?
2. What should be the default role?
3. Why track `created_at` and `updated_at`?

### Step 2: Create Role Model

```python
class Role(db.Model):
    """Role model for RBAC"""
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # admin, user, moderator
    description = db.Column(db.String(255))
    permissions = db.Column(db.JSON, nullable=False, default={})
    
    def __repr__(self):
        return f'<Role {self.name}>'
```

**Discussion:**
- Why store permissions as JSON?
- What permissions should each role have?

---

## 🔑 Password Hashing Functions

### Step 3: Create Auth Functions

**File: `auth.py` (Part 1)**

```python
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models import User

# ==================== Password Functions ====================

def hash_password(password):
    """
    Hash a password using PBKDF2-SHA256
    
    Args:
        password (str): Plain text password
        
    Returns:
        str: Hashed password
        
    Example:
        >>> hashed = hash_password("MyPassword123")
        >>> # Store hashed in database
    """
    return generate_password_hash(
        password,
        method='pbkdf2:sha256',  # Algorithm
        salt_length=16            # Salt size in bytes
    )

def check_password(password, hashed):
    """
    Verify password against hash (constant-time comparison)
    
    Args:
        password (str): Plain text password to verify
        hashed (str): Stored password hash
        
    Returns:
        bool: True if password matches, False otherwise
        
    Example:
        >>> check_password("MyPassword123", hashed_password)
        True
    """
    return check_password_hash(hashed, password)

def create_user(username, email, password, role='user'):
    """
    Create a new user with hashed password
    
    Args:
        username (str): Unique username
        email (str): Unique email
        password (str): Plain text password (will be hashed)
        role (str): User role (default: 'user')
        
    Returns:
        tuple: (user_object, message)
        
    Example:
        >>> user, msg = create_user("john", "john@example.com", "Pass123")
        >>> print(msg)
        'User created successfully'
    """
    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return None, "Username already exists"
    
    if User.query.filter_by(email=email).first():
        return None, "Email already exists"
    
    # Hash password
    hashed_password = hash_password(password)
    
    # Create user
    user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        role=role
    )
    
    db.session.add(user)
    db.session.commit()
    
    return user, "User created successfully"

def authenticate_user(username, password):
    """
    Find user and verify password
    
    Args:
        username (str): Username to authenticate
        password (str): Password to verify
        
    Returns:
        tuple: (user_object, status_message)
        
    Example:
        >>> user, msg = authenticate_user("john", "Pass123")
        >>> if user:
        ...     print(f"Welcome {user.username}")
    """
    # Find user
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return None, "Invalid username or password"
    
    # Check password
    if not check_password(password, user.password_hash):
        return None, "Invalid username or password"
    
    return user, "Authentication successful"
```

**Study Questions:**
1. Why return a tuple `(user, message)` instead of raising exceptions?
2. What's a "constant-time comparison"?
3. Why not accept plaintext password in database?

---

## ✅ Assignment Day 1

### Part 1: Set Up Database

```python
# main.py
from flask import Flask
from database import db
from config import Config
from models import User, Role

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()
    print("Database initialized!")

if __name__ == '__main__':
    app.run(debug=True)
```

### Part 2: Test Password Hashing

```python
# test_password_hashing.py
from main import app, db
from auth import hash_password, check_password, create_user
from models import User

with app.app_context():
    # Test 1: Hash and verify password
    print("Test 1: Password Hashing")
    hashed = hash_password("SecurePass123")
    print(f"Original: SecurePass123")
    print(f"Hashed:   {hashed}")
    print(f"Match:    {check_password('SecurePass123', hashed)}")
    print(f"Wrong:    {check_password('WrongPass', hashed)}")
    print()
    
    # Test 2: Create user
    print("Test 2: Create User")
    user, msg = create_user("john_doe", "john@example.com", "Password123")
    print(f"Message: {msg}")
    print(f"User: {user}")
    print()
    
    # Test 3: Authenticate
    print("Test 3: Authenticate User")
    from auth import authenticate_user
    user, msg = authenticate_user("john_doe", "Password123")
    print(f"Message: {msg}")
    print(f"User ID: {user.id if user else 'None'}")
    print(f"Role: {user.role if user else 'None'}")
    print()
    
    # Test 4: Wrong password
    print("Test 4: Wrong Password")
    user, msg = authenticate_user("john_doe", "WrongPassword")
    print(f"Message: {msg}")
    print(f"Authenticated: {user is not None}")
```

**Run and observe:**
```bash
python test_password_hashing.py
```

### Part 3: Implement Role-Based User Creation

```python
# Extend auth.py with role assignment
def create_admin_user(username, email, password):
    """Create an admin user"""
    return create_user(username, email, password, role='admin')

def create_moderator_user(username, email, password):
    """Create a moderator user"""
    return create_user(username, email, password, role='moderator')

def get_user_by_username(username):
    """Retrieve user by username"""
    return User.query.filter_by(username=username).first()

def get_user_by_id(user_id):
    """Retrieve user by ID"""
    return User.query.get(user_id)
```

---

## 🧪 Day 1 Deliverables

**By end of Day 1, you should have:**

- ✅ Created `models.py` with User and Role models
- ✅ Created `auth.py` with password hashing functions
- ✅ Implemented user creation with role assignment
- ✅ Implemented user authentication (username + password)
- ✅ Tested password hashing and authentication
- ✅ Understood RBAC concepts

**Files Created:**
```
week-8/
├── models.py          (User, Role models)
├── auth.py            (password hashing, user creation/auth)
├── test_password_hashing.py  (Test cases)
└── config.py, database.py, main.py  (Flask setup)
```

**Key Concepts Learned:**
- Why roles and permissions are important
- How password hashing works
- PBKDF2-SHA256 algorithm
- User creation and authentication flow

---

# ☀️ DAY 2: Middleware Basics & OTP Implementation

## 📚 Study Topics (Start Day 2)

### 1. Middleware Concept (30 min read)

**What is Middleware?**

Middleware is code that runs before/after request handling:

```
Request → Middleware → Route Handler → Response
          (validate here)
```

**In Flask:**
```python
# Middleware as Decorator
@app.before_request
def before():
    # Runs before every request
    pass

# Middleware as Decorator (custom)
from functools import wraps

def require_login(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Check if user logged in
        # If not, return error
        return f(*args, **kwargs)
    return wrapper

@app.route('/profile')
@require_login
def profile():
    # Only runs if require_login passes
    pass
```

**Flask-JWT Middleware:**
```python
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/api/protected')
@jwt_required()  # Middleware - checks JWT token
def protected():
    user_id = get_jwt_identity()  # Get data from token
    return f"User {user_id} accessed this"
```

**Key Insight:**
- Middleware = Gatekeeper that validates before allowing access
- Decorators in Python = Function wrappers

**Resources:**
- Flask Middleware: https://flask.palletsprojects.com/
- Flask-JWT-Extended: https://flask-jwt-extended.readthedocs.io/

### 2. One-Time Passwords (OTP) (30 min read)

**What is OTP?**

A single-use password code sent to user's email/phone.

```
User tries to login:
  ↓
  ✅ Correct password
  ↓
  → Send 6-digit code to email
  ↓
  User enters code from email
  ↓
  ✅ Code matches → Login success
```

**OTP Properties:**
- Random 6-digit code (1M possible combinations)
- Expires after 5 minutes
- Can only be used once
- Invalid after 3 failed attempts

**OTP Security:**
```
Brute force attack example:
- Attacker has 5 minutes
- Max 1,000,000 combinations
- With rate limiting: 300 attempts max
- Success rate: 0.03% (bad!)

Why OTP is effective:
- Time limit (5 minutes)
- Single use (can't reuse)
- Expiration (auto-delete)
- Rate limiting (max attempts)
```

**Email Integration:**
```
Why email(not SMS)?
✅ Easier to set up (Gmail SMTP)
✅ No phone requirements
✅ TLS encryption support
⚠️ Slower delivery (seconds)
⚠️ User might miss it
```

**Resources:**
- TOTP Standards: https://tools.ietf.org/html/rfc6238
- OTP Best Practices: https://cheatsheetseries.owasp.org/

---

## 💻 Hands-On: OTP & Email

### Step 1: Create OTP Model

**File: `models.py` (Add to existing)**

```python
from datetime import datetime, timedelta

class OTP(db.Model):
    """One-Time Password for 2FA"""
    __tablename__ = 'otp'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)  # 6-digit code
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    attempts = db.Column(db.Integer, default=0)
    
    # Relationship back to User
    user = db.relationship('User', backref=db.backref('otps', lazy=True))
    
    def __repr__(self):
        return f'<OTP for User {self.user_id}>'
    
    def is_expired(self):
        """Check if OTP has expired"""
        return datetime.utcnow() > self.expires_at
    
    def is_valid(self):
        """Check if OTP can still be used"""
        return not self.is_expired() and not self.is_verified
```

**Questions:**
1. Why store OTP expiration time instead of just a boolean?
2. Why track verification attempts?
3. What happens after `expires_at`?

### Step 2: OTP Generation & Storage

**File: `auth.py` (Add to existing)**

```python
import random
import string
from models import OTP
from datetime import datetime, timedelta

# ==================== OTP Functions ====================

def generate_otp(length=6):
    """
    Generate random numeric OTP
    
    Args:
        length (int): Number of digits (default: 6)
        
    Returns:
        str: Random 6-digit code (e.g., "123456")
        
    Example:
        >>> code = generate_otp()
        >>> print(code)
        '847362'
    """
    return ''.join(random.choices(string.digits, k=length))

def create_otp_for_user(user_id, expiry_minutes=5):
    """
    Generate OTP for user and save to database
    
    Args:
        user_id (int): User ID to create OTP for
        expiry_minutes (int): How long until OTP expires
        
    Returns:
        OTP: OTP object with code and expiration
        
    Example:
        >>> otp = create_otp_for_user(1)
        >>> print(f"Send code {otp.otp_code} to user")
    """
    # Delete any existing unverified OTPs for this user
    OTP.query.filter_by(user_id=user_id, is_verified=False).delete()
    
    # Generate new OTP
    otp_code = generate_otp()
    
    otp = OTP(
        user_id=user_id,
        otp_code=otp_code,
        expires_at=datetime.utcnow() + timedelta(minutes=expiry_minutes)
    )
    
    db.session.add(otp)
    db.session.commit()
    
    return otp

def verify_otp(user_id, otp_code):
    """
    Verify OTP code for user
    
    Args:
        user_id (int): User ID
        otp_code (str): Code to verify
        
    Returns:
        tuple: (is_valid, message)
        
    Example:
        >>> success, msg = verify_otp(1, "123456")
        >>> if success:
        ...     print("OTP verified!")
    """
    # Get the most recent OTP for user
    otp = OTP.query.filter_by(
        user_id=user_id, 
        is_verified=False
    ).order_by(OTP.created_at.desc()).first()
    
    if not otp:
        return False, "No OTP request found"
    
    # Check expiration
    if otp.is_expired():
        return False, "OTP has expired"
    
    # Increment attempts
    otp.attempts += 1
    
    # Check max attempts
    if otp.attempts > 3:
        db.session.commit()
        return False, "Too many failed attempts"
    
    # Verify code
    if otp.otp_code != otp_code:
        db.session.commit()
        return False, "Invalid OTP code"
    
    # Valid! Mark as verified
    otp.is_verified = True
    db.session.commit()
    
    return True, "OTP verified successfully"
```

**Study Questions:**
1. Why delete unverified OTPs before creating new one?
2. Why increment attempts before checking?
3. What happens if user enters wrong code multiple times?

### Step 3: Email Configuration

**File: `config.py` (Update)**

```python
import os

class Config:
    # Existing config...
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
    
    # NEW: Email Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # your-email@gmail.com
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # app-password from Google
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@app.com')
    
    # OTP Settings
    OTP_EXPIRY_MINUTES = 5
    OTP_LENGTH = 6
```

### Step 4: Email OTP Sending

**File: `auth.py` (Add to existing)**

```python
from flask_mail import Mail, Message

mail = Mail()

def send_otp_email(user, otp_code):
    """
    Send OTP code via email
    
    Args:
        user (User): User object with email
        otp_code (str): 6-digit OTP code
        
    Returns:
        tuple: (success, message)
        
    Example:
        >>> success, msg = send_otp_email(user, "123456")
        >>> if success:
        ...     print("Email sent!")
    """
    try:
        subject = "Your One-Time Password (OTP) for Login"
        body = f"""
Hello {user.username},

Your login OTP is: {otp_code}

This code will expire in 5 minutes.

Do not share your OTP with anyone.

Regards,
Authentication System
        """
        
        msg = Message(
            subject=subject,
            recipients=[user.email],
            body=body
        )
        
        mail.send(msg)
        return True, "OTP sent to email"
        
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"
```

---

## 🔐 Role-Based Middleware

### Step 5: Create RBAC Decorators

**File: `auth.py` (Add to existing)**

```python
from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# ==================== Middleware Functions ====================

def require_role(*required_roles):
    """
    Middleware decorator to enforce role-based access
    
    Usage:
        @app.route('/admin/users')
        @require_role('admin')
        def admin_users():
            return "Admin only"
        
        @app.route('/moderate')
        @require_role('admin', 'moderator')
        def moderate():
            return "Admin or Moderator"
    """
    def decorator(f):
        @wraps(f)
        @jwt_required()  # First check JWT token exists
        def wrapper(*args, **kwargs):
            # Get user ID from JWT token
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user:
                return jsonify({'message': 'User not found'}), 404
            
            # Check if user has required role
            if user.role not in required_roles:
                return jsonify({
                    'message': f'Access denied. Required role(s): {", ".join(required_roles)}'
                }), 403
            
            return f(*args, **kwargs)
        
        return wrapper
    return decorator

def require_2fa_verified(f):
    """
    Middleware to ensure 2FA verification
    
    Usage:
        @app.route('/protected')
        @require_2fa_verified
        def protected():
            return "2FA verified!"
    """
    @wraps(f)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Check if 2FA is verified
        if not getattr(user, 'two_fa_verified', False):
            return jsonify({'message': '2FA verification required'}), 403
        
        return f(*args, **kwargs)
    
    return wrapper
```

**Understanding the decorator:**
```
@require_role('admin')    ← Applied to route
↓
Wrapper function is called
↓
@jwt_required() checks JWT token
↓
get_jwt_identity() extracts user_id
↓
Check if user.role == 'admin'
↓
✅ Role matches → Call original function
❌ Role doesn't match → Return 403 error
```

---

## ✅ Assignment Day 2

### Part 1: Database Update

Add OTP and User role fields:

```python
# models.py - Update User model
class User(db.Model):
    # ... existing fields ...
    role = db.Column(db.String(20), default='user')
    two_fa_verified = db.Column(db.Boolean, default=False)  # NEW
```

### Part 2: Test OTP Generation

```python
# test_otp.py
from main import app, db
from auth import create_user, create_otp_for_user, verify_otp, generate_otp

with app.app_context():
    # Create a test user
    user, _ = create_user("otp_test", "test@example.com", "Password123")
    print(f"✓ User created: {user.username}")
    
    # Generate OTP
    otp = create_otp_for_user(user.id)
    print(f"✓ OTP generated: {otp.otp_code}")
    print(f"  Expires at: {otp.expires_at}")
    
    # Try to verify with wrong code
    success, msg = verify_otp(user.id, "000000")
    print(f"✗ Wrong code: {msg} (attempts: {verify_otp.attempts})")
    
    # Verify with correct code
    success, msg = verify_otp(user.id, otp.otp_code)
    print(f"✓ Correct code: {msg}")
```

### Part 3: Test Email (Optional)

Set up `.env` file:

```bash
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-app-password
```

Then test:
```python
# test_email.py
from main import app
from auth import create_user, create_otp_for_user, send_otp_email

with app.app_context():
    user, _ = create_user("email_test", "your-email@gmail.com", "Pass123")
    otp = create_otp_for_user(user.id)
    
    success, msg = send_otp_email(user, otp.otp_code)
    print(f"Email sent: {success} - {msg}")
    
    # Check your email!
```

### Part 4: Test Middleware

```python
# test_middleware.py
from main import app
from auth import require_role, create_user

# Create test users
with app.app_context():
    admin, _ = create_user("admin_user", "admin@test.com", "Pass123", role='admin')
    regular, _ = create_user("regular_user", "user@test.com", "Pass123", role='user')
    print("✓ Users created")
```

---

## 🧪 Day 2 Deliverables

**By end of Day 2, you should have:**

- ✅ Understood middleware concept
- ✅ Created OTP model and functions
- ✅ Implemented OTP generation and verification
- ✅ Set up email configuration
- ✅ Created role-based middleware decorators
- ✅ Tested OTP generation (and email if configured)

**Files Created/Updated:**
```
week-8/
├── models.py          (+ OTP model)
├── auth.py            (+ OTP & middleware)
├── config.py          (+ email config)
├── test_otp.py        (OTP testing)
└── .env               (email credentials)
```

**Key Concepts Learned:**
- What middleware does and why it's useful
- OTP generation and verification
- Email integration with Flask-Mail
- Role-based access control decorators

---

# 🌙 DAY 3: 2FA Complete + Account Security

## 📚 Study Topics (Start Day 3)

### 1. Two-Factor Authentication Flow (30 min read)

**Complete 2FA Flow:**

```
1. LOGIN ATTEMPT
   User enters: username + password
   
2. PASSWORD VERIFICATION
   ✅ Password correct
        → Generate OTP
        → Send to email
        → Return: "Check your email for OTP"
   ❌ Password wrong
        → Increment failed attempts
        → Possibly lock account

3. OTP ENTRY
   User enters: OTP code
   
4. OTP VERIFICATION
   ✅ Code correct and not expired
        → Generate JWT token
        → Return: token (user is logged in)
   ❌ Code wrong or expired
        → Increment attempts
        → Fail after 3 attempts

5. API ACCESS
   User sends: Authorization: Bearer {token}
   
6. TOKEN VERIFICATION
   ✅ Token valid and 2FA verified
        → Grant access
   ❌ Token invalid or 2FA not verified
        → Return 403 error
```

**Login Response Sequence:**
```python
# Step 1: Send username + password
POST /api/auth/login
{
  "username": "john",
  "password": "SecurePass123"
}

Response:
{
  "user_id": 1,
  "username": "john",
  "two_fa_required": true,
  "message": "OTP sent to your email"
}

# Step 2: Send OTP code
POST /api/auth/verify-otp
{
  "user_id": 1,
  "otp_code": "123456"
}

Response:
{
  "access_token": "eyJhbGc...",
  "user_id": 1,
  "username": "john"
}

# Step 3: Use token to access protected route
GET /api/users/profile
Authorization: Bearer eyJhbGc...

Response:
{
  "id": 1,
  "username": "john",
  "email": "john@example.com"
}
```

**Resources:**
- 2FA Best Practices: https://cheatsheetseries.owasp.org/
- Authentication Flows: https://auth0.com/

### 2. Account Lockout & Brute Force Protection (30 min read)

**The Problem:**

Attacker tries to guess password:
```
Attempt 1: password123
Attempt 2: password1234
Attempt 3: MyPassword
... (thousands more)
→ Eventually guesses correct password!
```

**Account Lockout Solution:**

```
Attempt 1: WRONG
Attempt 2: WRONG
Attempt 3: WRONG
Attempt 4: WRONG
Attempt 5: WRONG
         → 🔒 ACCOUNT LOCKED for 30 minutes

After 30 minutes → Account unlocks automatically
```

**Failed Attempts Tracking:**

```python
User.failed_login_attempts = 0  # Count wrong attempts
User.locked_until = null         # When account unlocks

# On login failure:
User.failed_login_attempts += 1
if User.failed_login_attempts >= 5:
    User.locked_until = now + 30 minutes

# On login success:
User.failed_login_attempts = 0
User.locked_until = null
```

**Lockout Benefits:**
- ✅ Defeats brute force attacks
- ✅ Prevents account compromise
- ✅ Gives admin time to respond

**Lockout Challenges:**
- ⚠️ User might forget password and get locked
- ⚠️ Legitimate users can be blocked
- Solution: Admin can manually unlock

**Resources:**
- OWASP Brute Force Protection: https://cheatsheetseries.owasp.org/
- Account Lockout Best Practices

### 3. Login Audit Logging (30 min read)

**Why Log Logins?**

Track suspicious activity:
```
Benefits:
✅ Detect multiple failed attempts (brute force)
✅ Identify unusual access patterns
✅ Compliance requirements (GDPR, PCI-DSS)
✅ Forensic investigation after breach
✅ Alert admins to suspicious activity

What to Log:
- User ID
- Success/Failure status
- Timestamp
- IP address
- Failure reason
```

**Logging Example:**
```
[2026-03-20 10:30:15] User 5 - FAILED - Invalid password
[2026-03-20 10:30:22] User 5 - FAILED - Invalid password
[2026-03-20 10:30:29] User 5 - FAILED - Invalid password
[2026-03-20 10:30:36] User 5 - FAILED - Invalid password
[2026-03-20 10:30:43] User 5 - FAILED - Invalid password
[2026-03-20 10:30:50] User 5 - ACCOUNT LOCKED

[2026-03-20 11:30:00] User 5 - ACCOUNT UNLOCKED by admin
```

**Query Examples:**
```python
# Find all locked accounts
locked = User.query.filter(User.locked_until > now).all()

# Find users with many failed attempts
suspicious = User.query.filter(User.failed_login_attempts > 3).all()

# Find failed logins in last hour
recent_failures = LoginAttempt.query.filter(
    LoginAttempt.success == False,
    LoginAttempt.timestamp > now - 1 hour
).all()
```

---

## 💻 Hands-On: Account Security

### Step 1: Update User Model for Lockout

**File: `models.py` (Update User class)**

```python
class User(db.Model):
    # ... existing fields ...
    
    # Lockout fields (NEW)
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)  # When to unlock
    two_fa_verified = db.Column(db.Boolean, default=False)  # 2FA status
    
    def is_account_locked(self):
        """
        Check if account is currently locked
        
        Returns:
            bool: True if locked, False otherwise
        """
        if self.locked_until and datetime.utcnow() < self.locked_until:
            return True
        return False
    
    def reset_failed_attempts(self):
        """Reset failed attempts and unlock account"""
        self.failed_login_attempts = 0
        self.locked_until = None
    
    def increment_failed_attempts(self, max_attempts=5, lockout_minutes=30):
        """Increment failed attempts and lock if needed"""
        self.failed_login_attempts += 1
        
        if self.failed_login_attempts >= max_attempts:
            self.locked_until = datetime.utcnow() + timedelta(minutes=lockout_minutes)
```

### Step 2: Create Login Attempt Model

**File: `models.py` (Add)**

```python
class LoginAttempt(db.Model):
    """Track all login attempts for security audit"""
    __tablename__ = 'login_attempt'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    success = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=True)  # IPv4 or IPv6
    reason = db.Column(db.String(255), nullable=True)  # Why it failed
    
    user = db.relationship('User', backref=db.backref('login_attempts', lazy=True))
    
    def __repr__(self):
        status = "✓" if self.success else "✗"
        return f'<LoginAttempt {status} User {self.user_id} at {self.timestamp}>'
```

**Study Questions:**
1. Why store IP address?
2. Why have a separate `reason` field?
3. Why use `backref` for relationship?

### Step 3: Update Authentication with Security

**File: `auth.py` (Update authenticate_user)**

```python
def authenticate_user(username, password):
    """
    Authenticate user with lockout protection
    
    Args:
        username (str): Username
        password (str): Password
        
    Returns:
        tuple: (user_object, message)
    """
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return None, "Invalid username or password"
    
    # Check if account is locked
    if user.is_account_locked():
        remaining = (user.locked_until - datetime.utcnow()).total_seconds() / 60
        return None, f"Account locked. Try again in {int(remaining)} minutes"
    
    # Check password
    if not check_password(password, user.password_hash):
        # Increment failed attempts
        user.increment_failed_attempts()
        db.session.commit()
        
        # Log failed attempt
        log_login_attempt(user.id, success=False, reason="Invalid password")
        
        # Check if now locked
        if user.is_account_locked():
            return None, f"Account locked after 5 failed attempts. Try again later."
        
        return None, "Invalid username or password"
    
    # Password correct - reset attempts
    user.reset_failed_attempts()
    db.session.commit()
    
    # Log successful password verification
    log_login_attempt(user.id, success=True)
    
    return user, "Authentication successful"

def log_login_attempt(user_id, success=True, reason=None, ip_address=None):
    """
    Log login attempt for security audit
    
    Args:
        user_id (int): User attempting login
        success (bool): Was attempt successful?
        reason (str): Why failed (for failures)
        ip_address (str): IP address of attempt
    """
    attempt = LoginAttempt(
        user_id=user_id,
        success=success,
        reason=reason,
        ip_address=ip_address
    )
    db.session.add(attempt)
    db.session.commit()
```

### Step 4: Create JWT Tokens

**File: `auth.py` (Add)**

```python
from flask_jwt_extended import JWTManager, create_access_token

jwt = JWTManager()

def create_jwt_token(user_id):
    """
    Create JWT access token for user
    
    Args:
        user_id (int): User ID to include in token
        
    Returns:
        str: JWT token
        
    Example:
        >>> token = create_jwt_token(5)
        >>> # Send token to client
    """
    user = User.query.get(user_id)
    if not user:
        return None
    
    additional_claims = {
        'username': user.username,
        'email': user.email,
        'role': user.role
    }
    
    access_token = create_access_token(
        identity=user_id,
        additional_claims=additional_claims
    )
    
    return access_token

def get_current_user():
    """Get current user from JWT token"""
    from flask_jwt_extended import get_jwt_identity
    user_id = get_jwt_identity()
    return User.query.get(user_id)
```

---

## 🚀 API Routes

### Step 5: Login & OTP Verification Routes

**File: `main.py`**

```python
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from database import db
from config import Config
from models import User, OTP
from auth import (
    authenticate_user, create_otp_for_user, send_otp_email,
    verify_otp, create_jwt_token, mail, jwt
)

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)
mail.init_app(app)

# ==================== Login Endpoint ====================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """
    Login endpoint - returns user_id to then verify OTP
    
    Request:
        {"username": "john", "password": "SecurePass123"}
    
    Response (success):
        {
          "user_id": 1,
          "message": "OTP sent to email"
        }
    
    Response (failure):
        {
          "message": "Account locked..."
        }
    """
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password required'}), 400
    
    username = data.get('username').strip()
    password = data.get('password')
    
    # Authenticate user
    user, auth_msg = authenticate_user(username, password)
    
    if not user:
        return jsonify({'message': auth_msg}), 401
    
    # Create OTP
    otp = create_otp_for_user(user.id)
    
    # Send OTP via email
    success, email_msg = send_otp_email(user, otp.otp_code)
    
    if not success:
        return jsonify({'message': f'Email error: {email_msg}'}), 500
    
    # Return user_id (client will use this to verify OTP)
    return jsonify({
        'user_id': user.id,
        'username': user.username,
        'message': 'OTP sent to your email'
    }), 200

# ==================== Verify OTP Endpoint ====================

@app.route('/api/auth/verify-otp', methods=['POST'])
def verify_two_fa():
    """
    Verify OTP and get JWT token
    
    Request:
        {"user_id": 1, "otp_code": "123456"}
    
    Response (success):
        {
          "access_token": "eyJhbGc...",
          "user_id": 1
        }
    
    Response (failure):
        {
          "message": "Invalid OTP"
        }
    """
    data = request.get_json()
    
    if not data or not data.get('user_id') or not data.get('otp_code'):
        return jsonify({'message': 'User ID and OTP code required'}), 400
    
    user_id = data.get('user_id')
    otp_code = data.get('otp_code').strip()
    
    # Verify OTP
    success, msg = verify_otp(user_id, otp_code)
    
    if not success:
        return jsonify({'message': msg}), 401
    
    # Get user
    user = User.query.get(user_id)
    
    # Mark 2FA as verified
    user.two_fa_verified = True
    db.session.commit()
    
    # Create JWT token
    token = create_jwt_token(user.id)
    
    return jsonify({
        'access_token': token,
        'user_id': user.id,
        'username': user.username,
        'message': 'OTP verified - You are now logged in'
    }), 200

# ==================== Protected Route Example ====================

@app.route('/api/users/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get current user's profile (2FA verified + JWT required)
    """
    user = get_current_user()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Check if 2FA verified
    if not user.two_fa_verified:
        return jsonify({'message': '2FA verification required'}), 403
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

---

## ✅ Assignment Day 3

### Part 1: Complete Login System

You now have:
- ✅ User registration with roles
- ✅ Password hashing and verification
- ✅ OTP generation and email sending
- ✅ Account lockout after 5 failed attempts
- ✅ JWT token generation
- ✅ Login attempt audit logging

### Part 2: Test Complete Flow

```python
# test_complete_flow.py
from main import app, db
from auth import create_user, authenticate_user, create_otp_for_user, verify_otp, create_jwt_token

print("=== COMPLETE 2FA LOGIN FLOW TEST ===\n")

with app.app_context():
    # Step 1: Register user
    print("Step 1: Register User")
    user, msg = create_user("testuser", "test@example.com", "SecurePass123")
    print(f"  ✓ {msg}")
    print(f"  User: {user.username}, Role: {user.role}\n")
    
    # Step 2: Authenticate (password check)
    print("Step 2: Authenticate with Password")
    user, msg = authenticate_user("testuser", "SecurePass123")
    print(f"  ✓ {msg}")
    print(f"  Failed attempts: {user.failed_login_attempts}\n")
    
    # Step 3: Generate OTP
    print("Step 3: Generate OTP")
    otp = create_otp_for_user(user.id)
    print(f"  ✓ OTP code: {otp.otp_code}")
    print(f"  Expires at: {otp.expires_at}\n")
    
    # Step 4: Verify OTP
    print("Step 4: Verify OTP")
    success, msg = verify_otp(user.id, otp.otp_code)
    if success:
        print(f"  ✓ {msg}\n")
    
    # Step 5: Create JWT token
    print("Step 5: Create JWT Token")
    token = create_jwt_token(user.id)
    print(f"  ✓ Token created")
    print(f"  Token: {token[:50]}...\n")
    
    print("=== LOGIN FLOW COMPLETE ===")

print("\n=== ACCOUNT LOCKOUT TEST ===\n")

with app.app_context():
    # Create new user
    user, _ = create_user("locktest", "lock@example.com", "LockPass123")
    print("User created for lockout test\n")
    
    # Try wrong password 5 times
    for i in range(5):
        user_result, msg = authenticate_user("locktest", "WrongPassword")
        failed = User.query.get(user.id).failed_login_attempts
        print(f"  Attempt {i+1}: {msg}")
        print(f"    Failed attempts: {failed}")
        if User.query.get(user.id).is_account_locked():
            print(f"    🔒 ACCOUNT LOCKED!\n")
            break
    
    # Try correct password after lockout
    user_result, msg = authenticate_user("locktest", "LockPass123")
    print(f"  Correct password: {msg}")
```

### Part 3: Test with cURL

```bash
# 1. Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"SecurePass123"}'

# Response:
# {"user_id":1,"username":"testuser","message":"OTP sent to your email"}

# 2. Verify OTP (check email for code)
curl -X POST http://localhost:5000/api/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"otp_code":"123456"}'

# Response:
# {"access_token":"eyJhbGc...","user_id":1,"username":"testuser"}

# 3. Access protected route
curl -X GET http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer eyJhbGc..."

# Response:
# {"id":1,"username":"testuser","email":"test@example.com","role":"user"}
```

---

## 🧪 Day 3 Deliverables

**By end of Day 3, you should have:**

- ✅ Complete 2FA login system
- ✅ Account lockout protection (5 failed attempts)
- ✅ Login attempt audit logging
- ✅ JWT token generation and validation
- ✅ Protected API routes with 2FA verification
- ✅ Fully tested complete authentication flow

**Files Completed:**
```
week-8/
├── models.py          (+ LoginAttempt, lockout fields)
├── auth.py            (+ lockout, JWT, logging)
├── main.py            (+ login, verify-otp, protected routes)
├── config.py          (complete)
├── database.py        (complete)
├── test_complete_flow.py  (full flow testing)
└── requirements.txt   (Flask, JWT, Mail)
```

**Key Concepts Learned:**
- Complete 2FA authentication flow
- Account lockout mechanisms
- Audit logging for security
- JWT token generation and validation
- Role-based access control

---

## 📚 Summary: 3-Day Learning Path

### Day 1: Foundation
```
User Roles & Permissions
        ↓
Password Hashing (PBKDF2-SHA256)
        ↓
Build: User model, password functions, user creation
```

### Day 2: OTP & Authorization
```
Middleware Concept
        ↓
OTP Generation & Email
        ↓
Role-Based Access Decorators
        ↓
Build: OTP model, send email, RBAC decorators
```

### Day 3: Complete 2FA System
```
2FA Flow & Account Lockout
        ↓
Login Attempt Tracking
        ↓
JWT Token & Protected Routes
        ↓
Build: Complete login system, lockout, audit logging
```

---

## 🎓 What You've Learned

**Day 1 (Foundations)**
- ✅ Why roles and permissions are important
- ✅ How passwords are securely hashed
- ✅ PBKDF2 algorithm and salt concept

**Day 2 (Middleware & OTP)**
- ✅ Middleware pattern and use cases
- ✅ OTP generation and verification
- ✅ Email integration with Flask-Mail
- ✅ Decorator-based RBAC

**Day 3 (Security & Complete System)**
- ✅ Complete 2FA authentication flow
- ✅ Account lockout and brute force protection
- ✅ Audit logging for compliance
- ✅ JWT tokens and protected routes
- ✅ How all pieces fit together

---

## 🚀 Next Steps (Optional)

After Day 3, you can extend the system with:
- [ ] TOTP support (Google Authenticator)
- [ ] SMS OTP as backup
- [ ] Password reset flow
- [ ] Email verification
- [ ] Session management
- [ ] Rate limiting
- [ ] Monitoring and alerts

---

## 📖 How to Use This Guide

**Option A: Structured Learning (Recommended)**
1. Read "📚 Study Topics" section carefully
2. Follow "💻 Hands-On" code examples
3. Complete "✅ Assignment" section
4. Run "🧪 Tests" to verify

**Option B: Quick Reference**
- Jump to "💻 Hands-On" to see code
- Copy code into your files
- Test with provided examples

**Option C: Learn by Building**
- Follow assignments first
- Refer back to study topics when confused
- Experiment and modify code

---

**Happy Learning! This is a real-world authentication system.** 🚀
