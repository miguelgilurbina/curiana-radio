"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

interface NavigationProps {
  editionNumber?: number;
}

export default function Navigation({ editionNumber }: NavigationProps) {
  const [isVisible, setIsVisible] = useState(true);
  const [lastScrollY, setLastScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      const currentScrollY = window.scrollY;

      // Show nav when scrolling up, hide when scrolling down
      // Always show if at top of page
      if (currentScrollY < 10) {
        setIsVisible(true);
      } else if (currentScrollY < lastScrollY) {
        setIsVisible(true);
      } else if (currentScrollY > lastScrollY && currentScrollY > 100) {
        setIsVisible(false);
      }

      setLastScrollY(currentScrollY);
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, [lastScrollY]);

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-transform duration-300 ${
        isVisible ? "translate-y-0" : "-translate-y-full"
      }`}
    >
      <div className="backdrop-blur-sm bg-earth-50/80 border-b border-earth-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo / Brand */}
            <Link
              href="/"
              className="flex items-center space-x-3 group"
            >
              <div className="font-serif text-xl md:text-2xl text-deep-900 group-hover:text-frequency transition-colors">
                Curiana Radio
              </div>
              <div className="hidden sm:block text-sm text-earth-600 font-sans tracking-wide">
                88.8 FM
              </div>
            </Link>

            {/* Navigation Items */}
            {/* Con Galería son cuatro enlaces visibles en móvil, y a 375px no
                caben. Hasta sm se aprietan cuerpo y espaciado, y la fila puede
                desplazarse en horizontal: así ninguna sección desaparece del
                menú en pantallas estrechas ni empuja la página de lado. De sm
                en adelante sobra sitio y todo vuelve a su tamaño. */}
            <div className="flex items-center space-x-3 sm:space-x-6 min-w-0 overflow-x-auto sm:overflow-x-visible [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
              {/* Edition Number (if on edition page) */}
              {editionNumber && (
                <div className="font-serif text-lg text-deep-800">
                  #{editionNumber}
                </div>
              )}

              {/* Archive Link */}
              <Link
                href="/archivo"
                className="shrink-0 whitespace-nowrap text-xs sm:text-sm font-sans text-deep-700 hover:text-frequency transition-colors tracking-normal sm:tracking-wide uppercase"
              >
                Archivo
              </Link>

              {/* JAI Sounds Link */}
              <Link
                href="/jai-sounds"
                className="shrink-0 whitespace-nowrap text-xs sm:text-sm font-sans text-deep-700 hover:text-frequency transition-colors tracking-normal sm:tracking-wide uppercase"
              >
                JAI Sounds
              </Link>

              {/* Galería Link */}
              <Link
                href="/galeria"
                className="shrink-0 whitespace-nowrap text-xs sm:text-sm font-sans text-deep-700 hover:text-frequency transition-colors tracking-normal sm:tracking-wide uppercase"
              >
                Galería
              </Link>

              {/* Simulador Link */}
              <Link
                href="/simulador"
                className="shrink-0 whitespace-nowrap text-xs sm:text-sm font-sans text-deep-700 hover:text-frequency transition-colors tracking-normal sm:tracking-wide uppercase"
              >
                Simulador
              </Link>

              {/* About Link (optional) */}
              <Link
                href="/sobre"
                className="hidden md:block shrink-0 whitespace-nowrap text-xs sm:text-sm font-sans text-deep-700 hover:text-frequency transition-colors tracking-normal sm:tracking-wide uppercase"
              >
                Sobre
              </Link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
