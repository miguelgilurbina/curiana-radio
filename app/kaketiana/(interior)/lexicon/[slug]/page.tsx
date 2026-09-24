import type { ReactNode } from "react";
import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import type { CitaFicha } from "@/types/fichas";
import { getFicha, getFichas, getFichasSeed, getVecinasFicha } from "@/lib/fichas";
import { CAPA } from "@/lib/sim-theme";
import { Overline } from "@/components/simulador/ui";
import { CapaSello } from "@/components/simulador/capa";

// La ficha de una palabra: se lee en diez segundos y se comparte sola. Arriba
// la voz, su glosa y cómo la sabemos; debajo, de dónde sale. Todo viene de
// content/wiki/fichas.json (export_fichas_seed.py, desde el lexicón).

interface FichaProps {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  return getFichas().map((f) => ({ slug: f.slug }));
}

export const dynamicParams = false;

function citaCorta(c: CitaFicha): string {
  return c.localizadores.length ? `${c.titulo}, ${c.localizadores.join(", ")}` : c.titulo;
}

export async function generateMetadata({ params }: FichaProps): Promise<Metadata> {
  const { slug } = await params;
  const f = getFicha(slug);
  if (!f) return { title: "No encontrado | Curiana Radio" };
  const etiqueta = CAPA[f.capa].label;
  const fuente = f.citas[0] ? ` Fuente: ${citaCorta(f.citas[0])}.` : "";
  const description = `«${f.glosa}» — voz caquetía ${etiqueta}.${fuente}`;
  return {
    title: `${f.forma} — ${f.glosa} · Kaketiana | Curiana Radio`,
    description,
    openGraph: { title: `${f.forma} — «${f.glosa}»`, description },
  };
}

/** «#41 (HB+E)» → «vía Adrián Hernández Baño y Juan Esteves», leyendo las
 *  siglas que el exportador sacó de la nota de Zavala en el vault. */
function viaSiglas(loc: string, siglas: Record<string, string>): string | null {
  const m = loc.match(/\(([A-Z+]+)\)/);
  if (!m) return null;
  const nombres = m[1].split("+").map((s) => siglas[s]).filter(Boolean);
  if (nombres.length === 0) return null;
  const lista =
    nombres.length === 1 ? nombres[0] : `${nombres.slice(0, -1).join(", ")} y ${nombres[nombres.length - 1]}`;
  return `vía ${lista}`;
}

function Fila({ titulo, children }: { titulo: string; children: ReactNode }) {
  return (
    <div className="grid gap-1 sm:grid-cols-[9.5rem_minmax(0,1fr)] sm:gap-4">
      <dt className="font-sans text-[0.7rem] font-medium uppercase tracking-[0.12em] text-(--sim-ink-faint) sm:pt-0.5">
        {titulo}
      </dt>
      <dd className="font-sans text-[0.95rem] leading-relaxed text-(--sim-ink)">{children}</dd>
    </div>
  );
}

