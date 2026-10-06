import type { Piel } from "./tipos";

// La noche de la v1: Lora para titular y susurrar, Inter para leer, mono para
// el dato. El acento es el oro de arena del shell (--noche-acento), y en claro
// la radio pasa al papel con su oro legible.
export const radio: Piel = {
  id: "radio",
  nombre: "La radio",
  concepto: "La emisora misma: la noche en movimiento de la v1, desde donde transmite todo lo demás.",
  manual: "BRAND_MVP §3.1, §10 y §13 · design_handoff_senales_luces",
  nativo: "oscuro",
  alterno: true,
  atributos: { "data-radio": "noche" },
  capitular: false,
};
