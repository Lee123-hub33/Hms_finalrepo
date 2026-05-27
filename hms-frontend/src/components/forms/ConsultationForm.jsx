// Fix [EMPTY]: was empty
// Fix [BUG]: field was notes — backend expects clinical_notes
import { useState } from "react";
import { addConsultation } from "../../api/clinical";
import { requestLab } from "../../api/lab";
import Input from "../ui/Input";
import Button from "../ui/Button";

export default function ConsultationForm({ encounterId, onSuccess }) {
  const [form, setForm] = useState({
    chief_complaint: "", clinical_notes: "", diagnosis: "",
  });
  const [labTest, setLabTest] = useState("");
  const [error, setError]   = useState("");
  const [loading, setLoading] = useState(false);

  const set = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await addConsultation({ encounter_id: parseInt(encounterId), ...form });
      
      if (labTest.trim()) {
        await requestLab({
          encounter_id: parseInt(encounterId),
          test_requested: labTest.trim()
        });
      }

      onSuccess?.();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to save consultation.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input label="Chief Complaint" value={form.chief_complaint}
        onChange={set("chief_complaint")} placeholder="e.g. Fever and headache" required />
      <div className="space-y-1">
        <label className="block text-xs font-semibold text-gray-600 uppercase tracking-wide">
          Clinical Notes
        </label>
        <textarea value={form.clinical_notes} onChange={set("clinical_notes")}
          placeholder="Detailed clinical evaluation..." rows={4}
          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm
            focus:outline-none focus:ring-2 focus:ring-blue-400" />
      </div>
      <Input label="Diagnosis" value={form.diagnosis} onChange={set("diagnosis")}
        placeholder="e.g. Malaria (ICD: B50)" required />
      
      <div className="pt-4 border-t border-gray-100">
        <Input 
          label="Request Lab Test (Optional)" 
          value={labTest} 
          onChange={(e) => setLabTest(e.target.value)}
          placeholder="e.g. Full Blood Count, Malaria Parasites" 
        />
      </div>

      {error && <p className="text-xs text-red-500">{error}</p>}
      <Button type="submit" variant="primary" disabled={loading} className="w-full">
        {loading ? "Saving..." : "Save Consultation & Request Lab"}
      </Button>
    </form>
  );
}