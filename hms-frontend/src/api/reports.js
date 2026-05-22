import api from "./axios";

export const getMOHSummary = (date) =>
  api.get("/reports/moh-summary", { params: { target_date: date } });
export const getDailyRegistry = (date) =>
  api.get("/reports/daily-registry", { params: { target_date: date } });
export const getANCReport = (month, year) =>
  api.get("/reports/anc", { params: { month, year } });