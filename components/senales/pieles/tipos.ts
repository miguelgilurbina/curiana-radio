import type { ComponentType } from "react";
import type { PielId } from "@/lib/senales-comun";
import type { Luz } from "@/lib/luz";

// La ficha de una piel. Una piel es un concepto estético completo, y es
// DATOS: su tinta y sus voces viven en globals.css («El motor de pieles»),
// como tokens de su sección mapeados al juego común de alias --e-*, que es
// lo único que lee la plantilla (app/senales/[slug]). Aquí va lo que el CSS
// no puede decir: de qué trata, de dónde sale, en qué luz nace y qué
// necesita cargar o poner sobre la cabecera.

export interface Piel {
  id: PielId;
  /** cómo se llama, para el manual y para elegirla */
  nombre: string;
  /** el concepto que viste: una frase */
  concepto: string;
  /** de dónde salen sus decisiones (un handoff, una sección del manual) */
  manual: string;
  /** su luz de origen: la identidad de su manual */
  nativo: Luz;
  /** si su otra luz está diseñada (su bloque html[data-luz] en globals.css);
   *  sin ella, la piel se queda en su luz y no ofrece el interruptor */
  alterno: boolean;
  /** los atributos de tema de su sección: activan sus tokens */
  atributos: Record<string, string>;
  /** si el primer párrafo abre con capitular (en --e-capitular) */
  capitular: boolean;
  /** clase extra de la cabecera (Buchibe: buc-cabecera, que fija el telón) */
  cabecera?: string;
  /** clases en la raíz de la página: las fuentes que la piel carga */
  raiz?: string;
  /** un script en línea que tiene que correr antes del primer pintado */
  script?: string;
  /** lo que va sobre la cabecera, a todo el ancho: la franja de Buchibe, la
   *  mancheta de un diario… */
  Antetitulo?: ComponentType;
}
