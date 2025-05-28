"use client"
import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User } from '@/types/api';
import { authApi } from '@/lib/api';
import { useRouter } from 'next/navigation';

function getCookie(name: string): string | null {
  if (typeof document === 'undefined') return null;
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop()!.split(';').shift() || null;
  return null;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string, password2: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      let token = localStorage.getItem('access_token');
      if (!token) {
        token = getCookie('access_token');
        if (token) {
          localStorage.setItem('access_token', token);
        }
      }
      if (token) {
        const response = await authApi.getProfile();
        setUser(response.data);
        console.log('Usuario seteado en contexto:', response.data);
      }
    } catch (error) {
      console.error('Error checking auth:', error);
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      document.cookie = 'access_token=; Max-Age=0; path=/;';
      document.cookie = 'refresh_token=; Max-Age=0; path=/;';
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = async (username: string, password: string) => {
    try {
      setError(null);
      const response = await authApi.login({ username, password });
      localStorage.setItem('access_token', response.access);
      localStorage.setItem('refresh_token', response.refresh);
      document.cookie = `access_token=${response.access}; path=/;`;
      document.cookie = `refresh_token=${response.refresh}; path=/;`;
      await checkAuth();
    } catch (error: any) {
      setError(error.response?.data?.message || 'Error al iniciar sesión');
      throw error;
    }
  };

  const register = async (username: string, email: string, password: string, password2: string) => {
    try {
      setError(null);
      await authApi.register({ username, email, password, password2 });
      await login(username, password);
    } catch (error: any) {
      setError(error.response?.data?.message || 'Error al registrar usuario');
      throw error;
    }
  };

  const logout = async () => {
    try {
      await authApi.logout();
      setUser(null);
      document.cookie = 'access_token=; Max-Age=0; path=/;';
      document.cookie = 'refresh_token=; Max-Age=0; path=/;';
      router.push('/');
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, error, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
} 