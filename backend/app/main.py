from fastapi import FastAPI, Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.auth import router as auth_router, get_current_user

app = FastAPI(title="LeaderAI")

# Mount static files
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Templates
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

# Include Auth Router
app.include_router(auth_router)

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
    return templates.TemplateResponse("index.html", {"request": request, "title": "LeaderAI", "user": user})
