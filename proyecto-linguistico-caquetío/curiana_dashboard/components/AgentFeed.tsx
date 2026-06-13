"use client";

import type { AgentResponse } from "@/lib/supabase";

interface Props {
  responses: AgentResponse[];
}

const TIER_LABEL: Record<number, string> = {
  1: "Cacique/Chamán",
  2: "Adulto",
  3: "Joven/Niño",
};

function ScoreBar({ score }: { score: number }) {
  const filled = Math.round(score);
  return (
    <span className="font-mono text-xs tracking-tighter">
      <span style={{ color: "#C47A2B" }}>{"●".repeat(filled)}</span>
      <span style={{ color: "#4A3520" }}>{"○".repeat(10 - filled)}</span>
      <span className="ml-1" style={{ color: "#9C8A6E" }}>
        {score.toFixed(1)}
      </span>
    </span>
  );
}

function LangBar({ response }: { response: AgentResponse }) {
  const langs = [
    { label: "C", pct: response.pct_caquetio,   color: "#C47A2B", title: "Caquetío" },
    { label: "W", pct: response.pct_wayunaiki,  color: "#2E7D4F", title: "Wayunaiki" },
    { label: "L", pct: response.pct_lokono,     color: "#5B4FCF", title: "Lokono" },
    { label: "T", pct: response.pct_taino,      color: "#B04040", title: "Taíno" },
    { label: "A", pct: response.pct_arahuacano, color: "#6D8A9E", title: "Arahuacano" },
  ].filter((l) => l.pct > 0);

  return (
    <div className="flex gap-1 mt-1 flex-wrap">
      {langs.map((l) => (
        <span
          key={l.label}
          title={`${l.title}: ${(l.pct * 100).toFixed(0)}%`}
          className="text-xs px-1.5 py-0.5 rounded font-mono"
          style={{ background: l.color + "33", color: l.color, border: `1px solid ${l.color}55` }}
        >
          {l.label} {(l.pct * 100).toFixed(0)}%
        </span>
      ))}
    </div>
  );
}

export default function AgentFeed({ responses }: Props) {
  if (responses.length === 0) {
    return (
      <div
        className="text-sm py-8 text-center rounded"
        style={{ color: "#9C8A6E", border: "1px solid #4A3520" }}
      >
        Esperando respuestas de los agentes...
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3 max-h-[520px] overflow-y-auto pr-1">
      {responses.map((r) => (
        <div
          key={r.id}
          className="rounded-lg p-4"
          style={{ background: "#2A1F14", border: "1px solid #4A3520" }}
        >
          {/* Header */}
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <span className="font-bold text-sm" style={{ color: "#C47A2B" }}>
                {r.agent_name}
              </span>
              <span
                className="text-xs px-1.5 py-0.5 rounded"
                style={{ background: "#4A352055", color: "#9C8A6E" }}
              >
                T{r.tier} · {TIER_LABEL[r.tier] ?? "Agente"}
              </span>
              <span className="text-xs" style={{ color: "#9C8A6E" }}>
                {r.ethnicity}
              </span>
            </div>
            <ScoreBar score={r.score} />
          </div>

          {/* Texto de la respuesta */}
          <p className="text-sm leading-relaxed" style={{ color: "#F5EDD6" }}>
            {r.response_text}
          </p>

          {/* Composición lingüística */}
          <LangBar response={r} />

          {/* Footer: neologismos + aspectos */}
          <div className="flex items-center gap-3 mt-2 text-xs" style={{ color: "#9C8A6E" }}>
            {r.neologisms_proposed > 0 && (
              <span style={{ color: "#C47A2B" }}>
                ✦ {r.neologisms_proposed} neologismo{r.neologisms_proposed > 1 ? "s" : ""}
              </span>
            )}
            {r.aspects_used?.length > 0 && (
              <span>aspectos: {r.aspects_used.join(", ")}</span>
            )}
            {r.words_used?.length > 0 && (
              <span>{r.words_used.length} palabras reconocidas</span>
            )}
            {r.langsmith_trace_url && (
              <a
                href={r.langsmith_trace_url}
                target="_blank"
                rel="noopener noreferrer"
                className="ml-auto hover:underline"
                style={{ color: "#6D8A9E" }}
              >
                LangSmith ↗
              </a>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
