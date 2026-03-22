# Week 8: Two-Factor Authentication with Email OTP & Role-Based Access Control

**Status:** Ready to Learn 📚 | **Date:** March 2026

## 📌 Choose Your Learning Path

👉 **NEW: 3-Day Incremental Learning** → [**Start Here: 3DAY_LEARNING_PATH.md**](3DAY_LEARNING_PATH.md)
- **Day 1:** User Roles & Permissions + Password Hashing
- **Day 2:** Middleware Basics & OTP Implementation
- **Day 3:** 2FA with Account Lockout & Audit Logging

✅ **Complete Implementation Details Below:**

A comprehensive authentication system implementing Two-Factor Authentication (2FA) with email-based OTP verification, role-based permissions, password hashing, middleware-based access control, and account lockout protection.

## 🎯 Project Overview

A production-ready authentication system featuring:
- **Email-Based OTP Verification** for 2FA with expiring codes
- **Role-Based Access Control (RBAC)** with admin, user, and moderator roles
- **Password Hashing** using PBKDF2-SHA256 with secure salt generation
- **Middleware-Based Authorization** with decorators for role and 2FA verification
- **Account Lockout** after 5 failed login attempts
- **Login Attempt Tracking** for security auditing
- **JWT-Based Authentication** with secure token generation
- **Email Notification System** for OTP delivery
- **Admin Dashboard** with user statistics and management

## 🚀 Features

### 🔐 Two-Factor Authentication (2FA)
- **Email OTP Generation**: 6-digit random codes sent via email
- **OTP Expiration**: Codes expire after 5 minutes
- **OTP Verification**: Limited attempts to prevent brute force
- **Resend Capability**: Users can request new OTP codes
- **Verified State Tracking**: System remembers 2FA completion status

### 👥 Role-Based Access Control (RBAC)
- **Three Role Tiers**: Admin, User, Moderator
- **Permission-Based Access**: Different API endpoints for different roles
- **Admin Features**:
  - View all users and their details
  - Lock/unlock user accounts
  - Update user roles
  - Access admin dashboard
- **Moderator Features**:
  - View user information
  - Edit user profiles
  - View and moderate reports
- **User Features**:
  - View and edit own profile
  - Create and view notes

### 🔑 Password & Security
- **PBKDF2-SHA256 Hashing**: Industry-standard password hashing
- **16-byte Salt**: Cryptographically secure salt generation
- **Minimum 8 Characters**: Password strength requirement
- **Secure Password Verification**: Constant-time comparison

### 🛡️ Account Security
- **Account Lockout**: 5 failed login attempts trigger 30-minute lockout
- **Failed Attempt Tracking**: System records all login failures
- **Login Audit Log**: Track successful and failed login attempts
- **IP Address Logging**: Record IP addresses for suspicious activity detection

### 🔗 Middleware & Decorators
- **@require_2fa_verified**: Ensures 2FA completion before access
- **@require_role()**: Enforces role-based access control
- **@require_2fa_and_role()**: Combined authentication and authorization
- **JWT Verification**: Built-in JWT token validation

### 📧 Email Integration
- **Gmail SMTP Support**: Easy Gmail configuration
- **OTP Email Notifications**: Automatic OTP delivery
- **Customizable Templates**: Template-based email generation
- **Error Handling**: Graceful failure handling

## 🛠️ Technical Stack

- **Backend Framework**: Flask 2.3.3
- **Database**: SQLAlchemy with PostgreSQL/SQLite support
- **Authentication**: Flask-JWT-Extended 4.5.3
- **Email**: Flask-Mail 0.9.1
- **Password Hashing**: Werkzeug security utilities
- **OTP Generation**: Python random module
- **Testing**: pytest with fixtures

## 📁 File Structure

```
week-8/
├── main.py              # Flask application and route endpoints
├── auth.py              # Authentication logic and decorators
├── models.py            # Database models (User, OTP, LoginAttempt, Role)
├── database.py          # SQLAlchemy database initialization
├── config.py            # Configuration for dev/test/production
├── test_api.py          # Comprehensive API tests
├── requirements.txt     # Python dependencies
├── docker-compose.yml   # PostgreSQL and Redis setup
└── README.md           # Project documentation
```

## 📊 Database Models

### User Model
```python
User(
    id: Integer (PK),
    username: String (unique),
    email: String (unique),
    password_hash: String,
    role: String (admin/user/moderator),
    is_active: Boolean,
    is_email_verified: Boolean,
    two_fa_enabled: Boolean,
    two_fa_verified: Boolean,
    failed_login_attempts: Integer,
    locked_until: DateTime,
    created_at: DateTime,
    updated_at: DateTime,
    last_login: DateTime
)
```

