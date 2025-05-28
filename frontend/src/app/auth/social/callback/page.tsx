'use client';
import { useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Logo from '@/components/Logo';

export default function SocialCallback() {
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    const token = searchParams.get('token');
    const refresh = searchParams.get('refresh');
    console.log('URL actual:', window.location.href);
    console.log('Token recibido:', token);
    console.log('Refresh recibido:', refresh);
    if (token) {
      localStorage.setItem('token', token);
      document.cookie = `access_token=${token}; path=/;`;
    }
    if (refresh) {
      localStorage.setItem('refresh_token', refresh);
      document.cookie = `refresh_token=${refresh}; path=/;`;
    }
    if (token) {
      console.log('Token y refresh guardados');
      router.push('/dashboard');
    } else {
      console.warn('No se recibió token, redirigiendo a /auth/error');
      router.push('/auth/error');
    }
  }, [router, searchParams]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-100 to-cyan-200">
      <Logo size={80} />
      <div className="mt-6 flex flex-col items-center">
        <div className="w-12 h-12 border-4 border-cyan-400 border-t-blue-600 rounded-full animate-spin mb-4"></div>
        <span className="text-lg font-semibold text-blue-700">Procesando login social...</span>
      </div>
    </div>
  );
} 