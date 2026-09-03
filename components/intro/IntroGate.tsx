"use client";

import { useCallback, useEffect, useState, useSyncExternalStore } from "react";
import { useRouter } from "next/navigation";
import IntroCuriana from "./IntroCuriana";

// La puerta: la intro se ve UNA vez por sesión en la landing. Recuerda con
// sessionStorage (no localStorage: la próxima visita vuelve a sintonizar).
// Con `siempre` (ruta /intro) se muestra de todos modos y al final navega a /.

export const CLAVE_INTRO_VISTA = "curianaIntroVista";
const ID_ESTILO_PREVIO = "intro-curiana-previo";

// El servidor rinde la cáscara de la intro por defecto (para que el primer
// paint de un visitante nuevo sea la intro, no la landing). Si la sesión ya
// la vio y recarga /, este script — que corre al parsear el HTML, antes de
// hidratar — la esconde para que el índigo no parpadee mientras carga el
// JS. El estilo se retira en cuanto React decide.
const SCRIPT_PREVIO =
  `try{if(sessionStorage.getItem("${CLAVE_INTRO_VISTA}")==="1"){` +
  `var s=document.createElement("style");s.id="${ID_ESTILO_PREVIO}";` +
  `s.textContent=".intro-curiana{display:none}";document.head.appendChild(s)}}catch(e){}`;

function yaVista(): boolean {
  try {
    return sessionStorage.getItem(CLAVE_INTRO_VISTA) === "1";
  } catch {
    return false;
  }
}

function marcarVista() {
  try {
    sessionStorage.setItem(CLAVE_INTRO_VISTA, "1");
  } catch {
    // modo privado estricto: la intro se repetirá, nada más
  }
}

const sinSuscripcion = () => () => {};
const desconocido = () => null;

export default function IntroGate({ siempre = false }: { siempre?: boolean }) {
  const router = useRouter();
  // null = el servidor (y la hidratación) todavía no saben; boolean = el cliente sí.
  const vista = useSyncExternalStore<boolean | null>(sinSuscripcion, yaVista, desconocido);
  const [cerrada, setCerrada] = useState(false);

  useEffect(() => {
    if (vista !== null) document.getElementById(ID_ESTILO_PREVIO)?.remove();
  }, [vista]);

  useEffect(() => {
    if (siempre) router.prefetch("/");
  }, [siempre, router]);

  const fin = useCallback(() => {
    marcarVista();
    if (siempre) router.replace("/");
    else setCerrada(true);
  }, [siempre, router]);

  if (cerrada || (vista === true && !siempre)) return null;

  return (
    <>
      {vista === null && !siempre && (
        <script dangerouslySetInnerHTML={{ __html: SCRIPT_PREVIO }} />
      )}
      {/* Sin JS no hay viaje ni botón que funcione: mejor no tapar la landing. */}
      <noscript>
        <style>{".intro-curiana{display:none}"}</style>
      </noscript>
      <IntroCuriana activa={vista !== null} amanecer={!siempre} onFin={fin} />
    </>
  );
}
