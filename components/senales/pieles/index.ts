import type { PielId } from "@/lib/senales-comun";
import type { Piel } from "./tipos";
import { radio } from "./radio";
import { kaketiana } from "./kaketiana";
import { jaiSounds } from "./jai-sounds";
import { galeria } from "./galeria";
import { buchibe } from "./buchibe";

// El motor de pieles de Señales. Una plantilla y N pieles: la estructura de
// una señal es siempre la misma (miga, título, sumario, dato, portada, cuerpo
// a 65ch, firma, pie); la piel decide la superficie, las voces, la tinta y lo
// que va sobre la cabecera. La idea (Miguel, 2026-10-04) es que la página sea
// «una máquina estética de conceptos»: cada concepto del proyecto puede tener
// su piel —una por arista hoy; mañana otras, como «Noticias Manifiesto»— y
// cualquier señal puede vestirse con cualquiera.
//
// La arista dice DÓNDE aparece una señal; la piel, CÓMO se ve. Cada arista
// trae su piel por defecto (PIEL_DE_ARISTA) y la señal puede pedir otra con
// `piel:` en el frontmatter.
//
// Una piel es DATOS (design_handoff_senales_luces): su tinta y sus voces son
// un bloque de CSS que mapea los tokens de su sección al juego común de
// alias --e-* (globals.css, «El motor de pieles»); la plantilla sólo lee los
// alias. Aquí queda su ficha.
//
// Cómo se crea una piel (BRAND_MVP §12):
//   1. Nómbrala en PIELES_IDS (lib/senales-comun.ts).
//   2. En globals.css: sus tokens bajo su atributo de tema, si trae colores
//      propios, y su bloque `[data-piel="<id>"]` con TODOS los alias --e-*
//      (copia uno vecino). Su otra luz, si existe, en
//      `html[data-luz="…"] [data-piel="<id>"]`, redefiniendo sus tokens.
//   3. Su ficha en esta carpeta: id, nombre, concepto, manual, nativo,
//      alterno, atributos y capitular; `cabecera`, `Antetitulo`, `raiz` o
//      `script` si los necesita.
//   4. Regístrala abajo. TypeScript no compila mientras falte alguna.
//   5. Documéntala en la tabla de BRAND_MVP §12, con el contraste medido.

export const PIELES: Record<PielId, Piel> = {
  radio,
  kaketiana,
  "jai-sounds": jaiSounds,
  galeria,
  buchibe,
};

export type { Piel } from "./tipos";
