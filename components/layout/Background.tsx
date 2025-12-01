"use client";

interface BackgroundProps {
  colors?: {
    start: string;
    middle1: string;
    middle2: string;
    end: string;
  };
  children?: React.ReactNode;
}

export default function Background({ colors, children }: BackgroundProps) {
  // Default earth tones + deep blue gradient
  const defaultColors = {
    start: "#dcd2c3", // earth-200
    middle1: "#8ca6c4", // deep-300
    middle2: "#c5b59f", // earth-300
    end: "#6685ac", // deep-400
  };

  const gradientColors = colors || defaultColors;

  return (
    <div className="relative min-h-screen">
      {/* Animated Gradient Background */}
      <div
        className="fixed inset-0 -z-10"
        style={{
          background: `linear-gradient(135deg, ${gradientColors.start}, ${gradientColors.middle1}, ${gradientColors.middle2}, ${gradientColors.end})`,
          backgroundSize: "400% 400%",
          animation: "gradient-shift 15s ease infinite",
        }}
      />

      {/* Subtle texture overlay (optional) */}
      <div
        className="fixed inset-0 -z-10 opacity-[0.03]"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23000000' fill-opacity='1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }}
      />

      {/* Content */}
      {children}
    </div>
  );
}
