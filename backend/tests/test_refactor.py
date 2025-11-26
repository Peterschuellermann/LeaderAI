import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from app.main import app
from app.config import settings
from app.models import Employee, Goal

client = TestClient(app)

def login(client):
    client.post(
        "/login",
        data={"username": settings.ADMIN_USERNAME, "password": settings.ADMIN_PASSWORD},
    )

@pytest.mark.asyncio
async def test_edit_employee_flow(db_session, override_get_db):
    login(client)
    
    # 1. Create Employee
    client.post(
        "/employees/",
        data={
            "name": "Refactor User",
            "role": "Dev",
            "email": "refactor@test.com",
            "notes": "Initial Note"
        }
    )
    
    result = await db_session.execute(select(Employee).filter_by(email="refactor@test.com"))
    emp = result.scalar_one()
    
    # 2. GET Edit Page
    response = client.get(f"/employees/{emp.id}/edit")
    assert response.status_code == 200
    assert "Refactor User" in response.text
    assert "Initial Note" in response.text
    
    # 3. POST Update with new note
    response = client.post(
        f"/employees/{emp.id}/edit",
        data={
            "name": "Refactor User Updated",
            "role": "Senior Dev",
            "email": "refactor@test.com",
            "skills": "Python, SQL",
            "potential": "P2",
            "new_note": "Second Note"
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    
    # 4. Check Detail Page
    db_session.expunge_all() # clear session
    response = client.get(f"/employees/{emp.id}")
    assert "Refactor User Updated" in response.text
    assert "Senior Dev" in response.text
    assert "Initial Note" in response.text
    assert "Second Note" in response.text
    assert "P2" in response.text # Check potential

@pytest.mark.asyncio
async def test_goal_detail_view(db_session, override_get_db):
    login(client)
    
    # 1. Create Employee
    client.post(
        "/employees/",
        data={
            "name": "Goal User",
            "role": "Dev",
            "email": "goal@test.com",
        }
    )
    result = await db_session.execute(select(Employee).filter_by(email="goal@test.com"))
    emp = result.scalar_one()

    # 2. Create Goal
    client.post(
        "/goals/",
        data={
            "title": "Detail Goal",
            "description": "Testing Goal Detail",
            "employee_id": emp.id,
            "status": "In Progress"
        }
    )
    
    result = await db_session.execute(select(Goal).filter_by(title="Detail Goal"))
    goal = result.scalar_one()
    
    # 3. GET Goal Detail
    response = client.get(f"/goals/{goal.id}")
    assert response.status_code == 200
    assert "Detail Goal" in response.text
    assert "Testing Goal Detail" in response.text
    assert "Pending" in response.text # Default status
    assert "Goal User" in response.text
