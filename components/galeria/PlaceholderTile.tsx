import { hashTexto } from "@/lib/mosaico";

/**
 * Tile para obras en estado "pendiente": el concepto ya existe, el render no.
 *
 * No inventa una imagen ni finge una: dibuja un degradado determinista a
 * partir del slug (misma obra = mismo degradado siempre, sin hydration
 * mismatch) y se declara pendiente en texto. Es un hueco reservado, no un
 * sustituto.
 */

const DEGRADADOS = [
  ["#4f3e35", "#b09880"], // earth-900 → earth-400
  ["#0f1621", "#4d6d94"], // deep-900 → deep-500
  ["#5f4a3f", "#ff6b35"], // earth-800 → frequency
  ["#1f2c3e", "#9d7f66"], // deep-800 → earth-500
  ["#2f425b", "#c5b59f"], // deep-700 → earth-300
] as const;

interface PlaceholderTileProps {
  slug: string;
  className?: string;
  /** En el mosaico el rótulo estorba; en la ficha grande, informa. */
  conRotulo?: boolean;
}

export default function PlaceholderTile({
  slug,
  className = "",
  conRotulo = true,
}: PlaceholderTileProps) {
  const h = hashTexto(slug);
  const [desde, hasta] = DEGRADADOS[h % DEGRADADOS.length];
  const angulo = 25 + (h % 7) * 20;

  return (
    <div
      aria-hidden="true"
      className={`relative overflow-hidden ${className}`}
      style={{
        background: `linear-gradient(${angulo}deg, ${desde}, ${hasta})`,
      }}
    >
      {/* Grano sutil: evita que el degradado se lea como una banda plana. */}
      <div
        className="absolute inset-0 opacity-20 mix-blend-overlay"
        style={{
          backgroundImage:
            "repeating-linear-gradient(90deg, rgba(255,255,255,.35) 0 1px, transparent 1px 3px)",
        }}
      />
      {conRotulo && (
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="font-sans text-[0.65rem] tracking-[0.25em] uppercase text-white/80">
            Sin render
          </span>
        </div>
      )}
    </div>
  );
}
