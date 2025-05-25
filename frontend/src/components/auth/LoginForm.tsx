'use client';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import InputField from '../form/InputField';
import Button from '../form/Button';
import FormError from '../form/FormError';
import SocialAuthButtons from './SocialAuthButtons';
import { useState } from 'react';

const schema = z.object({
  email: z.string().email('Email inválido'),
  password: z.string().min(6, 'La contraseña debe tener al menos 6 caracteres'),
});

type LoginData = z.infer<typeof schema>;

export default function LoginForm() {
  const [formError, setFormError] = useState('');
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: LoginData) => {
    setFormError('');
    // Aquí va la integración con la API
    // try {
    //   await loginApi(data);
    // } catch (e) {
    //   setFormError('Credenciales inválidas');
    // }
  };

  return (
    <>
      <form onSubmit={handleSubmit(onSubmit)} className="w-full">
        <FormError message={formError} />
        <InputField
          label="Email"
          type="email"
          autoComplete="email"
          {...register('email')}
          error={errors.email?.message}
          placeholder="tucorreo@ejemplo.com"
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
