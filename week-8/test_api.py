import pytest
import json
from main import app, db
from models import User
from config import TestingConfig

@pytest.fixture
def client():
    """Create test client"""
    app.config.from_object(TestingConfig)
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture
def admin_user(client):
    """Create admin user for testing"""
    response = client.post('/api/auth/bootstrap/admin',
        headers={'X-ADMIN-BOOTSTRAP-KEY': TestingConfig.ADMIN_BOOTSTRAP_KEY},
        json={
            'username': 'admin_test',
            'email': 'admin@test.com',
            'password': 'Admin@12345'
        }
    )
    return response.get_json()

@pytest.fixture
def regular_user(client):
    """Create regular user for testing"""
    response = client.post('/api/auth/register',
        json={
            'username': 'user_test',
            'email': 'user@test.com',
            'password': 'User@12345',
            'role': 'user'
        }
    )
    return response.get_json()

# ==================== Testing ====================

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'API is running'

def test_user_registration(client):
    """Test user registration"""
    response = client.post('/api/auth/register',
        json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPassword123'
        }
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'User registered successfully'
    assert data['user']['username'] == 'testuser'

def test_registration_duplicate_username(client, regular_user):
    """Test registration with duplicate username"""
    response = client.post('/api/auth/register',
        json={
            'username': 'user_test',  # Already exists
            'email': 'newuser@test.com',
            'password': 'Password123'
        }
    )
    assert response.status_code == 400
    data = response.get_json()
    assert 'already exists' in data['message']

def test_registration_weak_password(client):
    """Test registration with weak password"""
    response = client.post('/api/auth/register',
        json={
            'username': 'weakpass',
            'email': 'weak@test.com',
            'password': 'weak'
        }
    )
    assert response.status_code == 400
    data = response.get_json()
    assert 'at least 8 characters' in data['message']

def test_public_registration_rejects_admin_role(client):
    """Public register endpoint must not allow elevated roles."""
    response = client.post('/api/auth/register',
        json={
            'username': 'badadmin',
            'email': 'badadmin@test.com',
            'password': 'Admin@12345',
            'role': 'admin'
        }
    )
    assert response.status_code == 403
    data = response.get_json()
    assert 'Public registration only allows the user role' in data['message']

def test_bootstrap_admin_requires_key(client):
    """Admin bootstrap endpoint should reject missing or invalid bootstrap key."""
    response = client.post('/api/auth/bootstrap/admin',
        json={
            'username': 'admin_no_key',
            'email': 'admin_no_key@test.com',
            'password': 'Admin@12345'
        }
    )
    assert response.status_code == 401

def test_bootstrap_admin_creates_first_admin_only(client):
    """Bootstrap endpoint can create only the first admin account."""
    first = client.post('/api/auth/bootstrap/admin',
        headers={'X-ADMIN-BOOTSTRAP-KEY': TestingConfig.ADMIN_BOOTSTRAP_KEY},
        json={
            'username': 'admin_one',
            'email': 'admin_one@test.com',
            'password': 'Admin@12345'
        }
    )
    assert first.status_code == 201

    second = client.post('/api/auth/bootstrap/admin',
        headers={'X-ADMIN-BOOTSTRAP-KEY': TestingConfig.ADMIN_BOOTSTRAP_KEY},
        json={
            'username': 'admin_two',
            'email': 'admin_two@test.com',
            'password': 'Admin@12345'
        }
    )
    assert second.status_code == 409

