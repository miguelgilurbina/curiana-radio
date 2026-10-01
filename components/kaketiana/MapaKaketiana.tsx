"use client";

import { useEffect, useRef, useState } from "react";
import type * as LeafletNS from "leaflet";
import "leaflet/dist/leaflet.css";
import type { PuntoMapa } from "@/lib/mapa";
import { ESTILO_NIVEL, OCRE } from "@/lib/mapa-estilo";

// El mapa de la portada de Kaketiana: los topónimos del canon sobre el mapa de
// hoy. Cada punto lleva la gramática del trazo del manual (design_handoff_
// kaketiana): sólido es evidencia, firme es inferencia, discontinuo es duda.
// Lo que mide el trazo es la LECTURA del nombre (su nivel en el canon), no si
// el lugar existe: el nombre está en una fuente y en el mapa. Las teselas van
// en sepia, para que el mapa sea de la placa de sal y no un mapa cualquiera.

const TESELAS = "https://tile.openstreetmap.org/{z}/{x}/{y}.png";
const ATRIBUCION = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>';
function escapar(s: string): string {
  return s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]!);
}

export default function MapaKaketiana({ puntos }: { puntos: PuntoMapa[] }) {
  const contenedor = useRef<HTMLDivElement>(null);
  const [estado, setEstado] = useState<"cargando" | "listo" | "falla">("cargando");

  useEffect(() => {
    let vivo = true;
    let mapa: LeafletNS.Map | null = null;
    let observador: ResizeObserver | null = null;
    (async () => {
      try {
        const L = await import("leaflet");
        if (!vivo || !contenedor.current) return;
        mapa = L.map(contenedor.current, { scrollWheelZoom: false, attributionControl: true });
        L.tileLayer(TESELAS, { attribution: ATRIBUCION, maxZoom: 16 }).addTo(mapa);
        for (const p of puntos) {
          const e = ESTILO_NIVEL[p.nivel];
          L.circleMarker([p.lat, p.lon], {
            radius: e.radio,
            color: OCRE,
            weight: 1.5,
            fillColor: e.relleno,
            fillOpacity: e.opacidad,
            dashArray: e.trazo,
          })
            .bindTooltip(
              `<em>${escapar(p.forma)}</em> · ${escapar(p.nombre_en_el_mapa)}` +
                (p.glosa ? `<br><span style="opacity:.75">${escapar(p.glosa)}</span>` : "") +
                `<br><span style="opacity:.75">${
                  p.nivel === "sin" ? `sin lectura: ${escapar(p.motivo ?? "")}` : `lectura ${p.nivel}`
                }</span>`,
              { direction: "top", opacity: 0.95 },
            )
            .addTo(mapa);
        }
        const limites = puntos.length
          ? L.latLngBounds(puntos.map((p) => [p.lat, p.lon] as [number, number])).pad(0.08)
          : null;
        let encuadrado = false;
        const encuadrar = () => {
          if (!mapa) return;
          mapa.invalidateSize();
          if (encuadrado || !contenedor.current?.clientHeight) return;
          if (limites) mapa.fitBounds(limites);
          else mapa.setView([11.75, -70.0], 9);
          encuadrado = true;
        };
        encuadrar();
        observador = typeof ResizeObserver !== "undefined" ? new ResizeObserver(encuadrar) : null;
        observador?.observe(contenedor.current);
        setEstado("listo");
      } catch {
        if (vivo) setEstado("falla");
      }
    })();
    return () => {
      vivo = false;
      observador?.disconnect();
      mapa?.remove();
    };
  }, [puntos]);

  return (
    <div className="kk-mapa relative h-full w-full">
      <div ref={contenedor} className="h-full w-full" aria-label="Mapa de los topónimos del canon" role="region" />
      {estado !== "listo" && (
        <p className="absolute inset-0 flex items-center justify-center sim-mono text-[0.66rem] text-(--sim-ink-soft)">
          {estado === "falla" ? "[ el mapa no cargó: la lista está debajo ]" : "[ mapa · la Kaketiana ]"}
        </p>
      )}
    </div>
  );
}
