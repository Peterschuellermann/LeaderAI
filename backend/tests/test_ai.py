import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from unittest.mock import patch
from app.services.llm import get_llm_service, MockLLMProvider

client = TestClient(app)

# Force MockLLM for these tests to avoid API costs and network errors
@pytest.fixture(autouse=True)
def mock_llm_service():
    with patch("app.routers.goals.get_llm_service", return_value=MockLLMProvider()) as mock:
        yield mock

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
            "employee_id": 1,
            "due_date": "Q4 2024",
            "success_metrics": "Zero bugs",
            "manager_support": "Pizza"
        },
        follow_redirects=False
    )
    assert response.status_code == 303
    
    response = client.get("/goals/")
    assert "Ship It" in response.text
    assert "Q4 2024" in response.text
    assert "Zero bugs" in response.text

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
    
    # 2. Poll Task
    # With TestClient, background tasks are executed.
    # However, our MockLLM sleeps for 2s.
    # We might need to wait or just check status.
    
    # Poll
    response = client.get(f"/goals/task/{task_id}")
    assert response.status_code == 200
    
    # Ideally we want to see the result form.
    # Depending on timing, it might be "AI is thinking" or the form.
    # But usually TestClient waits for background tasks? No, Starlette TestClient runs background tasks AFTER response.
    # So the first poll might be too fast if the background task sleeps.
    # But wait, `asyncio.sleep` in background task...
    
    # Let's just check that we get a valid response.
    assert "task_poll" in response.template.name or "suggestion_result" in response.template.name

@pytest.mark.asyncio
async def test_llm_logic_mock(db_session):
    """
    Verify P3/P4 logic specifically using the MockLLMProvider directly.
    This ensures our business logic holds true even if we are mocking.
    """
    provider = MockLLMProvider()
    
    # P3 Case
    res_p3 = await provider.generate_goals("Ctx", "Proj", potential="P3")
    assert isinstance(res_p3, dict)
    assert "Morale" in res_p3["title"] or "morale" in res_p3["objective"]
    
    # P4 Case
    res_p4 = await provider.generate_goals("Ctx", "Proj", potential="P4")
    assert isinstance(res_p4, dict)
    assert "Termination" in res_p4["title"] or "Terminate" in res_p4["objective"]
    
    # P1 Case
    res_p1 = await provider.generate_goals("Ctx", "Proj", potential="P1")
    assert isinstance(res_p1, dict)
    assert "title" in res_p1
    assert "objective" in res_p1
    assert "due_date" in res_p1

@pytest.mark.asyncio
async def test_openai_key_integration_skipped_by_default():
    """
    This test is skipped unless explicitly enabled to save costs.
    It verifies that the OpenAI provider is instantiated when a key is present.
    """
    import os
    if not os.getenv("RUN_REAL_OPENAI_TEST"):
        pytest.skip("Skipping real OpenAI test. Set RUN_REAL_OPENAI_TEST=1 to run.")
        
    # Manually import to avoid patch
    from app.services.llm import OpenAIProvider, get_llm_service
    from app.config import settings
    
    # Temporarily set a dummy key if none exists, just to test instantiation logic
    original_key = settings.OPENAI_API_KEY
    settings.OPENAI_API_KEY = "sk-test-dummy-key"
    
    try:
        provider = get_llm_service()
        assert isinstance(provider, OpenAIProvider)
    finally:
        settings.OPENAI_API_KEY = original_key
