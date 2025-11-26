from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from pathlib import Path
from typing import List, Optional

from app.database import get_db
from app.models import Project, Employee, ProjectAssignment
from app.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")

@router.get("/", response_class=HTMLResponse)
async def list_projects(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_current_user)
):
    result = await db.execute(select(Project).order_by(Project.name))
    projects = result.scalars().all()
    return templates.TemplateResponse("projects/list.html", {
        "request": request, 
        "projects": projects,
        "user": user
    })

@router.get("/new", response_class=HTMLResponse)
async def new_project_form(
    request: Request, 
    user: str = Depends(get_current_user)
):
    return templates.TemplateResponse("projects/form.html", {"request": request, "user": user})

@router.post("/", response_class=HTMLResponse)
async def create_project(
    request: Request,
    name: str = Form(...),
    project_status: str = Form(..., alias="status"),
    description: str = Form(None),
    stakeholders: str = Form(""), # Comma separated
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_current_user)
):
    stakeholder_list = [s.strip() for s in stakeholders.split(",") if s.strip()]
    
    new_project = Project(
        name=name,
        status=project_status,
        description=description,
        stakeholders=stakeholder_list
    )
    
    db.add(new_project)
    await db.commit()
    return RedirectResponse(url="/projects", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/{project_id}", response_class=HTMLResponse)
async def project_detail(
    request: Request,
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_current_user)
):
    # Load project with assignments and employees
    result = await db.execute(
        select(Project)
        .options(selectinload(Project.assignments).selectinload(ProjectAssignment.employee))
        .filter(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get all employees for assignment dropdown
    emp_result = await db.execute(select(Employee))
    all_employees = emp_result.scalars().all()

    return templates.TemplateResponse("projects/detail.html", {
        "request": request, 
        "project": project,
        "all_employees": all_employees,
        "user": user
    })

@router.post("/{project_id}/assign")
async def assign_employee(
    project_id: int,
    employee_id: int = Form(...),
    role: str = Form(...),
    capacity: int = Form(100),
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_current_user)
):
    assignment = ProjectAssignment(
        project_id=project_id,
        employee_id=employee_id,
        role=role,
        capacity=capacity
    )
    db.add(assignment)
    await db.commit()
    return RedirectResponse(url=f"/projects/{project_id}", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/{project_id}/delete")
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_current_user)
):
    await db.execute(delete(Project).where(Project.id == project_id))
    await db.commit()
    return RedirectResponse(url="/projects", status_code=status.HTTP_303_SEE_OTHER)

