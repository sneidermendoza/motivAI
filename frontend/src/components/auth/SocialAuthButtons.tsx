import { FcGoogle } from 'react-icons/fc';
import { FaFacebook } from 'react-icons/fa';

export default function SocialAuthButtons() {
  const handleGoogleLogin = () => {
    const callbackUrl = encodeURIComponent('http://localhost:3000/auth/social/callback');
    window.location.href = `http://localhost:8000/auth/login/google-oauth2/?next=${callbackUrl}`;
  };

  const handleFacebookLogin = () => {
    const callbackUrl = encodeURIComponent('http://localhost:3000/auth/social/callback');
    window.location.href = `http://localhost:8000/auth/login/facebook/?next=${callbackUrl}`;
  };

  return (
    <div className="flex flex-row items-center justify-center gap-2 w-full mb-2">
      <span className="text-gray-500 text-xs mr-2">Continuar con:</span>
      <button
        type="button"
        aria-label="Continuar con Google"
        className="rounded-full p-1 bg-white shadow hover:scale-110 transition-transform border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-200 w-8 h-8 flex items-center justify-center"
        onClick={handleGoogleLogin}
      >
        <FcGoogle size={18} />
      </button>
      <button
        type="button"
        aria-label="Continuar con Facebook"
        className="rounded-full p-1 bg-white shadow hover:scale-110 transition-transform border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-200 w-8 h-8 flex items-center justify-center"
        onClick={handleFacebookLogin}
      >
        <FaFacebook size={18} className="text-[#1877F3]" />
      </button>
    </div>
  );
}
