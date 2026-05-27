// Fix [EMPTY]: was empty
const colours = {
  green:  "bg-green-100 text-green-800",
  red:    "bg-red-100 text-red-800",
  yellow: "bg-yellow-100 text-yellow-800",
  blue:   "bg-slate-100 text-slate-800",
  gray:   "bg-gray-100 text-gray-700",
};

export default function Badge({ label, color = "gray" }) {
  return (
    <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-semibold
      ${colours[color] || colours.gray}`}>
      {label}
    </span>
  );
}