'use client';
import SetPasswordForm from '@/components/auth/SetPasswordForm';
import { useSearchParams } from 'next/navigation';
import Logo from '@/components/Logo';

export default function ResetPasswordPage() {
  const searchParams = useSearchParams();
  const token = searchParams.get('token') || '';
  const email = searchParams.get('email') || '';

  if (!token || !email) {
    return (
      <div className="max-w-md mx-auto mt-12 p-6 bg-white rounded-lg shadow">
        <h2 className="text-xl font-bold mb-2 text-center">Enlace inválido</h2>
        <p className="text-center text-gray-600">El enlace de recuperación no es válido o está incompleto.</p>
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto mt-12 p-6 bg-white rounded-lg shadow">
      <div className="flex flex-col items-center mb-6">
        <Logo size={60} />
        <span className="mt-2 text-2xl font-extrabold text-blue-700 tracking-tight">motiv<span className="text-cyan-400">AI</span></span>
      </div>
      <h2 className="text-xl font-bold mb-4 text-center">Restablecer contraseña</h2>
      <SetPasswordForm token={token} email={email} />
    </div>
  );
} 