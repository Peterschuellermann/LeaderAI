# Project Goals

## Vision
To provide a lightweight, "zero-friction" tool for Engineering Managers and Team Leads to manage their "people and projects" data without the complexity of full-blown HRIS or Jira systems.

## Architectural Goals
1.  **Simplicity**: "Just works" deployment via Docker.
2.  **Performance**: Server-Side Rendering (SSR) + HTMX for instant interactions.
3.  **Privacy**: Self-hostable to keep sensitive employee data within the company network.
4.  **flexibility**: AI components are pluggable (OpenAI today, Local LLM tomorrow).

## Tech Stack Choices
*   **Python/FastAPI**: High performance, easy async (great for AI), strong typing.
*   **HTMX**: avoids the complexity of a separate React build pipeline; keeps the stack Python-centric.
*   **SQLite**: Zero-config database, sufficient for single-team usage. Easy to backup.
*   **TailwindCSS**: Utility-first styling for rapid UI development.

