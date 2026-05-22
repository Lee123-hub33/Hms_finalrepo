// Fix [EMPTY]: was empty
import api from "./axios";

export const register = (data) => api.post("/auth/register", data);
export const login = (username, password) => {
  const params = new URLSearchParams();
  params.append("username", username);
  params.append("password", password);
  return api.post("/auth/token", params, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
};
export const refreshToken = (refresh_token) =>
  api.post("/auth/refresh", { refresh_token });