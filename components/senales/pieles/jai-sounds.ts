import { frauncesJai } from "@/app/jai-sounds/fraunces-jai";
import { SCRIPT_SEMILLA } from "@/lib/jai-rotacion";
import type { Piel } from "./tipos";

// El dial: la Fraunces de JAI en sus voces, el dato en minúscula, el riel de
// 3px en la señal, radios 0 y NUNCA el naranja. La señal rota de matiz con la
// semilla de la sesión, como en la sección: por eso carga su fuente y su
// script.
export const jaiSounds: Piel = {
  id: "jai-sounds",
  nombre: "El dial",
  concepto: "La cabina de noche de JAI Sounds: se lee al oído, y el color de la señal cambia con cada visita.",
  manual: "design_handoff_jai_sounds · globals.css («Tema Dial») · design_handoff_senales_luces",
  nativo: "oscuro",
  alterno: true,
  atributos: { "data-jai-theme": "dial" },
  capitular: false,
  raiz: frauncesJai.variable,
  script: SCRIPT_SEMILLA,
};
