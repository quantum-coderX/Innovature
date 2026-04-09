import os
import shutil
import tempfile
from decimal import Decimal

import pytest
from flask_jwt_extended import create_access_token

from auth import ROLE_BUYER, ROLE_SELLER, hash_password

TEST_ROOT = tempfile.mkdtemp(prefix="week11-tests-")
TEST_DB = os.path.join(TEST_ROOT, "test.db")
TEST_UPLOAD_ROOT = os.path.join(TEST_ROOT, "uploads")
TEST_UPLOAD_PRODUCTS = os.path.join(TEST_UPLOAD_ROOT, "products")
TEST_UPLOAD_THUMBNAILS = os.path.join(TEST_UPLOAD_ROOT, "thumbnails")

os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"
os.environ["JWT_SECRET_KEY"] = "week11-test-secret-key-32-bytes-min"
os.environ["UPLOAD_FOLDER"] = TEST_UPLOAD_PRODUCTS
os.environ["THUMBNAIL_FOLDER"] = TEST_UPLOAD_THUMBNAILS

from main import app as flask_app  # noqa: E402
from database import db  # noqa: E402
from models import Category, Product, User  # noqa: E402


@pytest.fixture(scope="session")
def app():
    flask_app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{TEST_DB}",
        UPLOAD_FOLDER=TEST_UPLOAD_PRODUCTS,
        THUMBNAIL_FOLDER=TEST_UPLOAD_THUMBNAILS,
        ALLOWED_IMAGE_TYPES={"image/jpeg", "image/png", "image/webp"},
        MAX_IMAGE_SIZE_BYTES=5 * 1024 * 1024,
        MAX_IMAGES_PER_PRODUCT=5,
        THUMBNAIL_SIZE=(300, 300),
    )
    return flask_app


@pytest.fixture(autouse=True)
def reset_state(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

    os.makedirs(TEST_UPLOAD_PRODUCTS, exist_ok=True)
    os.makedirs(TEST_UPLOAD_THUMBNAILS, exist_ok=True)

    yield

    for folder in (TEST_UPLOAD_PRODUCTS, TEST_UPLOAD_THUMBNAILS):
        for name in os.listdir(folder):
            path = os.path.join(folder, name)
            if os.path.isfile(path):
                os.remove(path)


@pytest.fixture(scope="session", autouse=True)
def cleanup_session_artifacts():
    yield
    shutil.rmtree(TEST_ROOT, ignore_errors=True)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def make_user(app):
    def _make_user(*, email, role=ROLE_BUYER, name="User", password="password123", is_active=True):
        user = User(
            name=name,
            email=email,
            password_hash=hash_password(password),
            role=role,
            is_active=is_active,
        )
        db.session.add(user)
        db.session.commit()
        return user

    with app.app_context():
        yield _make_user


@pytest.fixture
def make_category(app):
    def _make_category(name="Category", description=""):
        category = Category(name=name, description=description or None)
        db.session.add(category)
        db.session.commit()
        return category

    with app.app_context():
        yield _make_category


@pytest.fixture
def make_product(app):
    def _make_product(*, seller_id, category_id, name="Product", price="10.00", stock=5, sku=None):
        product = Product(
            seller_id=seller_id,
            category_id=category_id,
            name=name,
            description="Demo",
            price=Decimal(str(price)),
            stock=stock,
            sku=sku,
        )
        db.session.add(product)
        db.session.commit()
        return product

    with app.app_context():
        yield _make_product


@pytest.fixture
def make_auth_header(app):
    def _make_auth_header(user_or_id, role_code=None):
        user_id = user_or_id
        if hasattr(user_or_id, "id"):
            # Detached SQLAlchemy objects may raise when touching unloaded attrs.
            user_id = user_or_id.__dict__.get("id")
        if user_id is None:
            raise ValueError("Could not resolve user id for JWT fixture")

        with app.app_context():
            token = create_access_token(
                identity=str(user_id),
                additional_claims={"role_code": role_code or ROLE_BUYER},
            )
        return {"Authorization": f"Bearer {token}"}

    return _make_auth_header
