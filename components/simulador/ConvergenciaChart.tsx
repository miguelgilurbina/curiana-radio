"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

// Dos curvas de distancia idiolectal media por día (lectura emergente): el run
// normal y su control de ablación. La evidencia de koineización no es que la
// normal baje — es la BRECHA entre ambas. Colores: normal en violeta de
// "experimento" (--sim), ablación en arena apagada (el control, sin andamiaje).
// El chart vive en el Acto I "laboratorio" (fondo deep-900): ejes, grilla y
// tooltip están afinados para ese registro oscuro.
const COLOR_NORMAL = "#8d83e8";
const COLOR_ABLACION = "#b09880";
const COLOR_GRID = "#2f425b";
const COLOR_TICK = "#8fa0b8";

interface Props {
  normal: number[];
  ablacion: number[];
}

export default function ConvergenciaChart({ normal, ablacion }: Props) {
  const n = Math.max(normal.length, ablacion.length);
  const data = Array.from({ length: n }, (_, i) => ({
    dia: i + 1,
    normal: normal[i] != null ? +normal[i].toFixed(4) : null,
    ablacion: ablacion[i] != null ? +ablacion[i].toFixed(4) : null,
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data} margin={{ top: 8, right: 12, left: -8, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke={COLOR_GRID} vertical={false} />
        <XAxis
          dataKey="dia"
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
          width={44}
          domain={["auto", "auto"]}
          tickFormatter={(v) => v.toFixed(2)}
        />
        <Tooltip
          formatter={(value: number, name: string) => [value?.toFixed(4), name]}
          labelFormatter={(v) => `Día ${v}`}
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
        <Legend
          verticalAlign="top"
          height={28}
          wrapperStyle={{ fontFamily: "Inter, sans-serif", fontSize: 12, color: "#c3cddb" }}
        />
        <Line
          type="monotone"
          dataKey="normal"
          name="Normal (con andamiaje)"
          stroke={COLOR_NORMAL}
          strokeWidth={2.5}
          dot={false}
          activeDot={{ r: 3, strokeWidth: 0 }}
          connectNulls
        />
        <Line
          type="monotone"
          dataKey="ablacion"
          name="Ablación (control)"
          stroke={COLOR_ABLACION}
          strokeWidth={2}
          strokeDasharray="5 4"
          dot={false}
          activeDot={{ r: 3, strokeWidth: 0 }}
          connectNulls
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
