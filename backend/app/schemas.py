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

