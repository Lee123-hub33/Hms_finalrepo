"""One-off helper: create a temporary Admin user and print an access token.

Usage (from project root):
    python scripts/create_temp_admin.py --username admin --password secret123

The script writes to the configured database. Remove the account manually after testing.
"""
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import argparse
from app.database import SessionLocal
from app.models.user import User
from app.models.staff import Staff, RoleEnum
from app.auth import hash_password, create_access_token


def main(username: str, password: str, name: str = "Temp Admin") -> None:
    db = SessionLocal()
    try:
        # check existing
        existing = db.query(User).filter(User.username == username).first()
        if existing:
            print(f"User '{username}' already exists (id={existing.id}). Updating password hash.")
            existing.hashed_password = hash_password(password)
            db.add(existing)
            db.commit()
            db.refresh(existing)
            user = existing
        else:
            user = User(username=username, hashed_password=hash_password(password))
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"Created user id={user.id} username={user.username}")

        staff = db.query(Staff).filter(Staff.user_id == user.id).first()
        if staff:
            print(f"Staff profile already exists (id={staff.id}, role={staff.role}).")
        else:
            staff = Staff(name=name, role=RoleEnum.admin, user_id=user.id)
            db.add(staff)
            db.commit()
            db.refresh(staff)
            print(f"Created staff id={staff.id} role={staff.role}")

        token = create_access_token(user.username)
        print("\nUse this Authorization header in requests:")
        print(f"Authorization: Bearer {token}\n")
        print("Example curl:")
        print(f"curl -H \"Authorization: Bearer {token}\" -H 'Content-Type: application/json' -d '{'{"ward_name":"Test","capacity":5}'}' http://localhost:8000/wards")
    finally:
        db.close()


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("--username", default="admin", help="Username for temp admin")
    p.add_argument("--password", default="adminpass", help="Password for temp admin")
    p.add_argument("--name", default="Temporary Admin", help="Staff name")
    args = p.parse_args()
    main(args.username, args.password, args.name)
