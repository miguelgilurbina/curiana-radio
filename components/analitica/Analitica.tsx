"use client";

import { useEffect } from "react";
import { Analytics } from "@vercel/analytics/next";
import { SpeedInsights } from "@vercel/speed-insights/next";
import { medir } from "@/lib/analitica";

// Visitas (Web Analytics), rendimiento real de quien visita (Speed Insights)
// y las salidas del sitio. Ambos scripts los sirve el propio dominio
// (/_vercel/…), sin cookies; hay que activarlos en el panel del proyecto.
export default function Analitica() {
  // Un solo oyente para todos los enlaces externos, en vez de marcar cada
  // <a>: captura también los que vienen del markdown del vault.
  useEffect(() => {
    function alClic(e: MouseEvent) {
      const a = (e.target as Element | null)?.closest?.("a[href]");
      if (!(a instanceof HTMLAnchorElement)) return;
      let url: URL;
      try {
        url = new URL(a.href);
      } catch {
        return;
      }
      if (!url.protocol.startsWith("http") || url.host === window.location.host) return;
      medir("salida", { destino: url.hostname.replace(/^www\./, ""), desde: window.location.pathname });
    }
    document.addEventListener("click", alClic, { capture: true });
    return () => document.removeEventListener("click", alClic, { capture: true });
  }, []);

  return (
    <>
      <Analytics />
      <SpeedInsights />
    </>
  );
}
