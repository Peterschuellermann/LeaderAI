# Features

## 👥 Team Management
*   **Employee Profiles**: Store details like Role, Skills, and contact info.
*   **Potential Rating**: Track employee potential (P1-P4) to identify high performers and those needing support.
*   **Skill Matrix**: Visualize team skills (via list view).
*   **Structured Notes Timeline**: Keep a chronological history of private notes on 1:1s and performance updates.
*   **Development Plans**: Create and track specific growth plans for each team member.

## 📂 Project Hub
*   **Project Tracking**: Manage projects with statuses (Active, On Hold, Completed).
*   **Stakeholders**: Keep track of who cares about what.
*   **Assignments & Capacity**: Assign team members to projects with specific roles and manage their capacity percentage to avoid burnout.
*   **Inline Editing**: Quickly update project status, description, and details directly from the project view.
*   **Dashboard**: Quick view of total projects and statuses.

## 🎯 Goals & AI Assistant
*   **Goal Setting**: Define objectives for employees linked to projects.
*   **Direct Goal Creation**: Easily set new goals directly from an employee's profile.
*   **Goal Details**: Track success metrics, manager support needed, and due dates.
*   **AI Goal Assistant**: 
    *   Automatically suggests relevant goals based on an employee's skills and current project context.
    *   Uses OpenAI (if configured) or a local Mock provider for testing.
*   **Background Processing**: AI tasks run in the background without freezing the UI.

## 🛡️ Security & DevOps
*   **Authentication**: Simple secure cookie-based login.
*   **Self-Hostable**: Dockerized for easy deployment anywhere.
*   **Data Safety**: Built-in backup scripts.
*   **Development Seed Data**: Automatically seeds a "Test User" employee when running in non-production environments.
