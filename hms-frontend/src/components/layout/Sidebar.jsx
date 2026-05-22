import { NavLink } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import {
  Users, UserPlus, ClipboardList, Activity,
  FlaskConical, Pill, Receipt, BarChart3, LogOut, Home
} from "lucide-react";

const links = [
  { to: "/", label: "Dashboard", icon: Home },
  { to: "/patients", label: "Patients", icon: Users },
  { to: "/registry", label: "Check In", icon: UserPlus },
  { to: "/clinical/vitals", label: "Vitals", icon: Activity },
  { to: "/clinical/consultation", label: "Consultation", icon: ClipboardList },
  { to: "/lab", label: "Laboratory", icon: FlaskConical },
  { to: "/pharmacy", label: "Pharmacy", icon: Pill },
  { to: "/billing", label: "Billing", icon: Receipt },
  { to: "/reports", label: "Reports", icon: BarChart3 },
];

export default function Sidebar() {
  const { logout } = useAuth();

  return (
    <aside className="w-64 bg-blue-900 text-white min-h-screen flex flex-col">
      <div className="p-6 text-xl font-bold border-b border-blue-700">
        🏥 HMS
      </div>
      <nav className="flex-1 p-4 space-y-1">
        {links.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            end={to === "/"}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition
              ${isActive ? "bg-blue-600" : "hover:bg-blue-800"}`
            }
          >
            <Icon size={16} />
            {label}
          </NavLink>
        ))}
      </nav>
      <button
        onClick={logout}
        className="flex items-center gap-3 px-7 py-4 text-sm hover:bg-blue-800"
      >
        <LogOut size={16} /> Logout
      </button>
    </aside>
  );
}