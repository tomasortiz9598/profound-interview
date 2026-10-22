# profound-interview

Hello World web app. The backend (FastAPI + PostgreSQL) serves a single greeting, and the webapp (React + Vite) displays it.

## Project layout
- `backend/` – FastAPI application, database models, and Alembic migrations.
- `webapp/` – React SPA served by Vite.

## Prerequisites
- Python 3.11 and [Pipenv](https://pipenv.pypa.io/en/latest/).
- Node.js 18+ and npm.
- Docker & Docker Compose (optional, for running Postgres and the API together).

## Environment configuration
1. Copy the example file and adjust values as needed:
   ```bash
   cd backend
   cp .env.example .env
   ```
2. PostgreSQL settings: `PGHOST=localhost`, `PGPORT=5432`, `PGUSER`, `PGPASSWORD`, `PGDATABASE=profound_interview`.
3. Alembic also respects `DATABASE_URL`; you may set `DATABASE_URL=postgresql://user:pass@localhost:5432/profound_interview` instead of the discrete vars if preferred.

## Backend (FastAPI)
Install dependencies:
```bash
cd backend
pipenv install --dev
```

### Start infrastructure
- **Docker (recommended for local dev)**:
  ```bash
  cd backend
  docker compose up --build
  ```
The API becomes available at `http://localhost:8000` and PostgreSQL at `localhost:5432`.

### Apply database migrations
```bash
cd backend
pipenv run alembic upgrade head
```
The first migration creates the `hello_worlds` table and inserts one row.

## Webapp (React + Vite)
```bash
cd webapp
npm install
npm run dev
```
The dev server runs on `http://localhost:5173` and proxies API calls to `http://localhost:8000`. Build for production with `npm run build` and preview the static output using `npm run preview`.

## Tests
- **Backend**: repository and endpoint tests mock the database session.
  ```bash
  cd backend
  pipenv run pytest
  ```
- **Webapp**: no automated tests are defined today.
