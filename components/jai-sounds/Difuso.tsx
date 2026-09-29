"use client";

import { useEffect, useRef, type ReactNode } from "react";

/**
 * Un fragmento del escrito que se enfoca al pasar por el centro de la
 * pantalla y se vuelve a difuminar al irse — el mensaje atraviesa la página
 * como una señal que entra y sale del dial.
 *
 * El atributo lo pone el efecto, nunca el servidor: sin JS, o con
 * movimiento reducido, el texto se queda nítido y se lee igual.
 */
export default function Difuso({
  children,
  className = "",
}: {
  children: ReactNode;
  className?: string;
}) {
  const ref = useRef<HTMLParagraphElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el || !("IntersectionObserver" in window)) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    el.dataset.difuso = "lejos";
    const observador = new IntersectionObserver(
      ([entrada]) => {
        el.dataset.difuso = entrada.isIntersecting ? "cerca" : "lejos";
      },
      // Nítido solo en la franja central: arriba y abajo, todavía señal.
      { rootMargin: "-22% 0px -22% 0px" }
    );
    observador.observe(el);
    return () => {
      observador.disconnect();
      delete el.dataset.difuso;
    };
  }, []);

  return (
    <p ref={ref} className={`jai-difuso ${className}`}>
      {children}
    </p>
  );
}
