# Workspace Docs — Stage 1: Workspace Notes (Auth + RBAC)

Stage 1 of the project that grows from Team Notes into a Document Intelligence Platform.
Goal of this stage: get comfortable with authentication, authorization (RBAC), clean FastAPI structure, SQLAlchemy 2.x, migrations, and testing.

> Working rule: design it yourself first, attempt it, then bring your design/code for review.
> Note: links below are to official docs and well-known references. If one has moved, search by its title.

---

## 1. Scope

Users sign up, create workspaces, add existing users with a role, and write notes inside a workspace.
Nothing else in this stage: no files, queues, caching, or AI.

---

## 2. Data model

**users**
- `id` (UUID), `email` (unique, stored lowercase), `hashed_password`, `full_name`, `is_active`, `created_at`

**workspaces**
- `id`, `name`, `created_by`, `created_at`

**workspace_members**
- `workspace_id`, `user_id`, `role` (enum: owner / editor / viewer), `joined_at`
- Primary key: (`workspace_id`, `user_id`)

**notes**
- `id`, `workspace_id`, `author_id`, `title`, `content`, `created_at`, `updated_at`

**refresh_tokens** (stretch)
- `id`, `user_id`, `token_hash`, `expires_at`, `revoked_at`

Indexes: `notes.workspace_id`, `workspace_members.user_id`.
Decide yourself: what happens to notes when a workspace is deleted (cascade vs soft delete) and when an author leaves.

---

## 3. Endpoints

**Auth**
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `GET /users/me`

**Workspaces**
- `POST /workspaces`
- `GET /workspaces` (only mine)
- `GET /workspaces/{id}`
- `PATCH /workspaces/{id}`
- `DELETE /workspaces/{id}`

**Members**
- `GET /workspaces/{id}/members`
- `POST /workspaces/{id}/members` (add by email)
- `PATCH /workspaces/{id}/members/{user_id}` (change role)
- `DELETE /workspaces/{id}/members/{user_id}` (remove or leave)

**Notes**
- `POST /workspaces/{id}/notes`
- `GET /workspaces/{id}/notes` (pagination + title filter)
- `GET /workspaces/{id}/notes/{note_id}`
- `PATCH /workspaces/{id}/notes/{note_id}`
- `DELETE /workspaces/{id}/notes/{note_id}`

---

## 4. Permission rules

| Action | Owner | Editor | Viewer | Non-member |
|---|---|---|---|---|
| View workspace and notes | Yes | Yes | Yes | 404 |
| Create note | Yes | Yes | No (403) | 404 |
| Edit/delete own note | Yes | Yes | No (403) | 404 |
| Edit/delete others' notes | Yes | No (403) | No (403) | 404 |
| Manage members/roles, rename/delete workspace | Yes | No (403) | No (403) | 404 |

Extra rules:
- Non-members get **404, not 403**, so a workspace's existence is not leaked.
- A workspace must always keep at least one owner (block the last owner from leaving or being demoted).
- The creator becomes owner automatically.

---

## 5. Auth design

- Hash passwords with argon2 (or bcrypt). Never log passwords.
- Access token (JWT): ~15 minutes, `sub` = user ID.
- Refresh token: ~7 days (stretch goal; store only a hash).
- Login returns a generic "invalid credentials" error whether the email or the password is wrong.
- `get_current_user` dependency: decode token, load user, reject inactive users.

---

## 6. Architecture

```
app/
  main.py            # app factory, routers, exception handlers
  core/              # config.py (pydantic-settings), security.py, errors.py
  db/                # session.py, base.py
  models/            # SQLAlchemy 2.x models
  schemas/           # Pydantic request/response models
  repositories/      # DB queries only
  services/          # business rules + permission checks
  api/
    deps.py          # get_db, get_current_user, get_membership
    routers/         # auth, workspaces, members, notes
tests/
alembic/
```

Strict flow: **router -> service -> repository**.
Routers hold no business logic. Repositories hold no permission logic.

---

## 7. Key patterns to implement

1. `get_membership(workspace_id)` dependency: resolves to the user's membership or raises 404.
2. Reusable `require_role(*roles)` dependency, plus an ownership check inside the service for "editor edits own notes".
3. Uniform error responses: `{"error": {"code": "...", "message": "..."}}` via custom exceptions and handlers.
4. Separate Pydantic schemas for create / update / read. Never return the password hash.
5. Async SQLAlchemy sessions via a `get_db` dependency.

---

## 8. Tests (pytest + test database)

- Register and login, including duplicate email and wrong password.
- Expired and tampered tokens are rejected.
- Every row of the permission matrix as parametrized tests.
- Last-owner protection.
- Pagination limits and ordering.

