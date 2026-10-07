import { GRADO_DE_CAPA, marcaDeForma, nombreDe } from "@/components/kaketiana/Etiqueta";

// La forma caquetía, como la pide el manual de Kaketiana (Vistas §03): display
// itálico en fuego (.kk-forma), con la marca del comparatista delante —el
// asterisco para lo que no está documentado, la virgulilla para lo que viene
// del habla viva—. Lo atestiguado va limpio. El título dice la capa entera.
export default function FormaCaquetia({
  forma,
  capa,
  className = "",
}: {
  forma: string;
  /** La capa de fichas.json: atestiguado, reconstruido, hipotetico, retroabstraido. */
  capa: string | null | undefined;
  className?: string;
}) {
  const grado = capa ? GRADO_DE_CAPA[capa] : undefined;
  return (
    <span className={`kk-forma ${className}`} title={grado ? nombreDe(grado) : undefined}>
      {marcaDeForma(grado)}
      {forma}
    </span>
  );
}
