import type { Piel } from "./tipos";

// La sala: la única superficie acromática. La interfaz calla donde el arte
// habla: las figuras salen de la columna hasta 72rem y el texto no lleva color.
export const galeria: Piel = {
  id: "galeria",
  nombre: "La sala neutra",
  concepto: "La sala de la Galería: gris sin matiz para que la imagen sea lo único que tiene color.",
  manual: "BRAND_MVP §3.1 (superficies de sección) · GALERIA.md · design_handoff_senales_luces",
  nativo: "oscuro",
  alterno: true,
  atributos: { "data-galeria-theme": "sala" },
  capitular: false,
};
