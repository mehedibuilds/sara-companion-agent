# Architecture Decision Records

## ADR-001: Explicit graph orchestration

**Status:** Accepted

SARA uses LangGraph to express the request lifecycle as named state transitions. This preserves observability and testability as new specialist agents, retries, or human approvals are introduced.

## ADR-002: SQLite/FTS5 as the initial memory backend

**Status:** Accepted

The product begins with a single-node, encrypted-volume-friendly storage profile. SQLite gives transactional local facts and FTS5 supports inexpensive semantic-adjacent retrieval for conversation continuity. A repository boundary (`MemoryStore`) isolates future migration to Postgres/vector search.

## ADR-003: Specialists behind a registry

**Status:** Accepted

Intent detection and capability execution are separated. A specialist is an async callable registered under a bounded intent. Provider SDKs and prompts remain within their capability module rather than leaking into orchestration.