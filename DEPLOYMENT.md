# AOCID Platform — Deployment & Operations

The AOCID platform is the **Ait Ourir Chess Club** website — a Django project
(`chess_club`) served at **https://aitourirchessclub.ma**. It runs in Docker on
the server **`arvps2`** (`148.113.203.224`, OVH) under `/opt/aocid`.

---

## 1. What changed (Sept 2026 migration)

- **Moved** off the old VPS (`aocidvps`, `135.125.133.3`) to `arvps2`, now fully
  **containerized with Docker Compose** (was a bare gunicorn+systemd setup).
- **Python 3.12** in the image (the host runs 3.13, which Django 4.2 / Pillow 10.1
  don't support — the container pins 3.12 so nothing on the host is needed).
- **PostgreSQL 14** in a container (data migrated via `pg_dump`/`pg_restore`).
- **DNS/TLS**: `@` and `www` A-records point to `arvps2`; Let's Encrypt certs on the
  host nginx.
- **Email fixed & re-homed**: outbound mail moved from the broken Office 365 account
  to the self-hosted server **`mail.sentinel.ma`**, sending as
  **`noreply@aitourirchessclub.ma`** (see `MAIL_SERVER.md` in the `sentinel` repo).
  - The book-download and contact/application forms used to hardcode
    `from_email="noreply@ekblocks.com"` — now `noreply@aitourirchessclub.ma`.
  - Contact-form messages are delivered to `settings.EMAIL_RECIPIENTS`
    (`mouadkommir@gmail.com` **and** `contact@aitourirchessclub.ma`).

---

## 2. Architecture

Host nginx (TLS, ports 80/443 for `aitourirchessclub.ma` + `www`)
→ proxies to `127.0.0.1:8085`
→ **compose stack** in `/opt/aocid`:

| Service | Image | Role |
|---------|-------|------|
| `db`    | `postgres:14-alpine` | database, named volume `aocid_pgdata` |
| `web`   | built (`python:3.12-slim` + gunicorn ×3) | the Django app; runs `migrate` + `collectstatic` on start |
| `nginx` | `nginx:alpine` | serves `/static` + `/media`, proxies to `web`; published on `127.0.0.1:8085` |

The compose **project name is pinned to `aocid`** (`name: aocid` in the compose
file) so the data volumes (`aocid_pgdata`, `aocid_staticdata`) are never recreated,
regardless of which directory compose is run from.

---

## 3. Repository layout (deployment-relevant)

```
Dockerfile                 # web image (python:3.12-slim, installs requirements.docker.txt)
.dockerignore
requirements.docker.txt    # authoritative pinned deps (incl. psycopg2-binary, gunicorn)
local_settings.example.py  # template for chess_club/local_settings.py (gitignored secrets)
deploy/
  docker-compose.yml       # the compose stack (source of truth)
  nginx.conf               # the in-container nginx config
  .env.example             # template for /opt/aocid/.env
  deploy.sh                # the redeploy script
```

---

## 4. Configuration & secrets (NOT in git)

| File | Location on server | Holds | Template |
|------|--------------------|-------|----------|
| `chess_club/local_settings.py` | `/opt/aocid/aocid_platform/` | DB creds, SMTP creds, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `SECURE_PROXY_SSL_HEADER` | `local_settings.example.py` |
| `.env` | `/opt/aocid/` | Postgres creds, `DB_HOST=db`, `EXTRA_ALLOWED_HOSTS`, `EXTRA_CSRF_ORIGINS` | `deploy/.env.example` |

Both are `.gitignore`d. `local_settings.py` is imported at the end of
`chess_club/settings.py`, so it overrides the defaults there.

---

## 5. Redeploying (normal workflow)

Edit locally → commit → push to `main` → on the server run:

```bash
bash /opt/aocid/aocid_platform/deploy/deploy.sh
```

`deploy.sh` does:
1. `git pull --ff-only origin main` in `/opt/aocid/aocid_platform`
2. copies `deploy/docker-compose.yml` and `deploy/nginx.conf` up to `/opt/aocid/`
3. `docker compose up -d --build web nginx` (the **`db` is left running/untouched**)

The `web` container runs `migrate --noinput` and `collectstatic --noinput` on every
start, so those happen automatically.

---

## 6. Common operations

```bash
cd /opt/aocid
docker compose ps                         # status
docker compose logs -f web                # app logs
docker compose exec web python manage.py shell        # Django shell
docker compose exec web python manage.py migrate      # manual migrate
docker compose restart web                # restart app only

# DB backup / restore
docker compose exec -T db pg_dump -Fc -U aocid_db_user aocid_db > backup.dump
docker compose exec -T db pg_restore --clean --if-exists -U aocid_db_user -d aocid_db < backup.dump
```

---

## 7. Bootstrapping a fresh server

1. Install Docker + Docker Compose; create `/opt/aocid` (owned by the deploy user).
2. `git clone git@github.com:aiokaizen/aocid_platform.git /opt/aocid/aocid_platform`
3. Create `/opt/aocid/.env` from `deploy/.env.example` (fill real values).
4. Create `chess_club/local_settings.py` from `local_settings.example.py` (fill real values).
5. `cp deploy/docker-compose.yml deploy/nginx.conf /opt/aocid/`
6. `cd /opt/aocid && docker compose up -d --build`
7. Restore the DB dump into the `db` container.
8. Add a host nginx vhost for `aitourirchessclub.ma` + `www` → `127.0.0.1:8085`, then
   `certbot --nginx -d aitourirchessclub.ma -d www.aitourirchessclub.ma`.

---

## 8. Notes

- Email deliverability, DKIM/SPF, and how to add mailboxes/domains are documented in
  **`MAIL_SERVER.md`** (in the `sentinel` repo and `/opt/mailserver/`).
- The repo has known Dependabot vulnerabilities (Django 4.2 + pinned older deps) — a
  dependency-update pass is advisable but was out of scope for the migration.
