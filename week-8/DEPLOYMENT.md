# Deployment Guide - Week 8 2FA Authentication System

## Overview

This guide covers deploying the 2FA Authentication system to production environments.

---

## 📋 Pre-Deployment Checklist

### Code Quality
- [ ] All tests passing (`pytest test_api.py -v`)
- [ ] No debug mode enabled
- [ ] All print statements removed
- [ ] Error handling comprehensive
- [ ] Input validation complete

### Security Configuration
- [ ] JWT_SECRET_KEY changed (32+ chars)
- [ ] FLASK_ENV set to "production"
- [ ] Debug mode disabled
- [ ] HTTPS enforced
- [ ] CORS properly configured
- [ ] Database backups configured
- [ ] ENABLE_ADMIN_BOOTSTRAP enabled only for first admin creation
- [ ] ENABLE_ADMIN_BOOTSTRAP disabled after bootstrap completes
- [ ] ADMIN_BOOTSTRAP_KEY rotated or removed after bootstrap

### Environment Variables
- [ ] Database connection string updated
- [ ] Email credentials verified
- [ ] All secrets in `.env` file
- [ ] `.env` file in `.gitignore`
- [ ] `.env.example` committed (no secrets)

### Dependencies
- [ ] All packages in requirements.txt
- [ ] No development-only packages in prod
- [ ] Versions pinned
- [ ] Security updates applied

---

## 🚀 Deployment Options

### Option 1: Docker Container

#### Build Docker Image

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=main.py
ENV FLASK_ENV=production

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

#### Build & Run

```bash
# Build image
docker build -t 2fa-auth-system:1.0 .

# Run container
docker run -d \
  --name 2fa-auth \
  -p 5000:5000 \
  --env-file .env \
  -v auth_data:/app/instance \
  2fa-auth-system:1.0
```

#### Docker Compose

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: production
      DATABASE_URL: postgresql://user:pass@db:5432/auth_db
    env_file:
      - .env
    depends_on:
      - db
    volumes:
      - ./logs:/app/logs

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: auth_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: auth_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Option 2: Heroku

#### Procfile
```
web: gunicorn main:app
worker: flask db upgrade
```

#### Deploy
```bash
# Login
heroku login

# Create app
heroku create 2fa-auth-system

# Set environment variables
heroku config:set JWT_SECRET_KEY=<your-secret>
heroku config:set MAIL_USERNAME=<your-email>
heroku config:set MAIL_PASSWORD=<your-app-password>
heroku config:set DATABASE_URL=postgresql://...

# Deploy
git push heroku main
```

### Option 3: AWS ECS

#### Task Definition
```json
{
  "family": "2fa-auth-system",
  "containerDefinitions": [
    {
      "name": "2fa-auth",
      "image": "2fa-auth-system:1.0",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "FLASK_ENV",
          "value": "production"
        }
      ]
    }
  ]
}
```

### Option 4: DigitalOcean App Platform

```yaml
name: 2fa-auth-system
services:
- name: api
  github:
    repo: your-username/2fa-auth-system
    branch: main
  build_command: pip install -r requirements.txt
  run_command: gunicorn main:app
  http_port: 5000
  envs:
  - key: FLASK_ENV
    value: production
databases:
- name: postgres
  engine: PG
  version: "15"
```

---

## 🗄️ Database Migration

### PostgreSQL Setup

```sql
-- Create database
CREATE DATABASE auth_db;

-- Create user
CREATE USER auth_user WITH PASSWORD 'strong_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE auth_db TO auth_user;

-- Connect and initialize
\c auth_db
```

### Migrate from SQLite to PostgreSQL

```bash
# Install migration tool
pip install alembic

# Export from SQLite
sqlite3 auth_system.db ".schema" > schema.sql

# Import to PostgreSQL
psql -U auth_user -d auth_db -f schema.sql
```

### Connection String Update
```bash
# .env
DATABASE_URL=postgresql://auth_user:password@localhost:5432/auth_db
```

---

## 🔒 HTTPS/TLS Configuration

### Let's Encrypt with Nginx

```nginx
server {
    listen 80;
    server_name api.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.example.com;

    ssl_certificate /etc/letsencrypt/live/api.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.example.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Certbot Setup
```bash
# Install
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --nginx -d api.example.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

---

## ⚙️ Production Configuration

### Gunicorn Configuration

```python
# gunicorn_config.py
import multiprocessing

bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 60
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
```

### Run with Gunicorn
```bash
gunicorn --config gunicorn_config.py main:app
```

### Supervisor Configuration

