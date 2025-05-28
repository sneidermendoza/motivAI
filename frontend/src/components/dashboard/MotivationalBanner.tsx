import Logo from '../Logo';

interface MotivationalBannerProps {
  username?: string;
  message?: string;
  onAction?: () => void;
  actionLabel?: string;
}

export default function MotivationalBanner({
  username,
  message = '¡Hoy es un gran día para avanzar en tu meta!',
  onAction,
  actionLabel = 'Crear nuevo plan',
}: MotivationalBannerProps) {
  return (
    <div className="relative bg-gradient-to-r from-indigo-100 to-blue-50 rounded-xl shadow-md p-6 flex flex-col md:flex-row items-center justify-between mb-6 overflow-hidden">
      <div className="flex-1">
        <div className="flex items-center mb-2">
          <Logo size={40} />
          <span className="text-2xl font-bold text-indigo-700 ml-2">motivAI</span>
        </div>
        <h2 className="text-xl md:text-2xl font-semibold text-gray-900 mb-2">
          {message} {username && <span className="text-indigo-600">{username}</span>}
        </h2>
        {onAction && (
          <button
            onClick={onAction}
            className="mt-3 px-6 py-2 bg-indigo-600 text-white rounded-lg font-semibold shadow hover:bg-indigo-700 transition"
          >
            {actionLabel}
          </button>
        )}
      </div>
      <div className="hidden md:block md:w-48 lg:w-56">
        {/* SVG ilustrativo, puedes reemplazarlo por una imagen personalizada */}
        <svg viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="100" cy="100" r="100" fill="#2563eb22" />
          <rect x="60" y="60" width="80" height="80" rx="20" fill="#2563eb" />
          <text x="100" y="120" textAnchor="middle" fill="#fff" fontSize="32" fontWeight="bold">💪</text>
        </svg>
      </div>
    </div>
  );
} 