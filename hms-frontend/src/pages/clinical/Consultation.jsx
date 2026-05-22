// Fix [BUG]: notes → clinical_notes
import { useState } from "react";
import ConsultationForm from "../../components/forms/ConsultationForm";
import Input from "../../components/ui/Input";
import Card from "../../components/ui/Card";

export default function Consultation() {
  const [encounterId, setEncounterId] = useState("");
  const [confirmed, setConfirmed]     = useState(false);
  const [submitted, setSubmitted]     = useState(false);

  return (
    <div className="p-6 max-w-lg space-y-4">
      <h1 className="text-xl font-bold text-gray-800">Physician Consultation</h1>

      {!confirmed ? (
        <Card title="Enter Encounter ID">
          <div className="space-y-3">
            <Input label="Encounter ID" type="number" value={encounterId}
              onChange={(e) => setEncounterId(e.target.value)} placeholder="From check-in" />
            <button onClick={() => encounterId && setConfirmed(true)}
              className="w-full bg-blue-700 text-white rounded-lg py-2 text-sm font-medium">
              Continue
            </button>
          </div>
        </Card>
      ) : submitted ? (
        <Card>
          <p className="text-center text-green-700 font-semibold">
            ✅ Consultation saved for Encounter #{encounterId}
          </p>
          <button onClick={() => { setSubmitted(false); setConfirmed(false); setEncounterId(""); }}
            className="mt-3 w-full text-sm text-blue-600 hover:underline">
            New consultation
          </button>
        </Card>
      ) : (
        <Card title={`Consultation — Encounter #${encounterId}`}>
          <ConsultationForm encounterId={encounterId} onSuccess={() => setSubmitted(true)} />
        </Card>
      )}
    </div>
  );
}