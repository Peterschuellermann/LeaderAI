from abc import ABC, abstractmethod
from typing import List
import asyncio
from app.config import settings
from openai import AsyncOpenAI

class LLMProvider(ABC):
    @abstractmethod
    async def generate_goals(self, employee_context: str, project_context: str) -> str:
        pass

    @abstractmethod
    async def analyze_skill_gap(self, team_skills: List[str], project_requirements: str) -> str:
        pass

class MockLLMProvider(LLMProvider):
    async def generate_goals(self, employee_context: str, project_context: str) -> str:
        await asyncio.sleep(2) # Simulate delay
        return f"""
        Based on {employee_context} and {project_context}, here are suggested goals:
        1. Improve Python type hinting proficiency.
        2. Lead the architecture review for the next sprint.
        3. Mentor junior developers on async patterns.
        """

    async def analyze_skill_gap(self, team_skills: List[str], project_requirements: str) -> str:
        await asyncio.sleep(2)
        return f"""
        Team skills: {', '.join(team_skills)}
        Project needs: {project_requirements}
        
        Gap Analysis:
        - Missing strong DevOps experience.
        - Need more React expertise.
        """

class OpenAIProvider(LLMProvider):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY if hasattr(settings, 'OPENAI_API_KEY') else "dummy")

    async def generate_goals(self, employee_context: str, project_context: str) -> str:
        if not hasattr(settings, 'OPENAI_API_KEY') or not settings.OPENAI_API_KEY:
             return "OpenAI API Key not configured."
             
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful engineering manager assistant."},
                {"role": "user", "content": f"Suggest 3 professional goals for an employee with this profile: {employee_context}. They are working on projects: {project_context}."}
            ]
        )
        return response.choices[0].message.content

    async def analyze_skill_gap(self, team_skills: List[str], project_requirements: str) -> str:
        if not hasattr(settings, 'OPENAI_API_KEY') or not settings.OPENAI_API_KEY:
             return "OpenAI API Key not configured."

        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful engineering manager assistant."},
                {"role": "user", "content": f"Compare these team skills: {', '.join(team_skills)} against these project requirements: {project_requirements}. Identify gaps."}
            ]
        )
        return response.choices[0].message.content

def get_llm_service() -> LLMProvider:
    # For now, default to Mock if no API key is present or if configured to use Mock
    # In a real app, check config.
    if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "dummy":
        return OpenAIProvider()
    return MockLLMProvider()

