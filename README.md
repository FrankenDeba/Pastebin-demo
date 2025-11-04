# pastebin-demo

# pastebin-demo

A small demo project demonstrating a Pastebin-like service with a FastAPI backend and a Vite + React (TypeScript) frontend. The repository includes Docker configuration and monitoring stacks (Prometheus / Loki / Promtail) for local testing.

Key points
- Backend: FastAPI (app/).
- Frontend: Vite + React + TypeScript (UI/).
- Container setups: Dockerfiles (root and app/) and docker-compose.yml.
- Monitoring: prometheus.yml, loki-config.yaml, promtail-config.yaml included.

Repository layout (top-level)
- .gitignore, Dockerfile, docker-compose.yml
- app/ — FastAPI application
    - app/main.py — application entry (ASGI)
    - app/models/ — data / CRUD
    - app/services/ — logger, analytics, reader, writter, middleware
    - app/Dockerfile
- UI/ — Vite + React TypeScript frontend
    - UI/src/ — components, assets, utils
    - UI/package.json, UI/vite.config.ts, UI/tsconfig*.json
- monitoring configs: prometheus.yml, loki-config.yaml, promtail-config.yaml
- requirements.txt — Python dependencies
- data_models.py — top-level data model definitions

Requirements
- Python 3.9+
- Node.js 16+ / npm or yarn
- Docker & docker-compose (for containerized runs)

Quickstart — local development

1) Backend (local, virtualenv recommended)
- Create and activate a virtualenv:
    - python -m venv .venv && source .venv/bin/activate
- Install dependencies:
    - pip install -r requirements.txt
- Run the app:
    - uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
- API docs (OpenAPI UI):
    - http://localhost:8000/docs

2) Frontend (UI/)
- Install and run:
    - cd UI
    - npm install
    - npm run dev
- Vite dev server default:
    - http://localhost:5173

3) Full stack with Docker Compose
- Start everything:
    - docker-compose up --build
- Backend default port: 8000. Frontend (Vite): 5173 (unless changed).

Building images manually
- Backend:
    - docker build -f app/Dockerfile -t pastebin-demo-backend app
- Frontend:
    - docker build -t pastebin-demo-frontend .

Monitoring (included)
- Example configs for Prometheus, Loki and Promtail are included for local experimentation. Integrate them into your docker-compose or monitoring stack as needed.

Usage guide (brief)
- Inspect the live OpenAPI docs for exact endpoints and payloads: GET /docs
- Common actions (examples assume typical paste endpoints; adapt to your API paths shown in /docs)

1) Create a paste (example)
- Request (JSON)
    - POST /pastes
    - Body: { "content": "My secret text", "expires_in": 3600 }
- curl example:
    - curl -X POST http://localhost:8000/pastes -H "Content-Type: application/json" -d '{"content":"My secret text","expires_in":3600}'

2) Retrieve a paste
- GET /pastes/{id}
- curl example:
    - curl http://localhost:8000/pastes/<PASTE_ID>

3) Delete / expire (if supported)
- DELETE /pastes/{id}
- curl example:
    - curl -X DELETE http://localhost:8000/pastes/<PASTE_ID>

Notes
- Endpoint names, request/response fields, authentication and extra features may differ — always verify /docs for the canonical API contract.
- For programmatic use, prefer the JSON API exposed via the FastAPI application and reuse the same base URL your frontend uses.

Notes & recommendations
- Persistence: this demo may not include a production DB. Add one for real persistence and update services/reader and services/writter.
- Env vars / secrets: configure environment variables for production deployments.
- Add a LICENSE if you intend to open-source under a specific license.

Contributing
- Fork, create a branch, and open a PR. Describe changes and run lint/tests locally (add tests if needed).

