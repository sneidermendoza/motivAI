'use client';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import InputField from '../form/InputField';
import Button from '../form/Button';
import FormError from '../form/FormError';
import SocialAuthButtons from './SocialAuthButtons';
import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';

const schema = z.object({
  name: z.string().min(2, 'El nombre es requerido'),
  email: z.string().email('Email inválido'),
  password: z.string().min(6, 'La contraseña debe tener al menos 6 caracteres'),
  password2: z.string(),
}).refine((data) => data.password === data.password2, {
  message: 'Las contraseñas no coinciden',
  path: ['password2'],
});

type RegisterData = z.infer<typeof schema>;

// Diccionario de traducción de errores comunes
const errorTranslations: Record<string, string> = {
  'A user with that username already exists.': 'Ya existe un usuario con ese nombre.',
  'A user with that email already exists.': 'Ya existe un usuario con ese email.',
  'This field may not be blank.': 'Este campo no puede estar vacío.',
  'This field is required.': 'Este campo es obligatorio.',
  'La contraseña debe contener letras y números.': 'La contraseña debe contener letras y números.',
  'Ensure this field has at least 8 characters.': 'Asegúrate de que este campo tenga al menos 8 caracteres.',
};

function translateError(msg: string) {
  return errorTranslations[msg] || msg;
}

export default function RegisterForm({ onLogin }: { onLogin?: () => void }) {
  const [formError, setFormError] = useState('');
  const { register: registerUser, error: authError } = useAuth();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterData>({
    resolver: zodResolver(schema),
  });
  const [backendFieldErrors, setBackendFieldErrors] = useState<Record<string, string[]>>({});

  const onSubmit = async (data: RegisterData) => {
    setFormError('');
    setBackendFieldErrors({});
    try {
      await registerUser(data.name, data.email, data.password, data.password2);
      // El contexto maneja el login automático y la redirección
    } catch (e: any) {
      // Extraer errores de campos del backend
      const backendData = e?.response?.data?.data;
      if (backendData && typeof backendData === 'object') {
        setBackendFieldErrors(backendData);
      }
      setFormError(e?.response?.data?.message || authError || 'Error al registrar usuario');
    }
  };

  return (
    <div className="w-full flex flex-col text-sm">
      <form onSubmit={handleSubmit(onSubmit)} className="w-full flex flex-col gap-1">
        <div className="mb-1">
          <InputField
            label="Nombre"
            type="text"
            autoComplete="name"
            {...register('name')}
            error={errors.name?.message || (backendFieldErrors.username && translateError(backendFieldErrors.username[0]))}
            placeholder="Tu nombre"
          />
        </div>
        <div className="mb-1">
          <InputField
            label="Email"
            type="email"
            autoComplete="email"
            {...register('email')}
            error={errors.email?.message || (backendFieldErrors.email && translateError(backendFieldErrors.email[0]))}
            placeholder="tucorreo@ejemplo.com"
          />
        </div>
        <div className="mb-1">
          <InputField
            label="Contraseña"
            type="password"
            autoComplete="new-password"
            {...register('password')}
            error={errors.password?.message || (backendFieldErrors.password && translateError(backendFieldErrors.password[0]))}
            placeholder="••••••••"
          />
        </div>
        <div className="mb-1">
          <InputField
            label="Confirmar contraseña"
            type="password"
            autoComplete="new-password"
            {...register('password2')}
            error={errors.password2?.message || (backendFieldErrors.password2 && translateError(backendFieldErrors.password2[0]))}
            placeholder="••••••••"
          />
        </div>
        <Button type="submit" loading={isSubmitting} className="mt-2 text-sm py-2">
          Registrarse
        </Button>
      </form>
      <div className="mt-4 flex flex-col items-center gap-1 text-sm">
        <SocialAuthButtons />
      </div>
      {/* <div className="mt-4 text-center text-sm w-full">
        <span className="text-gray-700">¿Ya tienes cuenta?</span>{' '}
        <button className="text-blue-600 font-semibold hover:underline" type="button" onClick={onLogin}>
          Inicia sesión
        </button>
      </div> */}
    </div>
  );
}
