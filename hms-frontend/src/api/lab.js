import api from "./axios";

export const requestLab = (data) => api.post("/lab", data);
export const enterResults = (id, data) => api.patch(`/lab/${id}/results`, data);
export const getLabRequests = (params) => api.get("/lab", { params });
export const getLabRequestsByEncounter = (encounterId) => api.get(`/lab/encounter/${encounterId}`);