from fastapi import APIRouter, Depends, status, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pathlib import Path
from typing import Optional, Dict
import uuid

from app.database import get_db
from app.models import Goal, Employee, Project
from app.auth import get_current_user
from app.services.llm import get_llm_service

router = APIRouter(prefix="/goals", tags=["goals"])
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")

# In-memory task store (Note: Not suitable for multi-worker production, use Redis instead)
tasks: Dict[str, dict] = {}

@router.get("/", response_class=HTMLResponse)
async def list_goals(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_current_user)
):
    result = await db.execute(select(Goal).order_by(Goal.status))
    goals = result.scalars().all()
    
    emp_result = await db.execute(select(Employee))
    employees = emp_result.scalars().all()

    return templates.TemplateResponse("goals/list.html", {
        "request": request, 
        "goals": goals,
        "employees": employees,
        "user": user
    })

@router.post("/", response_class=HTMLResponse)
async def create_goal(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    employee_id: int = Form(...),
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_current_user)
):
    goal = Goal(
        title=title,
        description=description,
        employee_id=employee_id,
        status="Pending"
    )
    db.add(goal)
    await db.commit()
    return RedirectResponse(url="/goals", status_code=status.HTTP_303_SEE_OTHER)

async def run_goal_generation_task(task_id: str, employee_id: int, project_id: int, db_session_factory):
    # We need a fresh session here if we were passing db, but we passed factory or just use IDs and get data.
    # Since we can't easily pass the async session across background task boundary without careful management,
    # let's assume we just need the input strings. 
    # BUT, we need to fetch data from DB to give to LLM.
    
    # For simplicity in MVP, I'll gather data in the endpoint and pass strings to this task.
    pass

async def process_ai_request(task_id: str, employee_context: str, project_context: str):
    llm = get_llm_service()
    result = await llm.generate_goals(employee_context, project_context)
    tasks[task_id] = {"status": "completed", "result": result}

@router.post("/generate_suggestions")
async def generate_suggestions(
    request: Request,
    background_tasks: BackgroundTasks,
    employee_id: int = Form(...),
    project_id: Optional[int] = Form(None),
    db: AsyncSession = Depends(get_db),
    user: str = Depends(get_current_user)
):
    # Fetch Context
    emp_result = await db.execute(select(Employee).filter(Employee.id == employee_id))
    employee = emp_result.scalar_one_or_none()
    
    if not employee:
        return "Employee not found"
        
    emp_context = f"Name: {employee.name}, Role: {employee.role}, Skills: {employee.skills}, Notes: {employee.notes}"
    proj_context = "General Improvement"
    
    if project_id:
        proj_result = await db.execute(select(Project).filter(Project.id == project_id))
        project = proj_result.scalar_one_or_none()
        if project:
            proj_context = f"Project: {project.name}, Description: {project.description}"

    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "pending"}
    
    background_tasks.add_task(process_ai_request, task_id, emp_context, proj_context)
    
    return templates.TemplateResponse("goals/task_poll.html", {
        "request": request, 
        "task_id": task_id
    })

@router.get("/task/{task_id}", response_class=HTMLResponse)
async def get_task_status(request: Request, task_id: str):
    task = tasks.get(task_id)
    if not task:
        return "Task not found"
    
    if task["status"] == "pending":
        return templates.TemplateResponse("goals/task_poll.html", {
            "request": request, 
            "task_id": task_id
        })
    
    # Completed
    return templates.TemplateResponse("goals/suggestion_result.html", {
        "request": request, 
        "result": task["result"]
    })

