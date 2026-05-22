// Fix [BUG]: removed updatePatient — PATCH /patients/{id} not in backend
import api from "./axios";

export const getPatients = (skip = 0, limit = 100) =>
  api.get("/patients", { params: { skip, limit } });
export const getPatient = (id) => api.get(`/patients/${id}`);
export const createPatient = (data) => api.post("/patients", data);