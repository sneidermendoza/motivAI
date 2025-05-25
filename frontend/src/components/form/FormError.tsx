interface FormErrorProps {
  message?: string;
}

export default function FormError({ message }: FormErrorProps) {
  if (!message) return null;
  return (
    <div className="w-full mb-4 text-center text-red-600 bg-red-50 border border-red-200 rounded-lg py-2 px-3 text-sm">
      {message}
    </div>
  );
}
