// Fix [EMPTY]: was empty
import { useAuth } from "../../hooks/useAuth";
import { Bell } from "lucide-react";

export default function Navbar() {
  const { user } = useAuth();
  return (
    <header className="h-14 bg-white border-b flex items-center justify-between px-6">
      <span className="text-sm text-gray-500">
        Welcome back, <span className="font-semibold text-gray-800">{user?.username}</span>
      </span>
      <div className="flex items-center gap-3">
        <button className="relative text-gray-500 hover:text-blue-600">
          <Bell size={18} />
        </button>
        <div className="w-8 h-8 rounded-full bg-blue-600 text-white text-xs
          flex items-center justify-center font-bold">
          {user?.username?.[0]?.toUpperCase()}
        </div>
      </div>
    </header>
  );
}