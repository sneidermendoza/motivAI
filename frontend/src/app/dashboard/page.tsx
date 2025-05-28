'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { plansApi } from '@/lib/api';
import { TrainingPlan } from '@/types/api';
import Link from 'next/link';

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
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-white shadow rounded-lg p-6">
        <h1 className="text-2xl font-bold text-gray-900">
          ¡Bienvenido, {user?.username}!
        </h1>
        <p className="mt-2 text-gray-600">
          Tu entrenador personal inteligente está listo para ayudarte a alcanzar tus objetivos.
        </p>
      </div>

      {/* Active Plan Section */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Tu Plan Activo
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
          <div className="text-center py-6">
            <p className="text-gray-600 mb-4">
              No tienes un plan activo. ¡Comienza tu viaje fitness ahora!
            </p>
            <Link
              href="/plans/new"
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Crear Nuevo Plan
            </Link>
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link
          href="/plans/new"
          className="bg-white shadow rounded-lg p-6 hover:shadow-md transition-shadow"
        >
          <h3 className="text-lg font-medium text-gray-900">Nuevo Plan</h3>
          <p className="mt-2 text-sm text-gray-600">
            Crea un nuevo plan de entrenamiento personalizado
          </p>
        </Link>
        <Link
          href="/progress"
          className="bg-white shadow rounded-lg p-6 hover:shadow-md transition-shadow"
        >
          <h3 className="text-lg font-medium text-gray-900">Registrar Progreso</h3>
          <p className="mt-2 text-sm text-gray-600">
            Actualiza tus medidas y fotos de progreso
          </p>
        </Link>
        <Link
          href="/feedback"
          className="bg-white shadow rounded-lg p-6 hover:shadow-md transition-shadow"
        >
          <h3 className="text-lg font-medium text-gray-900">Feedback</h3>
          <p className="mt-2 text-sm text-gray-600">
            Envía tus sugerencias y comentarios
          </p>
        </Link>
      </div>
    </div>
  );
} 