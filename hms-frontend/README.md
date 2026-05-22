# Westhills HMS - Frontend Application

This is the responsive single-page application (SPA) client interface for the Westhills Hospital Management System. It provides dedicated modules for triage counters, clinical evaluation logs, laboratory requests, and hospital billing administration.

## 🛠️ Frontend Tech Stack

- **Core Engine:** React 18+ bundled via **Vite** (for blazing fast HMR compilation)
- **Styling UI:** **Tailwind CSS** (Utility-first responsive architecture)
- **State Management & Caching:** **React Query (TanStack Query)** for robust backend server-state synchronization
- **Routing Engine:** **React Router DOM v6** (Protected workflow authentication gates)
- **API Communication Client:** **Axios** (Configured with dynamic request interceptors for automated JWT Bearer authorization)
- **Icon Assets:** **Lucide React**

## 📂 Key Architecture Modules

- `src/context/AuthContext.jsx`: Intercepts system logins, handles form parameter parsing for backend authentication, and coordinates master state tracking.
- `src/pages/patients/`: Patient Registration lists and comprehensive history files.
- `src/pages/registry/CheckIn.jsx`: Triage station entry forms to initialize clinical encounters.
- `src/pages/clinical/`: Dual components for nursing vital signs logging and physician consultation records.
- `src/pages/lab/` & `src/pages/billing/`: Department interfaces matching lab orders and invoice calculations.

## 🚀 Quick Local Development Boot

Ensure your backend application engine is running concurrently on port `8000`.

1. **Navigate to the directory:**
   ```powershell
   cd hms-frontend