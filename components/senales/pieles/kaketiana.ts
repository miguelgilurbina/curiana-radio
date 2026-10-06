import type { Piel } from "./tipos";

// La placa 6b: Fraunces WONK en la display, la prosa del ensayo, la cita en
// serif sobre papel hundido con su riel de almagre, la capitular en rúbrica y
// los enlaces en salina. Su oscuro es tinta parda, no la noche azul del Acto I.
export const kaketiana: Piel = {
  id: "kaketiana",
  nombre: "Sal y almagre",
  concepto: "La placa clara, mineral y arqueológica de Kaketiana: se lee como un ensayo de investigación.",
  manual: "BRAND_MVP §11 · design_handoff_kaketiana (6b, 7a) · design_handoff_senales_luces",
  nativo: "claro",
  alterno: true,
  atributos: { "data-sim-theme": "cronista", "data-kk": "", "data-kk-dir": "sal" },
  capitular: true,
};
