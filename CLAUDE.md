# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Toutiao News System — a full-stack mobile-first news aggregation app with a Vue 3 frontend and an async Python/FastAPI backend.

## Development Commands

### Frontend (`xwzx-news/`)

```bash
cd xwzx-news
npm install          # install dependencies
npm run dev          # dev server at http://localhost:5173
npm run build        # production build
npm run preview      # preview production build
```

### Backend (`toutiao_app/`)

```bash
cd toutiao_app
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Full Stack via Docker

```bash
docker-compose up --build   # starts frontend (5173), backend (8000), MySQL (3307), Redis (6379)
```

**Database note:** `docker-compose.yml` creates a database named `toutiao`, but `toutiao_app/config/db_config.py` connects to `news_app`. When running outside Docker with a local MySQL, create the database as `news_app`. The SQL schema is at `toutiao_app/crud/database.sql`.

## Architecture

### Backend (`toutiao_app/`)

Async FastAPI app. All database operations use SQLAlchemy 2 async sessions with `aiomysql`.

- **`main.py`** — app entry point; registers 4 routers and CORS middleware
- **`routers/`** — HTTP endpoints (news, users, favorite, history); thin layer that delegates to `crud/`
- **`crud/`** — data access layer; `news_cache.py` wraps the news/category queries with Redis cache-aside logic
- **`models/`** — SQLAlchemy ORM models (User, UserToken, News, Category, Favorite, History)
- **`schemas/`** — Pydantic request/response models
- **`config/db_config.py`** — async engine and `get_db()` dependency injected into route handlers
- **`config/cache_conf.py`** — Redis async client; used by `cache/news_cache.py` for TTL-based caching
- **`utils/response.py`** — standard response wrapper `{code, message, data}` used by all endpoints
- **`utils/auth.py` / `security.py`** — JWT token creation/verification (python-jose) and bcrypt password hashing; tokens expire after 7 days

### Frontend (`xwzx-news/src/`)

Vue 3 SPA targeting mobile screens via Vant 4 component library.

- **`config/api.js`** — backend base URL (`http://127.0.0.1:8000`) and Alibaba Qwen AI chat config; update `baseURL` when deploying
- **`router/index.js`** — 12 lazy-loaded routes; `keepAlive: true` on Home, Category, AIChat, My to preserve scroll state
- **`store/`** — Pinia stores with `pinia-plugin-persistedstate`; modules for user auth state, news data, theme (dark/light), and language (i18n)
- **`views/`** — one component per route; `AIChat.vue` calls the Qwen API directly from the browser using the key in `api.js`
- **`i18n/`** — vue-i18n setup for multi-language support
- News content in `NewsDetail.vue` is rendered as Markdown using `marked` + `DOMPurify` for sanitization

### Data Flow

1. Frontend calls `http://127.0.0.1:8000` (configured in `src/config/api.js`)
2. Router → crud function → check Redis cache → if miss, query MySQL → populate cache
3. All responses follow `{code, message, data}` shape from `utils/response.py`
4. Auth token passed in `Authorization` header; validated via `utils/auth.py` dependency

## Key Configuration

| Setting | Location | Value |
|---|---|---|
| Backend DB URL | `toutiao_app/config/db_config.py` | `mysql+aiomysql://root:123456@mysql:3306/news_app` |
| Redis URL | `toutiao_app/config/cache_conf.py` | `redis://redis:6379` (Docker) |
| Frontend API base | `xwzx-news/src/config/api.js` | `http://127.0.0.1:8000` |
| AI chat key | `xwzx-news/src/config/api.js` | Qwen API key (Alibaba DashScope) |
