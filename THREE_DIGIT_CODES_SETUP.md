# Three-digit chart of accounts — deployment instructions

The default codes now use three digits (100 Cash on Hand, 110 Medicine Inventory, etc.). New custom accounts must use exactly three digits.

## Important: existing PostgreSQL server

1. Back up your live PostgreSQL database first. Do not skip this step.
2. Temporarily stop journal posting while migrating.
3. Keep your DATABASE_URL environment variable configured for the same PostgreSQL database (never commit it).
4. Using the OLD or NEW project source with the production DATABASE_URL, run `python migrate_account_codes_3digit.py` **once** before deploying updated application files. This changes legacy default account codes while keeping account IDs and journal entries intact. If a destination code is already in use, it stops without changes.
5. Deploy the updated code, restart the app, then verify the journal, ledger, trial balance, and audit log on the live site.

**Not a live deployment:** This ZIP only provides the updated code and migration script. The Render site remains unchanged until you deploy them.

**Audit history:** Previous audit records retain the original four-digit codes as a historical snapshot; don't rewrite historical audit logs.

**Custom account codes:** Existing user-created codes longer than three digits remain in the database to prevent breaking records. New codes must be three digits. Review legacy custom codes separately if you want to change them too.
