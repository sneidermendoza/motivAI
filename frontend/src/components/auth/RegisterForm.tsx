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
  name: z.string().min(2, 'El nombre es requerido'),
  email: z.string().email('Email inválido'),
  password: z.string().min(6, 'La contraseña debe tener al menos 6 caracteres'),
  password2: z.string(),
}).refine((data) => data.password === data.password2, {
  message: 'Las contraseñas no coinciden',
  path: ['password2'],
});

type RegisterData = z.infer<typeof schema>;

export default function RegisterForm({ onLogin }: { onLogin?: () => void }) {
  const [formError, setFormError] = useState('');
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: RegisterData) => {
    setFormError('');
    // Aquí va la integración con la API
    // try {
    //   await registerApi(data);
    // } catch (e) {
    //   setFormError('Error al registrar usuario');
    // }
  };

  return (
    <>
      <form onSubmit={handleSubmit(onSubmit)} className="w-full">
        <FormError message={formError} />
        <InputField
          label="Nombre"
          type="text"
          autoComplete="name"
          {...register('name')}
          error={errors.name?.message}
          placeholder="Tu nombre"
        />
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
          autoComplete="new-password"
          {...register('password')}
          error={errors.password?.message}
          placeholder="••••••••"
        />
        <InputField
          label="Confirmar contraseña"
          type="password"
          autoComplete="new-password"
          {...register('password2')}
          error={errors.password2?.message}
          placeholder="••••••••"
        />
        <Button type="submit" loading={isSubmitting} className="mt-2">
          Registrarse
        </Button>
      </form>
      <div className="mt-6">
        <SocialAuthButtons />
      </div>
      {/* <div className="mt-4 text-center text-sm w-full">
        <span className="text-gray-700">¿Ya tienes cuenta?</span>{' '}
        <button className="text-blue-600 font-semibold hover:underline" type="button" onClick={onLogin}>
          Inicia sesión
        </button>
      </div> */}
    </>
  );
}
