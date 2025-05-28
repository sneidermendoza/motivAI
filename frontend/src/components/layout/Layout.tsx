"use client"
import { ReactNode } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import SidebarNav from './SidebarNav';
import UserAvatar from './UserAvatar';
import { ArrowLeftOnRectangleIcon } from '@heroicons/react/24/outline';

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const { user, logout } = useAuth();
  const pathname = usePathname();

  return (
    <div className="min-h-screen bg-gray-100 flex">
      {/* SidebarNav (desktop) y TabBar (mobile) */}
      <SidebarNav />
      <div className="flex-1 flex flex-col min-h-screen md:pl-20" style={{ marginLeft: '0', marginTop: '0' }}>
        {/* Navbar superior */}
        <nav className="bg-white shadow-lg px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between sticky top-0 z-20">
          <div className="flex items-center space-x-4">
            <Link href="/" className="text-2xl font-bold text-indigo-600">motivAI</Link>
          </div>
          {user && (
            <div className="flex items-center space-x-2">
              <UserAvatar username={user.username} photoUrl={user.foto_perfil || undefined} size={36} />
              <button
                onClick={logout}
                className="p-2 rounded-full hover:bg-indigo-50 text-indigo-600"
                title="Cerrar sesión"
              >
                <ArrowLeftOnRectangleIcon className="w-6 h-6" />
              </button>
            </div>
          )}
        </nav>
        {/* Main Content */}
        <main className="flex-1 max-w-7xl mx-auto py-6 sm:px-6 lg:px-8 w-full">
          {children}
        </main>
      </div>
    </div>
  );
} 