### OTP Model
```python
OTP(
    id: Integer (PK),
    user_id: Integer (FK),
    otp_code: String (6 digits),
    is_verified: Boolean,
    created_at: DateTime,
    expires_at: DateTime,
    attempts: Integer
)
```

### LoginAttempt Model
```python
LoginAttempt(
    id: Integer (PK),
    user_id: Integer (FK),
    ip_address: String,
    success: Boolean,
    timestamp: DateTime,
    reason: String
)
```

### Role Model
```python
Role(
    id: Integer (PK),
    name: String (unique),
    description: String,
    permissions: JSON
)
```

## 🔄 Authentication Flow

### 1. User Registration
```
POST /api/auth/register
├── Input: username, email, password
├── Hash password using PBKDF2-SHA256
├── Public signup always creates role=user
└── Response: User details with ID
```

### 1.1 Admin Bootstrap (One-Time)
```
POST /api/auth/bootstrap/admin
├── Header: X-ADMIN-BOOTSTRAP-KEY
├── Input: username, email, password
├── Creates first admin account only
└── Response: Admin details with ID
```

### 2. User Login
```
POST /api/auth/login
├── Input: username, password
├── Check account lockout status
├── Verify password against hash
├── Reset failed attempts on success
├── Generate 6-digit OTP
├── Send OTP via email
└── Response: user_id (for OTP verification)
```

### 3. OTP Verification
```
POST /api/auth/verify-otp
├── Input: user_id, otp_code
├── Check OTP expiration (5 minutes)
├── Verify OTP code matches
├── Mark OTP as verified
├── Generate JWT token
├── Update last login timestamp
└── Response: JWT access token
```

### 4. Resend OTP
```
POST /api/auth/resend-otp
├── Input: user_id
├── Delete previous unverified OTP
├── Generate new OTP code
├── Send new OTP via email
└── Response: Success message
```

## 🚀 API Endpoints

### Authentication Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/bootstrap/admin` | Bootstrap first admin (one-time) | No |
| POST | `/api/auth/login` | Login and get OTP | No |
| POST | `/api/auth/admin/login` | Admin login and get OTP | No |
| POST | `/api/auth/verify-otp` | Verify OTP and get token | No |
| POST | `/api/auth/resend-otp` | Resend OTP to email | No |

### User Endpoints
| Method | Endpoint | Description | Auth Required | Role Required |
|--------|----------|-------------|----------------|---------------|
| GET | `/api/users/profile` | Get user profile | Yes (2FA) | - |
| PUT | `/api/users/profile` | Update profile | Yes (2FA) | - |
| GET | `/api/users` | List all users | Yes (2FA) | admin |
| GET | `/api/users/<id>` | Get user details | Yes (2FA) | admin |
| POST | `/api/users/<id>/lock` | Lock user account | Yes (2FA) | admin |
| POST | `/api/users/<id>/unlock` | Unlock user account | Yes (2FA) | admin |
| PUT | `/api/users/<id>/role` | Update user role | Yes (2FA) | admin |

### Admin Endpoints
| Method | Endpoint | Description | Auth Required | Role Required |
|--------|----------|-------------|----------------|---------------|
| GET | `/api/admin/dashboard` | Admin dashboard stats | Yes (2FA) | admin |

## 📝 Usage Examples

### 0. What To Do First (Postman + Bootstrap Admin)

1. Set environment variables and restart app:
  - `ENABLE_ADMIN_BOOTSTRAP=True`
  - `ADMIN_BOOTSTRAP_KEY=change-me-bootstrap-key`
2. Re-import the latest Postman collection: `api.postman_collection.json`.
3. Set collection variable `admin_bootstrap_key` to the same value as `ADMIN_BOOTSTRAP_KEY`.
4. Run requests in order:
  - `Health Check`
  - `Bootstrap Admin (One-Time)`
  - `Admin Login (Send OTP)`
  - `Verify OTP`
5. Use `admin_token` for admin routes.
6. After first admin is created, set `ENABLE_ADMIN_BOOTSTRAP=False` and restart app.

### 1. Register a New User

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePassword123"
  }'
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "user"
  }
}
```

### 1.1 Bootstrap an Admin (One-Time)

Use these local/dev credentials for quick testing:

- Username: `admin_test`
- Email: `admin@test.com`
- Password: `Admin@12345`
- Header `X-ADMIN-BOOTSTRAP-KEY`: `change-me-bootstrap-key`

```bash
curl -X POST http://localhost:5000/api/auth/bootstrap/admin \
  -H "Content-Type: application/json" \
  -H "X-ADMIN-BOOTSTRAP-KEY: change-me-bootstrap-key" \
  -d '{
    "username": "admin_test",
    "email": "admin@test.com",
    "password": "Admin@12345"
  }'
