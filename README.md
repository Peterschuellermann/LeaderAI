# LeaderAI - Team Leadership Assistant

LeaderAI is a lightweight, self-hostable application designed to streamline a team lead's day-to-day tasks. It helps manage team members, projects, and goals, leveraging AI to provide actionable insights.

## 🚀 Quick Start (Docker)

The easiest way to run the application is using Docker Compose.

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/leaderai.git
    cd leaderai
    ```

2.  **Run with Docker Compose**:
    ```bash
    make run
    # OR
    docker-compose up --build
    ```

3.  **Access the App**:
    Open [http://localhost:8000](http://localhost:8000) in your browser.
    
    *   **Default Admin Credentials**:
        *   Username: `admin`
        *   Password: `password`
        *   *(Configure these in `.env` for production)*

## 🛠 Local Development (No Docker)

If you want to develop locally without Docker:

1.  **Create a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r backend/requirements.txt
    ```

3.  **Run the Server**:
    ```bash
    cd backend
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

4.  **Manage Server Processes**:
    
    If you encounter "address already in use" errors, use the following commands to manage running servers:

    ```bash
    # List all running LeaderAI server processes
    make list

    # Stop all running LeaderAI server processes (ports 8000-8005)
    make stop

    # Restart the application (stop + run)
    make restart
    ```

## 📚 Documentation

*   [Features](docs/FEATURES.md)
*   [Build & Deploy](docs/BUILD.md)
*   [Project Goals](docs/GOALS.md)
*   [User Acceptance Testing](docs/UAT.md)

## 🧪 Testing

To run the test suite (ensure you are in your virtual environment or using Docker):

```bash
# Local (with venv activated)
cd backend && pytest

# OR using Make (if dependencies are installed)
make test

# Verify code quality (lint + test) - recommended before pushing
make ready
```

## 🛠 Configuration

Create a `.env` file in the `backend/` directory (or use environment variables in Docker):

```env
SECRET_KEY=your_secure_secret
DATABASE_URL=sqlite+aiosqlite:///./leaderai.db
ADMIN_USERNAME=admin
ADMIN_PASSWORD=secure_password
OPENAI_API_KEY=sk-... (Optional: If missing, uses Mock AI)
```
