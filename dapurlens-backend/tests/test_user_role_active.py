
from app.models import User
from app.schemas import UserOut, TokenOut


def test_user_role_default():
    role_column = User.__table__.columns["role"]

    assert role_column.default.arg == "PENGGUNA"
    assert role_column.server_default.arg == "PENGGUNA"
    assert role_column.nullable is False


def test_user_is_active_default():
    active_column = User.__table__.columns["is_active"]

    assert active_column.default.arg is True
    assert active_column.server_default.arg == "true"
    assert active_column.nullable is False


def test_user_out_contains_role_and_active():
    user = UserOut(
        id=1,
        email="test@example.com",
        name="Test User",
        role="PENGGUNA",
        is_active=True,
    )

    assert user.role == "PENGGUNA"
    assert user.is_active is True


def test_login_response_contains_role_and_active():
    response = TokenOut(
        access_token="test-token",
        token_type="bearer",
        user={
            "id": 1,
            "email": "test@example.com",
            "name": "Test User",
            "role": "PENGGUNA",
            "is_active": True,
        },
    )

    assert response.user.role == "PENGGUNA"
    assert response.user.is_active is True


def test_me_endpoint_returns_role_and_active():
    from fastapi.testclient import TestClient
    from app.main import app
    from app.auth import get_current_user

    fake_user = User(
        id=1,
        email="test@example.com",
        name="Test User",
        hashed_password="fake-hash",
        role="PENGGUNA",
        is_active=True,
    )

    app.dependency_overrides[get_current_user] = lambda: fake_user
    try:
        response = TestClient(app).get("/api/auth/me")
    finally:
        app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 200
    assert response.json()["role"] == "PENGGUNA"
    assert response.json()["is_active"] is True


def test_login_endpoint_returns_role_and_active(monkeypatch):
    from fastapi.testclient import TestClient
    from app.main import app
    from app.database import get_db
    import app.main as main_module

    fake_user = User(
        id=1,
        email="test@example.com",
        name="Test User",
        hashed_password="fake-hash",
        role="PENGGUNA",
        is_active=True,
    )

    class FakeQuery:
        def filter(self, *args):
            return self

        def first(self):
            return fake_user

    class FakeDB:
        def query(self, *args):
            return FakeQuery()

    monkeypatch.setattr(main_module, "verify_password", lambda *args: True)
    monkeypatch.setattr(main_module, "create_access_token", lambda **kwargs: "test-token")

    app.dependency_overrides[get_db] = lambda: FakeDB()
    try:
        response = TestClient(app).post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 200
    assert response.json()["user"]["role"] == "PENGGUNA"
    assert response.json()["user"]["is_active"] is True
