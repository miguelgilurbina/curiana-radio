"use client";

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import type { LanguageDriftRow } from "@/lib/supabase";

interface Props {
  data: LanguageDriftRow[];
}

const LANGS = [
  { key: "avg_caquetio",   label: "Caquetío",   color: "#C47A2B" },
  { key: "avg_wayunaiki",  label: "Wayunaiki",  color: "#2E7D4F" },
  { key: "avg_lokono",     label: "Lokono",     color: "#5B4FCF" },
  { key: "avg_taino",      label: "Taíno",      color: "#B04040" },
  { key: "avg_proto_arahuaco", label: "Proto-arahuaco", color: "#6D8A9E" },
];

export default function LanguageDriftChart({ data }: Props) {
  // Transformar para Recharts: porcentajes → 0–100
  const chartData = data.map((row) => ({
    label: `D${row.day}T${row.turn_num}`,
    day: row.day,
    moment: row.moment,
    season: row.season,
    avg_caquetio:   +(row.avg_caquetio   * 100).toFixed(1),
    avg_wayunaiki:  +(row.avg_wayunaiki  * 100).toFixed(1),
    avg_lokono:     +(row.avg_lokono     * 100).toFixed(1),
    avg_taino:      +(row.avg_taino      * 100).toFixed(1),
    avg_proto_arahuaco: +(row.avg_proto_arahuaco * 100).toFixed(1),
    avg_score:      row.avg_score,
  }));

  if (chartData.length === 0) {
    return (
      <div
        className="flex items-center justify-center h-48 rounded text-sm"
        style={{ background: "#2A1F14", color: "#9C8A6E", border: "1px solid #4A3520" }}
      >
        Sin datos aún. Corre la simulación para ver la deriva lingüística.
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={320}>
      <AreaChart data={chartData} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#3A2A1A" />
        <XAxis
          dataKey="label"
          tick={{ fill: "#9C8A6E", fontSize: 11 }}
          interval="preserveStartEnd"
        />
        <YAxis
          tickFormatter={(v) => `${v}%`}
          tick={{ fill: "#9C8A6E", fontSize: 11 }}
          domain={[0, 100]}
        />
        <Tooltip
          formatter={(value: number, name: string) => [`${value}%`, name]}
          contentStyle={{
            background: "#2A1F14",
            border: "1px solid #4A3520",
            color: "#F5EDD6",
          }}
          labelStyle={{ color: "#C47A2B", fontWeight: "bold" }}
        />
        <Legend wrapperStyle={{ color: "#F5EDD6", fontSize: 12 }} />
        {LANGS.map((lang) => (
          <Area
            key={lang.key}
            type="monotone"
            dataKey={lang.key}
            name={lang.label}
            stroke={lang.color}
            fill={lang.color}
            fillOpacity={0.15}
            strokeWidth={2}
            dot={false}
            stackId="langs"
          />
        ))}
      </AreaChart>
    </ResponsiveContainer>
  );
}
