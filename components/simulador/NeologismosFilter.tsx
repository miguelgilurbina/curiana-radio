"use client";

import { useState } from "react";
import Link from "next/link";
import type { Neologismo } from "@/lib/neologismos";
import { Card, LangPill, Avatar, EmptyState } from "@/components/simulador/ui";
import { NEO_STATUS as STATUS } from "@/lib/sim-theme";

// Filtro client-side sobre datos ya cargados estáticamente -- sin Supabase,
// sin realtime. La interactividad no requiere una conexión en producción.
export default function NeologismosFilter({ neologismos }: { neologismos: Neologismo[] }) {
  const [statusFilter, setStatusFilter] = useState<"todos" | Neologismo["status"]>("todos");

  const counts = {
    total: neologismos.length,
    propuesto: neologismos.filter((n) => n.status === "propuesto").length,
    adoptado: neologismos.filter((n) => n.status === "adoptado").length,
    rechazado: neologismos.filter((n) => n.status === "rechazado").length,
  };
  const filtered = statusFilter === "todos" ? neologismos : neologismos.filter((n) => n.status === statusFilter);

  return (
    <div>
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

      {filtered.length === 0 ? (
        <EmptyState title="Sin neologismos con ese filtro" />
      ) : (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {filtered.map((n) => {
            const st = STATUS[n.status] ?? STATUS.propuesto;
            return (
              <Card key={n.id} className="flex flex-col p-4 sim-card-hover">
                <div className="flex items-start justify-between gap-2">
                  <span className="font-serif text-xl font-semibold text-frequency">{n.form}</span>
                  <LangPill color={st.color}>{st.label}</LangPill>
                </div>
                <p className="mt-2 font-sans text-sm text-deep-800">{n.meaning}</p>
                {n.components && <p className="mt-1.5 font-mono text-xs text-earth-500">{n.components}</p>}
                {n.morphological_rule && n.morphological_rule !== "desconocida" && (
                  <span className="mt-2 inline-block w-fit rounded px-1.5 py-0.5 font-sans text-xs" style={{ background: "#5B4FCF1a", color: "#5B4FCF" }}>
                    regla {n.morphological_rule}
                  </span>
                )}
                {n.destacado && (
                  <Link
                    href={`/simulador/personajes/${n.destacado.agente_slug}`}
                    className="mt-2 block rounded-lg bg-earth-100/70 p-2 font-sans text-xs text-earth-600 hover:text-frequency transition-colors"
                  >
                    ↳ apareció en una frase de <span className="font-medium">{n.destacado.agente}</span>
                  </Link>
                )}
                <div className="mt-3 flex items-center gap-2 border-t border-earth-200/70 pt-2 font-sans text-xs text-earth-500">
                  <Avatar name={n.proposed_by} size={20} />
                  <span>{n.proposed_by} · día {n.proposed_day}</span>
                </div>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}
