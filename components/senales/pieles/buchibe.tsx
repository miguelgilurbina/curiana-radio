import type { Piel } from "./tipos";

const FRAUNCES = "[font-family:var(--font-fraunces),var(--font-lora),Georgia,serif]";

/** La franja de su tarjeta en la landing: noche → ultramar, «Curiana Radio
 *  presenta» en oro. Va dentro de .buc-cabecera, así que no cambia de luz. */
function Presenta() {
  return (
    <div
      aria-hidden="true"
      className="flex flex-col items-center gap-0.5 px-6 py-4"
      style={{ background: "linear-gradient(180deg, var(--buc-noche), var(--buc-ultramar))" }}
    >
      <span className={`text-[0.8rem] uppercase tracking-[0.32em] text-(--buc-oro) ${FRAUNCES}`}>Curiana Radio</span>
      <span className={`text-[0.7rem] italic tracking-[0.18em] text-(--buc-oro) ${FRAUNCES}`}>presenta</span>
    </div>
  );
}

// El telón: la cabecera en el rojo teatral y el cuento en la noche ultramar,
// en serif, para leerse —o decirse— en voz alta. De día sólo pasa el cuerpo:
// el telón es el escenario, y el escenario no se prende.
export const buchibe: Piel = {
  id: "buchibe",
  nombre: "El telón",
  concepto: "Los Cuentos de Buchibe: se corre el telón y empieza el cuento, para leerse o decirse en voz alta.",
  manual: "BRAND_MVP §10 (la tarjeta de Buchibe) · globals.css («Tema Telón») · design_handoff_senales_luces",
  nativo: "oscuro",
  alterno: true,
  atributos: { "data-buchibe-theme": "telon" },
  capitular: true,
  cabecera: "buc-cabecera",
  Antetitulo: Presenta,
};