---

## 9. Build order

1. Project skeleton, config, DB session, first migration
2. Users: register, login, `/users/me`
3. Workspaces + automatic owner membership
4. Members and role management
5. Notes with permission rules
6. Error handling, pagination, full test suite
7. Refresh tokens (stretch)

---

## 10. Definition of done

- A viewer can't write, a non-member can't see anything, and tests prove both.
- You can explain, without notes, how a request flows from token to permission decision.
- You can add a fourth role (e.g. "commenter") by changing only one or two places.

## 11. Decisions that are deliberately yours

Soft vs hard delete, UUID vs integer keys, how invites work for users who don't exist yet, whether role checks live in dependencies or services. Write down what you chose and why.

---

# Resources by topic

## A. FastAPI structure and dependency injection
- FastAPI: Dependencies — https://fastapi.tiangolo.com/tutorial/dependencies/
- FastAPI: Dependencies in path operation decorators / with yield — https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
- FastAPI: Bigger Applications (routers, multiple files) — https://fastapi.tiangolo.com/tutorial/bigger-applications/
- FastAPI Best Practices (community, opinionated) — https://github.com/zhanymkanov/fastapi-best-practices
- Reference project to *read, not copy*: full-stack-fastapi-template — https://github.com/fastapi/full-stack-fastapi-template
  Focus on: how routers, models, dependencies, and settings are organized. Skip the frontend.

## B. Authentication: passwords, JWT, tokens
- FastAPI: Security intro — https://fastapi.tiangolo.com/tutorial/security/
- FastAPI: OAuth2 with Password (and hashing), Bearer with JWT — https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
- jwt.io: Introduction to JSON Web Tokens — https://jwt.io/introduction
- OWASP Password Storage Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- OWASP Authentication Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- argon2-cffi docs — https://argon2-cffi.readthedocs.io/
- Check which hashing library the current FastAPI security tutorial recommends, and why `passlib` is often avoided in new projects.

Questions to be able to answer afterward:
- Why hash instead of encrypt? Why a slow hash?
- Access vs refresh token: what does each protect against?
- Where should tokens live on the client, and what are the trade-offs?

## C. Authorization and RBAC
- OWASP Authorization Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- OWASP Top 10: Broken Access Control — https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- MDN: 401 vs 403 vs 404 — https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401 , .../403 , .../404
- Search: "RBAC vs ABAC" and "IDOR vulnerability" and read one good explainer of each.

Questions to be able to answer afterward:
- Authentication vs authorization?
- Why 404 for non-members?
- Why must permission checks live in one place?

## D. SQLAlchemy 2.x (async) and data modeling
- SQLAlchemy 2.0 Unified Tutorial — https://docs.sqlalchemy.org/en/20/tutorial/index.html
- Declarative mapping with `Mapped[]` / `mapped_column` — https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html
- Asyncio extension — https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- Relationship loading techniques (avoid N+1; lazy loading in async) — https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html
- Association objects (for `workspace_members` with extra columns) — https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#association-object

## E. Migrations
- Alembic tutorial — https://alembic.sqlalchemy.org/en/latest/tutorial.html
- Alembic autogenerate (and its limits) — https://alembic.sqlalchemy.org/en/latest/autogenerate.html
- Async Alembic recipe: search "Alembic async template" (`alembic init -t async`).

## F. Pydantic and settings
- Pydantic docs — https://docs.pydantic.dev/latest/
- Pydantic Settings — https://docs.pydantic.dev/latest/concepts/pydantic_settings/
- FastAPI: Response Model — https://fastapi.tiangolo.com/tutorial/response-model/
- FastAPI: Extra models (create/update/read separation) — https://fastapi.tiangolo.com/tutorial/extra-models/

## G. Error handling
- FastAPI: Handling Errors — https://fastapi.tiangolo.com/tutorial/handling-errors/
- RFC 9457 Problem Details for HTTP APIs (optional alternative to your own error shape) — https://www.rfc-editor.org/rfc/rfc9457

## H. Layered architecture (router / service / repository)
- Cosmic Python, Chapter 2: Repository Pattern — https://www.cosmicpython.com/book/chapter_02_repository.html
- Cosmic Python, Chapter 4: Service Layer — https://www.cosmicpython.com/book/chapter_04_service_layer.html
  Read for ideas, not to copy. The book is heavier than this stage needs. The goal is the separation of responsibilities.

## I. Pagination
- Use The Index, Luke: "No Offset" (why offset pagination gets slow) — https://use-the-index-luke.com/no-offset
- Search: "offset vs keyset pagination". Start with offset/limit; know the trade-off.

