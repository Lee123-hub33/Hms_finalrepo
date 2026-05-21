#!/usr/bin/env python3
"""Promote a user to Admin role."""
import sys
from app.database import SessionLocal
from app.models.user import User
from app.models.staff import Staff, RoleEnum


def main(username: str) -> None:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"User '{username}' not found")
            return

        staff = db.query(Staff).filter(Staff.user_id == user.id).first()
        if staff:
            staff.role = RoleEnum.admin
            db.add(staff)
            print(f"Updated staff id={staff.id} to Admin role")
        else:
            staff = Staff(name=username, role=RoleEnum.admin, user_id=user.id)
            db.add(staff)
            print(f"Created staff profile for {username} with Admin role")
        
        db.commit()
        print(f"User {username} is now Admin")
    finally:
        db.close()


if __name__ == '__main__':
    username = sys.argv[1] if len(sys.argv) > 1 else 'testuser'
    main(username)
