"""One-time migration of legacy four-digit DEFAULT account codes to three digits.
Run on a backed-up database during a maintenance window, BEFORE deploying new code.
Custom account codes are left untouched; collisions cause a safe refusal.
"""
from sqlalchemy import select
from database import connect
from models import Account

MAPPING = {"1000":"100","1100":"110","1200":"120","2000":"200",
           "3000":"300","3100":"310","4000":"400","4100":"410",
           "5000":"500","5100":"510","5200":"520","5300":"530",
           "5400":"540","5500":"550"}

def main():
    engine, sessions = connect()
    with sessions.begin() as db:
        accounts = list(db.scalars(select(Account)))
        codes = {a.code for a in accounts}
        moves = {old: new for old,new in MAPPING.items() if old in codes}
        conflicts = [(old,new) for old,new in moves.items() if new in codes]
        if conflicts:
            raise RuntimeError(f'Account code collision(s): {conflicts}; database unchanged')
        # Account primary keys remain the same; existing journal lines reference account IDs.
        for a in accounts:
            if a.code in moves:
                a.code = moves[a.code]
        db.flush()
        print(f'Updated {len(moves)} default account codes. Journal lines remain linked.')
    engine.dispose()

if __name__ == '__main__':
    main()
