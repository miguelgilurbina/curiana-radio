"use client";

import { useEffect, useState, useCallback } from "react";
import { supabase } from "@/lib/supabase";
import type {
  SimulationRun,
  AgentResponse,
  LanguageDriftRow,
  Neologism,
} from "@/lib/supabase";
import LanguageDriftChart from "@/components/simulador/LanguageDriftChart";
import AgentFeed from "@/components/simulador/AgentFeed";
import {
  Card,
  StatCard,
  Overline,
  LiveDot,
  LangPill,
  Skeleton,
  EmptyState,
  LANGS,
} from "@/components/simulador/ui";
import { NEO_STATUS } from "@/lib/sim-theme";

// ── Tarjeta de neologismo ─────────────────────────────────────────────
function NeoCard({ neo }: { neo: Neologism }) {
  const st = NEO_STATUS[neo.status] ?? NEO_STATUS.propuesto;
  return (
    <Card className="p-3.5">
      <div className="flex items-start justify-between gap-2">
        <span className="font-serif text-lg font-semibold text-frequency">{neo.form}</span>
        <LangPill color={st.color}>{st.label}</LangPill>
      </div>
      <p className="mt-1 font-sans text-sm text-deep-800">{neo.meaning}</p>
      <p className="mt-1.5 font-sans text-xs text-earth-500">
        {neo.components} · {neo.proposed_by} (día {neo.proposed_day})
      </p>
    </Card>
  );
}

