// Las voces de la plantilla de Señales. Cada clase lee los alias --e-* de la
// piel (globals.css, «El motor de pieles»): ninguna nombra una piel, así que
// la misma plantilla habla en la noche, en la sal, en el dial, en la sala o
// en el telón. El reparto es el del manual: el cartel grita, el oráculo
// susurra, el dato teclea.

export const VOZ = {
  /** el dato: mono 11px, con el tracking y la caja de la piel */
  dato: "font-mono text-[0.6875rem] leading-relaxed tracking-(--e-dato-tracking) [text-transform:var(--e-dato-caja)]",
  titulo:
    "font-(family-name:--e-tit-familia) [font-weight:var(--e-tit-peso)] [font-variation-settings:var(--e-tit-ejes)]",
  h2: "font-(family-name:--e-tit-familia) [font-weight:var(--e-tit-peso)] [font-variation-settings:var(--e-h2-ejes)]",
  /** el oráculo: sumario y firma */
  sumario:
    "font-(family-name:--e-sum-familia) [font-style:var(--e-sum-estilo)] [font-weight:var(--e-sum-peso)] [font-variation-settings:var(--e-sum-ejes)]",
  cuerpo: "font-(family-name:--e-cuerpo-familia) text-(length:--e-cuerpo-tamano) leading-(--e-cuerpo-interlineado)",
  cita: "font-(family-name:--e-cita-familia) [font-style:var(--e-cita-estilo)] [font-variation-settings:var(--e-sum-ejes)]",
  enlace:
    "text-(--e-enlace) underline underline-offset-[3px] transition-colors duration-300 hover:text-(--e-enlace-hover)",
  /** un dato que es enlace: secundario en reposo, la tinta de hover al pasar */
  accion: "transition-colors duration-300 hover:text-(--e-enlace-hover)",
} as const;
