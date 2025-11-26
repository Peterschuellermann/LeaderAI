# LeaderAI - Team Leadership Assistant

LeaderAI is a lightweight, self-hostable application designed to streamline a team lead's day-to-day tasks. It helps manage team members, projects, and goals, leveraging AI to provide actionable insights.

## 🚀 Quick Start (Local)

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

## 🛠 Configuration

Create a `.env` file in the `backend/` directory (or use environment variables in Docker):

```env
SECRET_KEY=your_secure_secret
DATABASE_URL=sqlite+aiosqlite:///./leaderai.db
ADMIN_USERNAME=admin
ADMIN_PASSWORD=secure_password
OPENAI_API_KEY=sk-... (Optional: If missing, uses Mock AI)
```

## 📚 Documentation

*   [Features](docs/FEATURES.md)
*   [Build & Deploy](docs/BUILD.md)
*   [Project Goals](docs/GOALS.md)
*   [User Acceptance Testing](docs/UAT.md)

## 🧪 Development

*   **Run Tests**: `make test`
*   **Linting**: `make lint`
*   **Backup Data**: `make backup`
