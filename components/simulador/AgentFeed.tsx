"use client";

import type { AgentResponse } from "@/lib/supabase";
import { Card, ScoreGauge, LangPill, LANGS } from "@/components/simulador/ui";

interface Props {
  responses: AgentResponse[];
}

const TIER_LABEL: Record<number, string> = {
  1: "Cacique / Piache",
  2: "Adulto",
  3: "Joven",
};

const LANG_BY_KEY = Object.fromEntries(LANGS.map((l) => [l.key, l]));

function Composition({ response }: { response: AgentResponse }) {
  const parts = [
    { key: "caquetío", pct: response.pct_caquetio },
    { key: "wayunaiki", pct: response.pct_wayunaiki },
    { key: "lokono", pct: response.pct_lokono },
    { key: "taíno", pct: response.pct_taino },
    { key: "arahuacano", pct: response.pct_arahuacano },
  ].filter((p) => p.pct > 0);
  if (parts.length === 0) return null;
  return (
    <div className="mt-3 flex flex-wrap gap-1.5">
      {parts.map((p) => {
        const lang = LANG_BY_KEY[p.key];
        return (
          <LangPill key={p.key} color={lang.color}>
            {lang.label} {(p.pct * 100).toFixed(0)}%
          </LangPill>
        );
      })}
    </div>
  );
}

export default function AgentFeed({ responses }: Props) {
  if (responses.length === 0) {
    return (
      <div className="flex h-40 items-center justify-center rounded-xl border border-dashed border-earth-300 font-sans text-sm text-earth-500">
        Esperando las primeras voces de la Curiana…
      </div>
    );
  }

  return (
    <div className="flex max-h-[560px] flex-col gap-3 overflow-y-auto pr-1">
      {responses.map((r) => (
        <Card key={r.id} className="p-4 transition-shadow hover:shadow-md">
          <div className="flex items-start justify-between gap-3">
            <div className="min-w-0">
              <div className="flex flex-wrap items-center gap-2">
                <span className="font-serif text-base font-semibold text-deep-900">{r.agent_name}</span>
                <span className="rounded-full bg-earth-100 px-2 py-0.5 font-sans text-[0.7rem] text-earth-600">
                  {TIER_LABEL[r.tier] ?? "Agente"}
                </span>
                <span className="font-sans text-[0.7rem] uppercase tracking-wide text-earth-500">{r.ethnicity}</span>
              </div>
            </div>
            <ScoreGauge score={r.score} />
          </div>

          <p className="mt-2.5 font-serif text-[0.95rem] leading-relaxed text-deep-800">
            {r.response_text}
          </p>

          <Composition response={r} />

          {(r.neologisms_proposed > 0 || (r.aspects_used?.length ?? 0) > 0 || (r.words_used?.length ?? 0) > 0) && (
            <div className="mt-3 flex flex-wrap items-center gap-x-3 gap-y-1 border-t border-earth-200/70 pt-2.5 font-sans text-xs text-earth-500">
              {r.neologisms_proposed > 0 && (
                <span className="font-medium text-frequency">
                  ✦ {r.neologisms_proposed} neologismo{r.neologisms_proposed > 1 ? "s" : ""}
                </span>
              )}
              {r.aspects_used?.length > 0 && <span>aspectos: {r.aspects_used.join(", ")}</span>}
              {r.words_used?.length > 0 && <span>{r.words_used.length} palabras caquetías</span>}
            </div>
          )}
        </Card>
      ))}
    </div>
  );
}
