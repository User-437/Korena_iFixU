"""Database connector: PostgreSQL for the app; SQLite only for offline/testing.

Supports DATABASE_URL (local/hosted) OR the separate PGHOST/PGUSER/... variables
used by Docker Compose. Separate PG variables safely handle special characters in
passwords without needing to URL-encode them.
"""
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from models import Base, User
from accounting import create_default_accounts

load_dotenv(Path(__file__).resolve().parent / '.env')


def resolve_database_url(url=None):
    """Return an explicit PostgreSQL/SQLite connection, never a silent MySQL fallback."""
    url = url or os.environ.get('DATABASE_URL')
    if url:
        # Some hosted providers give a plain postgres:// or postgresql:// URL.
        if isinstance(url, str) and url.startswith('postgres://'):
            url = 'postgresql+psycopg://' + url[len('postgres://'):]
        elif isinstance(url, str) and url.startswith('postgresql://'):
            url = 'postgresql+psycopg://' + url[len('postgresql://'):]
        if isinstance(url, str) and not url.startswith(('postgresql+psycopg://', 'sqlite://')):
            raise ValueError('Use a PostgreSQL URL (postgresql+psycopg://) or SQLite for offline/tests.')
        return url
    pg = {k: os.environ.get(k) for k in ('PGHOST', 'PGUSER', 'PGPASSWORD', 'PGDATABASE')}
    if all(pg.values()):
        return URL.create('postgresql+psycopg',
                          username=pg['PGUSER'], password=pg['PGPASSWORD'],
                          host=pg['PGHOST'], port=int(os.environ.get('PGPORT', '5432')),
                          database=pg['PGDATABASE'])
    raise RuntimeError('No PostgreSQL configured. Set DATABASE_URL in .env, or set PGHOST, PGUSER, PGPASSWORD, and PGDATABASE.')


def connect(url=None):
    resolved = resolve_database_url(url)
    params = {'pool_pre_ping': True}
    if str(resolved).startswith('sqlite:'):
        params['connect_args'] = {'check_same_thread': False}
    engine = create_engine(resolved, **params)
    return engine, sessionmaker(bind=engine, expire_on_commit=False)


def initialize(engine, sessions, email=None, password=None):
    """First run creates empty tables, three-digit accounts, and first administrator.

    Safe to call again: does not erase existing data or change existing password.
    """
    Base.metadata.create_all(engine)
    with sessions.begin() as db:
        create_default_accounts(db)
        if not db.query(User).first():
            if not password or len(password) < 10 or password.upper().startswith(('REPLACE_', 'CHANGEME', 'CHANGE_THIS')):
                raise ValueError('Set INITIAL_ADMIN_PASSWORD to 10+ characters in .env.')
            db.add(User(email=(email or 'admin@korena.local').lower().strip(),
                        password_hash=generate_password_hash(password), role='admin'))
