// Fix [EMPTY]: was empty
import { useState } from "react";
import { useCreatePatient } from "../../hooks/usePatients";
import Input from "../ui/Input";
import Button from "../ui/Button";

export default function PatientForm({ onSuccess }) {
  const [form, setForm] = useState({ name: "", age: "", gender: "Male" });
  const [error, setError] = useState("");
  const { mutateAsync, isPending } = useCreatePatient();

  const set = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await mutateAsync({ ...form, age: parseInt(form.age) });
      setForm({ name: "", age: "", gender: "Male" });
      onSuccess?.();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to register patient.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input label="Full Name" value={form.name} onChange={set("name")}
        placeholder="e.g. Jane Akinyi" required />
      <Input label="Age" type="number" value={form.age} onChange={set("age")}
        placeholder="e.g. 28" required />
      <div className="space-y-1">
        <label className="block text-xs font-semibold text-gray-600 uppercase tracking-wide">
          Gender
        </label>
        <select value={form.gender} onChange={set("gender")}
          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm
            focus:outline-none focus:ring-2 focus:ring-blue-400">
          <option>Male</option>
          <option>Female</option>
          <option>Other</option>
        </select>
      </div>
      {error && <p className="text-xs text-red-500">{error}</p>}
      <Button type="submit" variant="primary" disabled={isPending} className="w-full">
        {isPending ? "Saving..." : "Register Patient"}
      </Button>
    </form>
  );
}