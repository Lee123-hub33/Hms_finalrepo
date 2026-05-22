/** Format ISO date string to readable format */
export const formatDate = (iso) => {
  if (!iso) return "—";
  return new Date(iso).toLocaleDateString("en-KE", {
    year: "numeric", month: "short", day: "numeric",
  });
};

/** Format ISO datetime */
export const formatDateTime = (iso) => {
  if (!iso) return "—";
  return new Date(iso).toLocaleString("en-KE");
};

/** Capitalise first letter */
export const capitalize = (str) =>
  str ? str.charAt(0).toUpperCase() + str.slice(1) : "";

/** Status colour mapping for badges */
export const statusColor = (status) => {
  const map = {
    Paid: "green", Unpaid: "red",
    Completed: "green", Pending: "yellow",
    Dispensed: "green", Inpatient: "blue", Outpatient: "gray",
  };
  return map[status] || "gray";
};