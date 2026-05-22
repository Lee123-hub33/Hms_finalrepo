// Fix [MISSING]
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "./hooks/useAuth";
import Layout       from "./components/layout/Layout";
import Login        from "./pages/Login";
import Dashboard    from "./pages/Dashboard";
import PatientList  from "./pages/patients/PatientList";
import PatientDetail from "./pages/patients/PatientDetail";
import CheckIn      from "./pages/registry/CheckIn";
import Vitals       from "./pages/clinical/Vitals";
import Consultation from "./pages/clinical/Consultation";
import LabRequests  from "./pages/lab/LabRequests";
import Prescriptions from "./pages/pharmacy/Prescriptions";
import Billing      from "./pages/billing/Billing";
import Reports      from "./pages/reports/Reports";

function ProtectedRoute({ children }) {
  const { user } = useAuth();
  return user ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index              element={<Dashboard />} />
          <Route path="patients"    element={<PatientList />} />
          <Route path="patients/:id" element={<PatientDetail />} />
          <Route path="registry"    element={<CheckIn />} />
          <Route path="clinical/vitals"       element={<Vitals />} />
          <Route path="clinical/consultation" element={<Consultation />} />
          <Route path="lab"         element={<LabRequests />} />
          <Route path="pharmacy"    element={<Prescriptions />} />
          <Route path="billing"     element={<Billing />} />
          <Route path="reports"     element={<Reports />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}