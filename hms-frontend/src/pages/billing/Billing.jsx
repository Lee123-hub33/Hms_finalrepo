// Fix [BUG]: missing service_type field
import { useState } from "react";
import { createBill, markPaid } from "../../api/billing";
import Input from "../../components/ui/Input";
import Button from "../../components/ui/Button";
import Card from "../../components/ui/Card";

export default function Billing() {
  const [form, setForm]       = useState({ encounter_id: "", service_type: "", amount: "" });
  const [billId, setBillId]   = useState("");
  const [error, setError]     = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const set = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }));

  const handleBill = async (e) => {
    e.preventDefault();
    setError(""); setSuccess("");
    setLoading(true);
    try {
      const res = await createBill({
        encounter_id: parseInt(form.encounter_id),
        service_type: form.service_type,
        amount:       parseFloat(form.amount),
      });
      setSuccess(`✅ Invoice #${res.data.id} created. Use that ID to mark as paid.`);
      setForm({ encounter_id: "", service_type: "", amount: "" });
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create bill.");
    } finally {
      setLoading(false);
    }
  };

  const handlePay = async (e) => {
    e.preventDefault();
    setError(""); setSuccess("");
    try {
      await markPaid(parseInt(billId));
      setSuccess(`✅ Bill #${billId} marked as Paid.`);
      setBillId("");
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to mark as paid.");
    }
  };

  return (
    <div className="p-6 max-w-lg space-y-6">
      <h1 className="text-xl font-bold text-gray-800">Billing & Payments</h1>

      <Card title="Generate Invoice">
        <form onSubmit={handleBill} className="space-y-4">
          <Input label="Encounter ID" type="number" value={form.encounter_id}
            onChange={set("encounter_id")} placeholder="From check-in" required />
          <Input label="Service Type" value={form.service_type}
            onChange={set("service_type")} placeholder="e.g. OPD Consultation" required />
          <Input label="Amount (KES)" type="number" step="0.01" value={form.amount}
            onChange={set("amount")} placeholder="e.g. 500" required />
          {error   && <p className="text-xs text-red-500">{error}</p>}
          {success && <p className="text-xs text-green-600">{success}</p>}
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? "Generating..." : "Generate Invoice"}
          </Button>
        </form>
      </Card>

      <Card title="Mark Invoice as Paid">
        <form onSubmit={handlePay} className="space-y-4">
          <Input label="Bill ID" type="number" value={billId}
            onChange={(e) => setBillId(e.target.value)}
            placeholder="ID returned when invoice was created" required />
          <Button type="submit" variant="success" className="w-full">
            Confirm Payment
          </Button>
        </form>
      </Card>
    </div>
  );
}