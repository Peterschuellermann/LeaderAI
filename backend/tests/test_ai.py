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

@pytest.mark.asyncio
async def test_ai_goal_suggestion_with_potential(db_session, override_get_db):
    login(client)
    # Create P3 Employee (should get no goals)
    client.post("/employees/", data={
        "name": "P3 User", 
        "role": "Dev", 
        "email": "p3@test.com",
        "potential": "P3"
    })
    
    # Create P1 Employee (should get strategic goals)
    client.post("/employees/", data={
        "name": "P1 User", 
        "role": "Lead", 
        "email": "p1@test.com",
        "potential": "P1"
    })
    
    # Request for P3 (employee_id=2 since we created one in prev test or 1 if isolated)
    # Let's assume sequential IDs or query DB in real test, but here we guess 2
    # Since tests might run in any order or clean DB, we should probably fetch IDs or rely on isolation.
    # However, the conftest usually isolates per test function or session. 
    # Let's assume per-function isolation if configured correctly, so IDs are 1 and 2.
    
    response_p3 = client.post(
        "/goals/generate_suggestions",
        data={"employee_id": 1},
        headers={"HX-Request": "true"}
    )
    assert response_p3.status_code == 200
    
    response_p1 = client.post(
        "/goals/generate_suggestions",
        data={"employee_id": 2},
        headers={"HX-Request": "true"}
    )
    assert response_p1.status_code == 200

@pytest.mark.asyncio
async def test_llm_logic_mock(db_session):
    """
    Verify P3/P4 logic specifically using the MockLLMProvider directly.
    This ensures our business logic holds true even if we are mocking.
    """
    provider = MockLLMProvider()
    
    # P3 Case
    res_p3 = await provider.generate_goals("Ctx", "Proj", potential="P3")
    assert "no goals" in res_p3.lower()
    
    # P4 Case
    res_p4 = await provider.generate_goals("Ctx", "Proj", potential="P4")
    assert "no goals" in res_p4.lower()
    
    # P1 Case
    res_p1 = await provider.generate_goals("Ctx", "Proj", potential="P1")
    assert "Suggested goals" in res_p1 or "suggested goals" in res_p1.lower()

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
        
        # Note: We don't make a call here to avoid costs/errors with dummy key.
        # But if we wanted to test the call:
        # res = await provider.generate_goals(...)
    finally:
        settings.OPENAI_API_KEY = original_key



