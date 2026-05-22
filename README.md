# Westhills Hospital Management System - Backend API

A robust, production-ready backend REST API built to handle clinical registries, patient records, and doctor-encounter workflows. This system leverages structured SQLAlchemy models to enforce data integrity and implements strict Role-Based Access Control (RBAC) to secure sensitive healthcare data.

## 🚀 Tech Stack

- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL
- **Database Communication:** SQLAlchemy ORM
- **Security:** JWT (JSON Web Tokens), Passlib (Bcrypt hashing)
- **Server:** Uvicorn

## 🔐 Security & Access Control

The API implements an industry-standard security architecture to ensure HIPAA-compliant data isolation and user accountability.

### 1. Authentication
- **Mechanism:** OAuth2 with Password Bearer flow and **JWT (JSON Web Tokens)**.
- **Password Safety:** Raw passwords are never stored. All credentials undergo **Bcrypt** hashing via `passlib` before hitting the database.
- **Session Management:** Users authenticate at the `/auth/login` endpoint to receive a secure access token with a configurable expiration time.

### 2. Authorization & RBAC (Role-Based Access Control)
Access to resources is strictly gated based on the authenticated user's assigned role. The system enforces the principle of least privilege through custom FastAPI dependencies:

| Role | Permissions / Access Level |
| :--- | :--- |
| **Admin** | Full system access, staff management, audit logs, and system configurations. |
| **Doctor** | Read/Write access to clinical encounters, patient medical histories, and prescriptions. |
| **Nurse** | Read access to patient files, Write access to vitals, ward assignments, and triaging. |
| **Staff / Receptionist** | Patient registration, scheduling, and billing management. No access to clinical notes. |

*Example:* Endpoints like `POST /patients` or `DELETE /users` utilize a `RoleChecker(["Admin", "Doctor"])` dependency that intercepts requests, decodes the JWT payload, and raises a `403 Forbidden` error if the user lacks sufficient clearance.

## 🛠️ Core Features

- **Relational Patient Registries:** Structured management of patient demographics, clinical profiles, and medical histories.
- **Encounter Tracking:** Maps distinct clinical encounters dynamically between specific patients and medical personnel using relational models.
- **Inventory & Pharmacy Management:** Tracks medication stock levels, ward allocations, and dispenses prescriptions securely linked to clinician orders.
- **Async Database Operations:** Leverages asynchronous database queries to efficiently handle concurrent API requests.
- **Auto-generated Documentation:** Interactive API exploration via Swagger UI and ReDoc.

## 📦 Local Setup & Installation

### Prerequisites
- Python 3.10 or higher
- A running PostgreSQL instance

### Step-by-Step Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Lee123-hub33/Hms_finalrepo.git](https://github.com/Lee123-hub33/Hms_finalrepo.git)
   cd Hms_finalrepo
   