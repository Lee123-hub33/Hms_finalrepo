// Fix [EMPTY]: was empty
import api from "./axios";

export const createPrescription = (data) =>
  api.post("/pharmacy/prescription", data);
export const dispensePrescription = (id) =>
  api.patch(`/pharmacy/prescription/${id}/dispense`);