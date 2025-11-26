import pytest
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models import Employee, Project, ProjectAssignment, Goal

@pytest.mark.asyncio
async def test_create_employee(db_session):
    employee = Employee(
        name="John Doe",
        role="Developer",
        email="john@example.com",
        skills=["Python", "FastAPI"],
        notes="Great performance"
    )
    db_session.add(employee)
    await db_session.commit()

    result = await db_session.execute(select(Employee).filter_by(email="john@example.com"))
    saved_employee = result.scalar_one()
    
    assert saved_employee.name == "John Doe"
    assert saved_employee.skills == ["Python", "FastAPI"]

@pytest.mark.asyncio
async def test_project_assignment_relationship(db_session):
    # Create Employee
    emp = Employee(name="Alice", email="alice@test.com", role="Developer")
    db_session.add(emp)
    
    # Create Project
    proj = Project(name="Project X", status="Active")
    db_session.add(proj)
    await db_session.commit()
    
    # Assign
    assignment = ProjectAssignment(
        employee_id=emp.id,
        project_id=proj.id,
        role="Lead",
        capacity=50
    )
    db_session.add(assignment)
    await db_session.commit()
    
    # Verify relationships with eager loading
    stmt = select(Project).options(selectinload(Project.assignments)).filter_by(name="Project X")
    result = await db_session.execute(stmt)
    saved_proj = result.scalar_one()
    
    assert len(saved_proj.assignments) == 1
    assert saved_proj.assignments[0].role == "Lead"
    assert saved_proj.assignments[0].employee_id == emp.id

@pytest.mark.asyncio
async def test_goal_creation(db_session):
    emp = Employee(name="Bob", email="bob@test.com", role="Engineer")
    db_session.add(emp)
    await db_session.commit()
    
    goal = Goal(
        title="Learn Rust",
        description="Complete rustlings",
        employee_id=emp.id,
        status="Pending",
        due_date="Q4 2024",
        success_metrics="Complete 50 exercises",
        manager_support="Provide time"
    )
    db_session.add(goal)
    await db_session.commit()
    
    result = await db_session.execute(select(Goal).filter_by(title="Learn Rust"))
    saved_goal = result.scalar_one()
    
    assert saved_goal.employee_id == emp.id
    assert saved_goal.due_date == "Q4 2024"
    assert saved_goal.success_metrics == "Complete 50 exercises"
    assert saved_goal.manager_support == "Provide time"

