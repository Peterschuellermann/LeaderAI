from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from pathlib import Path

from app.database import get_db
from app.models import Employee
from app.auth import get_current_user

router = APIRouter(prefix="/employees", tags=["employees"])
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")

@router.get("/", response_class=HTMLResponse)
async def list_employees(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_current_user)
):
    result = await db.execute(select(Employee).order_by(Employee.name))
    employees = result.scalars().all()
    return templates.TemplateResponse("employees/list.html", {
        "request": request, 
        "employees": employees,
        "user": user
    })

@router.get("/new", response_class=HTMLResponse)
async def new_employee_form(
    request: Request, 
    user: str = Depends(get_current_user)
):
    return templates.TemplateResponse("employees/form.html", {"request": request, "user": user})

@router.post("/", response_class=HTMLResponse)
async def create_employee(
    request: Request,
    name: str = Form(...),
    role: str = Form(...),
    email: str = Form(...),
    skills: str = Form(""), # Comma separated
    notes: str = Form(None),
    development_plan: str = Form(None),
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_current_user)
):
    # Parse skills
    skill_list = [s.strip() for s in skills.split(",") if s.strip()]
    
    new_employee = Employee(
        name=name,
        role=role,
        email=email,
        skills=skill_list,
        notes=notes,
        development_plan=development_plan
    )
    
    try:
        db.add(new_employee)
        await db.commit()
        return RedirectResponse(url="/employees", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        # Ideally handle duplicate email error specifically
        return templates.TemplateResponse("employees/form.html", {
            "request": request, 
            "error": f"Error creating employee: {str(e)}",
            "user": user
        })

@router.get("/{employee_id}", response_class=HTMLResponse)
async def employee_detail(
    request: Request,
    employee_id: int,
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_current_user)
):
    result = await db.execute(select(Employee).filter(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
        
    return templates.TemplateResponse("employees/detail.html", {
        "request": request, 
        "employee": employee,
        "user": user
    })

@router.post("/{employee_id}/delete")
async def delete_employee(
    employee_id: int,
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_current_user)
):
    await db.execute(delete(Employee).where(Employee.id == employee_id))
    await db.commit()
    return RedirectResponse(url="/employees", status_code=status.HTTP_303_SEE_OTHER)

