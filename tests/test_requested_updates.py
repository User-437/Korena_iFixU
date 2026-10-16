"""Feature acceptance tests for five requested UI/account updates.

Run after installing requirements: python -m unittest discover -s tests -v
Uses an isolated temporary SQLite DB; never touches the production database.
"""
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from sqlalchemy import select
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from audit import ACTIONS
from accounting import AccountingError, add_account
from database import initialize
from models import Account, AuditLog, Entry, Line


class RequestedUIUpdatesTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.app = create_app({'DATABASE_URL': f'sqlite:///{self.temp.name}/test.db',
                               'TESTING': True, 'SECRET_KEY': 'test-secret'})
        self.engine = self.app.extensions['db_engine']
        self.Sessions = self.app.extensions['db_sessions']
        initialize(self.engine, self.Sessions, 'admin@korena.local', 'testing-password-123')
        self.client = self.app.test_client()

    def tearDown(self):
        self.engine.dispose()
        self.temp.cleanup()

    def csrf(self):
        with self.client.session_transaction() as sess:
            sess.setdefault('_csrf', 'test-csrf')
            return sess['_csrf']

    def login(self, password='testing-password-123'):
        return self.client.post('/login', data={'_csrf': self.csrf(),
                'email': 'admin@korena.local', 'password': password})

    def test_1_three_digit_codes_only(self):
        with self.Sessions.begin() as db:
            for account in db.scalars(select(Account)):
                self.assertRegex(account.code, r'^[0-9]{3}$')
            for code in ('23', '1234', '１２３', 'abc'):
                with self.assertRaisesRegex(AccountingError, 'exactly 3 digits'):
                    add_account(db, code, 'Test Account', 'expense')
            acc = add_account(db, '560', 'Transport Expense', 'expense')
            self.assertEqual(acc.code, '560')

    def test_2_deactivate_only_unused_accounts_and_log_action(self):
        self.login()
        response = self.client.get('/journal/new')
        self.assertIn(b'Remove an unused account', response.data)
        with self.Sessions() as db:
            unused = db.scalar(select(Account).where(Account.code == '550'))
            account_id = unused.id
        r = self.client.post(f'/journal/accounts/{account_id}/remove',
                             data={'_csrf': self.csrf()}, follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'removed from the active Chart of Accounts', r.data)
        with self.Sessions() as db:
            account = db.get(Account, account_id)
            self.assertFalse(account.active)
            self.assertIsNotNone(db.scalar(select(AuditLog).where(AuditLog.action == 'account.deactivated')))
        self.assertIn('account.deactivated', ACTIONS)
        audit_page = self.client.get('/audit')
        self.assertIn(b'account.deactivated', audit_page.data)

    def test_2_account_with_journal_entries_cannot_be_removed(self):
        self.login()
        self.client.post('/journal/new', data={
            '_csrf': self.csrf(), 'posted_on': '2026-09-01', 'reference': 'CHECK-1',
            'description': 'Cash sale', 'code': ['100', '400'],
            'debit': ['150.00', '0'], 'credit': ['0', '150.00']})
        with self.Sessions() as db:
            account_id = db.scalar(select(Account).where(Account.code == '100')).id
        r = self.client.post(f'/journal/accounts/{account_id}/remove',
                             data={'_csrf': self.csrf()}, follow_redirects=True)
        self.assertIn(b'Cannot remove this account', r.data)
        with self.Sessions() as db:
            self.assertTrue(db.get(Account, account_id).active)

    def test_3_show_password_button_on_login(self):
        page = self.client.get('/login')
        self.assertIn(b'id="toggle-password"', page.data)
        self.assertIn(b'id="login-password"', page.data)
        self.assertIn(b'ui-feedback.js', page.data)

    def test_4_notifications_and_audit_integrity_use_toasts(self):
        self.login()
        page = self.client.get('/audit?verify=1')
        self.assertIn(b'data-toast-on-load', page.data)
        self.assertIn(b'Integrity check passed', page.data)
        self.assertNotIn(b'class="flash success"', page.data)
        page = self.client.get('/journal/new')
        self.assertIn(b'window.korenaToast.error', page.data)

    def test_5_bad_password_keeps_email_and_shows_error_toast(self):
        response = self.login(password='incorrect')
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'value="admin@korena.local"', response.data)
        self.assertIn(b'Incorrect email or password.', response.data)
        self.assertIn(b'app-toast error', response.data)
        # The password value must never be placed into a rendered HTML attribute.
        self.assertNotIn(b'incorrect"', response.data)


if __name__ == '__main__':
    unittest.main()
