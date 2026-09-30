# DocVault AI

> Secure document ingestion, extraction, and object-storage backend built with FastAPI.

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-async-4169E1?logo=postgresql&logoColor=white)
![MinIO](https://img.shields.io/badge/Object%20Storage-MinIO-C72E49?logo=minio&logoColor=white)
![Status](https://img.shields.io/badge/status-active%20development-orange)

## Overview

DocVault AI is the backend foundation for a document intelligence platform. The current implementation focuses on the production plumbing that comes before RAG/AI: authentication, document validation, PDF/TXT ingestion, text extraction, object storage, metadata persistence, and failure handling.

AI retrieval and question-answering are roadmap items, not presented here as finished functionality.

## Implemented capabilities

- User authentication with JWT-based access control
- Authenticated PDF/TXT upload endpoint
- File-type and content validation
- 10 MB upload limit handling
- PDF text extraction through `pypdf`
- Extracted-text size cap to protect downstream processing
- Per-user object keys
- S3-compatible object storage through MinIO
- Async FastAPI + SQLAlchemy persistence layer
- Alembic migrations
- Explicit storage/validation/extraction error handling
- Health endpoint and interactive API docs

## Request flow

```text
Authenticated client
       |
       v
FastAPI /documents
       |
       +--> file validation
       |
       +--> text extraction (PDF/TXT)
       |
       +--> object key generation
       |
       +--> MinIO object storage
       |
       +--> PostgreSQL metadata
       v
 Document response
```

## Project structure

```text
app/
├── core/          # configuration and domain exceptions
├── db/            # async database session/base
├── dependencies/  # authentication dependencies
├── models/        # user/document persistence models
├── routers/       # auth and document endpoints
├── schemas/       # API contracts
├── services/      # auth, validation, extraction, storage, document workflow
└── main.py        # FastAPI app
migrations/        # Alembic migrations
```

## Configuration

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/docvault
JWT_SECRET_KEY=replace-with-a-long-random-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

STORAGE_ENDPOINT=localhost:9000
STORAGE_ACCESS_KEY=minioadmin
STORAGE_SECRET_KEY=change-me
STORAGE_BUCKET=docvault
STORAGE_SECURE=false
```

Do not commit real credentials.

## Running locally

Provision PostgreSQL and an S3-compatible MinIO service, create `.env`, install project dependencies, then:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` for Swagger UI.

## API highlights

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service health |
| Auth routes | `/auth/*` | Register/login/current-user flow |
| POST | `/documents` | Validate, extract, store, and persist a document |

## Engineering focus

- **Storage isolation:** generated object keys are namespaced by user.
- **Defensive ingestion:** invalid type/content, oversized files, extraction failures, and storage outages map to explicit API failures.
- **Blocking SDK isolation:** synchronous MinIO calls are moved into FastAPI's thread pool.
- **Bounded extraction:** extracted PDF text is capped before future AI processing.
- **Separation of concerns:** document orchestration, extraction, validation, storage, auth, routing, and persistence live in dedicated modules.

## Roadmap

The following are planned features:

- [ ] Complete AI service implementation
- [ ] Chunking and embedding pipeline
- [ ] Vector storage and semantic retrieval
- [ ] Source-grounded document Q&A
- [ ] Background ingestion jobs for large documents
- [ ] Automated unit/integration tests
- [ ] CI for linting, typing, and tests
- [ ] Docker Compose for API, PostgreSQL, and MinIO
- [ ] Observability, retention policy, and deployment documentation

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Use issues for scoped work and pull requests for reviewable changes.

## Status

DocVault AI is under active development. The current repository is a document-ingestion/storage backend foundation; AI/RAG capabilities are explicitly tracked as future work.