```

If this returns:
- `401`: `X-ADMIN-BOOTSTRAP-KEY` does not match `ADMIN_BOOTSTRAP_KEY`
- `403`: `ENABLE_ADMIN_BOOTSTRAP` is disabled
- `409`: an admin already exists (expected after first success)

### 2. Login and Request OTP

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePassword123"
  }'
```

**Response:**
```json
{
  "message": "OTP sent successfully to your email",
  "user_id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "two_fa_required": true,
  "otp_expiry_minutes": 5
}
```

### 3. Verify OTP and Get JWT Token

```bash
curl -X POST http://localhost:5000/api/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "otp_code": "123456"
  }'
```

**Response:**
```json
{
  "message": "OTP verified successfully",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "user"
  }
}
```

### 4. Access Protected Route with 2FA

```bash
curl -X GET http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "user",
    "is_active": true,
    "two_fa_enabled": true,
    "two_fa_verified": true,
    "is_email_verified": false,
    "last_login": "2026-03-20T15:30:45.123456",
    "created_at": "2026-03-20T15:25:00.000000"
  }
}
```

### 5. Admin List All Users

```bash
curl -X GET http://localhost:5000/api/users \
  -H "Authorization: Bearer {ADMIN_TOKEN}"
```

**Response:**
```json
{
  "users": [
    {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "role": "user",
      "is_active": true,
      "created_at": "2026-03-20T15:25:00.000000"
    }
  ],
  "total": 1,
  "pages": 1,
  "current_page": 1
}
```

### 6. Admin Lock User Account

```bash
curl -X POST http://localhost:5000/api/users/1/lock \
  -H "Authorization: Bearer {ADMIN_TOKEN}"
```

**Response:**
```json
{
  "message": "User account locked successfully"
}
```

### 7. Admin Update User Role

```bash
curl -X PUT http://localhost:5000/api/users/1/role \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {ADMIN_TOKEN}" \
  -d '{
    "role": "moderator"
  }'
```

**Response:**
```json
{
  "message": "User role updated successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "role": "moderator"
  }
}
```

## 🔧 Installation & Setup

### 1. Install Dependencies

```bash
cd week-8
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file:

```env
# Database
DATABASE_URL=sqlite:///auth_system.db

# JWT
JWT_SECRET_KEY=your-secret-key-change-this

# Email Configuration (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@2faauth.app

# Admin Bootstrap (one-time use)
ENABLE_ADMIN_BOOTSTRAP=True
ADMIN_BOOTSTRAP_KEY=change-me-bootstrap-key

# Flask
FLASK_ENV=development
FLASK_APP=main.py
```

### 3. Gmail App Password Setup

1. Enable 2FA on your Gmail account
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use generated password in `MAIL_PASSWORD` environment variable

### 4. Initialize Database

```bash
python -c "from main import app, db; app.app_context().push(); db.create_all()"
```

### 5. Run the Application

```bash
python main.py
```

Server will run on `http://localhost:5000`

## 🧪 Testing

### Run All Tests

```bash
pytest test_api.py -v
```

### Run Specific Test

```bash
pytest test_api.py::test_user_registration -v
```

### Test Coverage

```bash
pytest test_api.py --cov=main --cov=auth --cov=models
```

### Test Scenarios

- ✅ User registration
- ✅ Duplicate username/email validation
- ✅ Weak password detection
- ✅ Login with OTP trigger
- ✅ Invalid credentials handling
- ✅ OTP verification (success and failure)
- ✅ Invalid OTP attempt
- ✅ Account lockout after 5 failed attempts
- ✅ Role-based access control
- ✅ 2FA enforcement
- ✅ Admin user management

## 🔐 Security Features

### Password Security
- ✅ PBKDF2-SHA256 hashing algorithm
- ✅ 16-byte cryptographic salt
- ✅ Minimum 8-character requirement
- ✅ Constant-time comparison

### Account Protection
- ✅ 5 failed login attempt lockout
- ✅ 30-minute lockout duration
- ✅ Account unlock by admin
- ✅ Login attempt logging

### OTP Security
- ✅ 6-digit numeric codes
- ✅ 5-minute expiration
- ✅ Single use verification
- ✅ Maximum 3 verification attempts
- ✅ Email delivery confirmation

### API Security
- ✅ JWT token-based authentication
- ✅ Role-based access control
- ✅ 2FA verification middleware
- ✅ Rate limiting ready (can be added)
- ✅ CORS ready (can be configured)

## 📊 Security Audit Trail

All login attempts are logged with:
- User ID
- Success/Failure status
- IP address
- Timestamp
- Failure reason

Access this data for security audit reporting:

```python
from models import LoginAttempt
failed_attempts = LoginAttempt.query.filter_by(success=False).all()
```

## 🚀 Deployment Considerations

