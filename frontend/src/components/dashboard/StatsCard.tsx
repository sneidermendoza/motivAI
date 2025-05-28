import { ReactNode } from 'react';

interface StatsCardProps {
  icon: ReactNode;
  title: string;
  value: string | number;
  status?: string;
  accentColor?: string;
}

export default function StatsCard({ icon, title, value, status, accentColor = 'indigo' }: StatsCardProps) {
  return (
    <div className={`bg-white rounded-xl shadow-md p-5 flex flex-col items-center justify-center min-w-[120px] min-h-[120px]`}> 
      <div className={`text-3xl mb-2 text-${accentColor}-600`}>{icon}</div>
      <div className="text-2xl font-bold text-gray-900">{value}</div>
      <div className="text-sm text-gray-500 mb-1">{title}</div>
      {status && <div className="text-xs font-semibold text-green-500">{status}</div>}
    </div>
  );
} 