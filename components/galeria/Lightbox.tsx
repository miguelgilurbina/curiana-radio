"use client";

import { useCallback, useEffect, useRef } from "react";
import Link from "next/link";
import ImagenObra from "./ImagenObra";
import type { ObraGrid } from "@/types/galeria";

const FOCUSABLES =
  'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])';

interface LightboxProps {
  obras: ObraGrid[];
  blobBase: string | null;
  indice: number;
  onCerrar: () => void;
  onIr: (indice: number) => void;
}

export default function Lightbox({
  obras,
  blobBase,
  indice,
  onCerrar,
  onIr,
}: LightboxProps) {
  const dialogRef = useRef<HTMLDivElement>(null);
  const obra = obras[indice];

  const hayAnterior = indice > 0;
  const haySiguiente = indice < obras.length - 1;

  const anterior = useCallback(() => {
    if (hayAnterior) onIr(indice - 1);
  }, [hayAnterior, indice, onIr]);

  const siguiente = useCallback(() => {
    if (haySiguiente) onIr(indice + 1);
  }, [haySiguiente, indice, onIr]);

  // Al abrir: recordar quién tenía el foco para devolvérselo al cerrar. Sin
  // esto, cerrar el lightbox tira el foco al <body> y quien navega por teclado
  // pierde el sitio en la grilla.
  useEffect(() => {
    const previo = document.activeElement as HTMLElement | null;
    dialogRef.current?.focus();
    return () => previo?.focus?.();
  }, []);

  // Bloquear el scroll del fondo mientras el diálogo está abierto.
  useEffect(() => {
    const previo = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = previo;
    };
  }, []);

  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        e.preventDefault();
        onCerrar();
        return;
      }
      if (e.key === "ArrowLeft") {
        e.preventDefault();
        anterior();
        return;
      }
      if (e.key === "ArrowRight") {
        e.preventDefault();
        siguiente();
        return;
      }
      // Trampa de foco: el Tab no debe escaparse a la página de atrás.
      if (e.key === "Tab") {
        const nodos =
          dialogRef.current?.querySelectorAll<HTMLElement>(FOCUSABLES);
        if (!nodos || nodos.length === 0) return;
        const primero = nodos[0];
        const ultimo = nodos[nodos.length - 1];
        const activo = document.activeElement;
        if (e.shiftKey && (activo === primero || activo === dialogRef.current)) {
          e.preventDefault();
          ultimo.focus();
        } else if (!e.shiftKey && activo === ultimo) {
          e.preventDefault();
          primero.focus();
        }
      }
    };
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, [anterior, siguiente, onCerrar]);

  if (!obra) return null;

  const proporcion = obra.w && obra.h ? obra.w / obra.h : 4 / 5;

  return (
    <div
      className="fixed inset-0 z-[100] flex items-center justify-center bg-deep-900/95 p-4 backdrop-blur-sm sm:p-8"
      onClick={(e) => {
        if (e.target === e.currentTarget) onCerrar();
      }}
    >
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="lightbox-titulo"
        tabIndex={-1}
        className="relative flex max-h-full w-full max-w-6xl flex-col gap-6 overflow-y-auto outline-none lg:flex-row lg:items-center"
      >
        {/* Imagen */}
        <div className="flex min-w-0 flex-1 items-center justify-center">
          <div
            className="relative max-h-[70vh] w-full overflow-hidden"
            style={{ aspectRatio: `${proporcion}` }}
          >
            <ImagenObra
              obra={obra}
              blobBase={blobBase}
              prioridad
              sizes="(max-width: 1024px) 100vw, 66vw"
              className="h-full w-full object-contain"
            />
          </div>
        </div>

        {/* Ficha lateral */}
        <div className="w-full shrink-0 text-earth-100 lg:w-80">
          <div className="mb-3 font-sans text-xs tracking-[0.2em] uppercase text-earth-400">
            {indice + 1} / {obras.length}
          </div>
          <h2
            id="lightbox-titulo"
            className="mb-4 font-serif text-2xl leading-tight text-white"
          >
            {obra.titulo}
          </h2>

          <Link
            href={`/galeria/${obra.slug}`}
            className="inline-block border-b border-frequency font-sans text-sm text-frequency transition-colors hover:border-white hover:text-white"
          >
            Ver ficha completa
          </Link>

          {/* Navegación */}
          <div className="mt-6 flex gap-3">
            <button
              type="button"
              onClick={anterior}
              disabled={!hayAnterior}
              className="border border-earth-600 px-4 py-2 font-sans text-sm text-earth-200 transition-colors hover:border-frequency hover:text-frequency disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:border-earth-600 disabled:hover:text-earth-200"
            >
              ← Anterior
            </button>
            <button
              type="button"
              onClick={siguiente}
              disabled={!haySiguiente}
              className="border border-earth-600 px-4 py-2 font-sans text-sm text-earth-200 transition-colors hover:border-frequency hover:text-frequency disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:border-earth-600 disabled:hover:text-earth-200"
            >
              Siguiente →
            </button>
          </div>
        </div>

        <button
          type="button"
          onClick={onCerrar}
          aria-label="Cerrar"
          className="absolute right-0 top-0 flex h-10 w-10 items-center justify-center border border-earth-600 text-xl leading-none text-earth-200 transition-colors hover:border-frequency hover:text-frequency"
        >
          ×
        </button>
      </div>
    </div>
  );
}
