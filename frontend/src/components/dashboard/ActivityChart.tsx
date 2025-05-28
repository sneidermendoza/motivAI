export default function ActivityChart() {
  const days = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
  const values = [4, 6, 5, 8, 7, 10, 3]; // Dummy data
  const max = Math.max(...values);

  return (
    <div className="bg-white rounded-xl shadow-md p-5 flex flex-col items-center justify-center min-h-[180px]">
      <h3 className="text-lg font-semibold text-gray-900 mb-2">Actividad semanal</h3>
      <svg width="180" height="80" viewBox="0 0 180 80">
        {values.map((v, i) => (
          <rect
            key={i}
            x={i * 25 + 10}
            y={80 - (v / max) * 60}
            width="16"
            height={(v / max) * 60}
            fill={i === 5 ? '#2563eb' : '#a5b4fc'}
            rx="4"
          />
        ))}
      </svg>
      <div className="flex justify-between w-full mt-2 text-xs text-gray-500">
        {days.map((d, i) => (
          <span key={i} className="w-6 text-center">{d}</span>
        ))}
      </div>
    </div>
  );
} 