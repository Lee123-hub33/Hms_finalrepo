// Fix [BUG]: test_name → test_requested
import { useState } from "react";
import { requestLab } from "../../api/lab";
import Input from "../../components/ui/Input";
import Button from "../../components/ui/Button";
import Card from "../../components/ui/Card";

export default function LabRequests() {
  const [form, setForm]       = useState({ encounter_id: "", test_requested: "" });
  const [error, setError]     = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const set = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(""); setSuccess("");
    setLoading(true);
    try {
      await requestLab({
        encounter_id:   parseInt(form.encounter_id),
        test_requested: form.test_requested,
      });
      setSuccess("🔬 Lab request dispatched successfully.");
      setForm({ encounter_id: "", test_requested: "" });
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to send lab request.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-md space-y-4">
      <h1 className="text-xl font-bold text-gray-800">Laboratory Requests</h1>
      <Card>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input label="Encounter ID" type="number" value={form.encounter_id}
            onChange={set("encounter_id")} placeholder="From check-in" required />
          <Input label="Test Requested" value={form.test_requested}
            onChange={set("test_requested")} placeholder="e.g. Malaria BS, CBC, LFT" required />
          {error   && <p className="text-xs text-red-500">{error}</p>}
          {success && <p className="text-xs text-green-600">{success}</p>}
          <Button type="submit" variant="warning" className="w-full" disabled={loading}>
            {loading ? "Sending..." : "Dispatch Lab Request"}
          </Button>
        </form>
      </Card>
    </div>
  );
}