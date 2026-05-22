import api from "./axios";

export const checkIn = (data) => api.post("/registry/check-in", data);
export const getEncounter = (id) => api.get(`/registry/${id}`);
export const getPatientEncounters = (patientId) =>
  api.get(`/registry/patient/${patientId}`);