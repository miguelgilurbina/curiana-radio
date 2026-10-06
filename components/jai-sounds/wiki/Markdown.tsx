import type { ReactNode } from "react";

/**
 * El markdown de las reseñas, en lo poco que una reseña usa: párrafos,
 * `> cita`, *itálica*, **negrita** y [enlaces](https://…). Arma elementos de
 * React, nunca HTML crudo: el texto viene de una nota y no se confía en él.
 */
function enLinea(texto: string, clave: string): ReactNode[] {
  const partes = texto.split(/(\*\*[^*]+\*\*|\*[^*]+\*|\[[^\]]+\]\(https?:\/\/[^)\s]+\))/g);
  return partes.map((x, i) => {
    const k = `${clave}-${i}`;
    if (x.startsWith("**") && x.endsWith("**")) return <strong key={k} className="font-bold">{x.slice(2, -2)}</strong>;
    if (x.startsWith("*") && x.endsWith("*") && x.length > 2) return <em key={k}>{x.slice(1, -1)}</em>;
    const enlace = x.match(/^\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)$/);
    if (enlace) {
      return (
        <a key={k} href={enlace[2]} target="_blank" rel="noopener noreferrer" className="border-b border-(--jai-rule) transition-colors duration-300 hover:border-(--jai-senal)">
          {enlace[1]}
        </a>
      );
    }
    return x;
  });
}

export default function Markdown({ texto, tam = "pagina" }: { texto: string; tam?: "pagina" | "ficha" }) {
  const cuerpo = tam === "ficha" ? "text-xl leading-[1.45]" : "text-[clamp(19px,1.9vw,22px)] leading-[1.55]";
  const cita = tam === "ficha" ? "text-[22px] leading-[1.35]" : "text-[clamp(22px,2.3vw,26px)] leading-[1.35]";
  return (
    <>
      {texto
        .trim()
        .split(/\n\s*\n/)
        .map((p, i) =>
          p.startsWith(">") ? (
            <blockquote key={i} className={`jai-manifiesto my-1.5 border-l-3 border-(--jai-luz) pl-[18px] font-extrabold text-(--jai-luz) ${cita}`}>
              {enLinea(p.replace(/^>\s?/gm, "").replace(/\n/g, " "), `c${i}`)}
            </blockquote>
          ) : (
            <p key={i} className={`jai-manifiesto m-0 text-(--jai-luz) ${cuerpo}`}>
              {enLinea(p.replace(/\n/g, " "), `p${i}`)}
            </p>
          )
        )}
    </>
  );
}
