import { ReactNode } from "react";

// Heading Component
interface HeadingProps {
  level?: 1 | 2 | 3 | 4;
  children: ReactNode;
  className?: string;
}

export function Heading({ level = 1, children, className = "" }: HeadingProps) {
  const baseClasses = "font-serif text-deep-900 mb-4";

  const levelClasses = {
    1: "text-4xl md:text-6xl lg:text-7xl font-bold leading-tight",
    2: "text-3xl md:text-4xl lg:text-5xl font-semibold leading-tight",
    3: "text-2xl md:text-3xl lg:text-4xl font-semibold leading-snug",
    4: "text-xl md:text-2xl lg:text-3xl font-medium leading-snug",
  };

  const combinedClasses = `${baseClasses} ${levelClasses[level]} ${className}`;

  switch (level) {
    case 1:
      return <h1 className={combinedClasses}>{children}</h1>;
    case 2:
      return <h2 className={combinedClasses}>{children}</h2>;
    case 3:
      return <h3 className={combinedClasses}>{children}</h3>;
    case 4:
      return <h4 className={combinedClasses}>{children}</h4>;
    default:
      return <h1 className={combinedClasses}>{children}</h1>;
  }
}

// Body Text Component
interface BodyTextProps {
  children: ReactNode;
  className?: string;
  size?: "sm" | "md" | "lg";
}

export function BodyText({ children, className = "", size = "md" }: BodyTextProps) {
  const sizeClasses = {
    sm: "text-base leading-relaxed",
    md: "text-lg leading-relaxed md:text-body",
    lg: "text-xl leading-relaxed md:text-2xl",
  };

  return (
    <p className={`font-sans text-earth-800 mb-6 max-w-reading ${sizeClasses[size]} ${className}`}>
      {children}
    </p>
  );
}

// Quote Component
interface QuoteProps {
  children: ReactNode;
  author?: string;
  className?: string;
}

export function Quote({ children, author, className = "" }: QuoteProps) {
  return (
    <blockquote className={`my-8 pl-6 border-l-4 border-frequency ${className}`}>
      <p className="font-serif text-2xl md:text-3xl text-deep-800 italic leading-relaxed mb-4">
        {children}
      </p>
      {author && (
        <cite className="font-sans text-sm text-earth-600 not-italic tracking-wide">
          — {author}
        </cite>
      )}
    </blockquote>
  );
}

// Caption Component
interface CaptionProps {
  children: ReactNode;
  className?: string;
}

export function Caption({ children, className = "" }: CaptionProps) {
  return (
    <p className={`font-sans text-sm text-earth-600 italic mt-2 ${className}`}>
      {children}
    </p>
  );
}

// Section Title Component
interface SectionTitleProps {
  children: ReactNode;
  className?: string;
}

export function SectionTitle({ children, className = "" }: SectionTitleProps) {
  return (
    <h2 className={`font-sans text-xs tracking-[0.2em] uppercase text-earth-600 mb-6 ${className}`}>
      {children}
    </h2>
  );
}
