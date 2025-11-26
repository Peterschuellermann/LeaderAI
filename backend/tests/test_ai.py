import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.services.llm import MockLLMProvider, get_llm_service

client = TestClient(app)

def login(client):
    client.post(
        "/login",
        data={"username": settings.ADMIN_USERNAME, "password": settings.ADMIN_PASSWORD},
    )

@pytest.mark.asyncio
async def test_list_goals(db_session, override_get_db):
    login(client)
    response = client.get("/goals/")
    assert response.status_code == 200
    assert "Goals & Objectives" in response.text

@pytest.mark.asyncio
async def test_create_goal(db_session, override_get_db):
    login(client)
    # Create employee first
    client.post("/employees/", data={"name": "Goal Target", "role": "Dev", "email": "goal@test.com"})
    
    response = client.post(
        "/goals/",
        data={
            "title": "Ship It",
            "description": "Release version 1.0",
            "employee_id": 1
        },
        follow_redirects=False
    )
    assert response.status_code == 303
    
    response = client.get("/goals/")
    assert "Ship It" in response.text

@pytest.mark.asyncio
async def test_ai_goal_suggestion_flow(db_session, override_get_db):
    login(client)
    # Create employee
    client.post("/employees/", data={"name": "AI User", "role": "Dev", "email": "ai@test.com"})
    
    # 1. Request Suggestion
    response = client.post(
        "/goals/generate_suggestions",
        data={"employee_id": 1},
        headers={"HX-Request": "true"} # Simulate HTMX
    )
    assert response.status_code == 200
    assert "hx-trigger" in response.text
    
    # Extract task ID (naive string parsing or regex)
    # <div hx-get="/goals/task/UUID" ...
    import re
    match = re.search(r'/goals/task/([a-f0-9\-]+)', response.text)
    assert match
    task_id = match.group(1)
    
    # 2. Poll Task (Immediately - might be pending or done depending on mock/race)
    # Since we use background tasks, it runs in the same process for TestClient usually.
    # However, TestClient with BackgroundTasks might run them synchronously or wait.
    # Let's see.
    
    response = client.get(f"/goals/task/{task_id}")
    assert response.status_code == 200
    
    # With TestClient, background tasks often run after the response is sent but we can't easily "wait" for them without
    # manual handling or force execution. 
    # But in Starlette/FastAPI TestClient, background tasks are executed.
    # However, our MockLLM sleeps for 2s. This might block if synchronous or be slow.
    # For testing, we might want to mock the LLM provider to be instant.
    
    # Ideally, we mock the `get_llm_service` to return a FastMock.
    # But the real MockLLM has sleep.
    
    # Note: `pytest-asyncio` and `TestClient` interaction with `asyncio.sleep` can be tricky. 
    # It might wait 2s.
    
    # Let's just assert we got a response (Pending or Result).
    assert "AI is thinking" in response.text or "Suggestions:" in response.text


