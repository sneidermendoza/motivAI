import { FcGoogle } from 'react-icons/fc';
import { FaFacebook } from 'react-icons/fa';

export default function SocialAuthButtons() {
  return (
    <div className="flex flex-col items-center gap-2 w-full mb-4">
      <span className="text-gray-500 text-sm mb-1">Continuar con</span>
      <div className="flex gap-6 justify-center">
        <button
          type="button"
          aria-label="Continuar con Google"
          className="rounded-full p-2 bg-white shadow hover:scale-110 transition-transform border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-200"
          // onClick={handleGoogleLogin}
        >
          <FcGoogle size={32} />
        </button>
        <button
          type="button"
          aria-label="Continuar con Facebook"
          className="rounded-full p-2 bg-white shadow hover:scale-110 transition-transform border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-200"
          // onClick={handleFacebookLogin}
        >
          <FaFacebook size={34} className="text-[#1877F3]" />
        </button>
      </div>
    </div>
  );
}
