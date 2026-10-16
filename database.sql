-- POSTGRESQL ONLY: run the following TWO commands separately in pgAdmin
-- while connected as the PostgreSQL administrator (often called postgres).
-- On a FRESH server; do not run on an existing DB without checking first.
-- Replace the example password with the same value used in .env.
-- Step 1: execute by itself:
CREATE ROLE korena WITH LOGIN PASSWORD 'REPLACE_POSTGRES_PASSWORD';
-- Step 2: execute by itself (CREATE DATABASE must not run in a transaction):
CREATE DATABASE pharmaledger OWNER korena;
-- Then run: python manage.py init-db (creates all tables and default accounts)
