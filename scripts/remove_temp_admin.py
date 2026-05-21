#!/usr/bin/env python3
"""Remove the temporary admin user and related staff/refresh tokens."""
from app.database import SessionLocal
from app.models.user import User
from app.models.staff import Staff
from app.models.refresh_token import RefreshToken


def main(username: str = "temp_admin") -> None:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"No user found with username '{username}'")
            return

        refreshed = db.query(RefreshToken).filter(RefreshToken.user_id == user.id).all()
        if refreshed:
            print(f"Deleting {len(refreshed)} refresh/password-reset token(s)")
            for rt in refreshed:
                db.delete(rt)

        staff = db.query(Staff).filter(Staff.user_id == user.id).all()
        if staff:
            print(f"Deleting {len(staff)} staff record(s)")
            for s in staff:
                db.delete(s)

        print(f"Deleting user id={user.id} username={user.username}")
        db.delete(user)
        db.commit()
        print("Temporary admin account removed.")
    finally:
        db.close()


if __name__ == '__main__':
    main()
