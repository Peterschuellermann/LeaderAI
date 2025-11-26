from typing import List, Optional, Any
from sqlalchemy import String, Text, JSON, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    role: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    skills: Mapped[List[str]] = mapped_column(JSON, default=list)
    development_plan: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[List[str]] = mapped_column(JSON, default=list)
    potential: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    assignments: Mapped[List["ProjectAssignment"]] = relationship(back_populates="employee")
    goals: Mapped[List["Goal"]] = relationship(back_populates="employee")

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    status: Mapped[str] = mapped_column(String, default="Active")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    stakeholders: Mapped[List[Any]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    assignments: Mapped[List["ProjectAssignment"]] = relationship(back_populates="project")
    goals: Mapped[List["Goal"]] = relationship(back_populates="project")

class ProjectAssignment(Base):
    __tablename__ = "project_assignments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    role: Mapped[str] = mapped_column(String)
    capacity: Mapped[int] = mapped_column(default=100)
    
    employee: Mapped["Employee"] = relationship(back_populates="assignments")
    project: Mapped["Project"] = relationship(back_populates="assignments")

class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="Pending")
    
    due_date: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    success_metrics: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    manager_support: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    employee_id: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    
    ai_suggestions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    employee: Mapped[Optional["Employee"]] = relationship(back_populates="goals")
    project: Mapped[Optional["Project"]] = relationship(back_populates="goals")
