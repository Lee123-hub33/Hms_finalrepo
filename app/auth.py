"""
JWT authentication helpers and RBAC dependency.

SECRET_KEY and token expiry come from app.config — never hardcoded.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, List

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models.staff import Staff
from app.models.user import User

settings = get_settings()

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "bcrypt"],
    deprecated="auto",
)
bearer_scheme = HTTPBearer(auto_error=False)


# ── Password helpers ──────────────────────────────────────────────────────────

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(plain, hashed)
    except Exception:
        return False


# ── Token helpers ─────────────────────────────────────────────────────────────

def create_access_token(subject: str) -> str:
    expire  = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


# ── FastAPI dependencies ──────────────────────────────────────────────────────

def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise credentials_exc

    token = credentials.credentials
    try:
        payload: dict[str, Any] = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        sub = payload.get("sub")
        if not isinstance(sub, str):
            raise credentials_exc
        username: str = sub
    except JWTError:
        raise credentials_exc

    user = db.query(User).filter(User.username == username).first()
    if user is None or not user.is_active:
        raise credentials_exc
    return user


def get_current_staff(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Staff:
    staff = db.query(Staff).filter(Staff.user_id == current_user.id).first()
    if staff is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No staff profile associated with this account.",
        )
    return staff


def check_role(required_roles: List[str]):
    """
    RBAC dependency factory.
    Usage: dependencies=[Depends(check_role(["Admin", "Doctor"]))]
    """
    def _checker(staff: Staff = Depends(get_current_staff)) -> Staff:
        role_value = (
            staff.role.value if hasattr(staff.role, "value") else str(staff.role)
        )
        if role_value not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {required_roles}.",
            )
        return staff
    return _checker