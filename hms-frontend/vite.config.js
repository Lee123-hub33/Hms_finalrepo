import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      "/auth":      { target: "http://localhost:8000", changeOrigin: true },
      "/users":     { target: "http://localhost:8000", changeOrigin: true },
      "/patients":  { target: "http://localhost:8000", changeOrigin: true },
      "/encounters":{ target: "http://localhost:8000", changeOrigin: true },
      "/clinical":  { target: "http://localhost:8000", changeOrigin: true },
      "/vitals":    { target: "http://localhost:8000", changeOrigin: true },
      "/lab":       { target: "http://localhost:8000", changeOrigin: true },
      "/pharmacy":  { target: "http://localhost:8000", changeOrigin: true },
      "/billing":   { target: "http://localhost:8000", changeOrigin: true },
      "/reports":   { target: "http://localhost:8000", changeOrigin: true },
      "/wards":     { target: "http://localhost:8000", changeOrigin: true },
      "/registry":  { target: "http://localhost:8000", changeOrigin: true },
      "/staff":     { target: "http://localhost:8000", changeOrigin: true },
      "/doctors":   { target: "http://localhost:8000", changeOrigin: true },
      "/inventory": { target: "http://localhost:8000", changeOrigin: true },
      "/procedure": { target: "http://localhost:8000", changeOrigin: true },
    },
  },
});