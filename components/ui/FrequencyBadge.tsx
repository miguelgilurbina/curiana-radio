interface FrequencyBadgeProps {
  size?: "sm" | "md" | "lg";
  variant?: "default" | "outline";
}

export default function FrequencyBadge({
  size = "md",
  variant = "default",
}: FrequencyBadgeProps) {
  const sizeClasses = {
    sm: "px-3 py-1 text-xs",
    md: "px-4 py-2 text-sm",
    lg: "px-6 py-3 text-base",
  };

  const variantClasses = {
    default: "bg-frequency text-white border-2 border-frequency",
    outline: "bg-transparent text-frequency border-2 border-frequency",
  };

  return (
    <div
      className={`
        inline-flex items-center justify-center
        font-sans font-bold tracking-widest
        rounded-sm
        transition-all duration-300
        hover:scale-105 hover:shadow-lg
        ${sizeClasses[size]}
        ${variantClasses[variant]}
      `}
    >
      88.8 FM
    </div>
  );
}
