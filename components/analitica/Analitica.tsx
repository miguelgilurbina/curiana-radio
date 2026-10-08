"use client";

import { useEffect } from "react";
import { Analytics } from "@vercel/analytics/next";
import { SpeedInsights } from "@vercel/speed-insights/next";
import { antesDeEnviar, medir } from "@/lib/analitica";

// Visitas (Web Analytics), rendimiento real de quien visita (Speed Insights)
// y las salidas del sitio. Ambos scripts los sirve el propio dominio
// (/_vercel/…), sin cookies; hay que activarlos en el panel del proyecto.
// Va UNA vez, en el layout raíz: fuera de él, cada script se cargaría dos
// veces y contaría doble.
//
// Sin `mode`: lo detecta solo. Con `next dev` (y `vercel dev`) carga el
// script de depuración, que escribe cada vista y cada evento en la consola y
// no envía nada. En Vercel, las vistas previas se guardan aparte de
// producción (el panel muestra Production por defecto).
//
// `antesDeEnviar` (lib/analitica.ts) limpia cada URL antes de que salga: sin
// query salvo los utm_*, sin hash, y nada de las páginas de /suscripcion/.
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
      <Analytics beforeSend={antesDeEnviar} />
      <SpeedInsights beforeSend={antesDeEnviar} />
    </>
  );
}
