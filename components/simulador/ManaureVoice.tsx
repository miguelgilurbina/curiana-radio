import { MDXRemote } from "next-mdx-remote/rsc";
import type { ManaureFragment, TipoVoz } from "@/lib/manaure";

// Las dos voces de la wiki narrativa: el narrador (3ª persona, sobrio, sans)
// abre el marco; Manaure (1ª persona, Lora grande) habla desde su mundo.
// La honestidad metodológica vive en el badge, fuera del flujo narrativo.
const TIPO_LABEL: Record<TipoVoz, string> = {
  reconstruido: "voz reconstruida",
  hipotetico: "voz hipotética",
  imaginado: "voz imaginada",
};

const mdxComponents = {
  p: ({ children }: { children?: React.ReactNode }) => (
    <p className="mt-5 first:mt-0">{children}</p>
  ),
};

export default function ManaureVoice({
  fragment,
  variant = "inline",
}: {
  fragment: ManaureFragment;
  variant?: "hero" | "inline";
}) {
  const hero = variant === "hero";

  return (
    <figure className={hero ? "my-10 md:my-14" : "my-10 border-l-[3px] border-(--sim-fuego)/70 pl-5 md:pl-7"}>
      {fragment.narrador && (
        <p
          className={`max-w-reading font-sans leading-relaxed text-(--sim-ink-soft) ${
            hero ? "text-sm md:text-base" : "text-sm"
          }`}
        >
          {fragment.narrador}
        </p>
      )}

      <blockquote className={fragment.narrador ? "mt-6 md:mt-8" : ""}>
        {fragment.caquetio && (
          <p className={`font-serif italic text-(--sim-fuego) ${hero ? "text-2xl md:text-3xl" : "text-xl md:text-2xl"}`}>
            {fragment.caquetio}
          </p>
        )}
        {fragment.traduccion && (
          <p className="mt-1.5 font-sans text-sm text-(--sim-ink-faint)">{fragment.traduccion}</p>
        )}

        <div
          className={`font-serif leading-relaxed text-(--sim-ink) ${
            hero ? "sim-capitular mt-6 text-xl md:text-2xl" : "mt-5 text-lg md:text-xl"
          } ${fragment.caquetio ? "" : "mt-0"}`}
        >
          <MDXRemote source={fragment.body} components={mdxComponents} />
        </div>
      </blockquote>

      <figcaption className="mt-5 flex flex-wrap items-center gap-2 font-sans text-xs text-(--sim-ink-faint)">
        <span className="inline-flex items-center rounded-full border border-(--sim-rule) bg-(--sim-paper-deep) px-2 py-0.5 font-medium tracking-wide text-(--sim-ink-soft)">
          {TIPO_LABEL[fragment.tipo]}
        </span>
        {fragment.contexto && <span>{fragment.contexto}</span>}
      </figcaption>
    </figure>
  );
}
