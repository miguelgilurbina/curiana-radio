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

export default function Suscripcion() {
  const id = useId();
  const [email, setEmail] = useState("");
  const [estado, setEstado] = useState<"quieto" | "enviando" | "listo" | "error">("quieto");
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
      <p role="status" className="m-0 border-l-4 border-frequency/30 pl-4 font-mono text-[0.85rem] text-(--noche-hueso)">
        Señal registrada — quedaste en la frecuencia.
      </p>
    );
  }

  return (
    <form onSubmit={alEnviar} noValidate className="flex flex-col gap-2.5">
      <div className="flex flex-wrap gap-2.5">
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
          placeholder="tu@correo.com"
          aria-describedby={aviso ? `${id}-aviso` : undefined}
          aria-invalid={aviso && estado !== "error" ? true : undefined}
          className="min-w-[200px] flex-1 rounded-lg border border-(--noche-filete-fuerte) bg-(--noche-fondo) px-4 py-[13px] text-sm text-(--noche-hueso) placeholder:text-(--noche-hueso-2)/70 disabled:cursor-not-allowed disabled:opacity-60"
        />
        <button
          type="submit"
          disabled={!PROVEEDOR || estado === "enviando"}
          className="cursor-pointer rounded-[2px] bg-frequency px-[22px] py-[13px] text-[0.78rem] font-semibold uppercase tracking-[0.2em] text-white transition-all duration-300 hover:bg-(--noche-hueso) hover:text-(--noche-fondo) disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:bg-frequency disabled:hover:text-white"
        >
          {estado === "enviando" ? "Enviando…" : "Sintonizar"}
        </button>
      </div>
      {aviso && (
        <p id={`${id}-aviso`} role="alert" className="m-0 font-mono text-[0.72rem] text-(--noche-hueso-2)">
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
