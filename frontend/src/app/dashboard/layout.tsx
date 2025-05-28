import { AuthProvider } from "@/contexts/AuthContext";
import Layout from "@/components/layout/Layout";
import ProtectedRoute from '@/components/layout/ProtectedRoute';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <ProtectedRoute>
        <Layout>{children}</Layout>
      </ProtectedRoute>
    </AuthProvider>
  );
} 