/**
 * SIMULADOR — Tokens de diseño (única fuente de verdad de color)
 * =============================================================
 * Cambiar un color AQUÍ se propaga a todo el simulador (chart, feed, pills,
 * tablas, badges). La paleta de marca de la radio (earth/deep/frequency) vive
 * en `app/globals.css` + `tailwind.config.ts`; este archivo cubre los colores
 * *semánticos y de datos* propios del simulador.
 *
 * Ver el manual en BRAND_MVP.md.
 */

// ── Paleta de marca (espejo de los tokens de la radio, para uso inline) ──
export const BRAND = {
  frequency: "#FF6B35",
  deep900: "#0f1621",
  deep800: "#1f2c3e",
  deep700: "#2f425b",
  deep600: "#3d5777",
  earth700: "#72584a",
  earth600: "#8a6c57",
  earth500: "#9d7f66",
  earth300: "#c5b59f",
  earth200: "#dcd2c3",
  earth100: "#ede8e1",
  earth50: "#f8f6f3",
} as const;

// ── Lenguas fuente (colores de DATOS) ─────────────────────────────────
// El orden define la pila del área-chart de deriva.
export const LANGS = [
  { key: "caquetío", label: "Caquetío", color: "#C47A2B" }, // ocre
  { key: "wayunaiki", label: "Wayunaiki", color: "#2E7D4F" }, // verde golfete
  { key: "lokono", label: "Lokono", color: "#5B4FCF" }, // violeta
  { key: "taíno", label: "Taíno", color: "#B04040" }, // siena rojo
  { key: "proto-arahuaco", label: "Proto-arahuaco", color: "#6D8A9E" }, // azul pizarra
] as const;

export const LANG_COLORS: Record<string, string> = Object.fromEntries(
  LANGS.map((l) => [l.key, l.color])
);

// ── Estados de neologismo ─────────────────────────────────────────────
export const NEO_STATUS: Record<string, { label: string; color: string }> = {
  propuesto: { label: "propuesto", color: "#6D8A9E" },
  adoptado: { label: "adoptado", color: "#2E7D4F" },
  rechazado: { label: "rechazado", color: "#B04040" },
  ignorado: { label: "ignorado", color: "#9d7f66" },
};

// ── Semánticos (feedback) ─────────────────────────────────────────────
export const SEMANTIC = {
  success: "#2E7D4F",
  warning: "#C47A2B",
  danger: "#B04040",
} as const;

// Color del score según umbral (≥7 bien · ≥5 medio · <5 bajo).
export function scoreColor(score: number): string {
  return score >= 7 ? SEMANTIC.success : score >= 5 ? SEMANTIC.warning : SEMANTIC.danger;
}
