from sqlalchemy import Column, Integer, String, Text, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String)
    email = Column(String, unique=True, index=True)
    skills = Column(JSON, default=list)  # List of strings
    development_plan = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    potential = Column(String, nullable=True) # P1, P2, P3, P4
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    assignments = relationship("ProjectAssignment", back_populates="employee")
    goals = relationship("Goal", back_populates="employee")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(String, default="Active") # Active, Completed, On Hold
    description = Column(Text, nullable=True)
    stakeholders = Column(JSON, default=list) # List of stakeholder names/details
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    assignments = relationship("ProjectAssignment", back_populates="project")
    goals = relationship("Goal", back_populates="project")

class ProjectAssignment(Base):
    __tablename__ = "project_assignments"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    role = Column(String) # Role in this specific project
    capacity = Column(Integer, default=100) # Percentage
    
    employee = relationship("Employee", back_populates="assignments")
    project = relationship("Project", back_populates="assignments")

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text) # Objective
    status = Column(String, default="Pending") # Pending, In Progress, Achieved
    
    due_date = Column(String, nullable=True)
    success_metrics = Column(Text, nullable=True)
    manager_support = Column(Text, nullable=True)
    
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    
    ai_suggestions = Column(Text, nullable=True) # AI Generated tips
    
    employee = relationship("Employee", back_populates="goals")
    project = relationship("Project", back_populates="goals")

