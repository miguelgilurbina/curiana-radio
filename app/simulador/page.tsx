import Link from "next/link";
import { getResumen } from "@/lib/resumen";
import { getAllPersonajes } from "@/lib/personajes";
import { getNeologismos } from "@/lib/neologismos";
import LanguageDriftChart from "@/components/simulador/LanguageDriftChart";
import { Card, StatCard, Overline, Avatar, EmptyState } from "@/components/simulador/ui";

export default function ResumenPage() {
  const resumen = getResumen();
  const personajes = getAllPersonajes();
  const neologismos = getNeologismos();

  const Intro = (
    <Card className="mb-8 p-6 md:p-8">
      <Overline>Qué estás viendo</Overline>
      <p className="mt-3 font-serif text-xl md:text-2xl leading-snug text-deep-900">
        Sesenta personajes del pueblo Caquetío conversan en su lengua arahuaco reconstruida.
      </p>
      <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-earth-700">
        Esto es lo que encontramos en la primera simulación curada: agentes guiados por un modelo
        de lenguaje hablan, inventan palabras y adoptan las de otros. Su{" "}
        <span className="text-deep-800 font-medium">deriva lingüística</span> —cuánto caquetío
        usan, qué neologismos arraigan— quedó medida y graficada turno a turno.
        Golfete de Coro, Venezuela · siglos XIV-XV.
      </p>
    </Card>
  );

  if (!resumen) {
    return (
      <div>
        {Intro}
        <EmptyState
          title="Aún no hay un run curado"
          hint="Corre export_resumen_seed.py tras una simulación con --perfiles."
        />
      </div>
    );
  }

  const pctCaquetio = resumen.pct_caquetio_final != null ? `${Math.round(resumen.pct_caquetio_final * 100)}%` : "—";

  const momentos = personajes
    .flatMap((p) => p.quotes.map((q) => ({ ...q, agente: p.nombre, slug: p.slug })))
    .filter((q) => q.impacto_score != null)
    .sort((a, b) => (b.impacto_score ?? 0) - (a.impacto_score ?? 0))
    .slice(0, 4);

  // dedupe por cita: misma razón que en /simulador/neologisms -- una sola
  // frase puede declarar varios neologismos a la vez.
  const vistas = new Set<string>();
  const palabrasDestacadas = neologismos
    .filter((n) => n.destacado)
    .sort((a, b) => (b.destacado!.impacto_score ?? 0) - (a.destacado!.impacto_score ?? 0))
    .filter((n) => {
      if (vistas.has(n.destacado!.quote)) return false;
      vistas.add(n.destacado!.quote);
      return true;
    })
    .slice(0, 3);

  return (
    <div>
      <div className="mb-6 flex flex-wrap items-end justify-between gap-3">
        <div>
          <Overline>Run curado</Overline>
          <div className="mt-1 font-sans text-sm text-earth-600">
            <code className="rounded bg-earth-100 px-1.5 py-0.5 text-earth-700">{resumen.run_id.slice(0, 8)}</code>
            <span className="mx-2 text-earth-300">·</span>
            {resumen.model}
            <span className="mx-2 text-earth-300">·</span>
            {new Date(resumen.started_at).toLocaleDateString("es-VE", { dateStyle: "long" })}
          </div>
        </div>
      </div>

      {Intro}

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <StatCard label="Días simulados" value={resumen.total_days ?? 0} sub={`${resumen.total_turns ?? 0} turnos`} accent="#2f425b" />
        <StatCard label="Score promedio" value={resumen.avg_score?.toFixed(2) ?? "—"} sub="densidad lingüística / 10" accent="#2E7D4F" />
        <StatCard label="% Caquetío" value={pctCaquetio} sub="último turno" accent="#C47A2B" />
        <StatCard label="Neologismos adoptados" value={resumen.total_adoptados} sub={`de ${resumen.total_neologismos} propuestos`} accent="#5B4FCF" />
      </div>

      <Card className="mt-6 p-5 md:p-6">
        <Overline>Deriva lingüística</Overline>
        <h2 className="mt-1 font-serif text-xl font-semibold text-deep-900">Composición por turno</h2>
        <div className="mt-4">
          <LanguageDriftChart data={resumen.drift} />
        </div>
      </Card>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <div className="mb-3 flex items-baseline justify-between">
            <h2 className="font-serif text-xl font-semibold text-deep-900">Momentos destacados</h2>
            <Link href="/simulador/personajes" className="font-sans text-xs text-earth-500 hover:text-frequency transition-colors">
              ver todos los personajes →
            </Link>
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            {momentos.map((m, i) => (
              <Link key={i} href={`/simulador/personajes/${m.slug}`}>
                <Card className="h-full p-4 sim-card-hover">
                  <div className="flex items-center gap-2">
                    <Avatar name={m.agente} size={28} />
                    <span className="font-sans text-sm text-earth-600">{m.agente}</span>
                  </div>
                  <p className="mt-3 font-serif text-lg italic leading-snug text-deep-900">{m.quote}</p>
                  {m.traduccion && <p className="mt-2 font-sans text-sm text-earth-600">{m.traduccion}</p>}
                </Card>
              </Link>
            ))}
          </div>
        </div>
        <div>
          <div className="mb-3 flex items-baseline justify-between">
            <h2 className="font-serif text-xl font-semibold text-deep-900">Palabras que prendieron</h2>
            <Link href="/simulador/neologisms" className="font-sans text-xs text-earth-500 hover:text-frequency transition-colors">
              ver todas →
            </Link>
          </div>
          <div className="flex flex-col gap-3">
            {palabrasDestacadas.map((n) => (
              <Card key={n.id} className="p-3.5">
                <span className="font-serif text-lg font-semibold text-frequency">{n.form}</span>
                <p className="mt-1 font-sans text-sm text-deep-800">{n.meaning}</p>
                <p className="mt-1.5 font-sans text-xs text-earth-500">
                  acuñó {n.proposed_by} · día {n.proposed_day}
                </p>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
