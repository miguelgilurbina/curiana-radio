// La etiqueta epistémica: cómo sabemos cada palabra. Es la marca de la casa
// y se pinta igual en todos los niveles — el índice, la ficha, el wiki, el
// archivo de voces retiradas. Desde el 2026-10-03 es la escala del manual de
// Kaketiana (components/kaketiana/Etiqueta.tsx): la certeza es la solidez del
// trazo, ▮ atestiguado · ◆ reconstruido · ◇ hipotético · ~ retro-abstraído.
// Antes eran círculos de lleno a vacío en los colores --capa-*; la idea es la
// misma —que la etiqueta no dependa sólo del color— con un solo sistema.
import Etiqueta, { GRADO_DE_CAPA, glifoDe, nombreDe } from "@/components/kaketiana/Etiqueta";
import type { CapaEpistemica } from "@/lib/sim-theme";

const TINTA: Record<string, string> = {
  atest: "text-(--sim-ink)",
  rec: "text-(--sim-fuego)",
  hip: "text-(--sim-ink-soft)",
  retro: "text-(--sim-ink-soft)",
};

/** El glifo solo, para ir en línea junto a una forma o una cifra. */
export function CapaGlifo({ capa, size = 12 }: { capa: CapaEpistemica; size?: number }) {
  const grado = GRADO_DE_CAPA[capa];
  return (
    <span
      aria-hidden="true"
      title={nombreDe(grado)}
      className={`inline-block shrink-0 leading-none ${TINTA[grado]}`}
      style={{ fontSize: size }}
    >
      {glifoDe(grado)}
    </span>
  );
}

/** El chip del manual. `lg` para la cabecera de la ficha; `sm`, abreviado. */
export function CapaSello({ capa, tamano = "sm" }: { capa: CapaEpistemica; tamano?: "sm" | "lg" }) {
  return <Etiqueta grado={GRADO_DE_CAPA[capa]} corta={tamano === "sm"} />;
}
