# Build & Deploy Guide

## Building the Docker Image

To build the image locally:

```bash
docker-compose build
```

## Deployment (Self-Hosting)

### Prerequisites
*   A server (VPS, Raspberry Pi, etc.) with **Docker** and **Docker Compose** installed.

### Steps

1.  **Copy Files**:
    Copy `docker-compose.yml` and the `backend/` folder to your server.
    *   *Better*: Clone the repo on the server.

2.  **Configure Environment**:
    Create a `.env` file next to `docker-compose.yml`:
    ```bash
    SECRET_KEY=change_this_to_something_random
    ADMIN_PASSWORD=MySuperSecurePassword
    OPENAI_API_KEY=sk-proj-...
    ```

3.  **Start the Service**:
    ```bash
    docker-compose up -d
    ```

4.  **Verify**:
    Check logs: `docker-compose logs -f`
    Visit `http://your-server-ip:8000`

### Data Persistence
*   The SQLite database is stored in `backend/leaderai.db`.
*   The `docker-compose.yml` maps the `backend` directory to the container, so the DB file persists on the host.
*   **Backup**: Run `./scripts/backup.sh` periodically (add to cron).

### CI/CD
*   GitHub Actions are configured in `.github/workflows/test.yml` to run tests on every push.

