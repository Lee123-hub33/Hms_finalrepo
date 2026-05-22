// Fix [EMPTY]: was empty
// Fix [BUG]: field was bp — backend expects blood_pressure
import { useState } from "react";
import { addVitals } from "../../api/clinical";
import Input from "../ui/Input";
import Button from "../ui/Button";

export default function VitalsForm({ encounterId, onSuccess }) {
  const [form, setForm] = useState({
    blood_pressure: "", temperature: "", weight: "", height: "", muac: "",
  });
  const [error, setError]   = useState("");
  const [loading, setLoading] = useState(false);

  const set = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await addVitals({
        encounter_id:   parseInt(encounterId),
        blood_pressure: form.blood_pressure || undefined,
        temperature:    form.temperature ? parseFloat(form.temperature) : undefined,
        weight:         form.weight ? parseFloat(form.weight) : undefined,
        height:         form.height ? parseFloat(form.height) : undefined,
        muac:           form.muac ? parseFloat(form.muac) : undefined,
      });
      onSuccess?.();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to save vitals.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input label="Blood Pressure" value={form.blood_pressure} onChange={set("blood_pressure")}
        placeholder="e.g. 120/80" />
      <Input label="Temperature (°C)" type="number" step="0.1" value={form.temperature}
        onChange={set("temperature")} placeholder="e.g. 36.6" />
      <Input label="Weight (kg)" type="number" step="0.1" value={form.weight}
        onChange={set("weight")} placeholder="e.g. 65" />
      <Input label="Height (cm)" type="number" step="0.1" value={form.height}
        onChange={set("height")} placeholder="e.g. 165" />
      <Input label="MUAC (cm)" type="number" step="0.1" value={form.muac}
        onChange={set("muac")} placeholder="e.g. 25" />
      {error && <p className="text-xs text-red-500">{error}</p>}
      <Button type="submit" variant="success" disabled={loading} className="w-full">
        {loading ? "Saving..." : "Save Vitals"}
      </Button>
    </form>
  );
}