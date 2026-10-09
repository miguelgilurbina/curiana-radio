"use client";

import { useEffect, useId, useRef, useState, type FormEvent } from "react";
import { normalizarEmail, TEMA, TEMA_POR_DEFECTO, TEMAS, type Tema } from "@/lib/newsletter/suscriptor";

// El formulario del newsletter (lo monta Suscripcion.tsx, que sabe si está
// abierto). Postea a /api/suscripcion, del mismo origen, y dice lo que de
// verdad pasó: que salió el correo para confirmar, que la señal no salió o
// que hubo demasiados intentos (el 429 del Firewall de Vercel). La
// suscripción se mide al confirmar, no aquí (SuscripcionConfirmada.tsx).
//
// Dos formas: la de la landing (input y botón separados) y la del pie de la
// noche (shell 1a: input y botón unidos en un solo borde, SINTONIZAR → en
// mono). En las dos el botón es el acento de la noche con tinta de fondo
// (10.2:1); el naranja con texto blanco daba 2.8:1. Arriba, el tema: un
// selector segmentado en mono, en hueso el elegido.

const AVISO = {
  correo: "Revisa el correo: falta algo para que la señal llegue.",
  red: "La señal no salió. Prueba otra vez en un momento.",
  muchos: "Demasiados intentos; espera un momento.",
};

type Estado = "quieto" | "enviando" | "listo" | "error";

