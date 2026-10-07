import { frauncesJai } from "./fraunces-jai";
import { SCRIPT_SEMILLA } from "@/lib/jai-rotacion";


// El layout solo fija el registro de la sección; el chrome lo arma cada
// página. Mismo patrón que /simulador: la arista es dueña de su tema.
export default function JaiSoundsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div
      data-jai-theme="dial"
      className={`${frauncesJai.variable} min-h-screen bg-(--jai-noche) text-(--jai-luz) animate-fade-in`}
    >
      {/* La semilla del dial, antes del primer pintado (lib/jai-rotacion). */}
      <script dangerouslySetInnerHTML={{ __html: SCRIPT_SEMILLA }} />
      {children}
    </div>
  );
}
