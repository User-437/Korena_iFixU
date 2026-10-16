# Note about desktop setup in the PostgreSQL edition

The `Korena_JLT` Flask web app now uses **PostgreSQL** as its main database. Follow `START_HERE_POSTGRESQL.md` to install PostgreSQL locally or start the bundled Docker Compose stack.

The separate `desktop_launcher.py` / one-file offline executable is intentionally a different **standalone SQLite** workflow, not a PostgreSQL client. Its offline data will **not synchronize** into your PostgreSQL database. If you want a desktop window that connects to the shared database, use the thin `windows_client` wrapper described in `../INTEGRATED_SETUP.md`, which connects to the Korena Flask server—not directly to PostgreSQL.

**Do not use old MySQL/XAMPP setup instructions for this package.**
