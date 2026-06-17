"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import type { Neologism } from "@/lib/supabase";

const STATUS_COLORS: Record<string, string> = {
  propuesto: "#6D8A9E",
  adoptado:  "#2E7D4F",
  rechazado: "#B04040",
  ignorado:  "#4A3520",
};

function StatusPill({ status }: { status: string }) {
  const color = STATUS_COLORS[status] ?? "#9C8A6E";
  return (
    <span
      className="text-xs px-2 py-0.5 rounded-full"
      style={{ background: color + "22", color, border: `1px solid ${color}44` }}
    >
      {status}
    </span>
  );
}

export default function NeologismsPage() {
  const [neos, setNeos] = useState<Neologism[]>([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState("todos");

  useEffect(() => {
    // Último run
    supabase
      .from("simulation_runs")
      .select("id")
      .order("started_at", { ascending: false })
      .limit(1)
      .then(({ data: runs }) => {
        if (!runs || runs.length === 0) {
          setLoading(false);
          return;
        }
        const runId = runs[0].id;

        supabase
          .from("neologisms")
          .select("*")
          .eq("run_id", runId)
          .order("proposed_day")
          .then(({ data }) => {
            setNeos((data as Neologism[]) ?? []);
            setLoading(false);
          });

        // Real-time
        supabase
          .channel("neos-page")
          .on(
            "postgres_changes",
            { event: "*", schema: "public", table: "neologisms" },
            () => {
              supabase
                .from("neologisms")
                .select("*")
                .eq("run_id", runId)
                .order("proposed_day")
                .then(({ data }) => setNeos((data as Neologism[]) ?? []));
            }
          )
          .subscribe();
      });
  }, []);

  const filtered =
    statusFilter === "todos"
      ? neos
      : neos.filter((n) => n.status === statusFilter);

  const counts = {
    total: neos.length,
    propuesto: neos.filter((n) => n.status === "propuesto").length,
    adoptado:  neos.filter((n) => n.status === "adoptado").length,
    rechazado: neos.filter((n) => n.status === "rechazado").length,
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold" style={{ color: "#C47A2B" }}>
          Neologismos
        </h1>
        <p className="text-sm mt-1" style={{ color: "#9C8A6E" }}>
          Palabras inventadas durante la simulación
        </p>
      </div>

      {/* Contadores */}
      <div className="flex gap-3 flex-wrap">
        {(["todos", "propuesto", "adoptado", "rechazado"] as const).map(
          (s) => {
            const count =
              s === "todos"
                ? counts.total
                : counts[s as keyof typeof counts];
            const color = s === "todos" ? "#C47A2B" : STATUS_COLORS[s];
            return (
              <button
                key={s}
                onClick={() => setStatusFilter(s)}
                className="rounded px-3 py-2 text-sm transition-colors"
                style={{
                  background:
                    statusFilter === s ? color + "33" : "#2A1F14",
                  border: `1px solid ${statusFilter === s ? color : "#4A3520"}`,
                  color: statusFilter === s ? color : "#9C8A6E",
                  cursor: "pointer",
                }}
              >
                {s} · {count}
              </button>
            );
          }
        )}
      </div>

      {loading ? (
        <div className="text-center py-16" style={{ color: "#9C8A6E" }}>
          Cargando neologismos...
        </div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-16" style={{ color: "#9C8A6E" }}>
          {neos.length === 0
            ? "Sin neologismos aún. Los agentes los crean durante la simulación."
            : "Sin neologismos con ese filtro."}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((neo) => (
            <div
              key={neo.id}
              className="rounded-lg p-4 space-y-2"
              style={{
                background: "#2A1F14",
                border: `1px solid ${STATUS_COLORS[neo.status] + "44"}`,
              }}
            >
              {/* Forma */}
              <div className="flex items-start justify-between gap-2">
                <span className="text-xl font-bold" style={{ color: "#C47A2B" }}>
                  [{neo.form}]
                </span>
                <StatusPill status={neo.status} />
              </div>

              {/* Significado */}
              <p className="text-sm" style={{ color: "#F5EDD6" }}>
                {neo.meaning}
              </p>

              {/* Componentes */}
              {neo.components && (
                <p className="text-xs font-mono" style={{ color: "#9C8A6E" }}>
                  {neo.components}
                </p>
              )}

              {/* Regla morfológica */}
              {neo.morphological_rule && neo.morphological_rule !== "desconocida" && (
                <span
                  className="inline-block text-xs px-1.5 py-0.5 rounded"
                  style={{ background: "#5B4FCF22", color: "#5B4FCF" }}
                >
                  {neo.morphological_rule}
                </span>
              )}

              {/* Footer */}
              <div className="text-xs pt-1 border-t" style={{ color: "#9C8A6E", borderColor: "#4A3520" }}>
                Propuesto por{" "}
                <span style={{ color: "#C47A2B" }}>{neo.proposed_by}</span>
                {" "}· día {neo.proposed_day}
                {neo.adopted_by && neo.adopted_by.length > 0 && (
                  <div className="mt-0.5">
                    Adoptado por: {neo.adopted_by.join(", ")}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
