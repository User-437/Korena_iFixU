# Korena Pharmacy PharmaLedger — UI and account updates

Implemented:
1. Exactly three digits for newly created account codes. The seeded chart uses 100, 110, ... 550.
2. Admin-only 'Remove an unused account' in the Chart of Accounts on `/journal/new`. Removal **deactivates** an account, preserving audit history, and refuses accounts already referenced by journal lines. Removal is recorded in the audit log.
3. Show/Hide password control on login.
4. Sonner-inspired, dependency-free floating toast notifications with auto-dismiss and close button for flashed server messages. The existing server-side flash messages remain the source of truth.
5. Incorrect credentials render the login form again (HTTP 401) while keeping the entered email; password is intentionally cleared.

## Deploying to Render (not performed by this package)
- Back up PostgreSQL first.
- The current ZIP is application source, NOT a live Render deployment. Upload/deploy it using your current Render deployment method, then restart the server and verify the actual site.
- Existing database account codes remain unchanged until you run the existing `migrate_account_codes_3digit.py` migration. Review THREE_DIGIT_CODES_SETUP.md and make a backup first.
- Check signed-in admin behavior, email retention on failed login, account deactivation, account with journal lines refusal, toast behavior, mobile view, and audit integrity on the deployed instance.
- Account removal preserves rows and historic accounting relationships. Removal is limited to unused accounts by server-side validation.
- No actual passwords, keys, database dumps, or .env have been included in the package.
