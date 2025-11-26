from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from pathlib import Path

from app.database import get_db
from app.models import Employee, ProjectAssignment
from app.auth import get_current_user

router = APIRouter(prefix="/employees", tags=["employees"])
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")

@router.get("/", response_class=HTMLResponse)
async def list_employees(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_current_user)
):
    result = await db.execute(
        select(Employee)
        .options(selectinload(Employee.assignments).selectinload(ProjectAssignment.project))
        .options(selectinload(Employee.goals))
        .order_by(Employee.name)
    )
    employees = result.scalars().all()
    return templates.TemplateResponse(
        request=request,
        name="employees/list.html",
        context={
            "employees": employees,
            "user": user
        }
    )

@router.get("/new", response_class=HTMLResponse)
async def new_employee_form(
    request: Request, 
    user: str = Depends(get_current_user)
):
    return templates.TemplateResponse(request=request, name="employees/form.html", context={"user": user})

@router.post("/", response_class=HTMLResponse)
async def create_employee(
    request: Request,
    name: str = Form(...),
    role: str = Form(...),
    email: str = Form(...),
    skills: str = Form(""), # Comma separated
    notes: str = Form(None),
    development_plan: str = Form(None),
    potential: str = Form(None),
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_current_user)
):
    # Parse skills
    skill_list = [s.strip() for s in skills.split(",") if s.strip()]
    
    # Parse initial note
    notes_list = []
    if notes and notes.strip():
        notes_list.append(notes.strip())
    
    new_employee = Employee(
        name=name,
        role=role,
        email=email,
        skills=skill_list,
        notes=notes_list,
        development_plan=development_plan,
        potential=potential
    )
    
    try:
        db.add(new_employee)
        await db.commit()
        return RedirectResponse(url="/employees", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        # Ideally handle duplicate email error specifically
        return templates.TemplateResponse(
            request=request,
            name="employees/form.html",
            context={
                "error": f"Error creating employee: {str(e)}",
                "user": user
            }
        )

@router.get("/{employee_id}", response_class=HTMLResponse)
async def employee_detail(
    request: Request,
    employee_id: int,
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_current_user)
):
    result = await db.execute(
        select(Employee)
        .options(selectinload(Employee.assignments).selectinload(ProjectAssignment.project))
        .options(selectinload(Employee.goals))
        .filter(Employee.id == employee_id)
    )
    employee = result.scalar_one_or_none()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
        
    return templates.TemplateResponse(
        request=request,
        name="employees/detail.html",
        context={
            "employee": employee,
            "user": user
        }
    )

@router.get("/{employee_id}/edit", response_class=HTMLResponse)
async def edit_employee_form(
    request: Request,
    employee_id: int,
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_current_user)
):
    result = await db.execute(select(Employee).filter(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
        
    return templates.TemplateResponse(
        request=request, 
        name="employees/edit.html", 
        context={"employee": employee, "user": user}
    )

@router.post("/{employee_id}/edit", response_class=HTMLResponse)
async def update_employee(
    request: Request,
    employee_id: int,
    name: str = Form(...),
    role: str = Form(...),
    email: str = Form(...),
    skills: str = Form(""),
    potential: str = Form(None),
    development_plan: str = Form(None),
    new_note: str = Form(None),
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_current_user)
):
    result = await db.execute(select(Employee).filter(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
        
    employee.name = name
    employee.role = role
    employee.email = email
    employee.skills = [s.strip() for s in skills.split(",") if s.strip()]
    employee.potential = potential
    employee.development_plan = development_plan
    
    if new_note and new_note.strip():
        # Append to existing notes list
        # Ensure we are working with a list
        current_notes = list(employee.notes) if employee.notes else []
        current_notes.append(new_note.strip())
        employee.notes = current_notes
        
    await db.commit()
    return RedirectResponse(url=f"/employees/{employee_id}", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/{employee_id}/delete")
async def delete_employee(
    employee_id: int,
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_current_user)
):
    await db.execute(delete(Employee).where(Employee.id == employee_id))
    await db.commit()
    return RedirectResponse(url="/employees", status_code=status.HTTP_303_SEE_OTHER)
