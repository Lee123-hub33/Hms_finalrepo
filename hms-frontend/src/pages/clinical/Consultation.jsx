import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import ConsultationForm from "../../components/forms/ConsultationForm";
import Input from "../../components/ui/Input";
import Card from "../../components/ui/Card";
import Button from "../../components/ui/Button";
import Badge from "../../components/ui/Badge";
import { getVitals } from "../../api/clinical";
import { getLabRequestsByEncounter, requestLab } from "../../api/lab";
import { Activity, FlaskConical, Plus, Clipboard, Clock, CheckCircle2 } from "lucide-react";

export default function Consultation() {
  const [encounterId, setEncounterId] = useState("");
  const [confirmed, setConfirmed]     = useState(false);
  const [submitted, setSubmitted]     = useState(false);
  const queryClient = useQueryClient();

  // Quick lab order state
  const [newTestName, setNewTestName] = useState("");
  const [labError, setLabError]       = useState("");
  const [labSuccess, setLabSuccess]   = useState("");

  // Fetch Patient Vitals for the current encounter
  const { data: vitals, isLoading: loadingVitals } = useQuery({
    queryKey: ["vitals", encounterId],
    queryFn: () => getVitals(encounterId).then((r) => r.data),
    enabled: confirmed && !!encounterId,
    retry: false, // If no vitals recorded yet
  });

  // Fetch Lab Requests for this encounter
  const { data: labRequests, isLoading: loadingLab } = useQuery({
    queryKey: ["encounter-labs", encounterId],
    queryFn: () => getLabRequestsByEncounter(encounterId).then((r) => r.data),
    enabled: confirmed && !!encounterId,
  });

  // Quick lab request mutation
  const requestMutation = useMutation({
    mutationFn: requestLab,
    onSuccess: () => {
      setNewTestName("");
      setLabSuccess("🔬 Lab test ordered successfully.");
      queryClient.invalidateQueries({ queryKey: ["encounter-labs", encounterId] });
      setTimeout(() => setLabSuccess(""), 4000);
    },
    onError: (err) => {
      setLabError(err.response?.data?.detail || "Failed to order lab test.");
      setTimeout(() => setLabError(""), 4000);
    },
  });

  const handleOrderLab = (e) => {
    e.preventDefault();
    setLabError("");
    setLabSuccess("");
    if (!newTestName.trim()) {
      setLabError("Please specify a test name.");
      return;
    }
    requestMutation.mutate({
      encounter_id: parseInt(encounterId),
      test_requested: newTestName,
    });
  };

  return (
    <div className={`p-6 mx-auto space-y-6 ${confirmed ? "max-w-6xl" : "max-w-lg"}`}>
      <div className="flex justify-between items-center border-b pb-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
            <Clipboard className="text-slate-900" size={24} />
            Physician Consultation Room
          </h1>
          {confirmed && <p className="text-sm text-gray-500">Conducting evaluation for Encounter #{encounterId}</p>}
        </div>
      </div>

      {!confirmed ? (
        <Card title="Enter Encounter ID" className="shadow-md">
          <div className="space-y-4">
            <p className="text-sm text-gray-500">
              Enter the patient's Encounter ID from the triage or check-in queue to load their record.
            </p>
            <div className="space-y-3">
              <Input
                label="Encounter ID"
                type="number"
                value={encounterId}
                onChange={(e) => setEncounterId(e.target.value)}
                placeholder="e.g. 1001"
              />
              <button
                onClick={() => encounterId && setConfirmed(true)}
                className="w-full bg-slate-900 hover:bg-slate-800 text-white rounded-lg py-2.5 text-sm font-medium transition shadow-sm"
              >
                Continue to Consultation
              </button>
            </div>
          </div>
        </Card>
      ) : submitted ? (
        <Card className="max-w-md mx-auto text-center shadow-lg py-8 space-y-4">
          <div className="text-5xl">✅</div>
          <h3 className="text-lg font-bold text-green-800">Consultation Completed</h3>
          <p className="text-sm text-gray-600">
            Diagnosis and clinical evaluation notes have been saved successfully for Encounter #{encounterId}.
          </p>
          <Button
            variant="primary"
            onClick={() => {
              setSubmitted(false);
              setConfirmed(false);
              setEncounterId("");
            }}
            className="w-full"
          >
            Start New Consultation
          </Button>
        </Card>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Column: Vitals and Consultation Form (Span 7) */}
          <div className="lg:col-span-7 space-y-6">
            {/* Vitals Summary Card */}
            <Card className="shadow-sm border-l-4 border-l-slate-900">
              <div className="flex items-center justify-between mb-3 border-b pb-2">
                <h3 className="font-bold text-gray-800 flex items-center gap-1.5 text-sm">
                  <Activity className="text-slate-900" size={16} />
                  Patient Vitals
                </h3>
                {vitals?.recorded_at && (
                  <span className="text-xs text-gray-400">
                    Recorded {new Date(vitals.recorded_at).toLocaleTimeString()}
                  </span>
                )}
              </div>

              {loadingVitals ? (
                <p className="text-xs text-gray-400">Loading vitals...</p>
              ) : vitals ? (
                <div className="grid grid-cols-3 sm:grid-cols-5 gap-3 text-center">
                  <div className="bg-gray-50 p-2.5 rounded-lg border border-gray-100">
                    <p className="text-xs text-gray-500 font-medium">Temp</p>
                    <p className="text-sm font-bold text-gray-700">{vitals.temperature ?? "—"}°C</p>
                  </div>
                  <div className="bg-gray-50 p-2.5 rounded-lg border border-gray-100">
                    <p className="text-xs text-gray-500 font-medium">BP</p>
                    <p className="text-sm font-bold text-gray-700">{vitals.blood_pressure ?? "—"}</p>
                  </div>
                  <div className="bg-gray-50 p-2.5 rounded-lg border border-gray-100">
                    <p className="text-xs text-gray-500 font-medium">Weight</p>
                    <p className="text-sm font-bold text-gray-700">{vitals.weight ?? "—"} kg</p>
                  </div>
                  <div className="bg-gray-50 p-2.5 rounded-lg border border-gray-100">
                    <p className="text-xs text-gray-500 font-medium">Height</p>
                    <p className="text-sm font-bold text-gray-700">{vitals.height ?? "—"} cm</p>
                  </div>
                  <div className="bg-gray-50 p-2.5 rounded-lg border border-gray-100 col-span-3 sm:col-span-1">
                    <p className="text-xs text-gray-500 font-medium">MUAC</p>
                    <p className="text-sm font-bold text-gray-700">{vitals.muac ?? "—"} cm</p>
                  </div>
                </div>
              ) : (
                <p className="text-xs text-amber-600 bg-amber-50 p-2 rounded-lg">
                  ⚠️ No triage vitals recorded for this encounter yet.
                </p>
              )}
            </Card>

            {/* Consultation Details Card */}
            <Card title={`Consultation Diagnosis & Notes`} className="shadow-md">
              <ConsultationForm encounterId={encounterId} onSuccess={() => setSubmitted(true)} />
            </Card>
          </div>

          {/* Right Column: Lab Integration Panel (Span 5) */}
          <div className="lg:col-span-5 space-y-6">
            <Card className="shadow-md">
              <div className="flex items-center justify-between mb-4 border-b pb-2">
                <h3 className="font-bold text-gray-800 flex items-center gap-1.5 text-sm uppercase tracking-wide">
                  <FlaskConical className="text-purple-600" size={16} />
                  Laboratory Requests
                </h3>
                <Badge label={`${labRequests?.length || 0} Ordered`} color="blue" />
              </div>

              {/* Lab Request List */}
              <div className="space-y-3 max-h-[350px] overflow-y-auto pr-1">
                {loadingLab ? (
                  <p className="text-xs text-gray-400 text-center py-4">Loading lab requests...</p>
                ) : labRequests && labRequests.length > 0 ? (
                  labRequests.map((lab) => (
                    <div
                      key={lab.id}
                      className={`p-3.5 rounded-xl border transition ${
                        lab.status === "Completed"
                          ? "bg-emerald-50/40 border-emerald-100"
                          : "bg-amber-50/20 border-amber-100"
                      }`}
                    >
                      <div className="flex justify-between items-start gap-2">
                        <div>
                          <p className="text-sm font-semibold text-gray-800">{lab.test_requested}</p>
                          <p className="text-[10px] text-gray-400 mt-0.5">
                            Ordered: {new Date(lab.requested_at).toLocaleTimeString()}
                          </p>
                        </div>
                        <div className="flex items-center gap-1">
                          {lab.status === "Completed" ? (
                            <span className="flex items-center gap-1 text-xs text-emerald-700 font-semibold bg-emerald-100/70 px-2 py-0.5 rounded-full">
                              <CheckCircle2 size={12} /> {lab.status}
                            </span>
                          ) : (
                            <span className="flex items-center gap-1 text-xs text-amber-700 font-semibold bg-amber-100/70 px-2 py-0.5 rounded-full">
                              <Clock size={12} className="animate-spin-slow" /> {lab.status}
                            </span>
                          )}
                        </div>
                      </div>

                      {/* Display Results */}
                      {lab.status === "Completed" ? (
                        <div className="mt-2.5 space-y-2">
                          <div className="bg-white p-3 rounded-lg border border-emerald-100 text-xs shadow-sm">
                            <p className="font-semibold text-emerald-800 uppercase tracking-wide text-[9px] mb-1">
                              Laboratory Results:
                            </p>
                            <p className="text-gray-700 leading-relaxed whitespace-pre-line">{lab.results}</p>
                          </div>
                          {lab.technician_notes && (
                            <div className="bg-slate-50 p-3 rounded-lg border border-slate-100 text-xs shadow-sm">
                              <p className="font-semibold text-slate-800 uppercase tracking-wide text-[9px] mb-1">
                                Technician Notes:
                              </p>
                              <p className="text-gray-600 leading-relaxed whitespace-pre-line italic">
                                "{lab.technician_notes}"
                              </p>
                            </div>
                          )}
                        </div>
                      ) : (
                        <div className="mt-2.5 bg-gray-50/50 p-2.5 rounded-lg border border-dashed text-center text-xs text-gray-400">
                          Awaiting laboratory analysis...
                        </div>
                      )}
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8 text-gray-400 text-xs">
                    No lab tests requested for this encounter yet.
                  </div>
                )}
              </div>

              {/* Order Lab Form */}
              <div className="mt-5 pt-4 border-t border-gray-100">
                <h4 className="text-xs font-bold text-gray-600 uppercase mb-3 flex items-center gap-1">
                  <Plus size={14} /> Quick-Order Lab Test
                </h4>
                <form onSubmit={handleOrderLab} className="space-y-3">
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={newTestName}
                      onChange={(e) => setNewTestName(e.target.value)}
                      placeholder="e.g. Malaria BS, LFT, CBC"
                      className="flex-1 border border-gray-300 rounded-lg px-3 py-1.5 text-xs
                        focus:outline-none focus:ring-2 focus:ring-blue-400 bg-white"
                      required
                    />
                    <Button
                      type="submit"
                      variant="primary"
                      className="py-1.5 px-3 text-xs"
                      disabled={requestMutation.isPending}
                    >
                      {requestMutation.isPending ? "Ordering..." : "Order"}
                    </Button>
                  </div>
                  {labError && <p className="text-[10px] text-red-500 bg-red-50 p-1.5 rounded">{labError}</p>}
                  {labSuccess && <p className="text-[10px] text-green-600 bg-green-50 p-1.5 rounded">{labSuccess}</p>}
                </form>
              </div>
            </Card>
          </div>
        </div>
      )}
    </div>
  );
}