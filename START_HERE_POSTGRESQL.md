# START HERE — FRESH Korena + PostgreSQL (NO old data)

This package was adapted from the user's **Korena_PharmaLedger.zip** codebase. It is a clean setup: do NOT import MySQL dumps, run three-digit migrations, or copy old `.env` files. Choose **ONE** of the two ways to run it below.

## A. EASIEST: Docker Desktop (PostgreSQL + Flask together)

Requirements: Windows 10/11 with Docker Desktop (Linux containers/WSL 2 enabled), or a computer with Docker Engine and Compose.

1. Extract the ZIP. Go to `Korena_PharmaLedger_PWA_Project/Korena_JLT`.
2. In File Explorer, turn on **View > Show > File name extensions** (avoid `.env.txt`).
3. Copy `.env.server.example` to `.env` **in the Korena_JLT folder**.
4. Open `.env` in Notepad. Fill in the blank `POSTGRES_PASSWORD`, `FLASK_SECRET_KEY`, and `INITIAL_ADMIN_PASSWORD` values with unique credentials. `POSTGRES_PASSWORD` is the database password. Use a 32+ character random `FLASK_SECRET_KEY` (run `py -c "import secrets; print(secrets.token_hex(32))"`), your chosen `ADMIN_EMAIL`, and 10+ character `INITIAL_ADMIN_PASSWORD`. Keep `.env` private.
5. Launch Docker Desktop. Open PowerShell/Terminal in `Korena_JLT` and run:

   ```powershell
   docker compose up --build -d
   docker compose ps
   docker compose logs --tail=60 app
   ```

6. The first app startup **automatically runs `manage.py init-db`**: PostgreSQL creates 5 application tables (`users`, `accounts`, `entries`, `lines`, `audit_log`), default 3-digit accounts and the admin user. It does **not** add journal transactions.
7. Open **http://127.0.0.1:8000** and sign in using the admin email/password in `.env`.
8. Optional DEMO entries, only if you want them: `docker compose exec app python manage.py seed-demo` (10 fictional pharmacy entries plus opening capital). Skip for a blank Journal.

To stop: `docker compose down`. To start later: `docker compose up -d`. **NEVER `docker compose down -v`** unless you intentionally want to erase the database. Changing POSTGRES_PASSWORD in `.env` AFTER database creation does NOT update the existing database user password automatically.

To verify the Postgres data without adding tools locally, execute:

```powershell
docker compose exec db psql -U korena -d pharmaledger -c "\dt"
docker compose exec db psql -U korena -d pharmaledger -c "SELECT code, name FROM accounts ORDER BY code LIMIT 8;"
```

The `db` service does not publish port 5432 to the host (safer). For pgAdmin access, configure its connection through Docker networking or temporarily bind the DB to `127.0.0.1` with explicit credentials—do not expose it publicly.

## B. NO DOCKER: Installed PostgreSQL + Windows Python

Requirements: **PostgreSQL 16+**, optionally pgAdmin, and **Python 3.11+**. MySQL/XAMPP is not needed.

1. Install PostgreSQL and remember the administrator (`postgres`) password. Start the PostgreSQL service.
2. Open **pgAdmin > Servers > your server**, connect as `postgres`. In Query Tool run each statement below **one at a time**. Pick your own strong password and use the SAME password in `.env`:

   ```sql
   CREATE ROLE korena WITH LOGIN PASSWORD 'YOUR_OWN_POSTGRES_PASSWORD';
   ```

   Then, separately:

   ```sql
   CREATE DATABASE pharmaledger OWNER korena;
   ```

   **Alternative:** run the two separate commands in `database.sql` after replacing the placeholder. Do not run `CREATE DATABASE` inside a transaction block.

3. In `Korena_JLT`, copy `.env.example` to `.env`. Set:

   ```ini
   DATABASE_URL=postgresql+psycopg://korena:YOUR_OWN_POSTGRES_PASSWORD@127.0.0.1:5432/pharmaledger
   FLASK_SECRET_KEY=GENERATE_A_RANDOM_32_PLUS_CHARACTER_SECRET
   ADMIN_EMAIL=admin@korena.local
   INITIAL_ADMIN_PASSWORD=CHOOSE_YOUR_OWN_PASSWORD_AT_LEAST_10_CHARS
   PORT=5000
   ```

   If the database password contains `@`, `#`, `:`, `/`, `%`, etc., percent-encode it inside DATABASE_URL, or instead configure `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER` and `PGPASSWORD` environment variables (special characters are supported safely by that format). Avoid quoting values in `.env` unless you understand dotenv quoting.

4. From a PowerShell window opened in `Korena_JLT`:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe manage.py check-db
   .\.venv\Scripts\python.exe manage.py init-db
   .\.venv\Scripts\python.exe app.py
   ```

5. Open **http://127.0.0.1:5000** and sign in. If you prefer, `setup_windows.bat` and `start_windows.bat` automate most of the same steps AFTER PostgreSQL + `.env` are configured.
6. Optional demo entries: stop the web app with `Ctrl+C`, then run `.\.venv\Scripts\python.exe manage.py seed-demo` and restart the app.

## What you should see in a clean start

- A login page, then Journal / General Ledger / Trial Balance / admin Audit Log.
- At first, the Journal is **empty** (unless you explicitly seeded demo transactions).
- Default accounts are created with **3-digit codes**.
- An admin account exists, but **your username/password are what you set in `.env`**, not credentials inside the ZIP.
- PostgreSQL stores the data; `manage.py` uses SQLAlchemy to create the tables. You do **NOT** import MySQL `database.sql` syntax into PostgreSQL.

## Troubleshooting

| Problem | What to do |
|---|---|
| Docker says `POSTGRES_PASSWORD` is missing | Your `.env` is not beside `compose.yaml`, or is still empty. |
| App container restarting | Run `docker compose logs --tail=100 app`; check `FLASK_SECRET_KEY` and admin password. |
| `Connection refused` for port 5432 (Windows native) | Start the PostgreSQL service and check its configured port. |
| `password authentication failed for user korena` | Match role password to `.env` (on fresh setup); Postgres passwords are case-sensitive. |
| `database pharmaledger does not exist` | Create the database under pgAdmin as directed in step B2. |
| `No module named psycopg` | Install `requirements.txt` in the active `.venv`. |
| Can't log in after changing `.env` | The initial admin is created **once**. Changing its password in `.env` doesn't reset the existing database user's password. Use the password reset utility instead. |
| Need a totally new blank DB | Create a new PostgreSQL database (and adjust `.env`) or deliberately wipe the Docker volume **only if you want to lose all data**. |

## Security and scope

Use this for course/demo testing first. Do not upload `.env` or screenshots of passwords. If you want multiple devices to access the same database, deploy the Flask app behind HTTPS; keep PostgreSQL private and configure backups. The app is not a fully certified production accounting system and contains no data migration from older installations.
