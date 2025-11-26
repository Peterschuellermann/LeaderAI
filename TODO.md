# LeaderAI To-Do List

## Production Readiness

### Security (AppSec/ITSec)
- [ ] **Secure Sessions**: Replace plain `session_user` cookie with signed/encrypted sessions (e.g., `starlette.middleware.sessions.SessionMiddleware`).
- [ ] **CSRF Protection**: Implement CSRF tokens for forms (especially critical since we use cookies).
- [ ] **Secure Headers**: Add `TrustedHostMiddleware`, HSTS, CSP, and X-Content-Type-Options.
- [ ] **Rate Limiting**: Implement basic rate limiting for login endpoints to prevent brute force.
- [ ] **Input Validation**: Review and ensure all Pydantic models have strict types and validation.

### DevOps & Infrastructure
- [ ] **Production Dockerfile**: Create a multi-stage build to minimize image size and run as a non-root user.
- [ ] **WSGI/ASGI Server**: Configure `gunicorn` with `uvicorn.workers.UvicornWorker` for production resiliency.
- [ ] **Health Check**: Add a `/health` endpoint for orchestrators (K8s/Docker Swarm).
- [ ] **Structured Logging**: Replace `print` statements with a proper logging configuration (JSON format for prod).
- [ ] **Database Migrations**: Ensure `alembic upgrade head` runs reliably on container startup (or separate init container).
- [ ] **Backup Strategy**: Document or script automated backups (S3/remote storage) instead of local file backup.
