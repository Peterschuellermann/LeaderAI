from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class EmployeeBase(BaseModel):
    name: str
    role: str
    email: EmailStr
    skills: List[str] = []
    development_plan: Optional[str] = None
    notes: Optional[str] = None
    potential: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class EmployeeOut(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class GoalBase(BaseModel):
    title: str
    description: str # Objective
    due_date: Optional[str] = None
    success_metrics: Optional[str] = None
    manager_support: Optional[str] = None
    status: str = "Pending"

class GoalCreate(GoalBase):
    employee_id: int
    project_id: Optional[int] = None

class GoalOut(GoalBase):
    id: int
    employee_id: Optional[int] = None
    project_id: Optional[int] = None
    ai_suggestions: Optional[str] = None

    class Config:
        from_attributes = True
