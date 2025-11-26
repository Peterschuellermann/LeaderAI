from abc import ABC, abstractmethod
from typing import List, Optional
import asyncio
from app.config import settings
from openai import AsyncOpenAI

class LLMProvider(ABC):
    @abstractmethod
    async def generate_goals(self, employee_context: str, project_context: str, potential: str = None, criteria: str = None) -> str:
        pass

    @abstractmethod
    async def analyze_skill_gap(self, team_skills: List[str], project_requirements: str) -> str:
        pass

class MockLLMProvider(LLMProvider):
    async def generate_goals(self, employee_context: str, project_context: str, potential: str = None, criteria: str = None) -> str:
        await asyncio.sleep(2) # Simulate delay
        
        if potential in ["P3", "P4"]:
             return f"Based on potential rating {potential}, no goals are recommended at this time."

        return f"""
        Based on {employee_context} and {project_context} (Potential: {potential}), here are suggested goals:
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

    async def generate_goals(self, employee_context: str, project_context: str, potential: str = None, criteria: str = None) -> str:
        if not hasattr(settings, 'OPENAI_API_KEY') or not settings.OPENAI_API_KEY:
             return "OpenAI API Key not configured."
        
        # Potential Logic
        if potential == "P3":
            return "Employee is rated P3 (Good at job, no desire for more). No new goals recommended."
        if potential == "P4":
            return "Employee is rated P4 (Underperformance). No development goals recommended."
            
        system_prompt = "You are a helpful engineering manager assistant."
        user_prompt = f"Context: {employee_context}. Project: {project_context}. "
        
        if potential == "P1":
            user_prompt += "The employee is rated P1 (High Potential). Suggest strategic and long-term development goals that help them achieve major milestones or promotion."
        elif potential == "P2":
             user_prompt += "The employee is rated P2 (Potential but needs skills). Suggest training and skill-acquisition goals to help them close the gap and perform their role effectively."
        
        if criteria:
            user_prompt += f" Additional Criteria: {criteria}."
            
        user_prompt += " Suggest 3 distinct goals."

        response = await self.client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content

    async def analyze_skill_gap(self, team_skills: List[str], project_requirements: str) -> str:
        if not hasattr(settings, 'OPENAI_API_KEY') or not settings.OPENAI_API_KEY:
             return "OpenAI API Key not configured."

        response = await self.client.chat.completions.create(
            model="gpt-5-mini",
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
