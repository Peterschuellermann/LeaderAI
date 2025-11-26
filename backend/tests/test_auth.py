from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_read_root_unauthenticated():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"

def test_login_page():
    response = client.get("/login")
    assert response.status_code == 200
    assert "Login to LeaderAI" in response.text

def test_login_success():
    response = client.post(
        "/login",
        data={"username": settings.ADMIN_USERNAME, "password": settings.ADMIN_PASSWORD},
        follow_redirects=False
    )
    assert response.status_code == 303
    assert response.headers["location"] == "/"
    assert "session_user" in response.cookies

def test_login_failure():
    response = client.post(
        "/login",
        data={"username": "wrong", "password": "wrong"},
    )
    assert response.status_code == 200
    assert "Invalid credentials" in response.text

def test_access_protected_route():
    # Login first
    client.post(
        "/login",
        data={"username": settings.ADMIN_USERNAME, "password": settings.ADMIN_PASSWORD},
    )
    
    # Access root
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to LeaderAI" in response.text

