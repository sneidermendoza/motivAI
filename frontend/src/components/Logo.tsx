export default function Logo({ size = 80 }: { size?: number }) {
    return (
      <svg width={size} height={size} viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="60" cy="60" r="54" fill="#2563eb" stroke="#22d3ee" strokeWidth="6" />
        <path d="M40 80 Q60 40 80 80" stroke="#f59e42" strokeWidth="6" fill="none" />
        <circle cx="60" cy="60" r="18" fill="#22d3ee" />
      </svg>
    );
  }
  