// Fix [EMPTY]: was empty
export default function Button({
  children, onClick, type = "button",
  variant = "primary", disabled = false, className = "",
}) {
  const variants = {
    primary:   "bg-blue-600 hover:bg-blue-700 text-white",
    success:   "bg-emerald-600 hover:bg-emerald-700 text-white",
    danger:    "bg-red-600 hover:bg-red-700 text-white",
    warning:   "bg-amber-500 hover:bg-amber-600 text-white",
    secondary: "bg-gray-200 hover:bg-gray-300 text-gray-800",
    ghost:     "bg-transparent hover:bg-gray-100 text-gray-700",
  };
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`px-4 py-2 rounded-lg text-sm font-medium transition disabled:opacity-50
        disabled:cursor-not-allowed ${variants[variant]} ${className}`}
    >
      {children}
    </button>
  );
}