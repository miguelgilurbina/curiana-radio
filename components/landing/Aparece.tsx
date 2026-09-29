"use client";

import { useEffect, useRef, type ReactNode } from "react";

// La entrada de secciones de la landing: fade de 0.6 s subiendo 10 px, una
// sola vez, cuando la sección entra en pantalla. Solo se esconde lo que al
// hidratar todavía está abajo: sin JS (o con movimiento reducido) todo se ve
// desde el principio, y lo que ya está a la vista no parpadea.
export default function Aparece({ children, className = "" }: { children: ReactNode; className?: string }) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    if (el.getBoundingClientRect().top < window.innerHeight) return;
    el.dataset.oculto = "";
    const io = new IntersectionObserver(
      ([entrada]) => {
        if (!entrada.isIntersecting) return;
        delete el.dataset.oculto;
        io.disconnect();
      },
      { rootMargin: "0px 0px -8% 0px" },
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);

  return (
    <div ref={ref} className={`noche-aparece ${className}`}>
      {children}
    </div>
  );
}
