import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { HomeIcon, ArrowTrendingUpIcon, CalendarIcon, ChatBubbleLeftRightIcon, UserCircleIcon } from '@heroicons/react/24/outline';

const navItems = [
  { href: '/dashboard', icon: HomeIcon, label: 'Dashboard' },
  { href: '/progress', icon: ArrowTrendingUpIcon, label: 'Progreso' },
  { href: '/plans', icon: CalendarIcon, label: 'Planes' },
  { href: '/feedback', icon: ChatBubbleLeftRightIcon, label: 'Feedback' },
  { href: '/profile', icon: UserCircleIcon, label: 'Perfil' },
];

export default function SidebarNav() {
  const pathname = usePathname();
  return (
    <>
      {/* Sidebar desktop */}
      <nav className="hidden md:flex flex-col items-center bg-white shadow h-full w-20 py-6 fixed left-0 top-0 z-30">
        {navItems.map(({ href, icon: Icon, label }) => (
          <Link key={href} href={href} className={`mb-6 flex flex-col items-center group ${pathname === href ? 'text-indigo-600' : 'text-gray-400 hover:text-indigo-500'}`}> 
            <Icon className="w-7 h-7 mb-1" />
            <span className="text-xs font-medium group-hover:text-indigo-600 hidden xl:block">{label}</span>
          </Link>
        ))}
      </nav>
      {/* Tab bar mobile */}
      <nav className="fixed md:hidden bottom-0 left-0 right-0 bg-white shadow flex justify-around items-center h-16 z-30">
        {navItems.map(({ href, icon: Icon, label }) => (
          <Link key={href} href={href} className={`flex flex-col items-center group ${pathname === href ? 'text-indigo-600' : 'text-gray-400 hover:text-indigo-500'}`}> 
            <Icon className="w-7 h-7" />
            <span className="text-xs font-medium group-hover:text-indigo-600">{label}</span>
          </Link>
        ))}
      </nav>
    </>
  );
} 