```ini
[program:2fa-auth]
command=/venv/bin/gunicorn --bind 127.0.0.1:5000 main:app
directory=/app
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/2fa-auth/app.log
```

---

## 📊 Monitoring & Logging

### Application Logging

```python
# Add to main.py
import logging
from pythonjsonlogger import jsonlogger

logHandler = logging.FileHandler('logs/app.log')
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
```

### Nginx Access Logs
```bash
tail -f /var/log/nginx/access.log

# Filter failed logins
grep "api/auth/login" /var/log/nginx/access.log | grep 401
```

### Database Query Logging
```python
# Enable SQLAlchemy logging
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

### Monitoring Tools
- **Datadog**: APM and monitoring
- **New Relic**: Performance monitoring
- **Sentry**: Error tracking
- **ELK Stack**: Log aggregation

---

## 🚨 Error Handling

### Custom Error Pages

```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Server error: {error}')
    return jsonify({'message': 'Internal server error'}), 500
```

### Health Check Endpoint

```python
@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Check database
        db.session.execute('SELECT 1')
        status = 'healthy'
        code = 200
    except Exception as e:
        status = 'unhealthy'
        code = 500
        app.logger.error(f'Health check failed: {e}')
    
    return jsonify({'status': status}), code
```

---

## 🔄 Backup Strategy

### Database Backups

```bash
#!/bin/bash
# backup.sh
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# PostgreSQL backup
pg_dump -U auth_user -h localhost auth_db | gzip > backups/auth_db_$TIMESTAMP.sql.gz

# Encrypt backup
openssl enc -aes-256-cbc -salt -in backups/auth_db_$TIMESTAMP.sql.gz \
    -out backups/auth_db_$TIMESTAMP.sql.gz.enc

# Upload to cloud
aws s3 cp backups/auth_db_$TIMESTAMP.sql.gz.enc s3://backup-bucket/
```

### Restore from Backup
```bash
# Decrypt
openssl enc -aes-256-cbc -d -in backup.sql.gz.enc -out backup.sql.gz

# Restore
gunzip backup.sql.gz
psql -U auth_user -d auth_db < backup.sql
```

---

## 📈 Scaling Considerations

### Horizontal Scaling

```yaml
# Multiple app instances
services:
  app-1:
    image: 2fa-auth-system:1.0
    ports:
      - "5001:5000"
  app-2:
    image: 2fa-auth-system:1.0
    ports:
      - "5002:5000"
  app-3:
    image: 2fa-auth-system:1.0
    ports:
      - "5003:5000"
  
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

### Session Management

For multiple instances, use Redis:

```python
from flask_session import Session
from flask_redis import FlaskRedis

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
Session(app)
```

### Database Connection Pooling

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}
```

---

## 🚀 CI/CD Pipeline

### GitHub Actions

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - run: pip install -r requirements.txt
    - run: pytest test_api.py -v

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to production
      run: |
        # Deploy script here
        echo "Deploying to production..."
```

---

## 📊 Post-Deployment

### Verification Checklist

- [ ] Application starts without errors
- [ ] Health check endpoint returns 200
- [ ] Database migrations completed
- [ ] HTTPS certificate valid
- [ ] Email OTP working
- [ ] Admin panel accessible
- [ ] All API endpoints responding
- [ ] Monitoring/logging active
- [ ] Backups running
- [ ] Rate limiting active

### Performance Testing

```bash
# Load testing with Apache Bench
ab -n 1000 -c 10 http://localhost:5000/

# Real browser testing
# Use Postman or curl for API testing

# Monitor CPU/Memory
htop
```

---

## 🔐 Production Security Hardening

### Firewall Rules
```bash
# Allow only necessary ports
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22/tcp  # SSH
ufw enable
```

### Process Isolation
```bash
# Create system user
useradd -r -s /bin/bash app

# Run app as non-root
su - app -c "gunicorn ..."
```

### Environment Secrets
```bash
# Never commit secrets
echo ".env" >> .gitignore

# Use secrets management
# - AWS Secrets Manager
# - HashiCorp Vault
# - 1Password CLI
```

---

## 🆘 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Database connection failed | Check DATABASE_URL, verify network |
| Email OTP not sending | Verify MAIL_* credentials, check spam |
| JWT token errors | Verify JWT_SECRET_KEY, check token expiration |
| 500 errors | Check application logs, verify all dependencies |
| Port already in use | Change port or kill process: `lsof -i :5000` |

---

## 📞 Support

For deployment issues:
1. Check logs: `docker logs 2fa-auth`
2. Verify environment variables
3. Test database connectivity
4. Check firewall/security groups
5. Review security documentation

---

**Production-Ready Deployment** ✅
