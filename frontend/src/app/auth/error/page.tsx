import { useRouter } from 'next/router';

export default function AuthError() {
  const router = useRouter();

  return (
    <div>
      <h1>Error en la autenticación social</h1>
      <p>Hubo un problema al autenticar con el proveedor social.</p>
      <button onClick={() => router.push('/login')}>Volver a login</button>
    </div>
  );
} 