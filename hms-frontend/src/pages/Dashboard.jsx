// Fix [MISSING]
import { useQuery } from "@tanstack/react-query";
import { getPatients } from "../api/patients";
import { getMOHSummary } from "../api/reports";
import Card from "../components/ui/Card";
import { Users, UserCheck, Activity, TrendingUp } from "lucide-react";

function StatCard({ icon: Icon, label, value, color }) {
  return (
    <div className={`bg-white rounded-xl border p-5 flex items-center gap-4 shadow-sm`}>
      <div className={`p-3 rounded-lg ${color}`}>
        <Icon size={22} className="text-white" />
      </div>
      <div>
        <p className="text-xs text-gray-500 font-medium uppercase tracking-wide">{label}</p>
        <p className="text-2xl font-bold text-gray-800">{value ?? "—"}</p>
      </div>
    </div>
  );
}

export default function Dashboard() {
  const today = new Date().toISOString().split("T")[0];

  const { data: patients } = useQuery({
    queryKey: ["patients"],
    queryFn: () => getPatients().then((r) => r.data),
  });

  const { data: moh } = useQuery({
    queryKey: ["moh-summary", today],
    queryFn: () => getMOHSummary(today).then((r) => r.data),
  });

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-xl font-bold text-gray-800">Dashboard</h1>
        <p className="text-sm text-gray-500">Overview for {new Date().toDateString()}</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard icon={Users} label="Total Patients" value={patients?.length}
          color="bg-blue-600" />
        <StatCard icon={UserCheck} label="Under 5 Today"
          value={moh?.under_5_total ?? 0} color="bg-emerald-600" />
        <StatCard icon={Activity} label="Over 5 Today"
          value={moh?.over_5_total ?? 0} color="bg-amber-500" />
        <StatCard icon={TrendingUp} label="Total Today"
          value={(moh?.under_5_total ?? 0) + (moh?.over_5_total ?? 0)}
          color="bg-purple-600" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card title="Under 5 Diagnoses Today">
          {moh?.under_5 && Object.keys(moh.under_5).length ? (
            <ul className="space-y-2">
              {Object.entries(moh.under_5).map(([dx, count]) => (
                <li key={dx} className="flex justify-between text-sm">
                  <span className="text-gray-700">{dx}</span>
                  <span className="font-semibold text-blue-700">{count}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-gray-400">No data for today.</p>
          )}
        </Card>
        <Card title="Over 5 Diagnoses Today">
          {moh?.over_5 && Object.keys(moh.over_5).length ? (
            <ul className="space-y-2">
              {Object.entries(moh.over_5).map(([dx, count]) => (
                <li key={dx} className="flex justify-between text-sm">
                  <span className="text-gray-700">{dx}</span>
                  <span className="font-semibold text-purple-700">{count}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-gray-400">No data for today.</p>
          )}
        </Card>
      </div>
    </div>
  );
}