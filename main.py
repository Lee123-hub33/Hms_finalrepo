"""
Application entry point.

Wires all routers, configures CORS, and registers a global exception handler
so internal errors never leak stack traces to clients.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import app.models  # noqa: F401 — registers all tables with Base.metadata
from app.config import get_settings
from app.database import Base, engine
from app.routers import (
    auth,
    billing,
    clinical,
    doctor,
    inventory,
    lab,
    patients,
    pharmacy,
    procedure,
    registry,
    reports,
    staff,
    users,
    ward,
)

settings = get_settings()


# ── Lifespan (startup / shutdown) ─────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup — create any missing tables (use Alembic for migrations in prod)
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown — nothing to clean up; SQLAlchemy pool handles connections


# ── App factory ───────────────────────────────────────────────────────────────

app = FastAPI(
    title="Hospital Management System",
    description=(
        "MoH-compliant HMS with encounter-anchored clinical data, "
        "role-based access control, and reporting."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# ── CORS ──────────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,   # set in .env, not hardcoded
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Global exception handler ──────────────────────────────────────────────────

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """
    Catches any unhandled exception and returns a clean 500 JSON response.
    Stack traces are logged server-side but never sent to the client.
    """
    import logging
    logging.getLogger("uvicorn.error").exception("Unhandled error: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred."},
    )


# ── Routers ───────────────────────────────────────────────────────────────────

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(patients.router)
app.include_router(doctor.router)
app.include_router(staff.router)
app.include_router(ward.router)
app.include_router(registry.router)
app.include_router(clinical.router)
app.include_router(lab.router)
app.include_router(pharmacy.router)
app.include_router(procedure.router)
app.include_router(inventory.router)
app.include_router(billing.router)
app.include_router(reports.router)


# ── Health check ──────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def health_check() -> dict:
    return {
        "status": "online",
        "system": "HMS v1.0.0",
        "environment": settings.app_env,
    }