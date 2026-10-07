"use client";

import { useId, useState, type FormEvent } from "react";
import { medir } from "@/lib/analitica";

// El formulario de suscripción de la landing. El envío va al proveedor del
// newsletter, que se configura con NEXT_PUBLIC_SUSCRIPCION_URL (un endpoint
// que acepte un POST de formulario con el campo `email`, como el embed de
// Buttondown). Sin proveedor el formulario se muestra deshabilitado y lo
// dice: nunca un "Señal registrada" que no registró nada.
const PROVEEDOR = process.env.NEXT_PUBLIC_SUSCRIPCION_URL;
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// Dos formas: la de la landing (input y botón separados) y la del pie de la
// noche (shell 1a: input y botón unidos en un solo borde, SINTONIZAR → en
// mono). En las dos el botón es el acento de la noche con tinta de fondo
// (10.2:1); el naranja con texto blanco daba 2.8:1.
export default function Suscripcion({
  variante = "landing",
}: {
  variante?: "landing" | "pie";
}) {
  const pie = variante === "pie";
  const id = useId();
  const [email, setEmail] = useState("");
  const [estado, setEstado] = useState<
    "quieto" | "enviando" | "listo" | "error"
  >("quieto");
  const [aviso, setAviso] = useState("");

  async function alEnviar(e: FormEvent) {
    e.preventDefault();
    if (!PROVEEDOR) return;
    if (!EMAIL.test(email.trim())) {
      setAviso("Revisa el correo: falta algo para que la señal llegue.");
      return;
    }
    setAviso("");
    setEstado("enviando");
    try {
      const datos = new FormData();
      datos.set("email", email.trim());
      // no-cors: los embeds de newsletter no devuelven CORS; si la red falla,
      // fetch lanza y se avisa.
      await fetch(PROVEEDOR, { method: "POST", body: datos, mode: "no-cors" });
      setEstado("listo");
      medir("suscripcion", { desde: window.location.pathname });
    } catch {
      setEstado("error");
      setAviso("La señal no salió. Prueba otra vez en un momento.");
    }
  }

  if (estado === "listo") {
    return (
      <p
        role="status"
        className="m-0 border-l-4 border-(--noche-acento)/30 pl-4 font-mono text-[0.85rem] text-(--noche-hueso)"
      >
        Señal registrada — quedaste en la frecuencia.
      </p>
    );
  }

  return (
    <form onSubmit={alEnviar} noValidate className="flex flex-col gap-2.5">
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
          disabled={!PROVEEDOR}
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          aria-describedby={aviso ? `${id}-aviso` : undefined}
          aria-invalid={aviso && estado !== "error" ? true : undefined}
          placeholder={pie ? "tu@correo" : "tu@correo.com"}
          className={`min-w-0 flex-1 bg-(--noche-fondo) px-3.5 py-[13px] text-sm text-(--noche-hueso) placeholder:text-(--noche-dato) disabled:cursor-not-allowed disabled:opacity-60 ${
            pie
              ? "border-0"
              : "min-w-[200px] rounded-lg border border-(--noche-filete-fuerte) px-4"
          }`}
        />
        <button
          type="submit"
          disabled={!PROVEEDOR || estado === "enviando"}
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
      {aviso && (
        <p
          id={`${id}-aviso`}
          role="alert"
          className="m-0 font-mono text-[0.72rem] text-(--noche-hueso-2)"
        >
          {aviso}
        </p>
      )}
      {!PROVEEDOR && (
        <p className="m-0 font-mono text-[0.72rem] tracking-[0.14em] text-(--noche-hueso-2)">
          LA SUSCRIPCIÓN ABRE PRONTO
        </p>
      )}
    </form>
  );
}