export default async function FichaPage({ params }: FichaProps) {
  const { slug } = await params;
  const f = getFicha(slug);
  if (!f) notFound();

  const seed = getFichasSeed();
  const info = seed.capas[f.capa];
  const capa = CAPA[f.capa];
  const { anterior, siguiente } = getVecinasFicha(slug);
  const sinNada = f.citas.length === 0 && f.hermanas.length === 0 && !f.origen;

  return (
    <article className="mx-auto max-w-[680px]">
      <Link
        href="/kaketiana/lexicon"
        className="font-sans text-sm text-(--sim-ink-soft) transition-colors hover:text-(--sim-fuego)"
      >
        ← El diccionario
      </Link>

      {/* ── La voz ─────────────────────────────────────────────────── */}
      <header className="mt-6 border-t-[3px] pt-5" style={{ borderColor: capa.color }}>
        <CapaSello capa={f.capa} tamano="lg" />
        <h1 className="mt-3 break-words sim-display text-6xl font-semibold leading-none tracking-tight text-(--sim-ink) md:text-7xl">
          {f.forma}
        </h1>
        <p className="mt-4 font-serif text-2xl leading-snug text-(--sim-ink) md:text-[1.7rem]">{f.glosa}</p>
        <p className="mt-2 font-sans text-sm text-(--sim-ink-faint)">
          {f.categoria}
          {f.forma_fuente && (
            <>
              {f.categoria && <span aria-hidden="true"> · </span>}
              en la fuente, <em className="text-(--sim-ink-soft)">{f.forma_fuente}</em>
            </>
          )}
        </p>
      </header>

      {/* ── De dónde la sabemos ─────────────────────────────────────── */}
      <section className="mt-8 rounded-md border border-(--sim-rule) bg-(--sim-paper-deep) px-5 py-5">
        <Overline>De dónde la sabemos</Overline>
        <dl className="mt-4 space-y-4">
          {f.citas.length > 0 && (
            <Fila titulo={f.citas.length === 1 ? "Fuente" : "Fuentes"}>
              <ul className="space-y-1">
                {f.citas.map((c) => {
                  const via =
                    c.obra === "zavala-reyes-2015"
                      ? c.localizadores.map((l) => viaSiglas(l, seed.siglas_zavala)).find(Boolean)
                      : null;
                  return (
                    <li key={c.titulo}>
                      {c.obra && c.enlace ? (
                        <Link
                          href={`/kaketiana/bibliografia#${c.obra}`}
                          className="underline decoration-(--sim-rule) underline-offset-2 transition-colors hover:text-(--sim-fuego) hover:decoration-(--sim-fuego)"
                        >
                          {c.titulo}
                        </Link>
                      ) : (
                        <span>{c.titulo}</span>
                      )}
                      {c.localizadores.length > 0 && (
                        <span className="sim-mono text-[0.85em] text-(--sim-ink-soft)">
                          {" "}
                          · {c.localizadores.join(", ")}
                        </span>
                      )}
                      {via && <span className="text-sm text-(--sim-ink-faint)"> — {via}</span>}
                    </li>
                  );
                })}
              </ul>
            </Fila>
          )}

          {f.hermanas.length > 0 && (
            <Fila titulo={f.capa === "reconstruido" ? "Sale de" : "Hermanas que cita"}>
              {f.hermanas.map((h, i) => (
                <span key={h.lengua}>
                  {i > 0 && <span aria-hidden="true" className="text-(--sim-ink-faint)"> · </span>}
                  {h.lengua}
                  {!h.citada && (
                    <span className="text-sm text-(--sim-ink-faint)"> (un parentesco declarado sin obra)</span>
                  )}
                </span>
              ))}
            </Fila>
          )}

          {f.glosa_fuente && (
            <Fila titulo="La fuente dice">
              <span className="font-serif italic">«{f.glosa_fuente}»</span>
            </Fila>
          )}

          {f.sustituye.length > 0 && (
            <Fila titulo="Entró en lugar de">
              {f.sustituye.map((s, i) => (
                <span key={s.forma}>
                  {i > 0 && ", "}
                  {s.ancla ? (
                    <Link
                      href={`/kaketiana/lexicon/retiradas#${s.ancla}`}
                      className="sim-display font-semibold text-(--sim-ink-soft) line-through decoration-(--sim-ink-faint) transition-colors hover:text-(--sim-fuego)"
                    >
                      {s.forma}
                    </Link>
                  ) : (
                    <span className="sim-display font-semibold text-(--sim-ink-soft) line-through">{s.forma}</span>
                  )}
                  {s.glosa && <span className="text-sm text-(--sim-ink-faint)"> «{s.glosa}»</span>}
                </span>
              ))}
              <span className="text-sm text-(--sim-ink-faint)">, que el proyecto retiró.</span>
            </Fila>
          )}
        </dl>

        {(f.origen || f.sin_pareja || sinNada) && (
          <p className="mt-4 border-t border-(--sim-rule) pt-3 font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
            {f.origen === "acunacion" &&
              "Acuñación de trabajo del proyecto: no cita fuente ni lengua hermana. Se usa, y se dice."}
            {f.origen === "compuesto" &&
              "Compuesto del proyecto: sus piezas tienen fuente; la palabra entera, no."}
            {!f.origen && f.sin_pareja && "Ninguna lengua hermana le da pareja."}
            {sinNada && !f.sin_pareja && "La nota del lexicón no cita ninguna obra que el proyecto tenga registrada."}
          </p>
        )}
      </section>

      {/* ── Qué quiere decir la etiqueta ────────────────────────────── */}
      {info && (
        <p className="mt-6 max-w-reading font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
          <strong className="font-semibold" style={{ color: capa.color }}>
            {capa.label.charAt(0).toUpperCase() + capa.label.slice(1)}.
          </strong>{" "}
          {info.que_es} <em>Lo incierto:</em> {info.incierto.charAt(0).toLowerCase() + info.incierto.slice(1)}{" "}
          <Link
            href={`/kaketiana/lexicon?capa=${f.capa}`}
            className="whitespace-nowrap text-(--sim-fuego) transition-colors hover:text-(--sim-rubrica)"
          >
            Ver las {capa.plural} →
          </Link>
        </p>
      )}

      {/* ── En la simulación: el hueco de la corrida base ──────────── */}
      <section className="mt-8 rounded-md border border-dashed border-(--sim-rule) px-5 py-4">
        <Overline>En la simulación</Overline>
        <p className="mt-2 font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
          Pendiente de la corrida base
          {seed.pendiente_de_la_corrida_base.length > 0 && (
            <>: {seed.pendiente_de_la_corrida_base.join("; ")}.</>
          )}
        </p>
      </section>

      <nav className="mt-12 flex items-start justify-between gap-6 border-t border-(--sim-rule) pt-6 font-sans text-sm">
        {anterior ? (
          <Link
            href={`/kaketiana/lexicon/${anterior.slug}`}
            className="max-w-[45%] text-(--sim-ink-soft) transition-colors hover:text-(--sim-fuego)"
          >
            ← <span className="sim-display font-semibold">{anterior.forma}</span>
          </Link>
        ) : (
          <span />
        )}
        {siguiente && (
          <Link
            href={`/kaketiana/lexicon/${siguiente.slug}`}
            className="max-w-[45%] text-right text-(--sim-ink-soft) transition-colors hover:text-(--sim-fuego)"
          >
            <span className="sim-display font-semibold">{siguiente.forma}</span> →
          </Link>
        )}
      </nav>
    </article>
  );
}