## J. Testing
- FastAPI: Testing — https://fastapi.tiangolo.com/tutorial/testing/
- FastAPI: Async Tests — https://fastapi.tiangolo.com/advanced/async-tests/
- pytest: Parametrize — https://docs.pytest.org/en/stable/how-to/parametrize.html
- pytest: Fixtures — https://docs.pytest.org/en/stable/how-to/fixtures.html
- pytest-asyncio — https://pytest-asyncio.readthedocs.io/
- Search: "FastAPI async SQLAlchemy pytest transaction rollback fixture" to learn per-test DB isolation.

## K. Python concepts you'll lean on
- `enum` — https://docs.python.org/3/library/enum.html
- `typing` and type hints — https://docs.python.org/3/library/typing.html
- `contextlib` and async context managers — https://docs.python.org/3/library/contextlib.html
- Decorators and closures (for `require_role`): search "Real Python decorators primer".

---

# Frontend (optional, keep it small)

Backend is the point of this stage. Use Swagger UI (`/docs`) as your first client.
Build a UI only to feel the API from a user's side. Timebox it (a weekend), and let the UI expose gaps in your API design.

## Suggested stack (matches what you already know)
React + Vite + TypeScript, React Router, TanStack Query (server state), Tailwind CSS, and shadcn/ui components.
- Vite — https://vite.dev/guide/
- TanStack Query — https://tanstack.com/query/latest
- Tailwind CSS — https://tailwindcss.com/docs
- shadcn/ui — https://ui.shadcn.com/

## Screens to build (each maps to endpoints)

1. **Login / Register** -> `/auth/login`, `/auth/register`
2. **Workspace list + "Create workspace"** -> `GET/POST /workspaces`
3. **Workspace view with notes list** (search box, pagination) -> `GET /workspaces/{id}/notes`
4. **Note editor** (title + content; read-only for viewers) -> note endpoints
5. **Members settings page** (list, add by email, role dropdown, remove) -> members endpoints; owner-only controls

Basic layout:

```
+--------------------------------------------------+
| [Workspace switcher v]            [User menu v]  |
+-----------+--------------------------------------+
| Notes     |  Notes list                [+ New]   |
| Members   |  [ search................ ]          |
| Settings  |  - Title A     author  updated       |
|           |  - Title B     author  updated       |
|           |  [< prev]  page 1  [next >]          |
+-----------+--------------------------------------+
```

Members page:

```
Members                                  [+ Add member]
-----------------------------------------------------
 alice@x.com   Owner   (you)
 bob@x.com     [Editor v]   [Remove]
 carol@x.com   [Viewer v]   [Remove]
```

UI rules that reinforce backend rules:
- Hide or disable actions the user's role can't perform (but never rely on this; the backend enforces it).
- Show 403/404 states cleanly.
- Show validation errors from your uniform error format.

## Inspiration to analyze (study structure, don't clone)
- **Notion**: workspace switcher, sidebar, page list — https://www.notion.so
- **Linear**: clean workspace/team settings, members and roles — https://linear.app
- **Vercel**: team settings -> members and roles page (good model for your members screen) — https://vercel.com
- **GitHub**: organization -> People page and role dropdowns — https://github.com
- **Slack**: workspace switching and invite flow — https://slack.com
- **shadcn/ui examples**: dashboard, authentication, and settings layouts you can adapt — https://ui.shadcn.com/examples
- **shadcn/ui blocks**: ready login/signup and sidebar blocks — https://ui.shadcn.com/blocks
- **Mobbin** (screenshots of real apps' flows; search "login", "team members", "settings") — https://mobbin.com
- **Dribbble / Behance**: search "team workspace dashboard", "members settings UI" for visual ideas.

How to analyze a reference:
1. Screenshot the screen and list every action on it.
2. Write which API call each action needs.
3. Note which actions depend on role.
4. Note what happens on error and on empty state.
5. Build that screen from your list.

---

# Suggested 2-week plan (adjust freely)

| Days | Focus |
|---|---|
| 1-2 | Skeleton, config, DB, Alembic, users + register/login |
| 3-4 | JWT, `get_current_user`, `/users/me`, workspaces |
| 5-6 | Members, roles, `get_membership`, `require_role` |
| 7-8 | Notes + ownership rules |
| 9-10 | Error handling, pagination, test suite |
| 11-12 | Review/refactor, optional refresh tokens |
| 13-14 | Optional small frontend, write your design note |

Write a one-page design note at the end: what you built, what broke, decisions you made, what you'd change.