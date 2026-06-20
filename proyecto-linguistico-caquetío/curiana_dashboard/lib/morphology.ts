// Reglas morfológicas del caquetío reconstruido, espejo liviano de las
// REGLAS_* en curiana_sim/curiana_lexicon.py. Solo para mostrar un tooltip
// gramatical sobre afijos reconocidos en el feed del dashboard.

export interface MorphemeGloss {
  gloss: string;
  desc: string;
}

// Sufijos (raíz + sufijo)
export const SUFFIX_RULES: Record<string, MorphemeGloss> = {
  ka: { gloss: "completivo", desc: "acción ya terminada" },
  ni: { gloss: "continuativo", desc: "acción en curso, ahora mismo" },
  da: { gloss: "prospectivo", desc: "intención o futuro" },
  ana: { gloss: "lugar de", desc: "topónimo, lugar asociado a la raíz" },
  gua: { gloss: "región de", desc: "área amplia asociada a la raíz" },
  bana: { gloss: "orilla de", desc: "borde, límite, punto de transición" },
  ko: { gloss: "agente masc.", desc: "hombre asociado a la raíz" },
  sha: { gloss: "agente fem.", desc: "mujer asociada a la raíz" },
  kana: { gloss: "plural/colectivo", desc: "grupo de, todos los..." },
  naiki: { gloss: "lengua de", desc: "idioma o habla de un pueblo" },
};

// Prefijos (prefijo + raíz)
export const PREFIX_RULES: Record<string, MorphemeGloss> = {
  ta: { gloss: "mi (posesivo)", desc: "1ra persona singular" },
  pi: { gloss: "tu (posesivo)", desc: "2da persona singular" },
  nü: { gloss: "su (posesivo)", desc: "3ra persona singular" },
  wa: { gloss: "nuestro (posesivo)", desc: "1ra persona plural" },
  ma: { gloss: "sin / no", desc: "privativo, negativo" },
  ka: { gloss: "el/la de", desc: "posesivo genérico, asociativo" },
};
