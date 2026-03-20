# Quick Start Guide for Week 8 - 2FA Authentication System

## 🚀 5-Minute Setup

### Step 1: Install Dependencies
```bash
cd week-8
pip install -r requirements.txt
```

### Step 2: Configure Email (Gmail)

1. Go to: https://myaccount.google.com/security
2. Enable "2-Step Verification"
3. Go to: https://myaccount.google.com/apppasswords
4. Create an "App password" for Mail > Windows Computer
5. Google will generate a 16-character password
6. Copy this password

### Step 3: Create .env File

```bash
# Copy template
cp .env.example .env

# Edit .env and add:
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=<16-char app password from step 5>
JWT_SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_urlsafe(32))">
```

### Step 4: Run Application

```bash
python main.py
```

Server will start at: **http://localhost:5000**

---

## 📋 Quick API Tests

### 1. Health Check
```bash
curl http://localhost:5000/
```

### 2. Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "your-email@gmail.com",
    "password": "TestPassword123"
  }'
```

### 3. Login (Sends OTP to Email)
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPassword123"
  }'
```
**Note:** Copy the `user_id` from response

### 4. Check Email for OTP Code

**Check your email inbox for 6-digit OTP**

### 5. Verify OTP (Replace with actual values)
```bash
curl -X POST http://localhost:5000/api/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "otp_code": "123456"
  }'
```
**Note:** Copy the `access_token` from response

### 6. Access Protected Route (Replace with your token)
```bash
curl http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🧪 Run Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest test_api.py -v

# Run specific test
pytest test_api.py::test_user_registration -v

# With coverage report
pytest test_api.py --cov=main --cov=auth
```

---

## 📁 Project Structure

```
week-8/
├── main.py              ← Flask app and routes
├── auth.py              ← Authentication logic
├── models.py            ← Database models
├── database.py          ← Database setup
├── config.py            ← Configuration
├── requirements.txt     ← Dependencies
├── test_api.py          ← Tests
├── docker-compose.yml   ← Docker setup (optional)
├── .env.example         ← Environment template
├── .env                 ← Your actual config (create this)
└── README.md            ← Full documentation
```

---

## 🔐 Key Features to Demo

### Feature 1: 2FA with Email OTP
- Register → Login → Receive OTP via email → Verify OTP → Get Token

### Feature 2: Account Lockout
- Try logging in 5 times with wrong password
- Account will be locked for 30 minutes
- Admin can unlock with: `POST /api/users/<id>/unlock`

### Feature 3: Role-Based Access
- Admin can view all users: `GET /api/users` (needs admin token)
- User cannot access this endpoint: Returns 403 Forbidden

### Feature 4: 2FA Middleware
- Some endpoints require 2FA verification
- Without verification: Returns 403 Forbidden
- Example: `GET /api/users/profile`

---

## 🛠️ Troubleshooting

### Issue: "No module named 'flask'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "OTP not received in email"
**Check:**
1. Is `MAIL_USERNAME` correct? (your gmail)
2. Is `MAIL_PASSWORD` correct? (16-char app password, not regular password)
3. Check spam folder
4. Try resend: `POST /api/auth/resend-otp`

### Issue: "SMTP error - Connection refused"
**Check:**
1. Gmail is configured: https://myaccount.google.com/apppasswords
2. 2-Step Verification is enabled
3. App password is correct (not regular password)

### Issue: "Database locked" or "Permission denied"
**Solution:**
```bash
# Delete old database
rm auth_system.db

# Run app again to recreate
python main.py
```

### Issue: "Cannot import module"
**Solution:**
```bash
# Verify all requirements installed
pip list | grep -i flask

# Reinstall everything
pip install -r requirements.txt --force-reinstall
```

---

## 🚀 Next Steps

1. **Read Full Documentation**: See `README.md` for complete details
2. **Explore API**: Try all endpoints with different roles
3. **Test Security**: Try to bypass authentication (should fail!)
4. **Customize**: Modify config.py for your needs
5. **Deploy**: Use docker-compose for production setup

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| Start app | `python main.py` |
| Run tests | `pytest test_api.py -v` |
| Install deps | `pip install -r requirements.txt` |
| Generate JWT secret | `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| Reset database | `rm auth_system.db` |
| View database | `sqlite3 auth_system.db` |

---

## 🎓 Learning Outcomes

After completing this project, you'll understand:
- ✅ Two-Factor Authentication flows
- ✅ OTP generation and verification
- ✅ Role-Based Access Control (RBAC)
- ✅ Password hashing and security
- ✅ Account lockout mechanisms
- ✅ JWT authentication
- ✅ Flask middleware/decorators
- ✅ Email integration
- ✅ API security best practices
- ✅ Audit logging and compliance

---

**Happy Learning! 🚀**