export default function FormularioSuscripcion({
  variante,
  abierta,
}: {
  variante: "landing" | "pie";
  abierta: boolean;
}) {
  const pie = variante === "pie";
  const id = useId();
  const [email, setEmail] = useState("");
  const [tema, setTema] = useState<Tema>(TEMA_POR_DEFECTO);
  const [estado, setEstado] = useState<Estado>("quieto");
  const [aviso, setAviso] = useState("");
  const confirmacion = useRef<HTMLParagraphElement>(null);

  // El formulario desaparece al salir el correo: el foco pasa al aviso para
  // que no quede perdido en la página (y el lector de pantalla lo lea).
  useEffect(() => {
    if (estado === "listo") confirmacion.current?.focus();
  }, [estado]);

  async function alEnviar(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!abierta || estado === "enviando") return;
    const correo = normalizarEmail(email);
    if (!correo) {
      setEstado("quieto");
      setAviso(AVISO.correo);
      return;
    }
    const sitio = String(new FormData(e.currentTarget).get("sitio") ?? "");
    setAviso("");
    setEstado("enviando");
    try {
      const respuesta = await fetch("/api/suscripcion", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: correo, tema, sitio, desde: window.location.pathname }),
      });
      if (respuesta.ok) {
        setEstado("listo");
        return;
      }
      setEstado("error");
      setAviso(
        respuesta.status === 429 ? AVISO.muchos : respuesta.status === 400 ? AVISO.correo : AVISO.red,
      );
    } catch {
      setEstado("error");
      setAviso(AVISO.red);
    }
  }

  if (estado === "listo") {
    return (
      <p
        ref={confirmacion}
        tabIndex={-1}
        role="status"
        className="m-0 border-l-4 border-(--noche-acento)/30 pl-4 font-mono text-[0.85rem] text-(--noche-hueso)"
      >
        Revisa tu correo: te mandamos un enlace para confirmar.
      </p>
    );
  }

  return (
    // method y action por si alguien envía antes de que cargue el JS: que el
    // correo viaje en el cuerpo de un POST y no en la URL de un GET.
    <form
      method="post"
      action="/api/suscripcion"
      onSubmit={alEnviar}
      noValidate
      className="relative flex flex-col gap-2.5"
    >
      {abierta && (
        <fieldset disabled={estado === "enviando"} className="m-0 min-w-0 border-0 p-0">
          <legend className="sr-only">Qué quieres recibir</legend>
          <div
            className={`flex divide-x divide-(--noche-filete-fuerte) border border-(--noche-filete-fuerte) ${
              pie ? "" : "rounded-[2px]"
            }`}
          >
            {TEMAS.map((t) => (
              <label
                key={t}
                className={`flex flex-auto cursor-pointer items-center justify-center text-center font-mono uppercase leading-snug text-(--noche-hueso-2) transition-colors duration-300 hover:text-(--noche-hueso) has-checked:bg-(--noche-hueso) has-checked:text-(--noche-fondo) has-focus-visible:outline-2 has-focus-visible:-outline-offset-2 has-focus-visible:outline-(--noche-acento) has-disabled:cursor-not-allowed has-disabled:opacity-60 ${
                  // en el pie, tracking corto para que las dos quepan en una
                  // fila en la columna de escritorio (~237 px a 1280)
                  pie
                    ? "min-h-11 px-2 py-2 text-[0.625rem] tracking-[0.1em] text-balance lg:min-h-0"
                    : "min-h-11 px-3 py-2.5 text-[0.6875rem] tracking-[0.16em] text-balance"
                }`}
              >
                <input
                  type="radio"
                  name="tema"
                  value={t}
                  checked={tema === t}
                  onChange={() => setTema(t)}
                  className="sr-only"
                />
                {TEMA[t].etiqueta}
              </label>
            ))}
          </div>
        </fieldset>
      )}
      <div
        className={
          pie
            ? "flex flex-col border border-(--noche-filete-fuerte) lg:flex-row"
            : "flex flex-wrap gap-2.5"
        }
      >
        <label htmlFor={id} className="sr-only">
          Tu correo
        </label>
        <input
          id={id}
          type="email"
          name="email"
          autoComplete="email"
          required
          disabled={!abierta}
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          aria-describedby={aviso ? `${id}-aviso` : undefined}
          aria-invalid={aviso === AVISO.correo ? true : undefined}
          placeholder={pie ? "tu@correo" : "tu@correo.com"}
          className={`min-w-0 flex-1 bg-(--noche-fondo) px-3.5 py-[13px] text-sm text-(--noche-hueso) placeholder:text-(--noche-dato) disabled:cursor-not-allowed disabled:opacity-60 ${
            pie
              ? "border-0"
              : "min-w-[200px] rounded-lg border border-(--noche-filete-fuerte) px-4"
          }`}
        />
        <button
          type="submit"
          disabled={!abierta || estado === "enviando"}
          className={`cursor-pointer bg-(--noche-acento) uppercase text-(--noche-fondo) transition-all duration-300 hover:bg-(--noche-hueso) disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:bg-(--noche-acento) ${
            pie
              ? "min-h-12 px-4 font-mono text-[0.6875rem] font-bold tracking-[0.2em] whitespace-nowrap lg:min-h-0"
              : "rounded-[2px] px-[22px] py-[13px] text-[0.78rem] font-semibold tracking-[0.2em]"
          }`}
        >
          {estado === "enviando"
            ? "Enviando…"
            : pie
              ? "Sintonizar →"
              : "Sintonizar"}
        </button>
      </div>
      {/* El campo trampa (honeypot): fuera de la pantalla, fuera del tabulador
          y oculto a los lectores de pantalla. Si llega lleno, la ruta dice
          que sí y no hace nada. */}
      {abierta && (
        <div aria-hidden="true" className="absolute -left-[10000px] top-0 h-px w-px overflow-hidden">
          <label htmlFor={`${id}-sitio`}>Deja este campo vacío</label>
          <input id={`${id}-sitio`} type="text" name="sitio" tabIndex={-1} autoComplete="off" defaultValue="" />
        </div>
      )}
      {aviso && (
        <p
          id={`${id}-aviso`}
          role="alert"
          className="m-0 font-mono text-[0.72rem] text-(--noche-hueso-2)"
        >
          {aviso}
        </p>
      )}
      {!abierta && (
        <p className="m-0 font-mono text-[0.72rem] tracking-[0.14em] text-(--noche-hueso-2)">
          LA SUSCRIPCIÓN ABRE PRONTO
        </p>
      )}
    </form>
  );
}
