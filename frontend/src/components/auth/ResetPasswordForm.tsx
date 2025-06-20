'use client';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import InputField from '../form/InputField';
import Button from '../form/Button';
import FormError from '../form/FormError';
import { useState } from 'react';
import { authApi } from '@/lib/api';

const schema = z.object({
  email: z.string().email('Email inválido'),
});

type ResetData = z.infer<typeof schema>;

export default function ResetPasswordForm({ onLogin }: { onLogin?: () => void }) {
  const [formError, setFormError] = useState('');
  const [success, setSuccess] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<ResetData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: ResetData) => {
    setFormError('');
    setSuccess(false);
    setSuccessMsg('');
    try {
      const res = await authApi.resetPassword({ email: data.email });
      setSuccess(true);
      setSuccessMsg(res.message || 'Si el correo existe, recibirás un enlace para restablecer tu contraseña.');
    } catch (e: any) {
      setFormError(e?.response?.data?.message || 'No se pudo enviar el correo de recuperación');
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="w-full">
      {success ? (
        <div className="w-full mb-4 text-center text-green-700 bg-green-50 border border-green-200 rounded-lg py-2 px-3 text-sm">
          {successMsg}
        </div>
      ) : (
        <>
          <FormError message={formError} />
          <InputField
            label="Email"
            type="email"
            autoComplete="email"
            {...register('email')}
            error={errors.email?.message}
            placeholder="tucorreo@ejemplo.com"
          />
          <Button type="submit" loading={isSubmitting} className="mt-2">
            Enviar enlace
          </Button>
        </>
      )}
      {/* <div className="mt-6 text-center text-sm w-full">
        <button className="text-blue-600 font-semibold hover:underline" type="button" onClick={onLogin}>
          Volver a iniciar sesión
        </button>
      </div> */}
    </form>
  );
}
