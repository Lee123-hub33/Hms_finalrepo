import api from "./axios";

export const addVitals = (data) => api.patch("/clinical/vitals", data);
export const addConsultation = (data) => api.post("/clinical/consultation", data);
export const addANC = (data) => api.post("/clinical/anc", data);