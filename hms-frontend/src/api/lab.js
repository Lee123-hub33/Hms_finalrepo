import api from "./axios";

export const requestLab = (data) => api.post("/lab", data);
export const enterResults = (id, data) => api.patch(`/lab/${id}/results`, data);