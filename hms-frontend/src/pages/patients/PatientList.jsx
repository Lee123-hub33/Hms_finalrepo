import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { usePatients } from "../../hooks/usePatients";
import Modal from "../../components/ui/Modal";
import PatientForm from "../../components/forms/PatientForm";
import Table from "../../components/ui/Table";
import Button from "../../components/ui/Button";
import { formatDate } from "../../utils/helpers";

const columns = [
  { key: "id",         label: "ID" },
  { key: "name",       label: "Name" },
  { key: "age",        label: "Age" },
  { key: "gender",     label: "Gender" },
  { key: "created_at", label: "Registered", render: (r) => formatDate(r.created_at) },
];

export default function PatientList() {
  const navigate         = useNavigate();
  const [open, setOpen]  = useState(false);
  const { data, isLoading } = usePatients();

  return (
    <div className="p-6 space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-xl font-bold text-gray-800">Patients</h1>
        <Button onClick={() => setOpen(true)}>+ Register Patient</Button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border">
        {isLoading ? (
          <p className="p-6 text-sm text-gray-400">Loading patients...</p>
        ) : (
          <Table
            columns={columns}
            data={data}
            onRowClick={(p) => navigate(`/patients/${p.id}`)}
          />
        )}
      </div>

      <Modal isOpen={open} onClose={() => setOpen(false)} title="Register New Patient">
        <PatientForm onSuccess={() => setOpen(false)} />
      </Modal>
    </div>
  );
}