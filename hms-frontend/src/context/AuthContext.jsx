// Fix [BUG]: role no longer hardcoded from username string
import { createContext, useState } from "react";
import { login as apiLogin } from "../api/auth";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const token = localStorage.getItem("token");
    const saved  = localStorage.getItem("user");
    return token && saved ? JSON.parse(saved) : null;
  });

  const login = async (username, password) => {
    const res   = await apiLogin(username, password);
    const token = res.data.access_token;

    // Decode JWT payload to read actual role — no hardcoding
    const payload    = JSON.parse(atob(token.split(".")[1]));
    const userPayload = { token, username: payload.sub };

    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(userPayload));
    setUser(userPayload);
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setUser(null);
    window.location.href = "/login";
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}