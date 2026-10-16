# Korena PharmaLedger — PostgreSQL Edition (FRESH DATABASE)

Korena is a Flask + SQLAlchemy web application with Journal, General Ledger, Trial Balance, account management, admin Audit Log, and CSV exports. In this edition PostgreSQL is the database for both local development and the shared server. **This ZIP contains code only, not an existing database.**

**Start here: [`START_HERE_POSTGRESQL.md`](START_HERE_POSTGRESQL.md)**. Follow the Docker Compose or the Windows native PostgreSQL instructions—**not both at once**.

- Default chart of accounts uses **three-digit codes** (`100`, `110`, `200`, etc.).
- `python manage.py init-db` creates tables, seeds default accounts and creates the first admin. It does not delete existing records if run again.
- `python manage.py seed-demo` is **OPTIONAL** and inserts fictional pharmacy examples; leave it out if you want a completely empty transaction journal.
- PostgreSQL is **not** XAMPP or phpMyAdmin. Use Docker Compose or an installed PostgreSQL server with pgAdmin/psql.
- The standalone offline desktop launcher still uses its **own local SQLite database** by design; it does not share the PostgreSQL data.
- Admin actions and journal posts are logged in `audit_log`. This is an educational project, not a certified production accounting system. Do not use real pharmacy/patient information for testing.

### Local operations (in the Korena_JLT folder)

```powershell
.\.venv\Scripts\python.exe manage.py check-db
.\.venv\Scripts\python.exe manage.py init-db
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe app.py
```

### Server operations (Docker)

```powershell
docker compose up --build -d
docker compose ps
docker compose logs -f app
# Optional: add fictional sample journal entries (only on an empty journal)
docker compose exec app python manage.py seed-demo
```

The PostgreSQL database is stored in the **named Docker volume**, not inside this ZIP. `docker compose down` stops services while keeping the data. **Never use `docker compose down -v`** unless you intentionally want to destroy the PostgreSQL data.

For Android/iOS/Windows thin-client integration see `../INTEGRATED_SETUP.md`. For a hosted multi-device deployment use an HTTPS reverse proxy and secure backups. Docker Compose in this ZIP binds the website to `127.0.0.1` by default, so other devices cannot reach it without additional network configuration.
