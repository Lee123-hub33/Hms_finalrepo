// Fix [EMPTY]: was placeholder only — now fully connected to API
import { useState } from "react";
import { createPrescription, dispensePrescription } from "../../api/pharmacy";
import Input from "../../components/ui/Input";
import Button from "../../components/ui/Button";
import Card from "../../components/ui/Card";

export default function Prescriptions() {
  const [form, setForm]         = useState({ encounter_id: "", prescription_details: "" });
  const [dispenseId, setDispenseId] = useState("");
  const [error, setError]       = useState("");
  const [success, setSuccess]   = useState("");
  const [loading, setLoading]   = useState(false);

  const set = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }));

  const handlePrescribe = async (e) => {
    e.preventDefault();
    setError(""); setSuccess("");
    setLoading(true);
    try {
      const res = await createPrescription({
        encounter_id:         parseInt(form.encounter_id),
        prescription_details: form.prescription_details,
      });
      setSuccess(`✅ Prescription #${res.data.id} created. Use that ID to dispense.`);
      setForm({ encounter_id: "", prescription_details: "" });
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create prescription.");
    } finally {
      setLoading(false);
    }
  };

  const handleDispense = async (e) => {
    e.preventDefault();
    setError(""); setSuccess("");
    try {
      await dispensePrescription(parseInt(dispenseId));
      setSuccess(`✅ Prescription #${dispenseId} marked as dispensed.`);
      setDispenseId("");
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to dispense.");
    }
  };

  return (
    <div className="p-6 max-w-lg space-y-6">
      <h1 className="text-xl font-bold text-gray-800">Pharmacy</h1>

      <Card title="Create Prescription">
        <form onSubmit={handlePrescribe} className="space-y-4">
          <Input label="Encounter ID" type="number" value={form.encounter_id}
            onChange={set("encounter_id")} placeholder="From check-in" required />
          <div className="space-y-1">
            <label className="block text-xs font-semibold text-gray-600 uppercase tracking-wide">
              Prescription Details
            </label>
            <textarea value={form.prescription_details} onChange={set("prescription_details")}
              placeholder="e.g. Amoxicillin 500mg TDS x 5 days..." rows={4}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm
                focus:outline-none focus:ring-2 focus:ring-blue-400" required />
          </div>
          {error   && <p className="text-xs text-red-500">{error}</p>}
          {success && <p className="text-xs text-green-600">{success}</p>}
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? "Saving..." : "Create Prescription"}
          </Button>
        </form>
      </Card>

      <Card title="Dispense Prescription">
        <form onSubmit={handleDispense} className="space-y-4">
          <Input label="Prescription ID" type="number" value={dispenseId}
            onChange={(e) => setDispenseId(e.target.value)}
            placeholder="ID returned when prescription was created" required />
          <Button type="submit" variant="success" className="w-full">
            Mark as Dispensed
          </Button>
        </form>
      </Card>
    </div>
  );
}