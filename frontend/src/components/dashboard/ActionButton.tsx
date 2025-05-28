interface ActionButtonProps {
  label: string;
  onClick: () => void;
  className?: string;
}

export default function ActionButton({ label, onClick, className = '' }: ActionButtonProps) {
  return (
    <button
      onClick={onClick}
      className={`w-full py-4 mt-6 bg-indigo-600 text-white text-lg font-bold rounded-xl shadow-lg hover:bg-indigo-700 transition ${className}`}
    >
      {label}
    </button>
  );
} 