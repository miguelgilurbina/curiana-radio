"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import type { Neologism } from "@/lib/supabase";
import { Card, Overline, LangPill, Skeleton, EmptyState } from "@/components/simulador/ui";
import { NEO_STATUS as STATUS } from "@/lib/sim-theme";

export default function NeologismsPage() {
  const [neos, setNeos] = useState<Neologism[]>([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState("todos");

  useEffect(() => {
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
        const fetchNeos = () =>
          supabase
            .from("neologisms")
            .select("*")
            .eq("run_id", runId)
            .order("proposed_day")
            .then(({ data }) => setNeos((data as Neologism[]) ?? []));
        fetchNeos().then(() => setLoading(false));
        supabase
          .channel("neos-page")
          .on("postgres_changes", { event: "*", schema: "public", table: "neologisms" }, () => fetchNeos())
          .subscribe();
      });
  }, []);

  const filtered = statusFilter === "todos" ? neos : neos.filter((n) => n.status === statusFilter);
  const counts = {
    total: neos.length,
    propuesto: neos.filter((n) => n.status === "propuesto").length,
    adoptado: neos.filter((n) => n.status === "adoptado").length,
    rechazado: neos.filter((n) => n.status === "rechazado").length,
  };

  return (
    <div>
      <header className="mb-6">
        <Overline>Léxico emergente</Overline>
        <h2 className="mt-1 font-serif text-2xl md:text-3xl font-semibold text-deep-900">Neologismos</h2>
        <p className="mt-1 font-sans text-sm text-earth-600">
          Palabras que los agentes inventan con sus propios morfemas. La comunidad las adopta cuando dos hablantes distintos las usan.
        </p>
      </header>

      <div className="mb-6 flex flex-wrap gap-2">
        {(["todos", "propuesto", "adoptado", "rechazado"] as const).map((s) => {
          const count = s === "todos" ? counts.total : counts[s as keyof typeof counts];
          const color = s === "todos" ? "#C47A2B" : STATUS[s].color;
          const active = statusFilter === s;
          return (
            <button
              key={s}
              onClick={() => setStatusFilter(s)}
              className="rounded-full border px-3 py-1.5 font-sans text-sm transition-colors"
              style={{
                background: active ? `${color}1a` : "transparent",
                borderColor: active ? color : "#dcd2c3",
                color: active ? color : "#72584a",
              }}
            >
              {s} · {count}
            </button>
          );
        })}
      </div>

      {loading ? (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <Card key={i} className="p-4">
              <Skeleton className="h-5 w-28" />
              <Skeleton className="mt-3 h-4 w-full" />
              <Skeleton className="mt-2 h-3 w-2/3" />
            </Card>
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <EmptyState
          title={neos.length === 0 ? "Sin neologismos todavía" : "Sin neologismos con ese filtro"}
          hint={neos.length === 0 ? "Los agentes los acuñan durante la simulación." : undefined}
        />
      ) : (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {filtered.map((neo) => {
            const st = STATUS[neo.status] ?? STATUS.propuesto;
            return (
              <Card key={neo.id} className="flex flex-col p-4 transition-shadow hover:shadow-md">
                <div className="flex items-start justify-between gap-2">
                  <span className="font-serif text-xl font-semibold text-frequency">{neo.form}</span>
                  <LangPill color={st.color}>{st.label}</LangPill>
                </div>
                <p className="mt-2 font-sans text-sm text-deep-800">{neo.meaning}</p>
                {neo.components && <p className="mt-1.5 font-mono text-xs text-earth-500">{neo.components}</p>}
                {neo.morphological_rule && neo.morphological_rule !== "desconocida" && (
                  <span className="mt-2 inline-block w-fit rounded px-1.5 py-0.5 font-sans text-xs" style={{ background: "#5B4FCF1a", color: "#5B4FCF" }}>
                    regla {neo.morphological_rule}
                  </span>
                )}
                <div className="mt-3 border-t border-earth-200/70 pt-2 font-sans text-xs text-earth-500">
                  Propuesto por <span className="text-earth-700">{neo.proposed_by}</span> · día {neo.proposed_day}
                  {neo.adopted_by && neo.adopted_by.length > 0 && (
                    <div className="mt-0.5">Adoptado por: {neo.adopted_by.join(", ")}</div>
                  )}
                </div>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}
