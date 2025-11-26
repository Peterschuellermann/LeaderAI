from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import asyncio
import json
from app.config import settings
from openai import AsyncOpenAI

class LLMProvider(ABC):
    @abstractmethod
    async def generate_goals(self, employee_context: str, project_context: str, potential: str = None, criteria: str = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def analyze_skill_gap(self, team_skills: List[str], project_requirements: str) -> str:
        pass

class MockLLMProvider(LLMProvider):
    async def generate_goals(self, employee_context: str, project_context: str, potential: str = None, criteria: str = None) -> Dict[str, Any]:
        await asyncio.sleep(2) # Simulate delay
        
        if potential in ["P3", "P4"]:
             return {
                 "title": "Maintenance Mode",
                 "objective": f"Employee is rated {potential}. Focus on maintaining current performance standards.",
                 "due_date": "Ongoing",
                 "success_metrics": "Maintain current KPI levels.",
                 "manager_support": "Regular check-ins."
             }

        return {
            "title": "Improve Python Proficiency",
            "objective": f"Enhance skills in Python based on {project_context}. Focus on async patterns.",
            "due_date": "Q1 2025",
            "success_metrics": "1. Complete advanced Python course.\n2. Refactor 3 legacy modules.",
            "manager_support": "Code reviews and pair programming sessions."
        }

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

    async def generate_goals(self, employee_context: str, project_context: str, potential: str = None, criteria: str = None) -> Dict[str, Any]:
        if not hasattr(settings, 'OPENAI_API_KEY') or not settings.OPENAI_API_KEY:
             return {"error": "OpenAI API Key not configured."}
        
        # Potential Logic
        if potential == "P3":
            return {
                 "title": "Maintenance",
                 "objective": "Employee is rated P3 (Good at job, no desire for more). Maintain current high standards.",
                 "due_date": "Ongoing",
                 "success_metrics": "Consistent delivery.",
                 "manager_support": "Quarterly reviews."
             }
        if potential == "P4":
            return {
                 "title": "Performance Improvement",
                 "objective": "Employee is rated P4 (Underperformance). Address performance gaps.",
                 "due_date": "Immediate",
                 "success_metrics": "Meet PIP requirements.",
                 "manager_support": "Weekly coaching."
             }
            
        system_prompt = "You are a helpful engineering manager assistant. Output ONLY valid JSON."
        user_prompt = f"Context: {employee_context}. Project: {project_context}. "
        
        if potential == "P1":
            user_prompt += "The employee is rated P1 (High Potential). Suggest a strategic development goal."
        elif potential == "P2":
             user_prompt += "The employee is rated P2 (Potential but needs skills). Suggest a skill-acquisition goal."
        
        if criteria:
            user_prompt += f" Additional Criteria: {criteria}."
            
        user_prompt += """
        Suggest ONE single goal.
        Return a JSON object with these keys:
        - title
        - objective
        - due_date
        - success_metrics
        - manager_support
        """

        try:
            response = await self.client.chat.completions.create(
                model="gpt-5-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            return {
                "title": "Error Generating Goal",
                "objective": f"Failed to generate goal: {str(e)}",
                "due_date": "",
                "success_metrics": "",
                "manager_support": ""
            }

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
