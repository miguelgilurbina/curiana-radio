import { ETIQUETA_LICENCIA, type TipoLicencia } from "@/types/galeria";

const ESTILO: Record<TipoLicencia, string> = {
  "cc-by-nc": "bg-earth-100 text-earth-800 border-earth-300",
  editorial: "bg-deep-100 text-deep-800 border-deep-300",
  comercial: "bg-frequency/10 text-frequency border-frequency/40",
  reservado: "bg-deep-900 text-earth-100 border-deep-900",
};

interface LicenciaBadgeProps {
  tipo: TipoLicencia;
  className?: string;
}

export default function LicenciaBadge({
  tipo,
  className = "",
}: LicenciaBadgeProps) {
  return (
    <span
      className={`inline-flex items-center border px-2 py-0.5 font-sans text-[0.65rem] tracking-[0.15em] uppercase ${ESTILO[tipo]} ${className}`}
    >
      {ETIQUETA_LICENCIA[tipo]}
    </span>
  );
}
