"use client";

import { useEffect, useRef, useState, type ReactNode } from "react";

// «Amanecer», el movimiento de entrada del manual de Kaketiana: la sección
// sube 14px y aparece, 600ms, una sola vez, al llegar al viewport. Mejora
// progresiva: el servidor la rinde visible, y al montar sólo se esconde lo que
// todavía está bajo el pliegue — lo que ya se ve no parpadea. Con
// prefers-reduced-motion no se mueve nada (lo resuelve el CSS de .kk-amanecer).
type Estado = "quieto" | "espera" | "visto";

export default function Amanecer({
  children,
  className = "",
  as: Tag = "div",
  id,
}: {
  children: ReactNode;
  className?: string;
  as?: "div" | "section";
  id?: string;
}) {
  const ref = useRef<HTMLElement | null>(null);
  const [estado, setEstado] = useState<Estado>("quieto");

  useEffect(() => {
    const el = ref.current;
    if (!el || typeof IntersectionObserver === "undefined") return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    // Ya en pantalla al montar: se queda como está, sin animar.
    if (el.getBoundingClientRect().top < window.innerHeight) return;
    // Decidir qué se esconde depende del DOM montado: no hay otra forma.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setEstado("espera");
    const io = new IntersectionObserver(
      (entradas) => {
        for (const e of entradas) {
          if (e.isIntersecting) {
            setEstado("visto");
            io.unobserve(e.target);
          }
        }
      },
      { rootMargin: "0px 0px -10% 0px" },
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);

  return (
    <Tag
      ref={ref as React.Ref<HTMLDivElement>}
      id={id}
      className={`kk-amanecer ${className}`}
      data-amanecer={estado === "quieto" ? undefined : estado}
    >
      {children}
    </Tag>
  );
}
