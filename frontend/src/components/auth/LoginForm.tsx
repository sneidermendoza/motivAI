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
import { useRouter } from 'next/navigation';

const schema = z.object({
  username: z.string().min(3, 'Ingresa tu email o nombre de usuario'),
  password: z.string().min(6, 'La contraseña debe tener al menos 6 caracteres'),
});

type LoginData = z.infer<typeof schema>;

export default function LoginForm() {
  const [formError, setFormError] = useState('');
  const { login, error: authError } = useAuth();
  const router = useRouter();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: LoginData) => {
    setFormError('');
    try {
      await login(data.username, data.password);
      // La redirección la maneja la landing page
    } catch (e: any) {
      setFormError(e?.response?.data?.message || authError || 'Credenciales inválidas');
      console.log('Error en login:', e);
    }
  };

  return (
    <>
      <form onSubmit={handleSubmit(onSubmit)} className="w-full">
        <FormError message={(formError || authError) || undefined} />
        <InputField
          label="Email o nombre de usuario"
          type="text"
          autoComplete="username"
          {...register('username')}
          error={errors.username?.message}
          placeholder="Tu email o usuario"
        />
        <InputField
          label="Contraseña"
          type="password"
          autoComplete="current-password"
          {...register('password')}
          error={errors.password?.message}
          placeholder="••••••••"
        />
        <Button type="submit" loading={isSubmitting} className="mt-2">
          Iniciar sesión
        </Button>
      </form>
      <div className="mt-6">
        <SocialAuthButtons />
      </div>
    </>
  );
}
