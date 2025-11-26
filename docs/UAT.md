# User Acceptance Testing (UAT) Script

Use this script to validate the application meets your needs.

## Scenario 1: Onboarding & Team Setup
1.  **Login**: Navigate to `/login`. Enter `admin` / `password` (or your config).
    *   *Pass*: Redirected to Dashboard.
2.  **Add Employee**: Go to "Team" -> "Add Employee".
    *   Name: "Jane Doe"
    *   Role: "Senior Engineer"
    *   Skills: "Python, Docker, Leadership"
    *   *Pass*: Employee appears in the list.
3.  **View Detail**: Click on "Jane Doe".
    *   *Pass*: See details and empty notes section.

## Scenario 2: Managing Work
1.  **Create Project**: Go to "Projects" -> "Create Project".
    *   Name: "Migration 2.0"
    *   Status: "Active"
    *   Stakeholders: "CTO"
    *   *Pass*: Project appears in list.
2.  **Assign Team**: Click "Migration 2.0". Scroll to "Assignments".
    *   Select "Jane Doe", Role "Lead", Capacity "50%".
    *   Click "Assign".
    *   *Pass*: Jane Doe appears in the assignment list.

## Scenario 3: AI Goal Setting
1.  **Navigate**: Go to "Goals".
2.  **AI Assistant**: Look for the "AI Goal Assistant" box.
    *   Select "Jane Doe".
    *   Click "Ask AI for Suggestions".
    *   *Pass*: "AI is thinking..." appears. After ~2-5 seconds, text suggestions appear.
3.  **Create Goal**: Copy a suggestion.
    *   Fill in the "Set New Goal" form with the suggestion.
    *   Click "Save Goal".
    *   *Pass*: Goal appears in "Active Goals" list.

## Scenario 4: Data Safety
1.  **Backup**: Run `./scripts/backup.sh` in your terminal.
    *   *Pass*: A `.db` file is created in `backups/`.


