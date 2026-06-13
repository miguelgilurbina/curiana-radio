"use client";

import { useEffect, useState, useCallback } from "react";
import { supabase } from "@/lib/supabase";
import type {
  SimulationRun,
  AgentResponse,
  LanguageDriftRow,
  Neologism,
} from "@/lib/supabase";
import LanguageDriftChart from "@/components/LanguageDriftChart";
import AgentFeed from "@/components/AgentFeed";

// ── Stat card ─────────────────────────────────────────────────────────
function StatCard({
  label,
  value,
  sub,
  color = "#C47A2B",
}: {
  label: string;
  value: string | number;
  sub?: string;
  color?: string;
}) {
  return (
    <div
      className="rounded-lg p-4"
      style={{ background: "#2A1F14", border: "1px solid #4A3520" }}
    >
      <div className="text-xs mb-1" style={{ color: "#9C8A6E" }}>
        {label}
      </div>
      <div className="text-2xl font-bold" style={{ color }}>
        {value}
      </div>
      {sub && (
        <div className="text-xs mt-1" style={{ color: "#9C8A6E" }}>
          {sub}
        </div>
      )}
    </div>
  );
}

// ── Neologism badge ───────────────────────────────────────────────────
function NeoTag({ neo }: { neo: Neologism }) {
  const statusColors: Record<string, string> = {
    propuesto: "#6D8A9E",
    adoptado: "#2E7D4F",
    rechazado: "#B04040",
    ignorado: "#4A3520",
  };
  return (
    <div
      className="rounded p-2 text-xs"
      style={{ background: "#2A1F14", border: `1px solid ${statusColors[neo.status]}44` }}
    >
      <span className="font-bold" style={{ color: "#C47A2B" }}>
        [{neo.form}]
      </span>
      <span className="ml-1" style={{ color: "#F5EDD6" }}>
        = {neo.meaning}
      </span>
      <div style={{ color: "#9C8A6E" }} className="mt-0.5">
        {neo.components} · por {neo.proposed_by} (día {neo.proposed_day})
      </div>
      <span
        className="inline-block mt-1 px-1.5 py-0.5 rounded text-xs"
        style={{
          background: statusColors[neo.status] + "22",
          color: statusColors[neo.status],
        }}
      >
        {neo.status}
      </span>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════════════
// PÁGINA PRINCIPAL
// ══════════════════════════════════════════════════════════════════════

export default function DashboardPage() {
  const [run, setRun] = useState<SimulationRun | null>(null);
  const [driftData, setDriftData] = useState<LanguageDriftRow[]>([]);
  const [responses, setResponses] = useState<AgentResponse[]>([]);
  const [neologisms, setNeologisms] = useState<Neologism[]>([]);
  const [loading, setLoading] = useState(true);
  const [liveStatus, setLiveStatus] = useState<"connecting" | "live" | "off">(
    "connecting"
  );

  // ── Cargar datos del run más reciente ────────────────────────────
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

    // Deriva lingüística (vista)
    const { data: drift } = await supabase
      .from("language_drift_by_turn")
      .select("*")
      .eq("run_id", latestRun.id)
      .order("day")
      .order("turn_num");
    setDriftData((drift as LanguageDriftRow[]) ?? []);

    // Últimas 30 respuestas
    const { data: resp } = await supabase
      .from("agent_responses")
      .select("*")
      .eq("run_id", latestRun.id)
      .order("created_at", { ascending: false })
      .limit(30);
    setResponses((resp as AgentResponse[]) ?? []);

    // Neologismos
    const { data: neos } = await supabase
      .from("neologisms")
      .select("*")
      .eq("run_id", latestRun.id)
      .order("proposed_day", { ascending: false })
      .limit(20);
    setNeologisms((neos as Neologism[]) ?? []);

    setLoading(false);
  }, []);

  // ── Real-time subscriptions ───────────────────────────────────────
  useEffect(() => {
    loadRun();

    const channel = supabase
      .channel("curiana-realtime")
      // Nuevas respuestas de agentes
      .on(
        "postgres_changes",
        { event: "INSERT", schema: "public", table: "agent_responses" },
        (payload) => {
          const newResp = payload.new as AgentResponse;
          setResponses((prev) => [newResp, ...prev].slice(0, 30));
        }
      )
      // Nuevos neologismos
      .on(
        "postgres_changes",
        { event: "INSERT", schema: "public", table: "neologisms" },
        (payload) => {
          setNeologisms((prev) => [payload.new as Neologism, ...prev].slice(0, 20));
        }
      )
      // Actualización de neologismos (status change)
      .on(
        "postgres_changes",
        { event: "UPDATE", schema: "public", table: "neologisms" },
        (payload) => {
          setNeologisms((prev) =>
            prev.map((n) => (n.id === payload.new.id ? (payload.new as Neologism) : n))
          );
        }
      )
      // Nuevos turnos → refrescar drift
      .on(
        "postgres_changes",
        { event: "INSERT", schema: "public", table: "turns" },
        async () => {
          if (!run) return;
          const { data } = await supabase
            .from("language_drift_by_turn")
            .select("*")
            .eq("run_id", run.id)
            .order("day")
            .order("turn_num");
          setDriftData((data as LanguageDriftRow[]) ?? []);
        }
      )
      .subscribe((status) => {
        setLiveStatus(status === "SUBSCRIBED" ? "live" : "connecting");
      });

    return () => {
      supabase.removeChannel(channel);
    };
  }, [loadRun, run]);

  // ── Stats derivadas ───────────────────────────────────────────────
  const avgScore =
    responses.length > 0
      ? (responses.reduce((s, r) => s + r.score, 0) / responses.length).toFixed(2)
      : "—";

  const avgCaquetio =
    driftData.length > 0
      ? (
          (driftData.at(-1)?.avg_caquetio ?? 0) * 100
        ).toFixed(0) + "%"
      : "—";

  const adoptedNeos = neologisms.filter((n) => n.status === "adoptado").length;

  // ── Render ────────────────────────────────────────────────────────
  if (loading) {
    return (
      <div
        className="flex items-center justify-center h-64 text-lg"
        style={{ color: "#9C8A6E" }}
      >
        Cargando datos de la simulación...
      </div>
    );
  }

  if (!run) {
    return (
      <div className="text-center py-16" style={{ color: "#9C8A6E" }}>
        <p className="text-xl mb-4" style={{ color: "#C47A2B" }}>
          ◈ Sin simulaciones aún
        </p>
        <p className="text-sm">
          Corre{" "}
          <code
            className="px-2 py-1 rounded text-xs"
            style={{ background: "#2A1F14", color: "#F5EDD6" }}
          >
            python curiana_orchestrator_v2.py --auto 10
          </code>{" "}
          para iniciar la primera simulación.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold" style={{ color: "#C47A2B" }}>
            Emergencia Lingüística Caquetía
          </h1>
          <p className="text-sm mt-1" style={{ color: "#9C8A6E" }}>
            Run{" "}
            <code
              className="px-1 py-0.5 rounded text-xs"
              style={{ background: "#2A1F14" }}
            >
              {run.id.slice(0, 8)}
            </code>{" "}
            · {run.model} ·{" "}
            {new Date(run.started_at).toLocaleString("es-VE", {
              dateStyle: "short",
              timeStyle: "short",
            })}
          </p>
        </div>
        <div className="flex items-center gap-2 text-xs">
          <span
            className="w-2 h-2 rounded-full"
            style={{
              background:
                liveStatus === "live"
                  ? "#2E7D4F"
                  : liveStatus === "connecting"
                  ? "#C47A2B"
                  : "#4A3520",
            }}
          />
          <span style={{ color: "#9C8A6E" }}>
            {liveStatus === "live"
              ? "En vivo"
              : liveStatus === "connecting"
              ? "Conectando..."
              : "Desconectado"}
          </span>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          label="Días simulados"
          value={run.total_days || driftData.at(-1)?.day || 0}
          sub={`${run.total_turns || 0} turnos`}
        />
        <StatCard
          label="Score promedio"
          value={avgScore}
          sub="densidad lingüística /10"
          color="#2E7D4F"
        />
        <StatCard
          label="% Caquetío (último turno)"
          value={avgCaquetio}
          sub="palabras del léxico atestiguado"
        />
        <StatCard
          label="Neologismos adoptados"
          value={adoptedNeos}
          sub={`de ${neologisms.length} propuestos`}
          color="#5B4FCF"
        />
      </div>

      {/* Chart */}
      <div
        className="rounded-lg p-5"
        style={{ background: "#2A1F14", border: "1px solid #4A3520" }}
      >
        <h2 className="text-sm font-semibold mb-4" style={{ color: "#F5EDD6" }}>
          Deriva lingüística por turno
          <span className="ml-2 font-normal text-xs" style={{ color: "#9C8A6E" }}>
            (composición de vocabulario por lengua fuente, % apilado)
          </span>
        </h2>
        <LanguageDriftChart data={driftData} />
      </div>

      {/* Feed + Neologismos */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Feed de agentes */}
        <div className="lg:col-span-2">
          <h2
            className="text-sm font-semibold mb-3"
            style={{ color: "#F5EDD6" }}
          >
            Respuestas de agentes
            <span className="ml-2 font-normal text-xs" style={{ color: "#9C8A6E" }}>
              (últimas 30, en tiempo real)
            </span>
          </h2>
          <AgentFeed responses={responses} />
        </div>

        {/* Neologismos */}
        <div>
          <h2
            className="text-sm font-semibold mb-3"
            style={{ color: "#F5EDD6" }}
          >
            Neologismos
            <span className="ml-2 font-normal text-xs" style={{ color: "#9C8A6E" }}>
              palabras inventadas
            </span>
          </h2>
          <div className="flex flex-col gap-2 max-h-[520px] overflow-y-auto">
            {neologisms.length === 0 ? (
              <div
                className="text-sm py-8 text-center rounded"
                style={{ color: "#9C8A6E", border: "1px solid #4A3520" }}
              >
                Sin neologismos aún.
              </div>
            ) : (
              neologisms.map((n) => <NeoTag key={n.id} neo={n} />)
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
