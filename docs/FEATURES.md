# Features

## 👥 Team Management
*   **Employee Profiles**: Store details like Role, Skills, Notes, and Development Plans.
*   **Skill Matrix**: Visualize team skills (via list view).
*   **Notes**: Keep private notes on 1:1s and performance.

## 📂 Project Hub
*   **Project Tracking**: Manage projects with statuses (Active, On Hold, Completed).
*   **Stakeholders**: Keep track of who cares about what.
*   **Assignments**: Assign team members to projects with specific roles and capacity percentages.
*   **Dashboard**: Quick view of total projects and statuses.

## 🎯 Goals & AI Assistant
*   **Goal Setting**: Define objectives for employees linked to projects.
*   **AI Goal Assistant**: 
    *   Automatically suggests relevant goals based on an employee's skills and current project context.
    *   Uses OpenAI (if configured) or a local Mock provider for testing.
*   **Background Processing**: AI tasks run in the background without freezing the UI.

## 🛡️ Security & DevOps
*   **Authentication**: Simple secure cookie-based login.
*   **Self-Hostable**: Dockerized for easy deployment anywhere.
*   **Data Safety**: Built-in backup scripts.
*   **Development Seed Data**: Automatically seeds a "Test User" employee when running in non-production environments.
