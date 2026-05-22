import { useParams, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getPatient } from "../../api/patients";
import { ArrowLeft, User } from "lucide-react";

export default function PatientDetail() {
  const { id } = useParams();
  const navigate = useNavigate();

  const { data: patient, isLoading, error } = useQuery({
    queryKey: ["patient", id],
    queryFn: () => getPatient(id).then((r) => r.data),
  });

  if (isLoading) return <div className="p-6 text-gray-500">Loading patient record...</div>;
  if (error) return <div className="p-6 text-red-500">Error fetching record or patient not found.</div>;

  return (
    <div className="p-6 max-w-3xl">
      <button 
        onClick={() => navigate("/patients")} 
        className="flex items-center gap-2 text-sm text-gray-600 hover:text-blue-600 mb-4 transition"
      >
        <ArrowLeft size={16} /> Back to Patients List
      </button>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <div className="p-6 bg-gradient-to-r from-blue-900 to-blue-800 text-white flex items-center gap-4">
          <div className="bg-blue-700 p-4 rounded-full">
            <User size={32} />
          </div>
          <div>
            <h1 className="text-xl font-bold">{patient?.name}</h1>
            <p className="text-sm opacity-90">Patient ID: #{patient?.id}</p>
          </div>
        </div>

        <div className="p-6 grid grid-cols-2 gap-4 text-sm border-b">
          <div>
            <span className="block text-gray-400 font-medium uppercase text-xs">Age</span>
            <span className="text-gray-800 font-semibold text-base">{patient?.age} Years Old</span>
          </div>
          <div>
            <span className="block text-gray-400 font-medium uppercase text-xs">Biological Gender</span>
            <span className="text-gray-800 font-semibold text-base">{patient?.gender}</span>
          </div>
        </div>
      </div>
    </div>
  );
}