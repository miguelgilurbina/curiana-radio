// El sello de Curiana Radio para la noche (shell La Noche, SHELL.md «Sello»):
// siempre cuadrado y sin recomponer. El PNG del handoff (2048px, 450 KB) se
// sirve como WebP pre-generado en tres tamaños, como el arte de la landing.
const TAMANOS = [112, 192, 300];

export default function Sello({ tamano, className = "" }: { tamano: number; className?: string }) {
  return (
    // eslint-disable-next-line @next/next/no-img-element -- WebP pre-generados, como la galería y la landing
    <img
      src={`/marca/sello-curiana-noche-${TAMANOS.find((t) => t >= tamano * 2) ?? 300}.webp`}
      srcSet={TAMANOS.map((t) => `/marca/sello-curiana-noche-${t}.webp ${t}w`).join(", ")}
      sizes={`${tamano}px`}
      width={tamano}
      height={tamano}
      alt="Curiana Radio"
      className={`block shrink-0 ${className}`}
      style={{ width: tamano, height: tamano }}
    />
  );
}
