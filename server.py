"""WSGI entry point for a PostgreSQL-backed Korena web server.

Run `python manage.py init-db` ONCE before Gunicorn starts. Docker Compose does
this automatically in the Dockerfile startup command.
"""
import os
from app import create_app

if not os.environ.get('DATABASE_URL') and not all(os.environ.get(key) for key in ('PGHOST', 'PGUSER', 'PGPASSWORD', 'PGDATABASE')):
    raise RuntimeError('Configure a PostgreSQL DATABASE_URL or PGHOST/PGUSER/PGPASSWORD/PGDATABASE before starting the server.')
if (not os.environ.get('FLASK_SECRET_KEY') or len(os.environ['FLASK_SECRET_KEY']) < 32
        or os.environ['FLASK_SECRET_KEY'].upper().startswith('REPLACE_')):
    raise RuntimeError('FLASK_SECRET_KEY must contain 32+ characters.')

app = create_app()
