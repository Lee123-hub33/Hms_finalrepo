import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuth } from "../../hooks/useAuth";
import { requestLab, enterResults, getLabRequests } from "../../api/lab";
import Input from "../../components/ui/Input";
import Button from "../../components/ui/Button";
import Card from "../../components/ui/Card";
import Table from "../../components/ui/Table";
import Badge from "../../components/ui/Badge";
import Modal from "../../components/ui/Modal";
import { FlaskConical, CheckCircle2, Clock, Plus, ClipboardList } from "lucide-react";

export default function LabRequests() {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const isLabTech = user?.role === "Lab";

  const [activeTab, setActiveTab] = useState(isLabTech ? "pending" : "request");
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedLab, setSelectedLab] = useState(null);
  const [resultsText, setResultsText] = useState("");
  const [techNotes, setTechNotes] = useState("");
  const [resultsError, setResultsError] = useState("");

  // Request form state
  const [form, setForm] = useState({ encounter_id: "", test_requested: "" });
  const [requestError, setRequestError] = useState("");
  const [requestSuccess, setRequestSuccess] = useState("");

  // Fetch pending requests
  const { data: pendingRequests, isLoading: loadingPending } = useQuery({
    queryKey: ["lab-requests", "Pending"],
    queryFn: () => getLabRequests({ status: "Pending" }).then((r) => r.data),
    enabled: !!user,
  });

  // Fetch completed requests
  const { data: completedRequests, isLoading: loadingCompleted } = useQuery({
    queryKey: ["lab-requests", "Completed"],
    queryFn: () => getLabRequests({ status: "Completed" }).then((r) => r.data),
    enabled: !!user,
  });

  // Mutation to request lab
  const requestMutation = useMutation({
    mutationFn: requestLab,
    onSuccess: () => {
      setRequestSuccess("🔬 Lab request dispatched successfully.");
      setForm({ encounter_id: "", test_requested: "" });
      queryClient.invalidateQueries({ queryKey: ["lab-requests"] });
    },
    onError: (err) => {
      setRequestError(err.response?.data?.detail || "Failed to send lab request.");
    },
  });

  // Mutation to enter results
  const resultsMutation = useMutation({
    mutationFn: ({ id, results, technician_notes }) => 
      enterResults(id, { results, technician_notes }),
    onSuccess: () => {
      setModalOpen(false);
      setSelectedLab(null);
      setResultsText("");
      setTechNotes("");
      queryClient.invalidateQueries({ queryKey: ["lab-requests"] });
    },
    onError: (err) => {
      setResultsError(err.response?.data?.detail || "Failed to submit lab results.");
    },
  });

  const handleRequestSubmit = (e) => {
    e.preventDefault();
    setRequestError("");
    setRequestSuccess("");
    requestMutation.mutate({
      encounter_id: parseInt(form.encounter_id),
      test_requested: form.test_requested,
    });
  };

  const handleResultsSubmit = (e) => {
    e.preventDefault();
    setResultsError("");
    if (!resultsText.trim()) {
      setResultsError("Results cannot be empty.");
      return;
    }
    resultsMutation.mutate({ 
      id: selectedLab.id, 
      results: resultsText,
      technician_notes: techNotes 
    });
  };

  const openResultsModal = (lab) => {
    setSelectedLab(lab);
    setResultsText("");
    setTechNotes("");
    setResultsError("");
    setModalOpen(true);
  };

  // Lab Tech Queue columns
  const pendingColumns = [
    { key: "id", label: "Request ID" },
    { key: "patient_name", label: "Patient" },
    { key: "encounter_id", label: "Encounter ID" },
    { key: "test_requested", label: "Test Requested" },
    {
      key: "requested_at",
      label: "Requested At",
      render: (row) => new Date(row.requested_at).toLocaleString(),
    },
    {
      key: "actions",
      label: "Action",
      render: (row) => (
        <Button variant="success" onClick={() => openResultsModal(row)} className="py-1 px-3 text-xs">
          Enter Results
        </Button>
      ),
    },
  ];

  const completedColumns = [
    { key: "id", label: "Request ID" },
    { key: "patient_name", label: "Patient" },
    { key: "encounter_id", label: "Encounter ID" },
    { key: "test_requested", label: "Test Requested" },
    { key: "results", label: "Results" },
    { key: "technician_notes", label: "Notes" },
    {
      key: "completed_at",
      label: "Completed At",
      render: (row) => new Date(row.completed_at).toLocaleString(),
    },
  ];

  // Doctor workbench columns
  const doctorRecentColumns = [
    { key: "id", label: "ID" },
    { key: "encounter_id", label: "Encounter" },
    { key: "test_requested", label: "Test Requested" },
    {
      key: "status",
      label: "Status",
      render: (row) => (
        <Badge
          label={row.status}
          color={row.status === "Completed" ? "green" : "yellow"}
        />
      ),
    },
    { key: "results", label: "Results" },
    { key: "technician_notes", label: "Notes" },
  ];

  return (
    <div className="p-6 space-y-6 max-w-6xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
            <FlaskConical className="text-slate-900" size={24} />
            Laboratory Management
          </h1>
          <p className="text-sm text-gray-500">
            {isLabTech ? "Lab Technician Portal — Process active orders" : "Physician Portal — Request & track lab tests"}
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="flex bg-gray-100 p-1 rounded-xl">
          {isLabTech ? (
            <>
              <button
                onClick={() => setActiveTab("pending")}
                className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg transition
                  ${activeTab === "pending" ? "bg-white text-slate-900 shadow-sm" : "text-gray-600 hover:text-gray-800"}`}
              >
                <Clock size={16} /> Pending Queue
              </button>
              <button
                onClick={() => setActiveTab("completed")}
                className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg transition
                  ${activeTab === "completed" ? "bg-white text-slate-900 shadow-sm" : "text-gray-600 hover:text-gray-800"}`}
              >
                <CheckCircle2 size={16} /> History
              </button>
            </>
          ) : (
            <>
              <button
                onClick={() => setActiveTab("request")}
                className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg transition
                  ${activeTab === "request" ? "bg-white text-slate-900 shadow-sm" : "text-gray-600 hover:text-gray-800"}`}
              >
                <Plus size={16} /> Order Test
              </button>
              <button
                onClick={() => setActiveTab("history")}
                className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg transition
                  ${activeTab === "history" ? "bg-white text-slate-900 shadow-sm" : "text-gray-600 hover:text-gray-800"}`}
              >
                <ClipboardList size={16} /> Track Results
              </button>
            </>
          )}
        </div>
      </div>

      {/* Lab Technician View */}
      {isLabTech && (
        <Card className="shadow-md">
          {activeTab === "pending" ? (
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold text-gray-800">Pending Lab Requests</h3>
                <Badge label={`${pendingRequests?.length || 0} Pending`} color="yellow" />
              </div>
              {loadingPending ? (
                <div className="text-center py-8 text-sm text-gray-500">Loading requests...</div>
              ) : (
                <Table columns={pendingColumns} data={pendingRequests} />
              )}
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold text-gray-800">Completed Lab Results</h3>
                <Badge label={`${completedRequests?.length || 0} Completed`} color="green" />
              </div>
              {loadingCompleted ? (
                <div className="text-center py-8 text-sm text-gray-500">Loading completed requests...</div>
              ) : (
                <Table columns={completedColumns} data={completedRequests} />
              )}
            </div>
          )}
        </Card>
      )}

      {/* Doctor/Fallback View */}
      {!isLabTech && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Order Request Form */}
          {activeTab === "request" ? (
            <div className="lg:col-span-1">
              <Card title="Dispatch Lab Request" className="shadow-md">
                <form onSubmit={handleRequestSubmit} className="space-y-4">
                  <Input
                    label="Encounter ID"
                    type="number"
                    value={form.encounter_id}
                    onChange={(e) => setForm({ ...form, encounter_id: e.target.value })}
                    placeholder="Enter patient encounter ID"
                    required
                  />
                  <Input
                    label="Test Requested"
                    value={form.test_requested}
                    onChange={(e) => setForm({ ...form, test_requested: e.target.value })}
                    placeholder="e.g. Malaria BS, CBC, Urinalysis"
                    required
                  />
                  {requestError && <p className="text-xs text-red-500 bg-red-50 p-2 rounded-lg">{requestError}</p>}
                  {requestSuccess && <p className="text-xs text-green-600 bg-green-50 p-2 rounded-lg">{requestSuccess}</p>}
                  <Button
                    type="submit"
                    variant="primary"
                    className="w-full"
                    disabled={requestMutation.isPending}
                  >
                    {requestMutation.isPending ? "Sending..." : "Dispatch Lab Request"}
                  </Button>
                </form>
              </Card>
            </div>
          ) : null}

          {/* Track Results */}
          <div className={activeTab === "request" ? "lg:col-span-2" : "lg:col-span-3"}>
            <Card title="Track Recent Lab Requests" className="shadow-md">
              {loadingPending || loadingCompleted ? (
                <div className="text-center py-8 text-sm text-gray-500">Loading data...</div>
              ) : (
                <Table
                  columns={doctorRecentColumns}
                  data={[...(pendingRequests || []), ...(completedRequests || [])]}
                />
              )}
            </Card>
          </div>
        </div>
      )}

      {/* Enter Results Modal */}
      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title="Submit Lab Results">
        {selectedLab && (
          <form onSubmit={handleResultsSubmit} className="space-y-4">
            <div className="bg-slate-50 p-4 rounded-xl space-y-2 border border-slate-100">
              <p className="text-sm font-semibold text-slate-900">Encounter ID: #{selectedLab.encounter_id}</p>
              <p className="text-sm text-slate-800">
                <span className="font-semibold">Patient:</span> {selectedLab.patient_name}
              </p>
              <p className="text-sm text-slate-800">
                <span className="font-semibold">Test Ordered:</span> {selectedLab.test_requested}
              </p>
            </div>

            <div className="space-y-1">
              <label className="block text-xs font-semibold text-gray-600 uppercase tracking-wide">
                Test Results
              </label>
              <textarea
                value={resultsText}
                onChange={(e) => setResultsText(e.target.value)}
                placeholder="Enter detailed laboratory findings, measurements, or diagnostic results..."
                rows={4}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm
                  focus:outline-none focus:ring-2 focus:ring-blue-400"
                required
              />
            </div>

            <div className="space-y-1">
              <label className="block text-xs font-semibold text-gray-600 uppercase tracking-wide">
                Technician Notes (Optional)
              </label>
              <textarea
                value={techNotes}
                onChange={(e) => setTechNotes(e.target.value)}
                placeholder="Any additional observations or comments..."
                rows={3}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm
                  focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
            </div>

            {resultsError && <p className="text-xs text-red-500 bg-red-50 p-2 rounded-lg">{resultsError}</p>}

            <div className="flex justify-end gap-2">
              <Button variant="secondary" onClick={() => setModalOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" variant="success" disabled={resultsMutation.isPending}>
                {resultsMutation.isPending ? "Submitting..." : "Submit & Complete"}
              </Button>
            </div>
          </form>
        )}
      </Modal>
    </div>
  );
}