export default function DashboardPage() {
  const [run, setRun] = useState<SimulationRun | null>(null);
  const [driftData, setDriftData] = useState<LanguageDriftRow[]>([]);
  const [responses, setResponses] = useState<AgentResponse[]>([]);
  const [neologisms, setNeologisms] = useState<Neologism[]>([]);
  const [loading, setLoading] = useState(true);
  const [liveStatus, setLiveStatus] = useState<"connecting" | "live" | "off">("connecting");

  const loadRun = useCallback(async () => {
    const { data: runs } = await supabase
      .from("simulation_runs")
      .select("*")
      .order("started_at", { ascending: false })
      .limit(1);

    if (!runs || runs.length === 0) {
      setLoading(false);
      return;
    }

    const latestRun = runs[0] as SimulationRun;
    setRun(latestRun);

    const { data: drift } = await supabase
      .from("language_drift_by_turn")
      .select("*")
      .eq("run_id", latestRun.id)
      .order("day")
      .order("turn_num");
    setDriftData((drift as LanguageDriftRow[]) ?? []);

    const { data: resp } = await supabase
      .from("agent_responses")
      .select("*")
      .eq("run_id", latestRun.id)
      .order("created_at", { ascending: false })
      .limit(30);
    setResponses((resp as AgentResponse[]) ?? []);

    const { data: neos } = await supabase
      .from("neologisms")
      .select("*")
      .eq("run_id", latestRun.id)
      .order("proposed_day", { ascending: false })
      .limit(20);
    setNeologisms((neos as Neologism[]) ?? []);

    setLoading(false);
  }, []);

  useEffect(() => {
    loadRun();

    const channel = supabase
      .channel("curiana-realtime")
      .on("postgres_changes", { event: "INSERT", schema: "public", table: "agent_responses" }, (payload) => {
        setResponses((prev) => [payload.new as AgentResponse, ...prev].slice(0, 30));
      })
      .on("postgres_changes", { event: "INSERT", schema: "public", table: "neologisms" }, (payload) => {
        setNeologisms((prev) => [payload.new as Neologism, ...prev].slice(0, 20));
      })
      .on("postgres_changes", { event: "UPDATE", schema: "public", table: "neologisms" }, (payload) => {
        setNeologisms((prev) => prev.map((n) => (n.id === payload.new.id ? (payload.new as Neologism) : n)));
      })
      .on("postgres_changes", { event: "INSERT", schema: "public", table: "turns" }, async () => {
        if (!run) return;
        const { data } = await supabase
          .from("language_drift_by_turn")
          .select("*")
          .eq("run_id", run.id)
          .order("day")
          .order("turn_num");
        setDriftData((data as LanguageDriftRow[]) ?? []);
      })
      .subscribe((status) => setLiveStatus(status === "SUBSCRIBED" ? "live" : "connecting"));

    return () => {
      supabase.removeChannel(channel);
    };
  }, [loadRun, run]);

  const avgScore =
    responses.length > 0
      ? (responses.reduce((s, r) => s + r.score, 0) / responses.length).toFixed(2)
      : "—";
  const avgCaquetio =
    driftData.length > 0 ? `${((driftData.at(-1)?.avg_caquetio ?? 0) * 100).toFixed(0)}%` : "—";
  const adoptedNeos = neologisms.filter((n) => n.status === "adoptado").length;

  // ── Intro (siempre visible, da contexto al visitante) ───────────────
  const Intro = (
    <Card className="mb-8 p-6 md:p-8">
      <Overline>Qué estás viendo</Overline>
      <p className="mt-3 font-serif text-xl md:text-2xl leading-snug text-deep-900">
        Sesenta personajes del pueblo Caquetío conversan en su lengua arahuaco reconstruida.
      </p>
      <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-earth-700">
        Cada turno, agentes guiados por un modelo de lenguaje hablan, inventan palabras y adoptan
        las de otros. Su <span className="text-deep-800 font-medium">deriva lingüística</span> —cuánto
        caquetío usan, qué neologismos arraigan— se mide y se grafica aquí en tiempo real.
        Golfete de Coro, Venezuela · siglos XIV-XV.
      </p>
    </Card>
  );

  // ── Loading ─────────────────────────────────────────────────────────
  if (loading) {
    return (
      <div>
        {Intro}
        <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <Card key={i} className="p-5">
              <Skeleton className="h-3 w-20" />
              <Skeleton className="mt-3 h-8 w-16" />
            </Card>
          ))}
        </div>
        <Skeleton className="mt-6 h-72 w-full rounded-2xl" />
      </div>
    );
  }

  // ── Sin run ─────────────────────────────────────────────────────────
  if (!run) {
    return (
      <div>
        {Intro}
        <EmptyState
          title="Aún no hay ninguna simulación"
          hint={
            <>
              Cuando se ejecute el orquestador, las voces de la Curiana aparecerán aquí en vivo.
              Vuelve pronto.
            </>
          }
        />
      </div>
    );
  }

  return (
    <div>
      {/* Encabezado del run */}
      <div className="mb-6 flex flex-wrap items-end justify-between gap-3">
        <div>
          <Overline>Run en curso</Overline>
          <div className="mt-1 font-sans text-sm text-earth-600">
            <code className="rounded bg-earth-100 px-1.5 py-0.5 text-earth-700">{run.id.slice(0, 8)}</code>
            <span className="mx-2 text-earth-300">·</span>
            {run.model}
            <span className="mx-2 text-earth-300">·</span>
            {new Date(run.started_at).toLocaleString("es-VE", { dateStyle: "short", timeStyle: "short" })}
          </div>
        </div>
        <LiveDot status={liveStatus} />
      </div>

      {Intro}

      {/* Métricas */}
      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <StatCard label="Días simulados" value={run.total_days || driftData.at(-1)?.day || 0} sub={`${run.total_turns || 0} turnos`} accent="#2f425b" />
        <StatCard label="Score promedio" value={avgScore} sub="densidad lingüística / 10" accent="#2E7D4F" />
        <StatCard label="% Caquetío" value={avgCaquetio} sub="último turno" accent="#C47A2B" />
        <StatCard label="Neologismos adoptados" value={adoptedNeos} sub={`de ${neologisms.length} propuestos`} accent="#5B4FCF" />
      </div>

      {/* Chart */}
      <Card className="mt-6 p-5 md:p-6">
        <div className="mb-4 flex flex-wrap items-baseline justify-between gap-2">
          <div>
            <Overline>Deriva lingüística</Overline>
            <h2 className="mt-1 font-serif text-xl font-semibold text-deep-900">Composición por turno</h2>
          </div>
          <div className="flex flex-wrap gap-3">
            {LANGS.map((l) => (
              <span key={l.key} className="inline-flex items-center gap-1.5 font-sans text-xs text-earth-600">
                <span className="h-2.5 w-2.5 rounded-sm" style={{ background: l.color }} />
                {l.label}
              </span>
            ))}
          </div>
        </div>
        <LanguageDriftChart data={driftData} />
      </Card>

      {/* Feed + Neologismos */}
      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <div className="mb-3 flex items-baseline justify-between">
            <h2 className="font-serif text-xl font-semibold text-deep-900">Voces de la Curiana</h2>
            <Overline>últimas 30</Overline>
          </div>
          <AgentFeed responses={responses} />
        </div>
        <div>
          <div className="mb-3 flex items-baseline justify-between">
            <h2 className="font-serif text-xl font-semibold text-deep-900">Palabras nuevas</h2>
            <Overline>{neologisms.length}</Overline>
          </div>
          <div className="flex max-h-[560px] flex-col gap-3 overflow-y-auto pr-1">
            {neologisms.length === 0 ? (
              <div className="flex h-40 items-center justify-center rounded-xl border border-dashed border-earth-300 font-sans text-sm text-earth-500">
                Sin neologismos aún.
              </div>
            ) : (
              neologisms.map((n) => <NeoCard key={n.id} neo={n} />)
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
