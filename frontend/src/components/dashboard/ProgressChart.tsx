export default function ProgressChart() {
  return (
    <div className="bg-white rounded-xl shadow-md p-5 flex flex-col items-center justify-center min-h-[180px]">
      <h3 className="text-lg font-semibold text-gray-900 mb-2">Progreso</h3>
      {/* Placeholder de gráfica */}
      <svg width="180" height="80" viewBox="0 0 180 80">
        <polyline
          fill="none"
          stroke="#2563eb"
          strokeWidth="4"
          points="0,60 30,50 60,55 90,30 120,40 150,20 180,35"
        />
        <circle cx="180" cy="35" r="5" fill="#2563eb" />
      </svg>
      <div className="text-sm text-gray-500 mt-2">Peso, energía, etc.</div>
    </div>
  );
} 