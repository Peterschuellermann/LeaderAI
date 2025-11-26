import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def login(client):
    client.post(
        "/login",
        data={"username": settings.ADMIN_USERNAME, "password": settings.ADMIN_PASSWORD},
    )

@pytest.mark.asyncio
async def test_list_projects(db_session, override_get_db):
    login(client)
    response = client.get("/projects/")
    assert response.status_code == 200
    assert "Projects" in response.text

@pytest.mark.asyncio
async def test_create_project(db_session, override_get_db):
    login(client)
    response = client.post(
        "/projects/",
        data={
            "name": "Alpha Protocol",
            "status": "Active",
            "description": "Top Secret",
            "stakeholders": "Director, Board",
        },
        follow_redirects=False
    )
    assert response.status_code == 303
    
    response = client.get("/projects/")
    assert "Alpha Protocol" in response.text

@pytest.mark.asyncio
async def test_assign_employee(db_session, override_get_db):
    login(client)
    
    # Setup: Create Employee and Project
    # For integration test without direct DB access in this function scope (unless we use a different fixture pattern),
    # we can just use the API to create them.
    
    client.post("/employees/", data={"name": "Agent 47", "role": "Specialist", "email": "47@ica.com"})
    client.post("/projects/", data={"name": "Target Acquisition", "status": "Active"})
    
    # Assuming IDs are 1 and 1 (dangerous in shared envs, but safe in isolated tests)
    # Let's do a listing to find IDs if we want to be safe, or just try 1.
    
    response = client.post(
        "/projects/1/assign",
        data={
            "employee_id": 1,
            "role": "Lead",
            "capacity": 100
        },
        follow_redirects=False
    )
    assert response.status_code == 303
    
    # Verify on detail page
    response = client.get("/projects/1")
    assert "Agent 47" in response.text
    assert "Lead (100%)" in response.text

