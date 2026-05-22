// Fix [EMPTY]: was empty
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getPatients, getPatient, createPatient } from "../api/patients";

export function usePatients() {
  return useQuery({
    queryKey: ["patients"],
    queryFn: () => getPatients().then((r) => r.data),
  });
}

export function usePatient(id) {
  return useQuery({
    queryKey: ["patient", id],
    queryFn: () => getPatient(id).then((r) => r.data),
    enabled: !!id,
  });
}

export function useCreatePatient() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: createPatient,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["patients"] }),
  });
}