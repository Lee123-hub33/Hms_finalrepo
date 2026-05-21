"""User management endpoints — admin only."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.auth import check_role
from app.database import get_db
from app.models.user import User
from app.schemas import UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["Users (Admin)"])


@router.get("", response_model=List[UserOut], dependencies=[Depends(check_role(["Admin"]))])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all users (admin only)."""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=UserOut, dependencies=[Depends(check_role(["Admin"]))])
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserOut, dependencies=[Depends(check_role(["Admin"]))])
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    """Update user (admin only) — can disable/enable accounts."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if data.is_active is not None:
        user.is_active = data.is_active
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=204, dependencies=[Depends(check_role(["Admin"]))])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete user (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
