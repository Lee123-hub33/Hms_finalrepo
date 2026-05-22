// Fix [BUG]: removed reason field, added visit_type, patient_status, triage_level
import { useState } from "react";
import { checkIn } from "../../api/encounters";
import Input from "../../components/ui/Input";
import Button from "../../components/ui/Button";
import Card from "../../components/ui/Card";

export default function CheckIn() {
  const [form, setForm] = useState({
    patient_id: "", visit_type: "OPD",
    patient_status: "Outpatient", triage_level: "Normal", ward_id: "",
  });
  const [result, setResult]   = useState(null);
  const [error, setError]     = useState("");
  const [loading, setLoading] = useState(false);

  const set = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const payload = {
        patient_id:     parseInt(form.patient_id),
        visit_type:     form.visit_type,
        patient_status: form.patient_status,
        triage_level:   form.triage_level,
        ward_id:        form.ward_id ? parseInt(form.ward_id) : null,
      };
      const res = await checkIn(payload);
      setResult(res.data);
      setForm({ patient_id: "", visit_type: "OPD",
        patient_status: "Outpatient", triage_level: "Normal", ward_id: "" });
    } catch (err) {
      setError(err.response?.data?.detail || "Check-in failed.");
    } finally {
      setLoading(false);
    }
  };

  const Select = ({ label, field, options }) => (
    <div className="space-y-1">
      <label className="block text-xs font-semibold text-gray-600 uppercase tracking-wide">
        {label}
      </label>
      <select value={form[field]} onChange={set(field)}
        className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm
          focus:outline-none focus:ring-2 focus:ring-blue-400">
        {options.map((o) => <option key={o}>{o}</option>)}
      </select>
    </div>
  );

  return (
    <div className="p-6 max-w-lg space-y-4">
      <h1 className="text-xl font-bold text-gray-800">Patient Check-In</h1>

      <Card>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input label="Patient ID" type="number" value={form.patient_id}
            onChange={set("patient_id")} placeholder="e.g. 1" required />
          <Select label="Visit Type" field="visit_type"
            options={["OPD", "ANC", "Emergency"]} />
          <Select label="Patient Status" field="patient_status"
            options={["Outpatient", "Inpatient"]} />
          <Select label="Triage Level" field="triage_level"
            options={["Normal", "Urgent", "Emergency"]} />
          <Input label="Ward ID (optional — inpatients only)" type="number"
            value={form.ward_id} onChange={set("ward_id")} placeholder="Leave blank if OPD" />
          {error && <p className="text-xs text-red-500 bg-red-50 px-3 py-2 rounded">{error}</p>}
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? "Checking in..." : "Confirm Check-In"}
          </Button>
        </form>
      </Card>

      {result && (
        <Card title="✅ Check-In Successful — Save this Encounter ID">
          <div className="text-center">
            <p className="text-4xl font-bold text-blue-700">{result.id}</p>
            <p className="text-xs text-gray-500 mt-1">Encounter ID</p>
          </div>
          <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
            <div><span className="text-gray-400">Visit Type</span>
              <p className="font-medium">{result.visit_type}</p></div>
            <div><span className="text-gray-400">Status</span>
              <p className="font-medium">{result.patient_status}</p></div>
            <div><span className="text-gray-400">Triage</span>
              <p className="font-medium">{result.triage_level}</p></div>
            <div><span className="text-gray-400">Time</span>
              <p className="font-medium">{new Date(result.created_at).toLocaleTimeString()}</p></div>
          </div>
        </Card>
      )}
    </div>
  );
}