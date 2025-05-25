import { ButtonHTMLAttributes } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  loading?: boolean;
  variant?: 'primary' | 'secondary';
}

export default function Button({
  loading = false,
  variant = 'primary',
  className = '',
  children,
  ...props
}: ButtonProps) {
  const base =
    'w-full py-2 px-4 rounded-lg font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-blue-200';
  const variants = {
    primary:
      'bg-blue-600 text-white hover:bg-blue-700 disabled:bg-blue-300',
    secondary:
      'bg-white text-blue-600 border border-blue-600 hover:bg-blue-50',
  };
  return (
    <button
      className={`${base} ${variants[variant]} ${className}`}
      disabled={loading || props.disabled}
      {...props}
    >
      {loading ? 'Cargando...' : children}
    </button>
  );
}
