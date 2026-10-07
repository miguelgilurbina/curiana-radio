"use client";

import { useEffect, useRef } from "react";
import { medir } from "@/lib/analitica";

// Una marca invisible al final de un texto largo. Cuenta como lectura cuando
// aparece en pantalla y la persona lleva al menos MINIMO en la página: así un
// salto al pie, o un texto corto que cabe entero al cargar, no pasan por
// lectura. Una vez por visita a la página.
const MINIMO_MS = 20_000;

export default function FinDeLectura({ pagina }: { pagina: string }) {
  const marca = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = marca.current;
    if (!el) return;
    const desde = performance.now();
    let contado = false;
    let espera: ReturnType<typeof setTimeout> | undefined;
    const contar = () => {
      if (contado) return;
      contado = true;
      medir("lectura", { pagina });
      observador.disconnect();
    };
    const observador = new IntersectionObserver(([entrada]) => {
      clearTimeout(espera);
      if (!entrada.isIntersecting) return;
      const falta = MINIMO_MS - (performance.now() - desde);
      // Si llegó al final antes del mínimo y se queda ahí, cuenta al cumplirlo.
      if (falta <= 0) contar();
      else espera = setTimeout(contar, falta);
    });
    observador.observe(el);
    return () => {
      clearTimeout(espera);
      observador.disconnect();
    };
  }, [pagina]);

  return <div ref={marca} aria-hidden="true" className="h-px" />;
}
