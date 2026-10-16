"""Configuration tests; no live PostgreSQL service needed."""
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from sqlalchemy.engine import URL

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from database import resolve_database_url


class PostgreSQLSetupTests(unittest.TestCase):
    def test_provider_urls_use_psycopg(self):
        self.assertEqual(resolve_database_url('postgres://u:p@host/db'),
                         'postgresql+psycopg://u:p@host/db')
        self.assertEqual(resolve_database_url('postgresql://u:p@host/db'),
                         'postgresql+psycopg://u:p@host/db')

    def test_structured_password_special_characters(self):
        with patch.dict(os.environ, {'DATABASE_URL': '', 'PGHOST': 'db', 'PGPORT': '5432',
                                     'PGDATABASE': 'pharmaledger', 'PGUSER': 'korena',
                                     'PGPASSWORD': 'p@ss:w/rd#'}, clear=True):
            url = resolve_database_url()
            self.assertIsInstance(url, URL)
            self.assertEqual(url.password, 'p@ss:w/rd#')
            self.assertEqual(url.drivername, 'postgresql+psycopg')

    def test_database_is_required_and_mysql_disallowed(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, 'No PostgreSQL'):
                resolve_database_url()
        with self.assertRaisesRegex(ValueError, 'PostgreSQL'):
            resolve_database_url('mysql+pymysql://root@localhost/db')

    def test_sqlite_only_as_explicit_offline_test_url(self):
        self.assertEqual(resolve_database_url('sqlite:///:memory:'), 'sqlite:///:memory:')


if __name__ == '__main__':
    unittest.main()
