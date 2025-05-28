"use client";
import { useEffect } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import Branding from '../components/Branding';
import AuthTabs from '../components/AuthTabs';

export default function HomePage() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && user) {
      router.push("/dashboard");
    }
  }, [user, loading, router]);

  if (loading) return null;

  // Si no hay usuario, muestra la landing page original
  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 via-cyan-400 to-orange-400 transition-colors duration-700">
      {/* Branding a la izquierda en desktop, arriba en mobile */}
      <section className="hidden md:flex flex-col justify-center items-center w-1/2 h-full">
        <Branding />
      </section>
      <section className="flex flex-col justify-center items-center w-full md:w-1/2 h-full p-4">
        <div className="w-full max-w-md bg-white rounded-2xl shadow-2xl p-8 animate-fade-in">
          <div className="block md:hidden mb-8">
            <Branding />
          </div>
          <AuthTabs />
        </div>
      </section>
    </main>
  );
}