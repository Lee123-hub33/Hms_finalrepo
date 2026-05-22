import { useState } from "react";
import { getMOHSummary } from "../../api/reports";

export default function Reports() {
  const [date, setDate] = useState("");
  const [reportData, setReportData] = useState(null);

  const fetchReport = async () => {
    if (!date) return;
    try {
      const res = await getMOHSummary(date);
      setReportData(res.data);
    } catch {
      alert("Error generating compiled administrative data files.");
    }
  };

  return (
    <div className="p-6 max-w-2xl">
      <h1 className="text-xl font-bold mb-2">Ministry of Health (MOH) Summary Logs</h1>
      <p className="text-xs text-gray-500 mb-4">Compile system encounters for public health reporting structures.</p>
      
      <div className="flex gap-3 mb-6 bg-white p-4 rounded-xl border shadow-sm items-end">
        <div className="flex-1">
          <label className="block text-xs font-semibold text-gray-600 mb-1">Target Compilation Date</label>
          <input 
            type="date" 
            value={date} 
            onChange={(e) => setDate(e.target.value)} 
            className="w-full border rounded-lg px-3 py-1.5 text-sm" 
          />
        </div>
        <button onClick={fetchReport} className="bg-blue-900 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-800 transition">
          Generate Log Report
        </button>
      </div>

      {reportData ? (
        <div className="bg-white p-5 rounded-xl border shadow-sm text-sm">
          <pre className="whitespace-pre-wrap text-xs bg-gray-50 p-3 rounded border text-gray-700">
            {JSON.stringify(reportData, null, 2)}
          </pre>
        </div>
      ) : (
        <div className="text-center text-sm text-gray-400 p-8 border border-dashed rounded-xl bg-gray-50">
          Select structural date limits above to summarize facility parameters.
        </div>
      )}
    </div>
  );
}