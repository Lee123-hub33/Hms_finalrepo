// Fix [EMPTY]: was empty
export default function Input({
  label, name, type = "text", value, onChange,
  placeholder, required, error, className = "", ...rest
}) {
  return (
    <div className="space-y-1">
      {label && (
        <label className="block text-xs font-semibold text-gray-600 uppercase tracking-wide">
          {label}
        </label>
      )}
      <input
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        className={`w-full border rounded-lg px-3 py-2 text-sm focus:outline-none
          focus:ring-2 focus:ring-blue-400 ${error ? "border-red-400" : "border-gray-300"}
          ${className}`}
        {...rest}
      />
      {error && <p className="text-xs text-red-500">{error}</p>}
    </div>
  );
}