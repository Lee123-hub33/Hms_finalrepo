// Fix [BUG]: bp → blood_pressure
import { useState } from "react";
import VitalsForm from "../../components/forms/VitalsForm";
import Input from "../../components/ui/Input";
import Card from "../../components/ui/Card";

export default function Vitals() {
  const [encounterId, setEncounterId] = useState("");
  const [submitted, setSubmitted]     = useState(false);
  const [confirmed, setConfirmed]     = useState(false);

  return (
    <div className="p-6 max-w-lg space-y-4">
      <h1 className="text-xl font-bold text-gray-800">Record Vitals</h1>

      {!confirmed ? (
        <Card title="Enter Encounter ID">
          <div className="space-y-3">
            <Input label="Encounter ID" type="number" value={encounterId}
              onChange={(e) => setEncounterId(e.target.value)}
              placeholder="From check-in" required />
            <button onClick={() => encounterId && setConfirmed(true)}
              className="w-full bg-blue-600 text-white rounded-lg py-2 text-sm font-medium">
              Continue
            </button>
          </div>
        </Card>
      ) : submitted ? (
        <Card>
          <p className="text-center text-green-700 font-semibold">
            ✅ Vitals saved for Encounter #{encounterId}
          </p>
          <button onClick={() => { setSubmitted(false); setConfirmed(false); setEncounterId(""); }}
            className="mt-3 w-full text-sm text-blue-600 hover:underline">
            Record for another encounter
          </button>
        </Card>
      ) : (
        <Card title={`Vitals — Encounter #${encounterId}`}>
          <VitalsForm encounterId={encounterId} onSuccess={() => setSubmitted(true)} />
        </Card>
      )}
    </div>
  );
}