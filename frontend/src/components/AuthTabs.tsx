"use client";
import { useState } from 'react';
import clsx from 'clsx';
import LoginForm from './auth/LoginForm';
import RegisterForm from './auth/RegisterForm';
import ResetPasswordForm from './auth/ResetPasswordForm';
import SetPasswordForm from './auth/SetPasswordForm';

const FORM = {
  LOGIN: 'login',
  REGISTER: 'register',
  RESET: 'reset',
  SET_PASSWORD: 'set_password',
};

export default function AuthTabs() {
  const [form, setForm] = useState(FORM.LOGIN);

  return (
    <div className={clsx(
      'relative',
      form === FORM.REGISTER ? 'min-h-[520px]' : 'min-h-[380px]'
    )}>
      {/* Login Form */}
      <div
        className={clsx(
          'absolute inset-0 transition-all duration-300 ease-out',
          form === FORM.LOGIN
            ? 'opacity-100 translate-x-0 pointer-events-auto z-10'
            : 'opacity-0 -translate-x-10 scale-95 pointer-events-none z-0'
        )}
      >
        <LoginForm />
        <div className="mt-4 text-center text-sm w-full">
          <span className="text-gray-700">¿No tienes cuenta?</span>{' '}
          <button className="text-blue-600 font-semibold hover:underline" onClick={() => setForm(FORM.REGISTER)}>
            Regístrate
          </button>
        </div>
        <div className="mt-2 text-center text-xs w-full">
          <button className="text-cyan-500 hover:underline" onClick={() => setForm(FORM.RESET)}>
            ¿Olvidaste tu contraseña?
          </button>
        </div>
      </div>
      {/* Register Form */}
      <div
        className={clsx(
          'absolute inset-0 transition-all duration-300 ease-out',
          form === FORM.REGISTER
            ? 'opacity-100 translate-x-0 pointer-events-auto z-10'
            : 'opacity-0 translate-x-10 scale-95 pointer-events-none z-0'
        )}
      >
        <RegisterForm />
        <div className="mt-6 text-center text-sm w-full">
          ¿Ya tienes cuenta?{' '}
          <button className="text-blue-600 font-semibold hover:underline" onClick={() => setForm(FORM.LOGIN)}>
            Inicia sesión
          </button>
        </div>
      </div>
      {/* Reset Password Form */}
      <div
        className={clsx(
          'absolute inset-0 transition-all duration-300 ease-out',
          form === FORM.RESET
            ? 'opacity-100 translate-x-0 pointer-events-auto z-10'
            : 'opacity-0 translate-y-10 scale-95 pointer-events-none z-0'
        )}
      >
        <div className="flex flex-col justify-center h-full">
          <ResetPasswordForm />
          <div className="mt-6 text-center text-sm w-full">
            <button className="text-blue-600 font-semibold hover:underline" onClick={() => setForm(FORM.LOGIN)}>
              Volver a iniciar sesión
            </button>
          </div>
          {/* Botón temporal para probar SetPasswordForm */}
          <div className="mt-2 text-center text-xs w-full">
            <button className="text-cyan-500 hover:underline" onClick={() => setForm(FORM.SET_PASSWORD)}>
              (Test) Ir a establecer nueva contraseña
            </button>
          </div>
        </div>
      </div>
      {/* Set Password Form (acceso normalmente por enlace, aquí solo para pruebas) */}
      <div
        className={clsx(
          'absolute inset-0 transition-all duration-300 ease-out',
          form === FORM.SET_PASSWORD
            ? 'opacity-100 translate-x-0 pointer-events-auto z-10'
            : 'opacity-0 translate-y-10 scale-95 pointer-events-none z-0'
        )}
      >
        <SetPasswordForm />
        <div className="mt-6 text-center text-sm w-full">
          <button className="text-blue-600 font-semibold hover:underline" onClick={() => setForm(FORM.LOGIN)}>
            Volver a iniciar sesión
          </button>
        </div>
      </div>
    </div>
  );
}
