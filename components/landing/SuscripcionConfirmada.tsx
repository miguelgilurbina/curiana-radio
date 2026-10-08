"use client";

import { useEffect, useRef } from "react";
import { medir } from "@/lib/analitica";
import type { Tema } from "@/lib/newsletter/suscriptor";

// Lo que pasa en el navegador cuando una suscripción queda confirmada
// (/suscripcion/confirmar): se mide —aquí, y no al enviar el formulario,
// porque recién ahora hay un suscriptor de verdad— y se borra el token de la
// barra, que lleva el correo firmado (no cifrado) y no tiene por qué quedar
// en el historial ni en una captura. No pinta nada.
export default function SuscripcionConfirmada({ tema }: { tema: Tema }) {
  const hecho = useRef(false);
  useEffect(() => {
    if (hecho.current) return;
    hecho.current = true;
    medir("suscripcion", { desde: tema });
    const url = new URL(window.location.href);
    if (url.searchParams.has("t")) {
      url.searchParams.delete("t");
      window.history.replaceState(null, "", `${url.pathname}${url.search}${url.hash}`);
    }
  }, [tema]);
  return null;
}
