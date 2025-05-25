'use client';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import InputField from '../form/InputField';
import Button from '../form/Button';
import FormError from '../form/FormError';
import { useState } from 'react';

const schema = z.object({
  password: z.string().min(6, 'La contraseña debe tener al menos 6 caracteres'),
  password2: z.string(),
}).refine((data) => data.password === data.password2, {
  message: 'Las contraseñas no coinciden',
  path: ['password2'],
});

type SetPasswordData = z.infer<typeof schema>;

export default function SetPasswordForm({ onLogin }: { onLogin?: () => void }) {
  const [formError, setFormError] = useState('');
  const [success, setSuccess] = useState(false);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<SetPasswordData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: SetPasswordData) => {
    setFormError('');
    setSuccess(false);
    // Aquí va la integración con la API
    // try {
    //   await setPasswordApi(data);
    //   setSuccess(true);
    // } catch (e) {
    //   setFormError('No se pudo establecer la contraseña');
    // }
    setSuccess(true); // Simulación
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="w-full">
      {success ? (
        <div className="w-full mb-4 text-center text-green-700 bg-green-50 border border-green-200 rounded-lg py-2 px-3 text-sm">
          ¡Contraseña establecida correctamente! Ya puedes iniciar sesión.
        </div>
      ) : (
        <>
          <FormError message={formError} />
          <InputField
            label="Nueva contraseña"
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
            Guardar contraseña
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
