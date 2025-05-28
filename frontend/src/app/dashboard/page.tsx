'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { plansApi } from '@/lib/api';
import { TrainingPlan } from '@/types/api';
import Link from 'next/link';
import MotivationalBanner from '@/components/dashboard/MotivationalBanner';
import StatsCard from '@/components/dashboard/StatsCard';
import ProgressChart from '@/components/dashboard/ProgressChart';
import ActivityChart from '@/components/dashboard/ActivityChart';
import ActionButton from '@/components/dashboard/ActionButton';
import { BoltIcon, FireIcon, HeartIcon, BeakerIcon, ArrowTrendingUpIcon, UserIcon } from '@heroicons/react/24/outline';

export default function DashboardPage() {
  const { user } = useAuth();
  const [activePlan, setActivePlan] = useState<TrainingPlan | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchActivePlan = async () => {
      try {
        const response = await plansApi.getPlans();
        const activePlan = response.data.find(plan => !plan.fecha_fin);
        setActivePlan(activePlan || null);
      } catch (error) {
        console.error('Error fetching active plan:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchActivePlan();
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Banner motivacional */}
      <MotivationalBanner
        username={user?.username}
        message="¡Hoy es un gran día para avanzar en tu meta,"
        actionLabel={activePlan ? undefined : 'Crear nuevo plan'}
        onAction={activePlan ? undefined : () => window.location.href = '/plans/new'}
      />

      {/* Cards flotantes de métricas */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
        <StatsCard icon={<BoltIcon width={32} />} title="Energía" value="78%" status="Good" accentColor="indigo" />
        <StatsCard icon={<FireIcon width={32} />} title="Calorías" value="1260" status="" accentColor="orange" />
        <StatsCard icon={<HeartIcon width={32} />} title="Pulso" value="65 bpm" status="Good" accentColor="red" />
        <StatsCard icon={<BeakerIcon width={32} />} title="Hidratación" value="Low" status="" accentColor="blue" />
        <StatsCard icon={<ArrowTrendingUpIcon width={32} />} title="Progreso" value="95%" status="" accentColor="green" />
        <StatsCard icon={<UserIcon width={32} />} title="Temperatura" value="36.8°" status="Good" accentColor="yellow" />
      </div>

      {/* Paneles de progreso y actividad */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ProgressChart />
        <ActivityChart />
      </div>

      {/* Plan activo o acción */}
      <div className="bg-white shadow rounded-xl p-6 mt-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          {activePlan ? 'Tu Plan Activo' : '¡Comienza tu viaje fitness ahora!'}
        </h2>
        {activePlan ? (
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-medium text-gray-900">
                {activePlan.objetivo}
              </h3>
              <p className="text-sm text-gray-500">
                Inicio: {new Date(activePlan.fecha_inicio).toLocaleDateString()}
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-gray-50 p-4 rounded-lg">
                <h4 className="font-medium text-gray-900">Próxima Rutina</h4>
                <p className="text-sm text-gray-600">
                  {activePlan.rutinas[0]?.tipo === 'entrenamiento'
                    ? `${activePlan.rutinas[0].ejercicios.length} ejercicios`
                    : 'Día de descanso'}
                </p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg">
                <h4 className="font-medium text-gray-900">Progreso</h4>
                <p className="text-sm text-gray-600">
                  {activePlan.rutinas.filter(r => r.realizada).length} de{' '}
                  {activePlan.rutinas.length} rutinas completadas
                </p>
              </div>
            </div>
            <Link
              href="/plans"
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Ver Plan Completo
            </Link>
          </div>
        ) : (
          <ActionButton label="Crear Nuevo Plan" onClick={() => window.location.href = '/plans/new'} />
        )}
      </div>
    </div>
  );
} 