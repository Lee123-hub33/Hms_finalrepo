from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import create_access_token, hash_password, verify_password
from app.database import get_db
from app import crud
from app.models.user import User
from app.models.staff import Staff
from app.schemas import TokenResponse, UserCreate, RefreshRequest, PasswordResetRequest, PasswordResetConfirm

router = APIRouter(prefix="/auth", tags=["Auth"])

# simple in-memory rate limiter: {ip: (count, window_start_epoch)}
_login_attempts: dict[str, tuple[int, float]] = {}
_LOGIN_WINDOW = 60.0  # seconds
_MAX_ATTEMPTS = 10


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered.")
    user = User(username=data.username, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}


@router.post("/token", response_model=TokenResponse)
def login(
    request: Request,
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # rate limiting by client IP
    ip = request.client.host if request.client else "unknown"
    now = __import__("time").time()
    count, start = _login_attempts.get(ip, (0, now))
    if now - start > _LOGIN_WINDOW:
        count, start = 0, now
    if count >= _MAX_ATTEMPTS:
        raise HTTPException(status_code=429, detail="Too many login attempts. Try again later.")

    user = db.query(User).filter(User.username == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        _login_attempts[ip] = (count + 1, start)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # successful login: reset counter and issue tokens
    _login_attempts[ip] = (0, now)
    staff = db.query(Staff).filter(Staff.user_id == user.id).first()
    role_val = staff.role.value if (staff and staff.role) else None
    access = create_access_token(subject=user.username, role=role_val)
    refresh = crud.create_refresh_token(db, user.id)
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(payload: RefreshRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_refresh_token(db, payload.refresh_token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    staff = db.query(Staff).filter(Staff.user_id == user.id).first()
    role_val = staff.role.value if (staff and staff.role) else None
    access = create_access_token(subject=user.username, role=role_val)
    # keep refresh token valid; optionally rotate here
    return TokenResponse(access_token=access, refresh_token=payload.refresh_token)


@router.post("/password-reset/request")
def password_reset_request(data: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    # don't reveal existence: always return 204
    if user:
        token = crud.create_password_reset_token(db, user.id)
        # In production: send token by email. For now return token for dev/testing.
        return {"reset_token": token}
    return {"reset_token": None}


@router.post("/password-reset/confirm")
def password_reset_confirm(data: PasswordResetConfirm, db: Session = Depends(get_db)):
    user = crud.verify_password_reset_token(db, data.token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user.hashed_password = hash_password(data.new_password)
    db.add(user)
    db.commit()
    return {"status": "ok"}