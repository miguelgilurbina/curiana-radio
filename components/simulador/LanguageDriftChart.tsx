"use client";

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import type { LanguageDriftRow } from "@/lib/supabase";
import { LANGS } from "@/components/simulador/ui";

interface Props {
  data: LanguageDriftRow[];
}

const SERIES = [
  { key: "avg_caquetio", lang: LANGS[0] },
  { key: "avg_wayunaiki", lang: LANGS[1] },
  { key: "avg_lokono", lang: LANGS[2] },
  { key: "avg_taino", lang: LANGS[3] },
  { key: "avg_proto_arahuaco", lang: LANGS[4] },
];

export default function LanguageDriftChart({ data }: Props) {
  const chartData = data.map((row) => ({
    label: `D${row.day}·T${row.turn_num}`,
    avg_caquetio: +(row.avg_caquetio * 100).toFixed(1),
    avg_wayunaiki: +(row.avg_wayunaiki * 100).toFixed(1),
    avg_lokono: +(row.avg_lokono * 100).toFixed(1),
    avg_taino: +(row.avg_taino * 100).toFixed(1),
    avg_proto_arahuaco: +(row.avg_proto_arahuaco * 100).toFixed(1),
  }));

  if (chartData.length === 0) {
    return (
      <div className="flex h-64 items-center justify-center rounded-xl border border-dashed border-earth-300 font-sans text-sm text-earth-500">
        Sin datos aún — la deriva aparecerá cuando corra la simulación.
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <AreaChart data={chartData} margin={{ top: 8, right: 8, left: -12, bottom: 0 }}>
        <defs>
          {SERIES.map(({ key, lang }) => (
            <linearGradient key={key} id={`g-${key}`} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={lang.color} stopOpacity={0.45} />
              <stop offset="100%" stopColor={lang.color} stopOpacity={0.06} />
            </linearGradient>
          ))}
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="#dcd2c3" vertical={false} />
        <XAxis
          dataKey="label"
          tick={{ fill: "#8a6c57", fontSize: 11, fontFamily: "Inter, sans-serif" }}
          tickLine={false}
          axisLine={{ stroke: "#dcd2c3" }}
          interval="preserveStartEnd"
        />
        <YAxis
          tickFormatter={(v) => `${v}%`}
          tick={{ fill: "#8a6c57", fontSize: 11, fontFamily: "Inter, sans-serif" }}
          tickLine={false}
          axisLine={false}
          domain={[0, 100]}
          width={42}
        />
        <Tooltip
          formatter={(value: number, name: string) => [`${value}%`, name]}
          contentStyle={{
            background: "#fffdf9",
            border: "1px solid #dcd2c3",
            borderRadius: 12,
            boxShadow: "0 8px 24px rgba(79,62,53,0.12)",
            fontFamily: "Inter, sans-serif",
            fontSize: 12,
          }}
          labelStyle={{ color: "#2f425b", fontWeight: 600, marginBottom: 4 }}
          cursor={{ stroke: "#c5b59f", strokeWidth: 1 }}
        />
        {SERIES.map(({ key, lang }) => (
          <Area
            key={key}
            type="monotone"
            dataKey={key}
            name={lang.label}
            stackId="langs"
            stroke={lang.color}
            strokeWidth={2}
            fill={`url(#g-${key})`}
            dot={false}
            activeDot={{ r: 3, strokeWidth: 0 }}
          />
        ))}
      </AreaChart>
    </ResponsiveContainer>
  );
}
