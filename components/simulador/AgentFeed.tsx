"use client";

import type { AgentResponse } from "@/lib/supabase";
import { Card, ScoreGauge, LangPill, Avatar, relativeTime, LANGS } from "@/components/simulador/ui";

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
    { key: "proto-arahuaco", pct: response.pct_proto_arahuaco },
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
        <Card key={r.id} className="p-4 sim-card-hover animate-fade-in">
          <div className="flex items-start gap-3">
            <Avatar name={r.agent_name} />
            <div className="min-w-0 flex-1">
              <div className="flex items-center justify-between gap-2">
                <span className="font-serif text-base font-semibold text-deep-900">{r.agent_name}</span>
                <ScoreGauge score={r.score} width={72} />
              </div>
              <div className="mt-0.5 flex flex-wrap items-center gap-x-2 gap-y-0.5 font-sans text-[0.7rem] text-earth-500">
                <span className="rounded-full bg-earth-100 px-1.5 py-0.5 text-earth-600">{TIER_LABEL[r.tier] ?? "Agente"}</span>
                <span className="uppercase tracking-wide">{r.ethnicity}</span>
                {relativeTime(r.created_at) && (
                  <>
                    <span className="text-earth-300">·</span>
                    <span>{relativeTime(r.created_at)}</span>
                  </>
                )}
              </div>
            </div>
          </div>

          <p className="mt-3 font-serif text-[0.95rem] leading-relaxed text-deep-800">
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
