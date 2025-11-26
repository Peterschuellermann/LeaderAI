import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from app.main import app
from app.config import settings
from app.models import Project, Employee, ProjectAssignment

client = TestClient(app)

def login(client):
    client.post(
        "/login",
        data={"username": settings.ADMIN_USERNAME, "password": settings.ADMIN_PASSWORD},
    )

@pytest.mark.asyncio
async def test_update_project(db_session, override_get_db):
    login(client)
    
    # Create Project
    client.post(
        "/projects/",
        data={
            "name": "Project X",
            "status": "Active",
            "description": "Initial Description",
            "stakeholders": "CEO",
        },
        follow_redirects=True
    )
    
    # Get Project ID
    result = await db_session.execute(select(Project).filter_by(name="Project X"))
    project = result.scalar_one()
    
    # Update Project
    response = client.post(
        f"/projects/{project.id}/update",
        data={
            "name": "Project X Updated",
            "status": "On Hold",
            "description": "Updated Description",
            "stakeholders": "CEO, CTO",
        },
        follow_redirects=False
    )
    assert response.status_code == 303
    
    # Refresh object in session to ensure fresh read in the app
    await db_session.refresh(project)
    
    # Verify Updates
    response = client.get(f"/projects/{project.id}")
    assert "Project X Updated" in response.text
    assert "On Hold" in response.text
    assert "Updated Description" in response.text
    assert "CEO, CTO" in response.text

@pytest.mark.asyncio
async def test_update_and_delete_assignment(db_session, override_get_db):
    login(client)
    
    # Setup: Create Employee and Project
    client.post("/employees/", data={"name": "Test Agent", "role": "Dev", "email": "test@agent.com"})
    client.post("/projects/", data={"name": "Project Y", "status": "Active"})
    
    # Get IDs
    emp_result = await db_session.execute(select(Employee).filter_by(email="test@agent.com"))
    emp = emp_result.scalar_one()
    
    proj_result = await db_session.execute(select(Project).filter_by(name="Project Y"))
    proj = proj_result.scalar_one()
    
    client.post(
        f"/projects/{proj.id}/assign",
        data={
            "employee_id": emp.id,
            "role": "Developer",
            "capacity": 50
        },
        follow_redirects=True
    )
    
    # Refresh project assignments
    await db_session.refresh(proj, attribute_names=["assignments"])
    
    # Verify Assignment
    response = client.get(f"/projects/{proj.id}")
    assert "Developer (50%)" in response.text
    
    # Get Assignment ID
    assign_result = await db_session.execute(select(ProjectAssignment).filter_by(project_id=proj.id, employee_id=emp.id))
    assignment = assign_result.scalar_one()
    
    # Update Assignment
    response = client.post(
        f"/projects/{proj.id}/assignments/{assignment.id}/update",
        data={
            "role": "Senior Developer",
            "capacity": 80
        },
        follow_redirects=False
    )
    assert response.status_code == 303
    
    # Refresh assignment
    await db_session.refresh(assignment)
    # Also refresh project assignments to be safe
    await db_session.refresh(proj, attribute_names=["assignments"])
    
    response = client.get(f"/projects/{proj.id}")
    assert "Senior Developer (80%)" in response.text
    
    # Delete Assignment
    response = client.post(
        f"/projects/{proj.id}/assignments/{assignment.id}/delete",
        follow_redirects=False
    )
    assert response.status_code == 303
    
    # Refresh project assignments to reflect deletion
    await db_session.refresh(proj, attribute_names=["assignments"])
    
    response = client.get(f"/projects/{proj.id}")
    assert "Senior Developer" not in response.text
    assert "No one assigned yet" in response.text
