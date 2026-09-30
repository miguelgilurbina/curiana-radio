"use client";

import { useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";
import type { DiaSerie } from "@/lib/serie";

// Los dos brazos de una serie de la era 2, día a día. Mismo registro oscuro y
// mismos colores que el chart del experimento de la era 1 (ConvergenciaChart):
// el brazo con escena en violeta de «experimento», el control en arena
// discontinua. Las líneas verticales tenues son los días de Capubana del brazo
// con escena — en el control son sólo el placebo: allí no hay reunión.
const COLOR_ESCENA = "#8d83e8";
const COLOR_CONTROL = "#b09880";
const COLOR_GRID = "#2f425b";
const COLOR_TICK = "#8fa0b8";
const COLOR_CAPUBANA = "#FF6B35";

type Lectura = "emergente" | "emergente_dia" | "ventana" | "acumulada" | "brecha";

const LECTURAS: { key: Lectura; label: string; nota: string }[] = [
  {
    key: "emergente",
    label: "Lo nuevo",
    nota: "Distancia entre las maneras de hablar contando sólo las palabras nacidas en la simulación, como la mide el motor. Baja = las voces se parecen más. Es la lectura del veredicto.",
  },
  {
    key: "emergente_dia",
    label: "Lo nuevo, día por día",
    nota: "La misma distancia, con lo dicho sólo ese día. Así se ve el efecto de un día suelto: los de Capubana, con todos en el cerro, caen.",
  },
  {
    key: "ventana",
    label: "El habla del día",
    nota: "Distancia contando todo lo que se dijo ese día, también el vocabulario que la comunidad ya traía.",
  },
  {
    key: "acumulada",
    label: "Todo lo dicho",
    nota: "Distancia sobre todo lo dicho desde el día 1. Baja casi siempre por pura acumulación: no es evidencia sola.",
  },
  {
    key: "brecha",
    label: "Entre pueblos",
    nota: "Cuánto más se parecen dos personas del mismo pueblo que dos de pueblos distintos (palabras nuevas, acumulado). Sobre cero = cada pueblo habla a su manera.",
  },
];

interface Props {
  escena: DiaSerie[];
  control: DiaSerie[];
  capubana: number[];
}

export default function SerieBrazosChart({ escena, control, capubana }: Props) {
  const [lectura, setLectura] = useState<Lectura>("emergente");
  const porDia = new Map<number, { dia: number; escena: number | null; control: number | null }>();
  for (const p of escena) porDia.set(p.dia, { dia: p.dia, escena: p[lectura], control: null });
  for (const p of control) {
    const fila = porDia.get(p.dia) ?? { dia: p.dia, escena: null, control: null };
    fila.control = p[lectura];
    porDia.set(p.dia, fila);
  }
  const data = [...porDia.values()].sort((a, b) => a.dia - b.dia);
  const actual = LECTURAS.find((l) => l.key === lectura)!;

  return (
    <div>
      <div role="tablist" aria-label="Lectura de la distancia" className="flex flex-wrap gap-2">
        {LECTURAS.map((l) => (
          <button
            key={l.key}
            role="tab"
            aria-selected={l.key === lectura}
            onClick={() => setLectura(l.key)}
            className={`rounded-full px-3 py-1 font-sans text-xs transition-colors ${
              l.key === lectura
                ? "bg-(--sim-ink) text-(--sim-paper)"
                : "border border-(--sim-rule) text-(--sim-ink-soft) hover:text-(--sim-ink)"
            }`}
          >
            {l.label}
          </button>
        ))}
      </div>
      <p className="mt-3 min-h-[2.5rem] max-w-reading font-sans text-xs leading-relaxed text-(--sim-ink-soft)">
        {actual.nota}
      </p>

      <div className="mt-2 flex flex-wrap items-center gap-x-5 gap-y-1 font-sans text-xs text-(--sim-ink-soft)">
        <span className="inline-flex items-center gap-2">
          <span aria-hidden="true" className="inline-block h-0.5 w-5" style={{ background: COLOR_ESCENA }} />
          Con escena
        </span>
        <span className="inline-flex items-center gap-2">
          <span
            aria-hidden="true"
            className="inline-block h-0 w-5 border-t-2 border-dashed"
            style={{ borderColor: COLOR_CONTROL }}
          />
          Control (sin escena)
        </span>
        {capubana.length > 0 && (
          <span className="inline-flex items-center gap-2">
            <span aria-hidden="true" className="inline-block h-3 w-px" style={{ background: COLOR_CAPUBANA }} />
            Día de Capubana
          </span>
        )}
      </div>

      <div className="mt-3">
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data} margin={{ top: 8, right: 12, left: -8, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke={COLOR_GRID} vertical={false} />
            {capubana.map((d) => (
              <ReferenceLine key={d} x={d} stroke={COLOR_CAPUBANA} strokeOpacity={0.35} strokeWidth={1} />
            ))}
            {lectura === "brecha" && <ReferenceLine y={0} stroke={COLOR_TICK} strokeOpacity={0.6} />}
            <XAxis
              dataKey="dia"
              type="number"
              domain={["dataMin", "dataMax"]}
              tickFormatter={(v) => `D${v}`}
              tick={{ fill: COLOR_TICK, fontSize: 11, fontFamily: "Inter, sans-serif" }}
              tickLine={false}
              axisLine={{ stroke: COLOR_GRID }}
              interval="preserveStartEnd"
              minTickGap={24}
            />
            <YAxis
              tick={{ fill: COLOR_TICK, fontSize: 11, fontFamily: "Inter, sans-serif" }}
              tickLine={false}
              axisLine={false}
              width={50}
              domain={["auto", "auto"]}
              tickFormatter={(v: number) => v.toFixed(lectura === "brecha" ? 3 : 2).replace(".", ",")}
            />
            <Tooltip
              formatter={(value: number, name: string) => [
                value == null ? "—" : value.toFixed(4).replace(".", ","),
                name,
              ]}
              labelFormatter={(v) => `Día ${v}${capubana.includes(Number(v)) ? " · Capubana" : ""}`}
              contentStyle={{
                background: "#1f2c3e",
                border: `1px solid ${COLOR_GRID}`,
                borderRadius: 12,
                boxShadow: "0 8px 24px rgba(0,0,0,0.35)",
                fontFamily: "Inter, sans-serif",
                fontSize: 12,
              }}
              labelStyle={{ color: "#f3ead4", fontWeight: 600, marginBottom: 4 }}
              cursor={{ stroke: "#3d5777", strokeWidth: 1 }}
            />
            <Line
              type="monotone"
              dataKey="escena"
              name="Con escena"
              stroke={COLOR_ESCENA}
              strokeWidth={2.5}
              dot={false}
              activeDot={{ r: 3, strokeWidth: 0 }}
              connectNulls
            />
            <Line
              type="monotone"
              dataKey="control"
              name="Control"
              stroke={COLOR_CONTROL}
              strokeWidth={2}
              strokeDasharray="5 4"
              dot={false}
              activeDot={{ r: 3, strokeWidth: 0 }}
              connectNulls
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
