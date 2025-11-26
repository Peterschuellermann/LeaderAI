# User Acceptance Testing (UAT) Script

Use this script to validate the application meets your needs.

## Scenario 1: Onboarding & Team Setup
1.  **Login**: Navigate to `/login`. Enter `admin` / `password` (or your config).
    *   *Pass*: Redirected to Dashboard.
2.  **Add Employee**: Go to "Team" -> "Add Employee".
    *   Name: "Jane Doe"
    *   Role: "Senior Engineer"
    *   Skills: "Python, Docker, Leadership"
    *   Potential: Select "P1 - High Potential / Strategic"
    *   *Pass*: Employee appears in the list.
3.  **View Detail**: Click on "Jane Doe".
    *   *Pass*: See details, including the "P1" Potential rating.
4.  **Edit Employee**: Click "Edit Profile".
    *   Add a note: "Initial onboarding complete."
    *   Click "Update Employee".
    *   *Pass*: Redirected to Detail view, note appears in timeline.

## Scenario 2: Managing Work
1.  **Create Project**: Go to "Projects" -> "Create Project".
    *   Name: "Migration 2.0"
    *   Status: "Active"
    *   Stakeholders: "CTO"
    *   *Pass*: Project appears in list.
2.  **Assign Team**: Click "Migration 2.0". Scroll to "Assignments".
    *   Select "Jane Doe", Role "Lead", Capacity "50".
    *   Click "Assign".
    *   *Pass*: Jane Doe appears in the assignment list with 50% capacity.
3.  **Inline Edit**: In the Project Detail view, click on the status (e.g., "Active").
    *   Change it to "On Hold" and click "Update".
    *   *Pass*: Status updates immediately without a full page reload (if configured) or updates on refresh.

## Scenario 3: AI & Goal Setting
1.  **AI Assistant**: Go to "Goals". Look for the "AI Goal Assistant" box.
    *   Select "Jane Doe".
    *   Click "Ask AI for Suggestions".
    *   *Pass*: "AI is thinking..." appears. After ~2-5 seconds, text suggestions appear.
2.  **Direct Goal Creation**: Go to "Team", click "Jane Doe".
    *   Click the "Set New Goal" button.
    *   *Pass*: Redirected to Goal form with Jane Doe pre-selected.
3.  **Create Goal**:
    *   Title: "Lead Migration"
    *   Success Metrics: "Zero downtime"
    *   Click "Save Goal".
    *   *Pass*: Goal appears in "Active Goals" list and on Jane's profile.

## Scenario 4: Data Safety
1.  **Backup**: Run `./scripts/backup.sh` in your terminal.
    *   *Pass*: A `.db` file is created in `backups/`.
