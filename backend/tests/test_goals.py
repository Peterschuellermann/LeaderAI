import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from app.main import app
from app.config import settings
from app.models import Employee

client = TestClient(app)

# Helper to authenticate
def login(client):
    client.post(
        "/login",
        data={"username": settings.ADMIN_USERNAME, "password": settings.ADMIN_PASSWORD},
    )

@pytest.mark.asyncio
async def test_goals_prefilled_employee(db_session, override_get_db):
    login(client)
    
    # Create a test employee
    client.post(
        "/employees/",
        data={
            "name": "Goal Target",
            "role": "Target Role",
            "email": "target@test.com",
            "skills": "Testing",
            "notes": "Notes"
        }
    )
    
    # Get ID
    result = await db_session.execute(select(Employee).filter_by(email="target@test.com"))
    emp = result.scalar_one()
    
    # GET /goals with employee_id
    response = client.get(f"/goals?employee_id={emp.id}")
    assert response.status_code == 200
    
    # Check if option is selected
    # We look for value="{emp.id}" ... selected
    # HTML might be slightly different so we check for the string
    expected_selected = f'value="{emp.id}" selected'
    # or just check if 'selected' attribute is present on the correct option
    # Given the template change: <option value="{{ emp.id }}" {% if ... %}selected{% endif %}>
    # It should render as <option value="X" selected>
    
    assert expected_selected in response.text
