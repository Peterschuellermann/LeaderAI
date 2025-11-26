from fastapi import FastAPI, Request, Depends, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import aiofiles
from sqlalchemy import select
from contextlib import asynccontextmanager

from app.auth import router as auth_router, get_current_user
from app.routers import employees, projects, goals
from app.config import settings
from app.database import SessionLocal, engine, Base
from app.models import Employee

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    if settings.ENVIRONMENT != "production":
        async with SessionLocal() as session:
            result = await session.execute(select(Employee).filter_by(email="test@example.com"))
            existing_user = result.scalar_one_or_none()
            
            if not existing_user:
                test_user = Employee(
                    name="Test User",
                    role="Tester",
                    email="test@example.com",
                    skills=["Manual Testing", "Bug Hunting"],
                    notes="Created automatically for development/testing."
                )
                session.add(test_user)
                await session.commit()
                print("Seeded test user: test@example.com")
    
    yield
    # Shutdown (if needed)

app = FastAPI(title="LeaderAI", lifespan=lifespan)

# Mount static files
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Templates
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

# Include Routers
app.include_router(auth_router)
app.include_router(employees.router)
app.include_router(projects.router)
app.include_router(goals.router)

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    # Allow public paths
    public_paths = ["/login", "/static", "/docs", "/openapi.json"]
    if any(request.url.path.startswith(path) for path in public_paths):
        return await call_next(request)
    
    # Check for session cookie
    user = request.cookies.get("session_user")
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    response = await call_next(request)
    return response

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, user: str = Depends(get_current_user)):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"title": "LeaderAI", "user": user}
    )

@app.get("/feedback", response_class=HTMLResponse)
async def feedback_form(request: Request, user: str = Depends(get_current_user)):
    return templates.TemplateResponse(request=request, name="feedback.html", context={"user": user})

@app.post("/feedback", response_class=HTMLResponse)
async def submit_feedback(
    request: Request, 
    feedback: str = Form(...),
    user: str = Depends(get_current_user)
):
    # Simple file append logging for MVP
    async with aiofiles.open("feedback.log", mode="a") as f:
        await f.write(f"User: {user} | Feedback: {feedback}\n")
    
    return templates.TemplateResponse(
        request=request,
        name="feedback.html",
        context={
            "user": user,
            "message": "Thank you for your feedback!",
        },
    )
