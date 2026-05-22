import api from "./axios";

export const createBill = (data) => api.post("/billing", data);
export const markPaid = (id) => api.patch(`/billing/${id}/pay`);