def test_login_triggers_otp(client, regular_user):
    """Test that login triggers OTP request"""
    response = client.post('/api/auth/login',
        json={
            'username': 'user_test',
            'password': 'User@12345'
        }
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['two_fa_required'] == True
    assert 'user_id' in data
    assert 'OTP sent' in data['message']

def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post('/api/auth/login',
        json={
            'username': 'nonexistent',
            'password': 'wrong_password'
        }
    )
    assert response.status_code == 401
    data = response.get_json()
    assert 'Invalid' in data['message']

def test_admin_login_with_admin_user(client, admin_user):
    """Test separate admin login endpoint with admin credentials"""
    response = client.post('/api/auth/admin/login',
        json={
            'username': 'admin_test',
            'password': 'Admin@12345'
        }
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['two_fa_required'] == True
    assert data['username'] == 'admin_test'

def test_admin_login_rejects_non_admin_user(client, regular_user):
    """Test separate admin login endpoint denies non-admin users"""
    response = client.post('/api/auth/admin/login',
        json={
            'username': 'user_test',
            'password': 'User@12345'
        }
    )
    assert response.status_code == 403
    data = response.get_json()
    assert 'Access denied' in data['message']

def test_verify_otp_success(client, regular_user):
    """Test successful OTP verification"""
    # First, login to get user_id and trigger OTP
    login_response = client.post('/api/auth/login',
        json={
            'username': 'user_test',
            'password': 'User@12345'
        }
    )
    user_id = login_response.get_json()['user_id']
    
    # Get OTP code from database
    from models import OTP
    with app.app_context():
        otp = OTP.query.filter_by(user_id=user_id).order_by(OTP.created_at.desc()).first()
        otp_code = otp.otp_code
    
    # Verify OTP
    response = client.post('/api/auth/verify-otp',
        json={
            'user_id': user_id,
            'otp_code': otp_code
        }
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'OTP verified' in data['message']
    assert 'access_token' in data
    assert data['user']['username'] == 'user_test'

def test_verify_invalid_otp(client, regular_user):
    """Test OTP verification with invalid code"""
    login_response = client.post('/api/auth/login',
        json={
            'username': 'user_test',
            'password': 'User@12345'
        }
    )
    user_id = login_response.get_json()['user_id']
    
    response = client.post('/api/auth/verify-otp',
        json={
            'user_id': user_id,
            'otp_code': '000000'
        }
    )
    assert response.status_code == 401
    data = response.get_json()
    assert 'Invalid OTP' in data['message']

def test_account_lockout(client):
    """Test account lockout after 5 failed attempts"""
    # Register user
    client.post('/api/auth/register',
        json={
            'username': 'locktest',
            'email': 'lock@test.com',
            'password': 'Password123'
        }
    )
    
    # Make 5 failed login attempts
    for i in range(5):
        response = client.post('/api/auth/login',
            json={
                'username': 'locktest',
                'password': 'wrong_password'
            }
        )
        assert response.status_code == 401
    
    # Try to login with correct password - should be locked
    response = client.post('/api/auth/login',
        json={
            'username': 'locktest',
            'password': 'Password123'
        }
    )
    assert response.status_code == 401
    data = response.get_json()
    assert 'Account locked' in data['message']

def test_list_users_admin_only(client, admin_user, regular_user):
    """Test that only admins can list users"""
    # First get admin token
    login_response = client.post('/api/auth/login',
        json={
            'username': 'admin_test',
            'password': 'Admin@12345'
        }
    )
    user_id = login_response.get_json()['user_id']
    
    # Get OTP and verify
    from models import OTP
    with app.app_context():
        otp = OTP.query.filter_by(user_id=user_id).order_by(OTP.created_at.desc()).first()
        otp_code = otp.otp_code
    
    verify_response = client.post('/api/auth/verify-otp',
        json={
            'user_id': user_id,
            'otp_code': otp_code
        }
    )
    admin_token = verify_response.get_json()['access_token']
    
    # List users with admin token
    response = client.get('/api/users',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'users' in data

def test_update_user_role_admin_only(client, admin_user, regular_user):
    """Test that only admins can update user roles"""
    admin_login = client.post('/api/auth/login',
        json={
            'username': 'admin_test',
            'password': 'Admin@12345'
        }
    )
    admin_user_id = admin_login.get_json()['user_id']
    
    # Get OTP and verify for admin
    from models import OTP
    with app.app_context():
        otp = OTP.query.filter_by(user_id=admin_user_id).order_by(OTP.created_at.desc()).first()
        otp_code = otp.otp_code
    
    admin_verify = client.post('/api/auth/verify-otp',
        json={
            'user_id': admin_user_id,
            'otp_code': otp_code
        }
    )
    admin_token = admin_verify.get_json()['access_token']
    
    # Get regular user ID
    with app.app_context():
        user = User.query.filter_by(username='user_test').first()
        user_id = user.id
    
    # Update user role
    response = client.put(f'/api/users/{user_id}/role',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={'role': 'moderator'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['user']['role'] == 'moderator'

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
