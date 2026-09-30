// La etiqueta epistémica del manual de Kaketiana (design_handoff_kaketiana):
// la certeza es la solidez del trazo. Una sola regla en todo el sitio — en
// prosa se abrevia, en tabla es la última columna, en imagen va dentro del
// marco. En la duda, el dato se degrada a la más débil.
export type Grado = "atest" | "rec" | "hip" | "retro" | "canon";

const GRADOS: Record<Grado, { glifo: string; largo: string; corto: string; clase: string }> = {
  atest: { glifo: "▮", largo: "atestiguado", corto: "atest.", clase: "kk-ep-a" },
  rec: { glifo: "◆", largo: "reconstruido", corto: "rec.", clase: "kk-ep-r" },
  hip: { glifo: "◇", largo: "hipotético", corto: "hip.", clase: "kk-ep-h" },
  retro: { glifo: "~", largo: "retro-abstraído", corto: "retro.", clase: "kk-ep-x" },
  // Sólo en el experimento: lo que dijo la simulación es ficción declarada.
  canon: { glifo: "◉", largo: "canon-simulación", corto: "canon", clase: "kk-ep-c" },
};

export default function Etiqueta({
  grado,
  corta = false,
  className = "",
  style,
}: {
  grado: Grado;
  /** La variante pequeña, para usar en línea o en una celda. */
  corta?: boolean;
  className?: string;
  style?: React.CSSProperties;
}) {
  const g = GRADOS[grado];
  return (
    <span
      className={`kk-ep ${g.clase} ${corta ? "kk-ep-s" : ""} ${className}`}
      style={style}
      title={g.largo}
    >
      <span aria-hidden="true">{g.glifo}</span>
      {corta ? g.corto : g.largo}
    </span>
  );
}
