import { UserCircleIcon } from '@heroicons/react/24/outline';

interface UserAvatarProps {
  username: string;
  photoUrl?: string;
  size?: number;
}

export default function UserAvatar({ username, photoUrl, size = 40 }: UserAvatarProps) {
  const safePhotoUrl = photoUrl || undefined;
  return (
    <div className="flex items-center space-x-2">
      {safePhotoUrl ? (
        <img
          src={safePhotoUrl}
          alt={username}
          className="rounded-full object-cover"
          style={{ width: size, height: size }}
        />
      ) : (
        <UserCircleIcon className="text-gray-400" style={{ width: size, height: size }} />
      )}
      <span className="hidden md:inline text-gray-700 font-medium">{username}</span>
    </div>
  );
} 