### For Production:
1. Change `JWT_SECRET_KEY` to a strong random value
2. Set `FLASK_ENV=production`
3. Use PostgreSQL instead of SQLite
4. Enable HTTPS/TLS
5. Set up proper email service (SendGrid, AWS SES, etc.)
6. Implement rate limiting
7. Add CORS configuration
8. Set up database backups
9. Use environment variables via `.env` file
10. Enable logging and monitoring
11. Disable `ENABLE_ADMIN_BOOTSTRAP` after first admin is created

### Docker Deployment

```bash
# Start PostgreSQL and Redis
docker-compose up -d

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://auth_user:auth_password@localhost:5432/auth_db

# Run Flask app
python main.py
```

## 🔄 Role-Based Permission Matrix

| Permission | Admin | Moderator | User |
|------------|-------|-----------|------|
| View Profile | ✅ | ✅ | ✅ |
| Edit Profile | ✅ | ✅ | ✅ |
| Create Notes | ✅ | ✅ | ✅ |
| View All Users | ✅ | ✅ | ❌ |
| Edit Users | ✅ | ✅ | ❌ |
| Delete Users | ✅ | ❌ | ❌ |
| Lock/Unlock Users | ✅ | ❌ | ❌ |
| Change User Roles | ✅ | ❌ | ❌ |
| View Reports | ✅ | ✅ | ❌ |
| Moderate Reports | ✅ | ✅ | ❌ |
| Access Admin Dashboard | ✅ | ❌ | ❌ |

## 🎯 Key Learnings

### 1. Two-Factor Authentication
- Understanding OTP generation and validation
- Email integration and delivery
- Expiring token management
- Brute force protection

### 2. Role-Based Access Control
- Designing permission hierarchies
- Implementing decorator-based middleware
- Managing role-specific features
- Audit trail for access control

### 3. Password Security
- PBKDF2 vs bcrypt vs argon2
- Salt generation and management
- Password hashing best practices
- Constant-time comparison

### 4. Account Lockout & Brute Force Protection
- Failed attempt tracking
- Exponential backoff strategies
- Account recovery mechanisms
- Security vs usability balance

### 5. JWT Authentication
- Token generation and validation
- Claim-based authorization
- Token expiration handling
- Refresh token strategies

### 6. Flask Middleware & Decorators
- Custom decorator patterns
- Chaining multiple decorators
- Error handling in middleware
- Dependency injection

## 🔮 Future Enhancements

1. **TOTP Support**: Time-based OTP using Google Authenticator
2. **Biometric Authentication**: Fingerprint/Face recognition
3. **SMS OTP**: Text message-based OTP
4. **Remember Device**: Skip 2FA on trusted devices
5. **OAuth Integration**: Google, GitHub, Microsoft login
6. **Rate Limiting**: Prevent password/OTP brute force
7. **Session Management**: Keep track of active sessions
8. **Password Reset**: Secure password reset flow
9. **Audit Logging**: Comprehensive security audit trail
10. **2FA Backup Codes**: Recovery codes for account access

## 📊 Performance Metrics

- **Password Hashing**: ~0.2s (configurable iterations)
- **OTP Generation**: <1ms
- **OTP Verification**: <5ms
- **JWT Creation**: <10ms
- **Database Query**: <50ms
- **Email Sending**: ~2-5s (external service)

## 🏆 Achievements

- ✅ **Robust 2FA System**: Email OTP with expiration
- ✅ **RBAC Implementation**: Three-tier role system
- ✅ **Security-First Design**: Account lockout and audit trail
- ✅ **Production-Ready Code**: Error handling and validation
- ✅ **Comprehensive Testing**: 11+ test cases covering all features
- ✅ **Complete Documentation**: API docs and usage examples
- ✅ **Middleware Pattern**: Reusable decorator-based auth

## 🔗 Configuration Reference

### OTP Settings
```python
OTP_EXPIRY_MINUTES = 5      # OTP valid for 5 minutes
OTP_LENGTH = 6              # 6-digit numeric OTP
```

### Account Lockout Settings
```python
MAX_LOGIN_ATTEMPTS = 5              # Lock after 5 failures
LOCKOUT_DURATION_MINUTES = 30       # Lock for 30 minutes
```

### Email Configuration
```python
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'
```

## 📞 Support & Troubleshooting

### OTP Not Received
1. Check `MAIL_USERNAME` and `MAIL_PASSWORD`
2. Verify Gmail App Password is enabled
3. Check spam folder
4. Enable "Less secure app access" (if not using App Password)

### Account Locked
1. Contact admin to unlock
2. Admin can use: `POST /api/users/<id>/unlock`
3. Wait 30 minutes for automatic unlock

### JWT Token Expired
1. Login again to get new token
2. Token expires after 1 hour
3. Implement refresh token flow for production

---

**Week 8 Complete** ✅ | **Next:** Advanced API Patterns Coming Soon
